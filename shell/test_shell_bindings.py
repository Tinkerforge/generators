#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Shell Bindings Tester
Copyright (C) 2012-2014, 2017-2018 Matthias Bolte <matthias@tinkerforge.com>

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
    def __init__(self, root_dir):
        common.Tester.__init__(self, 'shell', '.sh', root_dir)

    def test(self, cookie, path, extra):
        path_check = path.replace('.sh', '-check.sh')

        with open(path, 'r') as f:
            code = f.read()

        with open(path_check + '.tmp', 'w') as f:
            f.write(code.replace('; read dummy', '').replace('kill -- -$$', 'kill $(jobs -p)'))

        os.chmod(path_check + '.tmp', 0o755)
        os.rename(path_check + '.tmp', path_check)

        args = [path_check]
        env = {'TINKERFORGE_SHELL_BINDINGS_DRY_RUN': '1',
               'PATH': '/tmp/tester/shell:{0}'.format(os.environ['PATH'])}

        self.execute(cookie, args, env)

    def check_success(self, exit_code, output):
        return exit_code == 0 and output.strip() in ['', 'Press key to exit']

def run(root_dir):
    return ShellExamplesTester(root_dir).run()

if __name__ == '__main__':
    run(os.getcwd())
