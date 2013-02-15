#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C# ZIP Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_csharp_zip.py: Generator for C# ZIP

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
import glob
import re

sys.path.append(os.path.split(os.getcwd())[0])
import common

device = None

def copy_examples_for_zip():
    examples = common.find_examples(device, common.path_binding, 'csharp', 'Example', '.cs')
    dest = os.path.join('/tmp/generator/dll/examples/',
                        device.get_category(),
                        device.get_camel_case_name())

    if not os.path.exists(dest):
        os.makedirs(dest)

    for example in examples:
        shutil.copy(example[1], dest)

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)

    copy_examples_for_zip()

def generate(path):
    # Make temporary generator directory
    if os.path.exists('/tmp/generator'):
        shutil.rmtree('/tmp/generator/')
    os.makedirs('/tmp/generator/dll/source/Tinkerforge')
    os.chdir('/tmp/generator')

    # Copy examples
    common.generate(path, 'en', make_files, None, False)
    shutil.copy(common.path_binding.replace('/generators/csharp', '/doc/en/source/Software/Example.cs'),
                '/tmp/generator/dll/examples/ExampleEnumerate.cs')

    # Copy bindings and readme
    for filename in glob.glob(path + '/bindings/*.cs'):
        shutil.copy(filename, '/tmp/generator/dll/source/Tinkerforge')

    shutil.copy(path + '/IPConnection.cs', '/tmp/generator/dll/source/Tinkerforge')
    shutil.copy(path + '/changelog.txt', '/tmp/generator/dll')
    shutil.copy(path + '/Readme.txt', '/tmp/generator/dll')

    # Write AssemblyInfo
    version = common.get_changelog_version(path)
    file('/tmp/generator/dll/source/Tinkerforge/AssemblyInfo.cs', 'wb').write("""
using System.Reflection;
using System.Runtime.CompilerServices;

[assembly: AssemblyTitle("C# API Bindings")]
[assembly: AssemblyDescription("C# API Bindings for Tinkerforge Bricks and Bricklets")]
[assembly: AssemblyConfiguration("")]
[assembly: AssemblyCompany("Tinkerforge GmbH")]
[assembly: AssemblyProduct("C# API Bindings")]
[assembly: AssemblyCopyright("Tinkerforge GmbH 2011-2013")]
[assembly: AssemblyTrademark("")]
[assembly: AssemblyCulture("")]
[assembly: AssemblyVersion("{0}.{1}.{2}.0")]
""".format(*version))

    # Make dll
    args = ['/usr/bin/gmcs',
            '/optimize',
            '/target:library',
            '/out:/tmp/generator/dll/Tinkerforge.dll',
            '/doc:/tmp/generator/dll/Tinkerforge.xml',
            '/tmp/generator/dll/source/Tinkerforge/*.cs']
    if subprocess.call(args) != 0:
        raise Exception("Command '{0}' failed".format(' '.join(args)))

    # Make zip
    common.make_zip('csharp', '/tmp/generator/dll', path, version)

if __name__ == "__main__":
    generate(os.getcwd())
