#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LabVIEW ZIP Generator
Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_labview_zip.py: Generator for LabVIEW ZIP

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
import subprocess

sys.path.append(os.path.split(os.getcwd())[0])
import common
from labview_released_files import released_files

class LabVIEWZipGenerator(common.Generator):
    tmp_dir                    = '/tmp/generator/labview'
    tmp_source_tinkerforge_dir = os.path.join(tmp_dir, 'source', 'Tinkerforge')
    tmp_examples_dir           = os.path.join(tmp_dir, 'examples')
    tmp_examples_10_dir        = os.path.join(tmp_examples_dir, '10.0')

    def get_bindings_name(self):
        return 'labview'

    def prepare(self):
        common.recreate_directory(self.tmp_dir)
        os.makedirs(self.tmp_source_tinkerforge_dir)
        os.makedirs(self.tmp_examples_dir)
        os.makedirs(self.tmp_examples_10_dir)

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        tmp_examples_device_dir = os.path.join(self.tmp_examples_dir,
                                               device.get_category(),
                                               device.get_camel_case_name())
        tmp_examples_device_10_dir = os.path.join(self.tmp_examples_dir,
                                                  device.get_category(),
                                                  device.get_camel_case_name(),
                                                  '10.0')

        if not os.path.exists(tmp_examples_device_dir):
            os.makedirs(tmp_examples_device_dir)

        if not os.path.exists(tmp_examples_device_10_dir):
            os.makedirs(tmp_examples_device_10_dir)

        for example in common.find_device_examples(device, '^Example .*\.vi$'):
            shutil.copy(example[1], tmp_examples_device_dir)

            parts = os.path.split(example[1])
            shutil.copy(os.path.join(parts[0], '10.0', parts[1]), tmp_examples_device_10_dir)

    def finish(self):
        root_dir = self.get_bindings_root_directory()

        # Copy IP Connection examples
        for example in common.find_examples(root_dir, '^Example .*\.vi$'):
            shutil.copy(example[1], self.tmp_examples_dir)

            parts = os.path.split(example[1])
            shutil.copy(os.path.join(parts[0], '10.0', parts[1]), self.tmp_examples_10_dir)

        # Copy bindings and readme
        for filename in released_files:
            shutil.copy(os.path.join(root_dir, 'bindings', filename), self.tmp_source_tinkerforge_dir)

        shutil.copy(os.path.join(root_dir, '..', 'csharp', 'IPConnection.cs'), self.tmp_source_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'changelog.txt'),                   self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'readme.txt'),                      self.tmp_dir)

        # Make AssemblyInfo.cs
        version = common.get_changelog_version(root_dir)

        common.specialize_template(os.path.join(root_dir, 'AssemblyInfo.cs.template'),
                                   os.path.join(self.tmp_source_tinkerforge_dir, 'AssemblyInfo.cs'),
                                   {'<<VERSION>>': '.'.join(version)})

        # Make dll
        with common.ChangedDirectory(self.tmp_dir):
            args = ['/usr/bin/gmcs',
                    '/optimize',
                    '/target:library',
                    '/out:' + os.path.join(self.tmp_dir, 'Tinkerforge.dll'),
                    os.path.join(self.tmp_source_tinkerforge_dir, '*.cs')]

            if subprocess.call(args) != 0:
                raise Exception("Command '{0}' failed".format(' '.join(args)))

        # Make zip
        common.make_zip(self.get_bindings_name(), self.tmp_dir, root_dir, version)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', LabVIEWZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
