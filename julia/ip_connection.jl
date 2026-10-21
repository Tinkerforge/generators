export TinkerforgeError
abstract type TinkerforgeError <: Exception end

export TinkerforgeTimeoutError
struct TinkerforgeTimeoutError <: TinkerforgeError
  description::String
end

export TinkerforgeNotAddedError
struct TinkerforgeNotAddedError <: TinkerforgeError
  description::String
end

export TinkerforgeAlreadyConnectedError
struct TinkerforgeAlreadyConnectedError <: TinkerforgeError
  description::String
end

export TinkerforgeNotConnectedError
struct TinkerforgeNotConnectedError <: TinkerforgeError
  description::String
end

export TinkerforgeInvalidParameterError
struct TinkerforgeInvalidParameterError <: TinkerforgeError
  description::String
end

export TinkerforgeNotSupportedError
struct TinkerforgeNotSupportedError <: TinkerforgeError
  description::String
end

export TinkerforgeUnknownErrorCodeError
struct TinkerforgeUnknownErrorCodeError <: TinkerforgeError
  description::String
end

export TinkerforgeStreamOutOfSyncError
struct TinkerforgeStreamOutOfSyncError <: TinkerforgeError
  description::String
end

export TinkerforgeInvalidUidError
struct TinkerforgeInvalidUidError <: TinkerforgeError
  description::String
end

export TinkerforgeNonASCIICharInSecretError
struct TinkerforgeNonASCIICharInSecretError <: TinkerforgeError
  description::String
end

export TinkerforgeWrongDeviceTypeError
struct TinkerforgeWrongDeviceTypeError <: TinkerforgeError
  description::String
end

export TinkerforgeDeviceReplacedError
struct TinkerforgeDeviceReplacedError <: TinkerforgeError
  description::String
end

export TinkerforgeWrongResponseLengthError
struct TinkerforgeWrongResponseLengthError <: TinkerforgeError
  description::String
end

export ValueError
struct ValueError <: Exception 
    msg::String
end 

export DeviceIdentifierCheck, DEVICE_IDENTIFIER_CHECK_PENDING, DEVICE_IDENTIFIER_CHECK_MATCH, DEVICE_IDENTIFIER_CHECK_MISMATCH
@enum DeviceIdentifierCheck begin
	DEVICE_IDENTIFIER_CHECK_PENDING = 0
    DEVICE_IDENTIFIER_CHECK_MATCH = 1
    DEVICE_IDENTIFIER_CHECK_MISMATCH = 2
end

export ResponseExpected, RESPONSE_EXPECTED_INVALID_FUNCTION_ID, RESPONSE_EXPECTED_ALWAYS_TRUE, RESPONSE_EXPECTED_TRUE, RESPONSE_EXPECTED_FALSE
@enum ResponseExpected begin
	RESPONSE_EXPECTED_INVALID_FUNCTION_ID = 0
    RESPONSE_EXPECTED_ALWAYS_TRUE = 1 # getter
    RESPONSE_EXPECTED_TRUE = 2 # setter
    RESPONSE_EXPECTED_FALSE = 3 # setter, default
end

export TinkerforgeDevice
abstract type TinkerforgeDevice end

function _initDevice(device::TinkerforgeDevice)
	uid = py"base58decode"(device.uid_string)

	if uid > (1 << 64) - 1
        @warn "Code disabled"
        #throw(TinkerforgeInvalidUidError("UID '$(device.uid_string)' is too big"))
	end

	if uid > ((1 << 32) - 1)
		uid_ = uid64_to_uid32(uid)
	end

	if uid == 0
        throw(TinkerforgeInvalidUidError("UID '$(device.uid_string)' is empty or maps to zero"))
	end

	device.uid = uid
    
	device.response_expected[:FUNCTION_ADC_CALIBRATE] = RESPONSE_EXPECTED_ALWAYS_TRUE
	device.response_expected[:FUNCTION_GET_ADC_CALIBRATION] = RESPONSE_EXPECTED_ALWAYS_TRUE
	device.response_expected[:FUNCTION_READ_BRICKLET_UID] = RESPONSE_EXPECTED_ALWAYS_TRUE
	device.response_expected[:FUNCTION_WRITE_BRICKLET_UID] = RESPONSE_EXPECTED_ALWAYS_TRUE
end

function pack_struct(format::String, data)
    return py"pack_struct"(format, data)
end

function unpack_struct(format::String, data)
    return py"unpack_struct"(format, data)
end

export get_api_version
"""
Returns the API version (major, minor, revision) of the bindings for
this device.
"""
function get_api_version(device::TinkerforgeDevice)
	return device.api_version
end

export get_response_expected
"""
Returns the response expected flag for the function specified by the
*function_id* parameter. It is *true* if the function is expected to
send a response, *false* otherwise.

For getter functions this is enabled by functionault and cannot be disabled,
because those functions will always send a response. For callback
configuration functions it is enabled by functionault too, but can be
disabled via the set_response_expected function. For setter functions
it is disabled by functionault and can be enabled.

Enabling the response expected flag for a setter function allows to
detect timeouts and other error conditions calls of this setter as
well. The device will then send a response for this purpose. If this
flag is disabled for a setter function then no response is sent and
errors are silently ignored, because they cannot be detected.
"""
function get_response_expected(device::TinkerforgeDevice, function_id::Integer)
	if function_id < 0 || function_id >= length(device.response_expected)
		throw(ValueError("Function ID $function_id out of range"))
	end
	
	flag = function_id

	if flag == :RESPONSE_EXPECTED_INVALID_FUNCTION_ID
		throw(ValueError("Invalid function ID $function_id"))
	end

	return flag in [:RESPONSE_EXPECTED_ALWAYS_TRUE, :RESPONSE_EXPECTED_TRUE]
end

export set_response_expected
"""
Changes the response expected flag of the function specified by the
*function_id* parameter. This flag can only be changed for setter
(functionault value: *false*) and callback configuration functions
(functionault value: *true*). For getter functions it is always enabled.

Enabling the response expected flag for a setter function allows to
detect timeouts and other error conditions calls of this setter as
well. The device will then send a response for this purpose. If this
flag is disabled for a setter function then no response is sent and
errors are silently ignored, because they cannot be detected.
"""
function set_response_expected(device::TinkerforgeDevice, function_id, response_expected)
	if function_id < 0 || function_id >= length(device.response_expected)
		throw(ValueError("Function ID {$function_id} out of range"))
	end

	flag = device.response_expected[function_id]

	if flag == RESPONSE_EXPECTED_INVALID_FUNCTION_ID
		throw(ValueError("Invalid function ID {$function_id}"))
	end

	if flag == RESPONSE_EXPECTED_ALWAYS_TRUE
		throw(ValueError("Response Expected flag cannot be changed for function ID {$function_id}"))
	end

	if bool(response_expected)
		device.response_expected[function_id] = RESPONSE_EXPECTED_TRUE
	else
		device.response_expected[function_id] = RESPONSE_EXPECTED_FALSE
	end
end

export set_response_expected_all
"""
Changes the response expected flag for all setter and callback
configuration functions of this device at once.
"""
function set_response_expected_all(device::TinkerforgeDevice, response_expected)
	if bool(response_expected)
		flag = RESPONSE_EXPECTED_TRUE
	else
		flag = RESPONSE_EXPECTED_FALSE
	end

	for i in range(length(device.response_expected))
		if device.response_expected[i] in [RESPONSE_EXPECTED_TRUE, RESPONSE_EXPECTED_FALSE]
			device.response_expected[i] = flag
		end
	end
end

# internal
function check_validity(device::TinkerforgeDevice)
	if device.replaced
		throw(TinkerforgeDeviceReplacedError("Device has been replaced"))
	end

	if device.device_identifier < 0
		return nothing
	end

	if device.device_identifier_check == :DEVICE_IDENTIFIER_CHECK_MATCH
		return nothing
	end

	lock(device.device_identifier_lock) do
		if device.device_identifier_check == :DEVICE_IDENTIFIER_CHECK_PENDING
			device_identifier = send_request(device.ipcon, 255, (), "", 33, "8s 8s c 3B 3B H")[5+1] # <device>.get_identity

			if device_identifier == device.device_identifier
				device.device_identifier_check = :DEVICE_IDENTIFIER_CHECK_MATCH
			else
				device.device_identifier_check = :DEVICE_IDENTIFIER_CHECK_MISMATCH
				device.wrong_device_display_name = get_device_display_name(device_identifier)
			end
        end

		if device.device_identifier_check == :DEVICE_IDENTIFIER_CHECK_MISMATCH
			throw(TinkerforgeWrongDeviceTypeError("UID $(device.uid_string) belongs to a $(device.wrong_device_display_name) instead of the expected $(device.device_display_name)"))
		end
	end
end

export IPConnection
Base.@kwdef mutable struct IPConnection
	host::Union{IPAddr, Missing}
	port::Union{Integer, Missing}
	timeout::Real = 2.5
	auto_reconnect::Bool = true
	auto_reconnect_allowed::Bool = false
	auto_reconnect_pending::Bool = false
	auto_reconnect_internal::Bool = false
	connect_failure_callback::Union{Function, Nothing} = nothing
	sequence_number_lock::Base.AbstractLock = Base.ReentrantLock()
	next_sequence_number::Integer = 0 # protected by sequence_number_lock
	authentication_lock::Base.AbstractLock = Base.ReentrantLock()
	next_authentication_nonce::Integer = 0 # protected by authentication_lock
	devices = Dict()
	replace_lock::Base.AbstractLock = Base.ReentrantLock() # used to synchronize replacements in the devices dict
	registered_callbacks::Dict{Integer, Function} = Dict{Integer, Function}()
	socket = nothing # protected by socket_lock
	socket_id = 0 # protected by socket_lock
	socket_lock::Base.AbstractLock = Base.ReentrantLock()
	socket_send_lock::Base.AbstractLock = Base.ReentrantLock()
	receive_flag::Bool = false
	receive_thread = nothing
	callback = nothing
	disconnect_probe_flag::Bool = false
	disconnect_probe_queue = nothing
	disconnect_probe_thread = nothing
	waiter::Base.Semaphore = Base.Semaphore(10)
	brickd = nothing
end

export BrickDaemon
Base.@kwdef mutable struct BrickDaemon <: TinkerforgeDevice
    replaced::Bool
	uid::Union{Integer, Missing}
	uid_string::String
	ipcon::IPConnection
	device_identifier::Integer
	device_display_name::String
    device_url_part::String
	device_identifier_lock::Base.AbstractLock
	device_identifier_check::DeviceIdentifierCheck # protected by device_identifier_lock
	wrong_device_display_name::String # protected by device_identifier_lock
	api_version::Tuple{Integer, Integer, Integer}
	registered_callbacks::Dict{Integer, Function}
	expected_response_function_id::Union{Integer, Nothing} # protected by request_lock
	expected_response_sequence_number::Union{Integer, Nothing} # protected by request_lock
	response_queue::DataStructures.Queue{Symbol}
	request_lock::Base.AbstractLock
	stream_lock::Base.AbstractLock

    callbacks::Dict{Symbol, Integer}
    callback_formats::Dict{Symbol, Tuple{Integer, String}}
    high_level_callbacks::Dict{Symbol, Integer}
    id_definitions::Dict{Symbol, Integer}
    constants::Dict{Symbol, Integer}
    response_expected::DefaultDict{Symbol, ResponseExpected}

    """
    Creates an object with the unique device ID *uid* and adds it to
    the IP Connection *ipcon*.
    """
    function BrickDaemon(uid::String, ipcon::IPConnection)
        replaced = false
        uid_string = uid
        device_identifier = 0
        device_display_name = "Brick Daemon"
        device_url_part = "brick_daemon" # internal; TODO: Not specified; is this correct?
        device_identifier_lock = Base.ReentrantLock()
        device_identifier_check = DEVICE_IDENTIFIER_CHECK_PENDING # protected by device_identifier_lock
        wrong_device_display_name = "?" # protected by device_identifier_lock
        api_version = (0, 0, 0)
        registered_callbacks = Dict{Integer, Function}()
        expected_response_function_id = nothing # protected by request_lock
        expected_response_sequence_number = nothing # protected by request_lock
        response_queue = DataStructures.Queue{Symbol}()
        request_lock = Base.ReentrantLock()
        stream_lock = Base.ReentrantLock()

        callbacks = Dict{Symbol, Integer}()
        callback_formats = Dict{Symbol, Tuple{Integer, String}}()
        high_level_callbacks = Dict{Symbol, Integer}()
        id_definitions = Dict{Symbol, Integer}()
        constants = Dict{Symbol, Integer}()
        response_expected = DefaultDict{Symbol, ResponseExpected}(RESPONSE_EXPECTED_INVALID_FUNCTION_ID)

        #connected_uid::String
        #position::Char
        #hardware_version::Vector{Integer}
        #firmware_version::Vector{Integer}

        device = new(
            replaced,
            missing,
            uid_string,
            ipcon,
            device_identifier,
            device_display_name,
            device_url_part,
            device_identifier_lock,
            device_identifier_check,
            wrong_device_display_name,
            api_version,
            registered_callbacks,
            expected_response_function_id,
            expected_response_sequence_number,
            response_queue,
            request_lock,
            stream_lock,
            callbacks,
            callback_formats,
            high_level_callbacks,
            id_definitions,
            constants,
            response_expected
        )
        _initDevice(device)

        device.api_version = (2, 0, 0)

        device.id_definitions[:FUNCTION_GET_AUTHENTICATION_NONCE] = 1
        device.id_definitions[:FUNCTION_AUTHENTICATE] = 2

        device.response_expected[:FUNCTION_GET_AUTHENTICATION_NONCE] = RESPONSE_EXPECTED_ALWAYS_TRUE
        device.response_expected[:FUNCTION_AUTHENTICATE] = RESPONSE_EXPECTED_TRUE

        add_device(ipcon, device)

        return device
    end
end

export get_authentication_nonce
function get_authentication_nonce(device::BrickDaemon)
    return send_request(device, :FUNCTION_GET_AUTHENTICATION_NONCE, (), "", 12, "4B")
end

export authenticate
function authenticate(device::BrickDaemon, client_nonce, digest)
    send_request(device, :FUNCTION_AUTHENTICATE, (client_nonce, digest), "4B 20B", 0, "")
end

"""
Creates an IP Connection object that can be used to enumerate the available
devices. It is also required for the constructor of Bricks and Bricklets.
"""
function IPConnection(host::IPAddr, port::Integer)
    ipcon = IPConnection(host=host, port=port)
    brickd = BrickDaemon("2", ipcon)
    ipcon.brickd = brickd

    return ipcon
end
function IPConnection(host::String, port::Integer)
    if host == "localhost"
        hostIP = ip"127.0.0.1"
    else
        hostIP = parse(IPAddr, host)
    end

    return IPConnection(hostIP, port)
end

export TinkerforgeIPConFunctions, FUNCTION_ENUMERATE, FUNCTION_ADC_CALIBRATE,
       FUNCTION_GET_ADC_CALIBRATION, FUNCTION_READ_BRICKLET_UID, FUNCTION_WRITE_BRICKLET_UID,
       FUNCTION_DISCONNECT_PROBE
@enum TinkerforgeIPConFunctions begin
    FUNCTION_ENUMERATE = 254
    FUNCTION_ADC_CALIBRATE = 251
    FUNCTION_GET_ADC_CALIBRATION = 250
    FUNCTION_READ_BRICKLET_UID = 249
    FUNCTION_WRITE_BRICKLET_UID = 248
    FUNCTION_DISCONNECT_PROBE = 128
end

export TinkerforgeIPConCallbacks, CALLBACK_ENUMERATE, CALLBACK_CONNECTED, CALLBACK_DISCONNECTED
@enum TinkerforgeIPConCallbacks begin
    CALLBACK_ENUMERATE = 253
    CALLBACK_CONNECTED = 0
    CALLBACK_DISCONNECTED = 1
end

BROADCAST_UID = 0
DISCONNECT_PROBE_INTERVAL = 5

# enumeration_type parameter to the enumerate callback
export TinkerforgeIPConEnumerationType, ENUMERATION_TYPE_AVAILABLE, ENUMERATION_TYPE_CONNECTED, ENUMERATION_TYPE_DISCONNECTED
@enum TinkerforgeIPConEnumerationType begin
    ENUMERATION_TYPE_AVAILABLE = 0
    ENUMERATION_TYPE_CONNECTED = 1
    ENUMERATION_TYPE_DISCONNECTED = 2
end

# connect_reason parameter to the connected callback
export TinkerforgeIPConConnectReason, CONNECT_REASON_REQUEST, CONNECT_REASON_AUTO_RECONNECT
@enum TinkerforgeIPConConnectReason begin
    CONNECT_REASON_REQUEST = 0
    CONNECT_REASON_AUTO_RECONNECT = 1
end

# disconnect_reason parameter to the disconnected callback
export TinkerforgeIPConDisconnectReason, DISCONNECT_REASON_REQUEST, DISCONNECT_REASON_ERROR, DISCONNECT_REASON_SHUTDOWN
@enum TinkerforgeIPConDisconnectReason begin
    DISCONNECT_REASON_REQUEST = 0
    DISCONNECT_REASON_ERROR = 1
    DISCONNECT_REASON_SHUTDOWN = 2
end

# returned by get_connection_state
export TinkerforgeIPConConnectionState, CONNECTION_STATE_DISCONNECTED, CONNECTION_STATE_CONNECTED, CONNECTION_STATE_PENDING
@enum TinkerforgeIPConConnectionState begin
    CONNECTION_STATE_DISCONNECTED = 0
    CONNECTION_STATE_CONNECTED = 1
    CONNECTION_STATE_PENDING = 2 # auto-reconnect in process
end

export TinkerforgeIPConQueueState, QUEUE_EXIT, QUEUE_META, QUEUE_PACKET
@enum TinkerforgeIPConQueueState begin
    QUEUE_EXIT = 0
    QUEUE_META = 1
    QUEUE_PACKET = 2
end

export CallbackContext
mutable struct CallbackContext
    queue::Union{Base.Channel, Nothing}
    thread::Union{Base.Task, Nothing}
    packet_dispatch_allowed::Bool
    lock::Union{Base.AbstractLock, Nothing}

    function CallbackContext()
        return new(nothing, nothing, false, nothing)
    end
end

export connect
"""
Creates a TCP/IP connection to the given *host* and *port*. The host
and port can point to a Brick Daemon or to a WIFI/Ethernet Extension.

Devices can only be controlled when the connection was established
successfully.

Blocks until the connection is established and throws an exception if
there is no Brick Daemon or WIFI/Ethernet Extension listening at the
given host and port.
"""
function connect(ipcon::IPConnection)
    lock(ipcon.socket_lock) do
        if !isnothing(ipcon.socket)
            throw(TinkerforgeAlreadyConnectedError("Already connected to $(ipcon.host):$(ipcon.port)"))
        end

        connect_unlocked(ipcon, false)
    end

    return nothing
end
connect(host::IPAddr, port::Integer) = connect(IPConnection(host, port))
connect(host::String, port::Integer) = connect(IPConnection(host, port))

export disconnect
"""
Disconnects the TCP/IP connection from the Brick Daemon or the
WIFI/Ethernet Extension.
"""
function disconnect(ipcon::IPConnection)
    lock(ipcon.socket_lock) do
    ipcon.auto_reconnect_allowed = false

        if ipcon.auto_reconnect_pending
            # abort potentially pending auto reconnect
            ipcon.auto_reconnect_pending = false
        else
            if isnothing(ipcon.socket)
                throw(TinkerforgeNotConnectedError("Not connected"))
            end

            disconnect_unlocked(ipcon)
        end

        # end callback thread
        callback = ipcon.callback
        ipcon.callback = nothing
    end

    # do this outside of socket_lock to allow calling (dis-)connect from
    # the callbacks while blocking on the join call here
    callback.queue.put((IPConnection.QUEUE_META,
                        (IPConnection.CALLBACK_DISCONNECTED,
                            IPConnection.DISCONNECT_REASON_REQUEST, None)))
    callback.queue.put((IPConnection.QUEUE_EXIT, None))

    if threading.current_thread() != callback.thread
        callback.thread.join()
    end

    return nothing
end

export authenticate
"""
Performs an authentication handshake with the connected Brick Daemon or
WIFI/Ethernet Extension. If the handshake succeeds the connection switches
from non-authenticated to authenticated state and communication can
continue as normal. If the handshake fails then the connection gets closed.
Authentication can fail if the wrong secret was used or if authentication
is not enabled at all on the Brick Daemon or the WIFI/Ethernet Extension.

For more information about authentication see
https://www.tinkerforge.com/en/doc/Tutorials/Tutorial_Authentication/Tutorial.html
"""
function authenticate(ipcon::IPConnection, secret)
    try
        secret_bytes = acsii(secret)
    catch e
        if e isa ArgumentError
            throw(TinkerforgeNonASCIICharInSecretError("Authentication secret contains non-ASCII characters"))
        else
            rethrow()
        end
    end

    lock(ipcon.authentication_lock) do
        if ipcon.next_authentication_nonce == 0
            try
                ipcon.next_authentication_nonce = unpack_struct("<I", py"urandom"(4))[1]
            catch e
                subseconds, seconds = math.modf(time.time())
                seconds = int(seconds)
                subseconds = int(subseconds * 1000000)
                ipcon.next_authentication_nonce = ((seconds << 26 | seconds >> 6) & 0xFFFFFFFF) + subseconds + getpid()
            end
        end

        server_nonce = get_authentication_nonce(ipcon.brickd)
        client_nonce = unpack_struct("<4B", pack_struct("<I", ipcon.next_authentication_nonce))
        ipcon.next_authentication_nonce = (ipcon.next_authentication_nonce + 1) % (1 << 32)

        h = HMACState("sha1", secret_bytes)

        update!(h, pack_struct("<4B", server_nonce...))
        update!(h, pack_struct("<4B", client_nonce...))

        digest = unpack_struct("<20B", digest!(h))
        h = nothing

        authenticate(ipcon.brickd, client_nonce, digest)
    end
end

export get_connection_state
"""
Can return the following states:

- CONNECTION_STATE_DISCONNECTED: No connection is established.
- CONNECTION_STATE_CONNECTED: A connection to the Brick Daemon or
    the WIFI/Ethernet Extension is established.
- CONNECTION_STATE_PENDING: IP Connection is currently trying to
    connect.
"""
function get_connection_state(ipcon::IPConnection)
    if !isnothing(ipcon.socket)
        return CONNECTION_STATE_CONNECTED
    elseif self.auto_reconnect_pending
        return CONNECTION_STATE_PENDING
    else
        return CONNECTION_STATE_DISCONNECTED
    end
end

export set_auto_reconnect
"""
Enables or disables auto-reconnect. If auto-reconnect is enabled,
the IP Connection will try to reconnect to the previously given
host and port, if the connection is lost.

Default value is *true*.
"""
function set_auto_reconnect(ipcon::IPConnection, auto_reconnect::Bool)
    ipcon.auto_reconnect = auto_reconnect

    if !ipcon.auto_reconnect
        # abort potentially pending auto reconnect
        ipcon.auto_reconnect_allowed = false
    end
end

export get_auto_reconnect
"""
Returns *true* if auto-reconnect is enabled, *false* otherwise.
"""
function get_auto_reconnect(ipcon::IPConnection)
    return ipcon.auto_reconnect
end

export set_timeout
"""
Sets the timeout in seconds for getters and for setters for which the
response expected flag is activated.

Default timeout is 2.5.
"""
function set_timeout(ipcon::IPConnection, timeout::Real)
    if timeout < 0
        throw(ValueError("Timeout cannot be negative"))
    end

    ipcon.timeout = timeout
end

export get_timeout
"""
Returns the timeout as set by set_timeout.
"""
function get_timeout(ipcon::IPConnection)
    return ipcon.timeout
end

export enumerate
"""
Broadcasts an enumerate request. All devices will respond with an
enumerate callback.
"""
function enumerate(ipcon::IPConnection)
    request, _, _ = create_packet_header(ipcon, nothing, 8, FUNCTION_ENUMERATE)

    self.send(request)
end

export wait
"""
Stops the current thread until unwait is called.

This is useful if you rely solely on callbacks for events, if you want
to wait for a specific callback or if the IP Connection was created in
a thread.

Wait and unwait act in the same way as "acquire" and "release" of a
semaphore.
"""
function wait(ipcon::IPConnection)
    acquire(ipcon.waiter)
end

export unwait
"""
Unwaits the thread previously stopped by wait.

Wait and unwait act in the same way as "acquire" and "release" of
a semaphore.
"""
function unwait(ipcon::IPConnection)
    release(ipcon.waiter)
end

export register_callback
"""
Registers the given *function* with the given *callback_id*.
"""
function register_callback(ipcon::IPConnection, callback_id, function_)
    if isnothing(function_)
        delete!(ipcon.registered_callbacks, callback_id)
    else
        ipcon.registered_callbacks[callback_id] = function_
    end
end

# internal
function connect_unlocked(ipcon::IPConnection, is_auto_reconnect::Bool)
    # NOTE: assumes that socket is None and socket_lock is locked

    # create callback thread and queue
    if isnothing(ipcon.callback)
        try
            ipcon.callback = CallbackContext()
            ipcon.callback.queue = Base.Channel()
            ipcon.callback.packet_dispatch_allowed = false
            ipcon.callback.lock = Base.ReentrantLock()
            ipcon.callback.thread = Threads.@spawn callback_loop(ipcon)
            #ipcon.callback.thread.daemon = True
            #ipcon.callback.thread.start()
        catch e
            ipcon.callback = nothing
            rethrow()
        end
    end

    # create and connect socket
    tmp = TCPSocket()
    try
        timeout = 5
        t = Timer(_ -> tmp.status != StatusOpen ? close(tmp) : nothing, timeout)
        try
            tmp = Sockets.connect(tmp, ipcon.host, ipcon.port)
        catch e
            error("Could not connect to $(ipcon.host) on port $(ipcon.port) 
                    since the operations was timed out after $(timeout) seconds!")
        end
    catch e
        if ipcon.auto_reconnect_internal
            if is_auto_reconnect
                return
            end

            if !isnothing(ipcon.connect_failure_callback)
                connect_failure_callback(ipcon, e)
            end

            ipcon.auto_reconnect_allowed = true

            # FIXME: don't misuse disconnected-callback here to trigger an auto-reconnect
            #        because not actual connection has been established yet
            put!(ipcon.callback.queue, (QUEUE_META, (CALLBACK_DISCONNECTED, DISCONNECT_REASON_ERROR, nothing)))
        else
            # end callback thread
            if !is_auto_reconnect
                put!(ipcon.callback.queue, (QUEUE_EXIT, nothing))

                if Threads.threadid() != Threads.threadid(ipcon.callback.thread)
                    Base.wait(ipcon.callback.thread)
                end

                ipcon.callback = nothing
            end
        end
    end

    ipcon.socket = tmp
    ipcon.socket_id += 1

    # create disconnect probe thread
    try
        ipcon.disconnect_probe_flag = true
        ipcon.disconnect_probe_queue = Base.Channel()
        ipcon.disconnect_probe_thread = Threads.@spawn disconnect_probe_loop(ipcon)
        #self.disconnect_probe_thread.daemon = True
        #self.disconnect_probe_thread.start()
    catch e
        ipcon.disconnect_probe_thread = nothing

        # close socket
        close(ipcon.socket)
        ipcon.socket = nothing

        # end callback thread
        if !is_auto_reconnect
            put!(ipcon.callback.queue, (QUEUE_EXIT, nothing))

            if Threads.threadid() != Threads.threadid(ipcon.callback.thread)
                Base.wait(ipcon.callback.thread)
            end

            ipcon.callback = nothing
        end
            
        rethrow()
    end

    # create receive thread
    ipcon.callback.packet_dispatch_allowed = true

    try
        ipcon.receive_flag = true
        ipcon.receive_thread = Threads.@spawn receive_loop(ipcon, ipcon.socket_id)
        #ipcon.receive_thread.daemon = True
        #ipcon.receive_thread.start()
    catch e
        ipcon.receive_thread = nothing

        # close socket
        disconnect_unlocked(ipcon)

        # end callback thread
        if !is_auto_reconnect
            put!(ipcon.callback.queue, (QUEUE_EXIT, nothing))

            if Threads.threadid() != Threads.threadid(ipcon.callback.thread)
                wait(ipcon.callback.thread)
            end

            ipcon.callback = nothing
        end

        rethrow()
    end

    ipcon.auto_reconnect_allowed = false
    ipcon.auto_reconnect_pending = false

    if is_auto_reconnect
        connect_reason = CONNECT_REASON_AUTO_RECONNECT
    else
        connect_reason = CONNECT_REASON_REQUEST
    end

    put!(ipcon.callback.queue, (QUEUE_META, (CALLBACK_CONNECTED, connect_reason, nothing)))
end

# internal
function disconnect_unlocked(ipcon::IPConnection)
    # NOTE: assumes that socket is not None and socket_lock is locked

    # end disconnect probe thread
    put!(ipcon.disconnect_probe_queue, true)
    wait(ipcon.disconnect_probe_thread) # FIXME: use a timeout?
    ipcon.disconnect_probe_thread = nothing

    # stop dispatching packet callbacks before ending the receive
    # thread to avoid timeout exceptions due to callback functions
    # trying to call getters
    if Threads.threadid() != Threads.threadid(ipcon.callback.thread)
        # FIXME: cannot hold callback lock here because this can
        #        deadlock due to an ordering problem with the socket lock
        #with self.callback.lock:
        if true
            ipcon.callback.packet_dispatch_allowed = false
        end
    else
        ipcon.callback.packet_dispatch_allowed = false
    end

    # end receive thread
    ipcon.receive_flag = false

    # TODO: Do we need an alternative?
    # try
    #     self.socket.shutdown(socket.SHUT_RDWR)
    # catch socket.error
    #     pass
    # end

    if !isnothing(ipcon.receive_thread)
        Base.wait(ipcon.receive_thread) # FIXME: use a timeout?
        ipcon.receive_thread = nothing
    end

    # close socket
    close(ipcon.socket)
    ipcon.socket = nothing
end

# internal
function set_auto_reconnect_internal(ipcon::IPConnection, auto_reconnect, connect_failure_callback)
    ipcon.auto_reconnect_internal = auto_reconnect
    ipcon.connect_failure_callback = connect_failure_callback
end

# internal
function add_device(ipcon::IPConnection, device)
    lock(ipcon.replace_lock) do
        replaced_device = get(ipcon.devices, device.uid, nothing)

        if !isnothing(replaced_device)
            replaced_device.replaced = true
        end

        ipcon.devices[device.uid] = device
    end
end

# internal
function receive_loop(ipcon::IPConnection, socket_id)
    # if sys.hexversion < 0x03000000
    #     pending_data = ''
    # else
    #     pending_data = bytes()
    # end
    pending_data = ""

    while ipcon.receive_flag
        try
            data = read(ipcon.socket, 8192)
        catch e
            rethrow() # TODO: just for now
            #socket.timeout
            #continue

            #socket.error
            #     if self.receive_flag:
            #         e = sys.exc_info()[1]
            #         if e.errno == errno.EINTR:
            #             continue
            #         end

            #         self.handle_disconnect_by_peer(IPConnection.DISCONNECT_REASON_ERROR, socket_id, False)
            #     end

            #     break
        end

        if length(data) == 0
            if ipcon.receive_flag
                handle_disconnect_by_peer(ipcon, DISCONNECT_REASON_SHUTDOWN, socket_id, false)
            end

            break
        end

        pending_data *= data

        while ipcon.receive_flag
            if length(pending_data) < 8
                # Wait for complete header
                break
            end

            length = get_length_from_data(pending_data)

            if length(pending_data) < length_
                # Wait for complete packet
                break
            end

            packet = pending_data[1:length_]
            pending_data = pending_data[length_+1:end]

            handle_response(ipcon, packet)
        end
    end
end

# internal
function dispatch_meta(ipcon::IPConnection, function_id, parameter, socket_id)
    if function_id == CALLBACK_CONNECTED
        cb = get(ipcon.registered_callbacks, CALLBACK_CONNECTED, nothing)

        if !isnothing(cb)
            cb(parameter)
        end
    elseif function_id == CALLBACK_DISCONNECTED
        if parameter != DISCONNECT_REASON_REQUEST
            # need to do this here, the receive_loop is not allowed to
            # hold the socket_lock because this could cause a deadlock
            # with a concurrent call to the (dis-)connect function
            lock(ipcon.socket_lock) do
                # don't close the socket if it got disconnected or
                # reconnected in the meantime
                if !isnothing(ipcon.socket) && ipcon.socket_id == socket_id
                    # end disconnect probe thread
                    put!(ipcon.disconnect_probe_queue, true)
                    wait(ipcon.disconnect_probe_thread) # FIXME: use a timeout?
                    ipcon.disconnect_probe_thread = nothing

                    # close socket
                    close(ipcon.socket)
                    ipcon.socket = nothing
                end
            end
        end

        # FIXME: wait a moment here, otherwise the next connect
        # attempt will succeed, even if there is no open server
        # socket. the first receive will then fail directly
        sleep(0.1)

        cb = get(ipcon.registered_callbacks, CALLBACK_DISCONNECTED, nothing)

        if !isnothing(cb)
            cb(parameter)
        end

        if parameter != DISCONNECT_REASON_REQUEST && ipcon.auto_reconnect && ipcon.auto_reconnect_allowed
            ipcon.auto_reconnect_pending = true
            retry = true

            # block here until reconnect. this is okay, there is no
            # callback to deliver when there is no connection
            while retry
                retry = false

                lock(ipcon.socket_lock) do
                    if ipcon.auto_reconnect_allowed && isnothing(ipcon.socket)
                        try
                            connect_unlocked(ipcon, true)
                        catch e
                            retry = true
                        end
                    else
                        ipcon.auto_reconnect_pending = false
                    end
                end

                if retry
                    sleep(0.1)
                end
            end
        end
    end
end

# internal
function dispatch_packet(ipcon::IPConnection, packet)
    uid = get_uid_from_data(packet)
    length = get_length_from_data(packet)
    function_id = get_function_id_from_data(packet)
    payload = packet[8:end] # TODO: Have a close look with indexing!!! This is still like in python

    if function_id == CALLBACK_ENUMERATE

        cb = ipcon.registered_callbacks[CALLBACK_ENUMERATE]

        if isnothing(cb)
            return
        end

        if length(packet) != 34
            return # silently ignoring callback with wrong length
        end

        uid, connected_uid, position, hardware_version, firmware_version, device_identifier, enumeration_type = unpack_payload(payload, "8s 8s c 3B 3B H B")

        cb(uid, connected_uid, position, hardware_version,
            firmware_version, device_identifier, enumeration_type)

        return
    end

    device = ipcon.devices[uid]

    if isnothing(device)
        return
    end

    try
        device.check_validity()
    catch e
        return # silently ignoring callback for invalid device
    end

    if -function_id in device.high_level_callbacks
        hlcb = device.high_level_callbacks[-function_id] # [roles, options, data]
        length, form = device.callback_formats[function_id] # FIXME: currently assuming that low-level callback has more than one element

        if length(packet) != length
            return # silently ignoring callback with wrong length
        end

        llvalues = unpack_payload(payload, form)
        has_data = false
        data = nothing

        if !isnothing(hlcb[1]["fixed_length"])
            length = hlcb[1]["fixed_length"]
        else
            length = llvalues[findfirst("stream_length", hlcb[0])]
        end

        if !hlcb[1]["single_chunk"]
            chunk_offset = llvalues[findfirst("stream_chunk_offset", hlcb[0])]
        else
            chunk_offset = 0
        end

        chunk_data = llvalues[findfirst("stream_chunk_data", hlcb[0])]

        if isnothing(hlcb[2]) # no stream in-progress
            if chunk_offset == 0 # stream starts
                hlcb[2] = chunk_data

                if length(hlcb[2]) >= length_ # stream complete
                    has_data = true
                    data = hlcb[2][:length_]
                    hlcb[2] = nothing
                end
            else # ignore tail of current stream, wait for next stream start
                #pass
            end
        else # stream in-progress
            if chunk_offset != length(hlcb[2]) # stream out-of-sync
                has_data = true
                data = nothing
                hlcb[2] = nothing
            else # stream in-sync
                hlcb[2] += chunk_data

                if length(hlcb[2]) >= length_ # stream complete
                    has_data = true
                    data = hlcb[2][:length]
                    hlcb[2] = nothing
                end
            end
        end

        cb = device.registered_callbacks[-function_id]

        if has_data && !isnothing(cb)
            result = []

            for (role, llvalue) in zip(hlcb[0], llvalues)
                if role == "stream_chunk_data"
                    append!(result, data)
                elseif isnothing(role)
                    append!(result, llvalue)
                end
            end

            cb(tuple(result)...)
        end
    end

    cb = device.registered_callbacks[function_id]

    if !isnothing(cb)
        length, form = get(device.callback_formats, function_id, (nothing, nothing))

        if isnothing(length_)
            return # silently ignore registered but unknown callback
        end

        if length(packet) != length_
            return # silently ignoring callback with wrong length
        end

        if length(form) == 0
            cb()
        elseif !(' ' in form)
            cb(unpack_payload(payload, form))
        else
            cb(unpack_payload(payload, form)...)
        end
    end
end

# internal
function callback_loop(ipcon::IPConnection)
    callback = ipcon.callback
    while true
        kind, data = take!(callback.queue)

        # FIXME: cannot hold callback lock here because this can
        #        deadlock due to an ordering problem with the socket lock
        #with callback.lock:
        if true
            if kind == QUEUE_EXIT
                break
            elseif kind == QUEUE_META
                dispatch_meta(ipcon, data...)
            elseif kind == QUEUE_PACKET
                # don't dispatch callbacks when the receive thread isn't running
                if callback.packet_dispatch_allowed
                    dispatch_packet(ipcon, data)
                end
            end
        end
    end
end

# internal
# NOTE: the disconnect probe thread is not allowed to hold the socket_lock at any
#       time because it is created and joined while the socket_lock is locked
function disconnect_probe_loop(ipcon::IPConnection)
    disconnect_probe_queue = ipcon.disconnect_probe_queue
    request, _, _ = create_packet_header(ipcon, nothing, 8, FUNCTION_DISCONNECT_PROBE)

    while true
        # Here comes a crude way to express the following Pyrhon connected
        # try
        #     disconnect_probe_queue.get(true, DISCONNECT_PROBE_INTERVAL)
        #     break
        # catch queue.Empty
        #     pass

        wait_disconnect(timeout) = begin
            t = @async take!(disconnect_probe_queue)
            for i=1:20
                if istaskdone(t)
                    return true
                end
                sleep(timeout / N )
            end
            return false
        end

        if wait_disconnect(DISCONNECT_PROBE_INTERVAL)
            break
        end

        if ipcon.disconnect_probe_flag
            try
                lock(self.socket_send_lock) do
                    while true
                        try
                            send(ipcon.socket, request)
                            break
                        catch e
                            #socket.timeout
                            continue
                        end
                    end
                end
            catch e
                #socket.error
                handle_disconnect_by_peer(ipcon, DISCONNECT_REASON_ERROR, ipcon.socket_id, false)
                break
            end
        else
            ipcon.disconnect_probe_flag = true
        end
    end
end

# internal
function send(ipcon::IPConnection, packet)
    @warn "locking within send"
    lock(ipcon.socket_lock) do
        @warn "locked socket"
        if isnothing(ipcon.socket)
            throw(TinkerforgeNotConnectedError("Not connected"))
        end

        try
            lock(ipcon.socket_send_lock) do
                @warn "locked send"
                Base.write(ipcon.socket, packet)
            end
        catch e
            #socket.error
            handle_disconnect_by_peer(ipcon, DISCONNECT_REASON_ERROR, nothing, true)
            throw(TinkerforgeNotConnectedError("Not connected"))
        end

        ipcon.disconnect_probe_flag = false
    end
end

# internal
function send_request(device::TinkerforgeDevice, function_id::Symbol, data, form, length_ret, form_ret)
    ipcon = device.ipcon
    payload = py"pack_payload"(data, form)
    header, response_expected, sequence_number = create_packet_header(ipcon, device, 8 + length(payload), device.id_definitions[function_id])
    request = header * payload

    @warn "going into if" response_expected

    if response_expected
        @warn "locking"
        lock(device.request_lock) do
            @warn "locked"
            device.expected_response_function_id = function_id
            device.expected_response_sequence_number = sequence_number

            try
                @warn "try sending"
                send(ipcon, request)
                @warn "sending done"

                while true
                    # Here comes a crude way to express the following Python code
                    # response = device.response_queue.get(true, self.timeout)

                    wait_get(timeout) = begin
                        t = @async take!(device.response_queue)
                        for i=1:20
                            if istaskdone(t)
                                return fetch(t)
                            end
                            sleep(timeout / N )
                        end
                        return false
                    end

                    @warn "waiting for get"
                    response = wait_get(ipcon.timeout)
                    if response == false
                        throw(TinkerforgeTimeoutError("Timeout occured"))
                    end

                    if function_id == get_function_id_from_data(response) && sequence_number == get_sequence_number_from_data(response)
                        # ignore old responses that arrived after the timeout expired, but before setting
                        # expected_response_function_id and expected_response_sequence_number back to None
                        break
                    end
                end
            catch e
                #queue.Empty
                if e isa TinkerforgeTimeoutError
                    msg = "Did not receive response for function $function_id in time"
                    throw(TinkerforgeTimeoutError(msg))
                end
            finally
                device.expected_response_function_id = nothing
                device.expected_response_sequence_number = nothing
            end
        end

        error_code = get_error_code_from_data(response)

        if error_code == 0
            if length_ret == 0
                length_ret = 8 # setter with response-expected enabled
            end

            if length(response) != length_ret
                msg = "Expected response of $length_ret byte for function ID $function_id, got $(length(response)) byte instead"
                throw(TinkerforgeWrongResponseLengthError(msg))
            end
        elseif error_code == 1
            msg = "Got invalid parameter for function $function_id"
            throw(TinkerforgeInvalidParameterError(msg))
        elseif error_code == 2
            msg = "Function $function_id is not supported"
            throw(TinkerforgeNotSupportedError(msg))
        else
            msg = "Function $function_id returned an unknown error"
            throw(TinkerforgeUnknownErrorCodeError(msg))
        end

        if length(form_ret) > 0
            return unpack_payload(response[8:end], form_ret)
        end
    else
        @warn "sending without an expected response"
        send(ipcon, request)
    end
end

# internal
function get_next_sequence_number(ipcon::IPConnection)
    lock(ipcon.sequence_number_lock) do
        sequence_number = ipcon.next_sequence_number + 1
        ipcon.next_sequence_number = sequence_number % 15
        return sequence_number
    end
end

# internal
function handle_response(ipcon::IPConnection, packet)
    ipcon.disconnect_probe_flag = false

    function_id = get_function_id_from_data(packet)
    sequence_number = get_sequence_number_from_data(packet)

    if sequence_number == 0 && function_id == CALLBACK_ENUMERATE
        if CALLBACK_ENUMERATE in ipcon.registered_callbacks
            enqueue!(ipcon.callback.queue, (QUEUE_PACKET, packet))
        end

        return
    end

    uid = get_uid_from_data(packet)
    device = ipcon.devices[uid]

    if isnothing(device)
        return # Response from an unknown device, ignoring it
    end

    if sequence_number == 0
        if function_id in device.registered_callbacks || -function_id in device.high_level_callbacks
            enqueue!(ipcon.callback.queue, (QUEUE_PACKET, packet))
        end

        return
    end

    if device.expected_response_function_id == function_id && device.expected_response_sequence_number == sequence_number
        enqueue!(device.response_queue, packet)
        return
    end

    # Response seems to be OK, but can't be handled
end

# internal
function handle_disconnect_by_peer(ipcon::IPConnection, disconnect_reason::String, socket_id::Integer, disconnect_immediately::Bool)
    # NOTE: assumes that socket_lock is locked if disconnect_immediately is true

    ipcon.auto_reconnect_allowed = true

    if disconnect_immediately
        disconnect_unlocked(ipcon)
    end

    enqueue!(ipcon.callback.queue, (QUEUE_META, (CALLBACK_DISCONNECTED, disconnect_reason, socket_id)))
end

# internal
function create_packet_header(ipcon::IPConnection, device::TinkerforgeDevice, length_::Integer, function_id::Integer)
    uid = BROADCAST_UID
    sequence_number = get_next_sequence_number(ipcon)
    r_bit = 0

    if !isnothing(device)
        uid = device.uid

        if get_response_expected(device, function_id)
            r_bit = 1
        end
    end

    sequence_number_and_options = (sequence_number << 4) | (r_bit << 3)

    return (pack_struct("<IBBBB", (uid, length_, function_id, sequence_number_and_options, 0)), Bool(r_bit), sequence_number)
end

# internal
function get_adc_calibration(ipcon::IPConnection, device::TinkerforgeDevice)
    return send_request(ipcon, device,
                        :FUNCTION_GET_ADC_CALIBRATION,
                        (),
                        "",
                        12, "h h")
end

# internal
function adc_calibrate(ipcon::IPConnection, device::TinkerforgeDevice, port::Integer)
    send_request(device,
                 :FUNCTION_ADC_CALIBRATE,
                 (port,),
                 "c",
                 0, "")
end

# internal
function write_bricklet_uid(ipcon::IPConnection, device::TinkerforgeDevice, port::Integer, uid::String)
    uid_int = py"base58decode"(uid)

    send_request(ipcon, device,
                 :FUNCTION_WRITE_BRICKLET_UID,
                 (port, uid_int),
                 "c I",
                 0, "")
end

# internal
function read_bricklet_uid(ipcon::IPConnection, device, port)
    uid_int = send_request(ipcon,
                           device,
                           :FUNCTION_READ_BRICKLET_UID,
                           (port,),
                           "c", 12, "I")

    return py"base58encode"(uid_int)
end