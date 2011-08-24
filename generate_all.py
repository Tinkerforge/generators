#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

path = os.getcwd()
bindings = []
for d in os.listdir(path):
    if os.path.isdir(d):
        if not d in ('configs', '.git'):
            bindings.append(d)

for binding in bindings:
    path_binding = '{0}/{1}'.format(path, binding)
    sys.path.append(path_binding)
    module = __import__('generate_{0}_bindings'.format(binding))
    print("\nGenerating bindings for {0}:".format(binding))
    module.generate(path_binding)

for binding in bindings:
    path_binding = '{0}/{1}'.format(path, binding)
    sys.path.append(path_binding)
    module = __import__('generate_{0}_doc'.format(binding))
    print("\nGenerating documentation for {0}:".format(binding))
    module.generate(path_binding)

