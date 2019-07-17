#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OpenHAB ZIP Generator
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>

generate_openhab_zip.py: Generator for OpenHAB ZIP

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

class OpenHABZipGenerator(common.ZipGenerator):
    def __init__(self, *args):
        common.ZipGenerator.__init__(self, *args)

        self.tmp_dir                          = self.get_tmp_dir()

        self.tmp_bindings_dir = os.path.join(self.tmp_dir, 'src', 'main', 'java', 'com', 'tinkerforge')
        self.tmp_xml_dir = os.path.join(self.tmp_dir, 'src', 'main', 'resources', 'ESH-INF', 'thing')

        self.file_dests = {
            'about.html': '.',
            'NOTICE': '.',
            'pom.xml': '.',
            'README.md': '.',

            'feature.xml': './src/main/feature',
            'dependencies.xml': './src/main/history',
            'binding.xml': './src/main/resources/ESH-INF/binding',
            'tinkerforge_xx_XX.properties': './src/main/resources/ESH-INF/i18n',
            #'BrickDaemon.xml': './src/main/resources/ESH-INF/thing',

            'BrickDaemonDiscoveryService.java': './src/main/java/org/eclipse/smarthome/binding/tinkerforge/discovery',
            'TinkerforgeHandlerFactory.java': './src/main/java/org/eclipse/smarthome/binding/tinkerforge/internal',
            'TinkerforgeChannelTypeProvider.java': './src/main/java/org/eclipse/smarthome/binding/tinkerforge/internal',
            'TinkerforgeConfigDescriptionProvider.java': './src/main/java/org/eclipse/smarthome/binding/tinkerforge/internal',
            'TinkerforgeThingTypeProvider.java': './src/main/java/org/eclipse/smarthome/binding/tinkerforge/internal',

            'BrickDaemonHandler.java': './src/main/java/org/eclipse/smarthome/binding/tinkerforge/internal/handler',
            'DeviceHandler.java': './src/main/java/org/eclipse/smarthome/binding/tinkerforge/internal/handler',

            'BrickDaemon.java':               './src/main/java/com/tinkerforge',
            'BrickDaemonConfig.java':         './src/main/java/com/tinkerforge',
            'Device.java':                    './src/main/java/com/tinkerforge',
            'DeviceBase.java':                './src/main/java/com/tinkerforge',
            'DeviceInfo.java':                './src/main/java/com/tinkerforge',
            'DeviceListener.java':            './src/main/java/com/tinkerforge',
            'DeviceProvider.java':            './src/main/java/com/tinkerforge',
            'IPConnection.java':              './src/main/java/com/tinkerforge',
            'IPConnectionBase.java':          './src/main/java/com/tinkerforge',
            'TinkerforgeException.java':      './src/main/java/com/tinkerforge',
            'TimeoutException.java':          './src/main/java/com/tinkerforge',
            'AlreadyConnectedException.java': './src/main/java/com/tinkerforge',
            'NotConnectedException.java':     './src/main/java/com/tinkerforge',
            'CryptoException.java':           './src/main/java/com/tinkerforge',
            'NetworkException.java':          './src/main/java/com/tinkerforge',
            'StreamOutOfSyncException.java':  './src/main/java/com/tinkerforge',
            'InvalidParameterException.java': './src/main/java/com/tinkerforge',
            'NotSupportedException.java':     './src/main/java/com/tinkerforge',
            'UnknownErrorCodeException.java': './src/main/java/com/tinkerforge',
            'TinkerforgeListener.java':       './src/main/java/com/tinkerforge',
            'changelog.txt':                  '.',
            'readme.txt':                     '.',

            os.path.join(self.get_bindings_dir(), 'DeviceFactory.java'): './src/main/java/com/tinkerforge',
            os.path.join(self.get_bindings_dir(), 'TinkerforgeBindingConstants.java'): './src/main/java/org/eclipse/smarthome/binding/tinkerforge/internal'
        }
        self.file_dests = {os.path.join(self.get_bindings_dir(), '..', k): os.path.join(self.tmp_dir, *v.split('/')) for k, v in self.file_dests.items()}

        self.tmp_source_dir                   = os.path.join(self.tmp_dir, 'source')
        self.tmp_source_meta_inf_services_dir = os.path.join(self.tmp_source_dir, 'META-INF', 'services')
        self.tmp_source_com_tinkerforge_dir   = os.path.join(self.tmp_source_dir, 'com', 'tinkerforge')
        self.tmp_examples_dir                 = os.path.join(self.tmp_dir, 'examples')

    def get_bindings_name(self):
        return 'openhab'

    def prepare(self):
        common.recreate_dir(self.tmp_dir)
        for directory in self.file_dests.values():
            os.makedirs(directory, exist_ok=True)

    def generate(self, device):
        if not device.is_released():
            return

        if not 'openhab' in device.raw_data:
            return

        shutil.copy(os.path.join(self.get_bindings_dir(), device.get_category().camel+device.get_name().camel + '.java'), self.tmp_bindings_dir)
        shutil.copy(os.path.join(self.get_bindings_dir(), device.get_category().camel+device.get_name().camel + 'Config.java'), self.tmp_bindings_dir)
        #shutil.copy(os.path.join(self.get_bindings_dir(), device.get_category().camel+device.get_name().camel + '.xml'), self.tmp_xml_dir)

        # Copy device examples
        #tmp_examples_device_dir = os.path.join(self.tmp_examples_dir,
        #                                       device.get_category().camel,
        #                                       device.get_name().camel)

        #if not os.path.exists(tmp_examples_device_dir):
        #    os.makedirs(tmp_examples_device_dir)

        #for example in common.find_device_examples(device, r'^Example.*\.java$'):
        #    shutil.copy(example[1], tmp_examples_device_dir)

    def finish(self):
        root_dir = self.get_root_dir()

        if self.get_config_name().space == 'Tinkerforge':
            for src, dst in self.file_dests.items():
                shutil.copy(src, dst)
        else:
            shutil.copy(os.path.join(self.get_config_dir(), 'changelog.txt'), self.tmp_dir)
            shutil.copy(os.path.join(root_dir, 'custom.txt'), os.path.join(self.tmp_dir, 'readme.txt'))

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(root_dir):
    common.generate(root_dir, 'en', OpenHABZipGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
