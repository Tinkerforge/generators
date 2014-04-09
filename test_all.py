#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

path = os.getcwd()
bindings = []
for d in os.listdir(path):
    if os.path.isdir(d):
        if not d in ('configs', '.git', '__pycache__'):
            bindings.append(d)
bindings = sorted(bindings)

for binding in bindings:
    if binding in ('tcpip', 'modbus'):
        continue

    path_binding = '{0}/{1}'.format(path, binding)
    sys.path.append(path_binding)
    module = __import__('test_{0}_bindings'.format(binding))

    print("### testing {0} bindings:".format(binding))

    success = module.run(path_binding)

    if type(success) != bool:
        raise Exception('test_{0}_bindings.py returns wrong type from its run() function'.format(binding))

    if not success:
        sys.exit(1)

print('')
print('>>> Done <<<')
