This zip contains a Python egg with the bindings for all Tinkerforge Bricks and Bricklets (tinkerforge.egg), the source of the egg (in source/) and all available Python examples (in examples/).

You can install the egg with easy_install ("easy_install tinkerforge.egg").
After that you can use the examples as they are.

If you can't or don't want to use the egg, you can also use the source directly, just create a folder for your project and copy the tinkerforge folder from source/ and the example you want to try in there (e.g. the stepper configuration example from examples/brick/stepper/example_configuration.py).

example_folder/
 -> tinkerforge/
 -> example_configuration.py

If you just want to use a few Bricks or Bricklets and you don't want to have this many files in you project, you can also copy the files as they are needed, for the stepper examples we need ip_connection.py and stepper_brick.py. After copying these in the project folder  

example_folder/
 -> ip_connection.py
 -> brick_stepper.py
 -> example_configuration.py

we have to remove the tinkerforge package from the examples, i.e. instead of "from tinkerforge.ip_connection" and "from tinkerforge.brick_stepper" we use "from ip_connection" and "from brick_stepper". After that, the example can be executed again.
