<?php

require_once('Tinkerforge/IPConnection.php');

use Tinkerforge\IPConnection;
use Tinkerforge\TinkerforgeException;

const HOST = 'localhost';
const PORT = 4223;
const SECRET = 'My Authentication Secret!';

// Authenticate each time the connection got (re-)established
function cb_connected($connectReason, $userData)
{
	$ipcon = $userData;

	switch ($connectReason) {
	case IPConnection::CONNECT_REASON_REQUEST:
		echo "Connected by request\n";
		break;
	}

	// Authenticate first...
	try {
		$ipcon->authenticate(SECRET);
		echo "Authentication succeeded\n";
	} catch (TinkerforgeException $e) {
		echo "Could not authenticate: $e\n";
		return;
	}

	// ...then trigger enumerate
	$ipcon->enumerate();
}

// Print incoming enumeration
function cb_enumerate($uid, $connectedUid, $position,
                      $hardwareVersion, $firmwareVersion,
                      $deviceIdentifier, $enumerationType)
{
	echo "UID: $uid, Enumeration Type: $enumerationType\n";
}

// Create IP connection and connect to brickd
$ipcon = new IPConnection();

// Register connected callback to "cb_connected"
$ipcon->registerCallback(IPConnection::CALLBACK_CONNECTED, 'cb_connected', $ipcon);

// Register enumerate callback to "cb_enumerate"
$ipcon->registerCallback(IPConnection::CALLBACK_ENUMERATE, 'cb_enumerate');

$ipcon->connect(HOST, PORT);

echo "Press ctrl+c to exit\n";
$ipcon->dispatchCallbacks(-1); // Dispatch callbacks forever

?>
