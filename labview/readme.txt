Tinkerforge LabVIEW Bindings
============================

The LabVIEW bindings consist of a .NET library (.dll) for all Tinkerforge
Bricks and Bricklets (Tinkerforge.dll), the C# source of the library
(in source/) and all available LabVIEW examples (in examples/). The examples
are stored in LabVIEW 2013 format. All examples are provided in LabVIEW 2010
format as well.

The .NET support in LabVIEW is only available on Windows.

To make the bindings work LabVIEW has to be able to find the Tinkerforge.dll.
If you open an example then LabVIEW will search fo it and ask you if it could
not find it. You can avoid this search and ask procedure by putting the
Tinkerforge.dll in a folder known to LabVIEW. The easiest options are the
vi.lib folder of your LabVIEW installation or you can put it in the same
folder as the example you want to test. In both cases LabVIEW will find the
Tinkerforge.dll automatically and does not ask for your support. But LabVIEW
might warn that Tinkerforge.dll was loaded from a different folder. This
warning can be ignored.

As an example we will run the Stepper Brick configuration example. To do this
open examples/Brick/Stepper/Example Configuration.vi in LabVIEW, change the
UID to the one of your Stepper Brick and run it.

API Documentation and Examples
------------------------------

Links to the API documentation for the IP Connection, Bricks and Bricklets as
well as the examples from this ZIP file can be found at

 http://www.tinkerforge.com/en/doc/Software/API_Bindings_LabVIEW.html#api-documentation-and-examples
