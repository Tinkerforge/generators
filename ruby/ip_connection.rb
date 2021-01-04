# -*- ruby encoding: utf-8 -*-
# Copyright (C) 2012-2014, 2019-2020 Matthias Bolte <matthias@tinkerforge.com>
#
# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

require 'socket'
require 'thread'
require 'timeout'
require 'securerandom'
require 'openssl'
require_relative './device_display_names'

module Tinkerforge
  # internal
  class Base58
    ALPHABET = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'

    def self.encode(value)
      encoded = ''
      while value >= 58
        div, mod = value.divmod 58
        encoded = ALPHABET[mod, 1] + encoded
        value = div
      end
      ALPHABET[value, 1] + encoded
    end

    def self.decode(encoded)
      value = 0
      base = 1
      encoded.reverse.split(//).each do |c|
        index = ALPHABET.index c
        if index == nil
          raise ArgumentError, "UID '#{encoded}' contains invalid character"
        end
        value += index * base
        base *= 58
      end
      value
    end
  end

  class TinkerforgeException < RuntimeError
  end

  class TimeoutException < TinkerforgeException
  end

  class AlreadyConnectedException < TinkerforgeException
  end

  class NotConnectedException < TinkerforgeException
  end

  class InvalidParameterException < TinkerforgeException
  end

  class NotSupportedException < TinkerforgeException
  end

  class UnknownErrorCodeException < TinkerforgeException
  end

  class StreamOutOfSyncException < TinkerforgeException
  end

  class WrongDeviceTypeException < TinkerforgeException
  end

  class DeviceReplacedException < TinkerforgeException
  end

  class WrongResponseLengthException < TinkerforgeException
  end

  # internal
  class Packer
    def self.pack(unpacked, format)
      data = ''

      format.split(' ').each do |f|
        if f.length > 1
          f0 = f[0, 1]
          f1 = f[1..-1]
          r = []

          if f0 == '?'
            n1 = (Integer(f1) / 8.0).ceil
            r = Array.new(n1, 0)

            unpacked[0].each_with_index do |b, i|
              if b
                r[i / 8] |= 1 << (i % 8)
              end
            end

            data += r.pack "C#{n1}"
          elsif f0 == 'k'
            unpacked[0].each { |c| r << c.ord }
            data += r.pack "C#{f1}"
          else
            r = unpacked[0]
            if ['s', 'S', 'l', 'L', 'q', 'Q'].count(f0) > 0
              data += r.pack "#{f0}<#{f1}"
            elsif f0 == 'Z'
              data += [r].pack "#{f0}#{f1}"
            else
              data += r.pack "#{f0}#{f1}"
            end
          end
        else
          if f == '?'
            r = [unpacked[0] ? 1 : 0]
            data += r.pack 'C'
          elsif f == 'k'
            r = [unpacked[0].ord]
            data += r.pack 'C'
          else
            r = [unpacked[0]]
            if ['s', 'S', 'l', 'L', 'q', 'Q'].count(f) > 0
              data += r.pack "#{f}<"
            else
              data += r.pack f
            end
          end
        end

        unpacked = unpacked.drop 1
      end

      data
    end

    def self.unpack(data, format)
      unpacked = []

      format.split(' ').each do |f|
        if f.length > 1
          f0 = f[0, 1]
          f1 = f[1..-1]
          u = []

          if f0 == '?'
            n1 = (Integer(f1) / 8.0).ceil()
            r = data.unpack "C#{n1}a*"
            data = r[-1]
            r.delete_at(-1)

            for i in 0..Integer(f1) - 1
              u << ((r[i / 8] & (1 << (i % 8))) != 0)
            end
          elsif f0 == 'k'
            r = data.unpack "C#{f1}a*"
            data = r[-1]
            r.delete_at(-1)
            r.each { |c| u << c.chr }
          else
            if ['s', 'S', 'l', 'L', 'q', 'Q'].count(f0) > 0
              r = data.unpack "#{f}<a*"
            else
              r = data.unpack "#{f}a*"
            end
            data = r[-1]
            r.delete_at(-1)
            r.each { |k| u << k }
          end

          if u.length == 1
            u = u[0]
          end

          unpacked << u
        else
          r = []
          u = nil

          if f == '?'
            r = data.unpack "Ca*"
            u = r[0] != 0
          elsif f == 'k'
            r = data.unpack "Ca*"
            u = r[0].chr
          else
            if ['s', 'q', 'l', 'L', 'S', 'Q'].count(f) > 0
              r = data.unpack "#{f}<a*"
            else
              r = data.unpack "#{f}a*"
            end
            u = r[0]
          end

          data = r[1]
          unpacked << u
        end
      end

      unpacked
    end

    def self.get_uid_from_data(data)
      data[0, 4].unpack('L<')[0]
    end

    def self.get_length_from_data(data)
      data[4, 1].unpack('C')[0]
    end

    def self.get_function_id_from_data(data)
      data[5, 1].unpack('C')[0]
    end

    def self.get_sequence_number_from_data(data)
      (data[6, 1].unpack('C')[0] >> 4) & 0x0F
    end

    def self.get_error_code_from_data(data)
      (data[7, 1].unpack('C')[0] >> 6) & 0x03
    end
  end

  # internal
  class Device
    DEVICE_IDENTIFIER_CHECK_PENDING = 0
    DEVICE_IDENTIFIER_CHECK_MATCH = 1
    DEVICE_IDENTIFIER_CHECK_MISMATCH = 2

    RESPONSE_EXPECTED_INVALID_FUNCTION_ID = 0
    RESPONSE_EXPECTED_ALWAYS_TRUE = 1 # getter
    RESPONSE_EXPECTED_TRUE = 2 # setter
    RESPONSE_EXPECTED_FALSE = 3 # setter, default

    attr_accessor :replaced
    attr_accessor :uid
    attr_accessor :expected_response_function_id
    attr_accessor :expected_response_sequence_number
    attr_accessor :callback_formats
    attr_accessor :high_level_callbacks
    attr_accessor :registered_callbacks

    # internal
    def initialize(uid, ipcon, device_identifier, device_display_name)
      @replaced = false
      @uid = Base58.decode uid
      @uid_string = uid

      if @uid > (1 << 64) - 1
        raise ArgumentError, "UID '#{uid}' is too big"
      end

      if @uid > (1 << 32) - 1
        # convert from 64bit to 32bit
        value1 = @uid & 0xFFFFFFFF
        value2 = (@uid >> 32) & 0xFFFFFFFF

        @uid  = (value1 & 0x00000FFF)
        @uid |= (value1 & 0x0F000000) >> 12
        @uid |= (value2 & 0x0000003F) << 16
        @uid |= (value2 & 0x000F0000) << 6
        @uid |= (value2 & 0x3F000000) << 2
      end

      if @uid == 0
        raise ArgumentError, "UID '#{uid}' is empty or maps to zero"
      end

      @api_version = [0, 0, 0]

      @ipcon = ipcon

      @device_identifier = device_identifier
      @device_display_name = device_display_name
      @device_identifier_lock = Mutex.new
      @device_identifier_check = DEVICE_IDENTIFIER_CHECK_PENDING # protected by device_identifier_lock
      @wrong_device_display_name = '?' # protected by device_identifier_lock

      @request_mutex = Mutex.new

      @response_expected = Array.new(256, RESPONSE_EXPECTED_INVALID_FUNCTION_ID)

      @expected_response_function_id = 0
      @expected_response_sequence_number = 0

      @response_mutex = Mutex.new
      @response_condition = ConditionVariable.new
      @response_queue = Queue.new

      @stream_mutex = Mutex.new

      @callback_formats = {}
      @high_level_callbacks = {}
      @registered_callbacks = {}
    end

    # Returns the API version (major, minor, revision) of the bindings for
    # this device.
    def get_api_version
      @api_version
    end

    # Returns the response expected flag for the function specified by the
    # <tt>function_id</tt> parameter. It is <tt>true</tt> if the function is
    # expected to send a response, <tt>false</tt> otherwise.
    #
    # For getter functions this is enabled by default and cannot be disabled,
    # because those functions will always send a response. For callback
    # configuration functions it is enabled by default too, but can be
    # disabled via the set_response_expected function. For setter functions it
    # is disabled by default and can be enabled.
    #
    # Enabling the response expected flag for a setter function allows to
    # detect timeouts and other error conditions calls of this setter as
    # well. The device will then send a response for this purpose. If this
    # flag is disabled for a setter function then no response is sent and
    # errors are silently ignored, because they cannot be detected.
    def get_response_expected(function_id)
      if function_id < 0 or function_id > 255
        raise ArgumentError, "Function ID #{function_id} out of range"
      end

      flag = @response_expected[function_id]

      if flag == RESPONSE_EXPECTED_INVALID_FUNCTION_ID
        raise ArgumentError, "Invalid function ID #{function_id}"
      end

      if flag == RESPONSE_EXPECTED_ALWAYS_TRUE or \
         flag == RESPONSE_EXPECTED_TRUE
        true
      else
        false
      end
    end

    # Changes the response expected flag of the function specified by the
    # <tt>function_id</tt> parameter. This flag can only be changed for setter
    # (default value: <tt>false</tt>) and callback configuration functions
    # (default value: <tt>true</tt>). For getter functions it is always enabled.
    #
    # Enabling the response expected flag for a setter function allows to
    # detect timeouts and other error conditions calls of this setter as
    # well. The device will then send a response for this purpose. If this
    # flag is disabled for a setter function then no response is sent and
    # errors are silently ignored, because they cannot be detected.
    def set_response_expected(function_id, response_expected)
      if function_id < 0 or function_id > 255
        raise ArgumentError, "Function ID #{function_id} out of range"
      end

      flag = @response_expected[function_id]

      if flag == RESPONSE_EXPECTED_INVALID_FUNCTION_ID
        raise ArgumentError, "Invalid function ID #{function_id}"
      end

      if flag == RESPONSE_EXPECTED_ALWAYS_TRUE
        raise ArgumentError, "Response Expected flag cannot be changed for function ID #{function_id}"
      end

      if response_expected
        @response_expected[function_id] = RESPONSE_EXPECTED_TRUE
      else
        @response_expected[function_id] = RESPONSE_EXPECTED_FALSE
      end
    end

    # Changes the response expected flag for all setter and callback
    # configuration functions of this device at once.
    def set_response_expected_all(response_expected)
      if response_expected
        flag = RESPONSE_EXPECTED_TRUE
      else
        flag = RESPONSE_EXPECTED_FALSE
      end

      for function_id in 0..255
        if @response_expected[function_id] == RESPONSE_EXPECTED_TRUE or \
           @response_expected[function_id] == RESPONSE_EXPECTED_FALSE
          @response_expected[function_id] = flag
        end
      end
    end

    # internal
    def send_request(function_id, request_data, request_format,
                     expected_response_length, response_format)
      response = nil

      if request_data.length > 0
        payload = Packer.pack request_data, request_format
      else
        payload = ''
      end

      header, response_expected, sequence_number = \
        @ipcon.create_packet_header self, 8 + payload.length, function_id
      request = header + payload

      if response_expected
        packet = nil

        @request_mutex.synchronize {
          @expected_response_function_id = function_id
          @expected_response_sequence_number = sequence_number

          begin
            @ipcon.send_request request

            while true
              packet = dequeue_response "Did not receive response in time for function ID #{function_id}"

              if function_id == Packer.get_function_id_from_data(packet) and \
                 sequence_number == Packer.get_sequence_number_from_data(packet)
                # ignore old responses that arrived after the timeout expired, but before setting
                # expected_response_function_id and expected_response_sequence_number back to None
                break
              end
            end
          ensure
            @expected_response_function_id = 0
            @expected_response_sequence_number = 0
          end
        }

        error_code = Packer.get_error_code_from_data packet

        if error_code == 0
          if expected_response_length == 0
            expected_response_length = 8 # setter with response-expected enabled
          end

          if packet.length != expected_response_length
            raise WrongResponseLengthException, "Expected response of #{expected_response_length} byte for function ID #{function_id}, got #{packet.length} byte instead"
          end
        elsif error_code == 1
          raise InvalidParameterException, "Got invalid parameter for function ID #{function_id}"
        elsif error_code == 2
          raise NotSupportedException, "Function ID #{function_id} is not supported"
        else
          raise UnknownErrorCodeException, "Function ID #{function_id} returned an unknown error"
        end

        if response_format.length > 0
          response = Packer.unpack packet[8..-1], response_format

          if response.length == 1
            response = response[0]
          end
        end
      else
        @ipcon.send_request request
      end

      response
    end

    # internal
    def enqueue_response(response)
      @response_mutex.synchronize {
        @response_queue.push response
        @response_condition.signal
      }
    end

    # internal
    def dequeue_response(message)
      response = nil

      @response_mutex.synchronize {
        @response_condition.wait @response_mutex, @ipcon.timeout

        if @response_queue.empty?
          raise TimeoutException, message
        end

        response = @response_queue.pop
      }

      response
    end

    # internal
    def check_validity()
      if @replaced
        raise DeviceReplacedException, 'Device has been replaced'
      end

      if @device_identifier_check == DEVICE_IDENTIFIER_CHECK_MATCH
        return
      end

      @device_identifier_lock.synchronize {
        if @device_identifier_check == DEVICE_IDENTIFIER_CHECK_PENDING
          device_identifier = send_request(255, [], '', 33, 'Z8 Z8 k C3 C3 S')[5] # <device>.get_identity

          if device_identifier == @device_identifier
            @device_identifier_check = DEVICE_IDENTIFIER_CHECK_MATCH
          else
            @device_identifier_check = DEVICE_IDENTIFIER_CHECK_MISMATCH
            @wrong_device_display_name = get_device_display_name device_identifier
          end
        end

        if @device_identifier_check == DEVICE_IDENTIFIER_CHECK_MISMATCH
          raise WrongDeviceTypeException, "UID #{@uid_string} belongs to a #{@wrong_device_display_name} instead of the expected #{@device_display_name}"
        end
      }
    end
  end

  # internal
  class CallbackContext
    attr_accessor :queue
    attr_accessor :thread
    attr_accessor :mutex
    attr_accessor :packet_dispatch_allowed

    def initialize
      @queue = nil
      @thread = nil
      @mutex = nil
      @packet_dispatch_allowed = false
    end
  end

  # internal
  class BrickDaemon < Device
    FUNCTION_GET_AUTHENTICATION_NONCE = 1 # :nodoc:
    FUNCTION_AUTHENTICATE = 2 # :nodoc:

    # Creates an object with the unique device ID <tt>uid</tt> and adds it to
    # the IP Connection <tt>ipcon</tt>.
    def initialize(uid, ipcon)
      super uid, ipcon, 0, 'Brick Daemon'

      @api_version = [2, 0, 0]

      @response_expected[FUNCTION_GET_AUTHENTICATION_NONCE] = RESPONSE_EXPECTED_ALWAYS_TRUE
      @response_expected[FUNCTION_AUTHENTICATE] = RESPONSE_EXPECTED_TRUE

      @ipcon.add_device self
    end

    def get_authentication_nonce
      send_request FUNCTION_GET_AUTHENTICATION_NONCE, [], '', 12, 'C4'
    end

    def authenticate(client_nonce, digest)
      send_request FUNCTION_AUTHENTICATE, [client_nonce, digest], 'C4 C20', 0, ''
    end
  end

  class IPConnection
    attr_accessor :timeout

    CALLBACK_ENUMERATE = 253
    CALLBACK_CONNECTED = 0
    CALLBACK_DISCONNECTED = 1

    # enumeration_type parameter for CALLBACK_ENUMERATE
    ENUMERATION_TYPE_AVAILABLE = 0
    ENUMERATION_TYPE_CONNECTED = 1
    ENUMERATION_TYPE_DISCONNECTED = 2

    # connect_reason parameter for CALLBACK_CONNECTED
    CONNECT_REASON_REQUEST = 0
    CONNECT_REASON_AUTO_RECONNECT = 1

    # disconnect_reason parameter for CALLBACK_DISCONNECTED
    DISCONNECT_REASON_REQUEST = 0
    DISCONNECT_REASON_ERROR = 1
    DISCONNECT_REASON_SHUTDOWN = 2

    # returned by get_connection_state
    CONNECTION_STATE_DISCONNECTED = 0
    CONNECTION_STATE_CONNECTED = 1
    CONNECTION_STATE_PENDING = 2 # auto-reconnect in progress

    # Creates an IP Connection object that can be used to enumerate the
    # available devices. It is also required for the constructor of Bricks
    # and Bricklets.
    def initialize
      @host = nil
      @port = 0

      @timeout = 2.5

      @auto_reconnect = true
      @auto_reconnect_allowed = false
      @auto_reconnect_pending = false

      @next_sequence_number = 0 # protected by sequence_number_mutex
      @sequence_number_mutex = Mutex.new

      @next_authentication_nonce = 0 # protected by authentication_mutex
      @authentication_mutex = Mutex.new # protects authentication handshake

      @devices = {}
      @replace_mutex = Mutex.new # used to synchronize replacements in the devices dict

      @registered_callbacks = {}

      @socket_mutex = Mutex.new
      @socket_send_mutex = Mutex.new
      @socket = nil # protected by socket_mutex
      @socket_id = 0 # protected by socket_mutex

      @receive_flag = false
      @receive_thread = nil

      @callback = nil

      @disconnect_probe_flag = false
      @disconnect_probe_queue = nil
      @disconnect_probe_thread = nil # protected by socket_mutex

      @waiter_queue = Queue.new

      @brickd = BrickDaemon.new '2', self
    end

    # Creates a TCP/IP connection to the given <tt>host</tt> and <tt>port</tt>.
    # The host and port can point to a Brick Daemon or to a WIFI/Ethernet
    # Extension.
    #
    # Devices can only be controlled when the connection was established
    # successfully.
    #
    # Blocks until the connection is established and throws an exception if
    # there is no Brick Daemon or WIFI/Ethernet Extension listening at the
    # given host and port.
    def connect(host, port)
      @socket_mutex.synchronize {
        if @socket != nil
          raise AlreadyConnectedException, "Already connected to #{@host}:#{@port}"
        end

        @host = host
        @port = port

        connect_unlocked false
      }
    end

    # Disconnects the TCP/IP connection from the Brick Daemon or the
    # WIFI/Ethernet Extension.
    def disconnect
      callback = nil

      @socket_mutex.synchronize {
        @auto_reconnect_allowed = false

        if @auto_reconnect_pending
          # Abort pending auto reconnect
          @auto_reconnect_pending = false
        else
          if @socket == nil
            raise NotConnectedException, 'Not connected'
          end

          disconnect_unlocked
        end

        # Destroy callback thread
        callback = @callback
        @callback = nil
      }

      # Do this outside of socket_mutex to allow calling (dis-)connect from
      # the callbacks while blocking on the join call here
      callback.queue.push [QUEUE_KIND_META, [CALLBACK_DISCONNECTED,
                                             DISCONNECT_REASON_REQUEST, nil]]
      callback.queue.push [QUEUE_KIND_EXIT, nil]

      if Thread.current != callback.thread
        callback.thread.join
      end
    end

    # Performs an authentication handshake with the connected Brick Daemon or
    # WIFI/Ethernet Extension. If the handshake succeeds the connection switches
    # from non-authenticated to authenticated state and communication can
    # continue as normal. If the handshake fails then the connection gets closed.
    # Authentication can fail if the wrong secret was used or if authentication
    # is not enabled at all on the Brick Daemon or the WIFI/Ethernet Extension.
    #
    # For more information about authentication see
    # https://www.tinkerforge.com/en/doc/Tutorials/Tutorial_Authentication/Tutorial.html
    def authenticate(secret)
      if not secret.ascii_only?
        raise ArgumentError, "Authentication secret contains non-ASCII characters"
      end
      @authentication_mutex.synchronize {
        if @next_authentication_nonce == 0
          @next_authentication_nonce = SecureRandom.random_number(1 << 32)
        end

        server_nonce = @brickd.get_authentication_nonce
        client_nonce = Packer.unpack(Packer.pack([@next_authentication_nonce], 'L'), 'C4')[0]
        @next_authentication_nonce += 1
        nonce_bytes = Packer.pack [server_nonce, client_nonce], 'C4 C4'
        digest_bytes = OpenSSL::HMAC.digest 'sha1', secret, nonce_bytes
        digest = Packer.unpack(digest_bytes, 'C20')[0]

        @brickd.authenticate client_nonce, digest
      }
    end

    # Can return the following states:
    #
    # - CONNECTION_STATE_DISCONNECTED: No connection is established.
    # - CONNECTION_STATE_CONNECTED: A connection to the Brick Daemon or
    #   the WIFI/Ethernet Extension is established.
    # - CONNECTION_STATE_PENDING: IP Connection is currently trying to
    #   connect.
    def get_connection_state
      if @socket != nil
        CONNECTION_STATE_CONNECTED
      elsif @auto_reconnect_pending
        CONNECTION_STATE_PENDING
      else
        CONNECTION_STATE_DISCONNECTED
      end
    end

    # Enables or disables auto-reconnect. If auto-reconnect is enabled,
    # the IP Connection will try to reconnect to the previously given
    # host and port, if the connection is lost.
    #
    # Default value is <tt>true</tt>.
    def set_auto_reconnect(auto_reconnect)
      @auto_reconnect = auto_reconnect

      if not @auto_reconnect
        # Abort potentially pending auto reconnect
        @auto_reconnect_allowed = false
      end
    end

    # Returns <tt>true</tt> if auto-reconnect is enabled, <tt>false</tt>
    # otherwise.
    def get_auto_reconnect
      @auto_reconnect
    end

    # Sets the timeout in seconds for getters and for setters for which
    # the response expected flag is activated.
    #
    # Default timeout is 2.5.
    def set_timeout(timeout)
      @timeout = timeout
    end

    # Returns the timeout as set by set_timeout.
    def get_timeout
      @timeout
    end

    # Broadcasts an enumerate request. All devices will respond with an
    # enumerate callback.
    def enumerate
      request, _, _ = create_packet_header nil, 8, FUNCTION_ENUMERATE

      send_request request
    end

    # Stops the current thread until unwait is called.
    #
    # This is useful if you rely solely on callbacks for events, if you want
    # to wait for a specific callback or if the IP Connection was created in
    # a thread.
    #
    # Wait and unwait act in the same way as "acquire" and "release" of a
    # semaphore.
    def wait
      @waiter_queue.pop
    end

    # Unwaits the thread previously stopped by wait.
    #
    # Wait and unwait act in the same way as "acquire" and "release" of a
    # semaphore.
    def unwait
      @waiter_queue.push nil
    end

    # Registers a callback with ID <tt>id</tt> to the block <tt>block</tt>.
    def register_callback(id, &block)
      callback = block
      @registered_callbacks[id] = callback
    end

    # internal
    def add_device(device)
      @replace_mutex.synchronize {
        replaced_device = @devices.fetch device.uid, nil

        if replaced_device != nil
          replaced_device.replaced = true
        end

        @devices[device.uid] = device # FIXME: use a weakref here
      }
    end

    # internal
    def get_next_sequence_number
      @sequence_number_mutex.synchronize {
        sequence_number = @next_sequence_number + 1
        @next_sequence_number = sequence_number % 15
        sequence_number
      }
    end

    # internal
    def create_packet_header(device, length, function_id)
      uid = 0
      sequence_number = get_next_sequence_number
      response_expected = false
      r_bit = 0

      if device != nil
        uid = device.uid
        response_expected = device.get_response_expected function_id
      end

      if response_expected
        r_bit = 1
      end

      sequence_number_and_options = (sequence_number << 4) | (r_bit << 3)
      header = Packer.pack [uid, length, function_id, sequence_number_and_options, 0], 'L C C C C'

      [header, response_expected, sequence_number]
    end

    # internal
    def send_request(request)
      @socket_mutex.synchronize {
        if @socket == nil
          raise NotConnectedException, 'Not connected'
        end

        begin
          @socket_send_mutex.synchronize {
            @socket.send request, 0
          }
        rescue IOError
          handle_disconnect_by_peer DISCONNECT_REASON_ERROR, @socket_id, true
          raise NotConnectedException, 'Not connected'
        rescue Errno::ECONNRESET
          handle_disconnect_by_peer DISCONNECT_REASON_SHUTDOWN, @socket_id, true
          raise NotConnectedException, 'Not connected'
        end

        @disconnect_probe_flag = false
      }
    end

    private

    FUNCTION_DISCONNECT_PROBE = 128
    FUNCTION_ENUMERATE = 254

    QUEUE_KIND_EXIT = 0
    QUEUE_KIND_META = 1
    QUEUE_KIND_PACKET = 2

    DISCONNECT_PROBE_INTERVAL = 5

    # internal
    def connect_unlocked(is_auto_reconnect)
      # NOTE: Assumes that the socket mutex is locked

      # Create callback queue and thread
      if @callback == nil
        @callback = CallbackContext.new
        @callback.queue = Queue.new
        @callback.mutex = Mutex.new
        @callback.packet_dispatch_allowed = false
        @callback.thread = Thread.new(@callback) do |callback|
          callback_loop callback
        end
        @callback.thread.abort_on_exception = true
      end

      # Create socket
      @socket = TCPSocket.new @host, @port
      @socket.setsockopt(Socket::IPPROTO_TCP, Socket::TCP_NODELAY, 1)
      @socket_id += 1

      # Create disconnect probe thread
      @disconnect_probe_flag = true
      @disconnect_probe_queue = Queue.new
      @disconnect_probe_thread = Thread.new(@disconnect_probe_queue) do |disconnect_probe_queue|
        disconnect_probe_loop disconnect_probe_queue
      end
      @disconnect_probe_thread.abort_on_exception = true

      # Create receive thread
      @callback.packet_dispatch_allowed = true

      @receive_flag = true
      @receive_thread = Thread.new(@socket_id) do |socket_id|
        receive_loop socket_id
      end
      @receive_thread.abort_on_exception = true

      # Trigger connected callback
      if is_auto_reconnect
        connect_reason = CONNECT_REASON_AUTO_RECONNECT
      else
        connect_reason = CONNECT_REASON_REQUEST
      end

      @auto_reconnect_allowed = false
      @auto_reconnect_pending = false

      @callback.queue.push [QUEUE_KIND_META, [CALLBACK_CONNECTED,
                                              connect_reason, nil]]
    end

    # internal
    def disconnect_unlocked
      # NOTE: Assumes that the socket mutex is locked

      # Destroy disconnect probe thread
      @disconnect_probe_queue.push true
      @disconnect_probe_thread.join
      @disconnect_probe_thread = nil

      # Stop dispatching packet callbacks before ending the receive
      # thread to avoid timeout exceptions due to callback functions
      # trying to call getters
      if Thread.current != @callback.thread
        # FIXME: Cannot lock callback mutex here because this can
        #        deadlock due to an ordering problem with the socket mutex
        #@callback.mutex.synchronize {
          @callback.packet_dispatch_allowed = false
        #}
      else
        @callback.packet_dispatch_allowed = false
      end

      # Destroy receive thread
      @receive_flag = false

      @socket.shutdown(Socket::SHUT_RDWR)

      if @receive_thread != nil
        @receive_thread.join
        @receive_thread = nil
      end

      # Destroy socket
      @socket.close
      @socket = nil
    end

    # internal
    def receive_loop(socket_id)
      pending_data = ''

      while @receive_flag
        begin
          result = IO.select [@socket], [], [], 1
        rescue IOError
          # FIXME: handle this error?
          break
        end

        if result == nil or result[0].length < 1
          next
        end

        begin
          data = @socket.recv 8192
        rescue IOError
          handle_disconnect_by_peer DISCONNECT_REASON_ERROR, socket_id, false
          break
        rescue Errno::ECONNRESET
          handle_disconnect_by_peer DISCONNECT_REASON_SHUTDOWN, socket_id, false
          break
        rescue Errno::ESHUTDOWN
          # shutdown was called from disconnect_unlocked
          break
        end

        if not @receive_flag
          break
        end

        if data.length == 0
          if @receive_flag
            handle_disconnect_by_peer DISCONNECT_REASON_SHUTDOWN, socket_id, false
          end
          break
        end

        pending_data += data

        while @receive_flag
          if pending_data.length < 8
            # Wait for complete header
            break
          end

          length = Packer.get_length_from_data pending_data

          if pending_data.length < length
            # Wait for complete packet
            break
          end

          packet = pending_data[0, length]
          pending_data = pending_data[length..-1]

          handle_response packet
        end
      end
    end

    # internal
    def dispatch_meta(function_id, parameter, socket_id)
      if function_id == CALLBACK_CONNECTED
        cb = @registered_callbacks[CALLBACK_CONNECTED]

        if cb != nil
          cb.call parameter
        end
      elsif function_id == CALLBACK_DISCONNECTED
        if parameter != DISCONNECT_REASON_REQUEST
          # Need to do this here, the receive_loop is not allowed to
          # hold the socket_mutex because this could cause a deadlock
          # with a concurrent call to the (dis-)connect function
          @socket_mutex.synchronize {
            # Don't close the socket if it got disconnected or
            # reconnected in the meantime
            if @socket != nil and @socket_id == socket_id
              # Destroy disconnect probe thread
              @disconnect_probe_queue.push true
              @disconnect_probe_thread.join
              @disconnect_probe_thread = nil

              # Destroy socket
              @socket.close
              @socket = nil
            end
          }
        end

        # FIXME: Wait a moment here, otherwise the next connect
        # attempt will succeed, even if there is no open server
        # socket. the first receive will then fail directly
        sleep 0.1

        cb = @registered_callbacks[CALLBACK_DISCONNECTED]

        if cb != nil
          cb.call parameter
        end

        if parameter != DISCONNECT_REASON_REQUEST and @auto_reconnect and @auto_reconnect_allowed
          @auto_reconnect_pending = true
          retry_connect = true

          # Block here until reconnect. this is okay, there is no
          # callback to deliver when there is no connection
          while retry_connect
            retry_connect = false

            @socket_mutex.synchronize {
              if @auto_reconnect_allowed and @socket == nil
                begin
                  connect_unlocked true
                rescue
                  retry_connect = true
                end
              else
                @auto_reconnect_pending = false
              end
            }

            if retry_connect
              sleep 0.1
            end
          end
        end
      end
    end

    # internal
    def dispatch_packet(packet)
      uid = Packer.get_uid_from_data packet
      function_id = Packer.get_function_id_from_data packet

      if function_id == CALLBACK_ENUMERATE
        cb = @registered_callbacks[CALLBACK_ENUMERATE]

        if cb == nil
          return
        end

        if packet.length != 34
          return # silently ignoring callback with wrong length
        end

        payload = Packer.unpack packet[8..-1], 'Z8 Z8 k C3 C3 S C'

        cb.call(*payload)
        return
      end

      device = @devices[uid]

      if device != nil
        begin
          device.check_validity
        rescue TinkerforgeException
          return # silently ignoring callback for invalid device
        end

        if device.high_level_callbacks.has_key?(-function_id)
          hlcb = device.high_level_callbacks[-function_id] # [roles, options, data]
          format = device.callback_formats[function_id] # FIXME: currently assuming that low-level callback has more than one element

          if packet.length != format[0]
            return # silently ignoring callback with wrong length
          end

          payload = Packer.unpack packet[8..-1], format[1]
          has_data = false
          data = nil

          if hlcb[1]['fixed_length'] != nil
            length = hlcb[1]['fixed_length']
          else
            length = payload[hlcb[0].index 'stream_length']
          end

          if not hlcb[1]['single_chunk']
            chunk_offset = payload[hlcb[0].index 'stream_chunk_offset']
          else
            chunk_offset = 0
          end

          chunk_data = payload[hlcb[0].index 'stream_chunk_data']

          if hlcb[2] == nil # no stream in-progress
            if chunk_offset == 0 # stream starts
              hlcb[2] = chunk_data

              if hlcb[2].length >= length # stream complete
                has_data = true
                data = hlcb[2][0, length]
                hlcb[2] = nil
              else # ignore tail of current stream, wait for next stream start
              end
            else # stream in-progress
              if chunk_offset != hlcb[2].length # stream out-of-sync
                has_data = true
                data = nil
                hlcb[2] = nil
              else # stream in-sync
                hlcb[2] += chunk_data

                if hlcb[2].length >= length # stream complete
                  has_data = true
                  data = hlcb[2][0, length]
                  hlcb[2] = nil
                end
              end
            end

            cb = device.registered_callbacks[-function_id]

            if has_data and cb != nil
              result = []

              hlcb[0].zip(payload).each do |role, value|
                if role == 'stream_chunk_data'
                  result << data
                elsif role == nil
                  result << value
                end
              end

              cb.call(*result)
            end
          end
        end

        cb = device.registered_callbacks[function_id]

        if cb != nil
          format = device.callback_formats[function_id]

          if format == nil
            return # silently ignore registered but unknown callback
          end

          if packet.length != format[0]
            return # silently ignoring callback with wrong length
          end

          payload = Packer.unpack packet[8..-1], format[1]

          cb.call(*payload)
        end
      end
    end

    # internal
    def callback_loop(callback)
      alive = true

      while alive
        kind, data = callback.queue.pop

        # FIXME: Cannot lock callback mutex here because this can
        #        deadlock due to an ordering problem with the socket mutex
        # callback.mutex.synchronize {
          if kind == QUEUE_KIND_EXIT
            alive = false
          elsif kind == QUEUE_KIND_META
            function_id, parameter, socket_id = data

            dispatch_meta function_id, parameter, socket_id
          elsif kind == QUEUE_KIND_PACKET
            # don't dispatch callbacks when the receive thread isn't running
            if callback.packet_dispatch_allowed
              dispatch_packet data
            end
          end
        #}
      end
    end

    # internal
    def disconnect_probe_loop(disconnect_probe_queue)
      # NOTE: the disconnect probe thread is not allowed to hold the socket_mutex at any
      #       time because it is created and joined while the socket_mutex is locked

      request, _, _ = create_packet_header nil, 8, FUNCTION_DISCONNECT_PROBE

      while true
        begin
          Timeout::timeout(DISCONNECT_PROBE_INTERVAL) {
            disconnect_probe_queue.pop
          }
        rescue Timeout::Error
          if @disconnect_probe_flag
            begin
              @socket_send_mutex.synchronize {
                @socket.send request, 0
              }
            rescue IOError
              handle_disconnect_by_peer DISCONNECT_REASON_ERROR, @socket_id, false
              break
            rescue Errno::ECONNRESET
              handle_disconnect_by_peer DISCONNECT_REASON_SHUTDOWN, @socket_id, false
              break
            end
          else
            @disconnect_probe_flag = true
          end
          next
        end
        break
      end
    end

    # internal
    def handle_disconnect_by_peer(disconnect_reason, socket_id, disconnect_immediately)
      # NOTE: assumes that socket_mutex is locked if disconnect_immediately is true

      @auto_reconnect_allowed = true

      if disconnect_immediately
        disconnect_unlocked
      end

      @callback.queue.push [QUEUE_KIND_META, [CALLBACK_DISCONNECTED,
                                              disconnect_reason, socket_id]]
    end

    # internal
    def handle_response(packet)
      @disconnect_probe_flag = false

      function_id = Packer.get_function_id_from_data packet
      sequence_number = Packer.get_sequence_number_from_data packet

      if sequence_number == 0 and function_id == CALLBACK_ENUMERATE
        if @registered_callbacks.has_key? CALLBACK_ENUMERATE
          @callback.queue.push [QUEUE_KIND_PACKET, packet]
        end
        return
      end

      uid = Packer.get_uid_from_data packet
      device = @devices[uid]

      if device != nil
        if sequence_number == 0
          if device.registered_callbacks.has_key? function_id or \
             device.high_level_callbacks.has_key?(-function_id)
            @callback.queue.push [QUEUE_KIND_PACKET, packet]
          end
        elsif device.expected_response_function_id == function_id and \
              device.expected_response_sequence_number == sequence_number
          device.enqueue_response packet
        else
        end
      end
    end
  end
end
