#!/usr/bin/perl

use Tinkerforge::IPConnection;

use constant HOST => 'localhost';
use constant PORT => 4223;

# Print incoming enumeration
sub cb_enumerate
{
	my ($uid, $connected_uid, $position, $hardware_version,
	    $firmware_version, $device_identifier, $enumeration_type) = @_;

	print "UID:               $uid\n";
	print "Enumeration Type:  $enumeration_type\n";

	if ($enumeration_type == Tinkerforge::IPConnection->ENUMERATION_TYPE_DISCONNECTED)
	{
		print "\n";
		return;
	}

	print "Connected UID:     $connected_uid\n";
	print "Position:          $position\n";
	print "Hardware Version:  ".join('.', @$hardware_version)."\n";
	print "Firmware Version:  ".join('.', @$firmware_version)."\n";
	print "Device Identifier: $device_identifier\n";
	print "\n";
}

# Create connection and connect to brickd
my $ipcon = Tinkerforge::IPConnection->new();

$ipcon->connect(&HOST, &PORT);

# Register Enumerate Callback
$ipcon->register_callback($ipcon->CALLBACK_ENUMERATE, 'cb_enumerate');

# Trigger Enumerate
$ipcon->enumerate();

print "Press any key to exit...\n";
<STDIN>;
$ipcon->disconnect();
