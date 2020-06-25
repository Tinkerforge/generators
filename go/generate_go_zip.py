#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Go ZIP Generator
Copyright (C) 2018 Erik Fleckstein <erik@tinkerforge.com>

generate_go_zip.py: Generator for Go ZIP

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
import subprocess
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
from generators.go import go_common

class GoZipGenerator(go_common.GoGeneratorTrait, common.ZipGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tmp_dir          = self.get_zip_dir()
        self.tmp_bindings_dir = os.path.join(self.tmp_dir, 'github.com', 'Tinkerforge' , 'go-api-bindings')
        self.tmp_examples_dir = os.path.join(self.tmp_dir, 'examples')

    def prepare(self):
        super().prepare()

        os.makedirs(self.tmp_bindings_dir)
        os.makedirs(self.tmp_examples_dir)

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        tmp_examples_device_dir = os.path.join(self.tmp_examples_dir,
                                               device.get_name().camel_abbrv + device.get_category().camel_abbrv)

        if not os.path.exists(tmp_examples_device_dir):
            os.makedirs(tmp_examples_device_dir)

        for example in common.find_device_examples(device, r'^example_.*\.go$'):
            shutil.copy(example[1], os.path.join(tmp_examples_device_dir, example[0]))

    def finish(self):
        root_dir = self.get_root_dir()

        # Copy IP Connection examples
        if self.get_config_name().space == 'Tinkerforge':
            for example in common.find_examples(root_dir, r'^example_.*\.go$'):
                shutil.copy(example[1], self.tmp_examples_dir)


        for filename in self.get_released_files():
            path = os.path.join(self.get_bindings_dir(), filename)
            target_folder = os.path.splitext(os.path.basename(filename))[0]
            target_folder = os.path.join(self.tmp_bindings_dir, target_folder)
            os.makedirs(target_folder)
            shutil.copy(path, os.path.join(target_folder, filename))

        copy_map = {
            "internal": [
                'base58.go',
                'byteconverter.go',
                'device.go',
                'bindings/device_display_names.go',
                'ipconnection.go'
            ],
            "ipconnection": [
                "ipcon_handle.go"
            ],
            "": [
                "doc.go"
            ]
        }

        top_level_files = [
            'changelog.txt',
            'readme.txt',
            'LICENSE',
        ]

        for f in top_level_files:
            shutil.copy(os.path.join(root_dir, f), self.tmp_dir)

        for dir, files in copy_map.items():
            path = os.path.join(self.tmp_bindings_dir, dir)

            if not os.path.exists(path):
                os.makedirs(path)
            for f in files:
                shutil.copy(os.path.join(root_dir, f), path)

        output = subprocess.check_output(["go", "fmt"], cwd=self.tmp_bindings_dir, stderr=subprocess.STDOUT).decode('utf-8').strip()

        if len(output) > 0:
            print("Got the following output from go fmt:")
            print(output)

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(root_dir):
    common.generate(root_dir, 'en', GoZipGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
