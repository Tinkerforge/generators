#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Bindings Tester
Copyright (C) 2012-2017 Matthias Bolte <matthias@tinkerforge.com>

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
import glob
import shutil

sys.path.append(os.path.split(os.getcwd())[0])
import common

class CExamplesTester(common.Tester):
    def __init__(self, bindings_root_directory, compiler, extra_paths):
        common.Tester.__init__(self, 'c', '.c', bindings_root_directory, comment=compiler, extra_paths=extra_paths)

        self.compiler = compiler

    def after_unzip(self):
        print('>>> patching ip_connection.c')

        with open('/tmp/tester/c/source/ip_connection.c', 'r') as f:
            code = f.read()

        # GCC 7 complains that _BSD_SOURCE is deprecated, patch the code to
        # avoid the warning, but keep using _BSD_SOURCE in the actual code for
        # backwards compatibility
        code = code.replace(' _BSD_SOURCE', ' _DEFAULT_SOURCE')

        with open('/tmp/tester/c/source/ip_connection.c', 'w') as f:
            f.write(code)

        return True

    def test(self, cookie, path, extra):
        # skip OLED scribble example because mingw32 has no libgd package
        if self.compiler.startswith('mingw32-') and path.endswith('example_scribble.c'):
            self.execute(cookie, ['true'])
            return

        if extra:
            shutil.copy(path, '/tmp/tester/c')
            path = os.path.join('/tmp/tester/c', os.path.split(path)[1])

        output = path[:-2]

        if not extra and '/brick' in path:
            dirname = os.path.split(path)[0]
            device = '/tmp/tester/c/source/{0}_{1}.c'.format(os.path.split(os.path.split(dirname)[0])[-1], os.path.split(dirname)[-1])
        else:
            device = ''

        args = []

        if self.compiler == 'gcc':
            args += ['/usr/bin/gcc', '-std=c99', '-pthread']
        elif self.compiler == 'g++':
            args += ['/usr/bin/g++', '-std=c++98', '-pthread']
        elif self.compiler == 'mingw32-gcc':
            args += ['/usr/bin/x86_64-w64-mingw32-gcc', '-Wno-error=return-type']
        elif self.compiler == 'mingw32-g++':
            args += ['/usr/bin/x86_64-w64-mingw32-g++', '-Wno-error=return-type']
        elif self.compiler == 'scan-build clang':
            args += ['/usr/bin/scan-build', '/usr/bin/clang', '-std=c99', '-pthread']
        else:
            raise common.GeneratorError('Invalid compiler ' + self.compiler)

        args += ['-Wall',
                 '-Wextra',
                 '-Werror',
                 '-O2',
                 '-I/tmp/tester/c/source',
                 '-o',
                 output,
                 '/tmp/tester/c/source/ip_connection.c']

        if len(device) > 0:
            args.append(device)
        elif extra:
            dependencies = glob.glob('/tmp/tester/c/source/*.c')
            dependencies.remove('/tmp/tester/c/source/ip_connection.c')
            args.append('-Wno-error=unused-parameter')
            args += dependencies

        args.append(path)

        if self.compiler.startswith('mingw32-'):
            args += ['-lws2_32']

        if path.endswith('example_scribble.c'):
            args += ['-lm', '-lgd']

        self.execute(cookie, args)

def run(bindings_root_directory):
    extra_paths = [os.path.join(bindings_root_directory, '../../weather-station/write_to_lcd/c/weather_station.c'),
                   os.path.join(bindings_root_directory, '../../hardware-hacking/remote_switch/c/remote_switch.c'),
                   os.path.join(bindings_root_directory, '../../hardware-hacking/smoke_detector/c/smoke_detector.c')]

    if not CExamplesTester(bindings_root_directory, 'gcc', extra_paths).run():
        return False

    if not CExamplesTester(bindings_root_directory, 'g++', extra_paths).run():
        return False

    if not CExamplesTester(bindings_root_directory, 'mingw32-gcc', extra_paths).run():
        return False

    if not CExamplesTester(bindings_root_directory, 'mingw32-g++', extra_paths).run():
        return False

    return CExamplesTester(bindings_root_directory, 'scan-build clang', extra_paths).run()

if __name__ == "__main__":
    run(os.getcwd())
