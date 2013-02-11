#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Delphi Documentation Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_delphi_doc.py: Generator for Delphi documentation

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
import delphi_common

device = None

def copy_examples_for_zip():
    examples = common.find_examples(device, common.path_binding, 'delphi', 'Example', '.pas')
    dest = os.path.join('/tmp/generator/examples/',
                        device.get_category(),
                        device.get_camel_case_name())

    if not os.path.exists(dest):
        os.makedirs(dest)

    for example in examples:
        shutil.copy(example[1], dest)

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)

    copy_examples_for_zip()

def generate(path):
    common.path_binding = path
    path_list = path.split('/')
    path_list[-1] = 'configs'
    path_config = '/'.join(path_list)
    sys.path.append(path_config)
    configs = os.listdir(path_config)

    # Make temporary generator directory
    if os.path.exists('/tmp/generator'):
        shutil.rmtree('/tmp/generator/')
    os.makedirs('/tmp/generator/bindings')
    os.chdir('/tmp/generator/bindings')

    # Copy examples
    common.import_and_make(configs, path, make_files)
    shutil.copy(common.path_binding.replace('/generators/delphi', '/doc/en/source/Software/Example.pas'),
                '/tmp/generator/examples/ExampleEnumerate.pas')

    # Copy bindings and readme
    for filename in glob.glob(path + '/bindings/*.pas'):
        shutil.copy(filename, '/tmp/generator/bindings')

    shutil.copy(path + '/Base58.pas', '/tmp/generator/bindings')
    shutil.copy(path + '/BlockingQueue.pas', '/tmp/generator/bindings')
    shutil.copy(path + '/Device.pas', '/tmp/generator/bindings')
    shutil.copy(path + '/IPConnection.pas', '/tmp/generator/bindings')
    shutil.copy(path + '/LEConverter.pas', '/tmp/generator/bindings')
    shutil.copy(path + '/TimedSemaphore.pas', '/tmp/generator/bindings')
    shutil.copy(path + '/changelog.txt', '/tmp/generator/')
    shutil.copy(path + '/readme.txt', '/tmp/generator/')

    # Make zip
    version = common.get_changelog_version(path)
    common.make_zip('delphi', '/tmp/generator', path, version)

if __name__ == "__main__":
    generate(os.getcwd())
