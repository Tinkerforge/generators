// The IP Connection manages the communication between the API bindings and the Brick Daemon or a WIFI/Ethernet Extension.
// Before Bricks and Bricklets can be controlled using their API an IP Connection has to be created and its TCP/IP connection has to be established.
package ipconnection

import (
	"encoding/binary"
	"time"

	"github.com/Tinkerforge/go-api-bindings/internal"
)

// The IP Connection manages the communication between the API bindings and the Brick Daemon or a WIFI/Ethernet Extension.
// Before Bricks and Bricklets can be controlled using their API an IP Connection has to be created and its TCP/IP connection has to be established.
type IPConnection struct {
	handle internal.IPConnection
}

// Creates an IP Connection object that can be used to enumerate the available devices. It is also required for the constructor of Bricks and Bricklets.
func New() IPConnection {
	return IPConnection{internal.NewIPConnection()}
}

// Stops the IP Connection's goroutines.
func (ipcon *IPConnection) Close() {
	ipcon.handle.Close()
}

// For internal use only.
func (ipcon *IPConnection) GetInternalHandle() interface{} {
	return ipcon.handle
}

// Creates a TCP/IP connection to the given `addr` with the form "host:port", as described here: https://golang.org/pkg/net/#Dial . The host and port can refer to a Brick Daemon or to a WIFI/Ethernet Extension.
//
// Devices can only be controlled when the connection was established successfully.
func (ipcon *IPConnection) Connect(addr string) error {
	return ipcon.handle.Connect(addr)
}

// Disconnects the TCP/IP connection from the Brick Daemon or the WIFI/Ethernet Extension.
func (ipcon *IPConnection) Disconnect() {
	ipcon.handle.Disconnect()
}

// Callbacks registered to this event are called whenever the IP Connection got connected to a Brick Daemon or to a WIFI/Ethernet Extension.
// This function returns a registration ID which is used to deregister the callback when it should not be called anymore.
func (ipcon *IPConnection) RegisterConnectCallback(fn func(ConnectReason)) uint64 {
	wrapper := func(reason uint8) { fn(ConnectReason(reason)) }
	return ipcon.handle.RegisterConnectCallback(wrapper)
}

// Callbacks registered to this event are called whenever the IP Connection got disconnected from a Brick Daemon or to a WIFI/Ethernet Extension.
// This function returns a registration ID which is used to deregister the callback when it should not be called anymore.
func (ipcon *IPConnection) RegisterDisconnectCallback(fn func(DisconnectReason)) uint64 {
	wrapper := func(reason uint8) { fn(DisconnectReason(reason)) }
	return ipcon.handle.RegisterDisconnectCallback(wrapper)
}

// Callbacks registered to this event are called whenever a enumerate event is received.
// This function returns a registration ID which is used to deregister the callback when it should not be called anymore.
func (ipcon *IPConnection) RegisterEnumerateCallback(fn func(EnumerateResponse)) uint64 {
	wrapper := func(bytes []byte) {
		var resp EnumerateResponse
		fillFromLeBytes(&resp, bytes[8:])
		fn(resp)
	}
	return ipcon.handle.RegisterEnumerateCallback(wrapper)
}

// Deregisters the connect callback with the given registration ID.
func (ipcon *IPConnection) DeregisterConnectCallback(registrationID uint64) {
	ipcon.handle.DeregisterConnectCallback(registrationID)
}

// Deregisters the disconnect callback with the given registration ID.
func (ipcon *IPConnection) DeregisterDisconnectCallback(registrationID uint64) {
	ipcon.handle.DeregisterDisconnectCallback(registrationID)
}

// Deregisters the enumerate callback with the given registration ID.
func (ipcon *IPConnection) DeregisterEnumerateCallback(registrationID uint64) {
	ipcon.handle.DeregisterEnumerateCallback(registrationID)
}

// Sets the timeout for getters and for setters for which the response expected flag is activated.
//
// Default timeout is 2,5s.
func (ipcon *IPConnection) SetTimeout(timeout time.Duration) {
	ipcon.handle.SetTimeout(timeout)
}

// Returns the timeout as set by SetTimeout
func (ipcon *IPConnection) GetTimeout() time.Duration {
	return ipcon.handle.GetTimeout()
}

// Enables or disables auto-reconnect. If auto-reconnect is enabled, the IP Connection will try to reconnect to
// the previously given host and port, if the currently existing connection is lost.
// Therefore, auto-reconnect only does something after a successful connect call.
//
// Default value is true.
func (ipcon *IPConnection) SetAutoReconnect(autoReconnectEnabled bool) {
	ipcon.handle.SetAutoReconnect(autoReconnectEnabled)
}

// Returns true if auto-reconnect is enabled, false otherwise.
func (ipcon *IPConnection) GetAutoReconnect() bool {
	return ipcon.handle.GetAutoReconnect()
}

// Queries the current connection state.
func (ipcon *IPConnection) GetConnectionState() ConnectionState {
	return ConnectionState(ipcon.handle.GetConnectionState())
}

// Broadcasts an enumerate request. All devices will respond with an enumerate event.
func (ipcon *IPConnection) Enumerate() {
	ipcon.handle.Enumerate()
}

// Performs an authentication handshake with the connected Brick Daemon or WIFI/Ethernet Extension.
// If the handshake succeeds the connection switches from non-authenticated to authenticated state
// and communication can continue as normal. If the handshake fails then the connection gets closed.
// Authentication can fail if the wrong secret was used or if authentication is not enabled at all
// on the Brick Daemon or the WIFI/Ethernet Extension.
//
// See the authentication tutorial for more information.
func (ipcon *IPConnection) Authenticate(secret string) error {
	return ipcon.handle.Authenticate(secret)
}

// This enum specifies the reason of a successful connection.
// It is generated by the connect callback.
type ConnectReason = uint8

const (
	// Connection established after request from user.
	ConnectReasonRequest ConnectReason = iota
	// Connection after auto-reconnect.
	ConnectReasonAutoReconnect
)

// This enum specifies the reason of a connections termination.
// It is generated by the disconnect callback.
type DisconnectReason = uint8

const (
	// Disconnect was requested by user.
	DisconnectReasonRequest DisconnectReason = iota
	// Disconnect because of an unresolvable error.
	DisconnectReasonError
	// Disconnect initiated by Brick Daemon or WIFI/Ethernet Extension.
	DisconnectReasonShutdown
)

// Type of enumeration of a device.
type EnumerationType = uint8

const (
	// Device is available (enumeration triggered by user).
	// This enumeration type can occur multiple times for the same device.
	EnumerationTypeAvailable EnumerationType = iota
	// Device is newly connected (automatically send by Brick after establishing a communication connection).
	// This indicates that the device has potentially lost its previous configuration and needs to be reconfigured.
	EnumerationTypeConnected
	// Device is disconnected (only possible for USB connection). In this case only uid and enumerationType are valid.
	EnumerationTypeDisconnected
)

// Devices send `EnumerateResponse`s when they are connected, disconnected or when an enumeration was
// triggered by the user using the enumerate method.
type EnumerateResponse struct {
	// The UID of the device.
	UID string
	// UID where the device is connected to.
	// For a Bricklet this will be a UID of the Brick where it is connected to.
	// For a Brick it will be the UID of the bottom Master Brick in the stack.
	// For the bottom Master Brick in a stack this will be "0".
	// With this information it is possible to reconstruct the complete network topology.
	ConnectedUID string
	// For Bricks: '0' - '8' (position in stack). For Bricklets: 'a' - 'd' (position on Brick).
	Position rune
	// Major, minor and release number for hardware version.
	HardwareVersion [3]uint8
	// Major, minor and release number for firmware version.
	FirmwareVersion [3]uint8
	// A number that represents the device.
	// The device identifier numbers can be found here: https://www.tinkerforge.com/en/doc/Software/Device_Identifier.html
	// There are also constants for these numbers named following this pattern:
	//
	// <device-package>.DeviceIdentifier
	//
	// For example: master_brick.DeviceIdentifier or ambient_light_bricklet.DeviceIdentifier.
	DeviceIdentifier uint16
	// Type of enumeration.
	EnumerationType EnumerationType
}

func fillFromLeBytes(resp *EnumerateResponse, bytes []byte) {
	resp.UID = internal.ByteSliceToString(bytes[0:8])
	resp.ConnectedUID = internal.ByteSliceToString(bytes[8:16])
	resp.Position = rune(bytes[16])
	resp.HardwareVersion = [3]uint8{bytes[17], bytes[18], bytes[19]}
	resp.FirmwareVersion = [3]uint8{bytes[20], bytes[21], bytes[22]}
	resp.DeviceIdentifier = binary.LittleEndian.Uint16(bytes[23:25])
	resp.EnumerationType = EnumerationType(bytes[25])
}

func bytesExpected(resp *EnumerateResponse) int {
	return 26
}

type ConnectionState = uint8

const (
	ConnectionStateDisconnected ConnectionState = iota
	ConnectionStateConnected
	ConnectionStatePending
)
