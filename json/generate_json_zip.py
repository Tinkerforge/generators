#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JSON ZIP Generator
Copyright (C) 2017-2018 Matthias Bolte <matthias@tinkerforge.com>

generate_json_zip.py: Generator for JSON ZIP

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
from generators.json.generate_json_bindings import JSONGeneratorTrait

class JSONZipGenerator(JSONGeneratorTrait, common.ZipGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tmp_dir        = self.get_zip_dir()
        self.tmp_source_dir = os.path.join(self.tmp_dir, 'source')

    def prepare(self):
        super().prepare()

        os.makedirs(self.tmp_source_dir)

    def generate(self, device):
        pass

    def finish(self):
        root_dir = self.get_root_dir()

        # Copy bindings and readme
        for filename in self.get_released_files():
            shutil.copy(os.path.join(self.get_bindings_dir(), filename), self.tmp_source_dir)

        if self.get_config_name().space == 'Tinkerforge':
            shutil.copy(os.path.join(root_dir, 'changelog.txt'),                self.tmp_dir)
            shutil.copy(os.path.join(root_dir, 'readme.txt'),                   self.tmp_dir)
            shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'), self.tmp_dir)
        else:
            shutil.copy(os.path.join(self.get_config_dir(), 'changelog.txt'),   self.tmp_dir)
            shutil.copy(os.path.join(root_dir, 'custom.txt'),                   os.path.join(self.tmp_dir, 'readme.txt'))

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(root_dir, language):
    common.generate(root_dir, language, JSONZipGenerator)

if __name__ == '__main__':
    common.dockerize('json', __file__)

    generate(os.getcwd(), 'en')
