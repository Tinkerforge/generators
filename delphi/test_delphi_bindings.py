#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Delphi Bindings Tester
Copyright (C) 2012-2014, 2017 Matthias Bolte <matthias@tinkerforge.com>

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
import os
import shutil

sys.path.append(os.path.split(os.getcwd())[0])
import common

class DelphiExamplesTester(common.Tester):
    # FIXME: examples can not be tested in parallel, because of the shared
    # output directory and the way FPC works
    PROCESSES = 1

    def __init__(self, bindings_root_directory, extra_paths):
        common.Tester.__init__(self, 'delphi', '.pas', bindings_root_directory, extra_paths=extra_paths)

    def test(self, cookie, path, extra):
        if extra:
            shutil.copy(path, '/tmp/tester/delphi')
            path = os.path.join('/tmp/tester/delphi', os.path.split(path)[1])

        args = ['/usr/bin/fpc',
                '-vw',
                '-Fu/tmp/tester/delphi/source',
                '-l',
                path]

        retcode, output = common.check_output_and_error(args)
        output = output.strip('\r\n')
        success = retcode == 0 and 'warning(s) issued' not in output

        self.handle_result(cookie, output, success)

def run(bindings_root_directory):
    extra_paths = [os.path.join(bindings_root_directory, '../../weather-station/write_to_lcd/delphi/WeatherStation.pas'),
                   os.path.join(bindings_root_directory, '../../hardware-hacking/remote_switch/delphi/RemoteSwitch.pas'),
                   os.path.join(bindings_root_directory, '../../hardware-hacking/smoke_detector/delphi/SmokeDetector.pas')]

    return DelphiExamplesTester(bindings_root_directory, extra_paths).run()

if __name__ == "__main__":
    run(os.getcwd())
