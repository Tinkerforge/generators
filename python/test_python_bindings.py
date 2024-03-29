#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python Bindings Tester
Copyright (C) 2012-2014, 2017-2018 Matthias Bolte <matthias@tinkerforge.com>

test_python_bindings.py: Tests the Python bindings

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
import subprocess
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

class PythonTester(common.Tester):
    def __init__(self, root_dir, python, extra_paths):
        common.Tester.__init__(self, 'python', '.py', root_dir, comment=python, subdirs=['examples', 'source'], extra_paths=extra_paths)

        self.python = python

    def test(self, cookie, tmp_dir, scratch_dir, path, extra):
        args = [self.python,
                '-c',
                'import py_compile; py_compile.compile("{0}", doraise=True)'.format(path)]

        self.execute(cookie, args)

class PylintTester(common.Tester):
    def __init__(self, root_dir, python, comment, extra_paths):
        common.Tester.__init__(self, 'python', '.py', root_dir, comment=comment, subdirs=['examples', 'source'], extra_paths=extra_paths)

        self.python = python

    def test(self, cookie, tmp_dir, scratch_dir, path, extra):
        teardown = None

        if self.python == 'python3':
            with open(path, 'r') as f:
                code = f.read()

            code = code.replace('raw_input(', 'input(')
            path_check = path.replace('.py', '_check.py')

            with open(path_check, 'w') as f:
                f.write(code)

            path = path_check
            teardown = lambda: [os.remove(path)]

        args = [self.python,
                '-c',
                'import sys; sys.path.insert(0, "{0}"); import pylint; pylint.run_pylint()'.format(os.path.join(tmp_dir, 'source')),
                '-E',
                '--disable=no-name-in-module,assignment-from-no-return',
                path]

        self.execute(cookie, args, teardown=teardown)

def test(root_dir):
    extra_paths = [os.path.join(root_dir, '../../weather-station/demo/starter_kit_weather_station_demo/main.py'),
                   os.path.join(root_dir, '../../weather-station/write_to_lcd/python/weather_station.py'),
                   os.path.join(root_dir, '../../hardware-hacking/remote_switch/python/remote_switch.py'),
                   os.path.join(root_dir, '../../hardware-hacking/smoke_detector/python/smoke_detector.py'),
                   os.path.join(root_dir, '../../blinkenlights/demo/starter_kit_blinkenlights_demo/main.py'),
                   os.path.join(root_dir, '../../blinkenlights/demo/starter_kit_blinkenlights_demo/fire_widget.py'),
                   os.path.join(root_dir, '../../blinkenlights/demo/starter_kit_blinkenlights_demo/pong_widget.py'),
                   os.path.join(root_dir, '../../blinkenlights/demo/starter_kit_blinkenlights_demo/tetris_widget.py'),
                   os.path.join(root_dir, '../../blinkenlights/demo/starter_kit_blinkenlights_demo/images_widget.py'),
                   os.path.join(root_dir, '../../blinkenlights/demo/starter_kit_blinkenlights_demo/rainbow_widget.py'),
                   os.path.join(root_dir, '../../blinkenlights/demo/starter_kit_blinkenlights_demo/text_widget.py'),
                   os.path.join(root_dir, '../../blinkenlights/fire/python/fire.py'),
                   os.path.join(root_dir, '../../blinkenlights/games/python/keypress.py'),
                   os.path.join(root_dir, '../../blinkenlights/games/python/pong.py'),
                   os.path.join(root_dir, '../../blinkenlights/games/python/repeated_timer.py'),
                   os.path.join(root_dir, '../../blinkenlights/games/python/tetris.py'),
                   os.path.join(root_dir, '../../blinkenlights/images/python/images.py'),
                   os.path.join(root_dir, '../../blinkenlights/rainbow/python/rainbow.py'),
                   os.path.join(root_dir, '../../blinkenlights/text/python/text.py')]

    python2 = None

    if os.path.exists('/usr/bin/python') and subprocess.check_output(['python', '--version'], encoding='utf-8').startswith('Python 2.'):
        python2 = 'python'
    elif os.path.exists('/usr/bin/python2'):
        python2 = 'python2'

    if python2 != None:
        if not PythonTester(root_dir, python2, extra_paths).run():
            return False

        # FIXME: doesn't handle PyQt related super false-positves yet
        if subprocess.call([python2, '-m', 'pylint', '-h'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            print('\nSkipping pylint test, module not available\n')
        else:
            if not PylintTester(root_dir, python2, 'pylint', []).run():#extra_paths).run():
                return False

    if not PythonTester(root_dir, 'python3', extra_paths).run():
        return False

    # FIXME: doesn't handle PyQt related super false-positves yet
    return PylintTester(root_dir, 'python3', 'pylint3', []).run()#extra_paths).run()

if __name__ == '__main__':
    common.dockerize('python', __file__)

    test(os.getcwd())
