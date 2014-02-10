The Mathematica bindings consist of a .NET library (.dll) for all Tinkerforge
Bricks and Bricklets (Tinkerforge.dll), the C# source of the library
(in source/) and all available Mathematica examples (in examples/).

The .NET/Link support in Mathematica requires the .NET Framework on Windows and
the Mono Framework on Linux and Mac OS X.

As an example we will run the Stepper Brick configuration example. To do this
open the examples/Brick/Stepper/ExampleConfiguration.nb Notebook in
Mathematica, change the UID to the one of your Stepper Brick and evaluate all
cells in top-down order.

If you moved the Notebook file to a different folder you might need to change
the LoadNETAssembly[] line to make Mathematica find the Tinkerforge.dll:

 LoadNETAssembly["Tinkerforge",NotebookDirectory[]<>"../.."]

Replace the NotebookDirectory[]<>"../.." parameter with an absolute path
to the folder that contains the Tinkerforge.dll.

Documentation for the API can be found at

 http://www.tinkerforge.com/en/doc/Software/API_Bindings_VBNET.html#api-documentation-and-examples
