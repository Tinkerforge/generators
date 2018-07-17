#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import tempfile
import common

args = sys.argv[1:]

if len(args) == 0:
    bindings = os.path.split(os.getcwd())[-1]
else:
    bindings = args[0].rstrip('/')

root = os.path.split(__file__)[0]

with common.ChangedDirectory(root):
    version = common.get_changelog_version(bindings)

base = os.path.join(root, bindings)
tmp = tempfile.mkdtemp()

if os.system('bash -cex "curl http://download.tinkerforge.com/bindings/{0}/tinkerforge_{0}_bindings_latest.zip -o {1}/tinkerforge_{0}_bindings_latest.zip"'.format(bindings, tmp)) != 0:
    print 'download latest.zip failed'
    sys.exit(1)

if os.system('bash -cex "pushd {1} && unzip -q -d latest tinkerforge_{0}_bindings_latest.zip && popd"'.format(bindings, tmp)) != 0:
    print 'unzip latest.zip failed'
    sys.exit(1)

if os.system('bash -cex "cp {0}/tinkerforge_{1}_bindings_{3}_{4}_{5}.zip {2} && pushd {2} && unzip -q -d {3}_{4}_{5} tinkerforge_{1}_bindings_{3}_{4}_{5}.zip && popd"'.format(base, bindings, tmp, *version)) != 0:
    print 'copy/unzip current.zip failed'
    sys.exit(1)

if os.system('bash -cx "pushd {0} && diff -ur latest/ {1}_{2}_{3}/ > diff1.diff; popd"'.format(tmp, *version)) != 0:
    print 'diff latest vs current failed'
    sys.exit(1)

with open(os.path.join(tmp, 'diff1.diff'), 'r') as f:
    diffs = [[[]]] # list of diffs as lists of lines

    for line in f.readlines():
        if line.startswith('diff ') or line[0] not in ['@', '-', '+', ' ']:
            diffs.append([[]])

        if line.startswith('@@ '):
            diffs[-1].append([])

        diffs[-1][-1].append(line)

c_like_header1 = re.compile(r'^@@ -1,5 \+1,5 @@\n' + \
' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n' + \
'- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'  \*                                                           \*\n' + \
'  \* .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
'  \*                                                           \*\n$')

c_like_header2 = re.compile(r'^@@ -1,7 \+1,7 @@\n' + \
' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n' + \
'- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'  \*                                                           \*\n' + \
'- \* .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
'\+ \* .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
'  \*                                                           \*\n' + \
'  \* If you have a bugfix for this file and want to commit it, \*\n' + \
'  \* please fix the bug in the generator\. You can find a link  \*\n$')

delphi_header1 = re.compile(r'^@@ -1,7 \+1,7 @@\n' + \
' {\n' + \
'-  This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.\n' + \
'\+  This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.\n' + \
' \n' + \
'-  Delphi/Lazarus Bindings Version 2\.[0-9]+\.[0-9]+\n' + \
'\+  Delphi/Lazarus Bindings Version 2\.[0-9]+\.[0-9]+\n' + \
' \n' + \
'   If you have a bugfix for this file and want to commit it,\n' + \
'   please fix the bug in the generator\. You can find a link\n$')

delphi_header2 = re.compile(r'^@@ -1,5 \+1,5 @@\n' + \
' {\n' + \
'-  This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.\n' + \
'\+  This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.\n' + \
' \n' + \
'   Delphi/Lazarus Bindings Version 2\.[0-9]+\.[0-9]+\n' + \
' \n$')

javascript_header1 = re.compile(r'^@@ -[0-9]+,7 \+[0-9]+,7 @@\n' + \
' \n' + \
' },{"\./Device":[0-9]+}\],[0-9]+:\[function\(require,module,exports\){\n' + \
' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n' + \
'- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'  \*                                                           \*\n' + \
'  \* JavaScript Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
'  \*                                                           \*\n$')

javascript_header2 = re.compile(r'^@@ -[0-9]+,9 \+[0-9]+,9 @@\n' + \
' \n' + \
' module\.exports = Brick[A-Za-z0-9]+;\n' + \
' \n' + \
'-},{"\./Device":[0-9]+}\],[0-9]+:\[function\(require,module,exports\){\n' + \
'\+},{"\./Device":[0-9]+}\],[0-9]+:\[function\(require,module,exports\){\n' + \
' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\n' + \
'- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'  \*                                                           \*\n' + \
'  \* JavaScript Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
'  \*                                                           \*\n$')

perl_header1 = re.compile(r'^@@ -1,5 \+1,5 @@\n' + \
' #############################################################\n' + \
'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
' #                                                           #\n' + \
' # .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
' #                                                           #\n$')

perl_header2 = re.compile(r'^@@ -1,7 \+1,7 @@\n' + \
' #############################################################\n' + \
'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
' #                                                           #\n' + \
'-# .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
'\+# .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
' #                                                           #\n' + \
' # If you have a bugfix for this file and want to commit it, #\n' + \
' # please fix the bug in the generator. You can find a link  #\n$')

php_header1 = re.compile(r'^@@ -1,7 \+1,7 @@\n' + \
' <\?php\n' + \
' \n' + \
' /\* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\\n' + \
'- \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'\+ \* This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      \*\n' + \
'  \*                                                           \*\n' + \
'  \* .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+\*\n' + \
'  \*                                                           \*\n$')

php_header2 = re.compile(r'^@@ -1,9 \+1,9 @@\n' + \
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

python_header1 = re.compile(r'^@@ -1,6 \+1,6 @@\n' + \
' # -\*- coding: utf-8 -\*-\n' + \
' #############################################################\n' + \
'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
' #                                                           #\n' + \
' # .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
' #                                                           #\n$')

python_header2 = re.compile(r'^@@ -1,8 \+1,8 @@\n' + \
' # -\*- coding: utf-8 -\*-\n' + \
' #############################################################\n' + \
'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
' #                                                           #\n' + \
'-# .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
'\+# .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
' #                                                           #\n' + \
' # If you have a bugfix for this file and want to commit it, #\n' + \
' # please fix the bug in the generator. You can find a link  #\n$')

ruby_header1 = re.compile(r'^@@ -1,6 \+1,6 @@\n' + \
' # -\*- ruby encoding: utf-8 -\*-\n' + \
' #############################################################\n' + \
'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
' #                                                           #\n' + \
' # .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
' #                                                           #\n$')

ruby_header2 = re.compile(r'^@@ -1,8 \+1,8 @@\n' + \
' # -\*- ruby encoding: utf-8 -\*-\n' + \
' #############################################################\n' + \
'-# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
'\+# This file was automatically generated on [0-9]{4}-[0-9]{2}-[0-9]{2}\.      #\n' + \
' #                                                           #\n' + \
'-# .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
'\+# .+ Bindings Version 2\.[0-9]+\.[0-9]+[ ]+#\n' + \
' #                                                           #\n' + \
' # If you have a bugfix for this file and want to commit it, #\n' + \
' # please fix the bug in the generator. You can find a link  #\n$')

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
       filtered_lines[0].startswith('diff -ur ') and \
       filtered_lines[1].startswith('--- ') and \
       filtered_lines[2].startswith('+++ ') and \
       filtered_lines[3].endswith('// dropped header hunk\n'):
        filtered += [filtered_lines[0].rstrip() + ' // dropped header diff\n']
    else:
        filtered += filtered_lines

with open(os.path.join(tmp, 'diff2.diff'), 'w') as f:
    f.writelines(filtered)

if os.system('bash -c "pushd {0} && geany diff2.diff && popd"'.format(tmp)) != 0:
    print 'geany diff.diff failed'
    sys.exit(1)
