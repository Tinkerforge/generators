#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java Maven Package Generator
Copyright (C) 2014, 2018 Matthias Bolte <matthias@tinkerforge.com>

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

if sys.hexversion < 0x3050000:
    print('Python >= 3.5 required')
    sys.exit(1)

import os
import shutil
import subprocess
import importlib.util

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
    generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
    generators_module = importlib.util.module_from_spec(generators_spec)

    generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common
from generators.java import java_common

def generate(root_dir):
    tmp_dir        = os.path.join(root_dir, 'maven_package')
    tmp_source_dir = os.path.join(tmp_dir, 'source')

    # Make directories
    common.recreate_dir(tmp_dir)

    # Unzip
    version = common.get_changelog_version(root_dir)

    common.execute(['unzip',
                    '-q',
                    os.path.join(root_dir, 'tinkerforge_java_bindings_{0}_{1}_{2}.zip'.format(*version)),
                    '-d',
                    tmp_dir])

    # Override pom.xml
    common.specialize_template(os.path.join(root_dir, 'pom.xml.bundle-template'),
                               os.path.join(tmp_source_dir, 'pom.xml'),
                               {'{{VERSION}}': '.'.join(version)})

    # Make package
    with common.ChangedDirectory(tmp_source_dir):
        # FIXME: maven-toolchains-plugin doesn't stop the default JDK from
        #        leaking into the build process. it is still necessary to set
        #        JAVA_HOME to Java 8 in order to stop the default JDK from
        #        being recorded as the Build-Jdk-Spec in the manifest file.
        env = dict(os.environ)
        env['JAVA_HOME'] = java_common.detect_java_home()

        common.execute(['mvn',
                        'clean',
                        'verify'],
                       env=env)

if __name__ == "__main__":
    generate(os.getcwd())
