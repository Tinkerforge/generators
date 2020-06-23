#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.hexversion < 0x3050000:
    print('Python >= 3.5 required')
    sys.exit(1)

import os
import importlib.util

generators_dir = os.path.dirname(os.path.realpath(__file__))

def create_generators_module():
    generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
    generators_module = importlib.util.module_from_spec(generators_spec)

    generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

positive = set()
negative = set()
bindings = set()

for arg in sys.argv[1:]:
    if arg.startswith('-'):
        negative.add(arg[1:])
    else:
        positive.add(arg)

for d in os.listdir(generators_dir):
    if os.path.isdir(d):
        if d not in ['configs', '.git', '__pycache__', '.vscode']:
            bindings.add(d)

if not positive <= bindings or not negative <= bindings:
    print('Error: Invalid argument')

if len(positive) > 0 and len(negative) > 0:
    print('Error: Cannot mix positive and negative arguments')

if len(positive) > 0:
    bindings = positive
else:
    bindings -= negative

bindings = sorted(list(bindings))

for binding in bindings:
    if binding in ['stubs', 'tvpl']:
        continue

    module = importlib.import_module('generators.{0}.test_{0}_bindings'.format(binding))

    print("### testing {0} bindings:".format(binding))

    success = module.run(os.path.join(generators_dir, binding))

    if not isinstance(success, bool):
        raise Exception('test_{0}_bindings.py returns wrong type from its run() function'.format(binding))

    if not success:
        sys.exit(1)

print('')
print('>>> Done <<<')
