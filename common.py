# -*- coding: utf-8 -*-

"""
Common Generator Library
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

common.py: Common Library for generation of bindings and documentation

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

import os
import shutil
import re

gen_text_star = """/* ***********************************************************
 * This file was automatically generated on {0}.      *
 *                                                           *
 * If you have a bugfix for this file and want to commit it, *
 * please fix the bug in the generator. You can find a link  *
 * to the generator git on tinkerforge.com                   *
 *************************************************************/
"""

gen_text_hash = """#############################################################
# This file was automatically generated on {0}.      #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generator git on tinkerforge.com                   #
#############################################################
"""

gen_text_rst = """..
 #############################################################
 # This file was automatically generated on {0}.      #
 #                                                           #
 # If you have a bugfix for this file and want to commit it, #
 # please fix the bug in the generator. You can find a link  #
 # to the generator git on tinkerforge.com                   #
 #############################################################
"""

def shift_right(text, n):
    return text.replace('\n', '\n' + ' '*n)

def get_changelog_version(path):
    r = re.compile('^(\d+)\.(\d+)\.(\d+):')
    last = None
    for line in file(path + '/changelog.txt').readlines():
        m = r.match(line)

        if m is not None:
            last = (m.group(1), m.group(2), m.group(3))

    return last

def find_examples(com, path, dirname, prefix, suffix):
    start_path = path.replace('/generators/' + dirname, '')
    board = '{0}-{1}'.format(com['name'][1], com['category'].lower())
    board = board.replace('_', '-')
    board_path = os.path.join(start_path, board, 'software/examples/' + dirname)
    files = []
    for f in os.listdir(board_path):
        if f.startswith(prefix) and f.endswith(suffix):
            f_dir = '{0}/{1}'.format(board_path, f)
            lines = 0
            for line in open(os.path.join(f, f_dir)):
                lines += 1
            files.append((f, f_dir, lines))

    files.sort(lambda i, j: cmp(i[2], j[2]))

    return files

def copy_examples(copy_files, path):
    doc_path = '{0}/doc'.format(path)
    print('  * Copying examples:')
    for copy_file in copy_files:
        doc_dest = '{0}/{1}'.format(doc_path, copy_file[1])
        doc_src = copy_file[0]
        shutil.copy(doc_src, doc_dest)
        print('   - {0}'.format(copy_file[1]))

re_camel_case_to_space = re.compile('([A-Z][A-Z][a-z])|([a-z][A-Z])')

def camel_case_to_space(name):
    return re_camel_case_to_space.sub(lambda m: m.group()[:1] + " " + m.group()[1:], name)

class Device:
    def __init__(self, com):
        self.com = com
        self.all_packets = []
        self.function_packets = []
        self.callback_packets = []

        for i, packet in zip(range(len(com['packets'])), com['packets']):
            packet['function_id'] = i + 1
            self.all_packets.append(packet)

        for packet in self.all_packets:
            if packet['type'] == 'function':
                self.function_packets.append(packet)
            elif packet['type'] == 'callback':
                self.callback_packets.append(packet)
            else:
                raise ValueError('Invalid packet type ' + packet['type'])

    def get_version(self):
        return self.com['version']

    def get_category(self):
        return self.com['category']

    def get_camel_case_name(self):
        return self.com['name'][0]

    def get_headless_camel_case_name(self):
        m = re.match('([A-Z]+)(.*)', self.com['name'][0])
        return m.group(1).lower() + m.group(2)

    def get_underscore_name(self):
        return self.com['name'][1]

    # this is also the name stored in the firmware
    def get_display_name(self):
        return self.com['name'][2]

    def get_description(self):
        return self.com['description']

    def get_packets(self, typ=None):
        if typ is None:
            return self.all_packets
        elif typ == 'function':
            return self.function_packets
        elif typ == 'callback':
            return self.callback_packets
        else:
            raise ValueError('Invalid packet type ' + str(typ))

    def get_callback_count(self):
        return len(self.callback_packets)
