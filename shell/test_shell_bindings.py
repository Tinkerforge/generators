#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Shell Bindings Tester
Copyright (C) 2012-2014, 2017 Matthias Bolte <matthias@tinkerforge.com>

test_shell_bindings.py: Tests the Shell bindings

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

class ShellExamplesTester(common.Tester):
    def __init__(self, bindings_root_directory):
        common.Tester.__init__(self, 'shell', '.sh', bindings_root_directory)

    def test(self, cookie, path, extra):
        path_check = path.replace('.sh', '-check.sh')

        with open(path, 'r') as f:
            code = f.read()

        with open(path_check, 'w') as f:
            f.write(code.replace('; read dummy', '').replace('kill -- -$$', 'kill $(jobs -p)'))

        os.chmod(path_check, 0o755)

        args = [path_check]
        env = {'TINKERFORGE_SHELL_BINDINGS_DRY_RUN': '1',
               'PATH': '/tmp/tester/shell:{0}'.format(os.environ['PATH'])}

        retcode, output = common.check_output_and_error(args, env=env)
        success = retcode == 0 and output.strip() in ['', 'Press key to exit']

        self.handle_result(cookie, output, success)

def run(bindings_root_directory):
    return ShellExamplesTester(bindings_root_directory).run()

if __name__ == "__main__":
    run(os.getcwd())
