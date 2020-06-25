#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Rust Bindings Tester
Copyright (C) 2018 Erik Fleckstein <erik@tinkerforge.com>

test_rust_bindings.py: Tests the Rust bindings

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

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import shutil
import importlib.util
import importlib.machinery

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

    if sys.hexversion < 0x3050000:
        generators_module = importlib.machinery.SourceFileLoader('generators', os.path.join(generators_dir, '__init__.py')).load_module()
    else:
        generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
        generators_module = importlib.util.module_from_spec(generators_spec)

        generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common

class RustExamplesTester(common.Tester):
    def __init__(self, root_dir, extra_paths):
        common.Tester.__init__(self, 'rust', 'Cargo.toml', root_dir, subdirs=".")#, subdirs=["src"])

    def test(self, cookie, path, extra):
        example_path = os.path.join(os.path.dirname(path), 'examples')

        for (dirpath, _dirnames, filenames) in os.walk(example_path):
            for file in filenames:
                shutil.move(os.path.join(dirpath, file), os.path.join(example_path, dirpath+'_'+file))

        cargo_folder = os.path.join(os.path.dirname(path), ".cargo")

        os.makedirs(cargo_folder)
        with open(os.path.join(cargo_folder, "config"), 'w+') as f:
            f.write("""[target.x86_64-unknown-linux-gnu]
runner = ["/tmp/tester/rust/nothing.sh"]""")

        with open(os.path.join(os.path.dirname(path), "nothing.sh"), 'w+') as f:
            f.write("#!/bin/sh\n")

        os.chmod(os.path.join(os.path.dirname(path), "nothing.sh"), 0o777)
        
        with open(os.path.join(os.path.dirname(path), 'Cargo.toml'), 'r') as f:
            content = f.readlines()
            
        with open(os.path.join(os.path.dirname(path), 'Cargo.toml'), 'w') as f:
            for line in content:
                f.write(line)
                if line.startswith('[dependencies]'):
                    f.write('image = "0.20"\n')

        args = ['cargo',
                'test',
                '-q',
                '--target=x86_64-unknown-linux-gnu',
                '--release',
                '--examples',
                '--manifest-path',
                path,
                '--features=fail-on-warnings',
                '--no-fail-fast']

        print(">>> Compiling examples, this will take a while...")

        self.execute(cookie, args)

def run(root_dir):
    return RustExamplesTester(root_dir, None).run()

if __name__ == '__main__':
    run(os.getcwd())
