#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PHP ZIP Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
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
import subprocess

sys.path.append(os.path.split(os.getcwd())[0])
import common
import php_common
from php_released_files import released_files

class PHPZipGenerator(common.Generator):
    def get_bindings_name(self):
        return 'php'

    def prepare(self):
        common.recreate_directory('/tmp/generator')
        os.makedirs('/tmp/generator/pear/source/Tinkerforge')
        os.makedirs('/tmp/generator/pear/examples')

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        examples = common.find_device_examples(device, '^Example.*\.php$')
        dest = os.path.join('/tmp/generator/pear/examples', device.get_category(), device.get_camel_case_name())

        if not os.path.exists(dest):
            os.makedirs(dest)

        for example in examples:
            shutil.copy(example[1], dest)

    def finish(self):
        root = self.get_bindings_root_directory()

        # Copy examples
        shutil.copy(root.replace('/generators/php', '/doc/en/source/Software/Example.php'),
                    '/tmp/generator/pear/examples/ExampleEnumerate.php')

        # Copy bindings and readme
        package_files = ['<file name="Tinkerforge/IPConnection.php" role="php" />']
        for filename in released_files:
            shutil.copy(os.path.join(root, 'bindings', filename), '/tmp/generator/pear/source/Tinkerforge')
            package_files.append('<file name="Tinkerforge/{0}" role="php" />'.format(os.path.basename(filename)))

        shutil.copy(os.path.join(root, 'IPConnection.php'), '/tmp/generator/pear/source/Tinkerforge')
        shutil.copy(os.path.join(root, 'changelog.txt'), '/tmp/generator/pear')
        shutil.copy(os.path.join(root, 'readme.txt'), '/tmp/generator/pear')

        # Write package.xml
        version = common.get_changelog_version(root)
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        file('/tmp/generator/pear/source/package.xml', 'wb').write("""<?xml version="1.0" encoding="UTF-8"?>
<package packagerversion="1.9.0" version="2.0" xmlns="http://pear.php.net/dtd/package-2.0">
 <name>Tinkerforge</name>
 <uri>http://download.tinkerforge.com/bindings/php/pear/Tinkerforge-{2}.{3}.{4}</uri>
 <summary>PHP API Bindings for Tinkerforge Bricks and Bricklets</summary>
 <description>no description</description>
 <lead>
  <name>Matthias Bolte</name>
  <user>matthias</user>
  <email>matthias@tinkerforge.com</email>
  <active>yes</active>
 </lead>
 <date>{0}</date>
 <version>
  <release>{2}.{3}.{4}</release>
  <api>{2}.{3}.{4}</api>
 </version>
 <stability>
  <release>stable</release>
  <api>stable</api>
 </stability>
 <license>Public Domain</license>
 <notes>no notes</notes>
 <contents>
  <dir name="Tinkerforge">
   {1}
  </dir>
 </contents>
 <dependencies>
  <required>
   <php>
    <min>5.3.0</min>
   </php>
   <pearinstaller>
    <min>1.9.0</min>
   </pearinstaller>
  </required>
 </dependencies>
 <phprelease />
</package>
""".format(date, '\n    '.join(package_files), *version))

        # Make PEAR package
        with common.ChangedDirectory('/tmp/generator/pear/source'):
            args = ['/usr/bin/pear',
                    'package',
                    'package.xml']
            if subprocess.call(args) != 0:
                raise Exception("Command '{0}' failed".format(' '.join(args)))

        # Remove build stuff
        shutil.move('/tmp/generator/pear/source/Tinkerforge-{0}.{1}.{2}.tgz'.format(*version),
                    '/tmp/generator/pear/Tinkerforge.tgz')
        os.remove('/tmp/generator/pear/source/package.xml')

        # Make zip
        common.make_zip(self.get_bindings_name(), '/tmp/generator/pear', root, version)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', PHPZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
