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

if args.prepare:
    if args.bindings != None:
        ds = [args.bindings.rstrip('/')]
    else:
        parent_dir, bindings = os.path.split(os.getcwd())

        if parent_dir == generators_dir:
            ds = [bindings]
        else:
            ds = sorted(os.listdir(generators_dir))

    for d in ds:
        if d in ['configs', 'modbus', 'stubs', 'tcpip', 'tvpl', '.git', '__pycache__', '.vscode']:
            continue

        path = os.path.join(generators_dir, d)

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

    sys.exit(0)

if args.bindings != None:
    bindings = args.bindings.rstrip('/')
else:
    parent_dir, bindings = os.path.split(os.getcwd())

    if parent_dir != generators_dir:
        print('error: wrong working directory, cannot auto-detect bindings')
        sys.exit(1)

base = os.path.join(generators_dir, bindings)
version = common.get_changelog_version(base)
tmp = tempfile.mkdtemp()

if args.unreleased:
    shutil.copytree(os.path.join(base, 'zip_old'), os.path.join(tmp, 'old'))
else:
    if os.system('bash -cex "curl https://download.tinkerforge.com/bindings/{0}/tinkerforge_{0}_bindings_latest.zip -o {1}/old.zip"'.format(bindings, tmp)) != 0:
        print('download latest.zip failed')
        sys.exit(1)

    if os.system('bash -cex "pushd {1} && unzip -q -d old old.zip && popd"'.format(bindings, tmp)) != 0:
        print('unzip latest.zip failed')
        sys.exit(1)

if os.system('bash -cex "cp {0}/tinkerforge_{1}_bindings_{3}_{4}_{5}.zip {2} && pushd {2} && unzip -q -d new tinkerforge_{1}_bindings_{3}_{4}_{5}.zip && popd"'.format(base, bindings, tmp, *version)) != 0:
    print('copy and unzip new.zip failed')
    sys.exit(1)

if os.system('bash -cx "pushd {0} && diff -ru6 old/ new/ > diff1.diff; popd"'.format(tmp)) != 0:
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

with open(os.path.join(tmp, 'diff2.diff'), 'w') as f:
    f.writelines(filtered)

if os.system('bash -c "pushd {} && {} diff2.diff && popd"'.format(tmp, diff_tool)) != 0:
    print('{} diff.diff failed'.format(diff_tool))
    sys.exit(1)
