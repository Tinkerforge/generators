#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tinkerforge Visual Programming Language (TVPL) Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>

tvpl_common.py: Common Library for generation of TVPL bindings and documentation

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

class TVPLDevice(common.Device):
    def get_tvpl_block_name(self):
        return '_'.join([self.get_underscore_category(), self.get_underscore_name()])

class TVPLElement(common.Element):
    tvpl_types = {
        'int8':   'Number',
        'uint8':  'Number',
        'int16':  'Number',
        'uint16': 'Number',
        'int32':  'Number',
        'uint32': 'Number',
        'int64':  'Number',
        'uint64': 'Number',
        'float':  'Number',
        'bool':   'Boolean',
        'char':   'String',
        'string': 'String'
    }

    def get_tvpl_type(self):
        return self.tvpl_types[self.get_type()]
