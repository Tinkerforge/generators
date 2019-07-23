#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import tempfile
import shutil
import common

args = sys.argv[1:]

if '--prepare' in args:
    for d in os.listdir('.'):
        if not os.path.isdir(d):
            continue

        if d in ['configs', 'stubs', 'json', 'tvpl', '.git', '__pycache__', '.vscode']:
            continue

        doc_path = os.path.join(d, 'doc')
        doc_old_path = os.path.join(d, 'doc_old')

        if os.path.isdir(doc_old_path):
            shutil.rmtree(doc_old_path)

        shutil.copytree(doc_path, doc_old_path)
else:
    if len(args) == 0:
        bindings = os.path.split(os.getcwd())[-1]
    else:
        bindings = args[0].rstrip('/')

    root = os.path.split(__file__)[0]

    if len(root) == 0:
        root = '.'

    base = os.path.join(root, bindings)
    tmp = tempfile.mkdtemp()

    if os.system('bash -cx "pushd {0} && diff -ur doc_old/ doc/ > {1}/diff.diff; popd"'.format(base, tmp)) != 0:
        print 'diff old vs new failed'
        sys.exit(1)

    if os.system('bash -c "geany {0}/diff.diff && popd"'.format(tmp)) != 0:
        print 'geany diff.diff failed'
        sys.exit(1)
