#!/usr/bin/env ruby
# -*- ruby encoding: utf-8 -*-

require 'tinkerforge/ip_connection'

include Tinkerforge

HOST = 'localhost'
PORT = 4223

# Create IP connection to brickd
ipcon = IPConnection.new
ipcon.connect HOST, PORT

# Enumerate Bricks and Bricklets
ipcon.register_callback(IPConnection::CALLBACK_ENUMERATE) do |uid, connected_uid, position,
                                                              hardware_version, firmware_version,
                                                              device_identifier, enumeration_type|
  puts "UID:               #{uid}"
  puts "Enumeration Type:  #{enumeration_type}"

  if enumeration_type != IPConnection::ENUMERATION_TYPE_DISCONNECTED
    puts "Connected UID:     #{connected_uid}"
    puts "Position:          #{position}"
    puts "Hardware Version:  #{hardware_version}"
    puts "Firmware Version:  #{firmware_version}"
    puts "Device Identifier: #{device_identifier}"
  end

  puts ''
end

ipcon.enumerate

puts 'Press key to exit'
$stdin.gets
ipcon.disconnect
