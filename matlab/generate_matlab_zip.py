#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MATLAB/Octave ZIP Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014-2015 Matthias Bolte <matthias@tinkerforge.com>

generate_matlab_zip.py: Generator for MATLAB/Octave ZIP

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
import subprocess
import glob

sys.path.append(os.path.split(os.getcwd())[0])
import common
from matlab_released_files import released_files

class MATLABZipGenerator(common.ZipGenerator):
    tmp_dir                               = '/tmp/generator/matlab'
    tmp_flavor_dir                        = {'matlab': os.path.join(tmp_dir, 'matlab'),
                                             'octave': os.path.join(tmp_dir, 'octave')}
    tmp_flavor_source_dir                 = {'matlab': os.path.join(tmp_flavor_dir['matlab'], 'source'),
                                             'octave': os.path.join(tmp_flavor_dir['octave'], 'source')}
    tmp_flavor_source_com_tinkerforge_dir = {'matlab': os.path.join(tmp_flavor_source_dir['matlab'], 'com', 'tinkerforge'),
                                             'octave': os.path.join(tmp_flavor_source_dir['octave'], 'com', 'tinkerforge')}
    tmp_flavor_examples_dir               = {'matlab': os.path.join(tmp_flavor_dir['matlab'], 'examples'),
                                             'octave': os.path.join(tmp_flavor_dir['octave'], 'examples')}

    def get_bindings_name(self):
        return 'matlab'

    def prepare(self):
        common.recreate_directory(self.tmp_dir)

        for flavor in ['matlab', 'octave']:
            os.makedirs(self.tmp_flavor_dir[flavor])
            os.makedirs(self.tmp_flavor_source_dir[flavor])
            os.makedirs(self.tmp_flavor_source_com_tinkerforge_dir[flavor])
            os.makedirs(self.tmp_flavor_examples_dir[flavor])

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        for flavor in ['matlab', 'octave']:
            tmp_examples_device_dir = os.path.join(self.tmp_flavor_examples_dir[flavor],
                                                   device.get_underscore_category(),
                                                   device.get_underscore_name())

            if not os.path.exists(tmp_examples_device_dir):
                os.makedirs(tmp_examples_device_dir)

            for example in common.find_device_examples(device, '^{0}_example_.*\.m$'.format(flavor)):
                shutil.copy(example[1], tmp_examples_device_dir)

    def finish(self):
        root_dir = self.get_bindings_root_directory()

        for flavor in ['matlab', 'octave']:
            tmp_dir = self.tmp_flavor_dir[flavor]
            tmp_source_dir = self.tmp_flavor_source_dir[flavor]
            tmp_source_com_tinkerforge_dir = self.tmp_flavor_source_com_tinkerforge_dir[flavor]
            tmp_examples_dir = self.tmp_flavor_examples_dir[flavor]

            # Copy IP Connection examples
            for example in common.find_examples(root_dir, '^' + flavor + '_example_.*\.m$'):
                shutil.copy(example[1], tmp_examples_dir)

            # Copy bindings and readme
            for filename in released_files + ['DeviceFactory.java']:
                shutil.copy(os.path.join(root_dir, 'bindings_' + flavor, filename), tmp_source_com_tinkerforge_dir)

            shutil.copy(os.path.join(root_dir, '..', 'java', 'BrickDaemon.java'),               tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'DeviceBase.java'),                tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'Device_{0}.java'.format(flavor)),               os.path.join(tmp_source_com_tinkerforge_dir, 'Device.java'))
            shutil.copy(os.path.join(root_dir, '..', 'java', 'DeviceListener.java'),            tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'IPConnection_{0}.java'.format(flavor)),         os.path.join(tmp_source_com_tinkerforge_dir, 'IPConnection.java'))
            shutil.copy(os.path.join(root_dir, '..', 'java', 'IPConnectionBase.java'),          tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'TinkerforgeException.java'),      tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'TimeoutException.java'),          tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'AlreadyConnectedException.java'), tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'NotConnectedException.java'),     tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'CryptoException.java'),           tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'NetworkException.java'),          tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'StreamOutOfSyncException.java'),  tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'TinkerforgeListener.java'),       tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'liboctaveinvokewrapper-linux-i386.so'),         tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'liboctaveinvokewrapper-linux-amd64.so'),        tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'liboctaveinvokewrapper-linux-arm.so'),          tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'liboctaveinvokewrapper-windows-x86.dll'),       tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'liboctaveinvokewrapper-windows-amd64.dll'),     tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'liboctaveinvokewrapper-mac-x86_64.dynlib'),     tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'changelog.txt'),                                self.tmp_dir)
            shutil.copy(os.path.join(root_dir, 'readme.txt'),                                   self.tmp_dir)
            shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'),                 self.tmp_dir)

            # Make manifest
            version = common.get_changelog_version(root_dir)

            with open(os.path.join(tmp_dir, 'manifest.txt'), 'w') as f:
                f.write('Bindings-Version: {1}.{2}.{3}\nBindings-Flavor: {0}\n'.format(flavor.upper(), *version))

            # Make jar
            with common.ChangedDirectory(tmp_dir):
                if flavor == 'octave':
                    classpath = '-classpath {0} '.format(os.path.join(root_dir, 'octave.jar'))
                else:
                    classpath = ''

                common.execute('/usr/bin/javac ' +
                               classpath +
                               '-Xlint ' +
                               '-source 1.6 ' +
                               '-target 1.6 ' +
                               os.path.join(tmp_source_com_tinkerforge_dir, '*.java'),
                               shell=True)

            with common.ChangedDirectory(tmp_source_dir):
                common.execute(['/usr/bin/jar',
                                'cfm',
                                os.path.join(tmp_dir, 'Tinkerforge.jar'),
                                os.path.join(tmp_dir, 'manifest.txt'),
                                'com'])

            # Remove manifest
            os.remove(os.path.join(tmp_dir, 'manifest.txt'))

            # Remove classes
            for f in os.listdir(tmp_source_com_tinkerforge_dir):
                if f.endswith('.class'):
                    os.remove(os.path.join(tmp_source_com_tinkerforge_dir, f))

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', MATLABZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
