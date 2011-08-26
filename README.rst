Generators
==========

This repository contains documentation/bindings generators and the configs 
for all Bricks and Bricklets, which describe the different language bindings.

Repository Content
------------------

language/ (c, python, etc):
 * Contains language specific ip_connection
 * and language specific documentation/bindings generators

configs/:
 * Contains the configs for all Bricks and Bricklets

generate_all.py:
 * Generates all bindings and documentations

copy_all.py:
 * Copies all bindings and documentations to the corresponding places

Usage
-----

To use the generators you have to clone _all_ Brick gits and _all_ 
Bricklet gits in parallel to the generator git. Otherwise the generator and
copy scripts can't find the examples that are used in the documentation.
