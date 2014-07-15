Tinkerforge Python Bindings
===========================

This ZIP contains the Python source of the bindings for all Tinkerforge Bricks
and Bricklets (in source/) and all available Python examples (in examples/).

You can install the bindings using setuptools by executing the following command
in the source/ folder:

 python setup.py install

The bindings are also available on the PyPI (https://pypi.python.org). You can
install them with the Python Package Installer pip (https://pip.pypa.io):

 pip install tinkerforge

After that you can use the examples as they are.

If you can't or don't want to install the bindings then you can also use the
source directly, just create a folder for your project and copy the tinkerforge/
folder from source/ and the example you want to try in there (e.g. the Stepper
Brick configuration example from examples/brick/stepper/example_configuration.py).

 example_folder/
 -> tinkerforge/
 -> example_configuration.py

If you just want to use a few Bricks or Bricklets and you don't want to have
this many files in you project, you can also copy the files as they are needed.
For the Stepper Brick examples we need ip_connection.py and brick_stepper.py.
After copying these in the project folder

 example_folder/
 -> ip_connection.py
 -> brick_stepper.py
 -> example_configuration.py

we have to remove the tinkerforge package from the examples, i.e. instead of
"from tinkerforge.ip_connection" and "from tinkerforge.brick_stepper" we use
"from ip_connection" and "from brick_stepper". After that, the example can be
executed again.

API Documentation and Examples
------------------------------

Links to the API documentation for the IP Connection, Bricks and Bricklets as
well as the examples from this ZIP file can be found at

 http://www.tinkerforge.com/en/doc/Software/API_Bindings_Python.html#api-documentation-and-examples
