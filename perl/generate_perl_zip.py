#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl ZIP Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_perl_zip.py: Generator for Perl ZIP

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
        os.makedirs('/tmp/generator/cpan/source/lib/Tinkerforge')
        os.makedirs('/tmp/generator/cpan/examples')

    def generate(self, device):
        if not device.is_released():
            return

        # Copy device examples
        examples = common.find_device_examples(device, '^example_.*\.pl$')
        dest = os.path.join('/tmp/generator/cpan/examples', device.get_category().lower(), device.get_underscore_name())

        if not os.path.exists(dest):
            os.makedirs(dest)

        for example in examples:
            shutil.copy(example[1], dest)

    def finish(self):
        root = self.get_bindings_root_directory()
        version = common.get_changelog_version(root)
        dot_version = "{0}.{1}.{2}".format(*version)

        # Copy IPConnection examples
        examples = common.find_examples(root, '^example_.*\.pl$')
        for example in examples:
            shutil.copy(example[1], '/tmp/generator/cpan/examples')

        # Copy bindings and readme
        for filename in released_files:
            shutil.copy(os.path.join(root, 'bindings', filename), '/tmp/generator/cpan/source/lib/Tinkerforge')

        shutil.copy(os.path.join(root, 'IPConnection.pm'), '/tmp/generator/cpan/source/lib/Tinkerforge')
        shutil.copy(os.path.join(root, 'Device.pm'), '/tmp/generator/cpan/source/lib/Tinkerforge')
        shutil.copy(os.path.join(root, 'Error.pm'), '/tmp/generator/cpan/source/lib/Tinkerforge')
        shutil.copy(os.path.join(root, 'changelog.txt'), '/tmp/generator/cpan')
        shutil.copy(os.path.join(root, 'readme.txt'), '/tmp/generator/cpan')

        # Generate the CPAN package structure
        modules = []

        for filename in released_files:
            modules.append('Tinkerforge::' + filename.replace('.pm', ''))

        modules.append("Tinkerforge::IPConnection")
        modules.append("Tinkerforge::Device")
        modules.append("Tinkerforge::Error")
        modules.append("Tinkerforge")

        modules = ','.join(modules)

        if os.path.exists('/tmp/generator/cpan/Tinkerforge'):
            shutil.rmtree('/tmp/generator/cpan/Tinkerforge')

        subprocess.call("module-starter --dir=/tmp/generator/cpan/Tinkerforge --module={0} --distro=Tinkerforge"
                        " --author=\"Ishraq Ibne Ashraf\" --email=ishraq@tinkerforge.com".format(modules), shell=True)

        # Version replacing
        common.replace_in_file(os.path.join(root, 'Tinkerforge.pm.template'),
                               '/tmp/generator/cpan/Tinkerforge/lib/Tinkerforge.pm',
                               '<TF_API_VERSION>', dot_version)
        shutil.copy('/tmp/generator/cpan/Tinkerforge/lib/Tinkerforge.pm', '/tmp/generator/cpan/source/lib')
        common.replace_in_file(os.path.join(root, 'README.template'),
                               '/tmp/generator/cpan/Tinkerforge/README',
                               '<TF_API_VERSION>', dot_version)

        # Copying bindings
        subprocess.call("rm -rf /tmp/generator/cpan/Tinkerforge/lib/Tinkerforge/*", shell=True)

        for filename in released_files:
            subprocess.call("cp -ar {0}/bindings/{1} /tmp/generator/cpan/Tinkerforge/lib/Tinkerforge/".format(root, filename), shell=True)

        # Copying IPconnection.pm, Device.pm and Error.pm
        subprocess.call("cp -ar {0}/IPConnection.pm /tmp/generator/cpan/Tinkerforge/lib/Tinkerforge/".format(root), shell=True)
        subprocess.call("cp -ar {0}/Device.pm /tmp/generator/cpan/Tinkerforge/lib/Tinkerforge/".format(root), shell=True)
        subprocess.call("cp -ar {0}/Error.pm /tmp/generator/cpan/Tinkerforge/lib/Tinkerforge/".format(root), shell=True)

        # Copying Changes
        subprocess.call("rm -rf /tmp/generator/cpan/Tinkerforge/Changes", shell=True)
        subprocess.call("cp -ar {0}/changelog.txt /tmp/generator/cpan/Tinkerforge/Changes".format(root), shell=True)

        # Copying Makefile.PL
        subprocess.call("rm -rf /tmp/generator/cpan/Tinkerforge/Makefile.PL", shell=True)
        subprocess.call("cp {0}/Makefile.PL /tmp/generator/cpan/Tinkerforge/Makefile.PL".format(root), shell=True)
        subprocess.call("cp {0}/Makefile.PL /tmp/generator/cpan/source/Makefile.PL".format(root), shell=True)

        # Modifying 00-load.t test file
        old_test_file = open('/tmp/generator/cpan/Tinkerforge/t/00-load.t')
        lines = old_test_file.readlines()
        old_test_file.close()

        subprocess.call("rm -rf /tmp/generator/cpan/Tinkerforge/t/00-load.t", shell=True)

        new_test_file = open('/tmp/generator/cpan/Tinkerforge/t/00-load.t','w')

        for i, line in enumerate(lines):
            if i == len(lines)-1:
                new_test_file.write("diag( \"Testing Tinkerforge $Tinkerforge::VERSION, Perl $], $^X\" );")
            else:
                new_test_file.write(line+"\n")

        new_test_file.close()

        # Generating the CPAN package archive and cleaning up
        subprocess.call("cd /tmp/generator/cpan/Tinkerforge/ && perl /tmp/generator/cpan/Tinkerforge/Makefile.PL", shell=True)
        subprocess.call("cd /tmp/generator/cpan/Tinkerforge/ && make dist", shell=True)
        shutil.copy("/tmp/generator/cpan/Tinkerforge/Tinkerforge-{0}.{1}.{2}.tar.gz".format(*version), root)
        shutil.rmtree('/tmp/generator/cpan/Tinkerforge')

        # Make zip
        common.make_zip(self.get_bindings_name(), '/tmp/generator/cpan', root, version)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', PerlZipGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
