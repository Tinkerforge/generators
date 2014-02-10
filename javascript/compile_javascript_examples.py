#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JavaScript Examples Compiler
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>

compile_javascript_examples.py: Compile all examples for the JavaScript bindings

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

class JavaScriptExamplesCompiler(common.ExamplesCompiler):
    def __init__(self, path, javascript, extra_examples):
        common.ExamplesCompiler.__init__(self, 'javascript', '.js', path, comment=javascript, subdirs=['examples', 'source'], extra_examples=extra_examples)

        self.javascript = javascript

    def compile(self, src, is_extra_example):
        if is_extra_example:
            shutil.copy(src, '/tmp/compiler/')
            src = os.path.join('/tmp/compiler/', os.path.split(src)[1])

        args = [self.javascript,
                '-c',
                'import py_compile; py_compile.compile("{0}", doraise=True)'.format(src)]

        return subprocess.call(args) == 0

def run(path):
    return

    extra_examples = [os.path.join(path, '../../weather-station/xively/javascript/weather_xively.js'),
                      os.path.join(path, '../../weather-station/write_to_lcd/javascript/weather_station.js'),
                      os.path.join(path, '../../hardware-hacking/remote_switch/javascript/remote_switch.js'),
                      os.path.join(path, '../../hardware-hacking/smoke_detector/javascript/smoke_detector.js'),
                      os.path.join(path, '../../blinkenlights/demo/src/demo.js'),
                      os.path.join(path, '../../blinkenlights/demo/src/fire_widget.js'),
                      os.path.join(path, '../../blinkenlights/demo/src/pong_widget.js'),
                      os.path.join(path, '../../blinkenlights/demo/src/tetris_widget.js'),
                      os.path.join(path, '../../blinkenlights/demo/src/images_widget.js'),
                      os.path.join(path, '../../blinkenlights/demo/src/rainbow_widget.js'),
                      os.path.join(path, '../../blinkenlights/demo/src/text_widget.js'),
                      os.path.join(path, '../../blinkenlights/fire/javascript/fire.js'),
                      os.path.join(path, '../../blinkenlights/games/javascript/keypress.js'),
                      os.path.join(path, '../../blinkenlights/games/javascript/pong.js'),
                      os.path.join(path, '../../blinkenlights/games/javascript/repeated_timer.js'),
                      os.path.join(path, '../../blinkenlights/games/javascript/tetris.js'),
                      os.path.join(path, '../../blinkenlights/images/javascript/images.js'),
                      os.path.join(path, '../../blinkenlights/rainbow/javascript/rainbow.js'),
                      os.path.join(path, '../../blinkenlights/text/javascript/text.js')]

    rc = JavaScriptExamplesCompiler(path, 'javascript', extra_examples).run()

    if rc != 0:
        return rc

    return JavaScriptExamplesCompiler(path, 'python3', extra_examples).run()

if __name__ == "__main__":
    sys.exit(run(os.getcwd()))
