#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl Bindings Tester
Copyright (C) 2012-2018 Matthias Bolte <matthias@tinkerforge.com>

test_perl_bindings.py: Tests the Perl bindings

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
import importlib.util
import importlib.machinery

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

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

class PerlCheckExamplesTester(common.Tester):
    def __init__(self, root_dir):
        common.Tester.__init__(self, 'perl', '.pl', root_dir, comment='check')

    def test(self, cookie, path, extra):
        path_check = path.replace('.pl', '_check.pl')

        with open(path, 'r') as f:
            code = f.read()

        with open(path_check, 'w') as f:
            f.write('use lib "/tmp/tester/perl/source/lib"; use strict; use warnings; CHECK { sub __check__ { ' + code + '\n\n}}\n\n__check__;\n')

        args = ['perl',
                '-cWT',
                path_check]

        self.execute(cookie, args)

    def check_success(self, exit_code, output):
        output = output.strip('\r\n')

        # FIXME: filter out some internal Perl problems with the Math::Complex module
        filtered_output = [line for line in output.split('\n') if not line.startswith('Prototype mismatch: sub Math::Complex::')]

        return exit_code == 0 and len(filtered_output) == 1 and 'syntax OK' in output

class PerlLintExamplesTester(common.Tester):
    def __init__(self, root_dir):
        common.Tester.__init__(self, 'perl', '.pl', root_dir, comment='lint')

    def test(self, cookie, path, extra):
        path_lint = path.replace('.pl', '_lint.pl')

        with open(path, 'r') as f:
            code = f.read()

        with open(path_lint, 'w') as f:
            f.write('use lib "/tmp/tester/perl/source/lib";' + code)

        args = ['perl',
                '-MO=Lint,all',
                path_lint]

        self.execute(cookie, args)

    def check_success(self, exit_code, output):
        output = output.strip('\r\n')

        if exit_code != 0 and output == "Can't locate object method \"NAME\" via package \"B::IV\" at /usr/share/perl5/B/Lint.pm line 577.\nCHECK failed--call queue aborted.":
            # FIXME: ignore the Lint module having bugs
            return True
        else:
            # FIXME: ignore the Lint module being confused about constants
            filtered_output = []

            for line in output.split('\n'):
                if not line.startswith("Bare sub name 'HOST' interpreted as string at") and \
                   not line.startswith("Bare sub name 'PORT' interpreted as string at") and \
                   not line.startswith("Bare sub name 'UID' interpreted as string at") and \
                   not line.startswith("Bare sub name 'SECRET' interpreted as string at") and \
                   not line.startswith("Bare sub name 'NUM_LEDS' interpreted as string at") and \
                   not line.startswith("Bare sub name 'NDEF_URI' interpreted as string at") and \
                   not line.startswith("Bare sub name 'WIDTH' interpreted as string at") and \
                   not line.startswith("Bare sub name 'HEIGHT' interpreted as string at"):
                    filtered_output.append(line)

            return exit_code == 0 and len(filtered_output) == 1 and 'syntax OK' in output

class PerlCriticExamplesTester(common.Tester):
    def __init__(self, root_dir):
        common.Tester.__init__(self, 'perl', '.pl', root_dir, comment='critic')

    def test(self, cookie, path, extra):
        args = ['perlcritic',
                #'--brutal', # FIXME
                '--verbose',
                '8',
                '--exclude=ProhibitSleepViaSelect',
                path]

        self.execute(cookie, args)

def run(root_dir):
    if not PerlCheckExamplesTester(root_dir).run():
        return False

    if not PerlLintExamplesTester(root_dir).run():
        return False

    return PerlCriticExamplesTester(root_dir).run()

if __name__ == "__main__":
    run(os.getcwd())
