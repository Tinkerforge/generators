#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MATLAB ZIP Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>

generate_matlab_zip.py: Generator for MATLAB ZIP

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
from matlab_released_files import released_files

class MATLABZipGenerator(common.Generator):
    def get_bindings_name(self):
        return 'matlab'

    def prepare(self):
        common.recreate_directory('/tmp/generator')
        os.makedirs('/tmp/generator/jar/source/com/tinkerforge')
        os.makedirs('/tmp/generator/jar/examples')

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        examples = common.find_device_examples(device, '^example_.*\.m$')
        dest = os.path.join('/tmp/generator/jar/examples', device.get_category(), device.get_camel_case_name())

        if not os.path.exists(dest):
            os.makedirs(dest)

        for example in examples:
            shutil.copy(example[1], dest)

    def finish(self):
        root = self.get_bindings_root_directory()

        # Copy IPConnection examples
        examples = common.find_examples(root, '^example_.*\.m$')
        for example in examples:
            shutil.copy(example[1], '/tmp/generator/jar/examples')

        # Copy bindings and readme
        for filename in released_files:
            shutil.copy(os.path.join(root, 'bindings', filename), '/tmp/generator/jar/source/com/tinkerforge')

        shutil.copy(os.path.join(root, '..', 'java', 'BrickDaemon.java'), '/tmp/generator/jar/source/com/tinkerforge')
        shutil.copy(os.path.join(root, '..', 'java', 'Device.java'), '/tmp/generator/jar/source/com/tinkerforge')
        shutil.copy(os.path.join(root, '..', 'java', 'DeviceListener.java'), '/tmp/generator/jar/source/com/tinkerforge')
        shutil.copy(os.path.join(root, 'IPConnection.java'), '/tmp/generator/jar/source/com/tinkerforge')
        shutil.copy(os.path.join(root, '..', 'java', 'IPConnectionBase.java'), '/tmp/generator/jar/source/com/tinkerforge')
        shutil.copy(os.path.join(root, '..', 'java', 'TinkerforgeException.java'), '/tmp/generator/jar/source/com/tinkerforge')
        shutil.copy(os.path.join(root, '..', 'java', 'TimeoutException.java'), '/tmp/generator/jar/source/com/tinkerforge')
        shutil.copy(os.path.join(root, '..', 'java', 'AlreadyConnectedException.java'), '/tmp/generator/jar/source/com/tinkerforge')
        shutil.copy(os.path.join(root, '..', 'java', 'NotConnectedException.java'), '/tmp/generator/jar/source/com/tinkerforge')
        shutil.copy(os.path.join(root, '..', 'java', 'TinkerforgeListener.java'), '/tmp/generator/jar/source/com/tinkerforge')
        shutil.copy(os.path.join(root, 'changelog.txt'), '/tmp/generator/jar')
        shutil.copy(os.path.join(root, 'readme.txt'), '/tmp/generator/jar')

        # Make Manifest
        version = common.get_changelog_version(root)
        file('/tmp/generator/manifest.txt', 'wb').write('Bindings-Version: {0}.{1}.{2}\nBindings-Flavor: MATLAB\n'.format(*version))

        # Make jar
        with common.ChangedDirectory('/tmp/generator'):
            args = ['/usr/bin/javac ' +
                    '-Xlint ' +
                    '/tmp/generator/jar/source/com/tinkerforge/*.java']
            if subprocess.call(args, shell=True) != 0:
                raise Exception("Command '{0}' failed".format(' '.join(args)))

        with common.ChangedDirectory('/tmp/generator/jar/source'):
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

        # FIXME: remove this
        shutil.copy('/tmp/generator/jar/Tinkerforge.jar', root)

        # Make zip
        common.make_zip(self.get_bindings_name(), '/tmp/generator/jar', root, version)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', MATLABZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
