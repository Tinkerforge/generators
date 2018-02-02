#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JSON ZIP Generator
Copyright (C) 2017-2018 Matthias Bolte <matthias@tinkerforge.com>

generate_json_zip.py: Generator for JSON ZIP

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
from json_released_files import released_files

class JSONZipGenerator(common.ZipGenerator):
    tmp_dir        = '/tmp/generator/json'
    tmp_source_dir = os.path.join(tmp_dir, 'source')

    def get_bindings_name(self):
        return 'json'

    def prepare(self):
        common.recreate_dir(self.tmp_dir)
        os.makedirs(self.tmp_source_dir)

    def generate(self, device):
        pass

    def finish(self):
        root_dir = self.get_root_dir()

        # Copy bindings and readme
        for filename in released_files:
            shutil.copy(os.path.join(self.get_bindings_dir(), filename), self.tmp_source_dir)

        shutil.copy(os.path.join(root_dir, 'readme.txt'),                   self.tmp_dir)
        shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'), self.tmp_dir)

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(root_dir):
    common.generate(root_dir, 'en', JSONZipGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
