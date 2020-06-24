#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java ZIP Generator
Copyright (C) 2012-2015, 2018, 2020 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_java_zip.py: Generator for Java ZIP

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
from generators.java import java_common

class JavaZipGenerator(java_common.JavaGeneratorTrait, common.ZipGenerator):
    def __init__(self, *args):
        common.ZipGenerator.__init__(self, *args)

        self.tmp_dir                                            = self.get_tmp_dir()
        self.tmp_source_dir                                     = os.path.join(self.tmp_dir, 'source')
        self.tmp_source_src_main_java_com_tinkerforge_dir       = os.path.join(self.tmp_source_dir, 'src', 'main', 'java', 'com', 'tinkerforge')
        self.tmp_source_src_main_resources_metainf_services_dir = os.path.join(self.tmp_source_dir, 'src', 'main', 'resources', 'META-INF', 'services')
        self.tmp_source_target_dir                              = os.path.join(self.tmp_source_dir, 'target')
        self.tmp_examples_dir                                   = os.path.join(self.tmp_dir, 'examples')

    def get_bindings_name(self):
        return 'java'

    def prepare(self):
        common.recreate_dir(self.tmp_dir)
        os.makedirs(self.tmp_source_dir)
        os.makedirs(self.tmp_source_src_main_java_com_tinkerforge_dir)
        os.makedirs(self.tmp_source_src_main_resources_metainf_services_dir)
        os.makedirs(self.tmp_examples_dir)

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        tmp_examples_device_dir = os.path.join(self.tmp_examples_dir,
                                               device.get_category().camel,
                                               device.get_name().camel)

        if not os.path.exists(tmp_examples_device_dir):
            os.makedirs(tmp_examples_device_dir)

        for example in common.find_device_examples(device, r'^Example.*\.java$'):
            shutil.copy(example[1], tmp_examples_device_dir)

    def finish(self):
        root_dir = self.get_root_dir()

        # Copy IP Connection examples
        if self.get_config_name().space == 'Tinkerforge':
            for example in common.find_examples(root_dir, r'^Example.*\.java$'):
                shutil.copy(example[1], self.tmp_examples_dir)

        # Copy bindings and readme
        for filename in self.get_released_files():
            shutil.copy(os.path.join(self.get_bindings_dir(), filename), self.tmp_source_src_main_java_com_tinkerforge_dir)

        shutil.copy(os.path.join(self.get_bindings_dir(), 'com.tinkerforge.DeviceProvider'), self.tmp_source_src_main_resources_metainf_services_dir)

        if self.get_config_name().space == 'Tinkerforge':
            shutil.copy(os.path.join(root_dir, 'BrickDaemon.java'),                  self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'Device.java'),                       self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'DeviceBase.java'),                   self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'DeviceListener.java'),               self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'DeviceProvider.java'),               self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'DeviceFactory.java'),                self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'IPConnection.java'),                 self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'IPConnectionBase.java'),             self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'TinkerforgeException.java'),         self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'TimeoutException.java'),             self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'AlreadyConnectedException.java'),    self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'NotConnectedException.java'),        self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'CryptoException.java'),              self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'NetworkException.java'),             self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'StreamOutOfSyncException.java'),     self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'InvalidParameterException.java'),    self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'NotSupportedException.java'),        self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'UnknownErrorCodeException.java'),    self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'WrongDeviceTypeException.java'),     self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'DeviceReplacedException.java'),      self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'WrongResponseLengthException.java'), self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'TinkerforgeListener.java'),          self.tmp_source_src_main_java_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'changelog.txt'),                     self.tmp_dir)
            shutil.copy(os.path.join(root_dir, 'readme.txt'),                        self.tmp_dir)
            shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'),      self.tmp_dir)
        else:
            shutil.copy(os.path.join(self.get_config_dir(), 'changelog.txt'),        self.tmp_dir)
            shutil.copy(os.path.join(root_dir, 'custom.txt'),                        os.path.join(self.tmp_dir, 'readme.txt'))

        # Make pom.xml
        version = self.get_changelog_version()

        if self.get_config_name().space == 'Tinkerforge':
            common.specialize_template(os.path.join(root_dir, 'pom.xml.jar-template'),
                                       os.path.join(self.tmp_source_dir, 'pom.xml'),
                                       {'{{VERSION}}': '.'.join(version)})
        else:
            common.specialize_template(os.path.join(root_dir, 'pom.xml.custom-template'),
                                       os.path.join(self.tmp_source_dir, 'pom.xml'),
                                       {'{{CONFIG_NAME}}': self.get_config_name().dash,
                                        '{{VERSION}}': '.'.join(version),
                                        '{{TINKERFORGE_VERSION}}': '.'.join(common.get_changelog_version(root_dir))})

        # Compile source
        with common.ChangedDirectory(self.tmp_source_dir):
            common.execute(['mvn', 'clean', 'verify'])

        os.rename(os.path.join(self.tmp_source_target_dir, '{0}-{1}.{2}.{3}.jar'.format(self.get_config_name().dash, *version)),
                  os.path.join(self.tmp_dir, '{0}.jar'.format(self.get_config_name().camel)))

        shutil.rmtree(self.tmp_source_target_dir)

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(root_dir):
    common.generate(root_dir, 'en', JavaZipGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
