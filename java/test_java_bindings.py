#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java Bindings Tester
Copyright (C) 2012-2014, 2017-2018 Matthias Bolte <matthias@tinkerforge.com>

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

if sys.hexversion < 0x3050000:
    print('Python >= 3.5 required')
    sys.exit(1)

import os
import subprocess
import shutil
import random
import importlib.util

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
    generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
    generators_module = importlib.util.module_from_spec(generators_spec)

    generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common
from generators.java import java_common

class JavaExamplesTester(common.Tester):
    def __init__(self, root_dir, extra_paths):
        common.Tester.__init__(self, 'java', '.java', root_dir, extra_paths=extra_paths)

    def test(self, cookie, path, extra):
        # create unique copy of the Tinkerforge.jar to avoid Java from randomly
        # complaining about the JAR being missing if Java is started multiple
        # times concurrently
        jar_path = '/tmp/tester/java/Tinkerforge.jar'
        tries = 100

        while os.path.exists(jar_path) and tries > 0:
            r = int(round(random.random() * 10000000000))
            jar_path = '/tmp/tester/java/Tinkerforge_{:010X}.jar'.format(r)
            tries -= 1

        if os.path.exists(jar_path):
            self.handle_result(cookie, 1, 'cloud not create unique copy of Tinkerforge.jar')
            return

        shutil.copy('/tmp/tester/java/Tinkerforge.jar', jar_path)

        if extra:
            shutil.copy(path, '/tmp/tester/java')
            path = os.path.join('/tmp/tester/java', os.path.split(path)[1])

        args = [os.path.join(java_common.detect_java_home(), 'bin/javac'),
                '-Xlint:all',
                '-Werror',
                '-cp',
                jar_path + ':.',
                path]

        self.execute(cookie, args)

class JavaDocTester(common.Tester):
    def __init__(self, root_dir):
        common.Tester.__init__(self, 'java', '.html', root_dir, subdirs=['javadoc/com/tinkerforge'])

    def after_unzip(self):
        print('>>> generating javadoc')

        args = [os.path.join(java_common.detect_java_home(), 'bin/javadoc'),
                '-quiet',
                '-d',
                '/tmp/tester/java/javadoc',
                '-classpath',
                '/tmp/tester/java/source/src/main/java',
                'com.tinkerforge']

        rc = subprocess.call(args)

        if rc != 0:
            print('>>> could not generate javadoc')
        else:
            print('>>> generating javadoc done\n')

        return rc == 0

    def test(self, cookie, path, extra):
        args = ['xmllint',
                '--noout',
                '--valid',
                '--html',
                path]

        self.execute(cookie, args)

    def check_success(self, exit_code, output):
        return exit_code == 0 and len(output.strip('\r\n')) == 0

def run(root_dir):
    extra_paths = [os.path.join(root_dir, '../../weather-station/examples/GuitarStation.java'),
                   os.path.join(root_dir, '../../weather-station/write_to_lcd/java/WeatherStation.java'),
                   os.path.join(root_dir, '../../hardware-hacking/remote_switch/java/RemoteSwitch.java'),
                   os.path.join(root_dir, '../../hardware-hacking/smoke_detector/java/SmokeDetector.java')]

    if not JavaExamplesTester(root_dir, extra_paths).run():
        return False

    return JavaDocTester(root_dir).run()

if __name__ == '__main__':
    run(os.getcwd())
