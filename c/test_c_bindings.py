#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Bindings Tester
Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>

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

    def test(self, src, is_extra_example):
        if is_extra_example:
            shutil.copy(src, '/tmp/tester/')
            src = os.path.join('/tmp/tester/', os.path.split(src)[1])

        dest = src[:-2]

        if not is_extra_example and '/brick' in src:
            dirname = os.path.split(src)[0]
            device = '/tmp/tester/source/{0}_{1}.c'.format(os.path.split(os.path.split(dirname)[0])[-1], os.path.split(dirname)[-1])
        else:
            device = ''

        args = []

        if self.compiler == 'gcc':
            args += ['/usr/bin/gcc', '-std=c99']
        elif self.compiler == 'g++':
            args += ['/usr/bin/g++', '-std=c++98']
        elif self.compiler == 'scan-build clang':
            args += ['/usr/bin/scan-build', '/usr/bin/clang', '-std=c99']
        else:
            raise ValueError('Invalid compiler ' + self.compiler);

        args += ['-Wall',
                 '-Wextra',
                 '-Werror',
                 '-O2',
                 '-pthread',
                 '-I/tmp/tester/source',
                 '-o',
                 dest,
                 '/tmp/tester/source/ip_connection.c']

        if len(device) > 0:
            args.append(device)
        elif is_extra_example:
            deps = glob.glob('/tmp/tester/source/*.c')
            deps.remove('/tmp/tester/source/ip_connection.c')
            args.append('-Wno-error=unused-parameter')
            args += deps

        args.append(src)

        return subprocess.call(args) == 0

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

    return CExamplesTester(path, 'scan-build clang', extra_examples).run()

if __name__ == "__main__":
    sys.exit(run(os.getcwd()))
