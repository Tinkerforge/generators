<hr />

# Tinkerforge

Tinkerforge is a Node.JS package that provides the
Tinkerforge API bindings for all Tinkerforge Bricks
and Bricklets.

## How to Install

```
npm install tinkerforge
```

## How to Use

To be able to use the bindings first the API must be
included in the code in following way:

```js
var Tinkerforge = require('Tinkerforge');
```

After that all the classes and their functionalities
provided by the binding can be accessed like:

```js
var IPConnection = Tinkerforge.IPConnection;
var BrickletDualButton = Tinkerforge.BrickletDualButton;
```

Then to create an instance of a class:

```js
IPConnection = new IPConnection();
BrickletDualButton = new BrickletDualButton();
```

Detailed documentation is available [here](http://www.tinkerforge.com)

## Examples

### Enumeration
```js
var Tinkerforge = require('Tinkerforge');
var IPConnection = Tinkerforge.IPConnection;

var HOST = 'localhost';
var PORT = 4223;

// Create connection and connect to brickd
ipcon = new IPConnection();
ipcon.connect(HOST, PORT);

// Register Enumerate Callback
ipcon.on(IPConnection.CALLBACK_ENUMERATE,
    // Print incoming enumeration
    function(uid, cuid, pos, hwv, fwv, devid, enumtype) {
        console.log('UID:               '+uid);
        console.log('Enumeration Type:  '+enumtype);
        if(enumtype === IPConnection.ENUMERATION_TYPE_DISCONNECTED) {
            return;
        }
        console.log('Connected UID:     '+cuid);
        console.log('Position:          '+pos);
        console.log('Hardware Version:  '+hwv);
        console.log('Firmware Version:  '+fwv);
        console.log('Device Identifier: '+devid);
        console.log('');
    }
);

// Trigger Enumerate
ipcon.enumerate();

console.log("Press any key to exit ...");
process.stdin.on('data',
    function(data) {
        ipcon.disconnect();
        process.exit(0);
    }
);
```
### Getter Call
```js
var IPConnection = require('Tinkerforge/IPConnection');
var BrickletHumidity = require('Tinkerforge/BrickletHumidity');

var HOST = 'localhost';
var PORT = 4223;
var UID = '7bA';// Change to your UID

var ipcon = new IPConnection();// Create IP connection
var h = new BrickletHumidity(UID, ipcon);// Create device object

ipcon.connect(HOST, PORT,
    function(error) {
        console.log('Error: '+error);        
    }
);// Connect to brickd

// Don't use device before ipcon is connected
ipcon.on(IPConnection.CALLBACK_CONNECTED,
    function(connectReason) {
        // Get current humidity (unit is %RH/10)
        h.getHumidity(
            function(rh) {
                console.log('Relative Humidity: '+rh/10+' %RH');
            },
            function(error) {
                console.log('Error: '+error);
            }
        );
    }
);

console.log("Press any key to exit ...");
process.stdin.on('data',
    function(data) {
        ipcon.disconnect();
        process.exit(0);
    }
);

```
### Setter and Callbacks
```js
var IPConnection = require('Tinkerforge/IPConnection');
var BrickletHumidity = require('Tinkerforge/BrickletHumidity');

var HOST = 'localhost';
var PORT = 4223;
var UID = '7bA';//Change to your UID

var ipcon = new IPConnection();//Create IP connection
var h = new BrickletHumidity(UID, ipcon);//Create device object

ipcon.connect(HOST, PORT,
    function(error) {
        console.log('Error: '+error);        
    }
);// Connect to brickd

//Don't use device before ipcon is connected
ipcon.on(IPConnection.CALLBACK_CONNECTED,
    function(connectReason) {
        // Set threshold callbacks with a debounce time of 10 seconds (10000ms)
        h.setDebouncePeriod(10000); 
        // Configure threshold for "outside of 30 to 60 %RH" (unit is %RH/10)
        h.setHumidityCallbackThreshold('o', 30*10, 60*10);    
    }
);

// Register threshold reached callback
h.on(BrickletHumidity.CALLBACK_HUMIDITY_REACHED,
    // Callback for humidity outside of 30 to 60 %RH
    function(humidity) {
        if(humidity < 30*10) {
            console.log('Humidity too low: '+humidity/10+' %RH');
        }
        if(humidity > 60*10) {
            console.log('Humidity too high: '+humidity/10+' %RH');
        }
    }
);

console.log("Press any key to exit ...");
process.stdin.on('data',
    function(data) {
        ipcon.disconnect();
        process.exit(0);
    }
);

```
## License

CC0

