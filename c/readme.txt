This zip contains the C/C++ bindings for all Tinkerforge Bricks and
Bricklets (in bindings/) and all available C/C++ examples (in
examples/).

To keep the C/C++ bindings stupid and simple, they only have
dependencies that are available nearly everywhere, thus making it
possible to compile into any project hassle-free. This means, the
bindings should work on most platforms (arm, x86, etc.) and on most
operating systems (Windows and posix systems such as linux and Mac
OS, etc.).

As an example we will compile the Stepper Brick configuration example with gcc
on Windows and linux.
For that we have to copy the IP Connection and the Stepper Brick
bindings (ip_connection.h, ip_connection.c, stepper_brick.c and 
stepper_brick.h) from the bindings/ folder as well as the
example_configuration.c from the examples/brick/stepper/ folder into our
project:

project_folder/
 -> ip_connection.c
 -> ip_connection.h
 -> brick_stepper.c
 -> brick_stepper.h
 -> example_configuration.c
 
The only dependency on Unix-like systems is pthread, therefore a
compilation of the project with gcc on linux looks like:

gcc -lpthread -o example_configuration brick_stepper.c ip_connection.c example_configuration.c

On Windows WinThreads???? (TODO) are used for threading, we can compile
the example as following:

gcc.exe ?????? -o example_configuration.exe brick_stepper.c ip_connection.c example_configuration.c
