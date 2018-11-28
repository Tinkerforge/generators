#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PHP Bindings Tester
Copyright (C) 2012-2014, 2017-2018 Matthias Bolte <matthias@tinkerforge.com>

test_php_bindings.py: Tests the PHP bindings

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

sys.path.append(os.path.split(os.getcwd())[0])
import common

class PHPTester(common.Tester):
    def __init__(self, root_dir, extra_paths):
        common.Tester.__init__(self, 'php', '.php', root_dir, subdirs=['examples', 'source'], extra_paths=extra_paths)

    def test(self, cookie, path, extra):
        args = ['php',
                '-l',
                path]

        self.execute(cookie, args)

def run(root_dir):
    extra_paths = [os.path.join(root_dir, '../../weather-station/website/php/WeatherStationWebsite.php'),
                   os.path.join(root_dir, '../../weather-station/write_to_lcd/php/WeatherStation.php'),
                   os.path.join(root_dir, '../../hardware-hacking/remote_switch/php/RemoteSwitch.php'),
                   os.path.join(root_dir, '../../hardware-hacking/smoke_detector/php/SmokeDetector.php')]

    return PHPTester(root_dir, extra_paths).run()

if __name__ == '__main__':
    run(os.getcwd())
