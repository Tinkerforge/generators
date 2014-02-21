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
from pprint import pprint
from PIL import Image

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

breadcrumbs_str = {
'en': """:breadcrumbs: <a href="../../index.html">Home</a> / <a href="../../Product_Overview.html#{0}s">{1}s</a> / {2}
""",
'de': """:breadcrumbs: <a href="../../index.html">Startseite</a> / <a href="../../Product_Overview.html#{0}s">{1}s</a> / {2}
"""
}

lang = 'en'

def shift_right(text, n):
    return text.replace('\n', '\n' + ' '*n)

def get_changelog_version(bindings_root_directory):
    r = re.compile('^(\d+)\.(\d+)\.(\d+):')
    last = None

    for line in file(os.path.join(bindings_root_directory, 'changelog.txt'), 'rb').readlines():
        m = r.match(line)

        if m is not None:
            last = (m.group(1), m.group(2), m.group(3))

    return last

def select_lang(d):
    if lang in d:
        return d[lang]
    elif 'en' in d:
        return d['en']
    else:
        return "Missing '{0}' documentation".format(lang)

def make_rst_header(device, ref_name, title, has_device_identifier_constant=True):
    category = device.get_category()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    full_title = '{0} - {1} {2}'.format(title, device.get_display_name(), category)
    full_title_underline = '='*len(full_title)
    breadcrumbs = select_lang(breadcrumbs_str).format(category.lower(), category, full_title)
    device_identifier_constant = {'en': '.. |device_identifier_constant| replace:: There is also a :ref:`constant <{0}_{1}_{2}_constants>` for the device identifier of this {3}.\n',
                                  'de': '.. |device_identifier_constant| replace:: Es gibt auch eine :ref:`Konstante <{0}_{1}_{2}_constants>` für den Device Identifier dieses {3}.\n'}
    if has_device_identifier_constant:
        device_identifier_constant = select_lang(device_identifier_constant).format(device.get_underscore_name(), category.lower(), ref_name, category)
    else:
        device_identifier_constant = '.. |device_identifier_constant| unicode:: 0xA0\n   :trim:\n'
    ref = '.. _{0}_{1}_{2}:\n'.format(device.get_underscore_name(), category.lower(), ref_name)
    return '{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n'.format(gen_text_rst.format(date),
                                                   breadcrumbs,
                                                   device_identifier_constant,
                                                   ref,
                                                   full_title,
                                                   full_title_underline)

def make_rst_summary(device, title, programming_language):
    not_released = {
    'en': """
.. note::
 {0} is currently in the prototype stage and the software/hardware
 as well as the documentation is in an incomplete state.

""",
    'de': """
.. note::
 {0} ist im Moment in der Prototyp-Phase und die Software/Hardware
 sowie die Dokumentation sind in einem unfertigen Zustand.

"""
    }

    summary = {
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

    brick = {
    'en': 'This Brick',
    'de': 'Dieser Brick'
    }

    bricklet = {
    'en': 'This Bricklet',
    'de': 'Dieses Bricklet'
    }

    hw_link = device.get_underscore_name() + '_' + device.get_category().lower()
    hw_test = hw_link + '_test'
    if programming_language is not None:
        title_link = ':ref:`{0} <api_bindings_{1}>`'.format(title, programming_language)
    else:
        title_link = title
    s = select_lang(summary).format(device.get_display_name(), device.get_category(), hw_link, hw_test, title_link)

    if not device.is_released():
        if device.get_category() == 'Brick':
            d = brick
        else:
            d = bricklet

        s = select_lang(not_released).format(select_lang(d)) + s

    return s

def make_rst_examples(title_from_file_name, device, base_path, dirname,
                      filename_prefix, filename_suffix, include_name,
                      language=None, url_fixer=None, is_picture=False,
                      additional_download_finder=None, display_name_fixer=None):
    if language is None:
       language = dirname

    ex = {
    'en': """
{0}

Examples
--------

The example code below is `Public Domain (CC0 1.0)
<http://creativecommons.org/publicdomain/zero/1.0/>`__.
""",
    'de': """
{0}

Beispiele
---------

Der folgende Beispielcode ist `Public Domain (CC0 1.0)
<http://creativecommons.org/publicdomain/zero/1.0/deed.de>`__.
"""
    }

    imp_code = """
{0}
{1}

{3}

.. literalinclude:: {2}
 :language: {4}
 :linenos:
 :tab-width: 4
"""

    imp_picture = """
{0}
{1}

{3}

.. image:: /Images/Screenshots/LabVIEW/{2}
 :scale: 100 %
 :alt: LabVIEW {0} Example
 :align: center
"""

    imp_picture_scroll = """
{0}
{1}

{3}

.. raw:: html

   <div class="horizontal-image-scroll">

.. image:: /Images/Screenshots/LabVIEW/{2}
 :scale: 100 %
 :alt: LabVIEW {0} Example
 :align: center

.. raw:: html

   </div>
"""

    download = '`Download ({0}) <{1}>`__'

    imp = imp_code
    if is_picture:
        imp = imp_picture_scroll

    ref = '.. _{0}_{1}_{2}_examples:\n'.format(device.get_underscore_name(),
                                               device.get_category().lower(),
                                               dirname)
    examples = select_lang(ex).format(ref)
    files = find_examples(device, base_path, dirname, filename_prefix, filename_suffix)
    copy_files = []

    for f in files:
        if is_picture:
            if Image.open(f[1]).size[0] > 950:
                imp = imp_picture_scroll
            else:
                imp = imp_picture

        include = '{0}_{1}_{2}_{3}'.format(device.get_camel_case_name(), device.get_category(), include_name, f[0].replace(' ', '_'))
        copy_files.append((f[1], include))
        title = title_from_file_name(f[0])
        git_name = device.get_underscore_name().replace('_', '-') + '-' + device.get_category().lower()
        url = 'https://github.com/Tinkerforge/{0}/raw/master/software/examples/{1}/{2}'.format(git_name, dirname, f[0].replace(' ', '%20'))

        if url_fixer is not None:
            url = url_fixer(url)

        display_name = f[0]

        if display_name_fixer is not None:
            display_name = display_name_fixer(display_name)

        downloads = []

        if additional_download_finder is not None:
            for additional_download in additional_download_finder(f[1]):
                additional_url = 'https://github.com/Tinkerforge/{0}/raw/master/software/examples/{1}/{2}'.format(git_name, dirname, additional_download.replace(' ', '%20'))
                downloads.append(download.format(additional_download, additional_url))

        downloads = [download.format(display_name, url)] + downloads

        examples += imp.format(title, '^'*len(title), include, ', '.join(downloads), language)

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
                ff = os.path.join(f, f_dir)

                if ff.endswith('.png'):
                    size = Image.open(ff).size
                    lines = size[0] * size[1]
                else:
                    for line in open(ff):
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

    if len(copy_files) == 0:
        print('   \033[01;31m! No examples\033[0m')

def make_zip(dirname, source_path, dest_path, version):
    zipname = 'tinkerforge_{0}_bindings_{1}_{2}_{3}.zip'.format(dirname, *version)

    with ChangedDirectory(source_path):
        args = ['/usr/bin/zip',
                '-q',
                '-r',
                zipname,
                '.']

        if subprocess.call(args) != 0:
            raise Exception("Command '{0}' failed".format(' '.join(args)))

        shutil.copy(zipname, dest_path)

re_camel_case_to_space = re.compile('([A-Z][A-Z][a-z])|([a-z][A-Z])|([a-zA-Z][0-9])')

def camel_case_to_space(name):
    return re_camel_case_to_space.sub(lambda m: m.group()[:1] + " " + m.group()[1:], name)

def format_since_firmware(device, packet):
    since = packet.get_since_firmware()

    if since is not None and since != [1, 0, 0]:
        if device.get_category() == 'Brick':
            suffix = 'Firmware'
        else:
            suffix = 'Plugin'

        return '\n.. versionadded:: {1}.{2}.{3}~({0})\n'.format(suffix, *since)
    else:
        return ''

def default_constant_format(prefix, constant_group, constant_item, value):
    return '* {0}{1}_{2} = {3}\n'.format(prefix, constant_group.get_upper_case_name(),
                                         constant_item.get_upper_case_name(), value)

def format_constants(prefix, packet,
                     constants_name={'en': 'constants', 'de': 'Konstanten'},
                     char_format="'{0}'",
                     constant_format_func=default_constant_format):
    constants_intro = {
'en': """
The following {0} are available for this function:

""",
'de': """
Die folgenden {0} sind für diese Funktion verfügbar:

"""
}
    constants = []

    for constant_group in packet.get_constant_groups():
        for constant_item in constant_group.get_items():
            if constant_group.get_type() == 'char':
                value = char_format.format(constant_item.get_value())
            else:
                value = str(constant_item.get_value())

            constants.append(constant_format_func(prefix, constant_group, constant_item, value))

    if len(constants) > 0:
        return select_lang(constants_intro).format(select_lang(constants_name)) + ''.join(constants)
    else:
        return ''

def format_function_id_constants(prefix, device,
                                 constants_name={'en': 'constants', 'de': 'Konstanten'}):
    str_constants = {
'en': """
The following function ID {0} are available for this function:

""",
'de': """
Die folgenden Funktions ID {0} sind für diese Funktion verfügbar:

"""
}
    str_constant = '* {0}FUNCTION_{1} = {2}\n'
    str_constants = select_lang(str_constants).format(select_lang(constants_name))
    for packet in device.get_packets('function'):
        if len(packet.get_elements('out')) == 0 and packet.get_function_id() >= 0:
            str_constants += str_constant.format(prefix,
                                                 packet.get_upper_case_name(),
                                                 packet.get_function_id())

    return str_constants

def handle_rst_word(text,
                    parameter={'en': 'parameter', 'de': 'Parameter'},
                    parameters={'en': 'parameters', 'de': 'Parameter'},
                    constants={'en': 'constants', 'de': 'Konstanten'}):
    text = text.replace(":word:`parameter`", select_lang(parameter))
    text = text.replace(":word:`parameters`", select_lang(parameters))
    text = text.replace(":word:`constants`", select_lang(constants))

    return text

def handle_rst_param(text, format_parameter):
    return re.sub('\:param\:\`([^\`]+)\`', lambda match: format_parameter(match.group(1)), text)

def handle_rst_substitutions(text, packet):
    subsitutions = packet.get_doc_substitutions()

    if len(subsitutions) == 0:
        return text

    for key, value in subsitutions.items():
        text = text.replace('|' + key + '|', value)

    return text

def underscore_to_headless_camel_case(name):
    parts = name.split('_')
    ret = parts[0]
    for part in parts[1:]:
        ret += part[0].upper() + part[1:]
    return ret

def underscore_to_space(name):
    ret = []
    for part in name.split('_'):
        ret.append(part[0].upper() + part[1:])
    return ' '.join(ret)

def recreate_directory(directory):
    directory = os.path.join(directory)
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

def generate(bindings_root_directory, language, generator_class):
    global lang
    lang = language

    path_config = os.path.join(bindings_root_directory, '..', 'configs')
    if path_config not in sys.path:
        sys.path.append(path_config)
    configs = sorted(os.listdir(path_config))

    configs.remove('device_commonconfig.py')
    configs.remove('brick_commonconfig.py')
    configs.remove('bricklet_commonconfig.py')

    common_device_packets = copy.deepcopy(__import__('device_commonconfig').common_packets)
    common_brick_packets = copy.deepcopy(__import__('brick_commonconfig').common_packets)
    common_bricklet_packets = copy.deepcopy(__import__('bricklet_commonconfig').common_packets)

    device_identifiers = []

    generator = generator_class(bindings_root_directory, language)

    generator.prepare()

    for config in configs:
        if config.endswith('_config.py'):
            com = copy.deepcopy(__import__(config[:-3]).com)
            if com['released']:
                print(' * {0}'.format(config[:-10]))
            else:
                print(' * {0} (not released)'.format(config[:-10]))

            def prepare_common_packets(common_packets):
                for common_packet in common_packets:
                    if common_packet['since_firmware'] is None:
                        continue

                    if com['name'][1] in common_packet['since_firmware']:
                        common_packet['since_firmware'] = \
                            common_packet['since_firmware'][com['name'][1]]
                    else:
                        common_packet['since_firmware'] = \
                            common_packet['since_firmware']['*']

                return common_packets

            if 'brick_' in config and 'common_included' not in com:
                common_packets = copy.deepcopy(common_device_packets) + copy.deepcopy(common_brick_packets)
                com['packets'].extend(prepare_common_packets(common_packets))
                com['common_included'] = True

            if 'bricklet_' in config and 'common_included' not in com:
                common_packets = copy.deepcopy(common_device_packets) + copy.deepcopy(common_bricklet_packets)
                com['packets'].extend(prepare_common_packets(common_packets))
                com['common_included'] = True

            device = generator.get_device_class()(com, generator)

            device_identifiers.append((device.get_device_identifier(), device.get_category() + ' ' + device.get_display_name()))

            generator.generate(device)

    generator.finish()

    f = open(os.path.join(bindings_root_directory, '..', 'device_identifiers.py'), 'wb')
    f.write('device_identifiers = ')
    pprint(sorted(device_identifiers),  f)
    f.close()

cn_valid_camel_case_chars = re.compile('^[A-Z][A-Za-z0-9]*$')
cn_valid_underscore_chars = re.compile('^[a-z][a-z0-9_]*$')
cn_valid_display_chars = re.compile('^[A-Z][A-Za-z0-9/ -]*$')
cn_valid_constant_camel_case_chars = re.compile('^[A-Za-z0-9]+$')
cn_valid_constant_underscore_chars = re.compile('^[a-z0-9_]+$')

cn_all_uppercase = ['api', 'ir', 'us', 'lcd', 'dc', 'imu', 'pwm', 'gps', 'io4',
                    'io16', 'led', 'i2c', 'ptc', 'rs485', 'eap', 'usb', 'mac',
                    '2d', '3d', '1k', '100k', '500k', '3v', '6v', '10v', '36v',
                    '45v', 'sps', 'oqpsk', 'bpsk40', 'dhcp', 'ip', 'wpa',
                    'wpa2', 'ca', 'wep', 'rgb']

cn_eap_suffix = ['fast', 'tls', 'ttls', 'peap', 'mschap', 'gtc']

cn_special_camel_case = {'mhz':   'MHz',
                         '20ma':  '20mA',
                         '50hz':  '50Hz',
                         '60hz':  '60Hz',
                         '1to11': '1To11',
                         '1to13': '1To13',
                         '1to14': '1To14'}

def check_name(camel_case, underscore, display, is_constant=False):
    if camel_case is not None:
        if is_constant:
            r = cn_valid_constant_camel_case_chars
        else:
            r = cn_valid_camel_case_chars

        if r.match(camel_case) is None:
            raise ValueError("camel case name '{0}' contains invalid chars".format(camel_case))

    if underscore is not None:
        if is_constant:
            r = cn_valid_constant_underscore_chars
        else:
            r = cn_valid_underscore_chars

        if r.match(underscore) is None:
            raise ValueError("underscore name '{0}' contains invalid chars".format(underscore))

    if display is not None:
        if cn_valid_display_chars.match(display) is None:
            raise ValueError("display name '{0}' contains invalid chars".format(display))

    if camel_case is not None and underscore is not None:
        # test 1
        camel_case_to_check = camel_case.lower()
        underscore_to_check = underscore.replace('_', '')

        if camel_case_to_check != underscore_to_check:
            raise ValueError("camel case name '{0}' ({1}) and underscore name '{2}' ({3}) mismatch (test 1)" \
                             .format(camel_case, camel_case_to_check, underscore, underscore_to_check))

        # test 2
        parts = []
        for part in underscore.split('_'):
            if part in cn_all_uppercase:
                parts.append(part.upper())
            elif part in cn_special_camel_case:
                parts.append(cn_special_camel_case[part])
            elif part in cn_eap_suffix and len(parts) > 0 and parts[-1] == 'EAP':
                parts.append(part.upper())
            else:
                parts.append(part[0].upper() + part[1:])

        underscore_to_check = ''.join(parts)

        if camel_case != underscore_to_check:
            raise ValueError("camel case name '{0}' and underscore name '{1}' ({2}) mismatch (test 2)" \
                             .format(camel_case, underscore, underscore_to_check))

    if camel_case is not None and display is not None:
        # test 1
        display_to_check = display.replace(' ', '').replace('-', '').replace('/', '')

        if camel_case != display_to_check:
            raise ValueError("camel case name '{0}' and display name '{1}' ({2}) mismatch (test 1)" \
                             .format(camel_case, display, display_to_check))

        # test 2
        camel_case_to_check = camel_case_to_space(camel_case)

        if camel_case in ['IO4', 'IO16']:
            camel_case_to_check = camel_case_to_check.replace(' ', '-')
        elif camel_case in ['Current12', 'Current25']:
            camel_case_to_check = camel_case_to_check.replace(' ', '')
        elif camel_case == 'VoltageCurrent':
            camel_case_to_check = camel_case_to_check.replace(' ', '/')
        elif camel_case.endswith('16x2'):
            camel_case_to_check = camel_case_to_check.replace('16x 2', '16x2')
        elif camel_case.endswith('20x4'):
            camel_case_to_check = camel_case_to_check.replace('20x 4', '20x4')
        elif camel_case.endswith('4x7'):
            camel_case_to_check = camel_case_to_check.replace('4x 7', '4x7')
        elif camel_case.endswith('020mA'):
            camel_case_to_check = camel_case_to_check.replace('020m A', '0-20mA')

        if camel_case_to_check != display:
            raise ValueError("camel case name '{0}' ({1}) and display name '{2}' mismatch (test 2)" \
                             .format(camel_case, camel_case_to_check, display))

    if underscore is not None and display is not None:
        display_to_check = display.replace(' ', '_').replace('/', '_')

        if display in ['IO-4', 'IO-16']:
            display_to_check = display_to_check.replace('-', '')
        else:
            display_to_check = display_to_check.replace('-', '_')

        display_to_check = display_to_check.lower()

        if underscore != display_to_check.lower():
            raise ValueError("underscore name '{0}' and display name '{1}' ({2}) mismatch" \
                             .format(underscore, display, display_to_check))

class ConstantItem:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def get_camel_case_name(self):
        return self.raw_data[0]

    def get_underscore_name(self):
        return self.raw_data[1]

    def get_upper_case_name(self):
        return self.get_underscore_name().upper()

    def get_dash_name(self):
        return self.get_underscore_name().replace('_', '-')

    def get_value(self):
        return self.raw_data[2]

class ConstantGroup:
    def __init__(self, element, type, raw_data, generator):
        self.type = type
        self.raw_data = raw_data
        self.elements = [element]
        self.items = []

        for item_raw_data in raw_data[2]:
            self.items.append(generator.get_constant_item_class()(item_raw_data))

    def add_elements(self, elements):
        self.elements += elements

    def get_camel_case_name(self):
        return self.raw_data[0]

    def get_underscore_name(self):
        return self.raw_data[1]

    def get_upper_case_name(self):
        return self.get_underscore_name().upper()

    def get_dash_name(self):
        return self.get_underscore_name().replace('_', '-')

    def get_type(self):
        return self.type

    def get_items(self):
        return self.items

    def get_elements(self):
        return self.elements

class Element:
    def __init__(self, packet, raw_data, generator):
        self.packet = packet
        self.raw_data = raw_data
        self.generator = generator
        self.constant_group = None

        if len(self.raw_data) > 4:
            self.constant_group = generator.get_constant_group_class()(self, self.raw_data[1], self.raw_data[4], generator)

    def get_packet(self):
        return self.packet

    def get_underscore_name(self):
        return self.raw_data[0]

    def get_headless_camel_case_name(self):
        return underscore_to_headless_camel_case(self.get_underscore_name())

    def get_dash_name(self):
        return self.get_underscore_name().replace('_', '-')

    def get_type(self):
        return self.raw_data[1]

    def get_cardinality(self):
        return self.raw_data[2]

    def get_direction(self):
        return self.raw_data[3]

    def get_constant_group(self):
        return self.constant_group

    def get_item_size(self):
        item_sizes = {
            'int8':   1,
            'uint8':  1,
            'int16':  2,
            'uint16': 2,
            'int32':  4,
            'uint32': 4,
            'int64':  8,
            'uint64': 8,
            'float':  4,
            'bool':   1,
            'char':   1,
            'string': 1
        }

        return item_sizes[self.get_type()]

    def get_size(self):
        return self.get_item_size() * self.get_cardinality()

class Packet:
    valid_types = set(['int8',
                       'uint8',
                       'int16',
                       'uint16',
                       'int32',
                       'uint32',
                       'int64',
                       'uint64',
                       'float',
                       'bool',
                       'char',
                       'string'])

    def __init__(self, device, raw_data, generator):
        self.device = device
        self.generator = generator
        self.raw_data = raw_data
        self.all_elements = []
        self.in_elements = []
        self.out_elements = []

        check_name(raw_data['name'][0], raw_data['name'][1], None)

        for raw_element in self.raw_data['elements']:
            element = generator.get_element_class()(self, raw_element, generator)

            self.all_elements.append(element)

            check_name(None, element.get_underscore_name(), None)

            if element.get_type() not in Packet.valid_types:
                raise ValueError('Invalid element type ' + element.get_type())

            if element.get_cardinality() < 1:
                raise ValueError('Invalid element size ' + element.get_cardinality())

            if element.get_direction() == 'in':
                self.in_elements.append(element)
            elif element.get_direction() == 'out':
                self.out_elements.append(element)
            else:
                raise ValueError('Invalid element direction ' + element.get_direction())

            constant_group = element.get_constant_group()

            if constant_group is not None:
                check_name(constant_group.get_camel_case_name(), constant_group.get_underscore_name(), None)

                for constant_item in constant_group.get_items():
                    check_name(constant_item.get_camel_case_name(), constant_item.get_underscore_name(), None, True)

        self.constant_groups = []

        for element in self.all_elements:
            constant_group = element.get_constant_group()

            if constant_group is None:
                continue

            for known_constant_group in self.constant_groups:
                if constant_group.get_underscore_name() != known_constant_group.get_underscore_name():
                    continue

                if constant_group.get_type() != known_constant_group.get_type():
                    raise ValueError('Multiple instance of constant group {0} with different types'.format(constant_group.get_underscore_name()))

                for constant_item, known_constant_item in zip(constant_group.get_items(), known_constant_group.get_items()):
                    a = known_constant_item.get_underscore_name()
                    b = constant_item.get_underscore_name()

                    if a != b:
                        raise ValueError('Constant item name ({0} != {1}) mismatch in constant group {2}'.format(a, b, constant_group.get_underscore_name()))

                    a = known_constant_item.get_value()
                    b = constant_item.get_value()

                    if a != b:
                        raise ValueError('Constant item value ({0} != {1}) mismatch in constant group {2}'.format(a, b, constant_group.get_underscore_name()))

                known_constant_group.add_elements(constant_group.get_elements())

                constant_group = None

                break

            if constant_group is not None:
                self.constant_groups.append(constant_group)

    def get_device(self):
        return self.device

    def get_type(self):
        return self.raw_data['type']

    def get_camel_case_name(self):
        return self.raw_data['name'][0]

    def get_headless_camel_case_name(self):
        m = re.match('([A-Z]+)(.*)', self.get_camel_case_name())
        return m.group(1).lower() + m.group(2)

    def get_underscore_name(self):
        return self.raw_data['name'][1]

    def get_upper_case_name(self):
        return self.get_underscore_name().upper()

    def get_dash_name(self):
        return self.get_underscore_name().replace('_', '-')

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
        return self.raw_data['since_firmware']

    def get_doc(self):
        return self.raw_data['doc']

    def get_doc_substitutions(self):
        doc = self.get_doc()

        if len(doc) < 3:
            return []

        if lang in doc[2]:
            subsitutions = doc[2][lang]
        else:
            subsitutions = doc[2]['*']

        filtered_subsitutions = {}
        bindings_name = self.get_device().get_generator().get_bindings_name()

        for key, value in subsitutions.items():
            if bindings_name in value:
                filtered_subsitutions[key] = value[bindings_name]
            else:
                filtered_subsitutions[key] = value['*']

        return filtered_subsitutions

    def get_function_id(self):
        return self.raw_data['function_id']

    def get_request_size(self):
        size = 8 # header
        for element in self.in_elements:
            size += element.get_size()
        return size

    def get_response_size(self):
        size = 8 # header
        for element in self.out_elements:
            size += element.get_size()
        return size

    def get_constant_groups(self):
        return self.constant_groups

    def get_formatted_constants(self, constant_format, char_format="'{0}'", **extra_value):
        constants = []

        for constant_group in self.get_constant_groups():
            for constant_item in constant_group.get_items():
                if constant_group.get_type() == 'char':
                    value = char_format.format(constant_item.get_value())
                else:
                    value = str(constant_item.get_value())

                constants.append(constant_format.format(constant_group_upper_case_name=constant_group.get_upper_case_name(),
                                                        constant_item_upper_case_name=constant_item.get_upper_case_name(),
                                                        constant_item_value=value,
                                                        **extra_value))

        return ''.join(constants)

    def has_prototype_in_device(self):
        if 'prototype_in_device' in self.raw_data:
            if self.raw_data['prototype_in_device']:
                return True
        return False

    def is_virtual(self):
        if 'is_virtual' in self.raw_data:
            if self.raw_data['is_virtual']:
                return True
        return False

class Device:
    def __init__(self, raw_data, generator):
        self.raw_data = raw_data
        self.generator = generator
        self.all_packets = []
        self.all_packets_without_doc_only = []
        self.all_function_packets = []
        self.all_function_packets_without_doc_only = []
        self.callback_packets = []

        check_name(raw_data['name'][0], raw_data['name'][1], raw_data['name'][2])

        for i, p in zip(range(len(raw_data['packets'])), raw_data['packets']):
            if not 'function_id' in p:
                p['function_id'] = i + 1

            packet = generator.get_packet_class()(self, p, generator)

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

        self.constant_groups = []

        for packet in self.all_packets:
            for constant_group in packet.get_constant_groups():
                for known_constant_group in self.constant_groups:
                    if constant_group.get_underscore_name() != known_constant_group.get_underscore_name():
                        continue

                    if constant_group.get_type() != known_constant_group.get_type():
                        raise ValueError('Multiple instance of constant group {0} with different types'.format(constant_group.get_underscore_name()))

                    for constant_item, known_constant_item in zip(constant_group.get_items(), known_constant_group.get_items()):
                        a = known_constant_item.get_underscore_name()
                        b = constant_item.get_underscore_name()

                        if a != b:
                            raise ValueError('Constant item name ({0} != {1}) mismatch in constant group {2}'.format(a, b, constant_group.get_underscore_name()))

                        a = known_constant_item.get_value()
                        b = constant_item.get_value()

                        if a != b:
                            raise ValueError('Constant item value ({0} != {1}) mismatch in constant group {2}'.format(a, b, constant_group.get_underscore_name()))

                    constant_group = None

                    break

                if constant_group is not None:
                    self.constant_groups.append(constant_group)

    def get_generator(self):
        return self.generator

    def is_released(self):
        return self.raw_data['released']

    def get_api_version(self):
        return self.raw_data['api_version']

    def get_api_doc(self):
        if 'api' in self.raw_data:
            return select_lang(self.raw_data['api'])
        else:
            return ''

    def get_category(self):
        return self.raw_data['category']

    def get_device_identifier(self):
        return self.raw_data['device_identifier']

    def get_camel_case_name(self):
        return self.raw_data['name'][0]

    def get_headless_camel_case_name(self):
        m = re.match('([A-Z]+)(.*)', self.get_camel_case_name())
        return m.group(1).lower() + m.group(2)

    def get_underscore_name(self):
        return self.raw_data['name'][1]

    def get_upper_case_name(self):
        return self.get_underscore_name().upper()

    def get_dash_name(self):
        return self.get_underscore_name().replace('_', '-')

    def get_display_name(self):
        return self.raw_data['name'][2]

    def get_description(self):
        return self.raw_data['description']

    def get_packets(self, type=None):
        if type is None:
            if self.generator.is_doc():
                return self.all_packets
            else:
                return self.all_packets_without_doc_only
        elif type == 'function':
            if self.generator.is_doc():
                return self.all_function_packets
            else:
                return self.all_function_packets_without_doc_only
        elif type == 'callback':
            return self.callback_packets
        else:
            raise ValueError('Invalid packet type ' + str(type))

    def get_callback_count(self):
        return len(self.callback_packets)

    def get_constant_groups(self):
        return self.constant_groups

    def get_formatted_constants(self, constant_format, char_format="'{0}'", **extra_value):
        constants = []

        for constant_group in self.get_constant_groups():
            for constant_item in constant_group.get_items():
                if constant_group.get_type() == 'char':
                    value = char_format.format(constant_item.get_value())
                else:
                    value = str(constant_item.get_value())

                constants.append(constant_format.format(constant_group_upper_case_name=constant_group.get_upper_case_name(),
                                                        constant_group_camel_case_name=constant_group.get_camel_case_name(),
                                                        constant_item_upper_case_name=constant_item.get_upper_case_name(),
                                                        constant_item_camel_case_name=constant_item.get_camel_case_name(),
                                                        constant_item_value=value,
                                                        **extra_value))

        return ''.join(constants)

class Generator:
    def __init__(self, bindings_root_directory, language):
        self.bindings_root_directory = bindings_root_directory
        self.language = language

    def get_bindings_name(self):
        raise Exception("get_bindings_name not implemented")

    def get_device_class(self):
        return Device

    def get_packet_class(self):
        return Packet

    def get_element_class(self):
        return Element

    def get_constant_group_class(self):
        return ConstantGroup

    def get_constant_item_class(self):
        return ConstantItem

    def get_bindings_root_directory(self):
        return self.bindings_root_directory

    def get_language(self):
        return self.language

    def is_doc(self):
        return False

    def prepare(self):
        pass

    def generate(self, device):
        pass

    def finish(self):
        pass

class DocGenerator(Generator):
    def is_doc(self):
        return True

    def prepare(self):
        recreate_directory(os.path.join(self.get_bindings_root_directory(), 'doc', self.get_language()))

class BindingsGenerator(Generator):
    released_files_name_prefix = None
    recreate_bindings_subdirectory = True

    def __init__(self, *args, **kwargs):
        Generator.__init__(self, *args, **kwargs)

        self.released_files = []

    def prepare(self):
        if self.recreate_bindings_subdirectory:
            recreate_directory(os.path.join(self.get_bindings_root_directory(), 'bindings'))

    def finish(self):
        if self.released_files_name_prefix is None:
            if len(self.released_files) > 0:
                raise Exception("Released files in list but name prefix not set")
        else:
            py = open(os.path.join(self.get_bindings_root_directory(), self.released_files_name_prefix + '_released_files.py'), 'wb')
            py.write('released_files = ' + repr(self.released_files))
            py.close()

class ExamplesCompiler:
    def __init__(self, name, extension, path, subdirs=['examples'], comment=None, extra_examples=[]):
        version = get_changelog_version(path)

        self.extension = extension
        self.path = path
        self.subdirs = subdirs[:]
        self.comment = comment
        self.extra_examples = extra_examples[:]
        self.zipname = 'tinkerforge_{0}_bindings_{1}_{2}_{3}.zip'.format(name, *version)
        self.compile_count = 0
        self.failure_count = 0

    def walker(self, arg, dirname, names):
        for name in names:
            if not name.endswith(self.extension):
                continue

            self.handle_source(os.path.join(dirname, name), False)

    def handle_source(self, src, is_extra_example):
        self.compile_count += 1

        if self.comment is not None:
            print('>>> [{0}] compiling {1}'.format(self.comment, src))
        else:
            print('>>> compiling {0}'.format(src))

        if not self.compile(src, is_extra_example):
            self.failure_count += 1

            print('>>> compilation failed\n')
        else:
            print('>>> compilation succeded\n')

    def compile(self, src, is_extra_example):
        return False

    def run(self):
        # Make temporary examples directory
        if os.path.exists('/tmp/compiler'):
            shutil.rmtree('/tmp/compiler/')

        os.makedirs('/tmp/compiler')

        with ChangedDirectory('/tmp/compiler'):
            shutil.copy(os.path.join(self.path, self.zipname), '/tmp/compiler/')

            # unzip
            print('>>> unpacking {0}'.format(self.zipname))

            args = ['/usr/bin/unzip',
                    '-q',
                    os.path.join('/tmp/compiler', self.zipname)]

            rc = subprocess.call(args)

            if rc != 0:
                print('### could not unpack {0}'.format(self.zipname))
                return 1

            # compile
            for subdir in self.subdirs:
                os.path.walk(os.path.join('/tmp/compiler', subdir), self.walker, None)

            for extra_example in self.extra_examples:
                self.handle_source(extra_example, True)

            # report
            if self.comment is not None:
                print('### [{0}] {1} files compiled, {2} failure(s) occurred'.format(self.comment, self.compile_count, self.failure_count))
            else:
                print('### {0} files compiled, {1} failure(s) occurred'.format(self.compile_count, self.failure_count))

        if self.failure_count > 0:
            return 1
        else:
            return 0

# use "with ChangedDirectory('/path/to/abc')" instead of "os.chdir('/path/to/abc')"
class ChangedDirectory:
    def __init__(self, directory):
        self.directory = directory

    def __enter__(self):
        self.previous_directory = os.getcwd()
        os.chdir(self.directory)

    def __exit__(self, type, value, traceback):
        os.chdir(self.previous_directory)
