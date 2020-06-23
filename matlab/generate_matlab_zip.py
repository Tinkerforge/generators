#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MATLAB/Octave ZIP Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014-2015, 2018, 2020 Matthias Bolte <matthias@tinkerforge.com>

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
from generators.matlab import matlab_common

class MATLABZipGenerator(matlab_common.MATLABGeneratorTrait, common.ZipGenerator):
    def __init__(self, *args):
        common.ZipGenerator.__init__(self, *args)

        self.tmp_dir                                 = self.get_tmp_dir()
        self.tmp_flavor_dir                          = {'matlab': os.path.join(self.tmp_dir, 'matlab'),
                                                        'octave': os.path.join(self.tmp_dir, 'octave')}
        self.tmp_flavor_source_dir                   = {'matlab': os.path.join(self.tmp_flavor_dir['matlab'], 'source'),
                                                        'octave': os.path.join(self.tmp_flavor_dir['octave'], 'source')}
        self.tmp_flavor_source_meta_inf_services_dir = {'matlab': os.path.join(self.tmp_flavor_source_dir['matlab'], 'META-INF', 'services'),
                                                        'octave': os.path.join(self.tmp_flavor_source_dir['octave'], 'META-INF', 'services')}
        self.tmp_flavor_source_com_tinkerforge_dir   = {'matlab': os.path.join(self.tmp_flavor_source_dir['matlab'], 'com', 'tinkerforge'),
                                                        'octave': os.path.join(self.tmp_flavor_source_dir['octave'], 'com', 'tinkerforge')}
        self.tmp_flavor_examples_dir                 = {'matlab': os.path.join(self.tmp_flavor_dir['matlab'], 'examples'),
                                                        'octave': os.path.join(self.tmp_flavor_dir['octave'], 'examples')}

    def get_bindings_name(self):
        return 'matlab'

    def prepare(self):
        common.recreate_dir(self.tmp_dir)

        for flavor in ['matlab', 'octave']:
            os.makedirs(self.tmp_flavor_dir[flavor])
            os.makedirs(self.tmp_flavor_source_dir[flavor])
            os.makedirs(self.tmp_flavor_source_meta_inf_services_dir[flavor])
            os.makedirs(self.tmp_flavor_source_com_tinkerforge_dir[flavor])
            os.makedirs(self.tmp_flavor_examples_dir[flavor])

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        for flavor in ['matlab', 'octave']:
            tmp_examples_device_dir = os.path.join(self.tmp_flavor_examples_dir[flavor],
                                                   device.get_category().under,
                                                   device.get_name().under)

            if not os.path.exists(tmp_examples_device_dir):
                os.makedirs(tmp_examples_device_dir)

            for example in common.find_device_examples(device, r'^{0}_example_.*\.m$'.format(flavor)):
                shutil.copy(example[1], tmp_examples_device_dir)

    def finish(self):
        root_dir = self.get_root_dir()

        for flavor in ['matlab', 'octave']:
            tmp_dir = self.tmp_flavor_dir[flavor]
            tmp_source_dir = self.tmp_flavor_source_dir[flavor]
            tmp_source_meta_inf_services_dir = self.tmp_flavor_source_meta_inf_services_dir[flavor]
            tmp_source_com_tinkerforge_dir = self.tmp_flavor_source_com_tinkerforge_dir[flavor]
            tmp_examples_dir = self.tmp_flavor_examples_dir[flavor]

            # Copy IP Connection examples
            if self.get_config_name().space == 'Tinkerforge':
                for example in common.find_examples(root_dir, '^' + flavor + r'_example_.*\.m$'):
                    shutil.copy(example[1], tmp_examples_dir)

            # Copy bindings and readme
            for filename in self.get_released_files():
                shutil.copy(os.path.join(root_dir, self.get_bindings_dir(), flavor, filename), tmp_source_com_tinkerforge_dir)

            shutil.copy(os.path.join(self.get_bindings_dir(), flavor, 'com.tinkerforge.DeviceProvider'), tmp_source_meta_inf_services_dir)

            shutil.copy(os.path.join(root_dir, '..', 'java', 'BrickDaemon.java'),                  tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'DeviceBase.java'),                   tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'Device_{0}.java'.format(flavor)),                  os.path.join(tmp_source_com_tinkerforge_dir, 'Device.java'))
            shutil.copy(os.path.join(root_dir, '..', 'java', 'DeviceListener.java'),               tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'DeviceProvider.java'),               tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'DeviceFactory.java'),                tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'IPConnection_{0}.java'.format(flavor)),            os.path.join(tmp_source_com_tinkerforge_dir, 'IPConnection.java'))
            shutil.copy(os.path.join(root_dir, '..', 'java', 'IPConnectionBase.java'),             tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'TinkerforgeException.java'),         tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'TimeoutException.java'),             tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'AlreadyConnectedException.java'),    tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'NotConnectedException.java'),        tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'CryptoException.java'),              tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'NetworkException.java'),             tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'StreamOutOfSyncException.java'),     tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'InvalidParameterException.java'),    tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'NotSupportedException.java'),        tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'UnknownErrorCodeException.java'),    tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'WrongDeviceTypeException.java'),     tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'DeviceReplacedException.java'),      tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'WrongResponseLengthException.java'), tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, '..', 'java', 'TinkerforgeListener.java'),          tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'liboctaveinvokewrapper-linux-i386.so'),            tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'liboctaveinvokewrapper-linux-amd64.so'),           tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'liboctaveinvokewrapper-linux-arm.so'),             tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'liboctaveinvokewrapper-windows-x86.dll'),          tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'liboctaveinvokewrapper-windows-amd64.dll'),        tmp_source_com_tinkerforge_dir)
            shutil.copy(os.path.join(root_dir, 'liboctaveinvokewrapper-macos-x86_64.dynlib'),      tmp_source_com_tinkerforge_dir)

            if self.get_config_name().space == 'Tinkerforge':
                shutil.copy(os.path.join(root_dir, 'changelog.txt'),                self.tmp_dir)
                shutil.copy(os.path.join(root_dir, 'readme.txt'),                   self.tmp_dir)
                shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'), self.tmp_dir)
            else:
                shutil.copy(os.path.join(self.get_config_dir(), 'changelog.txt'),   self.tmp_dir)

            # Make manifest
            version = self.get_changelog_version()

            with open(os.path.join(tmp_dir, 'manifest.txt'), 'w') as f:
                f.write('Bindings-Version: {1}.{2}.{3}\nBindings-Flavor: {0}\n'.format(flavor.upper(), *version))

            # Make jar
            with common.ChangedDirectory(tmp_dir):
                if flavor == 'octave':
                    classpath = '-classpath {0} '.format(os.path.join(root_dir, 'octave.jar'))
                else:
                    classpath = ''

                common.execute('javac ' +
                               classpath +
                               '-Xlint ' +
                               '-source 1.6 ' +
                               '-target 1.6 ' +
                               os.path.join(tmp_source_com_tinkerforge_dir, '*.java'),
                               shell=True)

            with common.ChangedDirectory(tmp_source_dir):
                common.execute(['jar',
                                'cfm',
                                os.path.join(tmp_dir, self.get_config_name().camel + '.jar'),
                                os.path.join(tmp_dir, 'manifest.txt'),
                                'com',
                                'META-INF'])

            # Remove manifest
            os.remove(os.path.join(tmp_dir, 'manifest.txt'))

            # Remove classes
            for f in os.listdir(tmp_source_com_tinkerforge_dir):
                if f.endswith('.class'):
                    os.remove(os.path.join(tmp_source_com_tinkerforge_dir, f))

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(root_dir):
    common.generate(root_dir, 'en', MATLABZipGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
