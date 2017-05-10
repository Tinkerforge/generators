#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java Generator
Copyright (C) 2012-2015, 2017 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2013 Olaf Lüke <olaf@tinkerforge.com>

java_common.py: Common Library for generation of Java bindings and documentation

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

sys.path.append(os.path.split(os.getcwd())[0])
import common

# this is a list of all the Bricks and Bricklets support by Java bindings
# version 2.1.12 released on 2017-04-21. this list is fixed and must never be
# changed. all devices in this list use the legacy type mapping. all devices
# added after Java bindings version 2.1.12 will use the new type mapping that
# maps all integer types smaller than int32 to int.
LEGACY_TYPE_DEVICES = {
'BrickDC',
'BrickIMU',
'BrickIMUV2',
'BrickMaster',
'BrickRED',
'BrickServo',
'BrickStepper',
'BrickSilentStepper',
'BrickletAccelerometer',
'BrickletAmbientLight',
'BrickletAmbientLightV2',
'BrickletAnalogIn',
'BrickletAnalogInV2',
'BrickletAnalogOut',
'BrickletAnalogOutV2',
'BrickletBarometer',
'BrickletCAN',
'BrickletCO2',
'BrickletColor',
'BrickletCurrent12',
'BrickletCurrent25',
'BrickletDistanceIR',
'BrickletDistanceUS',
'BrickletDualButton',
'BrickletDualRelay',
'BrickletDustDetector',
'BrickletGPS',
'BrickletHallEffect',
'BrickletHumidity',
'BrickletIndustrialAnalogOut',
'BrickletIndustrialDigitalIn4',
'BrickletIndustrialDigitalOut4',
'BrickletIndustrialDual020mA',
'BrickletIndustrialDualAnalogIn',
'BrickletIndustrialQuadRelay',
'BrickletIO16',
'BrickletIO4',
'BrickletJoystick',
'BrickletLaserRangeFinder',
'BrickletLCD16x2',
'BrickletLCD20x4',
'BrickletLEDStrip',
'BrickletLine',
'BrickletLinearPoti',
'BrickletLoadCell',
'BrickletMoisture',
'BrickletMotionDetector',
'BrickletMultiTouch',
'BrickletNFCRFID',
'BrickletOLED128x64',
'BrickletOLED64x48',
'BrickletPiezoBuzzer',
'BrickletPiezoSpeaker',
'BrickletPTC',
'BrickletRealTimeClock',
'BrickletRemoteSwitch',
'BrickletRGBLED',
'BrickletRotaryEncoder',
'BrickletRotaryPoti',
'BrickletRS232',
'BrickletSegmentDisplay4x7',
'BrickletSolidStateRelay',
'BrickletSoundIntensity',
'BrickletTemperature',
'BrickletTemperatureIR',
'BrickletThermocouple',
'BrickletTilt',
'BrickletUVLight',
'BrickletVoltage',
'BrickletVoltageCurrent'
}

class JavaDevice(common.Device):
    def get_java_class_name(self):
        return self.get_camel_case_category() + self.get_camel_case_name()

    def has_java_legacy_types(self):
        return self.get_java_class_name() in LEGACY_TYPE_DEVICES

class JavaPacket(common.Packet):
    def get_java_object_name(self):
        name = self.get_camel_case_name()
        if name.startswith('Get'):
            name = name[3:]

        return name

    def get_java_return_type(self, for_doc=False):
        elements = self.get_elements('out')

        if len(elements) == 0:
            return 'void'

        if len(elements) > 1:
            if for_doc:
                return self.get_device().get_java_class_name() + '.' + self.get_java_object_name()
            else:
                return self.get_java_object_name()

        return_type = elements[0].get_java_type()
        if hasattr(self.get_generator(), 'is_octave') and \
           self.get_generator().is_octave() and return_type == 'char':
            return_type = 'String'

        if elements[0].get_cardinality() > 1 and elements[0].get_type() != 'string':
            return_type += '[]'

        return return_type

    def get_java_parameter_list(self, just_types=False):
        param = []

        for element in self.get_elements():
            if element.get_direction() == 'out' and self.get_type() == 'function':
                continue
            java_type = element.get_java_type()
            if hasattr(self.get_generator(), 'is_octave') and \
               self.get_generator().is_octave() and java_type == 'char':
                java_type = 'String'
            name = element.get_headless_camel_case_name()
            arr = ''
            if element.get_cardinality() > 1 and element.get_type() != 'string':
                arr = '[]'

            if just_types:
                param.append('{0}{1}'.format(java_type, arr))
            else:
                param.append('{0}{1} {2}'.format(java_type, arr, name))

        return ', '.join(param)

java_legacy_type = {
    'int8':   'byte',
    'uint8':  'short',
    'int16':  'short',
    'uint16': 'int',
    'int32':  'int',
    'uint32': 'long',
    'int64':  'long',
    'uint64': 'long',
    'float':  'float',
    'bool':   'boolean',
    'char':   'char',
    'string': 'String'
}

java_type = {
    'int8':   'int',
    'uint8':  'int',
    'int16':  'int',
    'uint16': 'int',
    'int32':  'int',
    'uint32': 'long',
    'int64':  'long',
    'uint64': 'long',
    'float':  'float',
    'bool':   'boolean',
    'char':   'char',
    'string': 'String'
}

def get_java_type(type_, legacy):
    if legacy:
        return java_legacy_type[type_]
    else:
        return java_type[type_]

class JavaElement(common.Element):
    java_byte_buffer_method_suffix = {
        'int8':   '',
        'uint8':  '',
        'int16':  'Short',
        'uint16': 'Short',
        'int32':  'Int',
        'uint32': 'Int',
        'int64':  'Long',
        'uint64': 'Long',
        'float':  'Float',
        'bool':   '',
        'char':   '',
        'string': ''
    }

    java_byte_buffer_storage_type = {
        'int8':   'byte',
        'uint8':  'byte',
        'int16':  'short',
        'uint16': 'short',
        'int32':  'int',
        'uint32': 'int',
        'int64':  'long',
        'uint64': 'long',
        'float':  'float',
        'bool':   'byte',
        'char':   'byte',
        'string': 'byte'
    }

    def get_java_type(self):
        return get_java_type(self.get_type(), self.get_device().has_java_legacy_types())

    def get_java_byte_buffer_method_suffix(self):
        return JavaElement.java_byte_buffer_method_suffix[self.get_type()]

    def get_java_byte_buffer_storage_type(self):
        return JavaElement.java_byte_buffer_storage_type[self.get_type()]
