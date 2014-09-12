#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl CPAN Package Generator
Copyright (C) 2013-2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>

generate_perl_cpan_package.py: Generator for Perl CPAN Package

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
from perl_released_files import released_files

def generate(bindings_root_directory):
    tmp_dir                     = os.path.join(bindings_root_directory, 'cpan_package')
    tmp_unzipped_dir            = os.path.join(tmp_dir, 'unzipped')
    tmp_unzipped_source_dir     = os.path.join(tmp_unzipped_dir, 'source')
    tmp_unzipped_source_lib_dir = os.path.join(tmp_unzipped_source_dir, 'lib')
    tmp_cpan_dir                = os.path.join(tmp_dir, 'cpan')
    tmp_cpan_lib_dir            = os.path.join(tmp_cpan_dir, 'lib')

    # Make directories
    common.recreate_directory(tmp_dir)

    # Unzip
    version = common.get_changelog_version(bindings_root_directory)
    args = ['/usr/bin/unzip',
            '-q',
            os.path.join(bindings_root_directory, 'tinkerforge_perl_bindings_{0}_{1}_{2}.zip'.format(*version)),
            '-d',
            tmp_unzipped_dir]

    if subprocess.call(args) != 0:
        raise Exception("Command '{0}' failed".format(' '.join(args)))

    # Make CPAN package structure
    modules = ['Tinkerforge',
               'Tinkerforge::IPConnection',
               'Tinkerforge::Device',
               'Tinkerforge::Error']

    for filename in released_files:
        modules.append('Tinkerforge::' + filename.replace('.pm', ''))

    subprocess.call(("module-starter --dir={0} --module={1} --distro=Tinkerforge " +
                     "--author=\"Ishraq Ibne Ashraf\" --email=ishraq@tinkerforge.com").format(tmp_cpan_dir, ','.join(modules)), shell=True)

    # Make README
    common.specialize_template(os.path.join(bindings_root_directory, 'README.template'),
                               os.path.join(tmp_cpan_dir, 'README'),
                               {'<<VERSION>>': '.'.join(version)})

    # Make Changes
    shutil.copy(os.path.join(tmp_unzipped_dir, 'changelog.txt'), os.path.join(tmp_cpan_dir, 'Changes'))

    # Copy Makefile.PL
    shutil.copy(os.path.join(tmp_unzipped_source_dir, 'Makefile.PL'), tmp_cpan_dir)

    # Copy source
    shutil.rmtree(tmp_cpan_lib_dir)
    shutil.copytree(os.path.join(tmp_unzipped_source_lib_dir),
                    os.path.join(tmp_cpan_lib_dir))

    # Make package
    with common.ChangedDirectory(tmp_cpan_dir):
        args = ['/usr/bin/perl',
                'Makefile.PL']

        if subprocess.call(args) != 0:
            raise Exception("Command '{0}' failed".format(' '.join(args)))

        args = ['make',
                'dist']

        if subprocess.call(args) != 0:
            raise Exception("Command '{0}' failed".format(' '.join(args)))

    shutil.copy(os.path.join(tmp_cpan_dir, 'Tinkerforge-{0}.{1}.{2}.tar.gz'.format(*version)), bindings_root_directory)

if __name__ == "__main__":
    generate(os.getcwd())
