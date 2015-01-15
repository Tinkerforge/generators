#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Shell ZIP Generator
Copyright (C) 2012-2015 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_shell_zip.py: Generator for Shell ZIP

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

class ShellZipGenerator(common.Generator):
    tmp_dir          = '/tmp/generator/shell'
    tmp_examples_dir = os.path.join(tmp_dir, 'examples')

    def get_bindings_name(self):
        return 'shell'

    def prepare(self):
        common.recreate_directory(self.tmp_dir)
        os.makedirs(self.tmp_examples_dir)

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        tmp_examples_device_dir = os.path.join(self.tmp_examples_dir,
                                               device.get_category().lower(),
                                               device.get_underscore_name())

        if not os.path.exists(tmp_examples_device_dir):
            os.makedirs(tmp_examples_device_dir)

        for example in common.find_device_examples(device, '^example-.*\.sh$'):
            shutil.copy(example[1], tmp_examples_device_dir)

    def finish(self):
        root_dir = self.get_bindings_root_directory()

        # Copy IP Connection examples
        for example in common.find_examples(root_dir, '^example-.*\.sh$'):
            shutil.copy(example[1], self.tmp_examples_dir)

        # Copy bindings and readme
        shutil.copy(os.path.join(root_dir, 'tinkerforge'),                    self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'tinkerforge-bash-completion.sh'), self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'changelog.txt'),                  self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'readme.txt'),                     self.tmp_dir)
        shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'),   self.tmp_dir)

        # Make zip
        version = common.get_changelog_version(root_dir)

        common.make_zip(self.get_bindings_name(), self.tmp_dir, root_dir, version)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', ShellZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
