#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Visual Basic .NET Bindings Generator
Copyright (C) 2013, 2018 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>

generate_vbnet_bindings.py: Common library for generation of Visual Basic .NET bindings and documentation

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

class VBNETGeneratorTrait:
    def get_bindings_name(self):
        return 'vbnet'

    def get_bindings_display_name(self):
        return 'Visual Basic .NET'

    def get_doc_null_value_name(self):
        return 'Nothing'

    def get_doc_formatted_param(self, element):
        return element.get_name().headless

    def generates_high_level_callbacks(self):
        return True
