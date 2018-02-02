#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

path = os.getcwd()
positive = set()
negative = set()
bindings = set()

for arg in sys.argv[1:]:
    if arg.startswith('-'):
        negative.add(arg[1:])
    else:
        positive.add(arg)

for d in os.listdir(path):
    if os.path.isdir(d):
        if d not in ['configs', '.git', '__pycache__']:
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
    if binding in ['tcpip', 'modbus', 'json', 'tvpl']:
        continue

    path_binding = os.path.join(path, binding)
    sys.path.append(path_binding)
    module = __import__('test_{0}_bindings'.format(binding))

    print("### testing {0} bindings:".format(binding))

    success = module.run(path_binding)

    if not isinstance(success, bool):
        raise Exception('test_{0}_bindings.py returns wrong type from its run() function'.format(binding))

    if not success:
        sys.exit(1)

print('')
print('>>> Done <<<')
