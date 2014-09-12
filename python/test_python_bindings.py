#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Bindings Tester
Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>

test_python_bindings.py: Tests the Python bindings

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
import subprocess
import shutil

sys.path.append(os.path.split(os.getcwd())[0])
import common

class PythonExamplesTester(common.ExamplesTester):
    def __init__(self, path, python, extra_examples):
        common.ExamplesTester.__init__(self, 'python', '.py', path, comment=python, subdirs=['examples', 'source'], extra_examples=extra_examples)

        self.python = python

    def test(self, src, is_extra_example):
        if is_extra_example:
            shutil.copy(src, '/tmp/tester/python')
            src = os.path.join('/tmp/tester/python', os.path.split(src)[1])

        args = [self.python,
                '-c',
                'import py_compile; py_compile.compile("{0}", doraise=True)'.format(src)]

        return subprocess.call(args) == 0

def run(path):
    extra_examples = [os.path.join(path, '../../weather-station/xively/python/weather_xively.py'),
                      os.path.join(path, '../../weather-station/write_to_lcd/python/weather_station.py'),
                      os.path.join(path, '../../hardware-hacking/remote_switch/python/remote_switch.py'),
                      os.path.join(path, '../../hardware-hacking/smoke_detector/python/smoke_detector.py'),
                      os.path.join(path, '../../blinkenlights/demo/src/demo.py'),
                      os.path.join(path, '../../blinkenlights/demo/src/fire_widget.py'),
                      os.path.join(path, '../../blinkenlights/demo/src/pong_widget.py'),
                      os.path.join(path, '../../blinkenlights/demo/src/tetris_widget.py'),
                      os.path.join(path, '../../blinkenlights/demo/src/images_widget.py'),
                      os.path.join(path, '../../blinkenlights/demo/src/rainbow_widget.py'),
                      os.path.join(path, '../../blinkenlights/demo/src/text_widget.py'),
                      os.path.join(path, '../../blinkenlights/fire/python/fire.py'),
                      os.path.join(path, '../../blinkenlights/games/python/keypress.py'),
                      os.path.join(path, '../../blinkenlights/games/python/pong.py'),
                      os.path.join(path, '../../blinkenlights/games/python/repeated_timer.py'),
                      os.path.join(path, '../../blinkenlights/games/python/tetris.py'),
                      os.path.join(path, '../../blinkenlights/images/python/images.py'),
                      os.path.join(path, '../../blinkenlights/rainbow/python/rainbow.py'),
                      os.path.join(path, '../../blinkenlights/text/python/text.py')]

    success = PythonExamplesTester(path, 'python', extra_examples).run()

    if not success:
        return success

    return PythonExamplesTester(path, 'python3', extra_examples).run()

if __name__ == "__main__":
    sys.exit(run(os.getcwd()))
