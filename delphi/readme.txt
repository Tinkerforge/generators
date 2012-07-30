This zip contains the Delphi bindings for all Tinkerforge Bricks and Bricklets
(in bindings/) and all available Delphi examples (in examples/).

To keep the Delphi bindings stupid and simple, they only have dependencies that
are available nearly everywhere, thus making it possible to compile into any
project hassle-free. We do not offer a pre-compiled library, since it would be
a pain in the ass to provide them for all combinations of architectures and
operating systems. This means, the bindings should work on most architectures
(ARM, x86, etc.) and on most operating systems (Windows and POSIX systems such
as Linux and Mac OS, etc.).

As an example we will compile the Stepper Brick configuration example with
the Free Pascal Compiler (FPC) that comes with the Lazarus. For that we
have to copy the IP Connection (Base58.pas, BlockingQueue.pas, Device.pas,
IPConnection.pas, LEConverter.pas and TimedSemaphore.pas) and the Stepper
Brick bindings (BrickStepper.pas) from the bindings/ folder as well as the
ExampleConfiguration.pas from the examples/Brick/Stepper/ folder into our
project:

project_folder/
 -> Base58.pas
 -> BlockingQueue.pas
 -> Device.pas
 -> IPConnection.pas
 -> LEConverter.pas
 -> TimedSemaphore.pas
 -> BrickStepper.pas
 -> ExampleConfiguration.pas

FPC automatically finds the used units, therefore a compilation of the project
with FPC like:

fpc ExampleConfiguration.pas

With Lazarus we can use our project_folder/ as follows:

Project -> New Project from file ... ->
 choose project_folder/ExampleConfiguration.pas -> Open ->
 choose Console Application -> OK -> choose Application class name and Title ->
 OK

Now we are ready to go!

With Delphi XE2 (older Delphi version should work similar) we can use our
project_folder/ as follows. First rename ExampleConfiguration.pas to
ExampleConfiguration.dpr then click:

Project -> Add Existing Project... ->
 choose project_folder/ExampleConfiguration.dpr -> Open

Now we are ready to go again!

Documentation for the API can be found at http://www.tinkerforge.com/doc/index.html
