#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl ZIP Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_perl_zip.py: Generator for Perl ZIP

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
from perl_released_files import released_files

class PerlZipGenerator(common.Generator):
    def get_bindings_name(self):
        return 'perl'

    def prepare(self):
        common.recreate_directory('/tmp/generator')
        os.makedirs('/tmp/generator/cpan/source/Tinkerforge')
        os.makedirs('/tmp/generator/cpan/examples')

    def generate(self, device):
        if not device.is_released():
            return

        # Copy examples
        examples = common.find_examples(device, self.get_bindings_root_directory(), self.get_bindings_name(), 'example_', '.pl')
        dest = os.path.join('/tmp/generator/cpan/examples', device.get_category().lower(), device.get_underscore_name())

        if not os.path.exists(dest):
            os.makedirs(dest)

        for example in examples:
            shutil.copy(example[1], dest)

    def finish(self):
        root = self.get_bindings_root_directory()

        # Copy examples
        shutil.copy(root.replace('/generators/perl', '/doc/en/source/Software/example.pl'),
                    '/tmp/generator/cpan/examples/example_enumerate.pl')

        # Copy bindings and readme
        for filename in released_files:
            shutil.copy(os.path.join(root, 'bindings', filename), '/tmp/generator/cpan/source/Tinkerforge')

        shutil.copy(os.path.join(root, 'IPConnection.pm'), '/tmp/generator/cpan/source/Tinkerforge')
        shutil.copy(os.path.join(root, 'Device.pm'), '/tmp/generator/cpan/source/Tinkerforge')
        shutil.copy(os.path.join(root, 'changelog.txt'), '/tmp/generator/cpan')
        shutil.copy(os.path.join(root, 'readme.txt'), '/tmp/generator/cpan')

        # Make zip
        version = common.get_changelog_version(root)
        common.make_zip(self.get_bindings_name(), '/tmp/generator/cpan', root, version)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', PerlZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
