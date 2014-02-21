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
    module = __import__('compile_{0}_examples'.format(binding))

    print(">>> compiling examples for {0}:".format(binding))

    rc = module.run(path_binding)

    if rc != 0:
        sys.exit(rc)

print('>>> Done <<<')
