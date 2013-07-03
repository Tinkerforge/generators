#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java Examples Compiler
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>

compile_java_examples.py: Compile all examples for the Java bindings

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

sys.path.append(os.path.split(os.getcwd())[0])
import common

class JavaExamplesCompiler(common.ExamplesCompiler):
    def __init__(self, path, extra_examples):
        common.ExamplesCompiler.__init__(self, 'java', '.java', path, extra_examples=extra_examples)

    def compile(self, src, is_extra_example):
        args = ['/usr/bin/javac',
                '-Xlint',
                '-cp',
                '/tmp/compiler/Tinkerforge.jar:.',
                src]

        return subprocess.call(args) == 0

def run(path):
    extra_examples = [os.path.join(path, '../../weather-station/examples/GuitarStation.java'),
                      os.path.join(path, '../../weather-station/write_to_lcd/java/WeatherStation.java'),
                      os.path.join(path, '../../hardware-hacking/remote_switch/java/RemoteSwitch.java'),
                      os.path.join(path, '../../hardware-hacking/smoke_detector/java/SmokeDetector.java')]

    return JavaExamplesCompiler(path, extra_examples).run()

if __name__ == "__main__":
    sys.exit(run(os.getcwd()))
