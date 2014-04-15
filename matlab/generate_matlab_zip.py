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

        os.makedirs('/tmp/generator/jar/matlab/source/com/tinkerforge')
        os.makedirs('/tmp/generator/jar/matlab/examples')

        os.makedirs('/tmp/generator/jar/octave/source/com/tinkerforge')
        os.makedirs('/tmp/generator/jar/octave/examples')

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        for flavor in ['matlab', 'octave']:
            examples = common.find_device_examples(device, '^{0}_example_.*\.m$'.format(flavor))
            dest = os.path.join('/tmp/generator/jar/{0}/examples'.format(flavor), device.get_category().lower(), device.get_underscore_name())

            if not os.path.exists(dest):
                os.makedirs(dest)

            for example in examples:
                shutil.copy(example[1], dest)

    def finish(self):
        octave_jar_path = '-classpath /usr/share/octave/packages/java-1.2.8/octave.jar '
        root = self.get_bindings_root_directory()

        for flavor in ['matlab', 'octave']:
            jar_root = '/tmp/generator/jar/' + flavor

            # Copy IPConnection examples
            examples = common.find_examples(root, '^example_.*\.m$')
            for example in examples:
                shutil.copy(example[1], jar_root + '/examples')

            # Copy bindings and readme
            for filename in released_files:
                shutil.copy(os.path.join(root, 'bindings_' + flavor, filename), jar_root + '/source/com/tinkerforge')

            shutil.copy(os.path.join(root, '..', 'java', 'BrickDaemon.java'), jar_root + '/source/com/tinkerforge')
            shutil.copy(os.path.join(root, '..', 'java', 'DeviceBase.java'), jar_root + '/source/com/tinkerforge')
            shutil.copy(os.path.join(root, 'Device_{0}.java'.format(flavor)), jar_root + '/source/com/tinkerforge/Device.java')
            shutil.copy(os.path.join(root, '..', 'java', 'DeviceListener.java'), jar_root + '/source/com/tinkerforge')
            shutil.copy(os.path.join(root, 'IPConnection_{0}.java'.format(flavor)), jar_root + '/source/com/tinkerforge/IPConnection.java')
            shutil.copy(os.path.join(root, '..', 'java', 'IPConnectionBase.java'), jar_root + '/source/com/tinkerforge')
            shutil.copy(os.path.join(root, '..', 'java', 'TinkerforgeException.java'), jar_root + '/source/com/tinkerforge')
            shutil.copy(os.path.join(root, '..', 'java', 'TimeoutException.java'), jar_root + '/source/com/tinkerforge')
            shutil.copy(os.path.join(root, '..', 'java', 'AlreadyConnectedException.java'), jar_root + '/source/com/tinkerforge')
            shutil.copy(os.path.join(root, '..', 'java', 'NotConnectedException.java'), jar_root + '/source/com/tinkerforge')
            shutil.copy(os.path.join(root, '..', 'java', 'CryptoException.java'), jar_root + '/source/com/tinkerforge')
            shutil.copy(os.path.join(root, '..', 'java', 'TinkerforgeListener.java'), jar_root + '/source/com/tinkerforge')
            shutil.copy(os.path.join(root, 'changelog.txt'), '/tmp/generator/jar/')
            shutil.copy(os.path.join(root, 'readme.txt'), '/tmp/generator/jar/')

            # Make Manifest
            version = common.get_changelog_version(root)
            file('/tmp/generator/manifest.txt', 'wb').write('Bindings-Version: {1}.{2}.{3}\nBindings-Flavor: {0}\n'.format(flavor.upper(), *version))

            # Make jar
            with common.ChangedDirectory('/tmp/generator'):
                if flavor == 'octave':
                    args = ['/usr/bin/javac ' +
                            octave_jar_path +
                            '-Xlint ' +
                            '-source 1.5 ' +
                            '-target 1.5 ' +
                            jar_root + '/source/com/tinkerforge/*.java']
                else:
                    args = ['/usr/bin/javac ' +
                            '-Xlint ' +
                            '-source 1.5 ' +
                            '-target 1.5 ' +
                            jar_root + '/source/com/tinkerforge/*.java']
                if subprocess.call(args, shell=True) != 0:
                    raise Exception("Command '{0}' failed".format(' '.join(args)))

            with common.ChangedDirectory(jar_root + '/source'):
                args = ['/usr/bin/jar ' +
                        'cfm ' +
                        jar_root + '/Tinkerforge.jar ' +
                        '/tmp/generator/manifest.txt ' +
                        'com']
                if subprocess.call(args, shell=True) != 0:
                    raise Exception("Command '{0}' failed".format(' '.join(args)))

            # Remove class
            for f in os.listdir(jar_root + '/source/com/tinkerforge/'):
                if f.endswith('.class'):
                    os.remove(jar_root + '/source/com/tinkerforge/' + f)

            # FIXME: remove this
            shutil.copy(jar_root + '/Tinkerforge.jar', root + '/Tinkerforge_' + flavor + '.jar')

        # Make zip
        common.make_zip(self.get_bindings_name(), '/tmp/generator/jar', root, version)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', MATLABZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
