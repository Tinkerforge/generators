#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ ZIP Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
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
import subprocess
import glob
import re

sys.path.append(os.path.split(os.getcwd())[0])
import common

device = None

def copy_examples_for_zip():
    examples = common.find_examples(device, common.path_binding, 'c', 'example_', '.c')
    dest = os.path.join('/tmp/generator/examples/',
                        device.get_category().lower(),
                        device.get_underscore_name())

    if not os.path.exists(dest):
        os.makedirs(dest)

    for example in examples:
        shutil.copy(example[1], dest)

def make_files(device_, directory):
    global device
    device = device_

    copy_examples_for_zip()

def generate(path):
    # Make temporary generator directory
    if os.path.exists('/tmp/generator'):
        shutil.rmtree('/tmp/generator/')
    os.makedirs('/tmp/generator/bindings')
    os.chdir('/tmp/generator/bindings')

    # Copy examples
    common.generate(path, 'en', make_files, None, None, False)
    shutil.copy(common.path_binding.replace('/generators/c', '/doc/en/source/Software/example.c'),
                '/tmp/generator/examples/example_enumerate.c')

    # Copy bindings and readme
    for filename in glob.glob(path + '/bindings/*.[ch]'):
        shutil.copy(filename, '/tmp/generator/bindings')

    shutil.copy(path + '/ip_connection.c', '/tmp/generator/bindings')
    shutil.copy(path + '/ip_connection.h', '/tmp/generator/bindings')
    shutil.copy(path + '/changelog.txt', '/tmp/generator/')
    shutil.copy(path + '/readme.txt', '/tmp/generator/')

    # Make zip
    version = common.get_changelog_version(path)
    common.make_zip('c', '/tmp/generator', path, version)

if __name__ == "__main__":
    generate(os.getcwd())
