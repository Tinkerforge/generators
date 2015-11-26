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
    tmp_dir                                = os.path.join(bindings_root_directory, 'nuget_package')
    tmp_unzipped_20_dir                    = os.path.join(tmp_dir, 'unzipped_20')
    tmp_unzipped_40_dir                    = os.path.join(tmp_dir, 'unzipped_40')
    tmp_unzipped_40_source_tinkerforge_dir = os.path.join(tmp_unzipped_40_dir, 'source', 'Tinkerforge')

    # Make directories
    common.recreate_directory(tmp_dir)

    # Unzip
    version = common.get_changelog_version(bindings_root_directory)

    common.execute(['/usr/bin/unzip',
                    '-q',
                    os.path.join(bindings_root_directory, 'tinkerforge_csharp_bindings_{0}_{1}_{2}.zip'.format(*version)),
                    '-d',
                    tmp_unzipped_20_dir])

    shutil.copytree(tmp_unzipped_20_dir, tmp_unzipped_40_dir)

    # Make Tinkerforge.csproj for NET 4.0
    common.specialize_template(os.path.join(tmp_unzipped_40_source_tinkerforge_dir, 'Tinkerforge.csproj'),
                               os.path.join(tmp_unzipped_40_source_tinkerforge_dir, 'Tinkerforge.csproj'),
                               {'ToolsVersion="2.0"': 'ToolsVersion="4.0"'})

    # Make dll for NET 4.0
    with common.ChangedDirectory(tmp_unzipped_40_source_tinkerforge_dir):
        common.execute(['xbuild',
                        '/p:Configuration=Release',
                        os.path.join(tmp_unzipped_40_source_tinkerforge_dir, 'Tinkerforge.csproj')])

    # Download nuget.exe
    with common.ChangedDirectory(tmp_dir):
        common.execute(['wget', 'http://www.nuget.org/nuget.exe'])

    # Make Tinkerforge.nuspec
    common.specialize_template(os.path.join(bindings_root_directory, 'Tinkerforge.nuspec.template'),
                               os.path.join(tmp_dir, 'Tinkerforge.nuspec'),
                               {'{{VERSION}}': '.'.join(version)})

    # Make package
    with common.ChangedDirectory(tmp_dir):
        common.execute(['mono',
                        os.path.join(tmp_dir, 'nuget.exe'),
                        'pack',
                        os.path.join(tmp_dir, 'Tinkerforge.nuspec')])

    shutil.move(os.path.join(tmp_dir, 'Tinkerforge.{0}.{1}.{2}.nupkg'.format(*version)),
                os.path.join(bindings_root_directory, 'tinkerforge.{0}.{1}.{2}.nupkg'.format(*version)))

if __name__ == "__main__":
    generate(os.getcwd())
