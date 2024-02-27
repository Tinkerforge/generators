#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
C# NuGet Package Generator
Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>

generate_csharp_nuget_package.py: Generator for C# NuGet Package

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

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import shutil
import importlib.util
import importlib.machinery

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

    if sys.hexversion < 0x3050000:
        generators_module = importlib.machinery.SourceFileLoader('generators', os.path.join(generators_dir, '__init__.py')).load_module()
    else:
        generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
        generators_module = importlib.util.module_from_spec(generators_spec)

        generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common

def generate(root_dir):
    tmp_dir          = os.path.join(root_dir, 'nuget_package')
    tmp_unzipped_dir = os.path.join(tmp_dir, 'unzipped')

    # Make directories
    common.recreate_dir(tmp_dir)

    # Unzip
    version = common.get_changelog_version(root_dir)

    common.execute(['unzip',
                    '-q',
                    os.path.join(root_dir, 'tinkerforge_csharp_bindings_{0}_{1}_{2}.zip'.format(*version)),
                    '-d',
                    tmp_unzipped_dir])

    shutil.copy(os.path.join(root_dir, 'package.png'), tmp_dir)
    shutil.copy(os.path.join(root_dir, 'package.md'), tmp_dir)

    # Make all dlls
    with common.ChangedDirectory(os.path.join(tmp_unzipped_dir, 'source', 'Tinkerforge')):
        common.execute(['dotnet', 'build', '-c', 'Release'])

    # Download nuget.exe
    with common.ChangedDirectory(tmp_dir):
        common.execute(['wget', 'https://dist.nuget.org/win-x86-commandline/v6.9.1/nuget.exe'])

    # Make Tinkerforge.nuspec
    common.specialize_template(os.path.join(root_dir, 'Tinkerforge.nuspec.template'),
                               os.path.join(tmp_dir, 'Tinkerforge.nuspec'),
                               {'{{VERSION}}': '.'.join(version)})

    # Make package
    with common.ChangedDirectory(tmp_dir):
        common.execute(['mono', 'nuget.exe', 'pack', 'Tinkerforge.nuspec'])

    shutil.move(os.path.join(tmp_dir, 'Tinkerforge.{0}.{1}.{2}.nupkg'.format(*version)),
                os.path.join(root_dir, 'tinkerforge.{0}.{1}.{2}.nupkg'.format(*version)))

if __name__ == '__main__':
    common.dockerize('csharp', __file__)

    generate(os.getcwd())
