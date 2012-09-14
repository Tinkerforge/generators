This zip contains the C/C++ bindings for all Tinkerforge Bricks and Bricklets
(in bindings/) and all available C/C++ examples (in examples/).

To keep the C/C++ bindings stupid and simple, they only have dependencies that
are available nearly everywhere, thus making it possible to compile into any
project hassle-free. We do not offer a pre-compiled library, since it would be
a pain in the ass to provide them for all combinations of architectures and
operating systems. This means, the bindings should work on most architectures
(ARM, x86, etc.) and on most operating systems (Windows and POSIX systems such
as Linux and Mac OS, etc.).

As an example we will compile the Stepper Brick configuration example with gcc
on Windows and Linux. For that we have to copy the IP Connection and the Stepper
Brick bindings (ip_connection.h, ip_connection.c, brick_stepper.c and
brick_stepper.h) from the bindings/ folder as well as the example_configuration.c
from the examples/brick/stepper/ folder into our project:

project_folder/
 -> ip_connection.c
 -> ip_connection.h
 -> brick_stepper.c
 -> brick_stepper.h
 -> example_configuration.c

The only dependency on Unix-like systems is pthreads, therefore a compilation of
the project with GCC on Linux looks like:

gcc -pthread -o example_configuration brick_stepper.c ip_connection.c example_configuration.c

On Windows Win32 is used for threading and WinSock2 for the network connection.
Under MinGW we can compile the example as following (the library linking must
come after the source)::

gcc -o example_configuration.exe brick_stepper.c ip_connection.c example_configuration.c -lws2_32

With Visual Studio we can use our project_folder/ as follows:

* File
* New
* Project From Existing Code
* Choose Type "Visual C++"
* Choose project_folder/
* Choose a project name
* Click Next
* Choose "Console Application"
* Click Finish

Now we have to tell Visual Studio to use the C++ compiler, since we would need
C99 but Visual Studio can only compile C89. This problem can be avoided by using
the C++ compiler instead:

* Project
* Properties
* C/C++
* Advanced, option "Compile as"
* Choose "Compile as C++ Code (/TP)"

Also we have to include ws2_32.lib (WinSock2) by clicking on:

* Project
* Properties
* Linker
* Input, option "Additional Dependencies"
* Add "ws2_32.lib;"

Thats it, we are ready to go!

The Visual Studio compiler can also be used from the command line:

 cl.exe /TP /I. brick_stepper.c ip_connection.c example_configuration.c /link /out:example_configuration.exe ws2_32.lib

Documentation for the API can be found at http://www.tinkerforge.com/doc/index.html
