# -*- coding: utf-8 -*-

"""
Common Generator Library
Copyright (C) 2012-2015 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2012-2015 Olaf Lüke <olaf@tinkerforge.com>

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
import multiprocessing.dummy
from collections import namedtuple
from pprint import pprint

gen_text_star = """/* ***********************************************************
 * This file was automatically generated on {0}.      *
 *                                                           *
 * Bindings Version {1}.{2}.{3}                                    *
 *                                                           *
 * If you have a bugfix for this file and want to commit it, *
 * please fix the bug in the generator. You can find a link  *
 * to the generators git repository on tinkerforge.com       *
 *************************************************************/
"""

gen_text_hash = """#############################################################
# This file was automatically generated on {0}.      #
#                                                           #
# Bindings Version {1}.{2}.{3}                                    #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generators git repository on tinkerforge.com       #
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
 # to the generators git repository on tinkerforge.com       #
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
'en': """:breadcrumbs: <a href="../../index.html">Home</a> / <a href="../../index.html#software-{0}">Software</a> / {1}
""",
'de': """:breadcrumbs: <a href="../../index.html">Startseite</a> / <a href="../../index.html#software-{0}">Software</a> / {1}
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

def get_image_size(path):
    from PIL import Image

    return Image.open(path).size

def select_lang(d):
    if lang in d:
        return d[lang]
    elif 'en' in d:
        return d['en']
    else:
        return "Missing '{0}' documentation".format(lang)

def make_rst_header(device, has_device_identifier_constant=True):
    bindings_display_name = device.get_generator().get_bindings_display_name()
    ref_name = device.get_generator().get_bindings_name()
    category = device.get_category()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    full_title = '{0} - {1}'.format(bindings_display_name, device.get_long_display_name())
    full_title_underline = '='*len(full_title)
    breadcrumbs = select_lang(breadcrumbs_str).format(ref_name, full_title)
    device_identifier_constant = {'en': '.. |device_identifier_constant| replace:: There is also a :ref:`constant <{0}_{1}_{2}_constants>` for the device identifier of this {3}.\n',
                                  'de': '.. |device_identifier_constant| replace:: Es gibt auch eine :ref:`Konstante <{0}_{1}_{2}_constants>` für den Device Identifier dieses {3}.\n'}

    if device.is_released():
        orphan = ''
    else:
        orphan = ':orphan:'

    if has_device_identifier_constant:
        device_identifier_constant = select_lang(device_identifier_constant).format(device.get_underscore_name(), category.lower(), ref_name, category)
    else:
        device_identifier_constant = '.. |device_identifier_constant| unicode:: 0xA0\n   :trim:\n'

    ref = '.. _{0}_{1}_{2}:\n'.format(device.get_underscore_name(), category.lower(), ref_name)

    return '{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n'.format(gen_text_rst.format(date),
                                                        orphan,
                                                        breadcrumbs,
                                                        device_identifier_constant,
                                                        ref,
                                                        full_title,
                                                        full_title_underline)

def make_rst_summary(device, is_programming_language=True):
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
This is the description {0} for {1}. General information and technical
specifications for the {2} are summarized in its :ref:`hardware description
<{3}_description>`.
""",
    'de': """
Dies ist die Beschreibung {0} für {1}. Allgemeine Informationen über
die Funktionen und technischen Spezifikationen des {2} sind in dessen
:ref:`Hardware Beschreibung <{3}_description>` zusammengefasst.
"""
    }

    summary_install = {
    'en': """
An :ref:`installation guide <api_bindings_{0}_install>` for the {1} API
bindings is part of their general description.
""",
    'de': """
Eine :ref:`Installationanleitung <api_bindings_{0}_install>` für die {1} API
Bindings ist Teil deren allgemeine Beschreibung.
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

    programming_language_name_link = {
    'en': 'of the :ref:`{0} API bindings <api_bindings_{1}>`',
    'de': 'der :ref:`{0} API Bindings <api_bindings_{1}>`'
    }

    protocol_name_link = {
    'en': 'of the :ref:`{0} protocol <llproto_{1}>`',
    'de': 'des :ref:`{0} Protokolls <llproto_{1}>`'
    }

    brick_name = {
    'en': 'the :ref:`{0} <{1}_brick>`',
    'de': 'den :ref:`{0} <{1}_brick>`',
    }

    bricklet_name = {
    'en': 'the :ref:`{0} <{1}_bricklet>`',
    'de': 'das :ref:`{0} <{1}_bricklet>`',
    }

    # format bindings name
    if is_programming_language:
        bindings_name_link = select_lang(programming_language_name_link)
    else:
        bindings_name_link = select_lang(protocol_name_link)

    bindings_name_link = bindings_name_link.format(device.get_generator().get_bindings_display_name(),
                                                   device.get_generator().get_bindings_name())

    # format device name
    if device.get_category() == 'Brick':
        device_name = select_lang(brick_name)
    else:
        device_name = select_lang(bricklet_name)

    device_name = device_name.format(device.get_long_display_name(),
                                     device.get_underscore_name())

    s = select_lang(summary).format(bindings_name_link,
                                    device_name,
                                    device.get_long_display_name(),
                                    device.get_underscore_name() + '_' + device.get_category().lower())

    if is_programming_language:
        s += select_lang(summary_install).format(device.get_generator().get_bindings_name(),
                                                 device.get_generator().get_bindings_display_name())

    if not device.is_released():
        if device.get_category() == 'Brick':
            d = brick
        else:
            d = bricklet

        s = select_lang(not_released).format(select_lang(d)) + s

    return s

def make_rst_examples(title_from_filename, device,
                      url_fixer=None, is_picture=False, additional_download_finder=None,
                      display_name_fixer=None, language_from_filename=None,
                      add_test_link=False):
    bindings_name = device.get_generator().get_bindings_name()
    filename_regex = device.get_generator().get_doc_example_regex()

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
    url_format = 'https://github.com/Tinkerforge/{0}/raw/master/software/examples/{1}/{2}'

    imp = imp_code
    if is_picture:
        imp = imp_picture_scroll

    ref = '.. _{0}_{1}_{2}_examples:\n'.format(device.get_underscore_name(),
                                               device.get_category().lower(),
                                               bindings_name)
    examples = select_lang(ex).format(ref)
    files = find_device_examples(device, filename_regex)
    copy_files = []
    include_name = device.get_generator().get_doc_rst_filename_part()

    for f in files:
        if is_picture:
            if get_image_size(f[1])[0] > 950:
                imp = imp_picture_scroll
            else:
                imp = imp_picture

        if language_from_filename is None:
            language = bindings_name
        else:
            language = language_from_filename(f[0])

        include = '{0}_{1}_{2}_{3}'.format(device.get_camel_case_name(), device.get_category(), include_name, f[0].replace(' ', '_'))
        copy_files.append((f[1], include))
        title = title_from_filename(f[0])
        git_name = device.get_underscore_name().replace('_', '-') + '-' + device.get_category().lower()
        url = url_format.format(git_name, bindings_name, f[0].replace(' ', '%20'))

        if url_fixer is not None:
            url = url_fixer(url)

        display_name = f[0]

        if display_name_fixer is not None:
            display_name = display_name_fixer(display_name)

        downloads = []

        if additional_download_finder is not None:
            for additional_download in additional_download_finder(f[1]):
                additional_url = url_format.format(git_name, bindings_name, additional_download.replace(' ', '%20'))
                downloads.append(download.format(additional_download, additional_url))

        downloads = [download.format(display_name, url)] + downloads

        if add_test_link and include.endswith('.html'):
            downloads.append('`Test ({0}) <http://www.tinkerforge.com/{1}/doc/Software/Examples/JavaScript/{2}>`__'.format(display_name, lang, include))

        examples += imp.format(title, '^'*len(title), include, ', '.join(downloads), language)

    copy_examples(copy_files, device.get_generator().get_bindings_root_directory())
    return examples

def default_example_compare(i, j):
    c = cmp(i[2], j[2]) # lines

    if c != 0:
        return c

    return cmp(i[0], j[0]) # filename

def find_examples(examples_directory, filename_regex, compare_examples=default_example_compare):
    compiled_filename_regex = re.compile(filename_regex)
    examples = []

    if os.path.isdir(examples_directory):
        for example_filename in sorted(os.listdir(examples_directory)):
            if compiled_filename_regex.match(example_filename) is not None:
                example_path = os.path.join(examples_directory, example_filename)
                lines = 0

                if example_path.endswith('.png'):
                    size = get_image_size(example_path)
                    lines = size[0] * size[1]
                else:
                    for line in open(example_path):
                        lines += 1

                examples.append((example_filename, example_path, lines))

        examples.sort(compare_examples)

    return examples

def find_device_examples(device, filename_regex):
    bindings_name = device.get_generator().get_bindings_name()
    examples_directory = os.path.join(device.get_git_directory(), 'software', 'examples', bindings_name)

    return find_examples(examples_directory, filename_regex, device.get_generator().compare_examples)

def copy_examples(copy_files, path):
    doc_path = os.path.join(path, 'doc', lang)
    print('  * Copying examples:')
    for copy_file in copy_files:
        doc_dest = os.path.join(doc_path, copy_file[1])
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

    if since is not None and since > [2, 0, 0]:
        if device.get_category() == 'Brick':
            suffix = 'Firmware'
        else:
            suffix = 'Plugin'

        return '\n.. versionadded:: {1}.{2}.{3}$nbsp;({0})\n'.format(suffix, *since)
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

def make_headless_camel_case(camel_case_name, underscore_name):
    prefix_len = len(underscore_name.split('_')[0])

    return camel_case_name[:prefix_len].lower() + camel_case_name[prefix_len:]

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
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

def specialize_template(template_filename, destination_filename, replacements):
    template_file = open(template_filename, 'rb')
    lines = []
    replaced = set()

    for line in template_file.readlines():
        for key in replacements:
            replaced_line = line.replace(key, replacements[key])

            if replaced_line != line:
                replaced.add(key)

            line = replaced_line

        lines.append(line)

    template_file.close()

    if replaced != set(replacements.keys()):
        raise Exception('Not all replacements for {0} have been applied'.format(template_filename))

    destination_file = open(destination_filename, 'wb')
    destination_file.writelines(lines)
    destination_file.close()

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

    brick_infos = []
    bricklet_infos = []

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

                    if common_packet['since_firmware'] is None:
                        common_packet['to_be_removed'] = True

                return filter(lambda x: 'to_be_removed' not in x, common_packets)

            if 'brick_' in config and 'common_included' not in com:
                common_packets = copy.deepcopy(common_device_packets) + copy.deepcopy(common_brick_packets)
                com['packets'].extend(prepare_common_packets(common_packets))
                com['common_included'] = True

            if 'bricklet_' in config and 'common_included' not in com:
                common_packets = copy.deepcopy(common_device_packets) + copy.deepcopy(common_bricklet_packets)
                com['packets'].extend(prepare_common_packets(common_packets))
                com['common_included'] = True

            device = generator.get_device_class()(com, generator)

            if device.get_category() == 'Brick':
                ref_name = device.get_underscore_name() + '_brick'
                hardware_doc_name = device.get_short_display_name().replace(' ', '_').replace('/', '_').replace('-', '').replace('2.0', 'V2') + '_Brick'
                software_doc_prefix = device.get_camel_case_name() + '_Brick'
                git_name = device.get_underscore_name().replace('_', '-') + '-brick'

                if device.get_device_identifier() != 17:
                    firmware_url_part = device.get_underscore_name()
                else:
                    firmware_url_part = None

                device_info = (device.get_device_identifier(),
                               device.get_long_display_name(),
                               device.get_short_display_name(),
                               ref_name,
                               hardware_doc_name,
                               software_doc_prefix,
                               git_name,
                               firmware_url_part,
                               device.is_released(),
                               True,
                               {
                                   'en': device.get_description('en'),
                                   'de': device.get_description('de')
                               })

                brick_infos.append(device_info)
            else:
                ref_name = device.get_underscore_name() + '_bricklet'
                hardware_doc_name = device.get_short_display_name().replace(' ', '_').replace('/', '_').replace('-', '').replace('2.0', 'V2')
                software_doc_prefix = device.get_camel_case_name() + '_Bricklet'
                git_name = device.get_underscore_name().replace('_', '-') + '-bricklet'
                firmware_url_part = device.get_underscore_name()

                device_info = (device.get_device_identifier(),
                               device.get_long_display_name(),
                               device.get_short_display_name(),
                               ref_name,
                               hardware_doc_name,
                               software_doc_prefix,
                               git_name,
                               firmware_url_part,
                               device.is_released(),
                               True,
                               {
                                   'en': device.get_description('en'),
                                   'de': device.get_description('de')
                               })

                bricklet_infos.append(device_info)

            generator.generate(device)

    generator.finish()

    brick_infos.append((None, 'Debug Brick', 'Debug', 'debug_brick', 'Debug_Brick', None, 'debug-brick', None, True, False,
                        {'en': 'For Firmware Developers: JTAG and serial console',
                         'de': 'Für Firmware Entwickler: JTAG und serielle Konsole'}))

    bricklet_infos.append((None, 'Breakout Bricklet', 'Breakout', 'breakout_bricklet', 'Breakout', None, 'breakout-bricklet', None, True, False,
                           {'en': 'Makes all Bricklet signals available',
                            'de': 'Macht alle Bricklet Signale zugänglich'}))

    with open(os.path.join(bindings_root_directory, '..', 'device_infos.py'), 'wb') as f:
        f.write('from collections import namedtuple\n')
        f.write('\n')
        f.write("DeviceInfo = namedtuple('DeviceInfo', 'identifier long_display_name short_display_name ref_name hardware_doc_name software_doc_prefix git_name firmware_url_part is_released has_bindings description')\n")
        f.write('\n')
        f.write('brick_infos = \\\n')
        f.write('[\n')

        for brick_info in sorted(brick_infos):
            f.write('    DeviceInfo{0},\n'.format(brick_info))

        f.write(']\n')
        f.write('\n')
        f.write('bricklet_infos = \\\n')
        f.write('[\n')

        for bricklet_info in sorted(bricklet_infos):
            f.write('    DeviceInfo{0},\n'.format(bricklet_info))

        f.write(']\n')

cn_valid_camel_case_chars = re.compile('^[A-Z][A-Za-z0-9]*$')
cn_valid_underscore_chars = re.compile('^[a-z][a-z0-9_]*$')
cn_valid_display_chars = re.compile('^[A-Z][A-Za-z0-9/ -.]*$')
cn_valid_constant_camel_case_chars = re.compile('^[A-Za-z0-9]+$')
cn_valid_constant_underscore_chars = re.compile('^[a-z0-9_]+$')

cn_all_uppercase = ['api', 'ir', 'us', 'lcd', 'dc', 'imu', 'pwm', 'gps', 'id', 'io4',
                    'io16', 'led', 'i2c', 'ptc', 'red', 'rs485', 'eap', 'usb', 'mac',
                    '2d', '3d', '1k', '100k', '500k', '3v', '6v', '10v', '36v',
                    '45v', 'sps', 'oqpsk', 'bpsk40', 'dhcp', 'ip', 'wpa',
                    'wpa2', 'ca', 'wep', 'rgb', 'nfc', 'rfid', 'fifo',
                    'ws2801', 'ws2811', 'ws2812', 'adc', 'rs232', 'ac', 'oled',
                    '125dps', '250dps', '500dps', '1000dps', '2000dps', 'co2',]

cn_eap_suffix = ['fast', 'tls', 'ttls', 'peap', 'mschap', 'gtc']

cn_special_camel_case = {'mhz':      'MHz',
                         '20ma':     '20mA',
                         '24ma':     '24mA',
                         '5v':       '5V',
                         '10v':      '10V',
                         '64000lux': '64000Lux',
                         '32000lux': '32000Lux',
                         '16000lux': '16000Lux',
                         '8000lux':  '8000Lux',
                         '1300lux':  '1300Lux',
                         '600lux':   '600Lux',
                         '3hz':      '3Hz',
                         '6hz':      '6Hz',
                         '10hz':     '10Hz',
                         '12hz':     '12Hz',
                         '25hz':     '25Hz',
                         '50hz':     '50Hz',
                         '60hz':     '60Hz',
                         '80hz':     '80Hz',
                         '100hz':    '100Hz',
                         '200hz':    '200Hz',
                         '400hz':    '400Hz',
                         '800hz':    '800Hz',
                         '1600hz':   '1600Hz',
                         '1to11':    '1To11',
                         '1to13':    '1To13',
                         '1to14':    '1To14'}

def check_name(camel_case, underscore, short_display, long_display, is_constant=False, device_category=None):
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

    if short_display is not None:
        if cn_valid_display_chars.match(short_display) is None:
            raise ValueError("short display name '{0}' contains invalid chars".format(short_display))

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

    if camel_case is not None and short_display is not None:
        # test 1
        short_display_to_check = short_display.replace(' ', '').replace('-', '').replace('/', '')

        if short_display_to_check.endswith('2.0'):
            short_display_to_check = short_display_to_check.replace('2.0', 'V2')

        if camel_case != short_display_to_check:
            raise ValueError("camel case name '{0}' and short display name '{1}' ({2}) mismatch (test 1)" \
                             .format(camel_case, short_display, short_display_to_check))

        # test 2
        camel_case_to_check = camel_case_to_space(camel_case)

        if camel_case == 'IMUV2':
            camel_case_to_check = camel_case_to_check.replace('V 2', ' 2.0')
        elif camel_case_to_check.endswith('CO 2'):
            camel_case_to_check = camel_case_to_check.replace('CO 2', 'CO2')
        elif camel_case.endswith('V2'):
            camel_case_to_check = camel_case_to_check.replace('V2', '2.0')
        elif camel_case in ['IO4', 'IO16']:
            camel_case_to_check = camel_case_to_check.replace(' ', '-')
        elif camel_case in ['Current12', 'Current25']:
            camel_case_to_check = camel_case_to_check.replace(' ', '')
        elif camel_case == 'VoltageCurrent':
            camel_case_to_check = camel_case_to_check.replace(' ', '/')
        elif camel_case.endswith('16x2'):
            camel_case_to_check = camel_case_to_check.replace('16x 2', '16x2')
        elif camel_case.endswith('20x4'):
            camel_case_to_check = camel_case_to_check.replace('20x 4', '20x4')
        elif camel_case.endswith('128x64'):
            camel_case_to_check = camel_case_to_check.replace('128x 64', '128x64')
        elif camel_case.endswith('64x48'):
            camel_case_to_check = camel_case_to_check.replace('64x 48', '64x48')
        elif camel_case.endswith('4x7'):
            camel_case_to_check = camel_case_to_check.replace('4x 7', '4x7')
        elif camel_case.endswith('020mA'):
            camel_case_to_check = camel_case_to_check.replace('020m A', '0-20mA')
        elif camel_case.endswith('RS232'):
            camel_case_to_check = camel_case_to_check.replace('RS 232', 'RS232')
        elif camel_case == 'NFCRFID':
            camel_case_to_check = camel_case_to_check.replace('NFCRFID', 'NFC/RFID')

        if camel_case_to_check != short_display:
            raise ValueError("camel case name '{0}' ({1}) and short display name '{2}' mismatch (test 2)" \
                             .format(camel_case, camel_case_to_check, short_display))

    if underscore is not None and short_display is not None:
        short_display_to_check = short_display.replace(' ', '_').replace('/', '_')

        if short_display.endswith('2.0'):
            short_display_to_check = short_display_to_check.replace('2.0', 'V2')
        elif short_display in ['IO-4', 'IO-16']:
            short_display_to_check = short_display_to_check.replace('-', '')
        else:
            short_display_to_check = short_display_to_check.replace('-', '_')

        short_display_to_check = short_display_to_check.lower()

        if underscore != short_display_to_check.lower():
            raise ValueError("underscore name '{0}' and short display name '{1}' ({2}) mismatch" \
                             .format(underscore, short_display, short_display_to_check))

    if short_display != None and long_display != None and device_category != None:
        short_display_to_check = set(short_display.split(' ') + [device_category])
        long_display_to_check = set(long_display.split(' '))

        if short_display_to_check != long_display_to_check:
            raise ValueError("long display name '{0}' and short display name '{1}' + '{2}' ({3}) do not contain the same words" \
                             .format(long_display, short_display, device_category, ' '.join(list(short_display_to_check))))


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

        check_name(raw_data['name'][0], raw_data['name'][1], None, None)

        for raw_element in self.raw_data['elements']:
            element = generator.get_element_class()(self, raw_element, generator)

            self.all_elements.append(element)

            check_name(None, element.get_underscore_name(), None, None)

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
                check_name(constant_group.get_camel_case_name(), constant_group.get_underscore_name(), None, None)

                for constant_item in constant_group.get_items():
                    check_name(constant_item.get_camel_case_name(), constant_item.get_underscore_name(), None, None, is_constant=True)

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
        return make_headless_camel_case(self.get_camel_case_name(), self.get_underscore_name())

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

        check_name(raw_data['name'][0], raw_data['name'][1], raw_data['name'][2], raw_data['name'][3], device_category=raw_data['category'])

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
        return make_headless_camel_case(self.get_camel_case_name(), self.get_underscore_name())

    def get_underscore_name(self):
        return self.raw_data['name'][1]

    def get_upper_case_name(self):
        return self.get_underscore_name().upper()

    def get_dash_name(self):
        return self.get_underscore_name().replace('_', '-')

    def get_short_display_name(self):
        return self.raw_data['name'][2]

    def get_long_display_name(self):
        return self.raw_data['name'][3]

    def get_description(self, language='en'):
        return self.raw_data['description'][language]

    def get_git_directory(self):
        global_root_directory = os.path.normpath(os.path.join(self.get_generator().get_bindings_root_directory(), '..', '..'))
        git_name = self.get_dash_name() + '-' + self.get_category().lower()
        git_directory = os.path.join(global_root_directory, git_name)

        return git_directory

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

    def get_doc_rst_path(self):
        if not self.get_generator().is_doc():
            raise Exception("Invalid call in non-doc generator")

        filename = '{0}_{1}_{2}.rst'.format(self.get_camel_case_name(),
                                            self.get_category(),
                                            self.get_generator().get_doc_rst_filename_part())

        return os.path.join(self.get_generator().get_bindings_root_directory(),
                            'doc',
                            self.get_generator().get_language(),
                            filename)

    def get_doc_rst_ref_name(self):
        if not self.get_generator().is_doc():
            raise Exception("Invalid call in non-doc generator")

        return self.get_underscore_name() + '_' + self.get_category().lower()

class Generator:
    def __init__(self, bindings_root_directory, language):
        self.bindings_root_directory = bindings_root_directory
        self.language = language # en or de

    def get_bindings_name(self):
        raise Exception("get_bindings_name() not implemented")

    def get_bindings_display_name(self):
        raise Exception("get_bindings_display_name() not implemented")

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
        return self.language # en or de

    def is_doc(self):
        return False

    def compare_examples(self, example1, example2):
        return cmp(example1[2], example2[2])

    def prepare(self):
        pass

    def generate(self, device):
        raise Exception("generate() not implemented")

    def finish(self):
        pass

class DocGenerator(Generator):
    def __init__(self, *args, **kwargs):
        Generator.__init__(self, *args, **kwargs)

        if self.get_bindings_name() != self.get_doc_rst_filename_part().lower():
            raise Exception("bindings name '{0}' and doc rst name '{1}' do not match".format(self.get_bindings_name(), self.get_doc_rst_filename_part()))

    def get_doc_rst_filename_part(self):
        raise Exception("get_doc_rst_filename_part() not implemented")

    def get_doc_example_regex(self):
        raise Exception("get_doc_example_regex() not implemented")

    def is_doc(self):
        return True

    def prepare(self):
        Generator.prepare(self)

        recreate_directory(os.path.join(self.get_bindings_root_directory(), 'doc', self.get_language()))

    def finish(self):
        Generator.finish(self)

        # Copy IPConnection examples
        example_regex = self.get_doc_example_regex()

        if example_regex is not None:
            print(' * ip_connection')

            examples = find_examples(self.get_bindings_root_directory(), example_regex, self.compare_examples)
            copy_files = []

            for example in examples:
                include = 'IPConnection_{0}_{1}'.format(self.get_doc_rst_filename_part(), example[0].replace(' ', '_'))
                copy_files.append((example[1], include))

            copy_examples(copy_files, self.get_bindings_root_directory())

class BindingsGenerator(Generator):
    released_files_name_prefix = None
    recreate_bindings_subdirectory = True
    bindings_subdirectory_name = 'bindings'
    check_directory_name = True

    def __init__(self, *args, **kwargs):
        Generator.__init__(self, *args, **kwargs)

        directory = os.path.split(self.get_bindings_root_directory())[1]

        if self.check_directory_name and self.get_bindings_name() != directory:
            raise Exception("bindings root directory '{0}' and bindings name '{1}' do not match".format(directory, self.get_bindings_name()))

        self.released_files = []

    def prepare(self):
        if self.recreate_bindings_subdirectory:
            recreate_directory(os.path.join(self.get_bindings_root_directory(), self.bindings_subdirectory_name))

    def finish(self):
        if self.released_files_name_prefix is None:
            if len(self.released_files) > 0:
                raise Exception("Released files in list but name prefix not set")
        else:
            py = open(os.path.join(self.get_bindings_root_directory(), self.released_files_name_prefix + '_released_files.py'), 'wb')
            py.write('released_files = ' + repr(self.released_files))
            py.close()

def examples_tester_worker(cookie, args, env):
    try:
        output = subprocess.check_output(args, env=env, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return cookie, e.output, e.returncode == 0

    return cookie, output, True

class ExamplesTester:
    PROCESSES = 4

    def __init__(self, name, extension, path, subdirs=['examples'], comment=None, extra_examples=[]):
        version = get_changelog_version(path)

        self.name = name
        self.extension = extension
        self.path = path
        self.subdirs = subdirs[:]
        self.comment = comment
        self.extra_examples = extra_examples[:]
        self.zipname = 'tinkerforge_{0}_bindings_{1}_{2}_{3}.zip'.format(name, *version)
        self.test_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.pool = multiprocessing.dummy.Pool(processes=self.PROCESSES)

    def walker(self, arg, dirname, names):
        for name in names:
            if not name.endswith(self.extension):
                continue

            self.handle_source(os.path.join(dirname, name), False)

    def execute(self, cookie, args, env=None):
        def callback(result):
            self.handle_result(*result)

        self.pool.apply_async(examples_tester_worker, args=(cookie, args, env),
                              callback=callback)

    def handle_source(self, src, is_extra_example):
        self.test_count += 1
        self.test((src,), src, is_extra_example)

    def handle_result(self, cookie, output, success):
        src = cookie[0]

        if self.comment != None:
            print('>>> [{0}] testing {1}'.format(self.comment, src))
        else:
            print('>>> testing {0}'.format(src))

        output = output.strip()

        if len(output) > 0:
            print(output)

        if success:
            self.success_count += 1
            print('\033[01;32m>>> test succeded\033[0m\n')
        else:
            self.failure_count += 1
            print('\033[01;31m>>> test failed\033[0m\n')

    def test(self, cookie, src, is_extra_example):
        raise NotImplementedError()

    def run(self):
        tmp_dir = os.path.join('/tmp/tester', self.name)

        # Make temporary examples directory
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

        os.makedirs(tmp_dir)

        with ChangedDirectory(tmp_dir):
            shutil.copy(os.path.join(self.path, self.zipname), tmp_dir)

            # unzip
            print('>>> unpacking {0} to {1}'.format(self.zipname, tmp_dir))

            args = ['/usr/bin/unzip',
                    '-q',
                    os.path.join(tmp_dir, self.zipname)]

            rc = subprocess.call(args)

            if rc != 0:
                print('### could not unpack {0}'.format(self.zipname))
                return False

            print('>>> unpacking {0} done\n'.format(self.zipname))

            # test
            for subdir in self.subdirs:
                os.path.walk(os.path.join(tmp_dir, subdir), self.walker, None)

            for extra_example in self.extra_examples:
                self.handle_source(extra_example, True)

        self.pool.close()
        self.pool.join()

        # report
        if self.comment != None:
            print('### [{0}] {1} file(s) tested, {2} test(s) succeded, {3} failure(s) occurred'
                  .format(self.comment, self.test_count, self.success_count, self.failure_count))
        else:
            print('### {0} file(s) tested, {1} test(s) succeded, {2} failure(s) occurred'
                  .format(self.test_count, self.success_count, self.failure_count))

        return self.failure_count == 0

class SourceTester:
    def __init__(self, name, extension, path, subdirs=['source'], comment=None):
        version = get_changelog_version(path)

        self.name = name
        self.extension = extension
        self.path = path
        self.subdirs = subdirs[:]
        self.comment = comment
        self.zipname = 'tinkerforge_{0}_bindings_{1}_{2}_{3}.zip'.format(name, *version)
        self.test_count = 0
        self.failure_count = 0

    def walker(self, arg, dirname, names):
        for name in names:
            if not name.endswith(self.extension):
                continue

            self.handle_source(os.path.join(dirname, name))

    def handle_source(self, src):
        self.test_count += 1

        if self.comment is not None:
            print('>>> [{0}] testing {1}'.format(self.comment, src))
        else:
            print('>>> testing {0}'.format(src))

        if not self.test(src):
            self.failure_count += 1

            print('\033[01;31m>>> test failed\033[0m\n')
        else:
            print('\033[01;32m>>> test succeded\033[0m\n')

    def after_unzip(self):
        return True

    def test(self, src):
        raise NotImplementedError()

    def run(self):
        tmp_dir = os.path.join('/tmp/tester', self.name)

        # make temporary examples directory
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

        os.makedirs(tmp_dir)

        with ChangedDirectory(tmp_dir):
            shutil.copy(os.path.join(self.path, self.zipname), tmp_dir)

            # unzip
            print('>>> unpacking {0} to {1}'.format(self.zipname, tmp_dir))

            args = ['/usr/bin/unzip',
                    '-q',
                    os.path.join(tmp_dir, self.zipname)]

            rc = subprocess.call(args)

            if rc != 0:
                print('### could not unpack {0}'.format(self.zipname))
                return False

            print('>>> unpacking {0} done\n'.format(self.zipname))

            if not self.after_unzip():
                return False

            # test
            for subdir in self.subdirs:
                os.path.walk(os.path.join(tmp_dir, subdir), self.walker, None)

            # report
            if self.comment is not None:
                print('### [{0}] {1} files tested, {2} failure(s) occurred'.format(self.comment, self.test_count, self.failure_count))
            else:
                print('### {0} files tested, {1} failure(s) occurred'.format(self.test_count, self.failure_count))

        return self.failure_count == 0

# use "with ChangedDirectory('/path/to/abc')" instead of "os.chdir('/path/to/abc')"
class ChangedDirectory:
    def __init__(self, directory):
        self.directory = directory

    def __enter__(self):
        self.previous_directory = os.getcwd()
        os.chdir(self.directory)

    def __exit__(self, type, value, traceback):
        os.chdir(self.previous_directory)
