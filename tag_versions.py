#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import subprocess
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

from generators import common

def main():
    bindings = []

    for binding in sorted(os.listdir(generators_dir)):
        if not os.path.isdir(binding) or os.path.exists(os.path.join(generators_dir, binding, 'skip_tag_versions')):
            continue

        if binding not in ['.git', '.m2', '.vscode', '__pycache__', 'configs', 'docker']:
            bindings.append(binding)

    for binding in bindings:
        path = os.path.join(generators_dir, binding)
        version = common.get_changelog_version(path)
        tag = '{0}-{1}.{2}.{3}'.format(binding, *version)
        args = ['git', 'tag', tag]

        print('=== Tagging {0} ======'.format(tag))

        subprocess.call(args)

if __name__ == '__main__':
    main()
