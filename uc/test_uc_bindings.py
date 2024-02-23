#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
C/C++ for Microcontrollers Bindings Tester
Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>

test_uc_bindings.py: Tests the C/C++ bindings for Microcontrollers

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

import re
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

class UCExamplesTester(common.Tester):
    def __init__(self, root_dir, compiler, extra_paths, run_after_unzip):
        common.Tester.__init__(self, 'uc', '.c', root_dir, comment=compiler, extra_paths=extra_paths)

        self.compiler = compiler
        self.run_after_unzip = run_after_unzip

    def after_unzip(self, tmp_dir):
        os.rename(os.path.join(tmp_dir, 'source'), os.path.join(tmp_dir, 'src'))

        if not self.run_after_unzip:
            return True

        result = True

        with common.ChangedDirectory(tmp_dir):
            print('>>> building libuc.so')
            args = ['clang', '-ggdb', '-std=c99', '-DTF_NET_ENABLE=1', '-shared', '-pthread', '-fPIC', '-I', 'src', '-o', 'libuc.so', 'src/hal_null/hal_null.c', 'src/net_null/net_null.c']
            args += glob.glob(os.path.join(tmp_dir, 'src/bindings/*.c'))

            common.execute(args)

            print('>>> checking symbol prefix')
            args = ['nm', '-g', '-l', '--defined-only', 'libuc.so']
            _, output = common.check_output_and_error(args)

            for l in output.splitlines():
                splt = l.replace("\t", " ").split(" ", 3)
                symbol = splt[2]
                if len(splt) == 4:
                    location = splt[3]
                else:
                    location = "unknown location"

                if not symbol.startswith("tf_") and symbol not in ['__bss_start', '_edata', '_end', '_fini', '_init']:
                    print("{} Exported symbol {} is missing the tf_ prefix".format(location.replace(tmp_dir, "."), symbol))
                    result = False

            for type_ in ["struct", "enum"]:
                print('>>> checking {} names'.format(type_))
                args = ['grep', '-n', '-r', 'typedef {}'.format(type_), '--include=*.h', '--exclude=bcm2835.h', '.']
                _, output = common.check_output_and_error(args)

                for l in output.splitlines():
                    m = re.match(r"(.*):typedef {}(.*)\{{".format(type_), l)
                    if not m:
                        # forward declarations won't match the output
                        if not re.match(r"(.*):typedef {} ([^\s]*) \2".format(type_), l):
                            print("Failed to parse line {}".format(l))
                            result = False
                        continue

                    location, name =  m.groups()
                    if len(name.strip()) == 0:
                        print("{0} Found {1} definition not matching to pattern typedef {1} [name] {{...}} [name]. The duplicated name is required to be able to forward declare the {1}.".format(location, type_))
                        result = False
                        continue
                    name = name.strip()
                    if not name.startswith("TF_"):
                        print("{} {} {} is missing the TF_ prefix".format(location, type_, name))
                        result = False

            print('>>> checking enum value names')
            args = ['grep', '-lr', 'typedef enum', '--include=*.h', '--exclude=bcm2835.h', '.']
            _, output = common.check_output_and_error(args)
            files = output.splitlines()

            if len(files) > 0:
                args = ['sed', '-e', '/typedef enum/,/\}/!d'] + files
                _, output = common.check_output_and_error(args)
                for l in output.splitlines():
                    l = l.strip()
                    if l.startswith("typedef") or l.startswith("}"):
                        continue

                    if not l.startswith("TF_"):
                        print("Enum value {} is missing the TF_ prefix".format(l.split(" ")[0].replace(",", "")))
                        result = False

            define_whitelist = ["MIN", "MAX", "__GNUC_PREREQ"]

            print('>>> checking define names')
            args = ['grep', '-n', '-r', '#define ', '--include=*.h', '--exclude=bcm2835.h', '.']
            _, output = common.check_output_and_error(args)
            for l in output.splitlines():
                m = re.search(r"(.*):(?://)?\s*#define ([^\s\(]*)", l)
                if not m:
                    print("Failed to parse line {}".format(l))
                    result = False
                    continue

                location, name =  m.groups()
                if not name.startswith("TF_") and not name.startswith("tf_") and not name in define_whitelist:
                    print("{} Define {} is missing the TF_ prefix".format(location, name))
                    result = False

        if result:
            print('\033[01;32m>>> test succeeded\033[0m\n')
        else:
            print('\033[01;31m>>> test failed\033[0m\n')
        return result

    def test(self, cookie, tmp_dir, scratch_dir, path, extra):
        if extra:
            shutil.copy(path, tmp_dir)
            path = os.path.join(tmp_dir, os.path.split(path)[-1])

        output = path[:-2]

        if not extra and '/brick' in path:
            dirname = os.path.split(path)[0]
            device = os.path.join(tmp_dir, 'src/bindings/{0}_{1}.c'.format(os.path.split(os.path.split(dirname)[0])[-1], os.path.split(dirname)[-1]))
        else:
            device = ''

        args = []

        if self.compiler == 'gcc':
            args += ['gcc', '-std=c99', '-DTF_NET_ENABLE=1', '-Wall', '-Wextra', '-Wpedantic', '-Wno-padded']
        elif self.compiler == 'g++':
            args += ['g++', '-std=c++98', '-DTF_NET_ENABLE=1', '-Wall', '-Wextra', '-Wpedantic', '-Wno-padded', '-Wno-deprecated', '-Wno-variadic-macros', '-Wno-old-style-cast', '-Wno-c++20-extensions']
        elif self.compiler == 'mingw32-gcc':
            args += ['x86_64-w64-mingw32-gcc', '-DTF_NET_ENABLE=1', '-Wall', '-Wextra', '-Wpedantic', '-Wno-padded']
        elif self.compiler == 'mingw32-g++':
            args += ['x86_64-w64-mingw32-g++', '-DTF_NET_ENABLE=1', '-Wall', '-Wextra']
        elif self.compiler == 'clang':
            args += ['clang', '-std=c99', '-DTF_NET_ENABLE=1', '-Weverything', '-Wno-padded', '-Wno-declaration-after-statement']
        elif self.compiler == 'clang++':
            args += ['clang++', '-std=c++98', '-DTF_NET_ENABLE=1', '-Weverything', '-Wno-padded', '-Wno-deprecated', '-Wno-variadic-macros', '-Wno-old-style-cast', '-Wno-c++20-designator']
        elif self.compiler == 'scan-build clang':
            args += ['scan-build', 'clang', '-DTF_NET_ENABLE=1', '-std=c99']
        else:
            raise common.GeneratorError('Invalid compiler ' + self.compiler)

        args += ['-Wall',
                 '-Wextra',
                 '-Werror',
                 '-O2',
                 '-I' + tmp_dir,
                 '-I' + os.path.join(tmp_dir, 'src'),
                 '-o',
                 output,
                 os.path.join(tmp_dir, 'src/bindings/base58.c'),
                 os.path.join(tmp_dir, 'src/bindings/bricklet_unknown.c'),
                 os.path.join(tmp_dir, 'src/bindings/endian_convert.c'),
                 os.path.join(tmp_dir, 'src/bindings/hal_common.c'),
                 os.path.join(tmp_dir, 'src/bindings/packet_buffer.c'),
                 os.path.join(tmp_dir, 'src/bindings/pearson_hash.c'),
                 os.path.join(tmp_dir, 'src/bindings/spitfp.c'),
                 os.path.join(tmp_dir, 'src/bindings/streaming.c'),
                 os.path.join(tmp_dir, 'src/bindings/tfp.c'),
                 os.path.join(tmp_dir, 'src/bindings/tfp_header.c'),
                 os.path.join(tmp_dir, 'src/hal_null/hal_null.c'),
                 os.path.join(tmp_dir, 'src/hal_null/example_driver.c'),
                 os.path.join(tmp_dir, 'src/net_null/net_null.c'),]

        if len(device) > 0:
            args.append(device)
        elif extra:
            dependencies = glob.glob(os.path.join(tmp_dir, 'src/*.c'))
            dependencies.remove(os.path.join(tmp_dir, 'src/ip_connection.c'))
            args.append('-Wno-error=unused-parameter')
            args += dependencies

        args.append(path)

        if self.compiler.startswith('mingw32-'):
            args += ['-lws2_32']

        self.execute(cookie, args)

    def check_success(self, exit_code, output):
        if self.compiler == 'scan-build clang' and exit_code == 0 and 'scan-build: No bugs found.\n' not in output:
            return False

        return exit_code == 0

def test(root_dir):
    extra_paths = []

    if not UCExamplesTester(root_dir, 'clang', extra_paths, True).run():
        return False

    if not UCExamplesTester(root_dir, 'clang++', extra_paths, True).run():
        return False

    if not UCExamplesTester(root_dir, 'gcc', extra_paths, False).run():
        return False

    if not UCExamplesTester(root_dir, 'g++', extra_paths, False).run():
        return False

    if not UCExamplesTester(root_dir, 'mingw32-gcc', extra_paths, False).run():
        return False

    if not UCExamplesTester(root_dir, 'mingw32-g++', extra_paths, False).run():
        return False

    return UCExamplesTester(root_dir, 'scan-build clang', extra_paths, False).run()

if __name__ == '__main__':
    common.dockerize('uc', __file__)

    test(os.getcwd())
