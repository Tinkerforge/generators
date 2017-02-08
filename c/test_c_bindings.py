#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Bindings Tester
Copyright (C) 2012-2016 Matthias Bolte <matthias@tinkerforge.com>

test_c_bindings.py: Tests the C/C++ bindings

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
import shutil

sys.path.append(os.path.split(os.getcwd())[0])
import common

class CExamplesTester(common.ExamplesTester):
    def __init__(self, path, compiler, extra_examples):
        common.ExamplesTester.__init__(self, 'c', '.c', path, comment=compiler, extra_examples=extra_examples)

        self.compiler = compiler

    def test(self, cookie, src, is_extra_example):
        # skip OLED scribble example because mingw32 has no libgd package
        if self.compiler == 'mingw32-gcc' and src.endswith('example_scribble.c'):
            self.execute(cookie, ['true'])
            return

        if is_extra_example:
            shutil.copy(src, '/tmp/tester/c')
            src = os.path.join('/tmp/tester/c', os.path.split(src)[1])

        dest = src[:-2]

        if not is_extra_example and '/brick' in src:
            dirname = os.path.split(src)[0]
            device = '/tmp/tester/c/source/{0}_{1}.c'.format(os.path.split(os.path.split(dirname)[0])[-1], os.path.split(dirname)[-1])
        else:
            device = ''

        args = []

        if self.compiler == 'gcc':
            args += ['/usr/bin/gcc', '-std=c99', '-pthread']
        elif self.compiler == 'g++':
            args += ['/usr/bin/g++', '-std=c++98', '-pthread']
        elif self.compiler == 'mingw32-gcc':
            args += ['/usr/bin/x86_64-w64-mingw32-gcc', '-Wno-error=return-type', '-lws2_32']
        elif self.compiler == 'scan-build clang':
            args += ['/usr/bin/scan-build', '/usr/bin/clang', '-std=c99', '-pthread']
        else:
            raise common.GeneratorError('Invalid compiler ' + self.compiler);

        args += ['-Wall',
                 '-Wextra',
                 '-Werror',
                 '-O2',
                 '-I/tmp/tester/c/source',
                 '-o',
                 dest,
                 '/tmp/tester/c/source/ip_connection.c']

        if len(device) > 0:
            args.append(device)
        elif is_extra_example:
            deps = glob.glob('/tmp/tester/c/source/*.c')
            deps.remove('/tmp/tester/c/source/ip_connection.c')
            args.append('-Wno-error=unused-parameter')
            args += deps

        args.append(src)

        if self.compiler == 'mingw32-gcc':
            args += ['-lws2_32']

        if src.endswith('example_scribble.c'):
            args += ['-lm', '-lgd']

        self.execute(cookie, args)

def run(path):
    extra_examples = [os.path.join(path, '../../weather-station/write_to_lcd/c/weather_station.c'),
                      os.path.join(path, '../../hardware-hacking/remote_switch/c/remote_switch.c'),
                      os.path.join(path, '../../hardware-hacking/smoke_detector/c/smoke_detector.c')]

    success = CExamplesTester(path, 'gcc', extra_examples).run()

    if not success:
        return success

    success = CExamplesTester(path, 'g++', extra_examples).run()

    if not success:
        return success

    success = CExamplesTester(path, 'mingw32-gcc', extra_examples).run()

    if not success:
        return success

    return CExamplesTester(path, 'scan-build clang', extra_examples).run()

if __name__ == "__main__":
    sys.exit(run(os.getcwd()))
