#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MATLAB/Octave Generator
Copyright (C) 2012-2015, 2019 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2013 Olaf Lüke <olaf@tinkerforge.com>

matlab_common.py: Common Library for generation of MATLAB bindings and documentation

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

# this is a list of all the Bricks and Bricklets support by MATLAB bindings
# version 2.1.12 released on 2017-04-21. this list is fixed and must never be
# changed. all devices in this list use the legacy type mapping. all devices
# added after MATLAB bindings version 2.1.12 will use the new type mapping that
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

class MATLABDevice(common.Device):
    def get_matlab_class_name(self):
        return self.get_category().camel + self.get_name().camel

    def has_matlab_legacy_types(self):
        return self.get_matlab_class_name() in LEGACY_TYPE_DEVICES

class MATLABPacket(common.Packet):
    def get_matlab_object_name(self, high_level=False):
        name = self.get_name(skip=-2 if high_level and self.has_high_level() else 0).camel

        if name.startswith('Get'):
            name = name[3:]

        return name

    def get_matlab_return_type(self, for_doc=False, high_level=False):
        elements = self.get_elements(direction='out', high_level=high_level)

        if len(elements) == 0:
            return 'void'

        if len(elements) > 1:
            if for_doc:
                return self.get_device().get_matlab_class_name() + '.' + self.get_matlab_object_name(high_level=high_level)
            else:
                return self.get_matlab_object_name()

        return elements[0].get_matlab_type()

    def get_matlab_parameter_list(self, just_types=False, high_level=False):
        param = []

        for element in self.get_elements(high_level=high_level):
            if element.get_direction() == 'out' and self.get_type() == 'function':
                continue

            matlab_type = element.get_matlab_type()
            name = element.get_name().headless

            if just_types:
                param.append(matlab_type)
            else:
                param.append('{0} {1}'.format(matlab_type, name))

        return ', '.join(param)

matlab_legacy_types = {
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

matlab_types = {
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

def get_matlab_type(type_, cardinality, legacy=False, octave=False):
    if legacy:
        matlab_type = matlab_legacy_types[type_]
    else:
        matlab_type = matlab_types[type_]

    if cardinality != 1 and type_ != 'string':
        matlab_type += '[]'

    return matlab_type

class MATLABElement(common.Element):
    matlab_byte_buffer_method_suffix = {
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

    matlab_byte_buffer_storage_type = {
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

    def format_value(self, value):
        type_ = self.get_type()

        if type_ == 'float':
            return common.format_float(value)

        if type_ == 'bool':
            return str(bool(value)).lower()

        if type_ in ['char', 'string']:
            return "'{0}'".format(value.replace("'", "\\'"))

        return str(value)

    def get_matlab_type(self):
        return get_matlab_type(self.get_type(), self.get_cardinality(),
                               legacy=self.get_device().has_matlab_legacy_types())

    def get_matlab_byte_buffer_method_suffix(self):
        return MATLABElement.matlab_byte_buffer_method_suffix[self.get_type()]

    def get_matlab_byte_buffer_storage_type(self):
        return MATLABElement.matlab_byte_buffer_storage_type[self.get_type()]


class MATLABGeneratorTrait:
    def get_doc_null_value_name(self):
        return 'null'

    def get_doc_formatted_param(self, element):
        return element.get_name().headless
