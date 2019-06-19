#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MQTT Generator
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>

mqtt_common.py: Common Library for generation of MQTT bindings and documentation

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


class MQTTDevice(common.Device):
    def get_mqtt_device_name(self):
        if self.is_tng():
            return self.get_category().under + '_' + self.get_name().under

        return self.get_name().under + '_' + self.get_category().under

    def get_python_class_name(self):
        if self.is_tng():
            return self.get_category().camel + self.get_name().camel

        return self.get_name().camel + self.get_category().camel

class MQTTPacket(common.Packet):
    def get_mqtt_name(self, skip=0):
        return self.get_name(skip).under

    def get_python_name(self, skip=0):
        return self.get_name(skip).under

class MQTTElement(common.Element):
    mqtt_types = {
        'int8':   'int',
        'uint8':  'int',
        'int16':  'int',
        'uint16': 'int',
        'int32':  'int',
        'uint32': 'int',
        'int64':  'int',
        'uint64': 'int',
        'float':  'float',
        'bool':   'bool',
        'char':   'string',
        'string': 'string'
    }

    mqtt_struct_formats = {
        'int8':   'b',
        'uint8':  'B',
        'int16':  'h',
        'uint16': 'H',
        'int32':  'i',
        'uint32': 'I',
        'int64':  'q',
        'uint64': 'Q',
        'float':  'f',
        'bool':   '!',
        'char':   'c',
        'string': 's'
    }

    def get_mqtt_type(self, for_doc=False):
        t = MQTTElement.mqtt_types[self.get_type()]

        if self.get_type() == 'char' and not for_doc:
            return 'char'

        if self.get_cardinality() == 1 or t == 'string':
            return t

        if for_doc and self.get_cardinality() < 0:
            return '[{0},...]'.format(t)
        elif for_doc and self.get_cardinality() > 4:
            return '[{0},... (x{1})]'.format(t, self.get_cardinality())
        elif for_doc:
            return '[{0}]'.format(",".join([t] * self.get_cardinality()))
        else:
            return (t, self.get_cardinality())

    def get_mqtt_struct_format(self):
        f = MQTTElement.mqtt_struct_formats[self.get_type()]
        cardinality = self.get_cardinality()

        if cardinality > 1:
            f = str(cardinality) + f

        return f

    def get_symbols(self):
        symbols = {}
        constant_group = self.get_constant_group()

        if constant_group != None:
            for constant in constant_group.get_constants():
                symbols[constant.get_value()] = constant.get_name().under

        return symbols
