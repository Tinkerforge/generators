This ZIP contains the Node.js NPM package (tinkerforge.tgz) and the WebSocket
based browser version (in browser/) of the JavaScript bindings for all Tinkerforge
Bricks and Bricklets. The ZIP file also contains the source of the Node.js
implementation (in nodejs/source/) and the Node.js examples (in nodejs/examples/),
as well as the source of the browser implementation (in browser/source/) and
the HTML examples (in browser/exmaples/).

You can install the NPM Package locally with ("sudo npm -g install tinkerforge.tgz")
or from NPM registry with ("sudo npm -g install tinkerforge"). After that you
can use the examples as they are.

If you can't or don't want to use the NPM package, you can also use the source
directly. Just create a folder for your project and copy the Tinkerforge folder
from nodejs/source/ and the example you want to try in there (e.g. the Stepper Brick
configuration example from nodejs/examples/Brick/Stepper/ExampleConfiguration.js).

 example_folder/
 -> Tinkerforge/
 -> ExampleConfiguration.js

The require statement must be modified in this case as follows. Instead of:

 var Tinkerforge = require('tinkerforge');

 var ipcon = new Tinkerforge.IPConnection();
 var stepper = new Tinkerforge.BrickStepper(UID, ipcon);

use:

 var IPConnection = require('./Tinkerforge/IPConnection');
 var BrickStepper = require('./Tinkerforge/BrickStepper');

 var ipcon = new IPConnection();
 var stepper = new BrickStepper(UID, ipcon);

The Browser version of the JavaScript bindings is using WebSockets. They are
supported by Brick Daemon (since version 2.1.0) and the Ethernet Extension
(since Master Brick firmware version 2.2.0), but they are disabled by default
and need to be configured first:

 http://www.tinkerforge.com/en/doc/Software/Brickd.html#websocket-configuration
 http://www.tinkerforge.com/en/doc/Hardware/Master_Extensions/Ethernet_Extension.html#websockets

If WebSockets are enabled you can test the HTML examples. Just put the browser
JavaScript source file from browser/source/Tinkerforge.js and the HTML file
of the example that you want to try in the same directory and open the HTML
file with a browser.

Documentation for the API can be found at

 http://www.tinkerforge.com/en/doc/Software/API_Bindings_JavaScript.html#api-documentation-and-examples
