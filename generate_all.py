#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import socket
import common

path = os.getcwd()
bindings = []
for d in os.listdir(path):
    if os.path.isdir(d):
        if not d in ('configs', '.git', '__pycache__'):
            bindings.append(d)

# bindings
for binding in bindings:
    if binding in ('tcpip', 'modbus'):
        continue

    path_binding = '{0}/{1}'.format(path, binding)
    sys.path.append(path_binding)
    module = __import__('generate_{0}_bindings'.format(binding))
    print("\nGenerating bindings for {0}:".format(binding))
    module.generate(path_binding)

# doc
for binding in bindings:
    path_binding = '{0}/{1}'.format(path, binding)
    sys.path.append(path_binding)
    module = __import__('generate_{0}_doc'.format(binding))
    for lang in ['en', 'de']:
        print("\nGenerating '{0}' documentation for {1}:".format(lang, binding))
        module.generate(path_binding, lang)

# zip
if socket.gethostname() != 'tinkerforge.com':
    for binding in bindings:
        if binding in ('tcpip', 'modbus'):
            continue

        path_binding = '{0}/{1}'.format(path, binding)
        sys.path.append(path_binding)
        module = __import__('generate_{0}_zip'.format(binding))
        print("\nGenerating ZIP for {0}:".format(binding))
        module.generate(path_binding)
