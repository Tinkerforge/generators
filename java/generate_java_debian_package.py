#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java Debian Package Generator
Copyright (C) 2020 Matthias Bolte <matthias@tinkerforge.com>

generate_java_debian_package.py: Generator for Java Debian Package

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
import glob
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
    debian_dir            = os.path.join(root_dir, 'debian')
    tmp_dir               = os.path.join(root_dir, 'debian_package')
    tmp_source_dir        = os.path.join(tmp_dir, 'source')
    tmp_source_debian_dir = os.path.join(tmp_source_dir, 'debian')

    # Make directories
    common.recreate_dir(tmp_dir)

    # Unzip
    version = common.get_changelog_version(root_dir)

    common.execute(['unzip',
                    '-q',
                    os.path.join(root_dir, 'tinkerforge_java_bindings_{0}_{1}_{2}.zip'.format(*version)),
                    '-d',
                    tmp_dir])

    shutil.copytree(debian_dir, tmp_source_debian_dir)

    common.specialize_template(os.path.join(tmp_source_debian_dir, 'changelog.template'),
                               os.path.join(tmp_source_debian_dir, 'changelog'),
                               {'<<VERSION>>': '.'.join(version),
                                '<<DATE>>': subprocess.check_output(['date', '-R']).decode('utf-8')})

    # Make package
    with common.ChangedDirectory(tmp_source_dir):
        # FIXME: maven-toolchains-plugin doesn't stop the default JDK from
        #        leaking into the build process. it is still necessary to set
        #        JAVA_HOME to Java 8 in order to stop the default JDK from
        #        being recorded as the Build-Jdk-Spec in the manifest file.
        #        maven-javadoc-plugin doesn't respect the toolchain setting
        #        correctly and tries to run javadoc with options detected for
        #        the default JDK. this is fixed by setting JAVA_HOME also.
        env = dict(os.environ)
        env['JAVA_HOME'] = java_common.detect_java_home()

        common.execute(['dpkg-buildpackage',
                        '--no-sign'],
                       env=env)

    # Check package
    with common.ChangedDirectory(tmp_dir):
        common.execute(['lintian'] + glob.glob('*.deb'))

    for suffix in ['', '-doc']:
        shutil.move(os.path.join(tmp_dir, 'libtinkerforge-java{0}_{1}.{2}.{3}_all.deb'.format(suffix, *version)),
                    os.path.join(root_dir, 'libtinkerforge-java{0}_{1}.{2}.{3}_all.deb'.format(suffix, *version)))

if __name__ == '__main__':
    generate(os.getcwd())
