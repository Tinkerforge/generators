This zip contains a Node.JS NPM package (tinkerforge-<TF_API_VERSION>-5.tgz)
and the browser version of the Tinkerforge API (in browser/). The source
and examples of the Node.JS implementation (in nodejs/source/Tinkerforge) and
(in nodejs/examples), the examples of the browser API (in /browser/exmaples)
for all Tinkerforge Bricks and Bricklets.

You can install the NPM Package locally with
("sudo npm -g install tinkerforge-<TF_API_VERSION>-5.tgz") or from NPM registry with
("sudo npm -g install tinkerforge") After that you can use the examples as they are.

If you can't or don't want to use the NPM package, you can also use the source
directly, just create a folder for your project and copy the Tinkerforge folder
from source/ and the example you want to try in there (e.g. the Stepper Brick
configuration example from examples/brick/stepper/exampleConfiguration.js).

 example_folder/
 -> Tinkerforge/
 -> exampleConfiguration.js

The require statements must be modified in this case as follows,

instead of,

"var Tinkerforge = require('Tinkerforge');"
"var ipcon = new Tinkerforge.IPConnection();"
"var stepper = new Tinkerforge.BrickStepper();"

use,

"var IPConnection = require('./Tinkerforge/IPConnection')"
"var ipcon = new IPConnection();"
"var stepper = new BrickStepper();"

For using the API in browser/from html files,

<head>
    <script src="/path/to/Tinkerforge.js" type="text/javascript">
</head>

Documentation for the API can be found at

 http://www.tinkerforge.com/en/doc/Software/API_Bindings_Javascript.html#api-documentation-and-examples
