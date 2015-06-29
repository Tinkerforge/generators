#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java Bindings Tester
Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>

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

def check_output_and_error(*popenargs, **kwargs):
    process = subprocess.Popen(stdout=subprocess.PIPE, stderr=subprocess.PIPE, *popenargs, **kwargs)
    output, error = process.communicate()
    retcode = process.poll()
    return (retcode, output + error)

class JavaExamplesTester(common.ExamplesTester):
    def __init__(self, path, extra_examples):
        common.ExamplesTester.__init__(self, 'java', '.java', path, extra_examples=extra_examples)

    def test(self, cookie, src, is_extra_example):
        if is_extra_example:
            shutil.copy(src, '/tmp/tester/java')
            src = os.path.join('/tmp/tester/java', os.path.split(src)[1])

        args = ['/usr/bin/javac',
                '-Xlint',
                '-cp',
                '/tmp/tester/java/Tinkerforge.jar:.',
                src]

        self.execute(cookie, args)

class JavaSourceTester(common.SourceTester):
    def __init__(self, path):
        common.SourceTester.__init__(self, 'java', '.html', path, subdirs=['javadoc/com/tinkerforge'])

    def after_unzip(self):
        if not common.SourceTester.after_unzip(self):
            return False

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

    def test(self, src):
        args = ['/usr/bin/xmllint',
                '--noout',
                '--valid',
                '--html',
                src]

        retcode, output = check_output_and_error(args)
        output = output.strip('\r\n')

        if len(output) > 0:
            print(output)

        return retcode == 0 and len(output) == 0

def run(path):
    extra_examples = [os.path.join(path, '../../weather-station/examples/GuitarStation.java'),
                      os.path.join(path, '../../weather-station/write_to_lcd/java/WeatherStation.java'),
                      os.path.join(path, '../../hardware-hacking/remote_switch/java/RemoteSwitch.java'),
                      os.path.join(path, '../../hardware-hacking/smoke_detector/java/SmokeDetector.java')]

    if not JavaExamplesTester(path, extra_examples).run():
        return False

    return JavaSourceTester(path).run()

if __name__ == "__main__":
    sys.exit(run(os.getcwd()))
