#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JavaScript ZIP Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2014-2015, 2018 Matthias Bolte <matthias@tinkerforge.com>

generate_javascript_zip.py: Generator for JavaScript ZIP

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
from generators.javascript import javascript_common

class JavaScriptZipGenerator(javascript_common.JavascriptGeneratorTrait, common.ZipGenerator):
    def __init__(self, *args):
        common.ZipGenerator.__init__(self, *args)

        self.tmp_dir                           = self.get_tmp_dir()
        self.tmp_nodejs_dir                    = os.path.join(self.tmp_dir, 'nodejs')
        self.tmp_nodejs_source_dir             = os.path.join(self.tmp_nodejs_dir, 'source')
        self.tmp_nodejs_source_tinkerforge_dir = os.path.join(self.tmp_nodejs_source_dir, 'Tinkerforge')
        self.tmp_nodejs_examples_dir           = os.path.join(self.tmp_nodejs_dir, 'examples')
        self.tmp_nodejs_package_dir            = os.path.join(self.tmp_nodejs_dir, 'package')
        self.tmp_nodejs_package_lib_dir        = os.path.join(self.tmp_nodejs_package_dir, 'lib')
        self.tmp_browser_source_dir            = os.path.join(self.tmp_dir, 'browser', 'source')
        self.tmp_browser_examples_dir          = os.path.join(self.tmp_dir, 'browser', 'examples')

    def get_bindings_name(self):
        return 'javascript'

    def prepare(self):
        common.recreate_dir(self.tmp_dir)
        os.makedirs(self.tmp_nodejs_dir)
        os.makedirs(self.tmp_nodejs_source_dir)
        os.makedirs(self.tmp_nodejs_source_tinkerforge_dir)
        os.makedirs(self.tmp_nodejs_examples_dir)
        os.makedirs(self.tmp_nodejs_package_dir)
        os.makedirs(self.tmp_nodejs_package_lib_dir)
        os.makedirs(self.tmp_browser_source_dir)
        os.makedirs(self.tmp_browser_examples_dir)

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        tmp_nodejs_examples_device = os.path.join(self.tmp_nodejs_examples_dir,
                                                  device.get_category().camel,
                                                  device.get_name().camel)
        tmp_browser_examples_device = os.path.join(self.tmp_browser_examples_dir,
                                                   device.get_category().camel,
                                                   device.get_name().camel)

        if not os.path.exists(tmp_nodejs_examples_device):
            os.makedirs(tmp_nodejs_examples_device)

        if not os.path.exists(tmp_browser_examples_device):
            os.makedirs(tmp_browser_examples_device)

        for example in common.find_device_examples(device, r'^Example.*\.js'):
            shutil.copy(example[1], tmp_nodejs_examples_device)

        for example in common.find_device_examples(device, r'^Example.*\.html'):
            shutil.copy(example[1], tmp_browser_examples_device)

    def finish(self):
        root_dir = self.get_root_dir()

        # Copy IP Connection examples
        if self.get_config_name().space == 'Tinkerforge':
            for example in common.find_examples(root_dir, r'^Example.*\.js'):
                shutil.copy(example[1], self.tmp_nodejs_examples_dir)

            for example in common.find_examples(root_dir, r'^Example.*\.html'):
                shutil.copy(example[1], self.tmp_browser_examples_dir)

        # Copy bindings and readme
        for filename in self.get_released_files():
            if filename == 'TinkerforgeNPM.js':
                shutil.copy(os.path.join(self.get_bindings_dir(), filename), os.path.join(self.tmp_nodejs_package_dir, 'Tinkerforge.js'))
            elif filename == 'BrowserAPI.js':
                shutil.copy(os.path.join(self.get_bindings_dir(), filename), self.tmp_nodejs_source_tinkerforge_dir)
            elif filename == 'TinkerforgeSource.js':
                shutil.copy(os.path.join(self.get_bindings_dir(), filename), os.path.join(self.tmp_nodejs_source_dir, 'Tinkerforge.js'))
            else:
                shutil.copy(os.path.join(self.get_bindings_dir(), filename), self.tmp_nodejs_source_tinkerforge_dir)
                shutil.copy(os.path.join(self.get_bindings_dir(), filename), self.tmp_nodejs_package_lib_dir)

        # Make package.json
        version = self.get_changelog_version()

        common.specialize_template(os.path.join(root_dir, 'package.json.template'),
                                   os.path.join(self.tmp_nodejs_package_dir, 'package.json'),
                                   {'<<VERSION>>': '.'.join(version)})

        shutil.copy(os.path.join(root_dir, 'IPConnection.js'),              self.tmp_nodejs_package_lib_dir)
        shutil.copy(os.path.join(root_dir, 'Device.js'),                    self.tmp_nodejs_package_lib_dir)
        shutil.copy(os.path.join(root_dir, 'LICENSE'),                      self.tmp_nodejs_package_dir)
        shutil.copy(os.path.join(root_dir, 'README.md'),                    self.tmp_nodejs_package_dir)

        shutil.copy(os.path.join(root_dir, 'IPConnection.js'),              self.tmp_nodejs_source_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'Device.js'),                    self.tmp_nodejs_source_tinkerforge_dir)

        shutil.copy(os.path.join(root_dir, 'changelog.txt'),                self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'readme.txt'),                   self.tmp_dir)
        shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'), self.tmp_dir)

        # Copy browser specific files
        shutil.copy(os.path.join(root_dir, 'es5-shim.js'),                  self.tmp_nodejs_source_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'es5-sham.js'),                  self.tmp_nodejs_source_tinkerforge_dir)

        # Make Tinkerforge.js for browser with browserify
        retcode, output = common.check_output_and_error(['browserify', '--version'])

        if retcode != 0:
            raise common.GeneratorError('Could not get browserify version')

        if tuple([int(n) for n in output.strip('\r\n').split('.')]) < (13, 1, 1):
            raise common.GeneratorError('Need browserify version >= 13.1.1')

        with common.ChangedDirectory(self.tmp_nodejs_source_tinkerforge_dir):
            args = ['browserify']
            args.extend(sorted(os.listdir(self.tmp_nodejs_source_tinkerforge_dir)))
            args.append('-o')
            args.append(os.path.join(self.tmp_browser_source_dir, 'Tinkerforge.js'))

            common.execute(args)

        # Remove browser specific files
        os.remove(os.path.join(self.tmp_nodejs_source_tinkerforge_dir, 'BrowserAPI.js'))
        os.remove(os.path.join(self.tmp_nodejs_source_tinkerforge_dir, 'es5-shim.js'))
        os.remove(os.path.join(self.tmp_nodejs_source_tinkerforge_dir, 'es5-sham.js'))

        # Generate the NPM package and put it on the root of ZIP archive
        with common.ChangedDirectory(self.tmp_nodejs_package_dir):
            common.execute(['npm', 'pack'])

        package_name = 'tinkerforge-{0}.{1}.{2}.tgz'.format(*version)

        shutil.copy(os.path.join(self.tmp_nodejs_package_dir, package_name),
                    os.path.join(self.tmp_nodejs_dir, 'tinkerforge.tgz'))
        shutil.copy(os.path.join(self.tmp_nodejs_package_dir, package_name),
                    os.path.join(root_dir, package_name))

        # Remove package directory
        shutil.rmtree(self.tmp_nodejs_package_dir)

        # Make zip
        self.create_zip_file(self.tmp_dir)

        # copy Tinkerforge.js to bindings root dir so copy_all.py can pick it up
        shutil.copy(os.path.join(self.tmp_browser_source_dir, 'Tinkerforge.js'), root_dir)

def generate(root_dir):
    common.generate(root_dir, 'en', JavaScriptZipGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
