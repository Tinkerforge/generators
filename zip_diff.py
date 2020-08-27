#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ZIP Diff
Copyright (C) 2017-2020 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>

zip_diff.py: Tool for diffing API bindings ZIP files

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

argv = sys.argv[1:]

for path in [os.path.expanduser('~/.zip_diffrc'), './.zip_diffrc']:
    if os.path.exists(path):
        with open(path, 'r') as f:
            argv += shlex.split(f.read(), comments=True)

parser = argparse.ArgumentParser()

parser.add_argument('--prepare', action='store_true', help='prepare unreleased zip as old diff input')
parser.add_argument('--unreleased', action='store_true', help='use unreleased zip as old diff input')
parser.add_argument('--diff-tool', default='geany', help='program to open diff with')
parser.add_argument('bindings', nargs='?', help='bindings to create diff for')

args = parser.parse_args(argv)

diff_tool = args.diff_tool

ignored = ['configs', 'stubs', 'modbus', 'tcpip', 'tvpl', '.git', '__pycache__', '.vscode']

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

        zip_path = os.path.join(path, 'zip')
        zip_old_path = os.path.join(path, 'zip_old')

        if not os.path.isdir(zip_path):
            print('skipping {0}, no zip directory'.format(d))
            continue

        print('preparing ' + d)

        if os.path.isdir(zip_old_path):
            shutil.rmtree(zip_old_path)

        shutil.copytree(zip_path, zip_old_path)
else:
    c_like_header1 = re.compile(r'^@@ -1,8 \+1,8 @@\n' + \
    ' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n' + \
    '- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
    '\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
    '  \*                                                           \*\n' + \
    '  \* .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
    '  \*                                                           \*\n' + \
    '  \* If you have a bugfix for this file and want to commit it, \*\n' + \
    '  \* please fix the bug in the generator\. You can find a link  \*\n' + \
    '  \* to the generators git repository on tinkerforge\.com       \*\n$')

    c_like_header2 = re.compile(r'^@@ -1,10 \+1,10 @@\n' + \
    ' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n' + \
    '- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
    '\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
    '  \*                                                           \*\n' + \
    '- \* .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
    '\+ \* .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
    '  \*                                                           \*\n' + \
    '  \* If you have a bugfix for this file and want to commit it, \*\n' + \
    '  \* please fix the bug in the generator\. You can find a link  \*\n' + \
    '  \* to the generators git repository on tinkerforge\.com       \*\n' + \
    '  \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*/\n' + \
    ' \n$')

    delphi_header1 = re.compile(r'^@@ -1,8 \+1,8 @@\n' + \
    ' {\n' + \
    '-  This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.\n' + \
    '\+  This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.\n' + \
    ' \n' + \
    '   Delphi/Lazarus Bindings Version 2\.[0-9]+\.[0-9]+\n' + \
    ' \n' + \
    '   If you have a bugfix for this file and want to commit it,\n' + \
    '   please fix the bug in the generator\. You can find a link\n' + \
    '   to the generators git on tinkerforge\.com\n$')

    delphi_header2 = re.compile(r'^@@ -1,10 \+1,10 @@\n' + \
    ' {\n' + \
    '-  This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.\n' + \
    '\+  This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.\n' + \
    ' \n' + \
    '-  Delphi/Lazarus Bindings Version 2\.[0-9]+\.[0-9]+\n' + \
    '\+  Delphi/Lazarus Bindings Version 2\.[0-9]+\.[0-9]+\n' + \
    ' \n' + \
    '   If you have a bugfix for this file and want to commit it,\n' + \
    '   please fix the bug in the generator\. You can find a link\n' + \
    '   to the generators git on tinkerforge\.com\n' + \
    ' }\n' + \
    ' \n$')

    javascript_header1 = re.compile(r'^@@ -[0-9]+,8 \+[0-9]+,8 @@\n' + \
    ' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n' + \
    '- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
    '\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
    '  \*                                                           \*\n' + \
    '  \* JavaScript Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
    '  \*                                                           \*\n' + \
    '  \* If you have a bugfix for this file and want to commit it, \*\n' + \
    '  \* please fix the bug in the generator\. You can find a link  \*\n' + \
    '  \* to the generators git repository on tinkerforge\.com       \*\n$')

    javascript_header2 = re.compile(r'^@@ -[0-9]+,10 \+[0-9]+,10 @@\n' + \
    ' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n' + \
    '- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
    '\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
    '  \*                                                           \*\n' + \
    '- \* JavaScript Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
    '\+ \* JavaScript Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
    '  \*                                                           \*\n' + \
    '  \* If you have a bugfix for this file and want to commit it, \*\n' + \
    '  \* please fix the bug in the generator\. You can find a link  \*\n' + \
    '  \* to the generators git repository on tinkerforge\.com       \*\n' + \
    '  \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*/\n' + \
    ' \n$')

    javascript_header3 = re.compile(r'^@@ -[0-9]+,13 \+[0-9]+,13 @@\n' + \
    ' }\n' + \
    ' \n' + \
    ' module\.exports = Brick[A-Za-z0-9]+;\n' + \
    ' \n' + \
    ' },{"\./Device":[0-9]+,"\./IPConnection":[0-9]+}\],[0-9]+:\[function\(require,module,exports\){\n' + \
    ' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n' + \
    '- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
    '\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
    '  \*                                                           \*\n' + \
    '  \* JavaScript Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
    '  \*                                                           \*\n' + \
    '  \* If you have a bugfix for this file and want to commit it, \*\n' + \
    '  \* please fix the bug in the generator\. You can find a link  \*\n' + \
    '  \* to the generators git repository on tinkerforge\.com       \*\n$')

    javascript_header4 = re.compile(r'^@@ -[0-9]+,15 \+[0-9]+,15 @@\n' + \
    ' }\n' + \
    ' \n' + \
    ' module\.exports = Brick[A-Za-z0-9]+;\n' + \
    ' \n' + \
    ' },{"\./Device":[0-9]+,"\./IPConnection":[0-9]+}\],[0-9]+:\[function\(require,module,exports\){\n' + \
    ' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n' + \
    '- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
    '\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
    '  \*                                                           \*\n' + \
    '- \* JavaScript Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
    '\+ \* JavaScript Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
    '  \*                                                           \*\n' + \
    '  \* If you have a bugfix for this file and want to commit it, \*\n' + \
    '  \* please fix the bug in the generator\. You can find a link  \*\n' + \
    '  \* to the generators git repository on tinkerforge\.com       \*\n' + \
    '  \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*/\n' + \
    ' \n$')

    perl_header1 = re.compile(r'^@@ -1,8 \+1,8 @@\n' + \
    ' #############################################################\n' + \
    '-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
    '\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
    ' #                                                           #\n' + \
    ' # Perl Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
    ' #                                                           #\n' + \
    ' # If you have a bugfix for this file and want to commit it, #\n' + \
    ' # please fix the bug in the generator\. You can find a link  #\n' + \
    ' # to the generators git repository on tinkerforge\.com       #\n$')

    perl_header2 = re.compile(r'^@@ -1,10 \+1,10 @@\n' + \
    ' #############################################################\n' + \
    '-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
    '\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
    ' #                                                           #\n' + \
    '-# Perl Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
    '\+# Perl Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
    ' #                                                           #\n' + \
    ' # If you have a bugfix for this file and want to commit it, #\n' + \
    ' # please fix the bug in the generator\. You can find a link  #\n' + \
    ' # to the generators git repository on tinkerforge\.com       #\n' + \
    ' #############################################################\n' + \
    ' \n$')

    php_header1 = re.compile(r'^@@ -1,10 \+1,10 @@\n' + \
    ' <\?php\n' + \
    ' \n' + \
    ' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\\n' + \
    '- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
    '\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
    '  \*                                                           \*\n' + \
    '  \* PHP Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
    '  \*                                                           \*\n' + \
    '  \* If you have a bugfix for this file and want to commit it, \*\n' + \
    '  \* please fix the bug in the generator\. You can find a link  \*\n' + \
    '  \* to the generators git repository on tinkerforge\.com       \*\n$')

    php_header2 = re.compile(r'^@@ -1,12 \+1,12 @@\n' + \
    ' <\?php\n' + \
    ' \n' + \
    ' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\\n' + \
    '- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
    '\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
    '  \*                                                           \*\n' + \
    '- \* PHP Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
    '\+ \* PHP Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
    '  \*                                                           \*\n' + \
    '  \* If you have a bugfix for this file and want to commit it, \*\n' + \
    '  \* please fix the bug in the generator\. You can find a link  \*\n' + \
    '  \* to the generators git repository on tinkerforge\.com       \*\n' + \
    '  \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*/\n' + \
    ' \n$')

    python_header1 = re.compile(r'^@@ -1,9 \+1,9 @@\n' + \
    ' # -\*- coding: utf-8 -\*-\n' + \
    ' #############################################################\n' + \
    '-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
    '\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
    ' #                                                           #\n' + \
    ' # Python Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
    ' #                                                           #\n' + \
    ' # If you have a bugfix for this file and want to commit it, #\n' + \
    ' # please fix the bug in the generator\. You can find a link  #\n' + \
    ' # to the generators git repository on tinkerforge\.com       #\n$')

    python_header2 = re.compile(r'^@@ -1,11 \+1,11 @@\n' + \
    ' # -\*- coding: utf-8 -\*-\n' + \
    ' #############################################################\n' + \
    '-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
    '\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
    ' #                                                           #\n' + \
    '-# Python Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
    '\+# Python Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
    ' #                                                           #\n' + \
    ' # If you have a bugfix for this file and want to commit it, #\n' + \
    ' # please fix the bug in the generator\. You can find a link  #\n' + \
    ' # to the generators git repository on tinkerforge\.com       #\n' + \
    ' #############################################################\n' + \
    ' \n$')

    ruby_header1 = re.compile(r'^@@ -1,9 \+1,9 @@\n' + \
    ' # -\*- ruby encoding: utf-8 -\*-\n' + \
    ' #############################################################\n' + \
    '-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
    '\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
    ' #                                                           #\n' + \
    ' # Ruby Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
    ' #                                                           #\n' + \
    ' # If you have a bugfix for this file and want to commit it, #\n' + \
    ' # please fix the bug in the generator\. You can find a link  #\n' + \
    ' # to the generators git repository on tinkerforge\.com       #\n$')

    ruby_header2 = re.compile(r'^@@ -1,11 \+1,11 @@\n' + \
    ' # -\*- ruby encoding: utf-8 -\*-\n' + \
    ' #############################################################\n' + \
    '-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
    '\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
    ' #                                                           #\n' + \
    '-# Ruby Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
    '\+# Ruby Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
    ' #                                                           #\n' + \
    ' # If you have a bugfix for this file and want to commit it, #\n' + \
    ' # please fix the bug in the generator\. You can find a link  #\n' + \
    ' # to the generators git repository on tinkerforge\.com       #\n' + \
    ' #############################################################\n' + \
    ' \n$')

    tmp = tempfile.mkdtemp()

    print('using tmpdir ' + tmp)

    for b in bindings:
        path = os.path.join(generators_dir, b)

        if not os.path.isdir(path):
            continue

        if not os.path.isdir(os.path.join(path, 'zip')):
            print('skipping {0}, no zip directory'.format(b))
            continue

        version = common.get_changelog_version(path)

        if args.unreleased:
            if not os.path.isdir(os.path.join(path, 'zip_old')):
                print('skipping {0}, no zip_old directory'.format(b))
                continue

            print('diffing ' + b)

            shutil.copytree(os.path.join(path, 'zip_old'), os.path.join(tmp, 'old_{0}'.format(b)))
        else:
            print('diffing ' + b)

            if os.system('bash -ce "curl -sf https://download.tinkerforge.com/bindings/{0}/tinkerforge_{0}_bindings_latest.zip -o {1}/old_{0}.zip"'.format(b, tmp)) != 0:
                print('download latest.zip failed')
                sys.exit(1)

            if os.system('bash -ce "pushd {1} > /dev/null && unzip -q -d old_{0} old_{0}.zip && popd > /dev/null"'.format(b, tmp)) != 0:
                print('unzip latest.zip failed')
                sys.exit(1)

        if os.system('bash -ce "cp {0}/tinkerforge_{1}_bindings_{3}_{4}_{5}.zip {2} && pushd {2} > /dev/null && unzip -q -d new_{1} tinkerforge_{1}_bindings_{3}_{4}_{5}.zip && popd > /dev/null"'.format(path, b, tmp, *version)) != 0:
            print('copy and unzip new.zip failed')
            sys.exit(1)

        if os.system('bash -c "pushd {1} > /dev/null && diff -ru6 old_{0}/ new_{0}/ > diff_{0}.diff; popd > /dev/null"'.format(b, tmp)) != 0:
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

                if not c_like_header1.match(hunk) and \
                   not c_like_header2.match(hunk) and \
                   not delphi_header1.match(hunk) and \
                   not delphi_header2.match(hunk) and \
                   not javascript_header1.match(hunk) and \
                   not javascript_header2.match(hunk) and \
                   not javascript_header3.match(hunk) and \
                   not javascript_header4.match(hunk) and \
                   not perl_header1.match(hunk) and \
                   not perl_header2.match(hunk) and \
                   not php_header1.match(hunk) and \
                   not php_header2.match(hunk) and \
                   not python_header1.match(hunk) and \
                   not python_header2.match(hunk) and \
                   not ruby_header1.match(hunk) and \
                   not ruby_header2.match(hunk):
                    filtered_lines += lines
                else:
                    filtered_lines += [lines[0].rstrip() + ' // dropped header hunk\n']

            if len(filtered_lines) == 0:
                continue

            if len(filtered_lines) == 4 and \
               filtered_lines[0].startswith('diff -ru6 ') and \
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
