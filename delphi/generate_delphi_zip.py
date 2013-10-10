#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Delphi ZIP Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_delphi_doc.py: Generator for Delphi ZIP

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
import re

sys.path.append(os.path.split(os.getcwd())[0])
import common
import delphi_common
from delphi_released_files import released_files

device = None

def copy_examples_for_zip():
    if not device.is_released():
        return

    examples = common.find_examples(device, common.path_binding, 'delphi', 'Example', '.pas')
    dest = os.path.join('/tmp/generator/examples/',
                        device.get_category(),
                        device.get_camel_case_name())

    if not os.path.exists(dest):
        os.makedirs(dest)

    for example in examples:
        shutil.copy(example[1], dest)

def make_files(device_, directory):
    global device
    device = device_

    copy_examples_for_zip()

class DelphiZipGenerator(common.Generator):
    def prepare(self):
        pass

    def generate(self, device):
        make_files(device, self.get_bindings_root_directory())

    def finish(self):
        pass

def generate(path):
    # Make temporary generator directory
    if os.path.exists('/tmp/generator'):
        shutil.rmtree('/tmp/generator/')
    os.makedirs('/tmp/generator/bindings')
    os.chdir('/tmp/generator/bindings')

    # Copy examples
    common.generate(path, 'en', DelphiZipGenerator, False)
    shutil.copy(common.path_binding.replace('/generators/delphi', '/doc/en/source/Software/Example.pas'),
                '/tmp/generator/examples/ExampleEnumerate.pas')

    # Copy bindings and readme
    for filename in released_files:
        shutil.copy(os.path.join(path, 'bindings', filename), '/tmp/generator/bindings')

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
