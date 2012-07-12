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

  class Device
    RESPONSE_TIMEOUT = 2.5

    attr_accessor :uid
    attr_accessor :stack_id
    attr_accessor :expected_name
    attr_accessor :name
    attr_accessor :firmware_version
    attr_accessor :ipcon
    attr_accessor :expected_response_function_id
    attr_accessor :expected_response_length
    attr_accessor :callback_formats
    attr_accessor :registered_callbacks

    def initialize(uid)
      @uid = Base58.decode uid
      @stack_id = 0
      @expected_name = ''
      @name = ''

      @firmware_version = [0, 0, 0]
      @binding_version = [0, 0, 0]

      @ipcon = nil

      @request_mutex = Mutex.new

      @expected_response_function_id = 0
      @expected_response_length = 0

      @response_mutex = Mutex.new
      @response_condition = ConditionVariable.new
      @response_queue = Queue.new

      @callback_formats = {}
      @registered_callbacks = {}
    end

    def send_request(function_id, request_data, request_format,
                     response_length, response_format)
      if @ipcon == nil
        raise Exception, 'Not added to IPConnection'
      end

      payload = ''
      response = nil

      if request_data.length > 0
        payload = pack request_data, request_format
      end

      request = pack([@stack_id, function_id, 4 + payload.length], 'C C S') + payload

      @request_mutex.synchronize {
        if response_length > 0
          @expected_response_function_id = function_id
          @expected_response_length = 4 + response_length
        else
          @expected_response_function_id = 0
          @expected_response_length = 0
        end

        @ipcon.send request

        if response_length > 0
          packet = dequeue_response
          response = unpack packet[4..-1], response_format

          if response.length == 1
            response = response[0]
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
        @response_condition.wait @response_mutex, RESPONSE_TIMEOUT
        if @response_queue.empty?
          raise TimeoutException, message
        end
        response = @response_queue.pop
      }

      response
    end
  end

  class IPConnection
    BROADCAST_ADDRESS = 0

    FUNCTION_GET_STACK_ID = 255
    FUNCTION_ENUMERATE = 254
    FUNCTION_ENUMERATE_CALLBACK = 253

    def initialize(host, port)
      @socket = TCPSocket.new host, port

      @devices = {}
      @pending_add_device = nil
      @add_device_mutex = Mutex.new

      @enumerate_callback = nil
      @callback_queue = Queue.new

      @thread_run_flag = true
      @thread_receive = Thread.new { receive_loop }
      @thread_callback = Thread.new { callback_loop }
    end

    def add_device(device)
      @add_device_mutex.synchronize {
        request = pack [BROADCAST_ADDRESS, FUNCTION_GET_STACK_ID, 4 + 8, device.uid], 'C C S Q'
        @pending_add_device = device

        send request

        begin
          device.dequeue_response "Could not add device #{Base58.encode(device.uid)}, timeout"
        ensure
          @pending_add_device = nil
        end

        device.ipcon = self
      }
    end

    def join_thread
      @thread_receive.join
      @thread_callback.join
    end

    def destroy
      @thread_run_flag = false
      @callback_queue.push nil # unblock callback_loop
      @socket.shutdown(Socket::SHUT_RDWR)
      @socket.close
    end

    def enumerate(&block)
      @enumerate_callback = block

      send pack([BROADCAST_ADDRESS, FUNCTION_ENUMERATE, 4], 'C C S')
    end

    def send(request)
      @socket.send request, 0
    end

    private
    def receive_loop
      pending_data = ''

      while @thread_run_flag
        data = @socket.recv 8192

        if data.length == 0
          if @thread_run_flag
            $stderr.puts 'Socket disconnected by Server, destroying IPConnection'
            destroy
          end
          return
        end

        pending_data += data

        while true
          if pending_data.length < 4
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

    def callback_loop
      while @thread_run_flag
        packet = @callback_queue.pop

        if packet == nil
          next
        end

        stack_id = get_stack_id_from_data packet
        function_id = get_function_id_from_data packet

        if function_id == FUNCTION_ENUMERATE_CALLBACK
          payload = unpack packet[4..-1], 'Q Z40 C ?'

          uid = Base58::encode(payload[0])
          name = payload[1]
          stack_id = payload[2]
          is_new = payload[3]

          @enumerate_callback.call uid, name, stack_id, is_new
        else
          device = @devices[stack_id]

          if device.registered_callbacks.has_key? function_id
            payload = unpack packet[4..-1], device.callback_formats[function_id]
            device.registered_callbacks[function_id].call(*payload)
          end
        end
      end
    end

    def get_stack_id_from_data data
      data[0, 1].ord
    end

    def get_function_id_from_data data
      data[1, 1].ord
    end

    def get_length_from_data data
      data[2, 2].unpack('S<')[0]
    end

    def handle_response(packet)
      function_id = get_function_id_from_data packet

      if function_id == FUNCTION_GET_STACK_ID
        handle_add_device packet
        return
      end

      if function_id == FUNCTION_ENUMERATE_CALLBACK
        handle_enumerate packet
        return
      end

      stack_id = get_stack_id_from_data packet
      length = get_length_from_data packet

      if !@devices.has_key? stack_id
        # Response from an unknown device, ignoring it
        return
      end

      device = @devices[stack_id]
      if function_id == device.expected_response_function_id
        if length != device.expected_response_length
          $stderr.puts "Received malformed packet from #{stack_id}, ignoring it"
          return
        end

        device.enqueue_response packet
        return
      end

      if device.registered_callbacks.has_key? function_id
        @callback_queue.push packet
        return
      end

      # Response seems to be OK, but can't be handled, most likely
      # a callback without registered block
    end

    def handle_add_device(packet)
      if @pending_add_device == nil
        return
      end

      payload = unpack packet[4..-1], 'Q C C C Z40 C'

      if @pending_add_device.uid == payload[0]
        name = payload[4]
        i = name.rindex ' '

        if i == nil or name[0, i].gsub('-', ' ') != @pending_add_device.expected_name.gsub('-', ' ')
          return
        end

        @pending_add_device.firmware_version = [payload[1], payload[2], payload[3]]
        @pending_add_device.name = name
        @pending_add_device.stack_id = payload[5]
        @devices[payload[5]] = @pending_add_device
        @pending_add_device.enqueue_response nil
        @pending_add_device = nil
      end
    end

    def handle_enumerate(packet)
      if @enumerate_callback != nil
        @callback_queue.push packet
      end
    end
  end
end
