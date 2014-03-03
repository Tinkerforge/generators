#!/usr/bin/perl

use Tinkerforge::IPConnection;

use constant HOST => 'localhost';
use constant PORT => 4223;

# Print incoming enumeration
sub cb_enumerate()
{
	my ($uid, $connected_uid, $position, $hardware_version,
	    $firmware_version, $device_identifier, $enumeration_type) = @_;

	print "\nUID:               ".$uid;
	print "\nEnumeration Type:  ".$enumeration_type;

	if ($enumeration_type == Tinkerforge::IPConnection->ENUMERATION_TYPE_DISCONNECTED)
	{
		print "\n";
		return 1;
	}

	print "\nConnected UID:     ".$connected_uid;
	print "\nPosition:          ".$position;
	print "\nHardware Version:  ".join('.', @$hardware_version);
	print "\nFirmware Version:  ".join('.', @$firmware_version);
	print "\nDevice Identifier: ".$device_identifier;
	print "\n";
}

# Create connection and connect to brickd
my $ipcon = Tinkerforge::IPConnection->new();

$ipcon->connect(&HOST, &PORT);

# Register Enumerate Callback
$ipcon->register_callback($ipcon->CALLBACK_ENUMERATE, 'cb_enumerate');

# Trigger Enumerate
$ipcon->enumerate();

print "\nPress any key to exit...\n";
<STDIN>;
$ipcon->disconnect();
