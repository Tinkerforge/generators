Tinkerforge C# Bindings
=======================

This ZIP contains a C# library (.dll) for all Tinkerforge Bricks and Bricklets
(Tinkerforge.dll), the source of the library (in source/) and all available C#
examples (in examples/).

The library can be used without any further extensions. As an example lets
compile the configuration example of the Stepper Brick.

For this we create a folder and copy the Tinkerforge.dll and the
examples/Brick/Stepper/ExampleConfiguration.cs into this folder.

 example_folder/
 -> Tinkerforge.dll
 -> ExampleConfiguration.cs

In this folder we can now call the C# compiler with the following parameters
(1. Windows and 2. Linux/Mac OS X (Mono))

 1.) csc  /target:exe /reference:Tinkerforge.dll ExampleConfiguration.cs
 2.) gmcs /target:exe /reference:Tinkerforge.dll ExampleConfiguration.cs

Or, alternatively add the DLL and the Example in an C# development environment
of your choice (such as Visual Studio or Mono Develop).

API Documentation and Examples
------------------------------

Links to the API documentation for the IP Connection, Bricks and Bricklets as
well as the examples from this ZIP file can be found at

 http://www.tinkerforge.com/en/doc/Software/API_Bindings_CSharp.html#api-documentation-and-examples
