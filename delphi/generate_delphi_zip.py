#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Delphi/Lazarus ZIP Generator
Copyright (C) 2012-2015, 2017-2018 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_delphi_zip.py: Generator for Delphi/Lazarus ZIP

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

class DelphiZipGenerator(common.ZipGenerator):
    tmp_dir          = '/tmp/generator/delphi'
    tmp_source_dir   = os.path.join(tmp_dir, 'source')
    tmp_examples_dir = os.path.join(tmp_dir, 'examples')

    def get_bindings_name(self):
        return 'delphi'

    def prepare(self):
        common.recreate_dir(self.tmp_dir)
        os.makedirs(self.tmp_source_dir)
        os.makedirs(self.tmp_examples_dir)

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        tmp_examples_device_dir = os.path.join(self.tmp_examples_dir,
                                               device.get_camel_case_category(),
                                               device.get_camel_case_name())

        if not os.path.exists(tmp_examples_device_dir):
            os.makedirs(tmp_examples_device_dir)

        for example in common.find_device_examples(device, r'^Example.*\.pas$'):
            shutil.copy(example[1], tmp_examples_device_dir)

    def finish(self):
        root_dir = self.get_root_dir()

        # Copy IP Connection examples
        for example in common.find_examples(root_dir, r'^Example.*\.pas$'):
            shutil.copy(example[1], self.tmp_examples_dir)

        # Copy bindings and readme
        for filename in self.get_released_files():
            shutil.copy(os.path.join(self.get_bindings_dir(), filename), self.tmp_source_dir)

        shutil.copy(os.path.join(root_dir, 'Base58.pas'),                   self.tmp_source_dir)
        shutil.copy(os.path.join(root_dir, 'BlockingQueue.pas'),            self.tmp_source_dir)
        shutil.copy(os.path.join(root_dir, 'DeviceBase.pas'),               self.tmp_source_dir)
        shutil.copy(os.path.join(root_dir, 'Device.pas'),                   self.tmp_source_dir)
        shutil.copy(os.path.join(root_dir, 'IPConnection.pas'),             self.tmp_source_dir)
        shutil.copy(os.path.join(root_dir, 'LEConverter.pas'),              self.tmp_source_dir)
        shutil.copy(os.path.join(root_dir, 'TimedSemaphore.pas'),           self.tmp_source_dir)
        shutil.copy(os.path.join(root_dir, 'SHAone.pas'),                   self.tmp_source_dir)
        shutil.copy(os.path.join(root_dir, 'BrickDaemon.pas'),              self.tmp_source_dir)
        shutil.copy(os.path.join(root_dir, 'changelog.txt'),                self.tmp_dir)
        shutil.copy(os.path.join(root_dir, 'readme.txt'),                   self.tmp_dir)
        shutil.copy(os.path.join(root_dir, '..', 'configs', 'license.txt'), self.tmp_dir)

        # Make Makefile.fpc
        version = common.get_changelog_version(root_dir)
        units = sorted([filename.replace('.pas', '') for filename in os.listdir(self.tmp_source_dir)])

        common.specialize_template(os.path.join(root_dir, 'Makefile.fpc.template'),
                                   os.path.join(self.tmp_source_dir, 'Makefile.fpc'),
                                   {'<<UNITS>>': ' '.join(units),
                                    '<<VERSION>>': '.'.join(version)})

        # Make zip
        self.create_zip_file(self.tmp_dir)

def generate(root_dir):
    common.generate(root_dir, 'en', DelphiZipGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
