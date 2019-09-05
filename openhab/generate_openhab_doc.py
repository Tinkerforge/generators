#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
openHAB Documentation Generator
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>

generate_openhab_doc.py: Generator for openHAB documentation

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
import os

sys.path.append(os.path.split(os.getcwd())[0])
import common

class OpenHABDocGenerator(common.DocGenerator):
    def get_bindings_name(self):
        return 'openhab'

    def get_bindings_display_name(self):
        return 'openHAB'

    def get_doc_rst_filename_part(self):
        return 'openhab'

    def get_doc_example_regex(self):
        return r'^example_.*\.txt$'

    def generate(self, device):
        pass

    def get_doc_null_value_name(self):
        return 'null'

    def get_doc_formatted_param(self, element):
        return element.get_name().camel

def generate(root_dir, language):
    common.generate(root_dir, language, OpenHABDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print('=== Generating %s ===' % language)
        generate(os.getcwd(), language)
