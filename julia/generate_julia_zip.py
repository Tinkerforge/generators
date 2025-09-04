#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Julia ZIP Generator
Copyright (C) 2012-2015, 2017-2018 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_julia_zip.py: Generator for Julia ZIP

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
from generators.julia import julia_common

class JuliaZipGenerator(julia_common.JuliaGeneratorTrait, common.ZipGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tmp_dir                    = self.get_zip_dir()
        self.tmp_source_dir             = os.path.join(self.tmp_dir, 'src')
        self.tmp_source_devices_dir     = os.path.join(self.tmp_source_dir, 'devices')
        self.tmp_examples_dir           = os.path.join(self.tmp_dir, 'examples')

    def prepare(self):
        super().prepare()

        os.makedirs(self.tmp_source_dir)
        os.makedirs(self.tmp_source_devices_dir)
        os.makedirs(self.tmp_examples_dir)

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        tmp_examples_device = os.path.join(self.tmp_examples_dir,
                                           device.get_category().under,
                                           device.get_name().under)

        if not os.path.exists(tmp_examples_device):
            os.makedirs(tmp_examples_device)

        for example in common.find_device_examples(device, r'^example_.*\.jl$'):
            shutil.copy(example[1], tmp_examples_device)

    def finish(self):
        root_dir = self.get_root_dir()

        # Copy IP Connection examples
        if self.get_config_name().space == 'Tinkerforge':
            for example in common.find_examples(root_dir, r'^example_.*\.jl$'):
                shutil.copy(example[1], self.tmp_examples_dir)

        # Copy bindings and readme
        for filename in self.get_released_files() + ['device_factory.jl']:
            shutil.copy(os.path.join(self.get_bindings_dir(), filename), self.tmp_source_devices_dir)

        shutil.copy(os.path.join(root_dir, 'Tinkerforge.jl'),               self.tmp_source_dir)
        shutil.copy(os.path.join(root_dir, 'ip_connection_base.jl'),        self.tmp_source_dir)
        shutil.copy(os.path.join(root_dir, 'ip_connection.jl'),             self.tmp_source_dir)
        shutil.copy(os.path.join(root_dir, 'changelog.txt'),                self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'readme.txt'),                   self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'LICENSE'),                      self.tmp_dir)

        # Make Project.toml
        version = self.get_changelog_version()

        common.specialize_template(os.path.join(root_dir, 'Project.toml.template'),
                                   os.path.join(self.tmp_dir, 'Project.toml'),
                                   {'<<VERSION>>': '.'.join(version)})

        # Make zip
        #self.create_zip_file(self.tmp_dir)

def generate(root_dir, language, internal):
    common.generate(root_dir, language, internal, JuliaZipGenerator)

if __name__ == '__main__':
    args = common.dockerize('julia', __file__, add_internal_argument=True)

    generate(os.getcwd(), 'en', args.internal)
