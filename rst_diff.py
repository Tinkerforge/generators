#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
rST Diff
Copyright (C) 2019-2020 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2019-2020 Erik Fleckstein <erik@tinkerforge.com>

rst_diff.py: Tool for diffing API bindings documentation rST files

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

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

def main():
    argv = sys.argv[1:]

    for path in [os.path.expanduser('~/.rst_diffrc'), './.rst_diffrc']:
        if os.path.exists(path):
            with open(path, 'r') as f:
                argv += shlex.split(f.read(), comments=True)

    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--prepare', action='store_true', help='prepare current rst as old diff input')
    parser.add_argument('-d', '--diff-tool', default='geany', help='program to open diff file with')
    parser.add_argument('bindings', nargs='?', help='bindings to create diff file for')

    args = parser.parse_args(argv)

    diff_tool = args.diff_tool

    ignored = ['configs', 'stubs', 'json', 'saleae', 'tvpl', '.git', '__pycache__', '.vscode']

    if args.bindings != None:
        b = args.bindings.rstrip('/')

        if not os.path.isdir(os.path.join(generators_dir, b)):
            print('error: {0} is not a directory'.format(b))
            sys.exit(1)

        bindings = [b]
    elif os.path.samefile(generators_dir, os.getcwd()):
        bindings = sorted([x for x in os.listdir(generators_dir) if x not in ignored])
    else:
        parent_dir, b = os.path.split(os.getcwd())

        if parent_dir != generators_dir:
            print('error: wrong working directory, cannot auto-detect bindings')
            sys.exit(1)

        bindings = [b]

    if args.prepare:
        for b in bindings:
            path = os.path.join(generators_dir, b)

            if not os.path.isdir(path):
                continue

            doc_path = os.path.join(path, 'doc')
            doc_old_path = os.path.join(path, 'doc_old')

            if not os.path.isdir(doc_path):
                print('skipping {0}, no doc directory'.format(b))
                continue

            print('preparing ' + b)

            if os.path.isdir(doc_old_path):
                shutil.rmtree(doc_old_path)

            shutil.copytree(doc_path, doc_old_path)
    else:
        rst_header = re.compile(r"""^@@ -1,6 \+1,6 @@
     \.\.
      #############################################################
    - # This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #
    \+ # This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #
      #                                                           #
      # If you have a bugfix for this file and want to commit it, #
      # please fix the bug in the generator\. You can find a link  #$""")

        tmp = tempfile.mkdtemp()

        print('using tmpdir ' + tmp)

        for b in bindings:
            path = os.path.join(generators_dir, b)

            if not os.path.isdir(path):
                continue

            if not os.path.isdir(os.path.join(path, 'doc')):
                print('skipping {0}, no doc directory'.format(b))
                continue

            if not os.path.isdir(os.path.join(path, 'doc_old')):
                print('skipping {0}, no doc_old directory'.format(b))
                continue

            print('diffing ' + b)

            if os.system('bash -c "pushd {0} > /dev/null && diff -ru15 doc_old/ doc/ > {1}/diff_{2}.diff; popd > /dev/null"'.format(path, tmp, b)) != 0:
                print('diff old vs new failed')
                sys.exit(1)

            with open(os.path.join(tmp, 'diff_{0}.diff'.format(b)), 'r') as f:
                diffs = [[[]]] # list of diffs as lists of lines

                for line in f.readlines():
                    if line.startswith('diff ') or line[0] not in ['@', '-', '+', ' ']:
                        diffs.append([[]])

                    if line.startswith('@@ '):
                        diffs[-1].append([])

                    diffs[-1][-1].append(line)

            filtered = []

            for diff in diffs:
                filtered_lines = []

                for lines in diff:
                    if len(lines) == 0:
                        continue

                    hunk = ''.join(lines)

                    if not rst_header.match(hunk):
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

            with open(os.path.join(tmp, 'diff.diff'), 'a') as f:
                f.writelines(filtered)

        if os.system('bash -ce "{0} {1}/diff.diff"'.format(diff_tool, tmp)) != 0:
            print('{0} diff.diff failed'.format(diff_tool))
            sys.exit(1)

if __name__ == '__main__':
    main()
