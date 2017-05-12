#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JavaScript ZIP Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2014-2015 Matthias Bolte <matthias@tinkerforge.com>

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
import os
import shutil

sys.path.append(os.path.split(os.getcwd())[0])
import common
from javascript_released_files import released_files

class JavaScriptZipGenerator(common.ZipGenerator):
    tmp_dir                           = '/tmp/generator/javascript'
    tmp_nodejs_dir                    = os.path.join(tmp_dir, 'nodejs')
    tmp_nodejs_source_dir             = os.path.join(tmp_nodejs_dir, 'source')
    tmp_nodejs_source_tinkerforge_dir = os.path.join(tmp_nodejs_source_dir, 'Tinkerforge')
    tmp_nodejs_examples_dir           = os.path.join(tmp_nodejs_dir, 'examples')
    tmp_nodejs_package_dir            = os.path.join(tmp_nodejs_dir, 'package')
    tmp_nodejs_package_lib_dir        = os.path.join(tmp_nodejs_package_dir, 'lib')
    tmp_browser_source_dir            = os.path.join(tmp_dir, 'browser', 'source')
    tmp_browser_examples_dir          = os.path.join(tmp_dir, 'browser', 'examples')

    def get_bindings_name(self):
        return 'javascript'

    def prepare(self):
        common.recreate_directory(self.tmp_dir)
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
                                                  device.get_camel_case_category(),
                                                  device.get_camel_case_name())
        tmp_browser_examples_device = os.path.join(self.tmp_browser_examples_dir,
                                                   device.get_camel_case_category(),
                                                   device.get_camel_case_name())

        if not os.path.exists(tmp_nodejs_examples_device):
            os.makedirs(tmp_nodejs_examples_device)

        if not os.path.exists(tmp_browser_examples_device):
            os.makedirs(tmp_browser_examples_device)

        for example in common.find_device_examples(device, '^Example.*\.js'):
            shutil.copy(example[1], tmp_nodejs_examples_device)

        for example in common.find_device_examples(device, '^Example.*\.html'):
            shutil.copy(example[1], tmp_browser_examples_device)

    def finish(self):
        root_dir = self.get_bindings_root_directory()

        # Copy IP Connection examples
        for example in common.find_examples(root_dir, '^Example.*\.js'):
            shutil.copy(example[1], self.tmp_nodejs_examples_dir)

        for example in common.find_examples(root_dir, '^Example.*\.html'):
            shutil.copy(example[1], self.tmp_browser_examples_dir)

        # Copy bindings and readme
        for filename in released_files:
            if filename == 'TinkerforgeNPM.js':
                shutil.copy(os.path.join(root_dir, 'bindings', filename), os.path.join(self.tmp_nodejs_package_dir, 'Tinkerforge.js'))
            elif filename == 'BrowserAPI.js':
                shutil.copy(os.path.join(root_dir, 'bindings', filename), self.tmp_nodejs_source_tinkerforge_dir)
            elif filename == 'TinkerforgeSource.js':
                shutil.copy(os.path.join(root_dir, 'bindings', filename), os.path.join(self.tmp_nodejs_source_dir, 'Tinkerforge.js'))
            else:
                shutil.copy(os.path.join(root_dir, 'bindings', filename), self.tmp_nodejs_source_tinkerforge_dir)
                shutil.copy(os.path.join(root_dir, 'bindings', filename), self.tmp_nodejs_package_lib_dir)

        # Make package.json
        version = common.get_changelog_version(root_dir)

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

        if tuple([int(n) for n in output.strip(b'\r\n').split(b'.')]) < (13, 1, 1):
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

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', JavaScriptZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
