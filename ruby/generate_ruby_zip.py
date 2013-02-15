#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ruby ZIP Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_ruby_zip.py: Generator for Ruby ZIP

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
import re

sys.path.append(os.path.split(os.getcwd())[0])
import common

device = None

def copy_examples_for_zip():
    examples = common.find_examples(device, common.path_binding, 'ruby', 'example_', '.rb')
    dest = os.path.join('/tmp/generator/gem/examples/',
                        device.get_category().lower(),
                        device.get_underscore_name())

    if not os.path.exists(dest):
        os.makedirs(dest)

    for example in examples:
        shutil.copy(example[1], dest)

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)

    copy_examples_for_zip()

def generate(path):
    # Make temporary generator directory
    if os.path.exists('/tmp/generator'):
        shutil.rmtree('/tmp/generator/')
    os.makedirs('/tmp/generator/gem/source/lib/tinkerforge')
    os.chdir('/tmp/generator')

    # Copy examples
    common.generate(path, 'en', make_files, None, False)
    shutil.copy(common.path_binding.replace('/generators/ruby', '/doc/en/source/Software/example.rb'),
                '/tmp/generator/gem/examples/example_enumerate.rb')

    # Copy bindings and readme
    for filename in glob.glob(path + '/bindings/*.rb'):
        shutil.copy(filename, '/tmp/generator/gem/source/lib/tinkerforge')

    shutil.copy(path + '/ip_connection.rb', '/tmp/generator/gem/source/lib/tinkerforge')
    shutil.copy(path + '/changelog.txt', '/tmp/generator/gem')
    shutil.copy(path + '/readme.txt', '/tmp/generator/gem')

    # Write version.rb
    version = common.get_changelog_version(path)
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
  s.summary = "Ruby API Bindings for Tinkerforge Bricks and Bricklets"
  s.files = Dir['lib/*.rb'] + Dir['lib/tinkerforge/*.rb']
  s.has_rdoc = true
  s.rdoc_options << '--title' <<  'Tinkerforge'
  s.author = "Matthias Bolte"
  s.email = "matthias@tinkerforge.com"
  s.homepage = "http://www.tinkerforge.com/"
end
""".format(*version))

    # Make gem
    os.chdir('/tmp/generator/gem/source')
    args = ['/usr/bin/gem',
            'build',
            'tinkerforge.gemspec']
    subprocess.call(args)

    # Remove build stuff
    os.remove('/tmp/generator/gem/source/tinkerforge.gemspec')
    shutil.move('/tmp/generator/gem/source/tinkerforge-{0}.{1}.{2}.gem'.format(*version),
                '/tmp/generator/gem/tinkerforge.gem')
    shutil.move('/tmp/generator/gem/source/lib/tinkerforge.rb',
                '/tmp/generator/gem/source/')
    os.makedirs('/tmp/generator/gem/source/tinkerforge')
    for filename in glob.glob('/tmp/generator/gem/source/lib/tinkerforge/*.rb'):
        shutil.move(filename, '/tmp/generator/gem/source/tinkerforge/')
    shutil.rmtree('/tmp/generator/gem/source/lib/')

    # Make zip
    common.make_zip('ruby', '/tmp/generator/gem', path, version)

if __name__ == "__main__":
    generate(os.getcwd())
