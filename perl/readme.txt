This ZIP contains the Perl support for all Tinkerforge Bricks and Bricklets
(Tinkerforge.tar.gz), the source of the CPAN package (source/) and all available
Perl examples (examples/).

A CPAN package will be available soon. Then it will be possible to install
the Perl bindings support from CPAN.

Yon can also install the local version of the CPAN package by unpacking
Tinkerforge.tar.gz and running the following commands:

 perl Makefile.PL
 make
 make test
 make install

You can also use the source directly, just create a folder for your project and
copy the Tinkerforge/ folder from source/ and the example you want to try in
there (e.g. the Stepper configuration example from,
examples/brick/stepper/example_configuration.pl)

 example_folder/
  -> Tinkerforge/
  -> example_configuration.pl

You have to add a line on top of the file example_configuration.pl:

 use lib './';

If you just want to use a few Bricks or Bricklets and you don't want to have
this many files in you project, you can also copy the files as they are needed.
For the Stepper Brick examples we need IPConnection.pm and BrickStepper.pm.
After copying these in the project folder:

 example_folder/
  -> IPConnection.pm
  -> BrickStepper.pm
  -> example_configuration.pl

we have to remove the "Tinkerforge::" package from the examples, i.e. instead of:

 use Tinkerforge::IPConnection;
 use Tinkerforge::Device;
 use Tinkerforge::BrickStepper;

we use:

 use lib './';
 use IPConnection;
 use Device;
 use BrickStepper;

After that, the example can be executed again.

Documentation for the API can be found at

 http://www.tinkerforge.com/en/doc/Software/API_Bindings_Perl.html#api-documentation-and-examples
