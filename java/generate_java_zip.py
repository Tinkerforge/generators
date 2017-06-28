#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java ZIP Generator
Copyright (C) 2012-2015 Matthias Bolte <matthias@tinkerforge.com>
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
from java_released_files import released_files

class JavaZipGenerator(common.ZipGenerator):
    tmp_dir                        = '/tmp/generator/java'
    tmp_source_dir                 = os.path.join(tmp_dir, 'source')
    tmp_source_com_tinkerforge_dir = os.path.join(tmp_source_dir, 'com', 'tinkerforge')
    tmp_examples_dir               = os.path.join(tmp_dir, 'examples')

    def get_bindings_name(self):
        return 'java'

    def prepare(self):
        common.recreate_directory(self.tmp_dir)
        os.makedirs(self.tmp_source_dir)
        os.makedirs(self.tmp_source_com_tinkerforge_dir)
        os.makedirs(self.tmp_examples_dir)

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        tmp_examples_device_dir = os.path.join(self.tmp_examples_dir,
                                               device.get_camel_case_category(),
                                               device.get_camel_case_name())

        if not os.path.exists(tmp_examples_device_dir):
            os.makedirs(tmp_examples_device_dir)

        for example in common.find_device_examples(device, r'^Example.*\.java$'):
            shutil.copy(example[1], tmp_examples_device_dir)

    def finish(self):
        root_dir = self.get_bindings_root_directory()

        # Copy IP Connection examples
        for example in common.find_examples(root_dir, r'^Example.*\.java$'):
            shutil.copy(example[1], self.tmp_examples_dir)

        # Copy bindings and readme
        for filename in released_files + ['DeviceFactory.java']:
            shutil.copy(os.path.join(root_dir, 'bindings', filename), self.tmp_source_com_tinkerforge_dir)

        shutil.copy(os.path.join(root_dir, 'BrickDaemon.java'),               self.tmp_source_com_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'Device.java'),                    self.tmp_source_com_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'DeviceBase.java'),                self.tmp_source_com_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'DeviceListener.java'),            self.tmp_source_com_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'IPConnection.java'),              self.tmp_source_com_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'IPConnectionBase.java'),          self.tmp_source_com_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'TinkerforgeException.java'),      self.tmp_source_com_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'TimeoutException.java'),          self.tmp_source_com_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'AlreadyConnectedException.java'), self.tmp_source_com_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'NotConnectedException.java'),     self.tmp_source_com_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'CryptoException.java'),           self.tmp_source_com_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'NetworkException.java'),          self.tmp_source_com_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'StreamOutOfSyncException.java'),  self.tmp_source_com_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'TinkerforgeListener.java'),       self.tmp_source_com_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'changelog.txt'),                  self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'readme.txt'),                     self.tmp_dir)
        shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'),   self.tmp_dir)

        # Make manifest
        version = common.get_changelog_version(root_dir)

        with open(os.path.join(self.tmp_dir, 'manifest.txt'), 'w') as f:
            f.write('Bindings-Version: {0}.{1}.{2}\n'.format(*version))

        # Compile source
        with common.ChangedDirectory(self.tmp_dir):
            common.execute('/usr/bin/javac ' +
                           '-Xlint ' +
                           '-source 1.6 ' +
                           '-target 1.6 ' +
                           os.path.join(self.tmp_source_com_tinkerforge_dir, '*.java'),
                           shell=True)

        # Make jar
        with common.ChangedDirectory(self.tmp_source_dir):
            common.execute(['/usr/bin/jar',
                            'cfm',
                            os.path.join(self.tmp_dir, 'Tinkerforge.jar'),
                            os.path.join(self.tmp_dir, 'manifest.txt'),
                           'com'])

        # Remove manifest
        os.remove(os.path.join(self.tmp_dir, 'manifest.txt'))

        # Remove classes
        for f in os.listdir(self.tmp_source_com_tinkerforge_dir):
            if f.endswith('.class'):
                os.remove(os.path.join(self.tmp_source_com_tinkerforge_dir, f))

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', JavaZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
