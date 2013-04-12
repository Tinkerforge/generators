#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java ZIP Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_java_zip.py: Generator for Java ZIP

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
import glob
import re

sys.path.append(os.path.split(os.getcwd())[0])
import common

device = None

def copy_examples_for_zip():
    examples = common.find_examples(device, common.path_binding, 'java', 'Example', '.java')
    dest = os.path.join('/tmp/generator/jar/examples/',
                        device.get_category(),
                        device.get_camel_case_name())

    if not os.path.exists(dest):
        os.makedirs(dest)

    for example in examples:
        shutil.copy(example[1], dest)

def make_files(device_, directory):
    global device
    device = device_

    copy_examples_for_zip()

def generate(path):
    # Make temporary generator directory
    if os.path.exists('/tmp/generator'):
        shutil.rmtree('/tmp/generator/')
    os.makedirs('/tmp/generator/jar/source/com/tinkerforge')
    os.chdir('/tmp/generator')

    # Copy examples
    common.generate(path, 'en', make_files, None, None, False)

    lines = []
    for line in file(common.path_binding.replace('/generators/java', '/doc/en/source/Software/Example.java'), 'rb'):
        lines.append(line.replace('public class Example {', 'public class ExampleEnumerate {'))
    file('/tmp/generator/jar/examples/ExampleEnumerate.java', 'wb').writelines(lines)

    # Copy bindings and readme
    for filename in glob.glob(path + '/bindings/*.java'):
        shutil.copy(filename, '/tmp/generator/jar/source/com/tinkerforge')

    shutil.copy(path + '/Device.java', '/tmp/generator/jar/source/com/tinkerforge')
    shutil.copy(path + '/IPConnection.java', '/tmp/generator/jar/source/com/tinkerforge')
    shutil.copy(path + '/TinkerforgeException.java', '/tmp/generator/jar/source/com/tinkerforge')
    shutil.copy(path + '/TimeoutException.java', '/tmp/generator/jar/source/com/tinkerforge')
    shutil.copy(path + '/AlreadyConnectedException.java', '/tmp/generator/jar/source/com/tinkerforge')
    shutil.copy(path + '/NotConnectedException.java', '/tmp/generator/jar/source/com/tinkerforge')
    shutil.copy(path + '/changelog.txt', '/tmp/generator/jar')
    shutil.copy(path + '/Readme.txt', '/tmp/generator/jar')

    # Make Manifest
    version = common.get_changelog_version(path)
    file('/tmp/generator/manifest.txt', 'wb').write('Bindings-Version: {0}.{1}.{2}\n'.format(*version))

    # Make jar
    args = ['/usr/bin/javac ' +
            '-Xlint ' +
            '/tmp/generator/jar/source/com/tinkerforge/*.java']
    if subprocess.call(args, shell=True) != 0:
        raise Exception("Command '{0}' failed".format(' '.join(args)))

    os.chdir('/tmp/generator/jar/source')
    args = ['/usr/bin/jar ' +
            'cfm ' +
            '/tmp/generator/jar/Tinkerforge.jar ' +
            '/tmp/generator/manifest.txt ' +
            'com']
    if subprocess.call(args, shell=True) != 0:
        raise Exception("Command '{0}' failed".format(' '.join(args)))

    # Remove class
    for f in os.listdir('/tmp/generator/jar/source/com/tinkerforge/'):
        if f.endswith('.class'):
            os.remove('/tmp/generator/jar/source/com/tinkerforge/' + f)

    # Make zip
    common.make_zip('java', '/tmp/generator/jar', path, version)

if __name__ == "__main__":
    generate(os.getcwd())
