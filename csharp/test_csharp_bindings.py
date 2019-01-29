#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C# Bindings Tester
Copyright (C) 2012-2018 Matthias Bolte <matthias@tinkerforge.com>

test_csharp_bindings.py: Tests the C# bindings

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

class CSharpExamplesTester(common.Tester):
    def __init__(self, root_dir, extra_paths):
        common.Tester.__init__(self, 'csharp', '.cs', root_dir, extra_paths=extra_paths)

    def test(self, cookie, path, extra):
        if extra:
            shutil.copy(path, '/tmp/tester/csharp')
            path = os.path.join('/tmp/tester/csharp', os.path.split(path)[1])

        output = path[:-3] + '.exe'

        args = ['mcs',
                '/warn:4',
                '/optimize',
                '/target:exe',
                '/sdk:2',
                '/out:' + output,
                '/reference:System.Drawing.dll',
                '/reference:System.Windows.Forms.dll',
                '/reference:/tmp/tester/csharp/Tinkerforge.dll',
                path]

        self.execute(cookie, args)

def run(root_dir):
    extra_paths = [os.path.join(root_dir, '../../weather-station/button_control/csharp/WeatherStationButton.cs'),
                   os.path.join(root_dir, '../../weather-station/write_to_lcd/csharp/WeatherStation.cs'),
                   os.path.join(root_dir, '../../hardware-hacking/remote_switch/csharp/RemoteSwitch.cs'),
                   os.path.join(root_dir, '../../hardware-hacking/smoke_detector/csharp/SmokeDetector.cs')]

    return CSharpExamplesTester(root_dir, extra_paths).run()

if __name__ == '__main__':
    run(os.getcwd())
