#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PHP Debian Package Generator
Copyright (C) 2020 Matthias Bolte <matthias@tinkerforge.com>

generate_php_debian_package.py: Generator for PHP Debian Package

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

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import shutil
import subprocess
import glob
import importlib.util
import importlib.machinery

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

    if sys.hexversion < 0x3050000:
        generators_module = importlib.machinery.SourceFileLoader('generators', os.path.join(generators_dir, '__init__.py')).load_module()
    else:
        generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
        generators_module = importlib.util.module_from_spec(generators_spec)

        generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common

def generate(root_dir):
    version               = common.get_changelog_version(root_dir)
    debian_dir            = os.path.join(root_dir, 'debian')
    tmp_dir               = os.path.join(root_dir, 'debian_package')
    tmp_source_dir        = os.path.join(tmp_dir, 'source')
    tmp_source_debian_dir = os.path.join(tmp_source_dir, 'debian')
    tmp_build_dir         = os.path.join(tmp_dir, 'tinkerforge-php-bindings-{0}.{1}.{2}'.format(*version))

    # Make directories
    common.recreate_dir(tmp_dir)

    # Unzip
    common.execute(['unzip',
                    '-q',
                    os.path.join(root_dir, 'tinkerforge_php_bindings_{0}_{1}_{2}.zip'.format(*version)),
                    os.path.join('source', '*'),
                    '-d',
                    tmp_dir])

    shutil.copytree(debian_dir, tmp_source_debian_dir)

    common.specialize_template(os.path.join(tmp_source_debian_dir, 'changelog.template'),
                               os.path.join(tmp_source_debian_dir, 'changelog'),
                               {'<<VERSION>>': '.'.join(version),
                                '<<DATE>>': subprocess.check_output(['date', '-R']).decode('utf-8')},
                               remove_template=True)

    # Make package
    os.rename(tmp_source_dir, tmp_build_dir)

    with common.ChangedDirectory(tmp_build_dir):
        common.execute(['dpkg-buildpackage',
                        '--no-sign'])

    # Check package
    with common.ChangedDirectory(tmp_dir):
        common.execute(['lintian', '--pedantic'] + glob.glob('*.deb'))

if __name__ == '__main__':
    generate(os.getcwd())
