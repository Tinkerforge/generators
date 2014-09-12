#!/usr/bin/env python
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
import os
import shutil
import subprocess

sys.path.append(os.path.split(os.getcwd())[0])
import common

def generate(bindings_root_directory):
    tmp_dir          = os.path.join(bindings_root_directory, 'nuget_package')
    tmp_unzipped_dir = os.path.join(tmp_dir, 'unzipped')

    # Make directories
    common.recreate_directory(tmp_dir)

    # Unzip
    version = common.get_changelog_version(bindings_root_directory)
    args = ['/usr/bin/unzip',
            '-q',
            os.path.join(bindings_root_directory, 'tinkerforge_csharp_bindings_{0}_{1}_{2}.zip'.format(*version)),
            '-d',
            tmp_unzipped_dir]

    if subprocess.call(args) != 0:
        raise Exception("Command '{0}' failed".format(' '.join(args)))

    # Download nuget.exe
    with common.ChangedDirectory(tmp_dir):
        args = ['wget',
                'http://www.nuget.org/nuget.exe']

        if subprocess.call(args) != 0:
            raise Exception("Command '{0}' failed".format(' '.join(args)))

    # Make Tinkerforge.nuspec
    common.specialize_template(os.path.join(bindings_root_directory, 'Tinkerforge.nuspec.template'),
                               os.path.join(tmp_dir, 'Tinkerforge.nuspec'),
                               {'{{VERSION}}': '.'.join(version)})

    # Make package
    with common.ChangedDirectory(tmp_dir):
        args = ['mono',
                os.path.join(tmp_dir, 'nuget.exe'),
                'pack',
                os.path.join(tmp_dir, 'Tinkerforge.nuspec')]

        if subprocess.call(args) != 0:
            raise Exception("Command '{0}' failed".format(' '.join(args)))

    shutil.move(os.path.join(tmp_dir, 'Tinkerforge.{0}.{1}.{2}.nupkg'.format(*version)),
                os.path.join(bindings_root_directory, 'tinkerforge.{0}.{1}.{2}.nupkg'.format(*version)))

if __name__ == "__main__":
    generate(os.getcwd())
