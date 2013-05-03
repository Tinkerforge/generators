This zip contains a Ruby GEM with the bindings for all Tinkerforge Bricks and
Bricklets (tinkerforge.gem), the source of the GEM (in source/) and all available
Ruby examples (in examples/).

You can install the GEM with the gem tool ("gem install tinkerforge.egg").
After that you can use the examples as they are.

If you can't or don't want to use the GEM, you can also use the source directly,
just create a folder for your project and copy the tinkerforge folder from
source/ and the example you want to try in there (e.g. the Stepper Brick
configuration example from examples/brick/stepper/example_configuration.rb).

example_folder/
 -> tinkerforge/
 -> example_configuration.rb

You need to tell Ruby to look in the current folder for required modules:

ruby -I. example_configuration.rb

If you just want to use a few Bricks or Bricklets and you don't want to have
this many files in you project, you can also copy the files as they are needed.
For the Stepper Brick examples we need ip_connection.rb and brick_stepper.rb.
After copying these in the project folder

example_folder/
 -> ip_connection.rb
 -> brick_stepper.rb
 -> example_configuration.rb

we have to remove the tinkerforge package from the examples, i.e. instead of
"require 'tinkerforge/ip_connection'" and "require 'tinkerforge/brick_stepper'"
we use "require 'ip_connection'" and "require 'brick_stepper'". After that,
the example can be executed again.

Documentation for the API can be found at http://www.tinkerforge.com/en/doc/index.html
