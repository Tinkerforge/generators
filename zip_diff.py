#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import tempfile
import common

args = sys.argv[1:]

if len(args) == 0:
    print 'usage: zip_diff.py <bindings>'
    sys.exit(1)

bindings = args[0].rstrip('/')
version = common.get_changelog_version(bindings)
tmp = tempfile.mkdtemp()

if os.system('bash -c "curl http://download.tinkerforge.com/bindings/{0}/tinkerforge_{0}_bindings_latest.zip -o {1}/tinkerforge_{0}_bindings_latest.zip"'.format(bindings, tmp)) != 0:
    print 'download latest.zip failed'
    sys.exit(1)

if os.system('bash -c "pushd {1} && unzip -d latest tinkerforge_{0}_bindings_latest.zip && popd"'.format(bindings, tmp)) != 0:
    print 'unzip latest.zip failed'
    sys.exit(1)

if os.system('bash -c "cp {0}/tinkerforge_{0}_bindings_{2}_{3}_{4}.zip {1} && pushd {1} && unzip -d {2}_{3}_{4} tinkerforge_{0}_bindings_{2}_{3}_{4}.zip && popd"'.format(bindings, tmp, *version)) != 0:
    print 'copy/unzip current.zip failed'
    sys.exit(1)

if os.system('bash -c "pushd {1} && diff -ur latest/ {2}_{3}_{4}/ > diff1.diff; popd"'.format(bindings, tmp, *version)) != 0:
    print 'diff latest vs current failed'
    sys.exit(1)

with open(os.path.join(tmp, 'diff1.diff'), 'rb') as f:
    diffs = [[]]

    for line in f.readlines():
        if line.startswith('diff '):
            diffs.append([])

        diffs[-1].append(line)

c_like_header1 = re.compile('^@@ -1,5 \+1,5 @@\n' + \
' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\\n' + \
'- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'  \*                                                           \*\n' + \
'  \* .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
'  \*                                                           \*\n$')

c_like_header2 = re.compile('^@@ -1,7 \+1,7 @@\n' + \
' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\\n' + \
'- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'  \*                                                           \*\n' + \
'- \* .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
'\+ \* .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
'  \*                                                           \*\n' + \
'  \* If you have a bugfix for this file and want to commit it, \*\n' + \
'  \* please fix the bug in the generator\. You can find a link  \*\n$')

delphi_header1 = re.compile('^@@ -1,7 \+1,7 @@\n' + \
' {\n' + \
'-  This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.\n' + \
'\+  This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.\n' + \
' \n' + \
'-  Delphi/Lazarus Bindings Version 2\.[0-9]+\.[0-9]+\n' + \
'\+  Delphi/Lazarus Bindings Version 2\.[0-9]+\.[0-9]+\n' + \
' \n' + \
'   If you have a bugfix for this file and want to commit it,\n' + \
'   please fix the bug in the generator\. You can find a link\n$')

delphi_header2 = re.compile('^@@ -1,5 \+1,5 @@\n' + \
' {\n' + \
'-  This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.\n' + \
'\+  This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.\n' + \
' \n' + \
'   Delphi/Lazarus Bindings Version 2\.[0-9]+\.[0-9]+\n' + \
' \n$')

perl_header1 = re.compile('^@@ -1,5 \+1,5 @@\n' + \
' #############################################################\n' + \
'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}.      #\n' + \
'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}.      #\n' + \
' #                                                           #\n' + \
' # .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
' #                                                           #\n$')

perl_header2 = re.compile('^@@ -1,7 \+1,7 @@\n' + \
' #############################################################\n' + \
'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}.      #\n' + \
'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}.      #\n' + \
' #                                                           #\n' + \
'-# .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
'\+# .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
' #                                                           #\n' + \
' # If you have a bugfix for this file and want to commit it, #\n' + \
' # please fix the bug in the generator. You can find a link  #\n$')

php_header1 = re.compile('^@@ -1,7 \+1,7 @@\n' + \
' <\?php\n' + \
' \n' + \
' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\\n' + \
'- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'  \*                                                           \*\n' + \
'  \* .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
'  \*                                                           \*\n$')

php_header2 = re.compile('^@@ -1,9 \+1,9 @@\n' + \
' <\?php\n' + \
' \n' + \
' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\\n' + \
'- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'  \*                                                           \*\n' + \
'- \* .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
'\+ \* .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
'  \*                                                           \*\n' + \
'  \* If you have a bugfix for this file and want to commit it, \*\n' + \
'  \* please fix the bug in the generator\. You can find a link  \*\n$')

python_header1 = re.compile('^@@ -1,6 \+1,6 @@\n' + \
' # -\*- coding: utf-8 -\*-\n' + \
' #############################################################\n' + \
'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}.      #\n' + \
'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}.      #\n' + \
' #                                                           #\n' + \
' # .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
' #                                                           #\n$')

python_header2 = re.compile('^@@ -1,8 \+1,8 @@\n' + \
' # -\*- coding: utf-8 -\*-\n' + \
' #############################################################\n' + \
'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}.      #\n' + \
'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}.      #\n' + \
' #                                                           #\n' + \
'-# .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
'\+# .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
' #                                                           #\n' + \
' # If you have a bugfix for this file and want to commit it, #\n' + \
' # please fix the bug in the generator. You can find a link  #\n$')

ruby_header1 = re.compile('^@@ -1,6 \+1,6 @@\n' + \
' # -\*- ruby encoding: utf-8 -\*-\n' + \
' #############################################################\n' + \
'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}.      #\n' + \
'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}.      #\n' + \
' #                                                           #\n' + \
' # .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
' #                                                           #\n$')

ruby_header2 = re.compile('^@@ -1,8 \+1,8 @@\n' + \
' # -\*- ruby encoding: utf-8 -\*-\n' + \
' #############################################################\n' + \
'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}.      #\n' + \
'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}.      #\n' + \
' #                                                           #\n' + \
'-# .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
'\+# .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
' #                                                           #\n' + \
' # If you have a bugfix for this file and want to commit it, #\n' + \
' # please fix the bug in the generator. You can find a link  #\n$')

filtered_diffs = []

for diff in diffs:
    hunk = ''.join(diff[3:])

    if not c_like_header1.match(hunk) and \
       not c_like_header2.match(hunk) and \
       not delphi_header1.match(hunk) and \
       not delphi_header2.match(hunk) and \
       not perl_header1.match(hunk) and \
       not perl_header2.match(hunk) and \
       not php_header1.match(hunk) and \
       not php_header2.match(hunk) and \
       not python_header1.match(hunk) and \
       not python_header2.match(hunk) and \
       not ruby_header1.match(hunk) and \
       not ruby_header2.match(hunk):
        filtered_diffs.append(''.join(diff))
    else:
        filtered_diffs.append('DROPPED HEADER DIFF: ' + diff[0])

with open(os.path.join(tmp, 'diff2.diff'), 'wb') as f:
    f.writelines(filtered_diffs)

if os.system('bash -c "pushd {0} && geany diff2.diff && popd"'.format(tmp)) != 0:
    print 'geany diff.diff failed'
    sys.exit(1)
