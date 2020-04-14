#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tinkerforge Visual Programming Language (TVPL) ZIP Generator
Copyright (C) 2015 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2015, 2017-2018 Matthias Bolte <matthias@tinkerforge.com>

generate_tvpl_zip.py: Generator for TVPL ZIP

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

sys.path.append(os.path.split(os.getcwd())[0])
import common
import tvpl_common

class TVPLZipGenerator(tvpl_common.TVPLGeneratorTrait, common.ZipGenerator):
    def __init__(self, *args):
        common.ZipGenerator.__init__(self, *args)

        self.tmp_dir                       = self.get_tmp_dir()
        self.tmp_examples_dir              = os.path.join(self.tmp_dir, 'examples')
        self.tmp_source_dir                = os.path.join(self.tmp_dir, 'source')
        self.tmp_build_dir                 = os.path.join(self.tmp_dir, 'build')
        self.tmp_build_blockly_dir         = os.path.join(self.tmp_build_dir, 'blockly')
        self.tmp_build_closure_library_dir = os.path.join(self.tmp_build_dir, 'closure-library')

        self.tmp_javascript_dir            = '/tmp/generators/javascript'
        self.tmp_blocks_dir                = os.path.join(self.tmp_build_blockly_dir, 'blocks')
        self.tmp_generators_javascript_dir = os.path.join(self.tmp_build_blockly_dir, 'generators', 'javascript')
        self.tmp_generators_python_dir     = os.path.join(self.tmp_build_blockly_dir, 'generators', 'python')

        self.block_content                 = ''
        self.generator_javascript_content  = ''
        self.generator_python_content      = ''
        self.brick_toolbox_part            = {}
        self.bricklet_toolbox_part         = {}

    def get_bindings_name(self):
        return 'tvpl'

    def get_bindings_display_name(self):
        return 'Tinkerforge Visual Programming Language (TVPL)'

    def prepare(self):
        root_dir = self.get_root_dir()

        # Create directories
        common.recreate_dir(self.tmp_dir)
        os.makedirs(self.tmp_examples_dir)
        os.makedirs(self.tmp_source_dir)
        os.makedirs(self.tmp_build_dir)

        # Copy blockly and closure-library to build directory
        shutil.copytree(os.path.join(root_dir, '..', '..', 'tvpl-blockly'), self.tmp_build_blockly_dir,
                        ignore=shutil.ignore_patterns('*/.git'))
        shutil.copytree(os.path.join(root_dir, '..', '..', 'tvpl-closure-library'), self.tmp_build_closure_library_dir,
                        ignore=shutil.ignore_patterns('*/.git', '*_test.js'))

        # Copy css/, js/, index.html and programEditor.html
        shutil.copytree(os.path.join(root_dir, 'css'), os.path.join(self.tmp_source_dir, 'css'))
        shutil.copytree(os.path.join(root_dir, 'js'), os.path.join(self.tmp_source_dir, 'js'))
        shutil.copy(os.path.join(root_dir, 'index.html'), self.tmp_source_dir)
        shutil.copy(os.path.join(root_dir, 'programEditor.html'), self.tmp_source_dir)

        # Copy general examples
        for example in common.find_examples(root_dir, r'^example_.*\.tvpl$'):
            shutil.copy(example[1], self.tmp_examples_dir)

        # Copy changelog.txt and readme.txt
        shutil.copy(os.path.join(root_dir, 'changelog.txt'),self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'readme.txt'),self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'readme-alpha.txt'),self.tmp_dir)

        # Generate JavaScript bindings
        with common.ChangedDirectory(os.path.join(root_dir, '..', 'javascript')):
            common.execute(['python2', 'generate_javascript_bindings.py'])
            common.execute(['python2', 'generate_javascript_zip.py'])

        shutil.copy(os.path.join(self.tmp_javascript_dir, 'browser', 'source', 'Tinkerforge.js'),
                    os.path.join(self.tmp_source_dir, 'js', 'Tinkerforge.js'))

    def generate(self, device):
        root_dir = self.get_root_dir()

        if not device.is_released() or device.get_device_identifier() == 17:
            return

        device_name = device.get_category().under + '_' +  device.get_name().under

        # Collect device block definitions
        with open(os.path.join(self.get_bindings_dir(), device_name + '.block'), 'r') as f:
            self.block_content += f.read()

        # Collect device block generators
        with open(os.path.join(self.get_bindings_dir(), device_name + '.generator.javascript'), 'r') as f:
            self.generator_javascript_content += f.read()

        with open(os.path.join(self.get_bindings_dir(), device_name + '.generator.python'), 'r') as f:
            self.generator_python_content += f.read()

        # Collect device toolbox code
        with open(os.path.join(self.get_bindings_dir(), device_name + '.toolbox.part'), 'r') as f:
            if device.is_brick():
                self.brick_toolbox_part[device_name] = f.read()
            else:
                self.bricklet_toolbox_part[device_name] = f.read()

        # Copy device examples
        tmp_examples_device = os.path.join(self.tmp_examples_dir,
                                           device.get_category().under,
                                           device.get_name().under)

        if not os.path.exists(tmp_examples_device):
            os.makedirs(tmp_examples_device)

        for example in common.find_device_examples(device, r'^example_.*\.tvpl$'):
            shutil.copy(example[1], tmp_examples_device)

    def finish(self):
        root_dir = self.get_root_dir()
        block_header = '''{comment}
\'use strict\';
goog.provide(\'Blockly.Blocks.tinkerforge\');
goog.require(\'Blockly.Blocks\');

'''.format(comment=self.get_header_comment('asterisk'))
        generator_javascript_header = '''{comment}
\'use strict\';
goog.provide(\'Blockly.JavaScript.tinkerforge\');
goog.require(\'Blockly.JavaScript\');

'''.format(comment=self.get_header_comment('asterisk'))
        generator_python_header = '''{comment}
\'use strict\';
goog.provide(\'Blockly.Python.tinkerforge\');
goog.require(\'Blockly.Python\');

'''.format(comment=self.get_header_comment('asterisk'))

        # Prepare toolbox XML file content
        brick_toolbox = ''

        for device in sorted(self.brick_toolbox_part):
            brick_toolbox += self.brick_toolbox_part[device]

        bricklet_toolbox = ''

        for device in sorted(self.bricklet_toolbox_part):
            bricklet_toolbox += self.bricklet_toolbox_part[device]

        # Write block definition file
        with open(os.path.join(self.tmp_blocks_dir, 'tinkerforge.js'), 'w') as f:
            f.write(block_header + self.block_content)

        # Write JavaScript generator file
        with open(os.path.join(self.tmp_generators_javascript_dir, 'tinkerforge.js'), 'w') as f:
            f.write(generator_javascript_header + self.generator_javascript_content)

        # Write Python generator file
        with open(os.path.join(self.tmp_generators_python_dir, 'tinkerforge.js'), 'w') as f:
            f.write(generator_python_header + self.generator_python_content)

        # Write toolbox XML file
        with open(os.path.join(root_dir, 'toolbox.xml.part'), 'r') as f:
            toolbox = '<xml id="toolboxTVPL">' + \
                      '<category name="Bricks">' + \
                      brick_toolbox + \
                      '</category>' + \
                      '<category name="Bricklets">' + \
                      bricklet_toolbox + \
                      '</category>' + \
                      f.read()

        os.makedirs(os.path.join(self.tmp_source_dir, 'xml'))

        with open(os.path.join(self.tmp_source_dir, 'xml', 'toolbox.xml'), 'w') as f:
            f.write(self.get_header_comment('xml') + toolbox.replace('\n', ''))

        # Compile with closure library
        with common.ChangedDirectory(self.tmp_build_blockly_dir):
            common.execute(['python2', 'build.py'])

        # Get necessary files from the build directory
        shutil.rmtree(os.path.join(self.tmp_build_blockly_dir, 'msg', 'json'))

        for name in ['media', 'msg']:
            shutil.copytree(os.path.join(self.tmp_build_blockly_dir, name),
                            os.path.join(self.tmp_source_dir, name))

        for name in ['blockly_compressed.js', 'blocks_compressed.js', 'javascript_compressed.js', 'python_compressed.js']:
            shutil.copy(os.path.join(self.tmp_build_blockly_dir, name),
                        os.path.join(self.tmp_source_dir, 'js', name))

        shutil.rmtree(self.tmp_build_dir)

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(root_dir):
    common.generate(root_dir, 'en', TVPLZipGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
