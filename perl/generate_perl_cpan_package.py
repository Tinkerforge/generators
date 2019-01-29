#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl CPAN Package Generator
Copyright (C) 2013-2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014, 2018 Matthias Bolte <matthias@tinkerforge.com>

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

def generate(root_dir):
    tmp_dir                     = os.path.join(root_dir, 'cpan_package')
    tmp_unzipped_dir            = os.path.join(tmp_dir, 'unzipped')
    tmp_unzipped_source_dir     = os.path.join(tmp_unzipped_dir, 'source')
    tmp_unzipped_source_lib_dir = os.path.join(tmp_unzipped_source_dir, 'lib')
    tmp_cpan_dir                = os.path.join(tmp_dir, 'cpan')
    tmp_cpan_lib_dir            = os.path.join(tmp_cpan_dir, 'lib')

    # Make directories
    common.recreate_dir(tmp_dir)

    # Unzip
    version = common.get_changelog_version(root_dir)

    common.execute(['unzip',
                    '-q',
                    os.path.join(root_dir, 'tinkerforge_perl_bindings_{0}_{1}_{2}.zip'.format(*version)),
                    '-d',
                    tmp_unzipped_dir])

    # Make CPAN package structure
    modules = ['Tinkerforge']

    for filename in os.listdir(os.path.join(tmp_unzipped_source_lib_dir, 'Tinkerforge')):
        modules.append('Tinkerforge::' + filename.replace('.pm', ''))

    common.execute(['module-starter',
                    '--dir=' + tmp_cpan_dir,
                    '--module=' + ','.join(modules),
                    '--distro=Tinkerforge',
                    '--author="Ishraq Ibne Ashraf"',
                    '--email=ishraq@tinkerforge.com'])

    # Make README
    common.specialize_template(os.path.join(root_dir, 'README.template'),
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
        common.execute(['perl', 'Makefile.PL'])
        common.execute(['make', 'dist'])

    shutil.copy(os.path.join(tmp_cpan_dir, 'Tinkerforge-{0}.{1}.{2}.tar.gz'.format(*version)), root_dir)

if __name__ == "__main__":
    generate(os.getcwd())
