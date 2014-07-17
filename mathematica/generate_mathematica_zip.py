#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mathematica ZIP Generator
Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>
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
import subprocess

sys.path.append(os.path.split(os.getcwd())[0])
import common
from mathematica_released_files import released_files

class MathematicaZipGenerator(common.Generator):
    def get_bindings_name(self):
        return 'mathematica'

    def prepare(self):
        common.recreate_directory('/tmp/generator')
        os.makedirs('/tmp/generator/dll/source/Tinkerforge')
        os.makedirs('/tmp/generator/dll/examples')

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        examples = common.find_device_examples(device, '^Example.*\.nb$')
        dest = os.path.join('/tmp/generator/dll/examples', device.get_category(), device.get_camel_case_name())

        if not os.path.exists(dest):
            os.makedirs(dest)

        for example in examples:
            shutil.copy(example[1], dest)

    def finish(self):
        root = self.get_bindings_root_directory()

        # Copy IPConnection examples
        examples = common.find_examples(root, '^Example.*\.nb$')
        for example in examples:
            shutil.copy(example[1], '/tmp/generator/dll/examples')

        # Copy bindings and readme
        for filename in released_files:
            shutil.copy(os.path.join(root, 'bindings', filename), '/tmp/generator/dll/source/Tinkerforge')

        shutil.copy(os.path.join(root, '..', 'csharp', 'IPConnection.cs'), '/tmp/generator/dll/source/Tinkerforge')
        shutil.copy(os.path.join(root, 'changelog.txt'), '/tmp/generator/dll')
        shutil.copy(os.path.join(root, 'readme.txt'), '/tmp/generator/dll')

        # Write AssemblyInfo
        version = common.get_changelog_version(root)
        file('/tmp/generator/dll/source/Tinkerforge/AssemblyInfo.cs', 'wb').write("""
using System.Reflection;
using System.Runtime.CompilerServices;

[assembly: AssemblyTitle("Mathematica API Bindings")]
[assembly: AssemblyDescription("Mathematica API Bindings for Tinkerforge Bricks and Bricklets")]
[assembly: AssemblyConfiguration("")]
[assembly: AssemblyCompany("Tinkerforge GmbH")]
[assembly: AssemblyProduct("Mathematica API Bindings")]
[assembly: AssemblyCopyright("Tinkerforge GmbH 2011-2014")]
[assembly: AssemblyTrademark("")]
[assembly: AssemblyCulture("")]
[assembly: AssemblyVersion("{0}.{1}.{2}.0")]
""".format(*version))

        # Make dll
        with common.ChangedDirectory('/tmp/generator'):
            args = ['/usr/bin/gmcs',
                    '/optimize',
                    '/target:library',
                    '/out:/tmp/generator/dll/Tinkerforge.dll',
                    '/tmp/generator/dll/source/Tinkerforge/*.cs']
            if subprocess.call(args) != 0:
                raise Exception("Command '{0}' failed".format(' '.join(args)))

        # Make zip
        common.make_zip(self.get_bindings_name(), '/tmp/generator/dll', root, version)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', MathematicaZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
