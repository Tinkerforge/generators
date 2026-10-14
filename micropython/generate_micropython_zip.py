#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MicroPython ZIP Generator
Created by René Rohner
Copyright (C) 2026 Tinkerforge GmbH

generate_micropython_zip.py: Generator for MicroPython ZIP

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
import shutil
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
from generators.micropython import micropython_common

class MicroPythonZipGenerator(micropython_common.MicroPythonGeneratorTrait, common.ZipGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tmp_dir          = self.get_zip_dir()
        self.tmp_source_dir   = os.path.join(self.tmp_dir, 'source')
        self.tmp_examples_dir = os.path.join(self.tmp_dir, 'examples')
        self.tmp_stubs_dir    = os.path.join(self.tmp_dir, 'stubs')

    def prepare(self):
        super().prepare()

        os.makedirs(self.tmp_source_dir)
        os.makedirs(self.tmp_examples_dir)
        os.makedirs(self.tmp_stubs_dir)

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        tmp_examples_device = os.path.join(self.tmp_examples_dir,
                                           device.get_category().under,
                                           device.get_name().under)

        if not os.path.exists(tmp_examples_device):
            os.makedirs(tmp_examples_device)

        for example in common.find_device_examples(device, r'^example_.*\.py$'):
            shutil.copy(example[1], tmp_examples_device)

    def finish(self):
        root_dir = self.get_root_dir()

        # Copy IP Connection examples
        if self.get_config_name().space == 'Tinkerforge':
            for example in common.find_examples(root_dir, r'^example_.*\.py$'):
                shutil.copy(example[1], self.tmp_examples_dir)

        # Copy bindings and readme (flat layout, no package subdirectory)
        for filename in self.get_released_files() + ['device_factory.py']:
            shutil.copy(os.path.join(self.get_bindings_dir(), filename), self.tmp_source_dir)

        shutil.copy(os.path.join(root_dir, 'ip_connection.py'),             self.tmp_source_dir)
        shutil.copy(os.path.join(root_dir, 'changelog.txt'),                self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'readme.txt'),                   self.tmp_dir)
        shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'), self.tmp_dir)

        # Copy type stubs for IDE support
        stubs_dir = os.path.join(root_dir, 'stubs')

        if os.path.exists(stubs_dir):
            for filename in os.listdir(stubs_dir):
                if filename.endswith('.pyi'):
                    shutil.copy(os.path.join(stubs_dir, filename), self.tmp_stubs_dir)

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(root_dir, language, internal):
    common.generate(root_dir, language, internal, MicroPythonZipGenerator)

if __name__ == '__main__':
    args = common.dockerize('micropython', __file__, add_internal_argument=True)

    generate(os.getcwd(), 'en', args.internal)
