#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mathematica ZIP Generator
Copyright (C) 2012-2015, 2017 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_mathematica_zip.py: Generator for Mathematica ZIP

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
from mathematica_released_files import released_files

class MathematicaZipGenerator(common.ZipGenerator):
    tmp_dir                    = '/tmp/generator/mathematica'
    tmp_source_tinkerforge_dir = os.path.join(tmp_dir, 'source', 'Tinkerforge')
    tmp_examples_dir           = os.path.join(tmp_dir, 'examples')

    def get_bindings_name(self):
        return 'mathematica'

    def prepare(self):
        common.recreate_directory(self.tmp_dir)
        os.makedirs(self.tmp_source_tinkerforge_dir)
        os.makedirs(self.tmp_examples_dir)

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        tmp_examples_device_dir = os.path.join(self.tmp_examples_dir,
                                               device.get_camel_case_category(),
                                               device.get_camel_case_name())

        if not os.path.exists(tmp_examples_device_dir):
            os.makedirs(tmp_examples_device_dir)

        for example in common.find_device_examples(device, r'^Example.*\.nb$'):
            shutil.copy(example[1], tmp_examples_device_dir)

    def finish(self):
        root_dir = self.get_bindings_root_directory()

        # Copy IP Connection examples
        for example in common.find_examples(root_dir, r'^Example.*\.nb$'):
            shutil.copy(example[1], self.tmp_examples_dir)

        # Copy bindings and readme
        for filename in released_files:
            shutil.copy(os.path.join(root_dir, 'bindings', filename), self.tmp_source_tinkerforge_dir)

        shutil.copy(os.path.join(root_dir, '..', 'csharp', 'IPConnection.cs'), self.tmp_source_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'changelog.txt'),                   self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'readme.txt'),                      self.tmp_dir)
        shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'),    self.tmp_dir)

        # Make AssemblyInfo.cs
        version = common.get_changelog_version(root_dir)

        common.specialize_template(os.path.join(root_dir, '..', 'csharp', 'AssemblyInfo.cs.template'),
                                   os.path.join(self.tmp_source_tinkerforge_dir, 'AssemblyInfo.cs'),
                                   {'<<BINDINGS>>': 'Mathematica',
                                    '<<VERSION>>': '.'.join(version)})

        # Make dll
        with common.ChangedDirectory(self.tmp_dir):
            common.execute(['/usr/bin/mcs',
                            '/optimize',
                            '/sdk:2',
                            '/target:library',
                            '/out:' + os.path.join(self.tmp_dir, 'Tinkerforge.dll'),
                            os.path.join(self.tmp_source_tinkerforge_dir, '*.cs')])

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(bindings_root_directory):
    if not os.path.isfile(os.path.join('/usr/lib/mono/2.0/Microsoft.Common.tasks')):
        print('\033[01;31m>>> Could not find Mono SDK 2.0, skipping generation of Mathematica ZIP\033[0m')
        return

    common.generate(bindings_root_directory, 'en', MathematicaZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
