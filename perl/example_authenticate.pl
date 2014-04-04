#!/usr/bin/perl

use Tinkerforge::IPConnection;

use constant HOST => 'localhost';
use constant PORT => 4223;
use constant SECRET => 'My Authentication Secret!';

# Create IPConnection
our $ipcon = Tinkerforge::IPConnection->new();

# Authenticate each time the connection got (re-)established
sub cb_connected
{
	my ($connect_reason) = @_;

	if ($connect_reason == $ipcon->CONNECT_REASON_REQUEST)
	{
		print "Connected by request\n";
	}
	elsif ($connect_reason == $ipcon->CONNECT_REASON_AUTO_RECONNECT)
	{
		print "Auto-Reconnect\n";
	}

	# Authenticate first...
	eval
	{
		$ipcon->authenticate(&SECRET);
		print "Authentication succeeded\n";
	};
	if ($!)
	{
		print "Could not authenticate: $!\n";
		return;
	}

	# ...then trigger Enumerate
	$ipcon->enumerate();
}

# Print incoming enumeration
sub cb_enumerate
{
	my ($uid, $connected_uid, $position, $hardware_version,
	    $firmware_version, $device_identifier, $enumeration_type) = @_;

	print "UID: $uid, Enumeration Type: $enumeration_type\n";
}

# Register Connected Callback
$ipcon->register_callback($ipcon->CALLBACK_CONNECTED, 'cb_connected');

# Register Enumerate Callback
$ipcon->register_callback($ipcon->CALLBACK_ENUMERATE, 'cb_enumerate');

# Connect to brickd
$ipcon->connect(&HOST, &PORT);

print "Press any key to exit...\n";
<STDIN>;
$ipcon->disconnect();
