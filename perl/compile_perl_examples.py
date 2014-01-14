#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Examples Compiler
Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>

compile_perl_examples.py: Compile all examples for the Perl bindings

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

def check_output_and_error(*popenargs, **kwargs):
    process = subprocess.Popen(stdout=subprocess.PIPE, stderr=subprocess.PIPE, *popenargs, **kwargs)
    output, error = process.communicate()
    retcode = process.poll()
    return (retcode, output + error)

class PerlExamplesCompiler(common.ExamplesCompiler):
    def __init__(self, path, extra_examples):
        common.ExamplesCompiler.__init__(self, 'perl', '.pl', path, subdirs=['examples', 'source'], extra_examples=extra_examples)

    def compile(self, src, is_extra_example):
        if is_extra_example:
            shutil.copy(src, '/tmp/compiler/')
            src = os.path.join('/tmp/compiler/', os.path.split(src)[1])

        src_check = src.replace('.pl', '_check.pl')

        code = file(src, 'rb').read()
        file(src_check, 'wb').write('CHECK { sub __check__ { ' + code + '\n\n}}\n\n__check__;\n');

        args = ['perl',
                '-cWT',
                src_check]

        retcode, output = check_output_and_error(args)
        output = output.strip('\r\n')

        print output

        return retcode == 0 and len(output.split('\n')) == 1 and 'syntax OK' in output

def run(path):
    extra_examples = []

    return PerlExamplesCompiler(path, extra_examples).run()

if __name__ == "__main__":
    sys.exit(run(os.getcwd()))
