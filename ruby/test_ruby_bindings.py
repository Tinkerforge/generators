#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ruby Bindings Tester
Copyright (C) 2012-2014, 2017-2018 Matthias Bolte <matthias@tinkerforge.com>

test_ruby_bindings.py: Tests the Ruby bindings

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

if sys.hexversion < 0x3050000:
    print('Python >= 3.5 required')
    sys.exit(1)

import os
import importlib.util

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
    generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
    generators_module = importlib.util.module_from_spec(generators_spec)

    generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common

class RubyTester(common.Tester):
    def __init__(self, root_dir, extra_paths):
        common.Tester.__init__(self, 'ruby', '.rb', root_dir, subdirs=['examples', 'source'], extra_paths=extra_paths)

    def test(self, cookie, path, extra):
        args = ['ruby',
                '-wc',
                path]

        self.execute(cookie, args)

    def check_success(self, exit_code, output):
        output = output.strip('\r\n')

        return exit_code == 0 and len(output.split('\n')) == 1 and 'Syntax OK' in output

def run(root_dir):
    extra_paths = [os.path.join(root_dir, '../../weather-station/write_to_lcd/ruby/weather_station.rb'),
                   os.path.join(root_dir, '../../hardware-hacking/remote_switch/ruby/remote_switch.rb'),
                   os.path.join(root_dir, '../../hardware-hacking/smoke_detector/ruby/smoke_detector.rb')]

    return RubyTester(root_dir, extra_paths).run()

if __name__ == '__main__':
    run(os.getcwd())
