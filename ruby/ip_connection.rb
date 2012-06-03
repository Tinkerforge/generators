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
          data = wait_for_response
          response = unpack data[4, data.length - 4], response_format

          if response.length == 1
            response = response[0]
          end
        end
      }

      response
    end

    def wait_for_response(message = 'Did not receive response in time')
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

    def enqueue_response response
      @response_mutex.synchronize {
        @response_queue.push response
        @response_condition.signal
      }
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

      @enumerate_callback = nil
      @callback_queue = Queue.new

      @recv_loop_flag = true
      @thread_recv = Thread.new { recv_loop }
      @thread_callback = Thread.new { callback_loop }
    end

    def add_device(device)
      request = pack [BROADCAST_ADDRESS, FUNCTION_GET_STACK_ID, 4 + 8, device.uid], 'C C S Q'
      @pending_add_device = device

      send request

      begin
        device.wait_for_response "Could not add device #{Base58.encode(device.uid)}, timeout"
      ensure
        @pending_add_device = nil
      end

      device.ipcon = self
    end

    def join_thread
      @thread_recv.join
      @thread_callback.join
    end

    def destroy
      @recv_loop_flag = false
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
    def recv_loop
      while @recv_loop_flag
        data = @socket.recv 8192

        if data.length == 0
          if @recv_loop_flag
            $stderr.puts 'Socket disconnected by Server, destroying ipcon'
            destroy
          end
          return
        end

        while data.length > 0
          handled = handle_message data
          data = data[handled..-1]
        end
      end
    end

    def callback_loop
      while @recv_loop_flag
        data = @callback_queue.pop

        if data == nil
          next
        end

        stack_id = get_stack_id_from_data data
        function_id = get_function_id_from_data data
        length = get_length_from_data data

        if function_id == FUNCTION_ENUMERATE_CALLBACK
          payload = unpack data[4, length - 4], 'Q Z40 C ?'

          uid = Base58::encode(payload[0])
          name = payload[1]
          stack_id = payload[2]
          is_new = payload[3]

          @enumerate_callback.call uid, name, stack_id, is_new
        else
          device = @devices[stack_id]

          if device.registered_callbacks.has_key? function_id
            payload = unpack data[4, length - 4], device.callback_formats[function_id]
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

    def handle_message(data)
      function_id = get_function_id_from_data data

      if function_id == FUNCTION_GET_STACK_ID
        return handle_add_device data
      end

      if function_id == FUNCTION_ENUMERATE_CALLBACK
        return handle_enumerate data
      end

      stack_id = get_stack_id_from_data data
      length = get_length_from_data data

      if !@devices.has_key? stack_id
        # Message for an unknown device, ignoring it
        return length
      end

      device = @devices[stack_id]
      if function_id == device.expected_response_function_id
        if length != device.expected_response_length
          $stderr.puts "Received malformed message, discarded: #{stack_id}"
          return length
        end

        device.enqueue_response data
        return length
      end

      if device.registered_callbacks.has_key? function_id
        @callback_queue.push data
        return length
      end

      # Message seems to be OK, but can't be handled, most likely
      # a callback without registered function
      length
    end

    def handle_add_device(data)
      length = get_length_from_data data

      if @pending_add_device == nil
        return length
      end

      payload = unpack data[4, length - 4], 'Q C C C Z40 C'

      if @pending_add_device.uid == payload[0]
        name = payload[4]
        i = name.rindex ' '

        if i == nil or name[0, i].gsub('-', ' ') != @pending_add_device.expected_name.gsub('-', ' ')
          return length
        end

        @pending_add_device.firmware_version = [payload[1], payload[2], payload[3]]
        @pending_add_device.name = name
        @pending_add_device.stack_id = payload[5]
        @devices[payload[5]] = @pending_add_device
        @pending_add_device.enqueue_response nil
        @pending_add_device = nil
      end

      length
    end

    def handle_enumerate(data)
      length = get_length_from_data data

      if @enumerate_callback == nil
        return length
      end

      @callback_queue.push data

      length
    end
  end
end
