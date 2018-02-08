#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PHP ZIP Generator
Copyright (C) 2012-2015, 2018 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_php_zip.py: Generator for PHP ZIP

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

import datetime
import sys
import os
import shutil

sys.path.append(os.path.split(os.getcwd())[0])
import common

class PHPZipGenerator(common.ZipGenerator):
    tmp_dir                    = '/tmp/generator/php'
    tmp_source_dir             = os.path.join(tmp_dir, 'source')
    tmp_source_tinkerforge_dir = os.path.join(tmp_source_dir, 'Tinkerforge')
    tmp_examples_dir           = os.path.join(tmp_dir, 'examples')

    def get_bindings_name(self):
        return 'php'

    def prepare(self):
        common.recreate_dir(self.tmp_dir)
        os.makedirs(self.tmp_source_dir)
        os.makedirs(self.tmp_source_tinkerforge_dir)
        os.makedirs(self.tmp_examples_dir)

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        tmp_examples_device_dir = os.path.join(self.tmp_examples_dir,
                                               device.get_category().camel,
                                               device.get_name().camel)

        if not os.path.exists(tmp_examples_device_dir):
            os.makedirs(tmp_examples_device_dir)

        for example in common.find_device_examples(device, r'^Example.*\.php$'):
            shutil.copy(example[1], tmp_examples_device_dir)

    def finish(self):
        root_dir = self.get_root_dir()

        # Copy IP Connection examples
        for example in common.find_examples(root_dir, r'^Example.*\.php$'):
            shutil.copy(example[1], self.tmp_examples_dir)

        # Copy bindings and readme
        package_files = ['<file name="Tinkerforge/IPConnection.php" role="php" />']

        for filename in self.get_released_files():
            shutil.copy(os.path.join(self.get_bindings_dir(), filename), self.tmp_source_tinkerforge_dir)
            package_files.append('<file name="Tinkerforge/{0}" role="php" />'.format(os.path.basename(filename)))

        shutil.copy(os.path.join(root_dir, 'IPConnection.php'),             self.tmp_source_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'changelog.txt'),                self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'readme.txt'),                   self.tmp_dir)
        shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'), self.tmp_dir)

        # Make package.xml
        version = common.get_changelog_version(root_dir)
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        common.specialize_template(os.path.join(root_dir, 'package.xml.template'),
                                   os.path.join(self.tmp_source_dir, 'package.xml'),
                                   {'{{VERSION}}': '.'.join(version),
                                    '{{DATE}}': date,
                                    '{{FILES}}': '\n    '.join(package_files)})

        # Make PEAR package
        with common.ChangedDirectory(self.tmp_source_dir):
            common.execute(['/usr/bin/pear', 'package', 'package.xml'])

        # Remove build stuff
        shutil.move(os.path.join(self.tmp_source_dir, 'Tinkerforge-{0}.{1}.{2}.tgz'.format(*version)),
                    os.path.join(self.tmp_dir, 'Tinkerforge.tgz'))
        os.remove(os.path.join(self.tmp_source_dir, 'package.xml'))

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(root_dir):
    common.generate(root_dir, 'en', PHPZipGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
