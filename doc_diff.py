#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Documentation Diff
Copyright (C) 2019-2021 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2019-2020 Erik Fleckstein <erik@tinkerforge.com>

doc_diff.py: Tool for diffing API bindings documentation rST files

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

    # check old .rst_diffrc file for backward compatibility
    for path in [os.path.expanduser('~/.doc_diffrc'), './.doc_diffrc', os.path.expanduser('~/.rst_diffrc'), './.rst_diffrc']:
        if os.path.exists(path):
            with open(path, 'r') as f:
                argv += shlex.split(f.read(), comments=True)

    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--prepare', action='store_true', help='prepare current doc as old diff input')
    parser.add_argument('-d', '--diff-tool', default='./diff_view.py', help='program to open diff file with')
    parser.add_argument('-b', '--bindings', nargs=1, help='comma separated list of bindings, each prefixed by +/-/>=/>/<=/<')

    args = parser.parse_args(argv)

    all_bindings = []

    for binding in os.listdir(generators_dir):
        if not os.path.isdir(binding) or os.path.exists(os.path.join(generators_dir, binding, 'skip_doc_diff')):
            continue

        if binding not in ['.git', '.m2', '.vscode', '__pycache__', 'configs', 'docker']:
            all_bindings.append(binding)

    all_bindings = sorted(all_bindings)
    active_bindings = set(all_bindings)

    if args.bindings != None:
        try:
            active_bindings = common.apply_item_changes('binding', active_bindings, all_bindings, args.bindings[0].split(','))
        except Exception as e:
            print('error: {0}'.format(e))
            return 1

    if args.prepare:
        for binding in all_bindings:
            if binding not in active_bindings:
                continue

            if not os.path.isdir(path):
                print('skipping {0}, no {0} directory'.format(binding))
                continue

            doc_path = os.path.join(path, 'doc')
            doc_old_path = os.path.join(path, 'doc_old')

            if not os.path.isdir(doc_path):
                print('skipping {0}, no doc directory'.format(binding))
                continue

            print('preparing ' + binding)

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

        for binding in all_bindings:
            if binding not in active_bindings:
                continue

            path = os.path.join(generators_dir, binding)

            if not os.path.isdir(path):
                print('skipping {0}, no {0} directory'.format(binding))
                continue

            if not os.path.isdir(os.path.join(path, 'doc')):
                print('skipping {0}, no doc directory'.format(binding))
                continue

            if not os.path.isdir(os.path.join(path, 'doc_old')):
                print('skipping {0}, no doc_old directory'.format(binding))
                continue

            print('diffing ' + binding)

            if os.system('bash -c "pushd {0} > /dev/null && diff -ru15 doc_old/ doc/ > {1}/diff_{2}.diff; popd > /dev/null"'.format(path, tmp, binding)) != 0:
                print('error: diff old vs new failed')
                return 1

            with open(os.path.join(tmp, 'diff_{0}.diff'.format(binding)), 'r') as f:
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

        if os.system('bash -ce "{0} {1}/diff.diff"'.format(args.diff_tool, tmp)) != 0:
            print('{0} diff.diff failed'.format(args.diff_tool))
            return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
