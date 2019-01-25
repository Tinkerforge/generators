#!/usr/bin/env ruby
# -*- ruby encoding: utf-8 -*-

require 'tinkerforge/ip_connection'

include Tinkerforge

HOST = 'localhost'
PORT = 4223
SECRET = 'My Authentication Secret!'

# Create IP connection
ipcon = IPConnection.new

# Disable auto reconnect mechanism, in case we have the wrong secret. If the authentication is successful, reenable it.
ipcon.set_auto_reconnect false

# Authenticate each time the connection got (re-)established
ipcon.register_callback(IPConnection::CALLBACK_CONNECTED) do |connect_reason|
  case connect_reason
    when IPConnection::CONNECT_REASON_REQUEST
      puts 'Connected by request'
    when IPConnection::CONNECT_REASON_AUTO_RECONNECT
      puts 'Auto-Reconnect'
  end

  # Authenticate first...
  begin
    ipcon.authenticate SECRET
    puts 'Authentication succeeded'

    # ...reenable auto reconnect mechanism, as described below...
    ipcon.set_auto_reconnect true
    
    # ...then trigger enumerate
    ipcon.enumerate
  rescue
    puts 'Could not authenticate'
  end
end

# Print incoming enumeration
ipcon.register_callback(IPConnection::CALLBACK_ENUMERATE) do |uid, connected_uid, position,
                                                              hardware_version, firmware_version,
                                                              device_identifier, enumeration_type|
  puts "UID: #{uid}, Enumeration Type: #{enumeration_type}"
end

# Connecte to brickd
ipcon.connect HOST, PORT

puts 'Press key to exit'
$stdin.gets
ipcon.disconnect
