#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C# ZIP Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
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
import glob

sys.path.append(os.path.split(os.getcwd())[0])
import common
from csharp_released_files import released_files

class CSharpZipGenerator(common.Generator):
    def get_bindings_name(self):
        return 'csharp'

    def prepare(self):
        common.recreate_directory('/tmp/generator')
        os.makedirs('/tmp/generator/dll/source/Tinkerforge')
        os.makedirs('/tmp/generator/dll/examples')

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        examples = common.find_device_examples(device, '^Example.*\.cs$')
        dest = os.path.join('/tmp/generator/dll/examples', device.get_category(), device.get_camel_case_name())

        if not os.path.exists(dest):
            os.makedirs(dest)

        for example in examples:
            shutil.copy(example[1], dest)

    def finish(self):
        root = self.get_bindings_root_directory()
        tmp_src = '/tmp/generator/dll/source/Tinkerforge'

        # create AssemblyInfo
        version = common.get_changelog_version(root)
        print 'Generate AssemblyInfo.cs [{0}] ...'.format(os.path.join(tmp_src, 'AssemblyInfo.cs'))
        assembly_info = generate_assembly_info('Tinkerforge C# API Bindings',
                                               'C# API Bindings for Tinkerforge Bricks and Bricklets',
                                               'Tinkerforge GmbH',
                                               'C# API Bindings',
                                               'Tinkerforge GmbH 2011-2014',
                                               version)
        #print assembly_info # for debug
        file(os.path.join(tmp_src, 'AssemblyInfo.cs'), 'wb').write(assembly_info)

        # Copy special files, which are not generated binding files
        shutil.copy(os.path.join(root, 'IPConnection.cs'), tmp_src)

        # Copy IPConnection examples
        print 'Copy IPConnection examples'
        examples = common.find_examples(root, '^Example.*\.cs$')
        for example in examples:
            shutil.copy(example[1], '/tmp/generator/dll/examples')

        # Copy released files from bindings
        print 'Copy Bindings to output directory [{0}] ...'.format(tmp_src)
        for filename in released_files:
            print '\t => copy file: {0}'.format(os.path.join(root, 'bindings', filename)) # for debug
            shutil.copy(os.path.join(root, 'bindings', filename), tmp_src)

        # create project file
        print 'Generate project file [{0}] ...'.format(os.path.join(tmp_src, 'Tinkerforge.csproj'))
        project_file = generate_project_file(glob.glob(os.path.join(tmp_src, "*.cs")))
        file(os.path.join(tmp_src, 'Tinkerforge.csproj'), 'wb').write(project_file)

        # Copy info content (readme and changlog)
        shutil.copy(os.path.join(root, 'changelog.txt'), '/tmp/generator/dll')
        shutil.copy(os.path.join(root, 'readme.txt'), '/tmp/generator/dll')

        # Make (Release) dll
        print 'Generate Tinkerforge.dll (as Release version)...'
        with common.ChangedDirectory(tmp_src):
             args = ['xbuild',
                     os.path.join(tmp_src, 'Tinkerforge.csproj'),
                     '/p:Configuration=Release'] # generate explicit release version!

             if subprocess.call(args) != 0:
               raise Exception("Command '{0}' failed".format(' '.join(args)))

        # copy release build content (.dll/.mdb/.xml) to dll folder for zip creation
        print 'copy zip file content [{0}]'.format(os.path.join(tmp_src, 'bin/Release', 'Tinkerforge.dll'))
        shutil.copy(os.path.join(tmp_src, 'bin/Release', 'Tinkerforge.dll'), '/tmp/generator/dll')
        print 'copy zip file content [{0}]'.format(os.path.join(tmp_src, 'bin/Release', 'Tinkerforge.dll.mdb'))
        shutil.copy(os.path.join(tmp_src, 'bin/Release', 'Tinkerforge.dll.mdb'), '/tmp/generator/dll')
        print 'copy zip file content [{0}]'.format(os.path.join(tmp_src, 'bin/Release', 'Tinkerforge.xml'))
        shutil.copy(os.path.join(tmp_src, 'bin/Release', 'Tinkerforge.xml'), '/tmp/generator/dll')

        # clean up project content for zip
        args = ['xbuild','/nologo','/t:Clean','/verbosity:quiet','/p:Configuration=Release',
                os.path.join(tmp_src, 'Tinkerforge.csproj')]

        #print 'cleanup project stuff...'
        #if subprocess.call(args) != 0:
        #  print 'Warning: project content could not be cleaned.'

        # Make zip
        print 'Generate Zip file ...'
        common.make_zip(self.get_bindings_name(), '/tmp/generator/dll', root, version)

        # generate nuget package
        print 'Prepare package manager (NuGet):'
        tmp_package = '/tmp/generator/nuget'

        prepare_package_manager('Tinkerforge.csproj',
                                tmp_package,
                                'Tinkerforge',
                                version,
                                'Tinkerforge C# API Bindings',
                                'Tinkerforge GmbH',
                                'Tinkerforge GmbH',
                                'C# API Bindings for Tinkerforge Bricks and Bricklets',
                                'Tinkerforge GmbH 2011-2014')

        print 'Generate nuget package ...'
        generate_nuget_package(root,
                               os.path.join(tmp_src, 'Tinkerforge.csproj'),
                               os.path.join(tmp_package,'Tinkerforge.csproj.nuspec'),
                               tmp_package)
        print 'Success.'

def generate_assembly_info(title, description, company, product, copyright, version):
    result  = 'using System.Reflection;\n'
    result += 'using System.Runtime.CompilerServices;\n'
    result += '\n'
    result += '[assembly: AssemblyTitle("{0}")]\n'.format(title)
    result += '[assembly: AssemblyDescription("{0}")]\n'.format(description)
    result += '[assembly: AssemblyConfiguration("")]\n'
    result += '[assembly: AssemblyCompany("{0}")]\n'.format(company)
    result += '[assembly: AssemblyProduct("{0}")]\n'.format(product)
    result += '[assembly: AssemblyCopyright("{0}")]\n'.format(copyright)
    result += '[assembly: AssemblyTrademark("")]\n'
    result += '[assembly: AssemblyVersion("{0}.{1}.{2}.0")]\n'.format(*version)
    result += '[assembly: AssemblyFileVersion("{0}.{1}.{2}.0")]\n'.format(*version)

    return result

def generate_project_file(files):
    result = """<?xml version="1.0" encoding="utf-8"?>
<Project DefaultTargets="Build" ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <PropertyGroup>
    <Configuration Condition=" '$(Configuration)' == '' ">Debug</Configuration>
    <Platform Condition=" '$(Platform)' == '' ">AnyCPU</Platform>
    <ProjectGuid>{69C9A0E2-529F-420A-88F2-ED8E0818BDEC}</ProjectGuid>
    <OutputType>Library</OutputType>
    <RootNamespace>Tinkerforge</RootNamespace>
    <AssemblyName>Tinkerforge</AssemblyName>
  </PropertyGroup>
  <PropertyGroup Condition=" '$(Configuration)|$(Platform)' == 'Debug|AnyCPU' ">
    <DebugSymbols>true</DebugSymbols>
    <DebugType>full</DebugType>
    <Optimize>false</Optimize>
    <OutputPath>bin\Debug</OutputPath>
    <DefineConstants>DEBUG;</DefineConstants>
    <ErrorReport>prompt</ErrorReport>
    <WarningLevel>4</WarningLevel>
    <ConsolePause>false</ConsolePause>
    <DocumentationFile>bin\Debug\Tinkerforge.xml</DocumentationFile>
  </PropertyGroup>
  <PropertyGroup Condition=" '$(Configuration)|$(Platform)' == 'Release|AnyCPU' ">
    <DebugType>full</DebugType>
    <Optimize>true</Optimize>
    <OutputPath>bin\Release</OutputPath>
    <ErrorReport>prompt</ErrorReport>
    <WarningLevel>4</WarningLevel>
    <ConsolePause>false</ConsolePause>
    <DocumentationFile>bin\Release\Tinkerforge.xml</DocumentationFile>
  </PropertyGroup>
  <ItemGroup>
    <Reference Include="System" />
  </ItemGroup>\n"""

    # generate compile include node
    if len(files) > 0:
        result += '  <ItemGroup>\n'
        # concat cs file includes
        for file in files:
            print '\t => include file [{0}] to project.'.format(file)
            result += '    <Compile Include="' + os.path.basename(file) + '" />\n'
        result += '  </ItemGroup>\n'

    result += """  <Import Project="$(MSBuildBinPath)\Microsoft.CSharp.targets" />
</Project>"""

    return result

def prepare_package_manager(project_file_name,
                            tmp_packaged_dir,
                            package_id,
                            package_version,
                            package_title,
                            package_author,
                            package_owners,
                            package_description,
                            package_copyright):
    common.recreate_directory(tmp_packaged_dir)

    print 'Get package manager ...'
    if not os.path.exists(os.path.join(tmp_packaged_dir, 'nuget.exe')):
        with common.ChangedDirectory(tmp_packaged_dir):
            args = ['wget', 'http://nuget.org/nuget.exe']
            if subprocess.call(args) != 0:
                print 'Error: package manager could not be downloaded!'
                raise Exception("Command '{0}' failed".format(' '.join(args)))

    # generate package spec
    print '\t => generate package spec file [{0}] ...'.format(os.path.join(tmp_packaged_dir, '{0}.nuspec'. format(os.path.basename(project_file_name))))
    nuspec_file = generate_nuget_spec_file(package_id, package_version, package_title,
                                           package_author, package_owners, package_description,
                                           package_copyright, 'Tinkerforge.dll', 'Tinkerforge.xml')
    file(os.path.join(tmp_packaged_dir, '{0}.nuspec'.format(os.path.basename(project_file_name))), 'wb').write(nuspec_file)
    #shutil.copy(os.path.join(project_file_name,'Tinkerforge.nuspec'), tmp_packaged_dir)
    pass

def generate_nuget_spec_file(id, version, title, author, owners, description, copyright, assembly_name, assembly_xml_name):
    result  = '<?xml version="1.0"?>\n'
    result += '<package xmlns="http://schemas.microsoft.com/packaging/2011/08/nuspec.xsd">\n'
    result += '   <metadata>\n'
    result += '       <id>{0}</id>\n'.format(id)
    result += '       <version>{0}.{1}.{2}.0</version>\n'.format(*version)
    result += '       <title>{0}</title>\n'.format(title)
    result += '       <authors>{0}</authors>\n'.format(author)
    result += '       <owners>{0}</owners>\n'.format(owners)
    result += '       <requireLicenseAcceptance>false</requireLicenseAcceptance>\n'
    result += '       <description>{0}</description>\n'.format(description)
    result += '       <copyright>{0}</copyright>\n'.format(copyright)
    result += '       <dependencies />\n'
    result += '   </metadata>\n'
    result += '   <files>\n'
    result += '       <file src="bin/Release/{0}" target="lib/Net40"/>\n'.format(assembly_name) # on mono, no wildcats support!
    #result += '      <file src="bin/Release/{0}.mdb" target="lib/net40"/>\n'.format(os.path.basename(assembly_name)) # with mono, in case of windows 'pdb'
    result += '       <file src="bin/Release/{0}" target="lib/Net40"/>\n'.format(assembly_xml_name)
    result += '   </files>\n'
    result += '</package>'

    return result

def generate_nuget_package(output_folder, project_file_path, package_spec_file_path, build_path):
    print '\t => package output_folder: {0}'.format(output_folder)
    print '\t => project_file_path: {0}'.format(project_file_path)
    print '\t => package_spec_file_path: {0}'.format(package_spec_file_path)
    print '\t => use nuspec file [{0}]'.format(package_spec_file_path)
    print '\t => Copy spec file to [{0}]'.format(os.path.join(os.path.dirname(project_file_path), os.path.basename(package_spec_file_path)))

    nuspec_path = os.path.join(os.path.dirname(project_file_path),os.path.basename(package_spec_file_path))
    print 'Copy nuspec file to project source folder'.format(nuspec_path)
    shutil.copy(package_spec_file_path, nuspec_path)

    args = ['mono',
            os.path.join(build_path, 'nuget.exe'),
            'pack',
            nuspec_path,
            '-OutputDirectory',
            output_folder]

    with common.ChangedDirectory(os.path.dirname(project_file_path)):
        if subprocess.call(args) != 0:
            raise Exception("Command '{0}' failed".format(' '.join(args)))

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', CSharpZipGenerator)

if __name__ == "__main__":
    print 'Copy examples:'
    generate(os.getcwd())
