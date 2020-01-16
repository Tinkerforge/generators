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

        #TODO: use os.path.join
        self.file_dests = {
            'about.html':   '.',
            'NOTICE':       '.',
            'pom.xml':      '.',
            'README.md':    '.',
            'changelog.txt':'.',
            'readme.txt':   '.',

            'feature.xml':                  './src/main/feature',
            'dependencies.xml':             './src/main/history',
            'binding.xml':                  './src/main/resources/ESH-INF/binding',
            'tinkerforge_xx_XX.properties': './src/main/resources/ESH-INF/i18n',

            'BrickDaemonDiscoveryService.java': './src/main/java/org/eclipse/smarthome/binding/tinkerforge/discovery',
            'OutdoorWeatherDiscoveryService.java': './src/main/java/org/eclipse/smarthome/binding/tinkerforge/discovery',
            'TinkerforgeDiscoveryService.java': './src/main/java/org/eclipse/smarthome/binding/tinkerforge/discovery',

            'TinkerforgeHandlerFactory.java':               './src/main/java/org/eclipse/smarthome/binding/tinkerforge/internal',
            'TinkerforgeChannelTypeProvider.java':          './src/main/java/org/eclipse/smarthome/binding/tinkerforge/internal',
            'TinkerforgeConfigDescriptionProvider.java':    './src/main/java/org/eclipse/smarthome/binding/tinkerforge/internal',
            'TinkerforgeThingTypeProvider.java':            './src/main/java/org/eclipse/smarthome/binding/tinkerforge/internal',

            'BrickDaemonHandler.java':                      './src/main/java/org/eclipse/smarthome/binding/tinkerforge/internal/handler',
            'BrickletOutdoorWeatherHandler.java':           './src/main/java/org/eclipse/smarthome/binding/tinkerforge/internal/handler',
            'BrickletOutdoorWeatherSensorHandler.java':    './src/main/java/org/eclipse/smarthome/binding/tinkerforge/internal/handler',
            'BrickletOutdoorWeatherStationHandler.java':    './src/main/java/org/eclipse/smarthome/binding/tinkerforge/internal/handler',
            'DeviceHandler.java':                           './src/main/java/org/eclipse/smarthome/binding/tinkerforge/internal/handler',

            # Reuse from java generator
            '../java/AlreadyConnectedException.java': './src/main/java/com/tinkerforge',
            '../java/CryptoException.java':           './src/main/java/com/tinkerforge',
            '../java/DeviceBase.java':                './src/main/java/com/tinkerforge',
            '../java/DeviceListener.java':            './src/main/java/com/tinkerforge',
            '../java/DeviceProvider.java':            './src/main/java/com/tinkerforge',
            '../java/InvalidParameterException.java': './src/main/java/com/tinkerforge',
            '../java/NetworkException.java':          './src/main/java/com/tinkerforge',
            '../java/NotConnectedException.java':     './src/main/java/com/tinkerforge',
            '../java/NotSupportedException.java':     './src/main/java/com/tinkerforge',
            '../java/StreamOutOfSyncException.java':  './src/main/java/com/tinkerforge',
            '../java/TimeoutException.java':          './src/main/java/com/tinkerforge',
            '../java/TinkerforgeException.java':      './src/main/java/com/tinkerforge',
            '../java/UnknownErrorCodeException.java': './src/main/java/com/tinkerforge',

            'BrickDaemon.java':               './src/main/java/com/tinkerforge',
            'BrickDaemonConfig.java':         './src/main/java/com/tinkerforge',
            'DefaultActions.java':             './src/main/java/com/tinkerforge',
            'Device.java':                    './src/main/java/com/tinkerforge',
            'DeviceInfo.java':                './src/main/java/com/tinkerforge',
            'Helper.java':                    './src/main/java/com/tinkerforge',
            'IPConnection.java':              './src/main/java/com/tinkerforge',
            'IPConnectionBase.java':          './src/main/java/com/tinkerforge',
            'TinkerforgeListener.java':       './src/main/java/com/tinkerforge',

            'BrickletOutdoorWeather.java':       './src/main/java/com/tinkerforge',
            'BrickletOutdoorWeatherSensor.java':'./src/main/java/com/tinkerforge',
            'BrickletOutdoorWeatherSensorConfig.java':'./src/main/java/com/tinkerforge',
            'BrickletOutdoorWeatherStation.java':'./src/main/java/com/tinkerforge',
            'BrickletOutdoorWeatherStationConfig.java':'./src/main/java/com/tinkerforge',


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

    def get_doc_null_value_name(self):
        return 'null'

    def get_doc_formatted_param(self, element):
        return element.get_name().camel

    def prepare(self):
        common.recreate_dir(self.tmp_dir)

        for directory in self.file_dests.values():
            if not os.path.exists(directory):
                os.makedirs(directory)

    def generate(self, device):
        if not device.is_released():
            return

        device_file = os.path.join(self.get_bindings_dir(), device.get_category().camel+device.get_name().camel + '.java')
        if os.path.exists(device_file):
            shutil.copy(device_file, self.tmp_bindings_dir)

        for file in os.listdir(self.get_bindings_dir()):
            if device.get_category().camel+device.get_name().camel in file and (file.endswith('Config.java') or file.endswith('Actions.java')):
                shutil.copy(os.path.join(self.get_bindings_dir(), file), self.tmp_bindings_dir)

    def finish(self):
        root_dir = self.get_root_dir()

        if self.get_config_name().space == 'Tinkerforge':
            for src, dst in self.file_dests.items():
                shutil.copy(src, dst)
        else:
            shutil.copy(os.path.join(self.get_config_dir(), 'changelog.txt'), self.tmp_dir)
            shutil.copy(os.path.join(root_dir, 'custom.txt'), os.path.join(self.tmp_dir, 'readme.txt'))

        self.create_zip_file(self.tmp_dir)

def generate(root_dir):
    common.generate(root_dir, 'en', OpenHABZipGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
