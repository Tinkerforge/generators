#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ for Microcontrollers ZIP Generator
Copyright (C) 2012-2015, 2018 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>

generate_c_zip.py: Generator for C/C++ ZIP

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
from generators.uc import uc_common

class UCZipGenerator(uc_common.UCGeneratorTrait, common.ZipGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tmp_dir          = self.get_zip_dir()
        self.tmp_source_dir   = os.path.join(self.tmp_dir, 'source')
        self.tmp_bindings_dir = os.path.join(self.tmp_source_dir, 'bindings')
        self.tmp_examples_dir = os.path.join(self.tmp_dir, 'examples')

    def prepare(self):
        super().prepare()

        os.makedirs(self.tmp_source_dir)
        os.makedirs(self.tmp_bindings_dir)

    def generate(self, device):
        if not device.is_released():
            return
        if not device.has_comcu():
            return

        # Copy device examples
        tmp_examples_device_dir = os.path.join(self.tmp_examples_dir,
                                               device.get_category().under,
                                               device.get_name().under)

        if not os.path.exists(tmp_examples_device_dir):
            os.makedirs(tmp_examples_device_dir)

        for example in common.find_device_examples(device, r'^example_.*\.c$'):
            shutil.copy(example[1], tmp_examples_device_dir)

    def finish(self):
        root_dir = self.get_root_dir()

        bindings_files = [
            'base58.c',
            'base58.h',
            'config.h',
            'endian_convert.c',
            'endian_convert.h',
            'errors.inc',
            'errors.h',
            'hal_common.c',
            'hal_common.h',
            'macros.h',
            'packetbuffer.c',
            'packetbuffer.h',
            'pearson_hash.c',
            'pearson_hash.h',
            'spitfp.c',
            'spitfp.h',
            'tfp.c',
            'tfp.h',
        ]

        # Copy brick(let) specific bindings
        for filename in self.get_released_files() + ['bricklet_unknown.h', 'bricklet_unknown.c']:
            path = os.path.join(self.get_bindings_dir(), filename)
            shutil.copy(path, self.tmp_bindings_dir)

        # Copy static binding files
        for filename in bindings_files:
            path = os.path.join(root_dir, filename)
            shutil.copy(path, self.tmp_bindings_dir)

        # Copy all HALs
        for folder in next(os.walk('.'))[1]:
            if not folder.startswith('hal_'):
                continue
            shutil.copytree(os.path.join(root_dir, folder), os.path.join(self.tmp_source_dir, folder))

        shutil.copy(os.path.join(root_dir, 'beta', 'changelog.txt'),        self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'beta', 'README_EN.txt'),           self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'beta', 'README_DE.txt'),           self.tmp_dir)
        shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'), self.tmp_dir)

        shutil.copy(os.path.join(root_dir, 'beta', 'arduino.ino'),   self.tmp_source_dir)
        shutil.copy(os.path.join(root_dir, 'beta', 'arduino_esp32.ino'), self.tmp_source_dir)
        shutil.copy(os.path.join(root_dir, 'beta', 'main.c'),            self.tmp_source_dir)
        shutil.copy(os.path.join(root_dir, 'beta', 'Makefile'),          self.tmp_source_dir)
        shutil.copytree(os.path.join(root_dir, 'beta', 'demo'), os.path.join(self.tmp_source_dir, 'demo'))

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(root_dir):
    common.generate(root_dir, 'en', UCZipGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
