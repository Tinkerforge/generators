#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl Bindings Tester
Copyright (C) 2012-2017 Matthias Bolte <matthias@tinkerforge.com>

test_perl_bindings.py: Tests the Perl bindings

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

class PerlExamplesTester(common.ExamplesTester):
    def __init__(self, path, extra_examples):
        # FIXME: currently only the exampels code is checked, but not the actual bindings code in .pm files
        common.ExamplesTester.__init__(self, 'perl', '.pl', path, extra_examples=extra_examples)

    def test(self, cookie, src, is_extra_example):
        if is_extra_example:
            shutil.copy(src, '/tmp/tester/perl')
            src = os.path.join('/tmp/tester/perl', os.path.split(src)[1])

        src_check = src.replace('.pl', '_check.pl')

        with open(src, 'r') as f:
            code = f.read()

        with open(src_check, 'w') as f:
            f.write('use lib "/tmp/tester/perl/source/lib"; use strict; use warnings; CHECK { sub __check__ { ' + code + '\n\n}}\n\n__check__;\n');

        args = ['perl',
                '-cWT',
                src_check]

        retcode, output = check_output_and_error(args)
        output = output.strip('\r\n')

        # FIXME: filter out some internal Perl problems with the Math::Complex module
        filtered_output = [line for line in output.split('\n') if not line.startswith('Prototype mismatch: sub Math::Complex::')]
        success = retcode == 0 and len(filtered_output) == 1 and 'syntax OK' in output

        self.handle_result(cookie, output, success)

def run(path):
    extra_examples = []

    return PerlExamplesTester(path, extra_examples).run()

if __name__ == "__main__":
    sys.exit(run(os.getcwd()))
