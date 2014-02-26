This ZIP contains a Node.js NPM package (tinkerforge.tgz) and the browser
version (in browser/) of the bindings for all Tinkerforge Bricks and Bricklets.
The source and examples of the Node.js implementation (in nodejs/source) and
(in nodejs/examples), the examples of the browser API (in browser/exmaples)
for all Tinkerforge Bricks and Bricklets are included as well. The source of the
browser implementation can be found in (browser/source/).

You can install the NPM Package locally with ("sudo npm -g install tinkerforge.tgz")
or from NPM registry with ("sudo npm -g install tinkerforge"). After that you
can use the examples as they are.

If you can't or don't want to use the NPM package, you can also use the source
directly, just create a folder for your project and copy the Tinkerforge folder
from source/ and the example you want to try in there (e.g. the Stepper Brick
configuration example from examples/brick/stepper/ExampleConfiguration.js).

 example_folder/
 -> Tinkerforge/
 -> ExampleConfiguration.js

The required statements must be modified in this case as follows,

instead of,

"var Tinkerforge = require('Tinkerforge');"
"var ipcon = new Tinkerforge.IPConnection();"
"var stepper = new Tinkerforge.BrickStepper();"

use,

"var IPConnection = require('./Tinkerforge/IPConnection');"
"var BrickStepper = require('./Tinkerforge/BrickStepper');"
"var ipcon = new IPConnection();"
"var stepper = new BrickStepper();"

For using the HTML examples, just put the browser implementation source
file from (browser/source/Tinkerforge.js) and the HTML file of the example
that you want to try in the same directory and simply open the HTML file with
a browser.

Documentation for the API can be found at

 http://www.tinkerforge.com/en/doc/Software/API_Bindings_JavaScript.html#api-documentation-and-examples
