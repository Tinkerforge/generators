#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Go Bindings Tester
Copyright (C) 2018 Erik Fleckstein <erik@tinkerforge.com>

test_go_bindings.py: Tests the Go bindings

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

class GoExamplesTester(common.Tester):
    def __init__(self, root_dir, extra_paths):
        common.Tester.__init__(self, 'go', '.go', root_dir, subdirs=["examples"])#, subdirs=["src"])
        self.firstRun = True
        

    def test(self, cookie, path, extra):
        root_dir = os.path.join(os.path.dirname(path), '..')
        # ipconnection examples are one level higher than the rest.
        if not ("example_enumerate.go" in path or "example_authenticate.go" in path):
            root_dir = os.path.join(root_dir, "..")
        if self.firstRun:
            shutil.rmtree(os.path.join(root_dir, "src", "tinkerforge"), ignore_errors=True)
            shutil.move(os.path.join(root_dir, "tinkerforge"), os.path.join(root_dir, "src", "tinkerforge"))
            self.firstRun = False
        
        
        args = ['go', 'build', '-o', 'example', path]
        #args = ['pwd']
        #print(">>> Compiling examples, this will take a while...")
        self.execute(cookie, args, env={'GOPATH': os.path.normpath(root_dir)})

def run(root_dir):
    return GoExamplesTester(root_dir, None).run()

if __name__ == '__main__':
    run(os.getcwd())
