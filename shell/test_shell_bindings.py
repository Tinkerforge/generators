#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Shell Bindings Tester
Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>

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
import shutil

sys.path.append(os.path.split(os.getcwd())[0])
import common

class ShellExamplesTester(common.ExamplesTester):
    def __init__(self, path, extra_examples):
        common.ExamplesTester.__init__(self, 'shell', '.sh', path, extra_examples=extra_examples)

    def test(self, cookie, src, is_extra_example):
        args = [src]
        env = {'TINKERFORGE_SHELL_BINDINGS_DRY_RUN': '1',
               'PATH': '/tmp/tester/shell:{0}'.format(os.environ['PATH'])}

        self.execute(cookie, args, env)

def run(path):
    return ShellExamplesTester(path, []).run()

if __name__ == "__main__":
    sys.exit(run(os.getcwd()))
