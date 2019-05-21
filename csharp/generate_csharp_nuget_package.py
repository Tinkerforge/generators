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

NETCORE_CSPROJ = '''<?xml version="1.0" encoding="utf-8"?>
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>library</OutputType>
    <TargetFramework>netcoreapp2.0</TargetFramework>
    <GenerateAssemblyTitleAttribute>false</GenerateAssemblyTitleAttribute>
    <GenerateAssemblyConfigurationAttribute>false</GenerateAssemblyConfigurationAttribute>
    <GenerateAssemblyCompanyAttribute>false</GenerateAssemblyCompanyAttribute>
    <GenerateAssemblyProductAttribute>false</GenerateAssemblyProductAttribute>
    <GenerateAssemblyVersionAttribute>false</GenerateAssemblyVersionAttribute>
    <DocumentationFile>bin/Release/netcoreapp2.0/Tinkerforge.xml</DocumentationFile>
  </PropertyGroup>
</Project>
'''

def generate(root_dir):
    tmp_dir                                          = os.path.join(root_dir, 'nuget_package')
    tmp_unzipped_net20_dir                           = os.path.join(tmp_dir, 'unzipped_net20')
    tmp_unzipped_net40_dir                           = os.path.join(tmp_dir, 'unzipped_net40')
    tmp_unzipped_net40_source_tinkerforge_dir        = os.path.join(tmp_unzipped_net40_dir, 'source', 'Tinkerforge')
    tmp_unzipped_netcoreapp20_dir                    = os.path.join(tmp_dir, 'unzipped_netcoreapp20')
    tmp_unzipped_netcoreapp20_source_tinkerforge_dir = os.path.join(tmp_unzipped_netcoreapp20_dir, 'source', 'Tinkerforge')

    # Make directories
    common.recreate_dir(tmp_dir)

    # Unzip
    version = common.get_changelog_version(root_dir)

    common.execute(['unzip',
                    '-q',
                    os.path.join(root_dir, 'tinkerforge_csharp_bindings_{0}_{1}_{2}.zip'.format(*version)),
                    '-d',
                    tmp_unzipped_net20_dir])

    shutil.copytree(tmp_unzipped_net20_dir, tmp_unzipped_net40_dir)
    shutil.copytree(tmp_unzipped_net20_dir, tmp_unzipped_netcoreapp20_dir)

    # Make DLL for NET 4.0
    with common.ChangedDirectory(tmp_unzipped_net40_dir):
        common.execute(['mcs',
                        '/debug:full',
                        '/optimize+',
                        '/warn:4',
                        '/sdk:4',
                        '/target:library',
                        '/doc:' + os.path.join(tmp_unzipped_net40_dir, 'Tinkerforge.xml'),
                        '/out:' + os.path.join(tmp_unzipped_net40_dir, 'Tinkerforge.dll'),
                        os.path.join(tmp_unzipped_net40_source_tinkerforge_dir, '*.cs')])

    # Make DLL for NET Core 2.0
    with open(os.path.join(tmp_unzipped_netcoreapp20_source_tinkerforge_dir, 'Tinkerforge.csproj'), 'w') as f:
        f.write(NETCORE_CSPROJ)

    with common.ChangedDirectory(tmp_unzipped_netcoreapp20_source_tinkerforge_dir):
        common.execute(['dotnet',
                        'build',
                        '-c',
                        'Release'])

    # Download nuget.exe
    with common.ChangedDirectory(tmp_dir):
        common.execute(['wget', 'https://dist.nuget.org/win-x86-commandline/v5.0.2/nuget.exe'])

    # Make Tinkerforge.nuspec
    common.specialize_template(os.path.join(root_dir, 'Tinkerforge.nuspec.template'),
                               os.path.join(tmp_dir, 'Tinkerforge.nuspec'),
                               {'{{VERSION}}': '.'.join(version)})

    # Make package
    with common.ChangedDirectory(tmp_dir):
        common.execute(['mono',
                        os.path.join(tmp_dir, 'nuget.exe'),
                        'pack',
                        os.path.join(tmp_dir, 'Tinkerforge.nuspec')])

    shutil.move(os.path.join(tmp_dir, 'Tinkerforge.{0}.{1}.{2}.nupkg'.format(*version)),
                os.path.join(root_dir, 'tinkerforge.{0}.{1}.{2}.nupkg'.format(*version)))

if __name__ == '__main__':
    generate(os.getcwd())
