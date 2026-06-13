export TinkerforgeDevice
abstract type TinkerforgeDevice end

# returned by get_connection_state
export TinkerforgeIPConConnectionState, CONNECTION_STATE_DISCONNECTED, CONNECTION_STATE_CONNECTED, CONNECTION_STATE_PENDING
@enum TinkerforgeIPConConnectionState begin
    CONNECTION_STATE_DISCONNECTED = 0
    CONNECTION_STATE_CONNECTED = 1
    CONNECTION_STATE_PENDING = 2 # auto-reconnect in process
end

export IPConnection
mutable struct IPConnection
	ipconInternal::PyObject

  function IPConnection()
    package = pyimport("tinkerforge.ip_connection")
    ipconInternal = package.IPConnection()

    return new(ipconInternal)
  end
end

export connect
"""
    $(SIGNATURES)

Creates a TCP/IP connection to the given *host* and *port*. The host
and port can point to a Brick Daemon or to a WIFI/Ethernet Extension.
Devices can only be controlled when the connection was established
successfully.
Blocks until the connection is established and throws an exception if
there is no Brick Daemon or WIFI/Ethernet Extension listening at the
given host and port.
"""
connect(ipcon::IPConnection, host::IPAddr, port::Integer) = connect(ipcon, string(host), port)
connect(ipcon::IPConnection, host::String, port::Integer) = ipcon.ipconInternal.connect(host, port)
connect(ipcon::IPConnection) = connect(ipcon, "localhost", 4223)

export disconnect
"""
    $(SIGNATURES)

Disconnects the TCP/IP connection from the Brick Daemon or the
WIFI/Ethernet Extension.
"""
disconnect(ipcon::IPConnection) = ipcon.ipconInternal.disconnect()

export authenticate
"""
    $(SIGNATURES)

Performs an authentication handshake with the connected Brick Daemon or
WIFI/Ethernet Extension. If the handshake succeeds the connection switches
from non-authenticated to authenticated state and communication can
continue as normal. If the handshake fails then the connection gets closed.
Authentication can fail if the wrong secret was used or if authentication
is not enabled at all on the Brick Daemon or the WIFI/Ethernet Extension.
For more information about authentication see
https://www.tinkerforge.com/en/doc/Tutorials/Tutorial_Authentication/Tutorial.html
"""
authenticate(ipcon::IPConnection, secret::String) = ipcon.ipconInternal.authenticate(secret)

export get_connection_state
"""
    $(SIGNATURES)

Can return the following states:
- CONNECTION_STATE_DISCONNECTED: No connection is established.
- CONNECTION_STATE_CONNECTED: A connection to the Brick Daemon or
  the WIFI/Ethernet Extension is established.
- CONNECTION_STATE_PENDING: IP Connection is currently trying to
  connect.
"""
get_connection_state(ipcon::IPConnection) = TinkerforgeIPConConnectionState(ipcon.ipconInternal.get_connection_state())

export set_auto_reconnect
"""
    $(SIGNATURES)

Enables or disables auto-reconnect. If auto-reconnect is enabled,
the IP Connection will try to reconnect to the previously given
host and port, if the connection is lost.
Default value is *True*.
"""
set_auto_reconnect(ipcon::IPConnection, auto_reconnect::Bool) = ipcon.ipconInternal.set_auto_reconnect(auto_reconnect)

export get_auto_reconnect
"""
    $(SIGNATURES)

Returns *true* if auto-reconnect is enabled, *false* otherwise.
"""
get_auto_reconnect(ipcon::IPConnection) = ipcon.ipconInternal.get_auto_reconnect()
        

export set_timeout
"""
    $(SIGNATURES)

Sets the timeout in seconds for getters and for setters for which the
response expected flag is activated.
Default timeout is 2.5.
"""
set_timeout(ipcon::IPConnection, timeout::Real) = ipcon.ipconInternal.set_timeout(timeout)
 
export get_timeout
"""
    $(SIGNATURES)

Returns the timeout as set by set_timeout.
"""
get_timeout(ipcon::IPConnection) = ipcon.ipconInternal.get_timeout()

export enumerate
"""
    $(SIGNATURES)

Broadcasts an enumerate request. All devices will respond with an
enumerate callback.
"""
enumerate(ipcon::IPConnection) = ipcon.ipconInternal.enumerate()

export wait
"""
    $(SIGNATURES)

Stops the current thread until unwait is called.
This is useful if you rely solely on callbacks for events, if you want
to wait for a specific callback or if the IP Connection was created in
a thread.
Wait and unwait act in the same way as "acquire" and "release" of a
semaphore.
"""
wait(ipcon::IPConnection) =  ipcon.ipconInternal.wait()

export unwait
"""
    $(SIGNATURES)

Unwaits the thread previously stopped by wait.
Wait and unwait act in the same way as "acquire" and "release" of
a semaphore.
"""
unwait(ipcon::IPConnection) = ipcon.ipconInternal.unwait()

export register_callback
"""
    $(SIGNATURES)

Registers the given *function* with the given *callback_id*.
"""
register_callback(ipcon::IPConnection, callback_id::Integer, func::Function) = ipcon.ipconInternal.register_callback(callback_id, func)
