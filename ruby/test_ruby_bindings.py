#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ruby Bindings Tester
Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>

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
import os

sys.path.append(os.path.split(os.getcwd())[0])
import common

class RubyExamplesTester(common.ExamplesTester):
    def __init__(self, path, extra_examples):
        common.ExamplesTester.__init__(self, 'ruby', '.rb', path, subdirs=['examples', 'source'], extra_examples=extra_examples)

    def test(self, cookie, src, is_extra_example):
        args = ['/usr/bin/ruby',
                '-wc',
                src]

        retcode, output = common.check_output_and_error(args)
        output = output.strip('\r\n')
        success = retcode == 0 and len(output.split('\n')) == 1 and 'Syntax OK' in output

        self.handle_result(cookie, output, success)

def run(path):
    extra_examples = [os.path.join(path, '../../weather-station/write_to_lcd/ruby/weather_station.rb'),
                      os.path.join(path, '../../hardware-hacking/remote_switch/ruby/remote_switch.rb'),
                      os.path.join(path, '../../hardware-hacking/smoke_detector/ruby/smoke_detector.rb')]

    return RubyExamplesTester(path, extra_examples).run()

if __name__ == "__main__":
    sys.exit(run(os.getcwd()))
