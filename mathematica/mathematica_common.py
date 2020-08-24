#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mathematica Bindings Generator
Copyright (C) 2013-2014, 2018 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>

generate_mathematica_bindings.py: Common library for generation of Mathematica bindings and documentation

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

import copy
import re
import math

from generators import common

class MathematicaGeneratorTrait:
    def get_bindings_name(self):
        return 'mathematica'

    def get_bindings_display_name(self):
        return 'Mathematica'

    def get_doc_null_value_name(self):
        return 'Null'

    def get_doc_formatted_param(self, element):
        return element.get_name().headless
