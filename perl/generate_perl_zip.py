#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl ZIP Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_perl_zip.py: Generator for Perl ZIP

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
import subprocess
import glob

sys.path.append(os.path.split(os.getcwd())[0])
import common
from perl_released_files import released_files

class PerlZipGenerator(common.Generator):
    def get_bindings_name(self):
        return 'perl'

    def prepare(self):
        common.recreate_directory('/tmp/generator')
        os.makedirs('/tmp/generator/perl/source/Tinkerforge')
        os.makedirs('/tmp/generator/perl/examples')

    def generate(self, device):
        if not device.is_released():
            return

        # Copy examples
        examples = common.find_examples(device, self.get_bindings_root_directory(), self.get_bindings_name(), 'example_', '.pl')
        dest = os.path.join('/tmp/generator/perl/examples', device.get_category().lower(), device.get_underscore_name())

        if not os.path.exists(dest):
            os.makedirs(dest)

        for example in examples:
            shutil.copy(example[1], dest)

    def finish(self):
        root = self.get_bindings_root_directory()

        # Copy examples
        shutil.copy(root.replace('/generators/perl', '/doc/en/source/Software/example.pl'),
                    '/tmp/generator/perl/examples/example_enumerate.pl')

        # Copy bindings and readme
        for filename in released_files:
            shutil.copy(os.path.join(root, 'bindings', filename), '/tmp/generator/perl/source/Tinkerforge')

        shutil.copy(os.path.join(root, 'IPConnection.pm'), '/tmp/generator/perl/source/Tinkerforge')
        shutil.copy(os.path.join(root, 'Device.pm'), '/tmp/generator/perl/source/Tinkerforge')
        shutil.copy(os.path.join(root, 'changelog.txt'), '/tmp/generator/perl')
        shutil.copy(os.path.join(root, 'readme.txt'), '/tmp/generator/perl')

        # Generate the CPAN package structure
        modules = glob.glob("./bindings/*.pm")

        for i, module in enumerate(modules):
            module = module.replace("./bindings/","Tinkerforge::")
            module = module.replace(".pm","")
            modules[i] = module;
    
        modules.append("Tinkerforge::IPConnection")
        modules.append("Tinkerforge::Device")
        modules = ','.join(modules)

        if(os.path.isdir("/tmp/generator/perl/Tinkerforge")):
            subprocess.call("rm -rf /tmp/generator/perl/Tinkerforge")

        subprocess.call("module-starter --dir=/tmp/generator/perl/Tinkerforge --module="+modules+" --distro=Tinkerforge"\
        " --author=\"Ishraq Ibne Ashraf\" --email=ishraq@tinkerforge.com", shell=True)

        subprocess.call("rm -rf /tmp/generator/perl/Tinkerforge/lib/Tinkerforge/*", shell=True)
        subprocess.call("cp -ar ./bindings/* /tmp/generator/perl/Tinkerforge/lib/Tinkerforge/", shell=True)
        subprocess.call("cp -ar ./IPConnection.pm /tmp/generator/perl/Tinkerforge/lib/Tinkerforge/", shell=True)
        subprocess.call("cp -ar ./Device.pm /tmp/generator/perl/Tinkerforge/lib/Tinkerforge/", shell=True)
        subprocess.call("rm -rf /tmp/generator/perl/Tinkerforge/Makefile.PL", shell=True)
        subprocess.call("cp ./Makefile.PL /tmp/generator/perl/Tinkerforge/", shell=True)

        # Modifying 00-load.t test file
        old_test_file = open('/tmp/generator/perl/Tinkerforge/t/00-load.t')
        lines = old_test_file.readlines()
        old_test_file.close()
        
        subprocess.call("rm -rf /tmp/generator/perl/Tinkerforge/t/00-load.t", shell=True)

        new_test_file = open('/tmp/generator/perl/Tinkerforge/t/00-load.t','w')

        for i, line in enumerate(lines):
           if i == len(lines)-1:
                new_test_file.write("diag( \"Testing Tinkerforge $Tinkerforge::VERSION, Perl $], $^X\" );")
           else:
                new_test_file.write(line+"\n")

        new_test_file.close()

        # Generating the CPAN package archive and cleaning up
        subprocess.call("cd /tmp/generator/perl/Tinkerforge/ && perl /tmp/generator/perl/Tinkerforge/Makefile.PL", shell=True)
        subprocess.call("cd /tmp/generator/perl/Tinkerforge/ && make dist", shell=True)
        subprocess.call("cp /tmp/generator/perl/Tinkerforge/Tinkerforge-v2.0.0.tar.gz /tmp/generator/perl/", shell=True)
        subprocess.call("rm -rf /tmp/generator/perl/Tinkerforge/", shell=True)

        # Make zip
        version = common.get_changelog_version(root)
        common.make_zip(self.get_bindings_name(), '/tmp/generator/perl', root, version)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', PerlZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
