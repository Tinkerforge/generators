#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Delphi Bindings Tester
Copyright (C) 2012-2014, 2017-2018 Matthias Bolte <matthias@tinkerforge.com>

test_delphi_bindings.py: Tests the Delphi bindings

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
import shutil
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

class DelphiExamplesTester(common.Tester):
    # FIXME: examples can not be tested in parallel, because of the shared
    # output directory and the way FPC works
    PROCESSES = 1

    def __init__(self, root_dir, extra_paths):
        common.Tester.__init__(self, 'delphi', '.pas', root_dir, extra_paths=extra_paths)
        exit_code, output = common.check_output_and_error(['gcc', '--print-file-name', 'crtbeginS.o'])

        if exit_code != 0:
            raise common.GeneratorError('Failed to run gcc --print-file-name crtbeginS.o: exit_code: {}\n\t{}'.format(exit_code, output))

        self.lib_path = os.path.dirname(output)

    def test(self, cookie, tmp_dir, scratch_dir, path, extra):
        if extra:
            shutil.copy(path, tmp_dir)
            path = os.path.join(tmp_dir, os.path.split(path)[-1])

        args = ['fpc',
                '-vw',
                '-Fl{}/'.format(self.lib_path),
                '-Fu' + os.path.join(tmp_dir, 'source'),
                '-l',
                path]

        self.execute(cookie, args)

    def check_success(self, exit_code, output):
        return exit_code == 0 and 'warning(s) issued' not in output.strip('\r\n')

def test(root_dir):
    extra_paths = [os.path.join(root_dir, '../../weather-station/write_to_lcd/delphi/WeatherStation.pas'),
                   os.path.join(root_dir, '../../hardware-hacking/remote_switch/delphi/RemoteSwitch.pas'),
                   os.path.join(root_dir, '../../hardware-hacking/smoke_detector/delphi/SmokeDetector.pas')]

    return DelphiExamplesTester(root_dir, extra_paths).run()

if __name__ == '__main__':
    common.dockerize('delphi', __file__)

    test(os.getcwd())
