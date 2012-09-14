This zip contains a PEAR package with the bindings for all Tinkerforge Bricks
and Bricklets (Tinkerforge.tgz), the source of the PEAR package (in source/)
and all available PHP examples (in examples/).

You can install the PEAR package with the pear tool ("pear install Tinkerforge.tgz").
After that you can use the examples as they are.

If you can't or don't want to use the PEAR package, you can also use the source
directly, just create a folder for your project and copy the Tinkerforge folder
from source/ and the example you want to try in there (e.g. the Stepper Brick
configuration example from examples/brick/stepper/ExampleConfiguration.php).

example_folder/
 -> Tinkerforge/
 -> ExampleConfiguration.php

If you just want to use a few Bricks or Bricklets and you don't want to have
this many files in you project, you can also copy the files as they are needed.
For the Stepper Brick examples we need IPConnection.php and BrickStepper.php.
After copying these in the project folder

example_folder/
 -> IPConnection.php
 -> BrickStepper.php
 -> ExampleConfiguration.php

we have to remove the Tinkerforge folder from require_once statements in the
examples, i.e. instead of "require_once('Tinkerforge/IPConnection.php');" we
use "require_once('IPConnection.php');". After that, the example can be executed
again.

Documentation for the API can be found at http://www.tinkerforge.com/doc/index.html
