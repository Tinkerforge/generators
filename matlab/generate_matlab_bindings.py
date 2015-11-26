#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MATLAB/Octave Bindings Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2015 Matthias Bolte <matthias@tinkerforge.com>

generate_matlab_bindings.py: Generator for MATLAB/Octave bindings

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

import os
import sys

sys.path.append(os.path.split(os.getcwd())[0])
import common
from java.generate_java_bindings import JavaBindingsGenerator

class MATLABBindingsGenerator(JavaBindingsGenerator):
    bindings_subdirectory_name = 'bindings_matlab'

    def get_bindings_name(self):
        return 'matlab'

    def is_matlab(self):
        return True

class OcatveBindingsGenerator(JavaBindingsGenerator):
    check_bindings_root_directory_name = False
    bindings_subdirectory_name = 'bindings_octave'

    def get_bindings_name(self):
        return 'octave'

    def is_octave(self):
        return True

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', MATLABBindingsGenerator)
    common.generate(bindings_root_directory, 'en', OcatveBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
