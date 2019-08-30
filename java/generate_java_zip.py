#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java ZIP Generator
Copyright (C) 2012-2015, 2018 Matthias Bolte <matthias@tinkerforge.com>
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
import os
import shutil

sys.path.append(os.path.split(os.getcwd())[0])
import common
import java_common

class JavaZipGenerator(java_common.JavaGeneratorTrait, common.ZipGenerator):
    def __init__(self, *args):
        common.ZipGenerator.__init__(self, *args)

        self.tmp_dir                          = self.get_tmp_dir()
        self.tmp_source_dir                   = os.path.join(self.tmp_dir, 'source')
        self.tmp_source_meta_inf_services_dir = os.path.join(self.tmp_source_dir, 'META-INF', 'services')
        self.tmp_source_com_tinkerforge_dir   = os.path.join(self.tmp_source_dir, 'com', 'tinkerforge')
        self.tmp_examples_dir                 = os.path.join(self.tmp_dir, 'examples')

    def get_bindings_name(self):
        return 'java'

    def prepare(self):
        common.recreate_dir(self.tmp_dir)
        os.makedirs(self.tmp_source_dir)
        os.makedirs(self.tmp_source_meta_inf_services_dir)
        os.makedirs(self.tmp_source_com_tinkerforge_dir)
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
            shutil.copy(os.path.join(self.get_bindings_dir(), filename), self.tmp_source_com_tinkerforge_dir)

        shutil.copy(os.path.join(self.get_bindings_dir(), 'com.tinkerforge.DeviceProvider'), self.tmp_source_meta_inf_services_dir)

        if self.get_config_name().space == 'Tinkerforge':
            shutil.copy(os.path.join(root_dir, 'BrickDaemon.java'),               self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'Device.java'),                    self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'DeviceBase.java'),                self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'DeviceListener.java'),            self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'DeviceProvider.java'),            self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'DeviceFactory.java'),             self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'IPConnection.java'),              self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'IPConnectionBase.java'),          self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'TinkerforgeException.java'),      self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'TimeoutException.java'),          self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'AlreadyConnectedException.java'), self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'NotConnectedException.java'),     self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'CryptoException.java'),           self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'NetworkException.java'),          self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'StreamOutOfSyncException.java'),  self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'InvalidParameterException.java'), self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'NotSupportedException.java'),     self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'UnknownErrorCodeException.java'), self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'TinkerforgeListener.java'),       self.tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'changelog.txt'),                  self.tmp_dir)
            shutil.copy(os.path.join(root_dir, 'readme.txt'),                     self.tmp_dir)
            shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'),   self.tmp_dir)
        else:
            shutil.copy(os.path.join(self.get_config_dir(), 'changelog.txt'),   self.tmp_dir)
            shutil.copy(os.path.join(root_dir, 'custom.txt'),                   os.path.join(self.tmp_dir, 'readme.txt'))

        # Make manifest
        version = self.get_changelog_version()

        with open(os.path.join(self.tmp_dir, 'manifest.txt'), 'w') as f:
            f.write('Bindings-Version: {0}.{1}.{2}\n'.format(*version))

        # Compile source
        if self.get_config_name().space == 'Tinkerforge':
            class_path = ''
        else:
            class_path = '-cp /tmp/generators/java/Tinkerforge.jar '

        with common.ChangedDirectory(self.tmp_dir):
            common.execute('javac ' +
                           '-Xlint ' +
                           '-source 8 ' +
                           '-target 8 ' +
                           class_path +
                           os.path.join(self.tmp_source_com_tinkerforge_dir, '*.java'),
                           shell=True)

        # Make jar
        with common.ChangedDirectory(self.tmp_source_dir):
            common.execute(['jar',
                            'cfm',
                            os.path.join(self.tmp_dir, self.get_config_name().camel + '.jar'),
                            os.path.join(self.tmp_dir, 'manifest.txt'),
                           'com',
                           'META-INF'])

        # Remove manifest
        os.remove(os.path.join(self.tmp_dir, 'manifest.txt'))

        # Remove classes
        for name in os.listdir(self.tmp_source_com_tinkerforge_dir):
            if name.endswith('.class'):
                os.remove(os.path.join(self.tmp_source_com_tinkerforge_dir, name))

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(root_dir):
    common.generate(root_dir, 'en', JavaZipGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
