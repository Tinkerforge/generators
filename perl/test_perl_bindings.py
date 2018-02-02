#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl Bindings Tester
Copyright (C) 2012-2018 Matthias Bolte <matthias@tinkerforge.com>

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

sys.path.append(os.path.split(os.getcwd())[0])
import common

class PerlCheckExamplesTester(common.Tester):
    def __init__(self, root_dir):
        common.Tester.__init__(self, 'perl', '.pl', root_dir, comment='check')

    def test(self, cookie, path, extra):
        path_check = path.replace('.pl', '_check.pl')

        with open(path, 'r') as f:
            code = f.read()

        with open(path_check, 'w') as f:
            f.write('use lib "/tmp/tester/perl/source/lib"; use strict; use warnings; CHECK { sub __check__ { ' + code + '\n\n}}\n\n__check__;\n')

        args = ['perl',
                '-cWT',
                path_check]

        retcode, output = common.check_output_and_error(args)
        output = output.strip('\r\n')

        # FIXME: filter out some internal Perl problems with the Math::Complex module
        filtered_output = [line for line in output.split('\n') if not line.startswith('Prototype mismatch: sub Math::Complex::')]
        success = retcode == 0 and len(filtered_output) == 1 and 'syntax OK' in output

        self.handle_result(cookie, output, success)

class PerlLintExamplesTester(common.Tester):
    def __init__(self, root_dir):
        common.Tester.__init__(self, 'perl', '.pl', root_dir, comment='lint')

    def test(self, cookie, path, extra):
        path_lint = path.replace('.pl', '_lint.pl')

        with open(path, 'r') as f:
            code = f.read()

        with open(path_lint, 'w') as f:
            f.write('use lib "/tmp/tester/perl/source/lib";' + code)

        args = ['perl',
                '-MO=Lint,all',
                path_lint]

        self.execute(cookie, args)

def run(root_dir):
    if not PerlCheckExamplesTester(root_dir).run():
        return False

    return PerlLintExamplesTester(root_dir).run()

if __name__ == "__main__":
    run(os.getcwd())
