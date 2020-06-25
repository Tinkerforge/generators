#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MATLAB/Octave Bindings Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2015, 2018 Matthias Bolte <matthias@tinkerforge.com>

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

import sys

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import importlib.util
import importlib.machinery

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

    if sys.hexversion < 0x3050000:
        generators_module = importlib.machinery.SourceFileLoader('generators', os.path.join(generators_dir, '__init__.py')).load_module()
    else:
        generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
        generators_module = importlib.util.module_from_spec(generators_spec)

        generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common
from generators.java.generate_java_bindings import JavaBindingsGenerator
from generators.matlab import matlab_common

class MATLABBindingsGenerator(matlab_common.MATLABGeneratorTrait, JavaBindingsGenerator):
    def get_bindings_name(self):
        return 'matlab'

    def get_bindings_display_name(self):
        return 'MATLAB'

    def is_matlab(self):
        return True

class OcatveBindingsGenerator(matlab_common.MATLABGeneratorTrait, JavaBindingsGenerator):
    check_root_dir_name = False
    recreate_bindings_dir = False

    def get_bindings_name(self):
        return 'octave'

    def get_bindings_display_name(self):
        return 'Octave'

    def is_octave(self):
        return True

def generate(root_dir):
    print('=== Generating MATLAB ===')
    common.generate(root_dir, 'en', MATLABBindingsGenerator)

    print('=== Generating Octave ===')
    common.generate(root_dir, 'en', OcatveBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
