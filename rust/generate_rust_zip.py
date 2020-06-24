#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Rust ZIP Generator
Copyright (C) 2018 Erik Fleckstein <erik@tinkerforge.com>

generate_rust_zip.py: Generator for Rust ZIP

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
from generators.rust import rust_common

class RustZipGenerator(rust_common.RustGeneratorTrait, common.ZipGenerator):
    def __init__(self, *args):
        common.ZipGenerator.__init__(self, *args)

        self.tmp_dir          = self.get_tmp_dir()
        self.tmp_source_dir   = os.path.join(self.tmp_dir, 'src')
        self.tmp_bindings_dir = os.path.join(self.tmp_source_dir, 'bindings')
        self.tmp_examples_dir = os.path.join(self.tmp_dir, 'examples')

    def prepare(self):
        common.recreate_dir(self.tmp_dir)
        os.makedirs(self.tmp_source_dir)
        os.makedirs(self.tmp_bindings_dir)
        os.makedirs(self.tmp_examples_dir)

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        tmp_examples_device_dir = os.path.join(self.tmp_examples_dir,
                                               device.get_name().under + "_" + device.get_category().under)

        if not os.path.exists(tmp_examples_device_dir):
            os.makedirs(tmp_examples_device_dir)

        for example in common.find_device_examples(device, r'^example_.*\.rs$'):
            shutil.copy(example[1], os.path.join(tmp_examples_device_dir, example[0]))
            #shutil.copy(example[1], os.path.join(self.tmp_examples_dir, device.get_name().under + "_" + example[0]))

    def finish(self):
        root_dir = self.get_root_dir()

        # Copy IP Connection examples
        if self.get_config_name().space == 'Tinkerforge':
            for example in common.find_examples(root_dir, r'^example_.*\.rs$'):
                shutil.copy(example[1], self.tmp_examples_dir)


        for filename in self.get_released_files():
            path = os.path.join(self.get_bindings_dir(), filename)
            shutil.copy(path, self.tmp_bindings_dir)

        source_files = [
            'base58.rs',
            'converting_receiver.rs',
            'converting_callback_receiver.rs',
            'converting_high_level_callback_receiver.rs',
            'device.rs',
            'ip_connection.rs',
            'low_level_traits.rs',
        ]
        bindings_files = ['mod.rs']
        bindings_source_files = ['lib.rs', 'byte_converter.rs']
        bindings_top_level_files = ['Cargo.toml']
        top_level_files = [
            '.gitignore',
            'rustfmt.toml',
            'changelog.txt',
            'readme.txt',
            'readme.md',
            'LICENSE-APACHE',
            'LICENSE-CC0',
            'LICENSE-MIT'
        ]

        if self.get_config_name().space == 'Tinkerforge':
            for f in top_level_files:
                shutil.copy(os.path.join(root_dir, f), self.tmp_dir)
            for f in source_files:
                shutil.copy(os.path.join(root_dir, f), self.tmp_source_dir)
            for f in bindings_files:
                shutil.copy(os.path.join(root_dir, 'bindings', f), self.tmp_bindings_dir)
            for f in bindings_source_files:
                shutil.copy(os.path.join(root_dir, 'bindings', f), self.tmp_source_dir)
            for f in bindings_top_level_files:
                shutil.copy(os.path.join(root_dir, 'bindings', f), self.tmp_dir)
        else:
            shutil.copy(os.path.join(self.get_config_dir(), 'changelog.txt'),   self.tmp_dir)
            shutil.copy(os.path.join(root_dir, 'custom.txt'),                   os.path.join(self.tmp_dir, 'readme.txt'))

        output = subprocess.check_output(["cargo", "fmt"], cwd=self.tmp_dir, stderr=subprocess.STDOUT).decode('utf-8').strip()

        if len(output) > 0:
            print("Got the following output from cargo fmt:")
            print(output)

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(root_dir):
    common.generate(root_dir, 'en', RustZipGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
