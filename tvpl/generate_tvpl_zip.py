#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tinkerforge Visual Programming Language (TVPL) ZIP Generator
Copyright (C) 2015 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>

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
import os
import shutil
import subprocess
import datetime

sys.path.append(os.path.split(os.getcwd())[0])
import common
from tvpl_released_files import released_files

class TVPLZipGenerator(common.Generator):
    def __init__(self, bindings_root_directory, language):
        common.Generator.__init__(self, bindings_root_directory, language)
        self.path_dir_tmp                                = '/tmp/generator/tvpl'
        self.path_dir_tmp_javascript                     = '/tmp/generator/javascript'
        self.path_dir_tmp_closure_library                = '/tmp/generator/closure-library'
        self.path_dir_tmp_tinkerforge                    = os.path.join(self.path_dir_tmp, 'tinkerforge')
        self.path_dir_tmp_blocks                         = os.path.join(self.path_dir_tmp, 'blocks')
        self.path_dir_tmp_generators_javascript          = os.path.join(self.path_dir_tmp, 'generators', 'javascript')
        self.path_dir_tmp_generators_python              = os.path.join(self.path_dir_tmp, 'generators', 'python')
        self.path_dir_git_tvpl_blockly                   = os.path.join(self.get_bindings_root_directory(), '..', '..', 'tvpl-blockly')
        self.file_ext_block                              = '.block'
        self.file_ext_generator_javascript               = '.generator.javascript'
        self.file_ext_generator_python                   = '.generator.python'
        self.file_ext_toolbox_part                       = '.toolbox.part'
        self.file_content_block                          = ''
        self.file_content_generator_javascript           = ''
        self.file_content_generator_python               = ''
        self.dict_brick_file_content_xml_toolbox_part    = {}
        self.dict_bricklet_file_content_xml_toolbox_part = {}
        self.file_name_xml_toolbox_part_merge_with       = 'toolbox.xml.part'
        self.date                                        = datetime.datetime.now().strftime("%Y-%m-%d")
        self.version                                     = common.get_changelog_version(self.get_bindings_root_directory())
        self.file_content_append_block                   = '''{gentextstar}
\'use strict\';
goog.provide(\'Blockly.Blocks.tinkerforge\');
goog.require(\'Blockly.Blocks\');

'''.format(gentextstar = common.gen_text_star.format(self.date, *self.version))

        self.file_content_append_generator_javascript    = '''{gentextstar}
\'use strict\';
goog.provide(\'Blockly.JavaScript.tinkerforge\');
goog.require(\'Blockly.JavaScript\');

'''.format(gentextstar = common.gen_text_star.format(self.date, *self.version))

        self.file_content_append_generator_python        = '''{gentextstar}
\'use strict\';
goog.provide(\'Blockly.Python.tinkerforge\');
goog.require(\'Blockly.Python\');

'''.format(gentextstar = common.gen_text_star.format(self.date, *self.version))

    def get_bindings_name(self):
        return 'tvpl'

    def prepare(self):
        shutil.rmtree(self.path_dir_tmp, True)
        shutil.rmtree(self.path_dir_tmp_closure_library, True)
        shutil.copytree(self.path_dir_git_tvpl_blockly, self.path_dir_tmp)
        shutil.copytree(os.path.join(self.get_bindings_root_directory(), 'tinkerforge'), self.path_dir_tmp_tinkerforge)
        os.remove(os.path.join(self.path_dir_tmp_tinkerforge, 'xml', self.file_name_xml_toolbox_part_merge_with))

        previous_working_directory = os.getcwd()
        os.chdir(os.path.join(self.get_bindings_root_directory(), '..', 'javascript'))
        args = ['python']
        args.append('generate_javascript_bindings.py')
        if subprocess.call(args) != 0:
            raise Exception("Command '{cmdarg}' failed".format(cmdarg = ' '.join(args)))
        args = ['python']
        args.append(os.path.join(self.get_bindings_root_directory(), '..', 'javascript', 'generate_javascript_zip.py'))
        if subprocess.call(args) != 0:
            raise Exception("Command '{cmdarg}' failed".format(cmdarg = ' '.join(args)))
        os.chdir(previous_working_directory)

        shutil.copy(os.path.join(self.path_dir_tmp_javascript, 'browser', 'source', 'Tinkerforge.js'),
                    os.path.join(self.path_dir_tmp_tinkerforge, 'js', 'Tinkerforge.js'))
        shutil.copytree(os.path.join(self.get_bindings_root_directory(), '..', '..', 'tvpl-closure-library'),
                        self.path_dir_tmp_closure_library)

    def generate(self, device):
        if not device.is_released() or device.get_underscore_name() == 'red':
            return

        is_brick    = False
        is_bricklet = False

        if device.get_underscore_category() == 'brick':
            is_brick = True
        elif device.get_underscore_category() == 'bricklet':
            is_bricklet = True

        device_category_name          = '_'.join([device.get_underscore_category(), device.get_underscore_name()])
        filename_block                = device_category_name + self.file_ext_block
        filename_generator_javascript = device_category_name + self.file_ext_generator_javascript
        filename_generator_python     = device_category_name + self.file_ext_generator_python
        filename_toolbox_part         = device_category_name + self.file_ext_toolbox_part

        # Get device block definitions and append
        with open(os.path.join(self.bindings_root_directory, 'bindings', filename_block), 'r') as fh_block:
            self.file_content_block = self.file_content_block + fh_block.read()

        # Get device block generators and append
        with open(os.path.join(self.bindings_root_directory, 'bindings', filename_generator_javascript), 'r') as fh_generator_javascript:
            self.file_content_generator_javascript = self.file_content_generator_javascript + fh_generator_javascript.read()
        with open(os.path.join(self.bindings_root_directory, 'bindings', filename_generator_python), 'r') as fh_generator_python:
            self.file_content_generator_python = self.file_content_generator_python + fh_generator_python.read()

        # Get device toolbox code and put in dict
        with open(os.path.join(self.bindings_root_directory, 'bindings', filename_toolbox_part), 'r') as fh_toolbox_part:
            if is_brick:
                self.dict_brick_file_content_xml_toolbox_part[device_category_name] = fh_toolbox_part.read()
            elif is_bricklet:
                self.dict_bricklet_file_content_xml_toolbox_part[device_category_name] = fh_toolbox_part.read()

    def finish(self):
        root_dir = self.get_bindings_root_directory()

        # Prepare toolbox XML file content
        file_content_xml_toolbox_brick    = ''
        file_content_xml_toolbox_bricklet = ''

        for device in sorted(self.dict_brick_file_content_xml_toolbox_part):
            file_content_xml_toolbox_brick = file_content_xml_toolbox_brick + self.dict_brick_file_content_xml_toolbox_part[device]

        for device in sorted(self.dict_bricklet_file_content_xml_toolbox_part):
            file_content_xml_toolbox_bricklet = file_content_xml_toolbox_bricklet + self.dict_bricklet_file_content_xml_toolbox_part[device]

        # Write block definition file
        with open(os.path.join(self.path_dir_tmp_blocks, 'tinkerforge.js'), 'w') as fh_blocks:
            fh_blocks.write(self.file_content_append_block + self.file_content_block)

        # Write JavaScript generator file
        with open(os.path.join(self.path_dir_tmp_generators_javascript, 'tinkerforge.js'), 'w') as fh_generator_javascript:
            fh_generator_javascript.write(self.file_content_append_generator_javascript + self.file_content_generator_javascript)

        # Write Python generator file
        with open(os.path.join(self.path_dir_tmp_generators_python, 'tinkerforge.js'), 'w') as fh_generator_python:
            fh_generator_python.write(self.file_content_append_generator_python + self.file_content_generator_python)

        # Write toolbox XML file
        with open(os.path.join(root_dir, root_dir, 'tinkerforge', 'xml', self.file_name_xml_toolbox_part_merge_with), 'r') as fh_xml_toolbox_merge_with:
            file_content_xml_toolbox = '<xml id="blocklyToolbox">' + \
                                       '<category name="Tinkerforge">' + \
                                       '<category name="Bricks">' + \
                                       file_content_xml_toolbox_brick + \
                                       '</category>' + \
                                       '<category name="Bricklets">' + \
                                       file_content_xml_toolbox_bricklet + \
                                       '</category>' + \
                                       '</category>' + \
                                       '<sep></sep>' + \
                                       fh_xml_toolbox_merge_with.read()

            with open(os.path.join(self.path_dir_tmp_tinkerforge, 'xml', 'toolbox.xml'), 'w') as fh_xml_toolbox:
                fh_xml_toolbox.write('<!--\n' + common.gen_text_hash.format(self.date, *self.version) + \
                                     '-->\n' + file_content_xml_toolbox.replace('\n', ''))

        # Compile with closure library
        previous_working_directory = os.getcwd()
        os.chdir(self.path_dir_tmp)
        args = ['python']
        args.append(os.path.join(self.path_dir_tmp, 'build.py'))
        if subprocess.call(args) != 0:
            raise Exception("Command '{cmdarg}' failed".format(cmdarg = ' '.join(args)))
        os.chdir(previous_working_directory)

        # Make zip
        common.make_zip(self.get_bindings_name(),
                        self.path_dir_tmp,
                        root_dir,
                        common.get_changelog_version(root_dir))

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', TVPLZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
