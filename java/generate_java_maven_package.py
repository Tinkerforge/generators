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

def generate(root):
    version = common.get_changelog_version(root)
    maven_dir = os.path.join(root, 'maven-tmp')
    java_dir = os.path.join(maven_dir, 'src', 'main', 'java')
    unzipped_dir = os.path.join(maven_dir, 'unzipped')

    common.recreate_directory(maven_dir)
    os.makedirs(java_dir)

    shutil.copy('tinkerforge_java_bindings_{0}_{1}_{2}.zip'.format(*version), maven_dir)

    args = ['/usr/bin/unzip',
            '-q',
            'tinkerforge_java_bindings_{0}_{1}_{2}.zip'.format(*version),
            '-d',
            unzipped_dir]
    if subprocess.call(args) != 0:
        raise Exception("Command '{0}' failed".format(' '.join(args)))

    shutil.copytree(os.path.join(unzipped_dir, 'source', 'com'), os.path.join(java_dir, 'com'))

    common.replace_in_file('pom.xml.template',
                           os.path.join(maven_dir, 'pom.xml'),
                           '{{VERSION}}', '.'.join(version))

    with common.ChangedDirectory(maven_dir):
        args = ['/usr/bin/mvn',
                'clean',
                'verify']
        if subprocess.call(args) != 0:
            raise Exception("Command '{0}' failed".format(' '.join(args)))

if __name__ == "__main__":
    generate(os.getcwd())
