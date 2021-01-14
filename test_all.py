#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import re
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

def modify_items(kind, active_items, all_items, action, item):
    if item == 'all':
        if action == '+':
            active_items |= set(all_items)
        elif action == '-':
            active_items -= set(all_items)
        else:
            print('error: invalid --{0}s item: {1}'.format(kind, action + item))
            return None
    else:
        if item not in all_items:
            print('error: unknown {0}: {1}'.format(kind, item))
            return None

        if action == '+':
            active_items.add(item)
        elif action == '-':
            active_items.remove(item)
        elif action == '>=':
            active_items |= set(all_items[all_items.index(item):])
        elif action == '>':
            active_items |= set(all_items[all_items.index(item) + 1:])
        elif action == '<=':
            active_items |= set(all_items[:all_items.index(item) + 1])
        elif action == '<':
            active_items |= set(all_items[:all_items.index(item)])
        else:
            assert False, action

    return active_items

# FIXME: test custom bindings too

def main(args):
    all_bindings = []

    for binding in os.listdir(generators_dir):
        if not os.path.isdir(binding) or os.path.exists(os.path.join(generators_dir, binding, 'skip_test_all')):
            continue

        if binding not in ['.git', '.m2', '.vscode', '__pycache__', 'configs', 'docker']:
            all_bindings.append(binding)

    all_bindings = sorted(all_bindings)
    active_bindings = set(all_bindings)

    if args.bindings != None:
        for item in args.bindings[0].split(','):
            if len(item) == 0:
                print('error: empty --bindings item')
                return 1

            m = re.match(r'^(\+|-|>=|>|<=|<)(.*)$', item)

            if m == None:
                print('error: invalid --bindings item: {0}'.format(item))
                return 1

            action = m.group(1)
            binding = m.group(2)
            active_bindings = modify_items('binding', active_bindings, all_bindings, action, binding)

            if active_bindings == None:
                return 1

    for binding in all_bindings:
        if binding not in active_bindings:
            continue

        print('\033[01;32m>>> running tests for {0} bindings\033[0m'.format(binding))

        try:
            module = importlib.import_module('generators.{0}.test_{0}_bindings'.format(binding))
        except ImportError: # FIXME: Python 3.6 has ModuleNotFoundError, which would be better to use here, but Debian Stretch has only Python 3.5
            print('\033[01;36m### tests missing\033[0m')
        else:
            success = module.test(os.path.join(generators_dir, binding))

            if not isinstance(success, bool):
                print('error: test_{0}_bindings.py returns wrong type from its test() function'.format(binding))

            if not success:
                sys.exit(1)

    print('\033[01;35m>>> done\033[0m')

if __name__ == '__main__':
    def add_arguments(parser):
        parser.add_argument('-b', '--bindings', nargs=1, help='comma separated list of bindings, each prefixed by +/-')

    sys.exit(main(common.dockerize('', __file__, add_arguments=add_arguments)))
