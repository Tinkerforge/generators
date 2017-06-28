#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java Bindings Tester
Copyright (C) 2012-2014, 2017 Matthias Bolte <matthias@tinkerforge.com>

test_java_bindings.py: Tests the Java bindings

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
import subprocess
import shutil

sys.path.append(os.path.split(os.getcwd())[0])
import common

class JavaExamplesTester(common.Tester):
    def __init__(self, bindings_root_directory, extra_paths):
        common.Tester.__init__(self, 'java', '.java', bindings_root_directory, extra_paths=extra_paths)

    def test(self, cookie, path, extra):
        if extra:
            shutil.copy(path, '/tmp/tester/java')
            path = os.path.join('/tmp/tester/java', os.path.split(path)[1])

        args = ['/usr/bin/javac',
                '-Xlint',
                '-cp',
                '/tmp/tester/java/Tinkerforge.jar:.',
                path]

        self.execute(cookie, args)

class JavaDocTester(common.Tester):
    def __init__(self, bindings_root_directory):
        common.Tester.__init__(self, 'java', '.html', bindings_root_directory, subdirs=['javadoc/com/tinkerforge'])

    def after_unzip(self):
        print('>>> generating javadoc')

        args = ['/usr/bin/javadoc',
                '-quiet',
                '-d',
                '/tmp/tester/java/javadoc',
                '-classpath',
                '/tmp/tester/java/source',
                'com.tinkerforge']

        rc = subprocess.call(args)

        if rc != 0:
            print('>>> could not generate javadoc')
        else:
            print('>>> generating javadoc done\n')

        return rc == 0

    def test(self, cookie, path, extra):
        args = ['/usr/bin/xmllint',
                '--noout',
                '--valid',
                '--html',
                path]

        self.execute(cookie, args)

def run(bindings_root_directory):
    extra_paths = [os.path.join(bindings_root_directory, '../../weather-station/examples/GuitarStation.java'),
                   os.path.join(bindings_root_directory, '../../weather-station/write_to_lcd/java/WeatherStation.java'),
                   os.path.join(bindings_root_directory, '../../hardware-hacking/remote_switch/java/RemoteSwitch.java'),
                   os.path.join(bindings_root_directory, '../../hardware-hacking/smoke_detector/java/SmokeDetector.java')]

    if not JavaExamplesTester(bindings_root_directory, extra_paths).run():
        return False

    return JavaDocTester(bindings_root_directory).run()

if __name__ == "__main__":
    run(os.getcwd())
