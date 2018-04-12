<<<DEVICE_NAME_READABLE_README>>>

 *This Bricklet is currently in development*

This repository contains the firmware source code and the hardware design
files. The documentation generator configs can be found at
https://github.com/Tinkerforge/generators

Repository Content
------------------

software/:
 * examples/: Examples for all supported languages
 * build/: Makefile and compiled files
 * src/: Source code of firmware
 * generate_makefile: Shell script to generate Makefile from cmake script

hardware/:
 * Contains kicad project files and additionally schematics as pdf

datasheets/:
 * Contains datasheets for sensors and complex ICs that are used

Hardware
--------

The hardware is designed with the open source EDA Suite KiCad
(http://www.kicad-pcb.org). Before you are able to open the files,
you have to install the Tinkerforge kicad-libraries
(https://github.com/Tinkerforge/kicad-libraries). You can either clone
them directly in hardware/ or clone them in a separate folder and
symlink them into hardware/
(ln -s kicad_path/kicad-libraries project_path/hardware). After that you
can open the .pro file in hardware/ with kicad and from there view and
modify the schematics and the PCB layout.

Software
--------

 If you want to do your own Brick/Bricklet firmware development we highly
 recommend that you use our build environment setup script and read the
 tutorial: https://www.tinkerforge.com/en/doc/Tutorials/Tutorial_Build_Environment/Tutorial.html

To compile the C code we recommend you to install the newest GNU Arm Embedded 
Toolchain (https://launchpad.net/gcc-arm-embedded/+download).
You also need to install bricklib2 (https://github.com/Tinkerforge/bricklib2).

You can either clone it directly in software/src/ or clone it in a
separate folder and symlink it into software/src/
(ln -s bricklib_path/bricklib2 project_path/software/src/). Finally make sure to
have CMake installed (http://www.cmake.org/cmake/resources/software.html).

After that you can generate a Makefile from the cmake script with the
generate_makefile shell script (in software/) and build the firmware
by invoking make in software/build/. The firmware (.zbin) can then be found
in software/build/ and uploaded with brickv (click button "Flashing"
on start screen).
