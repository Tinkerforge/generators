#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Visual Basic .NET Bindings Generator
Copyright (C) 2013, 2018 Matthias Bolte <matthias@tinkerforge.com>

generate_vbnet_bindings.py: Generator for Visual Basic .NET bindings

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

sys.path.append(os.path.split(os.getcwd())[0])
import common
from csharp.generate_csharp_bindings import CSharpBindingsGenerator

class VBNETBindingsGenerator(CSharpBindingsGenerator):
    def get_bindings_name(self):
        return 'vbnet'

    def get_bindings_display_name(self):
        return 'Visual Basic .NET'

    def get_doc_null_value_name(self):
        return 'Nothing'

def generate(root_dir):
    common.generate(root_dir, 'en', VBNETBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
