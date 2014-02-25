#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ ZIP Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_c_zip.py: Generator for C/C++ ZIP

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
import shutil

sys.path.append(os.path.split(os.getcwd())[0])
import common
from c_released_files import released_files

class CZipGenerator(common.Generator):
    def get_bindings_name(self):
        return 'c'

    def prepare(self):
        common.recreate_directory('/tmp/generator')
        os.makedirs('/tmp/generator/bindings')
        os.makedirs('/tmp/generator/examples')

    def generate(self, device):
        if not device.is_released():
            return

        # Copy examples
        examples = common.find_examples(device, '^example_.*\.c$')
        dest = os.path.join('/tmp/generator/examples', device.get_category().lower(), device.get_underscore_name())

        if not os.path.exists(dest):
            os.makedirs(dest)

        for example in examples:
            shutil.copy(example[1], dest)

    def finish(self):
        root = self.get_bindings_root_directory()

        # Copy examples
        shutil.copy(root.replace('/generators/c', '/doc/en/source/Software/example.c'),
                    '/tmp/generator/examples/example_enumerate.c')

        # Copy bindings and readme
        for filename in released_files:
            shutil.copy(os.path.join(root, 'bindings', filename), '/tmp/generator/bindings')

        shutil.copy(os.path.join(root, 'ip_connection.c'), '/tmp/generator/bindings')
        shutil.copy(os.path.join(root, 'ip_connection.h'), '/tmp/generator/bindings')
        shutil.copy(os.path.join(root, 'changelog.txt'), '/tmp/generator')
        shutil.copy(os.path.join(root, 'readme.txt'), '/tmp/generator')

        # Make zip
        version = common.get_changelog_version(root)
        common.make_zip(self.get_bindings_name(), '/tmp/generator', root, version)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', CZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
