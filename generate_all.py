#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import socket
import common

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

path = os.getcwd()
bindings = []

for d in os.listdir(path):
    if os.path.isdir(d):
        if d not in ['configs', 'stubs', '.git', '__pycache__', '.vscode', 'embedded_c']:
            bindings.append(d)
            sys.path.append(os.path.join(path, d))

bindings = sorted(bindings)

# bindings
if 'bindings' in actions and socket.gethostname() != 'tinkerforge.com':
    for binding in bindings:
        if binding in ['tcpip', 'modbus', 'stubs', 'tvpl']:
            continue

        module = __import__('generate_{0}_bindings'.format(binding))
        print('\nGenerating bindings for {0}:'.format(binding))
        module.generate(os.path.join(path, binding))

# examples
if 'examples' in actions and socket.gethostname() != 'tinkerforge.com':
    for binding in bindings:
        if binding in ['tcpip', 'modbus', 'stubs', 'tvpl', 'saleae']:
            continue

        try:
            module = __import__('generate_{0}_examples'.format(binding))
        except ImportError:
            print("\nNo example generator for {0}".format(binding))
            continue

        print('\nGenerating examples for {0}:'.format(binding))
        module.generate(os.path.join(path, binding))

# doc
if 'doc' in actions:
    for binding in bindings:
        if binding in ['json', 'stubs', 'tvpl', 'saleae']:
            continue

        module = __import__('generate_{0}_doc'.format(binding))

        for lang in ['en', 'de']:
            print('\nGenerating {0} documentation for {1}:'.format(lang, binding))
            module.generate(os.path.join(path, binding), lang)

# zip
if 'zip' in actions and socket.gethostname() != 'tinkerforge.com':
    for binding in bindings:
        if binding in ['tcpip', 'modbus', 'stubs', 'tvpl']:
            continue

        module = __import__('generate_{0}_zip'.format(binding))
        print('\nGenerating ZIP for {0}:'.format(binding))
        module.generate(os.path.join(path, binding))

print('')
print('>>> Done <<<')
