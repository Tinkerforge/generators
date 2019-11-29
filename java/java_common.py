#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java Generator
Copyright (C) 2012-2015, 2017, 2019 Matthias Bolte <matthias@tinkerforge.com>
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
        return self.get_category().camel + self.get_name().camel

    def has_java_legacy_types(self):
        return self.get_java_class_name() in LEGACY_TYPE_DEVICES

class JavaPacket(common.Packet):
    def get_java_object_name(self, high_level=False):
        skip = 0

        if high_level and self.has_high_level():
            skip = -2

        name = self.get_name(skip=skip)

        if name.space.startswith('Get '):
            return name.camel[3:]

        return name.camel

    def get_java_return_type(self, for_doc=False, high_level=False):
        elements = self.get_elements(direction='out', high_level=high_level)

        if len(elements) == 0:
            return 'void'
        elif len(elements) > 1:
            if for_doc:
                return self.get_device().get_java_class_name() + '.' + self.get_java_object_name(high_level)
            else:
                return self.get_java_object_name(high_level)
        else:
            return elements[0].get_java_type()

    def get_java_parameters(self, context='signature', high_level=False):
        parameters = []

        for element in self.get_elements(high_level=high_level):
            if element.get_direction() == 'out' and self.get_type() == 'function':
                continue

            java_type = element.get_java_type()
            name = element.get_name().headless

            if context == 'signature':
                parameters.append('{0} {1}'.format(java_type, name))
            elif context == 'call':
                parameters.append(name)
            elif context == 'listener':
                if high_level and element.get_level() == 'high' and element.get_role() == 'stream_data':
                    name = '({0})highLevelCallback.data'.format(java_type)

                parameters.append(name)
            elif context == 'link':
                parameters.append(java_type)
            else:
                raise common.GeneratorError('Invalid context: ' + context)

        return ', '.join(parameters)

java_legacy_types = {
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

java_types = {
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

def get_java_type(type_, cardinality, legacy=False, octave=False):
    if legacy:
        java_type = java_legacy_types[type_]
    else:
        java_type = java_types[type_]

    if java_type == 'char' and octave:
        java_type = 'String'

    if cardinality != 1 and type_ != 'string':
        java_type += '[]'

    return java_type

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

    java_default_item_values = {
        'int8':   '0',
        'uint8':  '0',
        'int16':  '0',
        'uint16': '0',
        'int32':  '0',
        'uint32': '0',
        'int64':  '0',
        'uint64': '0',
        'float':  '0.0',
        'bool':   'false',
        'char':   "'\\0'",
        'string': None
    }

    def format_value(self, value):
        if isinstance(value, list):
            result = []

            for subvalue in value:
                result.append(self.format_value(subvalue))

            return '{{{0}}}'.format(', '.join(result))

        type_ = self.get_type()

        if type_ == 'float':
            return common.format_float(value) + 'f'

        if type_ == 'bool':
            return str(bool(value)).lower()

        if type_ == 'char':
            return "'{0}'".format(value.replace("'", "\\'"))

        if type_ == 'string':
            return '"{0}"'.format(value.replace('"', '\\"'))

        return str(value)

    def get_java_type(self):
        return get_java_type(self.get_type(), self.get_cardinality(),
                             legacy=self.get_device().has_java_legacy_types(),
                             octave=self.get_generator().is_octave())

    def get_java_byte_buffer_method_suffix(self):
        return JavaElement.java_byte_buffer_method_suffix[self.get_type()]

    def get_java_byte_buffer_storage_type(self):
        storage_type = JavaElement.java_byte_buffer_storage_type[self.get_type()]

        if self.get_cardinality() != 1 and storage_type != 'string':
            storage_type += '[]'

        return storage_type

    def get_java_new(self, cardinality=None):
        java_type = get_java_type(self.get_type(), 1,
                                  legacy=self.get_device().has_java_legacy_types(),
                                  octave=self.get_generator().is_octave())

        if cardinality == None:
            return 'new {0}[{1}]'.format(java_type, self.get_cardinality())
        else:
            return 'new {0}[{1}]'.format(java_type, cardinality)

    def get_java_default_item_value(self):
        if self.get_generator().is_octave() and self.get_type() == 'char':
            value = '""'
        else:
            value = JavaElement.java_default_item_values[self.get_type()]

        if value == None:
            common.GeneratorError('Invalid array item type: ' + self.get_type())

        return value

    def get_java_default_value(self):
        if self.get_cardinality() != 1:
            return 'null'
        else:
            return self.get_java_default_item_value()

class JavaGeneratorTrait:
    def get_doc_null_value_name(self):
        return 'null'

    def get_doc_formatted_param(self, element):
        return element.get_name().headless
