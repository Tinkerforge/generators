#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import socket
import importlib.util
import importlib.machinery

generators_dir = os.path.dirname(os.path.realpath(__file__))

def create_generators_module():
    if sys.hexversion < 0x3050000:
        generators_module = importlib.machinery.SourceFileLoader('generators', os.path.join(generators_dir, '__init__.py')).load_module()
    else:
        generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
        generators_module = importlib.util.module_from_spec(generators_spec)

        generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

positive = set()
negative = set()
actions = {'bindings', 'examples', 'doc', 'zip'}

for arg in sys.argv[1:]:
    if arg.startswith('-'):
        negative.add(arg[1:])
    else:
        positive.add(arg)

if not positive.issubset(actions) or not negative.issubset(actions):
    print('Error: Invalid argument')

if len(positive) > 0 and len(negative) > 0:
    print('Error: Cannot mix positive and negative arguments')

if len(positive) > 0:
    actions = positive
else:
    actions -= negative

# exclude examples if not explicitly specified
if 'examples' not in positive and 'examples' in actions:
    actions.remove('examples')

bindings = []

for d in os.listdir(generators_dir):
    if os.path.isdir(d):
        if d not in ['configs', 'stubs', '.git', '__pycache__', '.vscode', 'openhab']:
            bindings.append(d)

bindings = sorted(bindings)

# bindings
if 'bindings' in actions and socket.gethostname() != 'tinkerforge.com':
    for binding in bindings:
        if binding in ['tcpip', 'modbus', 'stubs', 'tvpl']:
            continue

        module = importlib.import_module('generators.{0}.generate_{0}_bindings'.format(binding))

        print('\nGenerating bindings for {0}:'.format(binding))

        module.generate(os.path.join(generators_dir, binding))

# examples
if 'examples' in actions and socket.gethostname() != 'tinkerforge.com':
    for binding in bindings:
        if binding in ['tcpip', 'modbus', 'stubs', 'tvpl', 'saleae']:
            continue

        try:
            module = importlib.import_module('generators.{0}.generate_{0}_examples'.format(binding))
        except ImportError:
            print("\nNo example generator for {0}".format(binding))
            continue

        print('\nGenerating examples for {0}:'.format(binding))

        module.generate(os.path.join(generators_dir, binding))

# doc
if 'doc' in actions:
    for binding in bindings:
        if binding in ['json', 'stubs', 'tvpl', 'saleae']:
            continue

        module = importlib.import_module('generators.{0}.generate_{0}_doc'.format(binding))

        for lang in ['en', 'de']:
            print('\nGenerating {0} documentation for {1}:'.format(lang, binding))

            module.generate(os.path.join(generators_dir, binding), lang)

# zip
if 'zip' in actions and socket.gethostname() != 'tinkerforge.com':
    for binding in bindings:
        if binding in ['tcpip', 'modbus', 'stubs', 'tvpl']:
            continue

        module = importlib.import_module('generators.{0}.generate_{0}_zip'.format(binding))

        print('\nGenerating ZIP for {0}:'.format(binding))

        module.generate(os.path.join(generators_dir, binding))

print('')
print('>>> Done <<<')
