#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ruby ZIP Generator
Copyright (C) 2012-2015, 2018 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_ruby_zip.py: Generator for Ruby ZIP

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
import ruby_common

class RubyZipGenerator(ruby_common.RubyGeneratorTrait, common.ZipGenerator):
    def __init__(self, *args):
        common.ZipGenerator.__init__(self, *args)

        self.tmp_dir                        = self.get_tmp_dir()
        self.tmp_source_dir                 = os.path.join(self.tmp_dir, 'source')
        self.tmp_source_lib_dir             = os.path.join(self.tmp_source_dir, 'lib')
        self.tmp_source_lib_tinkerforge_dir = os.path.join(self.tmp_source_lib_dir, 'tinkerforge')
        self.tmp_examples_dir               = os.path.join(self.tmp_dir, 'examples')

    def get_bindings_name(self):
        return 'ruby'

    def prepare(self):
        common.recreate_dir(self.tmp_dir)
        os.makedirs(self.tmp_source_dir)
        os.makedirs(self.tmp_source_lib_dir)
        os.makedirs(self.tmp_source_lib_tinkerforge_dir)
        os.makedirs(self.tmp_examples_dir)

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        tmp_examples_device = os.path.join(self.tmp_examples_dir,
                                           device.get_category().under,
                                           device.get_name().under)

        if not os.path.exists(tmp_examples_device):
            os.makedirs(tmp_examples_device)

        for example in common.find_device_examples(device, r'^example_.*\.rb$'):
            shutil.copy(example[1], tmp_examples_device)

    def finish(self):
        root_dir = self.get_root_dir()

        # Copy IP Connection examples
        if self.get_config_name().space == 'Tinkerforge':
            for example in common.find_examples(root_dir, r'^example_.*\.rb$'):
                shutil.copy(example[1], self.tmp_examples_dir)

        # Copy bindings and readme
        for filename in self.get_released_files():
            shutil.copy(os.path.join(self.get_bindings_dir(), filename), self.tmp_source_lib_tinkerforge_dir)

        shutil.copy(os.path.join(root_dir, 'ip_connection.rb'),             self.tmp_source_lib_tinkerforge_dir)
        shutil.copy(os.path.join(root_dir, 'changelog.txt'),                self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'readme.txt'),                   self.tmp_dir)
        shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'), self.tmp_dir)

        # Make version.rb
        version = self.get_changelog_version()

        with open(os.path.join(self.tmp_source_lib_tinkerforge_dir, 'version.rb'), 'w') as f:
            f.write("""
module Tinkerforge
  VERSION = '{0}.{1}.{2}'
end
""".format(*version))

        # Make tinkerforge.rb
        with open(os.path.join(self.tmp_source_lib_dir, 'tinkerforge.rb'), 'w') as f:
            f.write("""
require 'tinkerforge/version'

module Tinkerforge
end
""")

        # Make tinkerforge.gemspec
        tmp_gemspec = os.path.join(self.tmp_source_dir, 'tinkerforge.gemspec')

        common.specialize_template(os.path.join(root_dir, 'tinkerforge.gemspec.template'),
                                   tmp_gemspec,
                                   {'<<VERSION>>': '.'.join(version)})

        # Make gem
        with common.ChangedDirectory(self.tmp_source_dir):
            common.execute(['gem', 'build', 'tinkerforge.gemspec'])

        # Remove build stuff
        tmp_gem = os.path.join(self.tmp_source_dir, 'tinkerforge-{0}.{1}.{2}.gem'.format(*version))

        os.remove(tmp_gemspec)
        shutil.copy(tmp_gem, root_dir)
        shutil.move(tmp_gem, os.path.join(self.tmp_dir, 'tinkerforge.gem'))
        shutil.move(os.path.join(self.tmp_source_lib_dir, 'tinkerforge.rb'), self.tmp_source_dir)
        shutil.move(self.tmp_source_lib_tinkerforge_dir, os.path.join(self.tmp_source_dir, 'tinkerforge'))
        shutil.rmtree(self.tmp_source_lib_dir)

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(root_dir):
    common.generate(root_dir, 'en', RubyZipGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
