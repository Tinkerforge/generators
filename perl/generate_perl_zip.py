#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl ZIP Generator
Copyright (C) 2012-2015, 2017-2018 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_perl_zip.py: Generator for Perl ZIP

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
from perl_released_files import released_files

class PerlZipGenerator(common.ZipGenerator):
    tmp_dir                        = '/tmp/generator/perl'
    tmp_source_dir                 = os.path.join(tmp_dir, 'source')
    tmp_source_lib_dir             = os.path.join(tmp_source_dir, 'lib')
    tmp_source_lib_tinkerforge_dir = os.path.join(tmp_source_lib_dir, 'Tinkerforge')
    tmp_examples_dir               = os.path.join(tmp_dir, 'examples')

    def get_bindings_name(self):
        return 'perl'

    def prepare(self):
        common.recreate_dir(self.tmp_dir)
        os.makedirs(self.tmp_source_dir)
        os.makedirs(self.tmp_source_lib_tinkerforge_dir)
        os.makedirs(self.tmp_examples_dir)

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        tmp_examples_device = os.path.join(self.tmp_examples_dir,
                                           device.get_underscore_category(),
                                           device.get_underscore_name())

        if not os.path.exists(tmp_examples_device):
            os.makedirs(tmp_examples_device)

        for example in common.find_device_examples(device, r'^example_.*\.pl$'):
            shutil.copy(example[1], tmp_examples_device)

    def finish(self):
        root_dir = self.get_root_dir()

        # Copy IP Connection examples
        for example in common.find_examples(root_dir, r'^example_.*\.pl$'):
            shutil.copy(example[1], self.tmp_examples_dir)

        # Copy bindings and readme
        for filename in released_files:
            shutil.copy(os.path.join(self.get_bindings_dir(), filename), self.tmp_source_lib_tinkerforge_dir)

        shutil.copy(os.path.join(root_dir, 'IPConnection.pm'),              self.tmp_source_lib_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'Device.pm'),                    self.tmp_source_lib_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'Error.pm'),                     self.tmp_source_lib_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'changelog.txt'),                self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'readme.txt'),                   self.tmp_dir)
        shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'), self.tmp_dir)

        # Make Tinkerforge.pm
        version = common.get_changelog_version(root_dir)

        common.specialize_template(os.path.join(root_dir, 'Tinkerforge.pm.template'),
                                   os.path.join(self.tmp_source_lib_dir, 'Tinkerforge.pm'),
                                   {'<<VERSION>>': '.'.join(version)})

        # Copy Makefile.PL
        shutil.copy(os.path.join(root_dir, 'Makefile.PL'), self.tmp_source_dir)

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(root_dir):
    common.generate(root_dir, 'en', PerlZipGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
