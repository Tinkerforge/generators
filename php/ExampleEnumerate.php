<?php

require_once('Tinkerforge/IPConnection.php');

use Tinkerforge\IPConnection;

const HOST = 'localhost';
const PORT = 4223;

function cb_enumerate($uid, $connectedUid, $position,
                      $hardwareVersion, $firmwareVersion,
                      $deviceIdentifier, $enumerationType)
{
	echo "UID:               $uid\n";
	echo "Enumeration Type:  $enumerationType\n";

	if($enumerationType == IPConnection::ENUMERATION_TYPE_DISCONNECTED) {
		echo "\n";
		return;
	}

	echo "Connected UID:     $connectedUid\n";
	echo "Position:          $position\n";
	echo "Hardware Version:  $hardwareVersion[0].$hardwareVersion[1].$hardwareVersion[2]\n";
	echo "Firmware Version:  $firmwareVersion[0].$firmwareVersion[1].$firmwareVersion[2]\n";
	echo "Device Identifier: $deviceIdentifier\n";
	echo "\n";
}

// Create IP connection and connect to brickd
$ipcon = new IPConnection();
$ipcon->connect(HOST, PORT);

// Register enumeration callback to "cb_enumerate"
$ipcon->registerCallback(IPConnection::CALLBACK_ENUMERATE, 'cb_enumerate');

$ipcon->enumerate();

echo "Press ctrl+c to exit\n";
$ipcon->dispatchCallbacks(-1); // Dispatch callbacks forever

?>
