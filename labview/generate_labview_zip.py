#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LabVIEW ZIP Generator
Copyright (C) 2012-2015, 2018 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_labview_zip.py: Generator for LabVIEW ZIP

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

if sys.hexversion < 0x3050000:
    print('Python >= 3.5 required')
    sys.exit(1)

import os
import shutil
import subprocess
import importlib.util

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
    generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
    generators_module = importlib.util.module_from_spec(generators_spec)

    generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common

class LabVIEWZipGenerator(common.ZipGenerator):
    def __init__(self, *args):
        common.ZipGenerator.__init__(self, *args)

        self.tmp_dir                    = self.get_tmp_dir()
        self.tmp_source_tinkerforge_dir = os.path.join(self.tmp_dir, 'source', 'Tinkerforge')
        self.tmp_examples_dir           = os.path.join(self.tmp_dir, 'examples')
        self.tmp_examples_10_dir        = os.path.join(self.tmp_examples_dir, '10.0')

    def get_bindings_name(self):
        return 'labview'

    def get_doc_null_value_name(self):
        return 'null'

    def get_doc_formatted_param(self, element):
        return element.get_name().headless

    def prepare(self):
        common.recreate_dir(self.tmp_dir)
        os.makedirs(self.tmp_source_tinkerforge_dir)
        os.makedirs(self.tmp_examples_dir)
        os.makedirs(self.tmp_examples_10_dir)

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        tmp_examples_device_dir = os.path.join(self.tmp_examples_dir,
                                               device.get_category().camel,
                                               device.get_name().camel)
        tmp_examples_device_10_dir = os.path.join(self.tmp_examples_dir,
                                                  device.get_category().camel,
                                                  device.get_name().camel,
                                                  '10.0')

        if not os.path.exists(tmp_examples_device_dir):
            os.makedirs(tmp_examples_device_dir)

        if not os.path.exists(tmp_examples_device_10_dir):
            os.makedirs(tmp_examples_device_10_dir)

        for example in common.find_device_examples(device, '^Example .*\.vi$'):
            shutil.copy(example[1], tmp_examples_device_dir)

            parts = os.path.split(example[1])
            shutil.copy(os.path.join(parts[0], '10.0', parts[1]), tmp_examples_device_10_dir)

    def finish(self):
        root_dir = self.get_root_dir()

        # Copy IP Connection examples
        if self.get_config_name().space == 'Tinkerforge':
            for example in common.find_examples(root_dir, '^Example .*\.vi$'):
                shutil.copy(example[1], self.tmp_examples_dir)

                parts = os.path.split(example[1])
                shutil.copy(os.path.join(parts[0], '10.0', parts[1]), self.tmp_examples_10_dir)

        # Copy bindings and readme
        for filename in self.get_released_files():
            shutil.copy(os.path.join(self.get_bindings_dir(), filename), self.tmp_source_tinkerforge_dir)

        shutil.copy(os.path.join(root_dir, '..', 'csharp', 'IPConnection.cs'), self.tmp_source_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'changelog.txt'),                   self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'readme.txt'),                      self.tmp_dir)
        shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'),    self.tmp_dir)

        # Make AssemblyInfo.cs
        version = self.get_changelog_version()

        common.specialize_template(os.path.join(root_dir, '..', 'csharp', 'AssemblyInfo.cs.template'),
                                   os.path.join(self.tmp_source_tinkerforge_dir, 'AssemblyInfo.cs'),
                                   {'<<BINDINGS>>': 'LabVIEW',
                                    '<<VERSION>>': '.'.join(version)})

        # Make dll
        for sdk in [2, 4]:
            os.makedirs(os.path.join(self.tmp_dir, 'net{0}0'.format(sdk)))

            with common.ChangedDirectory(self.tmp_dir):
                common.execute(['mcs',
                                '/optimize+',
                                '/warn:4',
                                '/warnaserror',
                                '/sdk:{0}'.format(sdk),
                                '/target:library',
                                '/out:' + os.path.join(self.tmp_dir, 'net{0}0'.format(sdk), 'Tinkerforge.dll'),
                                os.path.join(self.tmp_source_tinkerforge_dir, '*.cs')])

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(root_dir):
    common.generate(root_dir, 'en', LabVIEWZipGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
