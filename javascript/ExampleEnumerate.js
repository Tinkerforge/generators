var Tinkerforge = require('tinkerforge');

var HOST = 'localhost';
var PORT = 4223;

// Create connection and connect to brickd
ipcon = new Tinkerforge.IPConnection();
ipcon.connect(HOST, PORT);

ipcon.on(Tinkerforge.IPConnection.CALLBACK_CONNECTED,
    function(connectReason) {
        // Trigger Enumerate
        ipcon.enumerate();
    }
);

// Register Enumerate Callback
ipcon.on(Tinkerforge.IPConnection.CALLBACK_ENUMERATE,
    // Print incoming enumeration
    function(uid, connectedUid, position, hardwareVersion, firmwareVersion,
             deviceIdentifier, enumerationType) {
        console.log('UID:               '+uid);
        console.log('Enumeration Type:  '+enumerationType);
        if(enumerationType === Tinkerforge.IPConnection.ENUMERATION_TYPE_DISCONNECTED) {
            console.log('');
            return;
        }
        console.log('Connected UID:     '+connectedUid);
        console.log('Position:          '+position);
        console.log('Hardware Version:  '+hardwareVersion);
        console.log('Firmware Version:  '+firmwareVersion);
        console.log('Device Identifier: '+deviceIdentifier);
        console.log('');
    }
);

console.log("Press any key to exit ...");
process.stdin.on('data',
    function(data) {
        ipcon.disconnect();
        process.exit(0);
    }
);
