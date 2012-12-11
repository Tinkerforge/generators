# -*- ruby encoding: utf-8 -*-
# Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
#
# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted.

require 'socket'
require 'thread'

module Tinkerforge
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
        value += index * base
        base *= 58
      end
      value
    end
  end

  class TimeoutException < RuntimeError
  end

  class NotSupportedException < RuntimeError
  end

  def pack(unpacked, format)
    data = ''
    format.split(' ').each do |f|
      if f.length > 1
        f0 = f[0, 1]
        f1 = f[1..-1]
        r = []

        if f0 == '?'
          unpacked[0].each { |b| r << b ? 1 : 0 }
          data += r.pack "C#{f1}"
        elsif f0 == 'k'
          unpacked[0].each { |c| r << c.ord }
          data += r.pack "c#{f1}"
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
          data += r.pack 'c'
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

  def unpack(data, format)
    unpacked = []
    format.split(' ').each do |f|
      if f.length > 1
        f0 = f[0, 1]
        f1 = f[1..-1]
        u = []

        if f0 == '?'
          r = data.unpack "C#{f1}a*"
          data = r[-1]
          r.delete_at(-1)
          r.each { |b| u << b != 0 }
        elsif f0 == 'k'
          r = data.unpack "c#{f1}a*"
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
          r.each { |i| u << i }
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
          r = data.unpack "ca*"
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

  def get_uid_from_data(data)
    data[0, 4].unpack('L<')[0]
  end

  def get_length_from_data(data)
    data[4, 1].unpack('C<')[0]
  end

  def get_function_id_from_data(data)
    data[5, 1].unpack('C<')[0]
  end

  def get_sequence_number_from_data(data)
    (data[6, 1].unpack('C<')[0] >> 4) & 0x0F
  end

  def get_error_code_from_data(data)
    (data[7, 1].unpack('C<')[0] >> 6) & 0x03
  end

  class Device
    RESPONSE_EXPECTED_INVALID_FUNCTION_ID = 0
    RESPONSE_EXPECTED_ALWAYS_TRUE = 1 # getter
    RESPONSE_EXPECTED_ALWAYS_FALSE = 2 # callback
    RESPONSE_EXPECTED_TRUE = 3 # setter
    RESPONSE_EXPECTED_FALSE = 4 # setter, default

    attr_accessor :uid
    attr_accessor :expected_response_function_id
    attr_accessor :expected_response_sequence_number
    attr_accessor :callback_formats
    attr_accessor :registered_callbacks

    def initialize(uid, ipcon)
      @uid = Base58.decode uid

      if @uid > 0xFFFFFFFF
        # convert from 64bit to 32bit
        value1 = @uid & 0xFFFFFFFF
        value2 = (@uid >> 32) & 0xFFFFFFFF

        @uid  = (value1 & 0x3F000000) << 2
        @uid |= (value1 & 0x000F0000) << 6
        @uid |= (value1 & 0x0000003F) << 16
        @uid |= (value2 & 0x0F000000) >> 12
        @uid |= (value2 & 0x00000FFF)
      end

      @api_version = [0, 0, 0]

      @ipcon = ipcon

      @request_mutex = Mutex.new

      @response_expected = Array.new(256, RESPONSE_EXPECTED_INVALID_FUNCTION_ID)
      @response_expected[IPConnection::FUNCTION_ENUMERATE] = RESPONSE_EXPECTED_FALSE
      @response_expected[IPConnection::CALLBACK_ENUMERATE] = RESPONSE_EXPECTED_ALWAYS_FALSE

      @expected_response_function_id = 0
      @expected_response_sequence_number = 0

      @response_mutex = Mutex.new
      @response_condition = ConditionVariable.new
      @response_queue = Queue.new

      @callback_formats = {}
      @registered_callbacks = {}

      @ipcon.devices[@uid] = self # FIXME: should use a weakref here
    end

    def get_response_expected(function_id)
      if function_id < 0 or function_id > 255
        raise ArgumentError, "Invalid function ID #{function_id}"
      end

      if @response_expected[function_id] == RESPONSE_EXPECTED_ALWAYS_TRUE or \
         @response_expected[function_id] == RESPONSE_EXPECTED_TRUE
        true
      elsif @response_expected[function_id] == RESPONSE_EXPECTED_ALWAYS_FALSE or \
            @response_expected[function_id] == RESPONSE_EXPECTED_FALSE
        false
      else
        raise ArgumentError, "Invalid function ID #{function_id}"
      end
    end

    def set_response_expected(function_id, response_expected)
      if function_id < 0 or function_id > 255
        raise ArgumentError, "Invalid function ID #{function_id}"
      end

      if @response_expected[function_id] == RESPONSE_EXPECTED_TRUE or \
         @response_expected[function_id] == RESPONSE_EXPECTED_FALSE
        if response_expected
          @response_expected[function_id] = RESPONSE_EXPECTED_TRUE
        else
          @response_expected[function_id] = RESPONSE_EXPECTED_FALSE
        end
      elsif @response_expected[function_id] == RESPONSE_EXPECTED_ALWAYS_TRUE or \
            @response_expected[function_id] == RESPONSE_EXPECTED_ALWAYS_FALSE
        raise ArgumentError, "Response Expected flag cannot be changed for function ID #{function_id}"
      else
        raise ArgumentError, "Invalid function ID #{function_id}"
      end
    end

    def set_response_expected_all(response_expected)
      for function_id in 0..255
        if @response_expected[function_id] == RESPONSE_EXPECTED_TRUE or \
           @response_expected[function_id] == RESPONSE_EXPECTED_FALSE
          if response_expected
            @response_expected[function_id] = RESPONSE_EXPECTED_TRUE
          else
            @response_expected[function_id] = RESPONSE_EXPECTED_FALSE
          end
        end
      end
    end

    def get_api_version
      @api_version
    end

    def send_request(function_id, request_data, request_format,
                     response_length, response_format)
      response = nil

      @request_mutex.synchronize {
        response_expected = false

        @ipcon.socket_mutex.synchronize {
          if @ipcon.socket == nil
            raise Exception, 'Not connected'
          end

          if request_data.length > 0
            payload = pack request_data, request_format
          else
            payload = ''
          end

          header, response_expected, sequence_number = \
            @ipcon.create_packet_header self, 8 + payload.length, function_id
          request = header + payload

          if response_expected
            @expected_response_function_id = function_id
            @expected_response_sequence_number = sequence_number
          end

          @ipcon.socket.send request, 0
        }

        if response_expected
          packet = dequeue_response
          error_code = get_error_code_from_data(packet)

          @expected_response_function_id = 0
          @expected_response_sequence_number = 0

          if error_code == 0
            # no error
          elsif error_code == 1
            raise NotSupportedException, "Got invalid parameter for function #{function_id}"
          elsif error_code == 2
            raise NotSupportedException, "Function #{function_id} is not supported"
          else
            raise NotSupportedException, "Function #{function_id} returned an unknown error"
          end

          if response_length > 0
            response = unpack packet[8..-1], response_format

            if response.length == 1
              response = response[0]
            end
          end
        end
      }

      response
    end

    def enqueue_response(response)
      @response_mutex.synchronize {
        @response_queue.push response
        @response_condition.signal
      }
    end

    def dequeue_response(message = 'Did not receive response in time')
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
  end

  class IPConnection
    attr_accessor :socket
    attr_accessor :socket_mutex
    attr_accessor :devices
    attr_accessor :timeout

    FUNCTION_ENUMERATE = 254
    CALLBACK_ENUMERATE = 253

    CALLBACK_CONNECTED = 0
    CALLBACK_DISCONNECTED = 1
    CALLBACK_AUTHENTICATION_ERROR = 2

    # enumeration_type parameter for CALLBACK_ENUMERATE
    ENUMERATION_TYPE_AVAILABLE = 0
    ENUMERATION_TYPE_CONNECTED = 1
    ENUMERATION_TYPE_DISCONNECTED = 2

    # connect_reason parameter for CALLBACK_CONNECTED
    CONNECT_REASON_REQUEST = 0,
    CONNECT_REASON_AUTO_RECONNECT = 1

    # disconnect_reason parameter for CALLBACK_DISCONNECTED
    DISCONNECT_REASON_REQUEST = 0
    DISCONNECT_REASON_ERROR = 1
    DISCONNECT_REASON_SHUTDOWN = 2

    # returned by get_connection_state
    CONNECTION_STATE_DISCONNECTED = 0
    CONNECTION_STATE_CONNECTED = 1
    CONNECTION_STATE_PENDING = 2 # auto-reconnect in progress

    # Creates an IP connection to the Brick Daemon with the given *host*
    # and *port*. With the IP connection itself it is possible to enumerate the
    # available devices. Other then that it is only used to add Bricks and
    # Bricklets to the connection.
    def initialize
      @host = nil
      @port = 0

      @timeout = 2500

      @auto_reconnect = true
      @auto_reconnect_allowed = false
      @auto_reconnect_pending = false

      @next_sequence_number = 0

      @devices = {}

      @registered_callbacks = {}

      @socket_mutex = Mutex.new
      @socket = nil

      @receive_flag = false
      @receive_thread = nil

      @callback_queue = nil
      @callback_thread = nil
    end

    def connect(host, port)
      @socket_mutex.synchronize {
        if @socket != nil
          raise Exception, 'Already connected'
        end

        @host = host
        @port = port

        connect_unlocked false
      }
    end

    def disconnect
      callback_queue = nil
      callback_thread = nil

      @socket_mutex.synchronize {
        @auto_reconnect_allowed = false

        if @auto_reconnect_pending
          # Abort pending auto reconnect
          @auto_reconnect_pending = false
        else
          if @socket == nil
            raise Exception, 'Not connected'
          end

          # Destroy receive thread
          @receive_flag = false

          @socket.shutdown(Socket::SHUT_RDWR)

          if Thread.current != @receive_thread
            @receive_thread.join
          end

          @receive_thread = nil

          # Destroy socket
          @socket.close
          @socket = nil
        end

        # Destroy callback thread
        callback_queue = @callback_queue
        callback_thread = @callback_thread

        @callback_queue = nil
        @callback_thread = nil
      }

      # Do this outside of socket_mutex to allow calling (dis-)connect from
      # the callbacks while blocking on the join call here
      callback_queue.push [QUEUE_KIND_META, [CALLBACK_DISCONNECTED, DISCONNECT_REASON_REQUEST]]
      callback_queue.push [QUEUE_KIND_EXIT, nil]

      if Thread.current != callback_thread
        callback_thread.join
      end
    end

    def get_connection_state
      if @socket != nil
        CONNECTION_STATE_CONNECTED
      elsif @auto_reconnect_pending
        CONNECTION_STATE_PENDING
      else
        CONNECTION_STATE_DISCONNECTED
      end
    end

    def set_auto_reconnect(auto_reconnect)
      @auto_reconnect = auto_reconnect

      if not @auto_reconnect
        # Abort potentially pending auto reconnect
        @auto_reconnect_allowed = false
      end
    end

    def get_auto_reconnect
      @auto_reconnect
    end

    def set_timeout(timeout)
      @timeout = timeout
    end

    def get_timeout
      @timeout
    end

    # This method registers a callback that receives four parameters:
    #
    # * *uid* - str: The UID of the device.
    # * *name* - str: The name of the device (includes "Brick" or "Bricklet" and a version number).
    # * *stack_id* - int: The stack ID of the device (you can find out the position in a stack with this).
    # * *is_new* - bool: True if the device is added, false if it is removed.
    #
    # There are three different possibilities for the callback to be called.
    # Firstly, the callback is called with all currently available devices in the
    # IP connection (with *is_new* true). Secondly, the callback is called if
    # a new Brick is plugged in via USB (with *is_new* true) and lastly it is
    # called if a Brick is unplugged (with *is_new* false).
    #
    # It should be possible to implement "plug 'n play" functionality with this
    # (as is done in Brick Viewer).
    def enumerate
      @socket_mutex.synchronize {
        if @socket == nil
          raise Exception, 'Not connected'
        end

        request, _, _ = create_packet_header nil, 8, FUNCTION_ENUMERATE

        @socket.send request, 0
      }
    end

    # Registers a callback with ID <tt>id</tt> to the block <tt>block</tt>.
    def register_callback(id, &block)
      callback = block
      @registered_callbacks[id] = callback
    end

    def get_next_sequence_number
      # NOTE: Assumes that the socket mutex is locked
      sequence_number = @next_sequence_number
      @next_sequence_number = (@next_sequence_number + 1) % 15

      sequence_number + 1
    end

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
      header = pack [uid, length, function_id, sequence_number_and_options, 0], 'L C C C C'

      [header, response_expected, sequence_number]
    end

    private

    QUEUE_KIND_EXIT = 0
    QUEUE_KIND_META = 1
    QUEUE_KIND_PACKET = 2

    def connect_unlocked(is_auto_reconnect)
      # NOTE: Assumes that the socket mutex is locked

      # Create callback queue and thread
      if @callback_thread == nil
        @callback_queue = Queue.new
        @callback_thread = Thread.new(@callback_queue) do |queue|
          callback_loop queue
        end
        @callback_thread.abort_on_exception = true
      end

      # Create socket
      @socket = TCPSocket.new @host, @port

      # Create receive thread
      @receive_flag = true
      @receive_thread = Thread.new { receive_loop }
      @receive_thread.abort_on_exception = true

      # Trigger connected callback
      if is_auto_reconnect
        connect_reason = CONNECT_REASON_AUTO_RECONNECT
      else
        connect_reason = CONNECT_REASON_REQUEST
      end

      @auto_reconnect_allowed = false;
      @auto_reconnect_pending = false;

      @callback_queue.push [QUEUE_KIND_META, [CALLBACK_CONNECTED, connect_reason]]
    end

    def receive_loop
      pending_data = ''

      while @receive_flag
        begin
          result = IO.select [@socket], [], [], 1
        rescue IOError
          break
        end

        if result == nil or result[0].length < 1
          next
        end

        begin
          data = @socket.recv 8192
        rescue IOError
          @auto_reconnect_allowed = true
          @receive_flag = false
          @callback_queue.push [QUEUE_KIND_META, [CALLBACK_DISCONNECTED, DISCONNECT_REASON_ERROR]]
          break
        end

        if data.length == 0
          if @receive_flag
            @auto_reconnect_allowed = true
            @receive_flag = false
            @callback_queue.push [QUEUE_KIND_META, [CALLBACK_DISCONNECTED, DISCONNECT_REASON_SHUTDOWN]]
          end
          break
        end

        pending_data += data

        while true
          if pending_data.length < 8
            # Wait for complete header
            break
          end

          length = get_length_from_data pending_data

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

    def dispatch_meta(function_id, parameter)
      if function_id == CALLBACK_CONNECTED
        if @registered_callbacks.has_key? CALLBACK_CONNECTED
          @registered_callbacks[CALLBACK_CONNECTED].call parameter
        end
      elsif function_id == CALLBACK_DISCONNECTED
        # need to do this here, the receive_loop is not allowed to
        # hold the socket_lock because this could cause a deadlock
        # with a concurrent call to the (dis-)connect function
        @socket_mutex.synchronize {
          if @socket != nil
            @socket.close
            @socket = nil
          end
        }

        # FIXME: wait a moment here, otherwise the next connect
        # attempt will succeed, even if there is no open server
        # socket. the first receive will then fail directly
        sleep 0.1

        if @registered_callbacks.has_key? CALLBACK_DISCONNECTED
          @registered_callbacks[CALLBACK_DISCONNECTED].call parameter
        end

        if parameter != DISCONNECT_REASON_REQUEST and @auto_reconnect and @auto_reconnect_allowed
          @auto_reconnect_pending = true
          retry_connect = true

          # block here until reconnect. this is okay, there is no
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

    def dispatch_packet(packet)
      uid = get_uid_from_data packet
      length = get_length_from_data packet
      function_id = get_function_id_from_data packet

      if function_id == CALLBACK_ENUMERATE and \
         @registered_callbacks.has_key? CALLBACK_ENUMERATE
        payload = unpack packet[8..-1], 'Z8 Z8 k C3 C3 S C'
        @registered_callbacks[CALLBACK_ENUMERATE].call(*payload)
      elsif @devices.has_key? uid
        device = @devices[uid]

        if device.registered_callbacks.has_key? function_id
          payload = unpack packet[8..-1], device.callback_formats[function_id]
          device.registered_callbacks[function_id].call(*payload)
        end
      end
    end

    def callback_loop(callback_queue)
      while true
        kind, data = callback_queue.pop

        if kind == QUEUE_KIND_EXIT
          break
        elsif kind == QUEUE_KIND_META
          function_id, parameter = data

          dispatch_meta function_id, parameter
        elsif kind == QUEUE_KIND_PACKET
          # don't dispatch callbacks when the receive thread isn't running
          if @receive_flag
            dispatch_packet data
          end
        end
      end
    end

    def handle_response(packet)
      uid = get_uid_from_data packet
      function_id = get_function_id_from_data packet
      sequence_number = get_sequence_number_from_data packet

      if sequence_number == 0 and function_id == CALLBACK_ENUMERATE
        if @registered_callbacks.has_key? CALLBACK_ENUMERATE
          @callback_queue.push [QUEUE_KIND_PACKET, packet]
        end
      elsif @devices.has_key? uid
        device = @devices[uid]

        if sequence_number == 0
          if device.registered_callbacks.has_key? function_id
            @callback_queue.push [QUEUE_KIND_PACKET, packet]
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
