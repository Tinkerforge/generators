#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ZIP Diff
Copyright (C) 2017-2021 Matthias Bolte <matthias@tinkerforge.com>
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

def main():
    argv = sys.argv[1:]

    for path in [os.path.expanduser('~/.zip_diffrc'), './.zip_diffrc']:
        if os.path.exists(path):
            with open(path, 'r') as f:
                argv += shlex.split(f.read(), comments=True)

    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--prepare', action='store_true', help='prepare unreleased zip as old diff input')
    parser.add_argument('-u', '--unreleased', action='store_true', help='use unreleased zip as old diff input')
    parser.add_argument('-d', '--diff-tool', default='./diff_view.py', help='program to open diff with')
    parser.add_argument('-b', '--bindings', nargs=1, help='comma separated list of bindings, each prefixed by +/-/>=/>/<=/<')
    parser.add_argument('-s', '--ignore-space-change', action='store_true', help='ignore changes in the amount of white space')

    args = parser.parse_args(argv)

    all_bindings = []

    for binding in os.listdir(generators_dir):
        if not os.path.isdir(os.path.join(generators_dir, binding)) or os.path.exists(os.path.join(generators_dir, binding, 'skip_zip_diff')):
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
    else:
        binding = os.path.relpath(os.getcwd(), generators_dir)

        if binding in all_bindings:
            active_bindings = set([binding])

    if args.prepare:
        for binding in all_bindings:
            if binding not in active_bindings:
                continue

            path = os.path.join(generators_dir, binding)

            if not os.path.isdir(path):
                print('skipping {0}, no {0} directory'.format(binding))
                continue

            zip_path = os.path.join(path, 'zip')
            zip_old_path = os.path.join(path, 'zip_old')

            if not os.path.isdir(zip_path):
                print('skipping {0}, no zip directory'.format(binding))
                continue

            print('preparing ' + binding)

            if os.path.isdir(zip_old_path):
                shutil.rmtree(zip_old_path)

            shutil.copytree(zip_path, zip_old_path)
    else:
        c_like_header1 = re.compile(r'^@@ -1,8 \+1,8 @@\n' + \
        r' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n' + \
        r'- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
        r'\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
        r'  \*                                                           \*\n' + \
        r'  \* .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
        r'  \*                                                           \*\n' + \
        r'  \* If you have a bugfix for this file and want to commit it, \*\n' + \
        r'  \* please fix the bug in the generator\. You can find a link  \*\n' + \
        r'  \* to the generators git repository on tinkerforge\.com       \*\n$')

        c_like_header2 = re.compile(r'^@@ -1,10 \+1,10 @@\n' + \
        r' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n' + \
        r'- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
        r'\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
        r'  \*                                                           \*\n' + \
        r'- \* .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
        r'\+ \* .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
        r'  \*                                                           \*\n' + \
        r'  \* If you have a bugfix for this file and want to commit it, \*\n' + \
        r'  \* please fix the bug in the generator\. You can find a link  \*\n' + \
        r'  \* to the generators git repository on tinkerforge\.com       \*\n' + \
        r'  \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*/\n' + \
        r' \n$')

        delphi_header1 = re.compile(r'^@@ -1,8 \+1,8 @@\n' + \
        r' {\n' + \
        r'-  This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.\n' + \
        r'\+  This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.\n' + \
        r' \n' + \
        r'   Delphi/Lazarus Bindings Version 2\.[0-9]+\.[0-9]+\n' + \
        r' \n' + \
        r'   If you have a bugfix for this file and want to commit it,\n' + \
        r'   please fix the bug in the generator\. You can find a link\n' + \
        r'   to the generators git on tinkerforge\.com\n$')

        delphi_header2 = re.compile(r'^@@ -1,10 \+1,10 @@\n' + \
        r' {\n' + \
        r'-  This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.\n' + \
        r'\+  This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.\n' + \
        r' \n' + \
        r'-  Delphi/Lazarus Bindings Version 2\.[0-9]+\.[0-9]+\n' + \
        r'\+  Delphi/Lazarus Bindings Version 2\.[0-9]+\.[0-9]+\n' + \
        r' \n' + \
        r'   If you have a bugfix for this file and want to commit it,\n' + \
        r'   please fix the bug in the generator\. You can find a link\n' + \
        r'   to the generators git on tinkerforge\.com\n' + \
        r' }\n' + \
        r' \n$')

        javascript_header1 = re.compile(r'^@@ -[0-9]+,8 \+[0-9]+,8 @@\n' + \
        r' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n' + \
        r'- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
        r'\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
        r'  \*                                                           \*\n' + \
        r'  \* JavaScript Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
        r'  \*                                                           \*\n' + \
        r'  \* If you have a bugfix for this file and want to commit it, \*\n' + \
        r'  \* please fix the bug in the generator\. You can find a link  \*\n' + \
        r'  \* to the generators git repository on tinkerforge\.com       \*\n$')

        javascript_header2 = re.compile(r'^@@ -[0-9]+,10 \+[0-9]+,10 @@\n' + \
        r' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n' + \
        r'- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
        r'\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
        r'  \*                                                           \*\n' + \
        r'- \* JavaScript Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
        r'\+ \* JavaScript Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
        r'  \*                                                           \*\n' + \
        r'  \* If you have a bugfix for this file and want to commit it, \*\n' + \
        r'  \* please fix the bug in the generator\. You can find a link  \*\n' + \
        r'  \* to the generators git repository on tinkerforge\.com       \*\n' + \
        r'  \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*/\n' + \
        r' \n$')

        javascript_header3 = re.compile(r'^@@ -[0-9]+,13 \+[0-9]+,13 @@\n' + \
        r' }\n' + \
        r' \n' + \
        r' module\.exports = Brick[A-Za-z0-9]+;\n' + \
        r' \n' + \
        r' },{"\./Device":[0-9]+,"\./IPConnection":[0-9]+}\],[0-9]+:\[function\(require,module,exports\){\n' + \
        r' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n' + \
        r'- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
        r'\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
        r'  \*                                                           \*\n' + \
        r'  \* JavaScript Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
        r'  \*                                                           \*\n' + \
        r'  \* If you have a bugfix for this file and want to commit it, \*\n' + \
        r'  \* please fix the bug in the generator\. You can find a link  \*\n' + \
        r'  \* to the generators git repository on tinkerforge\.com       \*\n$')

        javascript_header4 = re.compile(r'^@@ -[0-9]+,15 \+[0-9]+,15 @@\n' + \
        r' }\n' + \
        r' \n' + \
        r' module\.exports = Brick[A-Za-z0-9]+;\n' + \
        r' \n' + \
        r' },{"\./Device":[0-9]+,"\./IPConnection":[0-9]+}\],[0-9]+:\[function\(require,module,exports\){\n' + \
        r' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n' + \
        r'- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
        r'\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
        r'  \*                                                           \*\n' + \
        r'- \* JavaScript Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
        r'\+ \* JavaScript Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
        r'  \*                                                           \*\n' + \
        r'  \* If you have a bugfix for this file and want to commit it, \*\n' + \
        r'  \* please fix the bug in the generator\. You can find a link  \*\n' + \
        r'  \* to the generators git repository on tinkerforge\.com       \*\n' + \
        r'  \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*/\n' + \
        r' \n$')

        perl_header1 = re.compile(r'^@@ -1,8 \+1,8 @@\n' + \
        r' #############################################################\n' + \
        r'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
        r'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
        r' #                                                           #\n' + \
        r' # Perl Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
        r' #                                                           #\n' + \
        r' # If you have a bugfix for this file and want to commit it, #\n' + \
        r' # please fix the bug in the generator\. You can find a link  #\n' + \
        r' # to the generators git repository on tinkerforge\.com       #\n$')

        perl_header2 = re.compile(r'^@@ -1,10 \+1,10 @@\n' + \
        r' #############################################################\n' + \
        r'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
        r'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
        r' #                                                           #\n' + \
        r'-# Perl Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
        r'\+# Perl Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
        r' #                                                           #\n' + \
        r' # If you have a bugfix for this file and want to commit it, #\n' + \
        r' # please fix the bug in the generator\. You can find a link  #\n' + \
        r' # to the generators git repository on tinkerforge\.com       #\n' + \
        r' #############################################################\n' + \
        r' \n$')

        php_header1 = re.compile(r'^@@ -1,10 \+1,10 @@\n' + \
        r' <\?php\n' + \
        r' \n' + \
        r' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\\n' + \
        r'- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
        r'\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
        r'  \*                                                           \*\n' + \
        r'  \* PHP Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
        r'  \*                                                           \*\n' + \
        r'  \* If you have a bugfix for this file and want to commit it, \*\n' + \
        r'  \* please fix the bug in the generator\. You can find a link  \*\n' + \
        r'  \* to the generators git repository on tinkerforge\.com       \*\n$')

        php_header2 = re.compile(r'^@@ -1,12 \+1,12 @@\n' + \
        r' <\?php\n' + \
        r' \n' + \
        r' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\\n' + \
        r'- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
        r'\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
        r'  \*                                                           \*\n' + \
        r'- \* PHP Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
        r'\+ \* PHP Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
        r'  \*                                                           \*\n' + \
        r'  \* If you have a bugfix for this file and want to commit it, \*\n' + \
        r'  \* please fix the bug in the generator\. You can find a link  \*\n' + \
        r'  \* to the generators git repository on tinkerforge\.com       \*\n' + \
        r'  \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*/\n' + \
        r' \n$')

        python_header1 = re.compile(r'^@@ -1,9 \+1,9 @@\n' + \
        r' # -\*- coding: utf-8 -\*-\n' + \
        r' #############################################################\n' + \
        r'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
        r'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
        r' #                                                           #\n' + \
        r' # Python Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
        r' #                                                           #\n' + \
        r' # If you have a bugfix for this file and want to commit it, #\n' + \
        r' # please fix the bug in the generator\. You can find a link  #\n' + \
        r' # to the generators git repository on tinkerforge\.com       #\n$')

        python_header2 = re.compile(r'^@@ -1,11 \+1,11 @@\n' + \
        r' # -\*- coding: utf-8 -\*-\n' + \
        r' #############################################################\n' + \
        r'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
        r'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
        r' #                                                           #\n' + \
        r'-# Python Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
        r'\+# Python Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
        r' #                                                           #\n' + \
        r' # If you have a bugfix for this file and want to commit it, #\n' + \
        r' # please fix the bug in the generator\. You can find a link  #\n' + \
        r' # to the generators git repository on tinkerforge\.com       #\n' + \
        r' #############################################################\n' + \
        r' \n$')

        ruby_header1 = re.compile(r'^@@ -1,9 \+1,9 @@\n' + \
        r' # -\*- ruby encoding: utf-8 -\*-\n' + \
        r' #############################################################\n' + \
        r'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
        r'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
        r' #                                                           #\n' + \
        r' # Ruby Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
        r' #                                                           #\n' + \
        r' # If you have a bugfix for this file and want to commit it, #\n' + \
        r' # please fix the bug in the generator\. You can find a link  #\n' + \
        r' # to the generators git repository on tinkerforge\.com       #\n$')

        ruby_header2 = re.compile(r'^@@ -1,11 \+1,11 @@\n' + \
        r' # -\*- ruby encoding: utf-8 -\*-\n' + \
        r' #############################################################\n' + \
        r'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
        r'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
        r' #                                                           #\n' + \
        r'-# Ruby Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
        r'\+# Ruby Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
        r' #                                                           #\n' + \
        r' # If you have a bugfix for this file and want to commit it, #\n' + \
        r' # please fix the bug in the generator\. You can find a link  #\n' + \
        r' # to the generators git repository on tinkerforge\.com       #\n' + \
        r' #############################################################\n' + \
        r' \n$')

        tmp = tempfile.mkdtemp()

        print('using tmpdir ' + tmp)

        for binding in all_bindings:
            if binding not in active_bindings:
                continue

            path = os.path.join(generators_dir, binding)

            if not os.path.isdir(path):
                print('skipping {0}, no {0} directory'.format(binding))
                continue

            if not os.path.isdir(os.path.join(path, 'zip')):
                print('skipping {0}, no zip directory'.format(binding))
                continue

            version = common.get_changelog_version(path)

            if args.unreleased:
                if not os.path.isdir(os.path.join(path, 'zip_old')):
                    print('skipping {0}, no zip_old directory'.format(binding))
                    continue

                print('diffing ' + binding)

                shutil.copytree(os.path.join(path, 'zip_old'), os.path.join(tmp, 'old_{0}'.format(binding)))
            else:
                print('diffing ' + binding)

                if os.system('bash -ce "curl -sf https://download.tinkerforge.com/bindings/{0}/tinkerforge_{0}_bindings_latest.zip -o {1}/old_{0}.zip"'.format(binding, tmp)) != 0:
                    print('error: download latest.zip failed')
                    return 1

                if os.system('bash -ce "pushd {1} > /dev/null && unzip -q -d old_{0} old_{0}.zip && popd > /dev/null"'.format(binding, tmp)) != 0:
                    print('error: unzip latest.zip failed')
                    return 1

            if os.system('bash -ce "cp {0}/tinkerforge_{1}_bindings_{3}_{4}_{5}.zip {2} && pushd {2} > /dev/null && unzip -q -d new_{1} tinkerforge_{1}_bindings_{3}_{4}_{5}.zip && popd > /dev/null"'.format(path, binding, tmp, *version)) != 0:
                print('error: copy and unzip new.zip failed')
                return 1

            if os.system('bash -c "pushd {1} > /dev/null && diff -r{2}u6 old_{0}/ new_{0}/ > diff_{0}.diff; popd > /dev/null"'.format(binding, tmp, 'b' if args.ignore_space_change else '')) != 0:
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

        if os.system('bash -ce "{0} {1}/diff.diff"'.format(args.diff_tool, tmp)) != 0:
            print('{0} diff.diff failed'.format(args.diff_tool))
            return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
