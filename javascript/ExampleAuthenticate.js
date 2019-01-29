var Tinkerforge = require('tinkerforge');

var HOST = 'localhost';
var PORT = 4223;
var SECRET = 'My Authentication Secret!';

ipcon = new Tinkerforge.IPConnection(); // Create IP connection
ipcon.connect(HOST, PORT,
    function(error) {
        console.log('Error: '+error);
    }
); // Connect to brickd

// Disable auto reconnect mechanism, in case we have the wrong secret.
// If the authentication is successful, reenable it.
ipcon.setAutoReconnect(false);

// Register Connected Callback
ipcon.on(Tinkerforge.IPConnection.CALLBACK_CONNECTED,
    // Authenticate each time the connection got (re-)established
    function(connectReason) {
        switch(connectReason) {
        case Tinkerforge.IPConnection.CONNECT_REASON_REQUEST:
            console.log('Connected by request');
            break;
        case Tinkerforge.IPConnection.CONNECT_REASON_AUTO_RECONNECT:
            console.log('Auto-Reconnected');
            break;
        }
        ipcon.authenticate(SECRET,
            function() {
                console.log('Authentication succeeded');

                // ...reenable auto reconnect mechanism, as described above...
                ipcon.setAutoReconnect(true);

                // ...then trigger Enumerate
                ipcon.enumerate();
            },
            function(error) {
                console.log('Could not authenticate: '+error);
            }
        );
    }
);

// Register Enumerate Callback
ipcon.on(Tinkerforge.IPConnection.CALLBACK_ENUMERATE,
    // Print incoming enumeration
    function(uid, connectedUid, position, hardwareVersion, firmwareVersion,
             deviceIdentifier, enumerationType) {
        console.log('UID: '+uid+', Enumeration Type: '+enumerationType);
    }
);

console.log("Press any key to exit ...");
process.stdin.on('data',
    function(data) {
        ipcon.disconnect();
        process.exit(0);
    }
);
