#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MQTT ZIP Generator
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>

generate_MQTT_zip.py: Generator for MQTT ZIP

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
from generators.mqtt import mqtt_common

class MQTTZipGenerator(mqtt_common.MQTTGeneratorTrait, common.ZipGenerator):
    def __init__(self, *args):
        common.ZipGenerator.__init__(self, *args)

        self.tmp_dir          = self.get_tmp_dir()
        self.tmp_examples_dir = os.path.join(self.tmp_dir, 'examples')

    def prepare(self):
        common.recreate_dir(self.tmp_dir)
        os.makedirs(self.tmp_examples_dir)

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        tmp_examples_device_dir = os.path.join(self.tmp_examples_dir,
                                               device.get_category().under,
                                               device.get_name().under)

        if not os.path.exists(tmp_examples_device_dir):
            os.makedirs(tmp_examples_device_dir)

        for example in common.find_device_examples(device, r'^example-.*\.txt$'):
            shutil.copy(example[1], tmp_examples_device_dir)

    def finish(self):
        root_dir = self.get_root_dir()
        bindings_dir = self.get_bindings_dir()

        # Copy IP Connection examples
        if self.get_config_name().space == 'Tinkerforge':
            for example in common.find_examples(root_dir, r'^example-.*\.txt$'):
                shutil.copy(example[1], self.tmp_examples_dir)

        # Copy bindings and readme
        shutil.copy(os.path.join(bindings_dir, 'tinkerforge_mqtt'),           self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'tinkerforge_mqtt.service'),       self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'changelog.txt'),                  self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'readme.txt'),                     self.tmp_dir)
        shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'),   self.tmp_dir)

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(root_dir):
    common.generate(root_dir, 'en', MQTTZipGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
