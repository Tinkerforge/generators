package internal

import (
	"fmt"
	"sync"
)

type ResponseExpectedFlag = uint8

const (
	ResponseExpectedFlagInvalidFunctionID ResponseExpectedFlag = iota
	ResponseExpectedFlagFalse
	ResponseExpectedFlagTrue
	ResponseExpectedFlagAlwaysTrue
)

type Device struct {
	apiVersion       [3]uint8
	ResponseExpected [256]ResponseExpectedFlag
	internalUID      uint32
	regTX            chan<- Request
	callbackRegTX    chan<- CallbackRegistration
	callbackDeregTX  chan<- CallbackDeregistration
	highLevelLocks   []sync.Mutex
	initialized      bool
}

func NewDevice(apiVersion [3]uint8, uid string, ipcon *IPConnection, highLevelFunctionCount uint8) (Device, error) {
	internalUID, err := Base58ToU32(uid)
	if err != nil {
		result := Device{}
		result.initialized = false
		return result, err
	}
	return Device{
		apiVersion,
		[256]ResponseExpectedFlag{},
		internalUID,
		ipcon.Req,
		ipcon.CallbackReg,
		ipcon.CallbackDereg,
		make([]sync.Mutex, highLevelFunctionCount),
		true}, nil
}

func (device *Device) GetAPIVersion() [3]uint8 {
	return device.apiVersion
}

func (device *Device) GetResponseExpected(functionID uint8) (bool, error) {
	switch device.ResponseExpected[functionID] {
	case ResponseExpectedFlagAlwaysTrue:
		return true, nil
	case ResponseExpectedFlagTrue:
		return true, nil
	case ResponseExpectedFlagFalse:
		return false, nil
	default:
		return false, fmt.Errorf("unknown function with ID %d", functionID)
	}
}

func (device *Device) SetResponseExpected(functionID uint8, responseExpected bool) error {
	switch device.ResponseExpected[functionID] {
	case ResponseExpectedFlagAlwaysTrue:
		return fmt.Errorf("response expected for function with ID %d is always true", functionID)
	case ResponseExpectedFlagInvalidFunctionID:
		return fmt.Errorf("unknown function with ID %d", functionID)
	default:
		if responseExpected {
			device.ResponseExpected[functionID] = ResponseExpectedFlagTrue
		} else {
			device.ResponseExpected[functionID] = ResponseExpectedFlagFalse
		}
	}
	return nil
}

func (device *Device) SetResponseExpectedAll(responseExpected bool) {
	for i, respExp := range device.ResponseExpected {
		if respExp == ResponseExpectedFlagTrue || respExp == ResponseExpectedFlagFalse {
			if responseExpected {
				device.ResponseExpected[i] = ResponseExpectedFlagTrue
			} else {
				device.ResponseExpected[i] = ResponseExpectedFlagFalse
			}
		}
	}
}

func (device *Device) Set(functionID uint8, payload []byte) ([]byte, error) {
	if !device.initialized {
		return nil, fmt.Errorf("device is not initialized")
	}
	responseExpected := !(device.ResponseExpected[functionID] == ResponseExpectedFlagFalse)

	if responseExpected {
		return device.Get(functionID, payload)
	}

	header := PacketHeader{
		device.internalUID,
		uint8(len(payload) + PacketHeaderSize),
		functionID,
		0,
		false,
		0}

	bytes := append(header.ToLeBytes(), payload[:]...)
	device.regTX <- Request{bytes[:], nil, nil}
	return nil, nil
}

func (device *Device) Get(functionID uint8, payload []byte) ([]byte, error) {
	if !device.initialized {
		return nil, fmt.Errorf("device is not initialized")
	}
	header := PacketHeader{
		device.internalUID,
		uint8(len(payload) + PacketHeaderSize),
		functionID,
		0,
		true,
		0}
	bytes := append(header.ToLeBytes(), payload[:]...)

	return ReqWithTimeout(bytes, device.regTX)
}

type LowLevelWriteResult struct {
	Written uint64
	Result  []byte
}

func (device *Device) SetHighLevel(lowLevelClosure func(uint64, uint64, []byte) (LowLevelWriteResult, error), highLevelFunctionIdx uint8, elementSizeInBit uint64, chunkLenInBit uint64, payload []byte) (LowLevelWriteResult, error) {
	if !device.initialized {
		return LowLevelWriteResult{}, fmt.Errorf("device is not initialized")
	}
	length := uint64(len(payload)) * 8 / elementSizeInBit
	chunkOffset := uint64(0) * 8 / elementSizeInBit

	device.highLevelLocks[highLevelFunctionIdx].Lock()
	defer device.highLevelLocks[highLevelFunctionIdx].Unlock()

	if length == 0 {
		return lowLevelClosure(length, chunkOffset, []byte{})
	}
	writtenSum := uint64(0)
	for {
		toWrite := MinU(uint64(chunkOffset+chunkLenInBit), uint64(length))
		result, err := lowLevelClosure(length, chunkOffset, payload[chunkOffset/8:toWrite/8])
		if err != nil {
			return result, err
		}
		written := result.Written * 8
		writtenSum += written
		if written < chunkLenInBit {
			result.Written = writtenSum / 8
			return result, nil
		}
		chunkOffset += chunkLenInBit
		if chunkOffset >= length {
			result.Written = length / 8
			return result, nil
		}
	}
}

type LowLevelResult struct {
	Length      uint64
	ChunkOffset uint64
	ChunkData   []byte
	Result      []byte
}

func (device *Device) GetHighLevel(lowLevelClosure func() (LowLevelResult, error), highLevelFunctionIdx uint8, elementSizeInBit uint64) ([]byte, []byte, error) {
	if !device.initialized {
		return nil, nil, fmt.Errorf("device is not initialized")
	}
	chunkOffset := uint64(0) * elementSizeInBit
	device.highLevelLocks[highLevelFunctionIdx].Lock()
	defer device.highLevelLocks[highLevelFunctionIdx].Unlock()

	result, err := lowLevelClosure()
	if err != nil {
		return nil, nil, err
	}
	outOfSync := result.ChunkOffset != 0
	messageLength := result.Length * elementSizeInBit

	if !outOfSync {
		buf := make([]byte, 0, messageLength/8)
		firstReadLen := MinU(uint64(len(result.ChunkData)*8), uint64(messageLength-chunkOffset))
		buf = append(buf, result.ChunkData[0:firstReadLen/8]...)
		chunkOffset += firstReadLen
		for chunkOffset < messageLength {
			result, err = lowLevelClosure()
			if err != nil {
				return nil, nil, err
			}
			outOfSync = result.ChunkOffset*elementSizeInBit != chunkOffset || result.Length*elementSizeInBit != messageLength
			if outOfSync {
				break
			}
			readLen := MinU(uint64(len(result.ChunkData)*8), uint64(messageLength-chunkOffset))
			buf = append(buf, result.ChunkData[0:readLen/8]...)
			chunkOffset += readLen
		}
		if !outOfSync {
			return buf, result.Result, nil
		}
	}

	chunkOffset = result.ChunkOffset
	for chunkOffset+uint64(len(result.ChunkData)*8) < messageLength {
		chunkOffset += uint64(len(result.ChunkData) * 8)
		result, _ = lowLevelClosure()
	}
	return nil, nil, fmt.Errorf("stream is out of sync, please retry")
}

func (device *Device) RegisterCallback(functionID uint8, fn func([]byte)) uint64 {
	idChan := make(chan uint64, ChannelSize)
	device.callbackRegTX <- CallbackRegistration{device.internalUID, functionID, fn, idChan}
	return <-idChan
}

func (device *Device) DeregisterCallback(functionID uint8, registrationID uint64) {
	device.callbackDeregTX <- CallbackDeregistration{device.internalUID, functionID, registrationID}
}
