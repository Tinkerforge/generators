package internal

import (
	"crypto/hmac"
	"crypto/rand"
	"crypto/sha1"
	"encoding/binary"
	"fmt"
	"net"
	"sync"
	"sync/atomic"
	"time"
)

type BrickletError uint8

const (
	BrickletErrorSuccess BrickletError = iota
	BrickletErrorInvalidParameter
	BrickletErrorFunctionNotSupported
	BrickletErrorUnknownError
)

func (e BrickletError) Error() string {
	switch e {
	case 0:
		return "Success"
	case 1:
		return "Invalid parameter"
	case 2:
		return "Function not supported"
	case 3:
		return "Currently unused error code"
	default:
		return "Unknown Error"
	}
}

type IPConnection struct {
	//When reordering this struct, keep timeout at the top, as it needs to be 64-bit aligned for atomic operations.
	timeout               int64	
	connection            net.Conn	
	connectionState       int32	
	terminate             chan struct{}
	connReq               chan connectRequest
	disconnReq            chan chan<- struct{}
	Req                   chan Request
	CallbackReg           chan CallbackRegistration
	CallbackDereg         chan CallbackDeregistration
	connectCallbackReg    chan ConnectCallbackRegistration
	disconnectCallbackReg chan DisconnectCallbackRegistration
	enumerateCallbackReg  chan CallbackRegistration
	ipconCallbackDereg    chan IPConCallbackDeregistration	
	autoReconnect         chan bool
	autoReconnectCache    bool
	authenticateMutex     sync.Mutex
}

func NewIPConnection() IPConnection {
	ipcon := IPConnection{
		(time.Millisecond * 2500).Nanoseconds(),
		nil,
		0,
		make(chan struct{}, ChannelSize),
		make(chan connectRequest, connReqChannelSize),
		make(chan chan<- struct{}, ChannelSize),
		make(chan Request, ChannelSize),
		make(chan CallbackRegistration, ChannelSize),
		make(chan CallbackDeregistration, ChannelSize),
		make(chan ConnectCallbackRegistration, ChannelSize),
		make(chan DisconnectCallbackRegistration, ChannelSize),
		make(chan CallbackRegistration, ChannelSize),
		make(chan IPConCallbackDeregistration, ChannelSize),		
		make(chan bool, ChannelSize),
		true,
		sync.Mutex{}}

	callbackConnection := make(chan callbackConnectionState, ChannelSize)
	callback := make(chan [80]byte, ChannelSize)

	go socketThreadFn(ipcon.connection,
		&ipcon.connectionState,
		&ipcon.timeout,
		ipcon.autoReconnect,
		ipcon.terminate,
		ipcon.connReq,
		ipcon.disconnReq,
		ipcon.Req,
		callbackConnection,
		callback)

	go callbackThreadFn(
		callbackConnection,
		callback,
		ipcon.terminate,
		ipcon.CallbackReg,
		ipcon.CallbackDereg,
		ipcon.connectCallbackReg,
		ipcon.disconnectCallbackReg,
		ipcon.enumerateCallbackReg,
		ipcon.ipconCallbackDereg)

	return ipcon
}

func (ipcon *IPConnection) Close() {
	ipcon.terminate <- struct{}{} //write twice to end socket and callback thread
	ipcon.terminate <- struct{}{}

	if ipcon.connection != nil {
		ipcon.connection.Close()
	}
}

func (ipcon *IPConnection) Connect(addr string) error {
	done := make(chan error, 1)
	ipcon.connReq <- connectRequest{addr, false, done}
	return <-done
}

func (ipcon *IPConnection) Disconnect() {
	done := make(chan struct{}, 1)
	ipcon.disconnReq <- done
	<-done
}

func (ipcon *IPConnection) RegisterConnectCallback(fn func(uint8)) uint64 {
	idChan := make(chan uint64, ChannelSize)
	ipcon.connectCallbackReg <- ConnectCallbackRegistration{fn, idChan}
	return <-idChan
}

func (ipcon *IPConnection) DeregisterConnectCallback(callbackID uint64) {
	ipcon.ipconCallbackDereg <- IPConCallbackDeregistration{
		callbackID}
}

func (ipcon *IPConnection) DeregisterDisconnectCallback(callbackID uint64) {
	ipcon.ipconCallbackDereg <- IPConCallbackDeregistration{
		callbackID}
}

func (ipcon *IPConnection) DeregisterEnumerateCallback(callbackID uint64) {
	ipcon.ipconCallbackDereg <- IPConCallbackDeregistration{
		callbackID}
}

func (ipcon *IPConnection) RegisterDisconnectCallback(fn func(uint8)) uint64 {
	idChan := make(chan uint64, ChannelSize)
	ipcon.disconnectCallbackReg <- DisconnectCallbackRegistration{fn, idChan}
	return <-idChan
}

func (ipcon *IPConnection) RegisterEnumerateCallback(fn func([]byte)) uint64 {
	idChan := make(chan uint64, ChannelSize)
	ipcon.enumerateCallbackReg <- CallbackRegistration{0, 0, fn, idChan}
	return <-idChan
}

func (ipcon *IPConnection) SetTimeout(timeout time.Duration) {
	atomic.StoreInt64(&ipcon.timeout, timeout.Nanoseconds())
}

func (ipcon *IPConnection) GetTimeout() time.Duration {
	return time.Duration(atomic.LoadInt64(&ipcon.timeout))
}

func (ipcon *IPConnection) GetConnectionState() ConnectionState {
	return ConnectionState(atomic.LoadInt32(&ipcon.connectionState))
}

func (ipcon *IPConnection) SetAutoReconnect(autoReconnectEnabled bool) {
	ipcon.autoReconnect <- autoReconnectEnabled
	ipcon.autoReconnectCache = autoReconnectEnabled
}

func (ipcon *IPConnection) GetAutoReconnect() bool {
	return ipcon.autoReconnectCache
}

func (ipcon *IPConnection) Enumerate() {
	header := PacketHeader{0, 8, 254, 0, false, 0}
	payload := header.ToLeBytes()

	ipcon.Req <- Request{
		payload,
		nil,
		nil}
}

func (ipcon *IPConnection) Authenticate(secret string) error {
	ipcon.authenticateMutex.Lock()
	defer ipcon.authenticateMutex.Unlock()
	//Get server nonce
	header := PacketHeader{1, PacketHeaderSize, 1, 0, true, 0}
	payload := header.ToLeBytes()
	resp, err := ReqWithTimeout(payload, ipcon.Req)
	if err != nil {
		return fmt.Errorf("could not get server nonce: %s", err)
	}

	var respHeader PacketHeader
	respHeader.FillFromBytes(resp)
	if respHeader.ErrorCode != 0 {
		return BrickletError(respHeader.ErrorCode)
	}

	serverNonce := resp[PacketHeaderSize : PacketHeaderSize+4]

	//Create client nonce
	clientNonce := make([]byte, 4)
	_, err = rand.Read(clientNonce)
	if err != nil {
		return err
	}

	//Concat and hash
	toHash := append(serverNonce, clientNonce...)
	mac := hmac.New(sha1.New, []byte(secret))
	mac.Write(toHash)
	//Send result to authenticate
	result := mac.Sum(clientNonce)
	header = PacketHeader{1, PacketHeaderSize + uint8(len(result)), 2, 0, true, 0}
	payload = append(header.ToLeBytes(), result...)

	resp, err = ReqWithTimeout(payload, ipcon.Req)
	if err != nil {
		return fmt.Errorf("received no response before timeout, maybe the secret is wrong: %s", err)
	}
	if len(resp) > 0 {
		respHeader.FillFromBytes(resp)
		if respHeader.ErrorCode != 0 {
			return BrickletError(respHeader.ErrorCode)
		}
	}
	return nil
}

func readIntoPacketBuffer(readBuffer []byte, packetBuffer []byte, bytesToRead uint64, readBufferLevel *uint64, packetBufferLevel *uint64) {
	copy(packetBuffer[*packetBufferLevel:], readBuffer[:bytesToRead])
	copy(readBuffer[:bytesToRead], readBuffer[bytesToRead:])
	for index := range readBuffer[:uint64(len(readBuffer))-bytesToRead] {
		readBuffer[index] = readBuffer[uint64(index)+bytesToRead]
		readBuffer[uint64(index)+bytesToRead] = 0
	}

	*readBufferLevel -= bytesToRead
	*packetBufferLevel += bytesToRead
}

func removeFromPacketBuffer(bytesRead uint64, packetBuffer []byte, packetBufferLevel *uint64) {
	copy(packetBuffer[:bytesRead], packetBuffer[bytesRead:])
	for index := range packetBuffer[:uint64(len(packetBuffer))-bytesRead] {
		packetBuffer[index] = packetBuffer[uint64(index)+bytesRead]
		packetBuffer[uint64(index)+bytesRead] = 0
	}
	*packetBufferLevel -= bytesRead
}

func socketReadThreadFn(connection net.Conn, socketClosed chan<- bool, respTX chan<- [80]byte) {
	const MaxPacketSize = PacketHeaderSize + 64 + 8
	const ReadBufferSize = MaxPacketSize * 100

	var readBuffer [ReadBufferSize]byte
	var readBufferLevel uint64
	var packetBuffer [MaxPacketSize * 2]byte
	var packetBufferLevel uint64
	var packetBufferPendingBytes uint64

	for {
		if ReadBufferSize-readBufferLevel > MaxPacketSize {
			bytesRead, err := connection.Read(readBuffer[readBufferLevel:ReadBufferSize])
			if err != nil {
				if neterr, ok := err.(net.Error); !ok || !neterr.Timeout() {
					socketClosed <- false
					break
				}
			}

			if bytesRead == 0 {
				socketClosed <- true
				break
			}

			readBufferLevel += uint64(bytesRead)
		}

		for {
			//Don't have a complete header yet
			if packetBufferLevel == 0 && readBufferLevel < PacketHeaderSize {
				break
			}

			//Read header
			if packetBufferLevel == 0 {
				readIntoPacketBuffer(readBuffer[:], packetBuffer[:], PacketHeaderSize, &readBufferLevel, &packetBufferLevel)
				var header PacketHeader
				header.FillFromBytes(packetBuffer[:PacketHeaderSize])

				//removeFromPacketBuffer(PacketHeaderSize, packetBuffer[:], &packetBufferLevel)
				packetBufferPendingBytes = uint64(header.Length) - PacketHeaderSize
			}

			//Read payload
			if packetBufferPendingBytes > 0 && readBufferLevel > 0 {
				toRead := MinU(uint64(packetBufferPendingBytes), uint64(readBufferLevel))
				readIntoPacketBuffer(readBuffer[:], packetBuffer[:], toRead, &readBufferLevel, &packetBufferLevel)
				packetBufferPendingBytes -= toRead
			}

			//Packet complete
			if packetBufferPendingBytes == 0 {
				var header PacketHeader
				header.FillFromBytes(packetBuffer[:PacketHeaderSize])
				//payload := packetBuffer[PacketHeaderSize:header.Length]

				var packet [80]byte
				copy(packet[:], packetBuffer[:header.Length])
				respTX <- packet
				removeFromPacketBuffer(uint64(header.Length), packetBuffer[:], &packetBufferLevel)
			} else {
				break
			}
		}
	}
}

type responseQueueKey struct {
	uid        uint32
	functionID uint8
	seqNum     uint8
}

type callbackKey struct {
	uid        uint32
	functionID uint8
}

type connectRequest struct {
	addr        string
	isReconnect bool
	doneRx      chan<- error
}

type ConnectReason uint8

const (
	ConnectReasonRequest ConnectReason = iota
	ConnectReasonAutoReconnect
)

type DisconnectReason uint8

const (
	DisconnectReasonRequest DisconnectReason = iota
	DisconnectReasonError
	DisconnectReasonShutdown
)

type EnumerationType uint8

const (
	EnumerationTypeAvailable EnumerationType = iota
	EnumerationTypeConnected
	EnumerationTypeDisconnected
)

func callbackThreadFn(
	connectStateRX <-chan callbackConnectionState,
	callbackRX <-chan [80]byte,

	terminationRX <-chan struct{},

	callbackRegRX <-chan CallbackRegistration,
	CallbackDeregRX <-chan CallbackDeregistration,
	connectCallbackRegRX <-chan ConnectCallbackRegistration,
	disconnectCallbackRegRX <-chan DisconnectCallbackRegistration,
	enumerateCallbackRegRX <-chan CallbackRegistration,
	ipconDeregRX <-chan IPConCallbackDeregistration) {

	callbackRegistrationID := uint64(0)
	registeredCallbacks := make(map[callbackKey][]CallbackContainer)
	connectCallbacks := make([]ConnectCallbackContainer, 0)
	disconnectCallbacks := make([]DisconnectCallbackContainer, 0)
	enumerateCallbacks := make([]CallbackContainer, 0)

	for {
		select {
		case <-terminationRX:
			return
		//Notify of connect/disconnect
		case connectInfo := <-connectStateRX:
			switch connectInfo {
			case callbackConnectionStateAutoReconnect:
				for _, container := range connectCallbacks {
					container.Callback(uint8(ConnectReasonAutoReconnect))
				}
			case callbackConnectionStateConnectRequest:
				for _, container := range connectCallbacks {
					container.Callback(uint8(ConnectReasonRequest))
				}
			case callbackConnectionStateDisconnectRequest:
				for _, container := range disconnectCallbacks {
					container.Callback(uint8(DisconnectReasonRequest))
				}
			case callbackConnectionStateDisconnectError:
				for _, container := range disconnectCallbacks {
					container.Callback(uint8(DisconnectReasonError))
				}
			case callbackConnectionStateDisconnectShutdown:
				for _, container := range disconnectCallbacks {
					container.Callback(uint8(DisconnectReasonShutdown))
				}
			}
		case packet := <-callbackRX:
			var header PacketHeader
			header.FillFromBytes(packet[:])
			if header.FunctionID == 253 {
				for _, container := range enumerateCallbacks {
					go container.Callback(packet[:])
				}
			} else {
				key := callbackKey{header.UID, header.FunctionID}
				if registeredCallbacks[key] == nil {
					break
				}
				for _, container := range registeredCallbacks[key] {
					go container.Callback(packet[:])
				}
			}
		//Register a callback
		case callbackReg := <-callbackRegRX:
			{
				key := callbackKey{callbackReg.UID, callbackReg.FunctionID}
				if registeredCallbacks[key] == nil {
					registeredCallbacks[key] = make([]CallbackContainer, 0)
				}
				registeredCallbacks[key] = append(registeredCallbacks[key],
					CallbackContainer{
						callbackRegistrationID,
						callbackReg.Callback})
				callbackReg.RegIDTX <- callbackRegistrationID
				callbackRegistrationID++
			}
		//Deregister a callback
		case CallbackDereg := <-CallbackDeregRX:
			{
				key := callbackKey{CallbackDereg.UID, CallbackDereg.FunctionID}
				if registeredCallbacks[key] == nil {
					break
				}

				idxToRemove := -1
				for idx, callback := range registeredCallbacks[key] {
					if callback.RegID == CallbackDereg.CallbackID {
						idxToRemove = idx
					}
				}
				if idxToRemove == -1 {
					break
				}

				registeredCallbacks[key][idxToRemove] = registeredCallbacks[key][len(registeredCallbacks[key])-1]
				registeredCallbacks[key] = registeredCallbacks[key][:len(registeredCallbacks[key])-1]
			}
		//Register connect callback
		case connectCallback := <-connectCallbackRegRX:
			{
				connectCallbacks = append(connectCallbacks, ConnectCallbackContainer{
					callbackRegistrationID,
					connectCallback.Callback})
				connectCallback.RegIDTX <- callbackRegistrationID
				callbackRegistrationID++
			}
		//Deregister connect, disconnect or enumerate callback
		case CallbackDereg := <-ipconDeregRX:
			{
				//Search in connect callbacks
				idxToRemove := -1
				for idx, callback := range connectCallbacks {
					if callback.RegID == CallbackDereg.CallbackID {
						idxToRemove = idx
					}
				}
				if idxToRemove != -1 {
					connectCallbacks[idxToRemove] = connectCallbacks[len(connectCallbacks)-1]
					connectCallbacks = connectCallbacks[:len(connectCallbacks)-1]
					break
				}

				//Search in disconnect callbacks
				for idx, callback := range disconnectCallbacks {
					if callback.RegID == CallbackDereg.CallbackID {
						idxToRemove = idx
					}
				}
				if idxToRemove != -1 {
					disconnectCallbacks[idxToRemove] = disconnectCallbacks[len(disconnectCallbacks)-1]
					disconnectCallbacks = disconnectCallbacks[:len(disconnectCallbacks)-1]
					break
				}

				//Search in enumerate callbacks
				for idx, callback := range enumerateCallbacks {
					if callback.RegID == CallbackDereg.CallbackID {
						idxToRemove = idx
					}
				}
				if idxToRemove != -1 {
					enumerateCallbacks[idxToRemove] = enumerateCallbacks[len(enumerateCallbacks)-1]
					enumerateCallbacks = enumerateCallbacks[:len(enumerateCallbacks)-1]
					break
				}
			}

		//Register disconnect callback
		case disconnectCallback := <-disconnectCallbackRegRX:
			{
				disconnectCallbacks = append(disconnectCallbacks, DisconnectCallbackContainer{
					callbackRegistrationID,
					disconnectCallback.Callback})
				disconnectCallback.RegIDTX <- callbackRegistrationID
				callbackRegistrationID++
			}
		//Register enumerate callback
		case enumerateCallback := <-enumerateCallbackRegRX:
			{
				enumerateCallbacks = append(enumerateCallbacks, CallbackContainer{
					callbackRegistrationID,
					enumerateCallback.Callback})
				enumerateCallback.RegIDTX <- callbackRegistrationID
				callbackRegistrationID++
			}
		}
	}

}

type callbackConnectionState uint8

const (
	callbackConnectionStateAutoReconnect callbackConnectionState = iota
	callbackConnectionStateConnectRequest
	callbackConnectionStateDisconnectRequest //Don't change this order, as it must be the same as the DisconnectReason's.
	callbackConnectionStateDisconnectError
	callbackConnectionStateDisconnectShutdown
)

func socketThreadFn(connection net.Conn,
	connectionState *int32,
	timeout *int64,
	autoReconnectRX <-chan bool,
	terminationRX <-chan struct{},
	connReq chan connectRequest,
	disconnReqRX <-chan chan<- struct{},
	reqRX <-chan Request,
	connectionStateTX chan<- callbackConnectionState,
	callbackTX chan<- [80]byte) {

	var sessionID uint64
	autoReconnectAllowed := true
	autoReconnectEnabled := true
	isAutoReconnect := false
Thread:
	for {
		atomic.StoreInt32(connectionState, int32(ConnectionStateDisconnected))

		var seqNum byte = 1
		responseQueues := make(map[responseQueueKey][]chan<- []byte)
		disconnectReason := DisconnectReasonError

		var connRequest connectRequest
	WaitForConnect:
		for {
			select {
			//Terminate
			case <-terminationRX:
				break Thread
			case arEnable := <-autoReconnectRX:
				autoReconnectEnabled = arEnable
			case connRequest = <-connReq:
				if connRequest.isReconnect && (!autoReconnectAllowed || !autoReconnectEnabled) {
					continue WaitForConnect
				}
				break WaitForConnect
			case channel := <-disconnReqRX:
				autoReconnectAllowed = false
				channel <- struct{}{}
			case req := <-reqRX:
				to := time.Duration(0)
				if req.TimeoutTx != nil {
					req.TimeoutTx <- to
				}
			}
		}

		isAutoReconnect = connRequest.isReconnect

		sessionID++
		atomic.StoreInt32(connectionState, int32(ConnectionStatePending))

		connection, err := Connect(connRequest.addr)
		if err != nil {
			if connRequest.doneRx != nil {
				connRequest.doneRx <- err
			}
			connReq <- connectRequest{connRequest.addr, true, nil}
			continue Thread
		}

		responseChannel := make(chan [80]byte, 1)
		socketClosed := make(chan bool, 1)
		go socketReadThreadFn(connection, socketClosed, responseChannel)

		if connRequest.doneRx != nil {
			connRequest.doneRx <- nil
		}

		atomic.StoreInt32(connectionState, 1)
		if isAutoReconnect {
			connectionStateTX <- callbackConnectionStateAutoReconnect
		} else {
			connectionStateTX <- callbackConnectionStateConnectRequest
		}

	Connection:
		for {
			select {
			//Terminate
			case <-terminationRX:
				break Thread
			case arEnable := <-autoReconnectRX:
				autoReconnectEnabled = arEnable
			//Disconnect
			case channel := <-disconnReqRX:
				{
					connection.Close()
					disconnectReason = DisconnectReasonRequest
					channel <- struct{}{}
					break Connection
				}
			//Read thread noticed, that the socket was closed
			case wasShutdown := <-socketClosed:
				{
					if autoReconnectEnabled {
						connReq <- connectRequest{connRequest.addr, true, nil}
					}

					if wasShutdown {
						disconnectReason = DisconnectReasonShutdown
					} else {
						disconnectReason = DisconnectReasonError
					}
					break Connection
				}
			//Timeout: send Disconnect probe
			case <-time.After(5 * time.Second):
				{
					header := PacketHeader{0, 8, 128, 1, false, 0}
					deadline := time.Now().Add(time.Duration(atomic.LoadInt64(timeout)))
					connection.SetWriteDeadline(deadline)
					connection.Write(header.ToLeBytes())
				}

			//Request
			case request := <-reqRX:
				{
					request.Packet[PacketHeaderSeqNumOffset] |= seqNum << 4
					seqNum++
					if seqNum > 15 {
						seqNum = 1
					}
					if request.ResponseTx != nil {
						var header PacketHeader
						header.FillFromBytes(request.Packet[:])
						key := responseQueueKey{header.UID, header.FunctionID, header.SequenceNumber}
						if responseQueues[key] == nil {
							responseQueues[key] = make([]chan<- []byte, 0)
						}
						responseQueues[key] = append(responseQueues[key], request.ResponseTx)
					}
					to := time.Duration(atomic.LoadInt64(timeout))
					deadline := time.Now().Add(to)
					connection.SetWriteDeadline(deadline)
					if request.TimeoutTx != nil {
						request.TimeoutTx <- to
					}
					_, err := connection.Write(request.Packet)
					if err != nil {
						if neterr, ok := err.(net.Error); ok && neterr.Timeout() {
							//remove channel
							if request.ResponseTx != nil {
								var header PacketHeader
								header.FillFromBytes(request.Packet[:])
								key := responseQueueKey{header.UID, header.FunctionID, header.SequenceNumber}
								responseQueues[key] = responseQueues[key][:len(responseQueues[key])-1]
							}
						} else {
							connection.Close()
							//Connection seems to be broken, try to reconnect
							if autoReconnectEnabled {
								connReq <- connectRequest{connRequest.addr, true, nil}
							}
							disconnectReason = DisconnectReasonError
							break Connection
						}
					}
				}
			//Response
			case response := <-responseChannel:
				{
					var header PacketHeader
					header.FillFromBytes(response[:])

					if header.SequenceNumber == 0 { //Callbacks
						callbackTX <- response
					} else { //Response for getter or setter
						key := responseQueueKey{header.UID, header.FunctionID, header.SequenceNumber}
						if val, ok := responseQueues[key]; ok && len(val) > 0 {
							val[0] <- response[:]
							close(responseQueues[key][0])
							responseQueues[key] = responseQueues[key][1:]
						}
					}
				}
			}
		}
		connectionStateTX <- callbackConnectionState(uint8(callbackConnectionStateDisconnectRequest) + uint8(disconnectReason))
	}
	atomic.StoreInt32(connectionState, 0)
	connectionStateTX <- callbackConnectionStateDisconnectRequest
}

const ChannelSize uint64 = 1 << 16

// Don't change this to a value less than the expected count of threads trying to connect:
// The socket thread puts reconnect requests in the same channel (and reads from it), so
// it would deadlock itself if the channel buffer were full.
const connReqChannelSize uint64 = 1 << 16

const PacketHeaderSize = 8
const PacketHeaderSeqNumOffset = 6

type PacketHeader struct {
	UID              uint32
	Length           uint8
	FunctionID       uint8
	SequenceNumber   uint8
	ResponseExpected bool
	ErrorCode        uint8
}

func (header *PacketHeader) FillFromBytes(bytes []byte) {
	header.UID = binary.LittleEndian.Uint32(bytes)
	header.Length = bytes[4]
	header.FunctionID = bytes[5]
	header.SequenceNumber = bytes[6] >> 4
	header.ResponseExpected = bytes[6]&0x8 == 1
	header.ErrorCode = bytes[7] >> 6
}

func (header PacketHeader) ToLeBytes() []byte {
	var bytes [8]byte
	binary.LittleEndian.PutUint32(bytes[0:4], header.UID)
	bytes[4] = header.Length
	bytes[5] = header.FunctionID
	bytes[6] = header.SequenceNumber << 4
	if header.ResponseExpected {
		bytes[6] |= 1 << 3
	}
	bytes[7] = header.ErrorCode << 6
	return bytes[0:8]
}

func (header PacketHeader) bytesExpected() int {
	return PacketHeaderSize
}

type Request struct {
	Packet     []byte
	TimeoutTx  chan<- time.Duration
	ResponseTx chan<- []byte
}

func ReqWithTimeout(packet []byte, reqTX chan<- Request) ([]byte, error) {
	responseChan := make(chan []byte, ChannelSize)
	timeoutChan := make(chan time.Duration, ChannelSize)
	reqTX <- Request{packet, timeoutChan, responseChan}
	timeout := <-timeoutChan //blocks until socket thread is processing this request

	select {
	case resp := <-responseChan:
		return resp, nil
	case <-time.After(timeout):
		return nil, fmt.Errorf("request timed out")
	}
}

func Connect(addr string) (net.Conn, error) {
	conn, err := net.DialTimeout("tcp", addr, 30*time.Second)
	if err != nil {
		return nil, err
	}
	tcpConn, _ := conn.(*net.TCPConn)
	tcpConn.SetNoDelay(true)
	return conn, nil
}

type CallbackRegistration struct {
	UID        uint32
	FunctionID uint8
	Callback   func([]byte)
	RegIDTX    chan<- uint64
}

type CallbackDeregistration struct {
	UID        uint32
	FunctionID uint8
	CallbackID uint64
}

type ConnectCallbackRegistration struct {
	Callback func(uint8)
	RegIDTX  chan<- uint64
}

type DisconnectCallbackRegistration struct {
	Callback func(uint8)
	RegIDTX  chan<- uint64
}

type IPConCallbackDeregistration struct {
	CallbackID uint64
}

type CallbackContainer struct {
	RegID    uint64
	Callback func([]byte)
}

type ConnectCallbackContainer struct {
	RegID    uint64
	Callback func(uint8)
}

type DisconnectCallbackContainer struct {
	RegID    uint64
	Callback func(uint8)
}

type ConnectionState uint8

const (
	ConnectionStateDisconnected ConnectionState = iota
	ConnectionStateConnected
	ConnectionStatePending
)
