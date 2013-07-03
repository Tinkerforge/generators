#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Examples Compiler
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>

compile_c_examples.py: Compile all examples for the C/C++ bindings

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
import glob

sys.path.append(os.path.split(os.getcwd())[0])
import common

class CExamplesCompiler(common.ExamplesCompiler):
    def __init__(self, path, compiler, extra_examples):
        common.ExamplesCompiler.__init__(self, 'c', '.c', path, comment=compiler, extra_examples=extra_examples)

        self.compiler = compiler

    def compile(self, src, is_extra_example):
        dest = src[:-2]

        if not is_extra_example and '/brick' in src:
            dirname = os.path.split(src)[0]
            device = '/tmp/compiler/bindings/{0}_{1}.c'.format(os.path.split(os.path.split(dirname)[0])[-1], os.path.split(dirname)[-1])
        else:
            device = ''

        args = []

        if self.compiler == 'gcc':
            args += ['/usr/bin/gcc', '-std=c99']
        else:
            args += ['/usr/bin/g++', '-std=c++98']

        args += ['-Wall',
                 '-Wextra',
                 '-Werror',
                 '-O2',
                 '-pthread',
                 '-I/tmp/compiler/bindings',
                 '-o',
                 dest,
                 '/tmp/compiler/bindings/ip_connection.c']

        if len(device) > 0:
            args.append(device)
        elif is_extra_example:
            deps = glob.glob('/tmp/compiler/bindings/*.c')
            deps.remove('/tmp/compiler/bindings/ip_connection.c')
            args.append('-Wno-error=unused-parameter')
            args += deps

        args.append(src)

        return subprocess.call(args) == 0

def run(path):
    extra_examples = [os.path.join(path, '../../weather-station/write_to_lcd/c/weather_station.c'),
                      os.path.join(path, '../../hardware-hacking/remote_switch/c/remote_switch.c'),
                      os.path.join(path, '../../hardware-hacking/smoke_detector/c/smoke_detector.c')]

    rc = CExamplesCompiler(path, 'gcc', extra_examples).run()

    if rc != 0:
        return rc

    return CExamplesCompiler(path, 'g++', extra_examples).run()

if __name__ == "__main__":
    sys.exit(run(os.getcwd()))
