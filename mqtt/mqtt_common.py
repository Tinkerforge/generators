#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MQTT Generator
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>
Copyright (C) 2019-2020 Matthias Bolte <matthias@tinkerforge.com>

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
import json

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
        'char':   'char',
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

    def format_value(self, value):
        return json.dumps(value, separators=(',', ':'))

    def get_mqtt_type(self, for_doc=False, cardinality=None):
        mqtt_type = MQTTElement.mqtt_types[self.get_type()]

        if cardinality == None:
            cardinality = self.get_cardinality()

        if cardinality == 1 or self.get_type() == 'string':
            return mqtt_type

        if for_doc:
            return '[{0}, ...]'.format(mqtt_type)

        return (mqtt_type, self.get_cardinality())

    def get_mqtt_struct_format(self):
        f = MQTTElement.mqtt_struct_formats[self.get_type()]
        cardinality = self.get_cardinality()

        if cardinality > 1:
            f = str(cardinality) + f

        return f

    def get_symbols(self):
        symbols = []

        # FIXME: currently common.py enforces that there is at most one contant group per element and not one per index
        constant_group = self.get_constant_group(index=self.get_indices()[0])

        if constant_group != None:
            symbols = ["{}: {}".format(repr(c.get_value()), repr(c.get_name().under)) for c in constant_group.get_constants()]

        return '{' + ', '.join(symbols) + '}'

class MQTTGeneratorTrait:
    def get_bindings_name(self):
        return 'mqtt'

    def get_bindings_display_name(self):
        return 'MQTT'

    def get_doc_null_value_name(self):
        return 'null'

    def get_doc_formatted_param(self, element):
        return element.get_name().under
