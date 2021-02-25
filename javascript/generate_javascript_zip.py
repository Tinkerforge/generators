#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JavaScript ZIP Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2014-2015, 2018, 2020 Matthias Bolte <matthias@tinkerforge.com>

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

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import shutil
import collections
import json
import subprocess
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
from generators.javascript import javascript_common

class JavaScriptZipGenerator(javascript_common.JavascriptGeneratorTrait, common.ZipGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tmp_dir                           = self.get_zip_dir()
        self.tmp_nodejs_dir                    = os.path.join(self.tmp_dir, 'nodejs')
        self.tmp_nodejs_source_dir             = os.path.join(self.tmp_nodejs_dir, 'source')
        self.tmp_nodejs_source_tinkerforge_dir = os.path.join(self.tmp_nodejs_source_dir, 'Tinkerforge')
        self.tmp_nodejs_examples_dir           = os.path.join(self.tmp_nodejs_dir, 'examples')
        self.tmp_nodejs_package_dir            = os.path.join(self.tmp_nodejs_dir, 'package')
        self.tmp_nodejs_package_lib_dir        = os.path.join(self.tmp_nodejs_package_dir, 'lib')
        self.tmp_browser_source_dir            = os.path.join(self.tmp_dir, 'browser', 'source')
        self.tmp_browser_examples_dir          = os.path.join(self.tmp_dir, 'browser', 'examples')

    def prepare(self):
        super().prepare()

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

    def patch_package_lock(self, path):
        # https://github.com/Tinkerforge/generators/commit/a05800794b2d1267bc04d6936315bc864cd60425
        cut_off_date = '2016-11-15'

        with open(path, 'r') as f:
            source = json.loads(f.read())

        target = {}

        target['requires'] = source['requires']
        target['lockfileVersion'] = source['lockfileVersion']
        target['dependencies'] = collections.OrderedDict()

        for package in source['dependencies']:
            print(package, '...')

            meta = json.loads(subprocess.check_output(['npm', 'view', '--json', package]).decode('utf-8'))
            candidate_version = None
            candidate_date = None

            for version in sorted(meta['versions']):
                date = meta['time'][version]

                if date < cut_off_date and (candidate_version == None or date > candidate_date):
                    candidate_version = version
                    candidate_date = date

            print(package, candidate_version, candidate_date)

            if candidate_version != None:
                target['dependencies'][package] = {'version': candidate_version}

        with open(path, 'w') as f:
            f.write(json.dumps(target, indent=2))

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

        # Ensure local browserify is installed
        browserify_dir = os.path.join(root_dir, 'browserify')
        browserify_version_path = os.path.join(browserify_dir, 'version')

        try:
            with open(browserify_version_path, 'r') as f:
                browserify_version = int(f.read().strip())
        except:
            browserify_version = None

        if browserify_version != 1:
            print('installing/updating local browserify installation')

            if os.path.exists(browserify_dir):
                shutil.rmtree(browserify_dir)

            os.mkdir(browserify_dir)

            with open(os.path.join(browserify_dir, 'package.json'), 'w') as f:
                f.write('{"dependencies": {"browserify": "13.1.1"}}\n')

            with common.ChangedDirectory(browserify_dir):
                common.execute(['npm', 'install'])

            self.patch_package_lock(os.path.join(browserify_dir, 'package-lock.json'))

            shutil.rmtree(os.path.join(browserify_dir, 'node_modules'))

            with common.ChangedDirectory(browserify_dir):
                common.execute(['npm', 'install', '--no-save'])

            with open(os.path.join(browserify_dir, 'version'), 'w') as f:
                f.write('1\n')

        # Make Tinkerforge.js for browser with browserify
        with common.ChangedDirectory(self.tmp_nodejs_source_tinkerforge_dir):
            args = ['node', os.path.join(browserify_dir, 'node_modules', 'browserify', 'bin', 'cmd.js')]
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

def generate(root_dir, language):
    common.generate(root_dir, language, JavaScriptZipGenerator)

if __name__ == '__main__':
    common.dockerize('javascript', __file__)

    generate(os.getcwd(), 'en')
