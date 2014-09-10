Generators
==========

This repository contains documentation/bindings generators and the configs
for all Bricks and Bricklets, which describe the different language bindings.

Repository Content
------------------

 * Contains language specific IP Connection
 * and language specific documentation/bindings generators

configs/:
 * Contains the configs for all Bricks and Bricklets

generate_all.py:
 * Generates all bindings and documentations

copy_all.py:
 * Copies all bindings and documentations to the corresponding places

Requirements
------------

The generators are written in Python and meant to be executed on Linux. They
work with Python 2.7. Python 3 will probably not work.

The generators for specific bindings can have extra requirements, typically
the compilers for compiled languages (the following list is incomplete):
 * C#: Mono 3.2 or higher (gmcs + runtime)

Usage
-----

If you only want to generate the bindings it is sufficient to clone this
repository. For example, to generate the C# bindings execute the following
commands:

    cd csharp
    python generate_csharp_bindings.py
    python generate_csharp_zip.py

If you want to generate the documentation as well, you have to clone **all**
Brick gits and **all** Bricklet gits in parallel to the generators git.
Otherwise the ``generate_all.py`` and ``copy_all.py`` scripts can't find the
examples that are used in the documentation.
