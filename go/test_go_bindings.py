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

if sys.hexversion < 0x3050000:
    print('Python >= 3.5 required')
    sys.exit(1)

import os
import shutil
import subprocess
import importlib.util

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
    generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
    generators_module = importlib.util.module_from_spec(generators_spec)

    generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common

class GoExamplesTester(common.Tester):
    def __init__(self, root_dir, extra_paths):
        common.Tester.__init__(self, 'go', '.go', root_dir, subdirs=["examples"])#, subdirs=["src"])
        self.firstRun = True
        self.go_cache_dir = subprocess.check_output(['go', 'env', 'GOCACHE']).strip()

    def test(self, cookie, path, extra):
        root_dir = os.path.join(os.path.dirname(path), '..')
        # ipconnection examples are one level higher than the rest.
        if not ("example_enumerate.go" in path or "example_authenticate.go" in path):
            root_dir = os.path.join(root_dir, "..")
        if self.firstRun:
            shutil.rmtree(os.path.join(root_dir, "src", "github.com"), ignore_errors=True)
            shutil.move(os.path.join(root_dir, "github.com"), os.path.join(root_dir, "src", "github.com"))
            self.firstRun = False


        args = ['go', 'build', '-o', os.path.join(os.path.dirname(path), 'example'), path]
        #args = ['pwd']
        #print(">>> Compiling examples, this will take a while...")
        self.execute(cookie, args, env={'GOPATH': os.path.normpath(root_dir), 'GOCACHE': self.go_cache_dir})

def run(root_dir):
    return GoExamplesTester(root_dir, None).run()

if __name__ == '__main__':
    run(os.getcwd())
