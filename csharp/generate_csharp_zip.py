#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C# ZIP Generator
Copyright (C) 2012-2015 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_csharp_zip.py: Generator for C# ZIP

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
from csharp_released_files import released_files

class CSharpZipGenerator(common.ZipGenerator):
    tmp_dir                    = '/tmp/generator/csharp'
    tmp_source_tinkerforge_dir = os.path.join(tmp_dir, 'source', 'Tinkerforge')
    tmp_examples_dir           = os.path.join(tmp_dir, 'examples')

    def get_bindings_name(self):
        return 'csharp'

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

        for example in common.find_device_examples(device, '^Example.*\.cs$'):
            shutil.copy(example[1], tmp_examples_device_dir)

    def finish(self):
        root_dir = self.get_bindings_root_directory()

        # Copy IP Connection examples
        for example in common.find_examples(root_dir, '^Example.*\.cs$'):
            shutil.copy(example[1], self.tmp_examples_dir)

        # Copy bindings and readme
        for filename in released_files:
            shutil.copy(os.path.join(root_dir, 'bindings', filename), self.tmp_source_tinkerforge_dir)

        shutil.copy(os.path.join(root_dir, 'IPConnection.cs'),              self.tmp_source_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'project.json'),                 self.tmp_source_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'project.lock.json'),            self.tmp_source_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'TinkerforgeUWP.rd.xml'),        self.tmp_source_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'changelog.txt'),                self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'readme.txt'),                   self.tmp_dir)
        shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'), self.tmp_dir)

        # Make AssemblyInfo.cs
        version = common.get_changelog_version(root_dir)

        common.specialize_template(os.path.join(root_dir, 'AssemblyInfo.cs.template'),
                                   os.path.join(self.tmp_source_tinkerforge_dir, 'AssemblyInfo.cs'),
                                   {'<<BINDINGS>>': 'C#',
                                    '<<VERSION>>': '.'.join(version)})

        # Make Tinkerforge(UWP).csproj
        project_items = []

        for filename in ['AssemblyInfo.cs', 'IPConnection.cs'] + released_files:
            project_items.append('<Compile Include="{0}" />'.format(filename))

        common.specialize_template(os.path.join(root_dir, 'Tinkerforge.csproj.template'),
                                   os.path.join(self.tmp_source_tinkerforge_dir, 'Tinkerforge.csproj'),
                                   {'{{TOOLS_VERSION}}': '2.0',
                                    '{{ITEMS}}': '\n    '.join(project_items)})

        common.specialize_template(os.path.join(root_dir, 'TinkerforgeUWP.csproj.template'),
                                   os.path.join(self.tmp_source_tinkerforge_dir, 'TinkerforgeUWP.csproj'),
                                   {'{{ITEMS}}': '\n    '.join(project_items)})

        # Make dll
        with common.ChangedDirectory(self.tmp_source_tinkerforge_dir):
            common.execute(['xbuild',
                            '/p:Configuration=Release',
                            os.path.join(self.tmp_source_tinkerforge_dir, 'Tinkerforge.csproj')])

        release_dir = os.path.join(self.tmp_source_tinkerforge_dir, 'bin', 'Release')

        shutil.copy(os.path.join(release_dir, 'Tinkerforge.dll'),     self.tmp_dir)
        shutil.copy(os.path.join(release_dir, 'Tinkerforge.dll.mdb'), self.tmp_dir)
        shutil.copy(os.path.join(release_dir, 'Tinkerforge.xml'),     self.tmp_dir)

        shutil.rmtree(os.path.join(self.tmp_source_tinkerforge_dir, 'bin'))
        shutil.rmtree(os.path.join(self.tmp_source_tinkerforge_dir, 'obj'))

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', CSharpZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
