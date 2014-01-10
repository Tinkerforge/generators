This zip contains the Perl support for all Tinkerforge Bricks and
Bricklets, the source is in ("source/Tinkerforge") and all the Perl examples in "examples/".

You can install the egg with CPAN ("sudo cpan install Tinkerforge").
After that you can use the examples as they are.

If you can't or don't want to use CPAN, you can also use the source
directly, just create a folder for your project and copy the ("Tinkerforge/")
folder from ("source/") and the example you want to try in there
(e.g. the Stepper configuration example from, "examples/brick/stepper/example_configuration.pl")

 example_folder/
  -> Tinkerforge/
  -> example_configuration.pl

we have to add a line on top of the file ("example_configuration.pl"):

 use lib './';

If you just want to use a few Bricks or Bricklets and you don't want to
have this many files in you project, you can also copy the files as they are
needed. For the Stepper Brick examples we need ("IPConnection.pm") and
("BrickStepper.pm"). After copying these in the project folder:

 example_folder/
  -> IPConnection.pm
  -> BrickStepper.pm
  -> example_configuration.pl

we have to remove the ("Tinkerforge::") package from the examples, i.e. instead of:

 use Tinkerforge::IPConnection;
 use Tinkerforge::Device;
 use Tinkerforge::BrickStepper;

we use:

 use lib './';
 use IPConnection;
 use Device;
 use DBrickStepper;

After that, the example can be executed again.

Documentation for the API can be found at

 http://www.tinkerforge.com/en/doc/Software/API_Bindings_Python.html#api-documentation-and-examples
