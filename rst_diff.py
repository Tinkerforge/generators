#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import re
import tempfile
import shutil
import argparse
import shlex
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

argv = sys.argv[1:]

for path in [os.path.expanduser('~/.rst_diffrc'), './.rst_diffrc']:
    if os.path.exists(path):
        with open(path, 'r') as f:
            argv += shlex.split(f.read(), comments=True)

parser = argparse.ArgumentParser()

parser.add_argument('--prepare', action='store_true', help='prepare current rst as old diff input')
parser.add_argument('--diff-tool', default='geany', help='program to open diff file with')
parser.add_argument('bindings', nargs='?', help='bindings to create diff file for')

args = parser.parse_args(argv)

diff_tool = args.diff_tool

if args.prepare:
    for d in os.listdir('.'):
        if not os.path.isdir(d):
            continue

        if d in ['configs', 'stubs', 'json', 'tvpl', '.git', '__pycache__', '.vscode']:
            continue

        doc_path = os.path.join(d, 'doc')
        doc_old_path = os.path.join(d, 'doc_old')

        if not os.path.isdir(doc_path):
            continue

        if os.path.isdir(doc_old_path):
            shutil.rmtree(doc_old_path)

        shutil.copytree(doc_path, doc_old_path)
else:
    if args.bindings != None:
        bindings = args.bindings.rstrip('/')
    else:
        parent_dir, bindings = os.path.split(os.getcwd())

        if parent_dir != generators_dir:
            print('error: wrong working directory, cannot auto-detect bindings')
            sys.exit(1)

    base = os.path.join(generators_dir, bindings)
    tmp = tempfile.mkdtemp()

    if os.system('bash -cx "pushd {0} && diff -U 15 -r doc_old/ doc/ > {1}/diff1.diff; popd"'.format(base, tmp)) != 0:
        print('diff old vs new failed')
        sys.exit(1)

    with open(os.path.join(tmp, 'diff1.diff'), 'r') as f:
        diffs = [[[]]] # list of diffs as lists of lines

        for line in f.readlines():
            if line.startswith('diff ') or line[0] not in ['@', '-', '+', ' ']:
                diffs.append([[]])

            if line.startswith('@@ '):
                diffs[-1].append([])

            diffs[-1][-1].append(line)

    header = re.compile(r"""^@@ -1,6 \+1,6 @@
 \.\.
  #############################################################
- # This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #
\+ # This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #
  #                                                           #
  # If you have a bugfix for this file and want to commit it, #
  # please fix the bug in the generator\. You can find a link  #$""")

    filtered = []

    for diff in diffs:
        filtered_lines = []

        for lines in diff:
            if len(lines) == 0:
                continue

            hunk = ''.join(lines)

            if not header.match(hunk):
                filtered_lines += lines
            else:
                filtered_lines += [lines[0].rstrip() + ' // dropped header hunk\n']

        if len(filtered_lines) == 0:
            continue

        if len(filtered_lines) == 4 and \
           filtered_lines[0].startswith('diff -U 15 -r ') and \
           filtered_lines[1].startswith('--- ') and \
           filtered_lines[2].startswith('+++ ') and \
           filtered_lines[3].endswith('// dropped header hunk\n'):
            filtered += [filtered_lines[0].rstrip() + ' // dropped header diff\n']
        else:
            filtered += filtered_lines

    with open(os.path.join(tmp, 'diff2.diff'), 'w') as f:
        f.writelines(filtered)

    if os.system('bash -c "{} {}/diff2.diff"'.format(diff_tool, tmp)) != 0:
        print('{} diff.diff failed'.format(diff_tool))
        sys.exit(1)
