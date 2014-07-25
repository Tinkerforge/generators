#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ruby ZIP Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
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
import subprocess
import glob

sys.path.append(os.path.split(os.getcwd())[0])
import common
from ruby_released_files import released_files

class RubyZipGenerator(common.Generator):
    def get_bindings_name(self):
        return 'ruby'

    def prepare(self):
        common.recreate_directory('/tmp/generator')
        os.makedirs('/tmp/generator/gem/source/lib/tinkerforge')
        os.makedirs('/tmp/generator/gem/examples')

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        examples = common.find_device_examples(device, '^example_.*\.rb$')
        dest = os.path.join('/tmp/generator/gem/examples', device.get_category().lower(), device.get_underscore_name())

        if not os.path.exists(dest):
            os.makedirs(dest)

        for example in examples:
            shutil.copy(example[1], dest)

    def finish(self):
        root = self.get_bindings_root_directory()

        # Copy IPConnection examples
        examples = common.find_examples(root, '^example_.*\.rb$')
        for example in examples:
            shutil.copy(example[1], '/tmp/generator/gem/examples')

        # Copy bindings and readme
        for filename in released_files:
            shutil.copy(os.path.join(root, 'bindings', filename), '/tmp/generator/gem/source/lib/tinkerforge')

        shutil.copy(os.path.join(root, 'ip_connection.rb'), '/tmp/generator/gem/source/lib/tinkerforge')
        shutil.copy(os.path.join(root, 'changelog.txt'), '/tmp/generator/gem')
        shutil.copy(os.path.join(root, 'readme.txt'), '/tmp/generator/gem')

        # Write version.rb
        version = common.get_changelog_version(root)
        file('/tmp/generator/gem/source/lib/tinkerforge/version.rb', 'wb').write("""
module Tinkerforge
  VERSION = '{0}.{1}.{2}'
end
""".format(*version))

        # Write tinkerforge.rb
        file('/tmp/generator/gem/source/lib/tinkerforge.rb', 'wb').write("""
require 'tinkerforge/version'

module Tinkerforge
end
""")

        # Write tinkerforge.gemspec
        file('/tmp/generator/gem/source/tinkerforge.gemspec', 'wb').write("""
spec = Gem::Specification.new do |s|
  s.name = 'tinkerforge'
  s.version = '{0}.{1}.{2}'
  s.summary = 'Ruby API Bindings for Tinkerforge Bricks and Bricklets'
  s.files = Dir['lib/*.rb'] + Dir['lib/tinkerforge/*.rb']
  s.has_rdoc = true
  s.rdoc_options << '--title' << 'Tinkerforge'
  s.required_ruby_version = '>= 1.9.0'
  s.license = 'CC0-1.0'
  s.author = 'Matthias Bolte'
  s.email = 'matthias@tinkerforge.com'
  s.homepage = 'http://www.tinkerforge.com/'
end
""".format(*version))

        # Make gem
        with common.ChangedDirectory('/tmp/generator/gem/source'):
            args = ['/usr/bin/gem',
                    'build',
                    'tinkerforge.gemspec']
            if subprocess.call(args) != 0:
                raise Exception("Command '{0}' failed".format(' '.join(args)))

        # Remove build stuff
        os.remove('/tmp/generator/gem/source/tinkerforge.gemspec')
        shutil.copy('/tmp/generator/gem/source/tinkerforge-{0}.{1}.{2}.gem'.format(*version), root)
        shutil.move('/tmp/generator/gem/source/tinkerforge-{0}.{1}.{2}.gem'.format(*version),
                    '/tmp/generator/gem/tinkerforge.gem')
        shutil.move('/tmp/generator/gem/source/lib/tinkerforge.rb',
                    '/tmp/generator/gem/source/')
        os.makedirs('/tmp/generator/gem/source/tinkerforge')
        for filename in glob.glob('/tmp/generator/gem/source/lib/tinkerforge/*.rb'):
            shutil.move(filename, '/tmp/generator/gem/source/tinkerforge/')
        shutil.rmtree('/tmp/generator/gem/source/lib/')

        # Make zip
        common.make_zip(self.get_bindings_name(), '/tmp/generator/gem', root, version)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', RubyZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
