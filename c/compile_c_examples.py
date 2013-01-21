#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Examples Compiler
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>

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
import shutil
import subprocess

sys.path.append(os.path.split(os.getcwd())[0])
import common

def walker(arg, dirname, names):
    for name in names:
        if not name.endswith('.c'):
            continue

        src = os.path.join(dirname, name);
        dest = src[:-2];
        if 'brick' in dirname:
            device = '/tmp/compiler/bindings/{0}_{1}.c'.format(os.path.split(os.path.split(dirname)[0])[-1], os.path.split(dirname)[-1])
        else:
            device = ''

        args = ['/usr/bin/gcc',
                '-std=c99',
                '-Wall',
                '-Wextra',
                '-pthread',
                '-I/tmp/compiler/bindings',
                '-o',
                dest,
                '/tmp/compiler/bindings/ip_connection.c']

        if len(device) > 0:
            args.append(device)

        args.append(src)

        print 'compiling (gcc) ' + src
        subprocess.call(args)

        args = ['/usr/bin/g++',
                '-std=c++98',
                '-Wall',
                '-Wextra',
                '-pthread',
                '-I/tmp/compiler/bindings',
                '-o',
                dest,
                '/tmp/compiler/bindings/ip_connection.c']

        if len(device) > 0:
            args.append(device)

        args.append(src)

        print 'compiling (g++) ' + src
        subprocess.call(args)

def compile(path):
    version = common.get_changelog_version(path)
    zipname = 'tinkerforge_c_bindings_{0}_{1}_{2}.zip'.format(*version)

    # Make temporary examples directory
    if os.path.exists('/tmp/compiler'):
        shutil.rmtree('/tmp/compiler/')
    os.makedirs('/tmp/compiler')
    os.chdir('/tmp/compiler')

    shutil.copy(os.path.join(path, zipname), '/tmp/compiler/')

    # unzip
    print 'unpacking ' + zipname
    args = ['/usr/bin/unzip',
            os.path.join('/tmp/compiler', zipname)]
    subprocess.call(args)

    # compile
    os.path.walk('/tmp/compiler/examples', walker, None)

if __name__ == "__main__":
    compile(os.getcwd())
