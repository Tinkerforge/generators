#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java Maven Package Generator
Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>

generate_java_maven_package.py: Generator for Java Maven Package

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
    tmp_dir               = os.path.join(bindings_root_directory, 'maven_package')
    tmp_src_main_java_dir = os.path.join(tmp_dir, 'src', 'main', 'java')
    tmp_unzipped_dir      = os.path.join(tmp_dir, 'unzipped')

    # Make directories
    common.recreate_directory(tmp_dir)
    os.makedirs(tmp_src_main_java_dir)

    # Unzip
    version = common.get_changelog_version(bindings_root_directory)

    common.execute(['/usr/bin/unzip',
                    '-q',
                    os.path.join(bindings_root_directory, 'tinkerforge_java_bindings_{0}_{1}_{2}.zip'.format(*version)),
                    '-d',
                    tmp_unzipped_dir])

    # Copy source
    shutil.copytree(os.path.join(tmp_unzipped_dir, 'source', 'com'),
                    os.path.join(tmp_src_main_java_dir, 'com'))

    # Make pom.xml
    common.specialize_template(os.path.join(bindings_root_directory, 'pom.xml.template'),
                               os.path.join(tmp_dir, 'pom.xml'),
                               {'{{VERSION}}': '.'.join(version)})

    # Make package
    with common.ChangedDirectory(tmp_dir):
        common.execute(['/usr/bin/mvn', 'clean', 'verify'])

if __name__ == "__main__":
    generate(os.getcwd())
