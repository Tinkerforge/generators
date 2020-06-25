#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ruby Debian Package Generator
Copyright (C) 2020 Matthias Bolte <matthias@tinkerforge.com>

generate_ruby_debian_package.py: Generator for Ruby Debian Package

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

def generate(root_dir):
    version                 = common.get_changelog_version(root_dir)
    debian_dir              = os.path.join(root_dir, 'debian')
    tmp_dir                 = os.path.join(root_dir, 'debian_package')
    tmp_bindings_dir        = os.path.join(tmp_dir, 'tinkerforge-ruby-bindings-{0}.{1}.{2}'.format(*version))
    tmp_bindings_debian_dir = os.path.join(tmp_bindings_dir, 'debian')

    # Make directories
    common.recreate_dir(tmp_dir)

    # Unzip
    common.execute(['unzip',
                    '-q',
                    os.path.join(root_dir, 'tinkerforge_ruby_bindings_{0}_{1}_{2}.zip'.format(*version)),
                    '-d',
                    tmp_dir])

    common.execute(['gem2tgz',
                    os.path.join(tmp_dir, 'tinkerforge.gem')])

    common.execute(['tar',
                    '-xf',
                    os.path.join(tmp_dir, 'tinkerforge.tar.gz'.format(*version)),
                    '-C',
                    tmp_dir])

    shutil.move(os.path.join(tmp_dir, 'tinkerforge'), tmp_bindings_dir)

    shutil.copytree(debian_dir, tmp_bindings_debian_dir)

    common.specialize_template(os.path.join(tmp_bindings_debian_dir, 'changelog.template'),
                               os.path.join(tmp_bindings_debian_dir, 'changelog'),
                               {'<<VERSION>>': '.'.join(version),
                                '<<DATE>>': subprocess.check_output(['date', '-R']).decode('utf-8')})

    # Make package
    with common.ChangedDirectory(tmp_bindings_dir):
        common.execute(['dpkg-buildpackage',
                        '--no-sign'])

    # Check package
    with common.ChangedDirectory(tmp_dir):
        common.execute(['lintian'] + glob.glob('*.deb'))

    shutil.move(os.path.join(tmp_dir, 'ruby-tinkerforge_{0}.{1}.{2}_all.deb'.format(*version)),
                os.path.join(root_dir, 'ruby-tinkerforge_{0}.{1}.{2}_all.deb'.format(*version)))

if __name__ == '__main__':
    generate(os.getcwd())