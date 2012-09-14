#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PHP ZIP Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_php_zip.py: Generator for PHP ZIP

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
import glob
import re
import php_common

sys.path.append(os.path.split(os.getcwd())[0])
import common

device = None

def copy_examples_for_zip():
    examples = common.find_examples(device, common.path_binding, 'php', 'Example', '.php')
    dest = os.path.join('/tmp/generator/pear/examples/',
                        device.get_category().lower(),
                        device.get_underscore_name())

    if not os.path.exists(dest):
        os.makedirs(dest)

    for example in examples:
        shutil.copy(example[1], dest)

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)

    copy_examples_for_zip()

def generate(path):
    common.path_binding = path
    path_list = path.split('/')
    path_list[-1] = 'configs'
    path_config = '/'.join(path_list)
    sys.path.append(path_config)
    configs = os.listdir(path_config)

    # Make temporary generator directory
    if os.path.exists('/tmp/generator'):
        shutil.rmtree('/tmp/generator/')
    os.makedirs('/tmp/generator/pear/source/Tinkerforge')
    os.chdir('/tmp/generator')

    # Make bindings
    for config in configs:
        if config.endswith('_config.py'):
            module = __import__(config[:-3])
            print(" * {0}".format(config[:-10]))
            make_files(module.com, path)

    # Copy bindings and readme
    package_files = ['<file name="Tinkerforge/IPConnection.php" role="php" />']
    for filename in glob.glob(path + '/bindings/*.php'):
        shutil.copy(filename, '/tmp/generator/pear/source/Tinkerforge')
        package_files.append('<file name="Tinkerforge/{0}" role="php" />'.format(os.path.basename(filename)))

    shutil.copy(path + '/IPConnection.php', '/tmp/generator/pear/source/Tinkerforge')
    shutil.copy(path + '/changelog.txt', '/tmp/generator/pear')
    shutil.copy(path + '/readme.txt', '/tmp/generator/pear')

    # Write package.xml
    version = common.get_changelog_version(path)
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
    os.chdir('/tmp/generator/pear/source')
    args = ['/usr/bin/pear',
            'package',
            'package.xml']
    subprocess.call(args)

    # Remove build stuff
    shutil.move('/tmp/generator/pear/source/Tinkerforge-{0}.{1}.{2}.tgz'.format(*version),
                '/tmp/generator/pear/Tinkerforge.tgz')
    os.remove('/tmp/generator/pear/source/package.xml')

    # Make zip
    common.make_zip('php', '/tmp/generator/pear', path, version)

if __name__ == "__main__":
    generate(os.getcwd())
