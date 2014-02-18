#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JavaScript ZIP Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014 Olaf Lüke <olaf@tinkerforge.com>

generator_javascript_zip.py: Generator for JavaScript ZIP

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
from javascript_released_files import released_files

class JavaScriptZipGenerator(common.Generator):
    def get_bindings_name(self):
        return 'javascript'

    def prepare(self):
        common.recreate_directory('/tmp/generator')
        os.makedirs('/tmp/generator/npn/nodejs/source/Tinkerforge')
        os.makedirs('/tmp/generator/npn/nodejs/examples')
        os.makedirs('/tmp/generator/npn/nodejs/npm_pkg_dir')
        os.makedirs('/tmp/generator/npn/nodejs/npm_pkg_dir/lib')
        os.makedirs('/tmp/generator/npn/browser/source')
        os.makedirs('/tmp/generator/npn/browser/examples')

    def generate(self, device):
        if not device.is_released():
            return

        # Copy examples
        examples_nodejs = common.find_examples(device, self.get_bindings_root_directory(), self.get_bindings_name(), 'Example', '.js')
        examples_browser = common.find_examples(device, self.get_bindings_root_directory(), self.get_bindings_name(), 'Example', '.html')
        dest_nodejs = os.path.join('/tmp/generator/npn/nodejs/examples/', device.get_category(), device.get_camel_case_name())
        dest_browser = os.path.join('/tmp/generator/npn/browser/examples/', device.get_category(), device.get_camel_case_name())

        if not os.path.exists(dest_nodejs):
            os.makedirs(dest_nodejs)
        if not os.path.exists(dest_browser):
            os.makedirs(dest_browser)

        for example in examples_nodejs:
            shutil.copy(example[1], dest_nodejs)

        for example in examples_browser:
            shutil.copy(example[1], dest_browser)

    def finish(self):
        root = self.get_bindings_root_directory()

        # Copy examples
        #shutil.copy(root.replace('/generators/javascript', '/doc/en/source/Software/Example.js'),
        #            '/tmp/generator/npn/examples/ExampleEnumerate.js')

        # Copy bindings and readme
        for filename in released_files:
            print filename
            if(filename == os.path.join(root, 'bindings', 'TinkerforgeMain.js')):
                shutil.copy(os.path.join(root, 'bindings', filename), '/tmp/generator/npn/nodejs/npm_pkg_dir/Tinkerforge.js')
                continue
            if(filename == os.path.join(root, 'bindings', 'BrowserAPI.js')):
                shutil.copy(os.path.join(root, 'bindings', filename), '/tmp/generator/npn/nodejs/source/Tinkerforge/')
                continue
            shutil.copy(os.path.join(root, 'bindings', filename), '/tmp/generator/npn/nodejs/source/Tinkerforge/')
            shutil.copy(os.path.join(root, 'bindings', filename), '/tmp/generator/npn/nodejs/npm_pkg_dir/lib/')

        dot_version = '.'.join(str(i) for i in common.get_changelog_version(root))

        # Replace <TF_API_VERSION> in package.json file
        package_json_file = open(os.path.join(root, 'package.json'), 'rb')
        package_json_lines = package_json_file.readlines()
        for i, package_json_line in enumerate(package_json_lines):
            package_json_lines[i] = package_json_line.replace("<TF_API_VERSION>", dot_version)
        package_json_file.close()
        package_json_file = open('/tmp/generator/npn/nodejs/npm_pkg_dir/package.json', 'wb+')
        for package_json_line in package_json_lines:
            package_json_file.write(str(package_json_line))
        package_json_file.close()

        #shutil.copy(os.path.join(root, 'package.json'), '/tmp/generator/npn/nodejs/npm_pkg_dir/package.json')
        shutil.copy(os.path.join(root, 'README.md'), '/tmp/generator/npn/nodejs/npm_pkg_dir/README.md')
        shutil.copy(os.path.join(root, 'LICENCE'), '/tmp/generator/npn/nodejs/npm_pkg_dir/LICENCE')
        shutil.copy(os.path.join(root, 'IPConnection.js'), '/tmp/generator/npn/nodejs/npm_pkg_dir/lib/IPConnection.js')
        shutil.copy(os.path.join(root, 'Device.js'), '/tmp/generator/npn/nodejs/npm_pkg_dir/lib/Device.js')

        # Replace <TF_API_VERSION> in readme.txt
        readme_txt_file = open(os.path.join(root, 'readme.txt'), 'rb')
        readme_txt_lines = readme_txt_file.readlines()
        for i, readme_txt_line in enumerate(readme_txt_lines):
            readme_txt_lines[i] = readme_txt_line.replace("<TF_API_VERSION>", dot_version)
        readme_txt_file.close()
        readme_txt_file = open('/tmp/generator/npn/readme.txt', 'wb+')
        for readme_txt_line in readme_txt_lines:
            readme_txt_file.write(str(readme_txt_line))
        readme_txt_file.close()

        shutil.copy(os.path.join(root, 'IPConnection.js'), '/tmp/generator/npn/nodejs/source/Tinkerforge')
        shutil.copy(os.path.join(root, 'Device.js'), '/tmp/generator/npn/nodejs/source/Tinkerforge')
        shutil.copy(os.path.join(root, 'changelog.txt'), '/tmp/generator/npn')

        # Copy browser specific files
        shutil.copy(os.path.join(root, 'es5-shim.js'), '/tmp/generator/npn/nodejs/source/Tinkerforge')
        shutil.copy(os.path.join(root, 'es5-sham.js'), '/tmp/generator/npn/nodejs/source/Tinkerforge')

        # Make Tinkerforge.js for browser with browserify
        os.chdir('/tmp/generator/npn/nodejs/source/Tinkerforge/')
        browserify_args = ['browserify']
        browserify_args.extend(os.listdir('/tmp/generator/npn/nodejs/source/Tinkerforge/'))
        browserify_args.append('-o')
        browserify_args.append('/tmp/generator/npn/browser/source/Tinkerforge.js')
        if subprocess.call(browserify_args) != 0:
            raise Exception("Command '{0}' failed".format(' '.join(browserify_args)))

        # Remove browser specific files
        os.remove('/tmp/generator/npn/nodejs/source/Tinkerforge/BrowserAPI.js')
        os.remove('/tmp/generator/npn/nodejs/source/Tinkerforge/es5-shim.js')
        os.remove('/tmp/generator/npn/nodejs/source/Tinkerforge/es5-sham.js')

        # Generate the NPM package and put it on the root of ZIP archive
        os.chdir('/tmp/generator/npn/nodejs/npm_pkg_dir')
        

        if subprocess.call('npm pack', shell=True) != 0:
            raise Exception("Command npm pack failed")
        
        shutil.copy(os.path.join('tinkerforge-'+dot_version+'.tgz'), '/tmp/generator/npn/tinkerforge-'+dot_version+'.tgz')    

        # Remove directory npm_pkg_dir
        shutil.rmtree('/tmp/generator/npn/nodejs/npm_pkg_dir/')

        # Make zip
        version = common.get_changelog_version(root)
        common.make_zip(self.get_bindings_name(), '/tmp/generator/npn', root, version)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', JavaScriptZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
