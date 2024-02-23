#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
C/C++ Bindings Tester
Copyright (C) 2012-2018 Matthias Bolte <matthias@tinkerforge.com>

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

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import glob
import shutil
import importlib.util
import importlib.machinery

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

    if sys.hexversion < 0x3050000:
        generators_module = importlib.machinery.SourceFileLoader('generators', os.path.join(generators_dir, '__init__.py')).load_module()
    else:
        generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
        generators_module = importlib.util.module_from_spec(generators_spec)

        generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common

class CExamplesTester(common.Tester):
    def __init__(self, root_dir, compiler, extra_paths):
        common.Tester.__init__(self, 'c', '.c', root_dir, comment=compiler, extra_paths=extra_paths)

        self.compiler = compiler

    def test(self, cookie, tmp_dir, scratch_dir, path, extra):
        uses_libgd = False

        with open(path, 'r') as f:
            uses_libgd = '#include <gd.h>' in f.read()

        # skip OLED scribble example because mingw32 has no libgd package
        if self.compiler.startswith('mingw32-') and uses_libgd:
            self.handle_result(cookie, 0, '>>> skipping')
            return

        if extra:
            shutil.copy(path, tmp_dir)
            path = os.path.join(tmp_dir, os.path.split(path)[-1])

        output = path[:-2]

        if not extra and '/brick' in path:
            dirname = os.path.split(path)[0]
            device = os.path.join(tmp_dir, 'source/{0}_{1}.c'.format(os.path.split(os.path.split(dirname)[0])[-1], os.path.split(dirname)[-1]))
        else:
            device = ''

        args = []

        if self.compiler == 'gcc':
            args += ['gcc', '-std=c99', '-pthread']
        elif self.compiler == 'g++':
            args += ['g++', '-std=c++98', '-pthread']
        elif self.compiler == 'mingw32-gcc':
            args += ['x86_64-w64-mingw32-gcc', '-Wno-error=return-type']
        elif self.compiler == 'mingw32-g++':
            args += ['x86_64-w64-mingw32-g++', '-Wno-error=return-type']
        elif self.compiler == 'clang':
            args += ['clang', '-std=c99', '-pthread']
        elif self.compiler == 'scan-build clang':
            args += ['scan-build', 'clang', '-std=c99', '-pthread']
        else:
            raise common.GeneratorError('Invalid compiler ' + self.compiler)

        args += ['-Wall',
                 '-Wextra',
                 '-Werror',
                 '-O2',
                 '-I' + os.path.join(tmp_dir, 'source'),
                 '-o',
                 output,
                 os.path.join(tmp_dir, 'source/ip_connection.c')]

        if len(device) > 0:
            args.append(device)
        elif extra:
            dependencies = glob.glob(os.path.join(tmp_dir, 'source/*.c'))
            dependencies.remove(os.path.join(tmp_dir, 'source/ip_connection.c'))
            args.append('-Wno-error=unused-parameter')
            args += dependencies

        args.append(path)

        if self.compiler.startswith('mingw32-'):
            args += ['-lws2_32']

        if uses_libgd:
            args += ['-lm', '-lgd']

        self.execute(cookie, args)

    def check_success(self, exit_code, output):
        if self.compiler == 'scan-build clang' and exit_code == 0 and 'scan-build: No bugs found.\n' not in output:
            return False

        return exit_code == 0

def test(root_dir):
    extra_paths = [os.path.join(root_dir, '../../weather-station/write_to_lcd/c/weather_station.c'),
                   os.path.join(root_dir, '../../hardware-hacking/remote_switch/c/remote_switch.c'),
                   os.path.join(root_dir, '../../hardware-hacking/smoke_detector/c/smoke_detector.c')]

    if not CExamplesTester(root_dir, 'gcc', extra_paths).run():
        return False

    if not CExamplesTester(root_dir, 'g++', extra_paths).run():
        return False

    if not CExamplesTester(root_dir, 'mingw32-gcc', extra_paths).run():
        return False

    if not CExamplesTester(root_dir, 'mingw32-g++', extra_paths).run():
        return False

    if not CExamplesTester(root_dir, 'clang', extra_paths).run():
        return False

    return CExamplesTester(root_dir, 'scan-build clang', extra_paths).run()

if __name__ == '__main__':
    common.dockerize('c', __file__)

    test(os.getcwd())
