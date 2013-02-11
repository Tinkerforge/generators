# -*- coding: utf-8 -*-

"""
Common Generator Library
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2012-2013 Olaf Lüke <olaf@tinkerforge.com>

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
import datetime
import subprocess
import sys
import copy
from collections import namedtuple

gen_text_star = """/* ***********************************************************
 * This file was automatically generated on {0}.      *
 *                                                           *
 * Bindings Version {1}.{2}.{3}                                    *
 *                                                           *
 * If you have a bugfix for this file and want to commit it, *
 * please fix the bug in the generator. You can find a link  *
 * to the generator git on tinkerforge.com                   *
 *************************************************************/
"""

gen_text_hash = """#############################################################
# This file was automatically generated on {0}.      #
#                                                           #
# Bindings Version {1}.{2}.{3}                                    #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generator git on tinkerforge.com                   #
#############################################################
"""

gen_text_curly = """{{
  This file was automatically generated on {0}.

  Bindings Version {1}.{2}.{3}

  If you have a bugfix for this file and want to commit it,
  please fix the bug in the generator. You can find a link
  to the generator git on tinkerforge.com
}}
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

bf_str = {
'en': """
Basic Functions
^^^^^^^^^^^^^^^

{0}

{1}
""",
'de': """
Grundfunktionen
^^^^^^^^^^^^^^^

{0}

{1}
"""
}

af_str = {
'en': """
Advanced Functions
^^^^^^^^^^^^^^^^^^

{0}
""",
'de': """
Fortgeschrittene Funktionen
^^^^^^^^^^^^^^^^^^^^^^^^^^^

{0}
"""
}

ccf_str = {
'en': """
Callback Configuration Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{0}

{1}
""",
'de': """
Konfigurationsfunktionen für Callbacks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{0}

{1}
"""
}

lang = 'en'
path_binding = ''
is_doc = False

OPTION_RETURN_EXPECTED = 1 << 3
OPTION_AUTHENTICATION  = 1 << 2

def shift_right(text, n):
    return text.replace('\n', '\n' + ' '*n)

def get_changelog_version(path):
    r = re.compile('^(\d+)\.(\d+)\.(\d+):')
    last = None
    for line in file(path + '/changelog.txt', 'rb').readlines():
        m = r.match(line)

        if m is not None:
            last = (m.group(1), m.group(2), m.group(3))

    return last

def get_type_size(typ):
    types = {
        'int8'   : 1,
        'uint8'  : 1,
        'int16'  : 2,
        'uint16' : 2,
        'int32'  : 4,
        'uint32' : 4,
        'int64'  : 8,
        'uint64' : 8,
        'float'  : 4,
        'bool'   : 1,
        'string' : 1,
        'char'   : 1
    }

    return types[typ]

def get_element_size(element):
    return get_type_size(element[1]) * element[2]

def select_lang(d):
    if lang in d:
        return d[lang]
    elif 'en' in d:
        return d['en']
    else:
        return "Missing '{0}' documentation".format(lang)

def make_rst_header(device, ref_name, title):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    ref = '.. _{0}_{1}_{2}:\n'.format(device.get_underscore_name(), device.get_category().lower(), ref_name)
    title = '{0} - {1} {2}'.format(title, device.get_display_name(), device.get_category())
    title_under = '='*len(title)
    return '{0}\n{1}\n{2}\n{3}\n'.format(gen_text_rst.format(date),
                                         ref,
                                         title,
                                         title_under)

def make_rst_summary(device, title):
    su = {
    'en': """
This is the API description for the {4} of the {0} {1}. General information
on what this device does and the technical specifications can be found
:ref:`here <{2}>`.

A tutorial on how to test the {0} {1} and get the first examples running
can be found :ref:`here <{3}>`.
""",
    'de': """
Dies ist die API Beschreibung für die {4} des {0} {1}s. Allgemeine Informationen
über die Funktionen des Gerätes und die technischen Spezifikationen sind
:ref:`hier <{2}>` zu finden.

Eine Anleitung wie der {0} {1} getestet werden kann und die ersten Beispiele
ausgeführt werden können ist :ref:`hier <{3}>` zu finden.
"""
    }

    hw_link = device.get_underscore_name() + '_' + device.get_category().lower()
    hw_test = hw_link + '_test'
    return select_lang(su).format(device.get_display_name(), device.get_category(), hw_link, hw_test, title)

def make_rst_examples(title_from_file, device, base_path, dirname,
                      filename_prefix, filename_suffix, include_name):
    ex = {
    'en': """
{0}

Examples
--------

The example code below is public domain.
""",
    'de': """
{0}

Beispiele
---------

Der folgende Beispielcode ist Public Domain.
"""
    }

    imp = {
    'en': """
{0}
{1}

`Download <https://github.com/Tinkerforge/{3}/raw/master/software/examples/{4}/{5}>`__

.. literalinclude:: {2}
 :language: {4}
 :linenos:
 :tab-width: 4
""",
    'de': """
{0}
{1}

`Download <https://github.com/Tinkerforge/{3}/raw/master/software/examples/{4}/{5}>`__

.. literalinclude:: {2}
 :language: {4}
 :linenos:
 :tab-width: 4
"""
    }

    ref = '.. _{0}_{1}_{2}_examples:\n'.format(device.get_underscore_name(),
                                               device.get_category().lower(),
                                               dirname)
    examples = select_lang(ex).format(ref)
    files = find_examples(device, base_path, dirname, filename_prefix, filename_suffix)
    copy_files = []
    for f in files:
        include = '{0}_{1}_{2}_{3}'.format(device.get_camel_case_name(), device.get_category(), include_name, f[0])
        copy_files.append((f[1], include))
        title = title_from_file(f[0])
        git_name = device.get_underscore_name().replace('_', '-') + '-' + device.get_category().lower()
        examples += select_lang(imp).format(title, '^'*len(title), include, git_name, dirname, f[0])

    copy_examples(copy_files, base_path)
    return examples

def find_examples(device, base_path, dirname, filename_prefix, filename_suffix):
    start_path = base_path.replace('/generators/' + dirname, '')
    board = '{0}-{1}'.format(device.get_underscore_name(), device.get_category().lower())
    board = board.replace('_', '-')
    board_path = os.path.join(start_path, board, 'software/examples/' + dirname)
    files = []

    try:
        for f in os.listdir(board_path):
            if f.startswith(filename_prefix) and f.endswith(filename_suffix):
                f_dir = '{0}/{1}'.format(board_path, f)
                lines = 0
                for line in open(os.path.join(f, f_dir)):
                    lines += 1
                files.append((f, f_dir, lines))

        files.sort(lambda i, j: cmp(i[2], j[2]))
    except:
        return []

    return files

def copy_examples(copy_files, path):
    doc_path = '{0}/doc/{1}'.format(path, lang)
    print('  * Copying examples:')
    for copy_file in copy_files:
        doc_dest = '{0}/{1}'.format(doc_path, copy_file[1])
        doc_src = copy_file[0]
        shutil.copy(doc_src, doc_dest)
        print('   - {0}'.format(copy_file[1]))

def make_zip(dirname, source_path, dest_path, version):
    zipname = 'tinkerforge_{0}_bindings_{1}_{2}_{3}.zip'.format(dirname, *version)
    os.chdir(source_path)
    args = ['/usr/bin/zip',
            '-r',
            zipname,
            '.']
    subprocess.call(args)
    shutil.copy(zipname, dest_path)

re_camel_case_to_space = re.compile('([A-Z][A-Z][a-z])|([a-z][A-Z])')

def camel_case_to_space(name):
    return re_camel_case_to_space.sub(lambda m: m.group()[:1] + " " + m.group()[1:], name)

def handle_since_firmware(text, device, packet):
    since = packet.get_since_firmware()

    if since is not None and since != [1, 0, 0]:
        if device.get_category() == 'Brick':
            suffix = 'Firmware'
        else:
            suffix = 'Plugin'

        text += '\n.. versionadded:: {1}.{2}.{3}~({0})\n'.format(suffix, *since)

    return text

def handle_constants(text, prefix, packet, constants_name = {'en': 'constants',
                                                             'de': 'Konstanten'}):
    str_constants = {
'en': """
The following {0} are available for this function:

""",
'de': """
Die folgenden {0} sind für diese Funktion verfügbar:

"""
}
    has_constant = False
    str_constant = '* {0}{1}_{2} = {3}\n'
    str_constants = select_lang(str_constants).format(select_lang(constants_name))
    constants = packet.get_constants()
    for constant in constants:
        for definition in constant.definitions:
            if constant.type == 'char':
                value = "'{0}'".format(definition.value)
            else:
                value = str(definition.value)

            has_constant = True
            str_constants += str_constant.format(prefix,
                                                 constant.name_uppercase,
                                                 definition.name_uppercase,
                                                 value)
    if has_constant:
        return text + str_constants

    return text

def handle_rst_if(text, device):
    lines = []

    for line in text.split('\n'):
        if ':if:' in line:
            m = re.match('(.*):if:([^:]+):`([^`]+)`(.*)', line)

            if m is None:
                raise 'invalid if: ' + line

            prefix = m.group(1)
            condition = m.group(2)
            body = m.group(3)
            suffix = m.group(4)

            name = device.get_underscore_name() + '-' + device.get_category().lower()

            if name == condition:
                lines.append(prefix + body + suffix)
            elif len(prefix + suffix) > 0:
                lines.append(prefix + suffix)
        else:
            lines.append(line)

    return '\n'.join(lines)

def underscore_to_headless_camel_case(name):
    parts = name.split('_')
    ret = parts[0]
    for part in parts[1:]:
        ret += part[0].upper() + part[1:]
    return ret

def prepare_doc(directory):
    directory = os.path.join(directory, 'doc', lang)
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

def prepare_bindings(directory):
    directory += '/bindings'
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

def generate(path, language, make_files, prepare, is_doc_):
    global lang
    global path_binding
    global is_doc
    lang = language
    path_binding = path
    is_doc = is_doc_

    path_list = path.split('/')
    path_list[-1] = 'configs'
    path_config = '/'.join(path_list)
    sys.path.append(path_config)
    configs = os.listdir(path_config)

    prepare(path)

    configs.remove('device_commonconfig.py')
    configs.remove('brick_commonconfig.py')
    configs.remove('bricklet_commonconfig.py')

    common_device_packets = __import__('device_commonconfig').common_packets
    common_brick_packets = __import__('brick_commonconfig').common_packets
    common_bricklet_packets = __import__('bricklet_commonconfig').common_packets

    for config in configs:
        if config.endswith('_config.py'):
            module = __import__(config[:-3])
            print(" * {0}".format(config[:-10]))

            def prepare_common_packets(common_packets):
                for common_packet in common_packets:
                    if common_packet['since_firmware'] is None:
                        continue

                    if module.com['name'][1] in common_packet['since_firmware']:
                        common_packet['since_firmware'] = \
                            common_packet['since_firmware'][module.com['name'][1]]
                    else:
                        common_packet['since_firmware'] = \
                            common_packet['since_firmware']['*']

                return common_packets

            if 'brick_' in config and 'common_included' not in module.com:
                common_packets = copy.deepcopy(common_device_packets) + copy.deepcopy(common_brick_packets)
                module.com['packets'].extend(prepare_common_packets(common_packets))
                module.com['common_included'] = True

            if 'bricklet_' in config and 'common_included' not in module.com:
                common_packets = copy.deepcopy(common_device_packets) + copy.deepcopy(common_bricklet_packets)
                module.com['packets'].extend(prepare_common_packets(common_packets))
                module.com['common_included'] = True

            make_files(module.com, path)

def import_and_make(configs, path, make_files):
    for config in configs:
        if config.endswith('_config.py'):
            module = __import__(config[:-3])
            print(" * {0}".format(config[:-10]))
            make_files(module.com, path)

class Packet:
    def __init__(self, packet):
        self.packet = packet
        self.all_elements = packet['elements']
        self.in_elements = []
        self.out_elements = []

        if packet['name'][0].lower() != packet['name'][1].replace('_', ''):
            raise ValueError('Name mismatch: ' + packet['name'][0] + ' != ' + packet['name'][1])

        for element in self.all_elements:
            if element[3] == 'in':
                self.in_elements.append(element)
            elif element[3] == 'out':
                self.out_elements.append(element)
            else:
                raise ValueError('Invalid element direction ' + element[3])

    def get_type(self):
        return self.packet['type']

    def get_camel_case_name(self):
        return self.packet['name'][0]

    def get_headless_camel_case_name(self):
        m = re.match('([A-Z]+)(.*)', self.packet['name'][0])
        return m.group(1).lower() + m.group(2)

    def get_underscore_name(self):
        return self.packet['name'][1]

    def get_upper_case_name(self):
        return self.packet['name'][1].upper()

    def get_elements(self, direction=None):
        if direction is None:
            return self.all_elements
        elif direction == 'in':
            return self.in_elements
        elif direction == 'out':
            return self.out_elements
        else:
            raise ValueError('Invalid element direction ' + str(direction))

    def get_since_firmware(self):
        return self.packet['since_firmware']

    def get_doc(self):
        return self.packet['doc']

    def get_function_id(self):
        return self.packet['function_id']

    def get_request_length(self):
        length = 8
        for element in self.in_elements:
            length += get_element_size(element)
        return length

    def get_response_length(self):
        length = 4
        for element in self.out_elements:
            length += get_element_size(element)
        return length

    def get_constants(self):
        ConstantDefinitionTuple = namedtuple('ConstantValues', ['name_camelcase', 'name_underscore', 'name_uppercase', 'value'])
        ConstantTuple = namedtuple('Constant', ['type', 'name_camelcase', 'name_underscore', 'name_uppercase', 'definitions'])

        def is_in_constants(constants, new_constant):
            for constant in constants:
                if constant.name_camelcase == new_constant[0]:
                    return True
            return False

        constants = []

        for element in self.all_elements:
            if len(element) > 4:
                c = element[4]
                if not is_in_constants(constants, c):
                    definitions = []
                    vs = c[2]
                    for v in vs:
                        definitions.append(ConstantDefinitionTuple(v[0], v[1], v[1].upper(), v[2]))
                    constants.append(ConstantTuple(element[1], c[0], c[1], c[1].upper(), definitions))

        return constants

    def has_prototype_in_device(self):
        if 'prototype_in_device' in self.packet:
            if self.packet['prototype_in_device'] == True:
                return True
        return False

class Device:
    def __init__(self, com):
        self.com = com
        self.all_packets = []
        self.all_packets_without_doc_only = []
        self.all_function_packets = []
        self.all_function_packets_without_doc_only = []
        self.callback_packets = []

        for i, p in zip(range(len(com['packets'])), com['packets']):
            if not 'function_id' in p:
                p['function_id'] = i + 1

            packet = Packet(p)

            self.all_packets.append(packet)

            if packet.get_function_id() >= 0:
                self.all_packets_without_doc_only.append(packet)

        for packet in self.all_packets:
            if packet.get_type() == 'function':
                self.all_function_packets.append(packet)

                if packet.get_function_id() >= 0:
                    self.all_function_packets_without_doc_only.append(packet)
            elif packet.get_type() == 'callback':
                self.callback_packets.append(packet)
            else:
                raise ValueError('Invalid packet type ' + packet.get_type())

    def get_api_version(self):
        return self.com['api_version']

    def get_category(self):
        return self.com['category']

    def get_device_identifier(self):
        return self.com['device_identifier']

    def get_camel_case_name(self):
        return self.com['name'][0]

    def get_headless_camel_case_name(self):
        m = re.match('([A-Z]+)(.*)', self.com['name'][0])
        return m.group(1).lower() + m.group(2)

    def get_underscore_name(self):
        return self.com['name'][1]

    def get_upper_case_name(self):
        return self.com['name'][1].upper()

    # this is also the name stored in the firmware
    def get_display_name(self):
        return self.com['name'][2]

    def get_description(self):
        return self.com['description']

    def get_packets(self, typ=None):
        if typ is None:
            if is_doc:
                return self.all_packets
            else:
                return self.all_packets_without_doc_only
        elif typ == 'function':
            if is_doc:
                return self.all_function_packets
            else:
                return self.all_function_packets_without_doc_only
        elif typ == 'callback':
            return self.callback_packets
        else:
            raise ValueError('Invalid packet type ' + str(typ))

    def get_callback_count(self):
        return len(self.callback_packets)


    def get_constants(self):
        ConstantDefinitionTuple = namedtuple('ConstantValues', ['name_camelcase', 'name_underscore', 'name_uppercase', 'value'])
        ConstantTuple = namedtuple('Constant', ['type', 'name_camelcase', 'name_underscore', 'name_uppercase', 'definitions'])

        def is_in_constants(constants, new_constant):
            for constant in constants:
                if constant.name_camelcase == new_constant[0]:
                    return True
            return False

        constants = []

        for packet in self.all_packets:
            for element in packet.all_elements:
                if len(element) > 4:
                    c = element[4]
                    if not is_in_constants(constants, c):
                        definitions = []
                        vs = c[2]
                        for v in vs:
                            definitions.append(ConstantDefinitionTuple(v[0], v[1], v[1].upper(), v[2]))
                        constants.append(ConstantTuple(element[1], c[0], c[1], c[1].upper(), definitions))

        return constants

class ExamplesCompiler:
    def __init__(self, name, extension, path, subdirs=['examples'], comment=None):
        version = get_changelog_version(path)

        self.extension = extension
        self.path = path
        self.subdirs = subdirs
        self.comment = comment
        self.zipname = 'tinkerforge_{0}_bindings_{1}_{2}_{3}.zip'.format(name, *version)
        self.compile_count = 0
        self.failure_count = 0

    def walker(self, arg, dirname, names):
        for name in names:
            if not name.endswith(self.extension):
                continue

            src = os.path.join(dirname, name)

            self.compile_count += 1

            if self.comment is not None:
                print('>>> [{0}] compiling {1}'.format(self.comment, src))
            else:
                print('>>> compiling {0}'.format(src))

            if not self.compile(os.path.join(dirname, name)):
                self.failure_count += 1

                print('>>> compilation failed\n')
            else:
                print('>>> compilation succeded\n')

    def compile(self, src):
        return False

    def run(self):
        cwd = os.getcwd()

        # Make temporary examples directory
        if os.path.exists('/tmp/compiler'):
            shutil.rmtree('/tmp/compiler/')

        os.makedirs('/tmp/compiler')
        os.chdir('/tmp/compiler')

        shutil.copy(os.path.join(self.path, self.zipname), '/tmp/compiler/')

        # unzip
        print('>>> unpacking {0}'.format(self.zipname))

        args = ['/usr/bin/unzip',
                os.path.join('/tmp/compiler', self.zipname)]

        rc = subprocess.call(args)

        if rc != 0:
            os.chdir(cwd)
            print('### could not unpack {0}'.format(self.zipname))
            return 1

        # compile
        for subdir in self.subdirs:
            os.path.walk(os.path.join('/tmp/compiler', subdir), self.walker, None)

        # report
        if self.comment is not None:
            print('### [{0}] {1} files compiled, {2} failure(s) occurred'.format(self.comment, self.compile_count, self.failure_count))
        else:
            print('### {0} files compiled, {1} failure(s) occurred'.format(self.compile_count, self.failure_count))

        os.chdir(cwd)

        if self.failure_count > 0:
            return 1
        else:
            return 0
