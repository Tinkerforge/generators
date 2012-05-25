#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PHP Examples Compiler
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>

compile_php_examples.py: Compile all examples for the PHP bindings

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
        if not name.endswith('.php'):
            continue

        src = os.path.join(dirname, name);

        args = ['/usr/bin/php',
                '-l',
                src]

        print 'compiling ' + src
        subprocess.call(args)

def compile(path):
    version = common.get_changelog_version(path)
    zipname = 'tinkerforge_php_bindings_{0}_{1}_{2}.zip'.format(*version)

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
    os.path.walk('/tmp/compiler/source', walker, None)

if __name__ == "__main__":
    compile(os.getcwd())
