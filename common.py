# -*- coding: utf-8 -*-

"""
Common Generator Library
Copyright (C) 2012-2017 Matthias Bolte <matthias@tinkerforge.com>
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
import math
import multiprocessing.dummy
from collections import namedtuple
from pprint import pprint
from copy import deepcopy

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

def strip_trailing_whitespace(text):
    lines = []

    for line in text.split('\n'):
        lines.append(line.rstrip())

    return '\n'.join(lines)

def get_changelog_version(bindings_root_directory):
    r = re.compile('^\S+: (\d+)\.(\d+)\.(\d+) \(\S+\)')
    last = None

    with open(os.path.join(bindings_root_directory, 'changelog.txt'), 'rb') as f:
        for line in f.readlines():
            m = r.match(line)

            if m is not None:
                last = (m.group(1), m.group(2), m.group(3))

    if last == None:
        raise GeneratorError('no version found in changelog: ' + bindings_root_directory)

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
        device_identifier_constant = select_lang(device_identifier_constant).format(device.get_underscore_name(),
                                                                                    device.get_underscore_category(),
                                                                                    ref_name,
                                                                                    device.get_camel_case_category())
    else:
        device_identifier_constant = '.. |device_identifier_constant| unicode:: 0xA0\n   :trim:\n'

    ref = '.. _{0}_{1}_{2}:\n'.format(device.get_underscore_name(), device.get_underscore_category(), ref_name)

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
    if device.is_brick():
        device_name = select_lang(brick_name)
    else:
        device_name = select_lang(bricklet_name)

    device_name = device_name.format(device.get_long_display_name(),
                                     device.get_underscore_name())

    s = select_lang(summary).format(bindings_name_link,
                                    device_name,
                                    device.get_long_display_name(),
                                    device.get_underscore_name() + '_' + device.get_underscore_category())

    if is_programming_language:
        s += select_lang(summary_install).format(device.get_generator().get_bindings_name(),
                                                 device.get_generator().get_bindings_display_name())

    if not device.is_released():
        if device.is_brick():
            d = brick
        else:
            d = bricklet

        s = select_lang(not_released).format(select_lang(d)) + s

    return s

def make_rst_examples(title_from_filename, device, url_fixer=None,
                      is_picture=False, additional_download_finder=None,
                      display_name_fixer=None, language_from_filename=None,
                      add_html_test_link=False, add_tvpl_test_link=False):
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
                                               device.get_underscore_category(),
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

        include = '{0}_{1}_{2}_{3}'.format(device.get_camel_case_name(), device.get_camel_case_category(), include_name, f[0].replace(' ', '_'))
        copy_files.append((f[1], include))
        title = title_from_filename(f[0])
        url = url_format.format(device.get_git_name(), bindings_name, f[0].replace(' ', '%20'))

        if url_fixer is not None:
            url = url_fixer(url)

        display_name = f[0]

        if display_name_fixer is not None:
            display_name = display_name_fixer(display_name)

        downloads = []

        if additional_download_finder is not None:
            for additional_download in additional_download_finder(f[1]):
                additional_url = url_format.format(device.get_git_name(), bindings_name, additional_download.replace(' ', '%20'))
                downloads.append(download.format(additional_download, additional_url))

        downloads = [download.format(display_name, url)] + downloads

        if add_html_test_link and include.endswith('.html'):
            downloads.append('`Test ({0}) <http://www.tinkerforge.com/{1}/doc/Software/Examples/JavaScript/{2}>`__'.format(display_name, lang, include))

        if add_tvpl_test_link and include.endswith('.tvpl'):
            downloads.append('`Test ({0}) <http://www.tinkerforge.com/{1}/tvpl/editor.html?example={2}/{3}/{4}>`__'
                             .format(display_name, lang, device.get_underscore_category(), device.get_underscore_name(), f[0]))

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

re_camel_case_to_space = re.compile('([A-Z][A-Z][a-z])|([a-z][A-Z])|([a-zA-Z][0-9])')

def camel_case_to_space(name):
    return re_camel_case_to_space.sub(lambda m: m.group()[:1] + " " + m.group()[1:], name)

def format_since_firmware(device, packet):
    since = packet.get_since_firmware()

    if since is not None and since > [2, 0, 0]:
        if device.is_brick():
            suffix = 'Firmware'
        else:
            suffix = 'Plugin'

        return '\n.. versionadded:: {1}.{2}.{3}$nbsp;({0})\n'.format(suffix, *since)
    else:
        return ''

def default_constant_format(prefix, constant_group, constant, value):
    return '* {0}{1}_{2} = {3}\n'.format(prefix, constant_group.get_upper_case_name(),
                                         constant.get_upper_case_name(), value)

def format_constants(prefix, packet,
                     constants_name={'en': 'constants', 'de': 'Konstanten'},
                     char_format="'{0}'",
                     constant_format_func=default_constant_format,
                     constants_intro=None):
    if constants_intro == None:
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
        for constant in constant_group.get_constants():
            if constant_group.get_type() == 'char':
                value = char_format.format(constant.get_value())
            else:
                value = str(constant.get_value())

            constants.append(constant_format_func(prefix, constant_group, constant, value))

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

def underscore_to_space(name):
    return ' '.join([part.capitalize() for part in name.split('_')])

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
        raise GeneratorError('Not all replacements for {0} have been applied'.format(template_filename))

    destination_file = open(destination_filename, 'wb')
    destination_file.writelines(lines)
    destination_file.close()

def make_c_like_bitmask(value, shift='{0} << {1}', combine='({0}) | ({1})'):
    if value == 0:
        return str(value)

    parts = []

    for i in range(64):
        if (value & (1 << i)) != 0:
            parts.append(shift.format(1, i))

    if len(parts) == 1:
        return parts[0]
    elif len(parts) == 2:
        return combine.format(parts[0], parts[1])
    else:
        raise GeneratorError('More than to bits ware not supported yet')

def wrap_non_empty(prefix, middle, suffix):
    if len(middle) > 0:
        return prefix + middle + suffix
    else:
        return ''

def execute(args, **kwargs):
    if subprocess.call(args, **kwargs) != 0:
        raise GeneratorError("Command '{0}' failed".format(' '.join(args) if isinstance(args, list) else args))

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
    common_bricklet_comcu_packets = copy.deepcopy(__import__('bricklet_comcu_commonconfig').common_packets)

    brick_infos = []
    bricklet_infos = []
    device_identifiers = set()

    generator = generator_class(bindings_root_directory, language)

    generator.prepare()

    for config in configs:
        if config.endswith('_config.py'):
            com = copy.deepcopy(__import__(config[:-3]).com)

            if com['documented'] and not com['released']:
                raise GeneratorError('{0} is marked as documented, but as not released'.format(config[:-10]))

            if not com['released'] and not com['documented']:
                print(' * {0} \033[01;36m(not released, not documented)\033[0m'.format(config[:-10]))
            elif not com['released']:
                print(' * {0} \033[01;36m(not released)\033[0m'.format(config[:-10]))
            elif not com['documented']:
                print(' * {0} \033[01;36m(not documented)\033[0m'.format(config[:-10]))
            else:
                print(' * {0}'.format(config[:-10]))

            def prepare_common_packets(common_packets):
                for common_packet in common_packets:
                    if common_packet['since_firmware'] is None:
                        continue

                    if com['name'] in common_packet['since_firmware']:
                        common_packet['since_firmware'] = \
                            common_packet['since_firmware'][com['name']]
                    else:
                        common_packet['since_firmware'] = \
                            common_packet['since_firmware']['*']

                    if common_packet['since_firmware'] is None:
                        common_packet['to_be_removed'] = True

                return filter(lambda x: 'to_be_removed' not in x, common_packets)

            if config.startswith('brick_') and 'common_included' not in com:
                common_packets = copy.deepcopy(common_device_packets) + copy.deepcopy(common_brick_packets)
                com['packets'].extend(prepare_common_packets(common_packets))
                com['common_included'] = True

            if config.startswith('bricklet_') and 'common_included' not in com:
                if com.get('has_comcu', False):
                    common_packets = copy.deepcopy(common_device_packets) + copy.deepcopy(common_bricklet_comcu_packets) + copy.deepcopy(common_bricklet_packets)
                else:
                    common_packets = copy.deepcopy(common_device_packets) + copy.deepcopy(common_bricklet_packets)

                com['packets'].extend(prepare_common_packets(common_packets))
                com['common_included'] = True

            device = generator.get_device_class()(com, generator)
            device_identifier = device.get_device_identifier()

            if device_identifier in device_identifiers:
                raise GeneratorError('Device identifier {0} is not unique'.format(device_identifier))

            device_identifiers.add(device_identifier)

            if device.is_brick():
                ref_name = device.get_underscore_name() + '_brick'
                hardware_doc_name = device.get_short_display_name().replace(' ', '_').replace('/', '_').replace('-', '').replace('2.0', 'V2') + '_Brick'
                software_doc_prefix = device.get_camel_case_name() + '_Brick'

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
                               device.get_git_name(),
                               firmware_url_part,
                               device.is_released(),
                               device.is_documented(),
                               True,
                               device.get_description())

                brick_infos.append(device_info)
            else:
                ref_name = device.get_underscore_name() + '_bricklet'
                hardware_doc_name = device.get_short_display_name().replace(' ', '_').replace('/', '_').replace('-', '').replace('2.0', 'V2')
                software_doc_prefix = device.get_camel_case_name() + '_Bricklet'
                firmware_url_part = device.get_underscore_name()

                device_info = (device.get_device_identifier(),
                               device.get_long_display_name(),
                               device.get_short_display_name(),
                               ref_name,
                               hardware_doc_name,
                               software_doc_prefix,
                               device.get_git_name(),
                               firmware_url_part,
                               device.is_released(),
                               device.is_documented(),
                               True,
                               device.get_description())

                bricklet_infos.append(device_info)

            generator.generate(device)

    generator.finish()

    brick_infos.append((None, 'Debug Brick', 'Debug', 'debug_brick', 'Debug_Brick', None, 'debug-brick', None, True, True, False,
                        {'en': 'For Firmware Developers: JTAG and serial console',
                         'de': 'Für Firmware Entwickler: JTAG und serielle Konsole'}))

    bricklet_infos.append((None, 'Breakout Bricklet', 'Breakout', 'breakout_bricklet', 'Breakout', None, 'breakout-bricklet', None, True, True, False,
                           {'en': 'Makes all Bricklet signals available',
                            'de': 'Macht alle Bricklet Signale zugänglich'}))

    with open(os.path.join(bindings_root_directory, '..', 'device_infos.py'), 'wb') as f:
        f.write('from collections import namedtuple\n')
        f.write('\n')
        f.write("DeviceInfo = namedtuple('DeviceInfo', 'identifier long_display_name short_display_name ref_name hardware_doc_name software_doc_prefix git_name firmware_url_part is_released is_documented has_bindings description')\n")
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

check_name_valid_word_head = re.compile('^[A-Z]+[A-Z0-9]*[a-z0-9]*$')
check_name_valid_word_tail = re.compile('^[A-Z0-9]+[a-z0-9]*$')
check_name_valid_word_constant = re.compile('^[A-Z0-9]+[a-z0-9]*$') # constants are allowed to start with numbers
check_name_exceptions_whole_name = ['Industrial Dual 0 20mA']
check_name_exceptions_word_in_constant = ['20mA', '24mA']

def check_name(name, display_name=None, is_constant=False):
    if isinstance(name, tuple):
        raise GeneratorError('Name {0} uses old tuple format, update it to new split-camel-case format'.format(name))

    if len(name) == 0:
        raise GeneratorError('Name is empty')

    if name not in check_name_exceptions_whole_name:
        words = name.split(' ')

        if not is_constant:
            if check_name_valid_word_head.match(words[0]) == None:
                raise GeneratorError("Word '{0}' in name '{1}' is invalid".format(words[0], name))

            for word in words[1:]:
                if check_name_valid_word_tail.match(word) == None:
                    raise GeneratorError("Word '{0}' in name '{1}' is invalid".format(word, name))
        else:
            for word in words:
                if word not in check_name_exceptions_word_in_constant and \
                   check_name_valid_word_constant.match(word) == None:
                    raise GeneratorError("Word '{0}' in constant name '{1}' is invalid".format(word, name))

    if display_name != None:
        display_name_to_check = display_name.replace('/', ' ')

        if display_name.endswith(' 2.0'):
            display_name_to_check = display_name_to_check.replace(' 2.0', ' V2')
        elif display_name in ['IO-4', 'IO-16']: # exceptions for legacy dash rules
            display_name_to_check = display_name_to_check.replace('-', '')
        else:
            display_name_to_check = display_name_to_check.replace('-', ' ')

        if name != display_name_to_check:
            raise GeneratorError("Name '{0}' and display name '{1}' ({2}) mismatch" \
                                 .format(name, display_name, display_name_to_check))

def break_string(string, marker, continuation='', max_length=90):
    result = string.replace('<BP>', ' ')

    if len(result) > max_length:
        prefix = result.split(marker)[0].split('\n')[-1].lstrip('\r')
        tabs = 0

        for c in prefix:
            if c != '\t':
                break

            tabs += 1

        indent = '\t' * tabs + ' ' * (len(prefix) - tabs + len(marker))
        parts = string.split('<BP>')
        result = parts[0]

        for part in parts[1:]:
            line = (result.split('\n')[-1] + ' ' + part.split('\n')[0]).replace('\t', '    ') + continuation

            if len(line) > max_length:
                result += continuation + '\n' + indent + part
            else:
                result += ' ' + part

    return result

class GeneratorError(Exception):
    pass

def skip_words(words, skip):
    if skip < 0:
        return words[:skip]
    else:
        return words[skip:]

class NameMixin:
    def _get_name(self):
        raise NotImplementedError()

    def get_name(self, skip=0, remove=None):
        words = skip_words(self._get_name().split(' '), skip)

        if remove in words:
            words.remove(remove)

        return ' '.join(words)

    def get_camel_case_name(self, skip=0):
        return ''.join(skip_words(self._get_name().split(' '), skip))

    def get_headless_camel_case_name(self, skip=0):
        words = skip_words(self._get_name().split(' '), skip)

        return ''.join([words[0].lower()] + words[1:])

    def get_underscore_name(self, skip=0):
        return '_'.join(skip_words(self._get_name().split(' '), skip)).lower()

    def get_upper_case_name(self, skip=0):
        return '_'.join(skip_words(self._get_name().split(' '), skip)).upper()

    def get_dash_name(self, skip=0):
        return '-'.join(skip_words(self._get_name().split(' '), skip)).lower()

class Constant(NameMixin):
    def __init__(self, raw_data, constant_group):
        self.raw_data = raw_data
        self.constant_group = constant_group

        if len(raw_data) != 2:
            raise GeneratorError('Invalid Constant: ' + repr(raw_data))

        check_name(raw_data[0], is_constant=True)

    def get_constant_group(self): # parent
        return self.constant_group

    def get_device(self):
        return self.get_constant_group().get_device()

    def get_generator(self):
        return self.get_constant_group().get_generator()

    def _get_name(self): # for NameMixin
        return self.raw_data[0]

    def get_value(self):
        return self.raw_data[1]

class ConstantGroup(NameMixin):
    def __init__(self, type_, raw_data, device):
        self.type_ = type_
        self.raw_data = raw_data
        self.device = device
        self.elements = []
        self.constants = []

        if len(raw_data) != 2:
            raise GeneratorError('Invalid ConstantGroup: ' + repr(raw_data))

        check_name(raw_data[0])

        for raw_constant in raw_data[1]:
            self.constants.append(self.get_generator().get_constant_class()(raw_constant, self))

    def get_elements(self): # parents
        return self.elements

    def get_device(self):
        return self.device

    def get_generator(self):
        return self.get_device().get_generator()

    def _get_name(self): # for NameMixin
        return self.raw_data[0]

    def get_type(self):
        return self.type_

    def get_constants(self):
        return self.constants

    def add_elements(self, elements):
        self.elements += elements

class Element(NameMixin):
    def __init__(self, raw_data, packet):
        self.raw_data = raw_data
        self.packet = packet
        self.constant_group = None

        check_name(raw_data[0])

        if len(raw_data) != 4 and len(raw_data) != 5:
            raise GeneratorError('Invalid Element: ' + repr(raw_data))

        if len(self.raw_data) > 4:
            self.constant_group = self.get_generator().get_constant_group_class()(raw_data[1], raw_data[4], self.get_device())
            self.constant_group.add_elements([self])

    def get_packet(self): # parent
        return self.packet

    def get_device(self):
        return self.packet.get_device()

    def get_generator(self):
        return self.packet.get_generator()

    def _get_name(self): # for NameMixin
        return self.raw_data[0]

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
        if self.get_type() == 'bool':
            return int(math.ceil(self.get_cardinality() / 8.0))
        else:
            return self.get_item_size() * self.get_cardinality()

class HighLevelStream(object):
    def __init__(self, raw_data, packet):
        self.raw_data = raw_data
        self.packet = packet

    def get_packet(self): # parent
        return self.packet

    def get_fixed_total_length(self):
        return self.raw_data.get('fixed_total_length', None)

    # FIXME: avoid all this NameMixin duplication here
    def _get_data_name(self):
        return self.raw_data.get('data_name', 'Data')

    def get_data_name(self, skip=0, remove=None):
        words = skip_words(self._get_data_name().split(' '), skip)

        if remove in words:
            words.remove(remove)

        return ' '.join(words)

    def get_data_camel_case_name(self, skip=0):
        return ''.join(skip_words(self._get_data_name().split(' '), skip))

    def get_data_headless_camel_case_name(self, skip=0):
        words = skip_words(self._get_data_name().split(' '), skip)

        return ''.join([words[0].lower()] + words[1:])

    def get_data_underscore_name(self, skip=0):
        return '_'.join(skip_words(self._get_data_name().split(' '), skip)).lower()

    def get_data_upper_case_name(self, skip=0):
        return '_'.join(skip_words(self._get_data_name().split(' '), skip)).upper()

    def get_data_dash_name(self, skip=0):
        return '-'.join(skip_words(self._get_data_name().split(' '), skip)).lower()

class HighLevelStreamIn(HighLevelStream):
    def __init__(self, raw_data, packet):
        HighLevelStream.__init__(self, raw_data, packet)

        if 'fixed_total_length' not in raw_data and \
           packet.elements_in[-3].get_name() != 'Stream Total Length':
            raise GeneratorError("Invalid element names for high-level feature 'stream_in'")

        if packet.elements_in[-2].get_name() != 'Stream Chunk Offset' or \
           packet.elements_in[-1].get_name() != 'Stream Chunk Data':
            raise GeneratorError("Invalid element names for high-level feature 'stream_in'")

        if 'fixed_total_length' not in raw_data and \
           packet.elements_in[-3].get_type() != packet.elements_in[-2].get_type():
            raise GeneratorError("Type of 'Stream Total Length' and 'Stream Chunk Offset' are different")

        if raw_data.get('short_write', False) and \
           packet.elements_out[-1].get_name() != 'Stream Chunk Written':
            raise GeneratorError("Invalid element names for high-level feature 'stream_in'")

    def get_total_length_element(self):
        if 'fixed_total_length' in self.raw_data:
            return None
        else:
            return self.packet.elements_in[-3]

    def get_chunk_offset_element(self):
        return self.packet.elements_in[-2]

    def get_chunk_data_element(self):
        return self.packet.elements_in[-1]

    def get_short_write(self):
        return self.raw_data.get('short_write', False)

class HighLevelStreamOut(HighLevelStream):
    def __init__(self, raw_data, packet):
        HighLevelStream.__init__(self, raw_data, packet)

        if 'fixed_total_length' not in raw_data and \
           packet.elements_out[-3].get_name() != 'Stream Total Length':
            raise GeneratorError("Invalid element names for high-level feature 'stream_out'")

        if packet.elements_out[-2].get_name() != 'Stream Chunk Offset' or \
           packet.elements_out[-1].get_name() != 'Stream Chunk Data':
            raise GeneratorError("Invalid element names for high-level feature 'stream_out'")

        if 'fixed_total_length' not in raw_data and \
           packet.elements_out[-3].get_type() != packet.elements_out[-2].get_type():
            raise GeneratorError("Type of 'Stream Total Length' and 'Stream Chunk Offset' are different")

    def get_total_length_element(self):
        if 'fixed_total_length' in self.raw_data:
            return None
        else:
            return self.packet.elements_out[-3]

    def get_chunk_offset_element(self):
        return self.packet.elements_out[-2]

    def get_chunk_data_element(self):
        return self.packet.elements_out[-1]

class Packet(NameMixin):
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

    def __init__(self, raw_data, device):
        self.raw_data = raw_data
        self.device = device
        self.elements_in = []
        self.elements_out = []
        self.high_level = {}
        self.high_level_elements_in = []
        self.high_level_elements_out = []

        check_name(raw_data['name'])

        if 'high_level' in raw_data and not raw_data['name'].endswith(' Low Level'):
            raise GeneratorError("Name of packet with high-level features has to end with 'Low Level'")

        for raw_element in self.raw_data['elements']:
            element = device.get_generator().get_element_class()(raw_element, self)

            if element.get_type() not in Packet.valid_types:
                raise GeneratorError('Invalid element type: ' + element.get_type())

            if element.get_cardinality() < 1:
                raise GeneratorError('Invalid element cardinality: ' + element.get_cardinality())

            if element.get_direction() == 'in':
                if len(self.elements_out) > 0:
                    raise GeneratorError("'in' element cannot come after 'out' element: " + element.get_name())

                self.elements_in.append(element)
            elif element.get_direction() == 'out':
                self.elements_out.append(element)
            else:
                raise GeneratorError('Invalid element direction ' + element.get_direction())

        raw_stream_in = raw_data.get('high_level', {}).get('stream_in', None)
        raw_stream_out = raw_data.get('high_level', {}).get('stream_out', None)

        if raw_stream_in != None and raw_stream_out != None:
            raise GeneratorError("Cannot combine high-level features 'stream_in' and 'stream_out'")
        elif raw_stream_in != None:
            stream_in = HighLevelStreamIn(raw_stream_in, self)
            raw_element = (stream_in.get_data_name(),) + deepcopy(self.elements_in[-1].raw_data[1:])

            self.high_level['stream_in'] = stream_in
            self.high_level_elements_in.append(device.get_generator().get_element_class()(raw_element, self))

        elif raw_stream_out != None:
            stream_out = HighLevelStreamOut(raw_stream_out, self)
            raw_element = (stream_out.get_data_name(),) + deepcopy(self.elements_out[-1].raw_data[1:])

            self.high_level['stream_out'] = stream_out
            self.high_level_elements_out.append(device.get_generator().get_element_class()(raw_element, self))

        self.constant_groups = []

        for element in self.elements_in + self.elements_out:
            constant_group = element.get_constant_group()

            if constant_group is None:
                continue

            for known_constant_group in self.constant_groups:
                if constant_group.get_underscore_name() != known_constant_group.get_underscore_name():
                    continue

                if constant_group.get_type() != known_constant_group.get_type():
                    raise GeneratorError('Multiple instance of constant group {0} with different types' \
                                         .format(constant_group.get_underscore_name()))

                for constant, known_constant in zip(constant_group.get_constants(), known_constant_group.get_constants()):
                    a = known_constant.get_underscore_name()
                    b = constant.get_underscore_name()

                    if a != b:
                        raise GeneratorError('Constant item name ({0} != {1}) mismatch in constant group {2}' \
                                             .format(a, b, constant_group.get_underscore_name()))

                    a = known_constant.get_value()
                    b = constant.get_value()

                    if a != b:
                        raise GeneratorError('Constant item value ({0} != {1}) mismatch in constant group {2}' \
                                             .format(a, b, constant_group.get_underscore_name()))

                known_constant_group.add_elements(constant_group.get_elements())

                constant_group = None

                break

            if constant_group is not None:
                self.constant_groups.append(constant_group)

    def get_device(self): # parent
        return self.device

    def get_generator(self):
        return self.device.get_generator()

    def get_type(self):
        return self.raw_data['type']

    def _get_name(self): # for NameMixin
        return self.raw_data['name']

    def get_elements(self, direction=None, high_level=False):
        elements_in = self.elements_in
        elements_out = self.elements_out

        if high_level:
            stream_in = self.get_high_level('stream_in')
            stream_out = self.get_high_level('stream_out')

            if stream_in != None:
                if stream_in.get_fixed_total_length() == None:
                    elements_in = elements_in[:-3]
                else:
                    elements_in = elements_in[:-2]

                elements_in += self.high_level_elements_in

            if stream_out != None:
                if stream_out.get_fixed_total_length() == None:
                    elements_out = elements_out[:-3]
                else:
                    elements_out = elements_out[:-2]

                elements_out += self.high_level_elements_out

        if direction is None:
            return elements_in + elements_out
        elif direction == 'in':
            return elements_in
        elif direction == 'out':
            return elements_out
        else:
            raise GeneratorError('Invalid element direction ' + direction)

    def has_high_level(self):
        return len(self.high_level) > 0

    def get_high_level(self, feature):
        if feature == 'stream_*':
            if 'stream_in' in self.high_level:
                return self.high_level['stream_in']
            elif 'stream_out' in self.high_level:
                return self.high_level['stream_out']
            else:
                return None
        else:
            return self.high_level.get(feature, None)

    def get_since_firmware(self):
        return self.raw_data['since_firmware']

    def get_doc_type(self):
        return self.raw_data['doc'][0]

    def get_doc_text(self):
        return self.raw_data['doc'][1]

    def get_doc_substitutions(self):
        doc = self.raw_data['doc']

        if len(doc) < 3:
            return []

        if lang in doc[2]:
            subsitutions = doc[2][lang]
        else:
            subsitutions = doc[2]['*']

        filtered_subsitutions = {}
        bindings_name = self.get_generator().get_bindings_name()

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
        for element in self.elements_in:
            size += element.get_size()
        return size

    def get_response_size(self):
        size = 8 # header
        for element in self.elements_out:
            size += element.get_size()
        return size

    def get_constant_groups(self):
        return self.constant_groups

    def get_formatted_constants(self, constant_format, char_format="'{0}'", **extra_value):
        constants = []

        for constant_group in self.get_constant_groups():
            for constant in constant_group.get_constants():
                if constant_group.get_type() == 'char':
                    value = char_format.format(constant.get_value())
                else:
                    value = str(constant.get_value())

                constants.append(constant_format.format(constant_group_upper_case_name=constant_group.get_upper_case_name(),
                                                        constant_upper_case_name=constant.get_upper_case_name(),
                                                        constant_value=value,
                                                        **extra_value))

        return ''.join(constants)

    def has_prototype_in_device(self):
        return self.raw_data.get('prototype_in_device', False)

    def is_virtual(self):
        return self.raw_data.get('is_virtual', False)

class Device(NameMixin):
    def __init__(self, raw_data, generator):
        self.raw_data = raw_data
        self.generator = generator
        self.all_packets = []
        self.all_packets_without_doc_only = []
        self.all_function_packets = []
        self.all_function_packets_without_doc_only = []
        self.callback_packets = []
        self.examples = []

        check_name(raw_data['name'], display_name=raw_data['display_name'])

        for i, raw_packet in zip(range(len(raw_data['packets'])), raw_data['packets']):
            if not 'function_id' in raw_packet:
                raw_packet['function_id'] = i + 1

            packet = generator.get_packet_class()(raw_packet, self)

            self.all_packets.append(packet)

            if packet.get_function_id() >= 0:
                self.all_packets_without_doc_only.append(packet)

        function_names = set()
        callback_names = set()

        for packet in self.all_packets:
            if packet.get_type() == 'function':
                if packet.get_name() in function_names:
                    raise GeneratorError('Function name is not unique: ' + packet.get_name())
                else:
                    function_names.add(packet.get_name())

                self.all_function_packets.append(packet)

                if packet.get_function_id() >= 0:
                    self.all_function_packets_without_doc_only.append(packet)
            elif packet.get_type() == 'callback':
                if 'Callback' in packet.get_name():
                    raise GeneratorError("Callback name cannot contain 'Callback': " + packet.get_name())

                if packet.get_name() in callback_names:
                    raise GeneratorError('Callback name is not unique: ' + packet.get_name())
                else:
                    callback_names.add(packet.get_name())

                self.callback_packets.append(packet)
            else:
                raise GeneratorError('Invalid packet type ' + packet.get_type())

        self.constant_groups = []

        for packet in self.all_packets:
            for constant_group in packet.get_constant_groups():
                for known_constant_group in self.constant_groups:
                    if constant_group.get_underscore_name() != known_constant_group.get_underscore_name():
                        continue

                    if constant_group.get_type() != known_constant_group.get_type():
                        raise GeneratorError('Multiple instance of constant group {0} with different types' \
                                             .format(constant_group.get_underscore_name()))

                    for constant, known_constant in zip(constant_group.get_constants(), known_constant_group.get_constants()):
                        a = known_constant.get_underscore_name()
                        b = constant.get_underscore_name()

                        if a != b:
                            raise GeneratorError('Constant name ({0} != {1}) mismatch in constant group {2}' \
                                                 .format(a, b, constant_group.get_underscore_name()))

                        a = known_constant.get_value()
                        b = constant.get_value()

                        if a != b:
                            raise GeneratorError('Constant value ({0} != {1}) mismatch in constant group {2}' \
                                                 .format(a, b, constant_group.get_underscore_name()))

                    constant_group = None
                    break

                if constant_group != None:
                    self.constant_groups.append(constant_group)

        for raw_example in raw_data['examples']:
            self.examples.append(generator.get_example_class()(raw_example, self))

    def get_generator(self): # parent
        return self.generator

    def is_released(self):
        return self.raw_data['released']

    def is_documented(self):
        return self.raw_data['documented']

    def get_author(self):
        return self.raw_data['author']

    def get_api_version(self):
        return self.raw_data['api_version']

    def get_doc(self):
        return self.raw_data.get('doc', {'en': '', 'de': ''})

    def get_category(self):
        return self.raw_data['category']

    def get_camel_case_category(self):
        return self.get_category().replace(' ', '')

    def get_underscore_category(self):
        return self.get_camel_case_category().lower()

    def get_upper_case_category(self):
        return self.get_underscore_category().upper()

    def get_dash_category(self):
        return self.get_underscore_category().replace('_', '-')

    def is_brick(self):
        return self.get_category() == 'Brick'

    def is_bricklet(self):
        return self.get_category() == 'Bricklet'

    def get_device_identifier(self):
        return self.raw_data['device_identifier']

    def _get_name(self): # for NameMixin
        return self.raw_data['name']

    def get_initial_name(self):
        name = self.get_name()

        if name.endswith(' V2'):
            name = name[:-3]
        elif name.endswith('mA'):
            name = name[:-2]
        elif name in ['IO4', 'IO16']:
            name = 'IO'

        name = re.sub('[0-9]+x[0-9]+', '', name).replace('  ', ' ').strip()

        if ' ' not in name and (name.isupper() or self.is_brick()):
            return name.replace(' ', '').lower()

        words = name.split(' ')

        def shorten(word):
            if (len(word) < 3 and word.isupper()) or word.isdigit():
                return word.lower()
            else:
                return word[0].lower()

        return ''.join(map(shorten, words))

    def get_short_display_name(self):
        return self.raw_data['display_name']

    def get_long_display_name(self):
        display_name = self.raw_data['display_name']

        if display_name.endswith(' 2.0'):
            parts = display_name.split(' ')
            parts.insert(-1, self.get_category())

            return ' '.join(parts)
        else:
            return display_name + ' ' + self.get_category()

    def get_manufacturer(self):
        return self.raw_data['manufacturer']

    def get_description(self):
        return self.raw_data['description']

    def get_git_name(self):
        return self.get_dash_name() + '-' + self.get_dash_category()

    def get_git_directory(self):
        global_root_directory = os.path.normpath(os.path.join(self.get_generator().get_bindings_root_directory(), '..', '..'))
        git_directory = os.path.join(global_root_directory, self.get_git_name())

        return git_directory

    def get_packets(self, type_=None):
        if type_ is None:
            if self.generator.is_doc():
                return self.all_packets
            else:
                return self.all_packets_without_doc_only
        elif type_ == 'function':
            if self.generator.is_doc():
                return self.all_function_packets
            else:
                return self.all_function_packets_without_doc_only
        elif type_ == 'callback':
            return self.callback_packets
        else:
            raise GeneratorError('Invalid packet type ' + str(type_))

    def get_packet_names(self, type_=None):
        return [packet.get_name() for packet in self.get_packets(type_)]

    def get_callback_count(self):
        return len(self.callback_packets)

    def get_constant_groups(self):
        return self.constant_groups

    def get_formatted_constants(self, constant_format, char_format="'{0}'", **extra_value):
        constants = []

        for constant_group in self.get_constant_groups():
            for constant in constant_group.get_constants():
                if constant_group.get_type() == 'char':
                    value = char_format.format(constant.get_value())
                else:
                    value = str(constant.get_value())

                constants.append(constant_format.format(constant_group_upper_case_name=constant_group.get_upper_case_name(),
                                                        constant_group_camel_case_name=constant_group.get_camel_case_name(),
                                                        constant_upper_case_name=constant.get_upper_case_name(),
                                                        constant_camel_case_name=constant.get_camel_case_name(),
                                                        constant_value=value,
                                                        **extra_value))

        return ''.join(constants)

    def get_doc_rst_path(self):
        if not self.get_generator().is_doc():
            raise GeneratorError("Invalid call in non-doc generator")

        filename = '{0}_{1}_{2}.rst'.format(self.get_camel_case_name(),
                                            self.get_camel_case_category(),
                                            self.get_generator().get_doc_rst_filename_part())

        return os.path.join(self.get_generator().get_bindings_root_directory(),
                            'doc',
                            self.get_generator().get_language(),
                            filename)

    def get_doc_rst_ref_name(self):
        if not self.get_generator().is_doc():
            raise GeneratorError("Invalid call in non-doc generator")

        return self.get_underscore_name() + '_' + self.get_underscore_category()

    def specialize_doc_rst_links(self, text, specializer, prefix=None):
        for keyword, type_ in [('func', 'function'), ('cb', 'callback')]:
            for packet in self.get_packets(type_):
                names = [packet.get_name()]

                if packet.has_high_level():
                    names.append(packet.get_name().replace(' Low Level', ''))

                for name in names:
                    generic_name = ':{0}:`{1}`'.format(keyword, name)
                    special_name = specializer(packet, packet.has_high_level() and not name.endswith(' Low Level'))

                    text = text.replace(generic_name, special_name)

            if prefix != None:
                p = '(?<!:' + prefix + ')(:' + keyword + ':`[^`]*`)'
            else:
                p = '(:' + keyword + ':`[^`]*`)'

            m = re.search(p, text)

            if m != None:
                raise GeneratorError('Unknown :{0}: found: {1}'.format(keyword, m.group(1)))

        return text

    def get_examples(self):
        return self.examples

class Example(NameMixin):
    def __init__(self, raw_data, device):
        self.raw_data = raw_data
        self.device = device

        check_name(raw_data['name'])

        self.functions = []
        self.cleanups = []

        if 'functions' in raw_data:
            for index, raw_function in enumerate(raw_data['functions']):
                if raw_function[0] == 'getter':
                    self.functions.append(self.get_generator().get_example_getter_function_class()(raw_function[1:], index, self))
                elif raw_function[0] == 'setter':
                    self.functions.append(self.get_generator().get_example_setter_function_class()(raw_function[1:], index, self))
                elif raw_function[0] == 'callback':
                    self.functions.append(self.get_generator().get_example_callback_function_class()(raw_function[1:], index, self))
                elif raw_function[0] == 'callback_period':
                    self.functions.append(self.get_generator().get_example_callback_period_function_class()(raw_function[1:], index, self))
                elif raw_function[0] == 'callback_threshold':
                    self.functions.append(self.get_generator().get_example_callback_threshold_function_class()(raw_function[1:], index, self))
                else:
                    self.functions.append(self.get_generator().get_example_special_function_class()(raw_function, index, self))

        if 'cleanups' in raw_data:
            for index, raw_cleanup in enumerate(raw_data['cleanups']):
                if raw_cleanup[0] == 'setter':
                    self.cleanups.append(self.get_generator().get_example_setter_function_class()(raw_cleanup[1:], -index, self))
                else:
                    raise GeneratorError('only setters are allowed as cleanup functions')

    def get_device(self): # parent
        return self.device

    def get_generator(self):
        return self.get_device().get_generator()

    def _get_name(self): # for NameMixin
        return self.raw_data['name']

    def get_functions(self):
        return self.functions

    def get_cleanups(self):
        return self.cleanups

    def is_incomplete(self):
        try:
            return self.raw_data['incomplete']
        except KeyError:
            return False

    def get_dummy_uid(self):
        if self.get_device().is_brick():
            return 'XXYYZZ'
        else:
            return 'XYZ'

class ExampleItem:
    def __init__(self, raw_data, index, example):
        self.raw_data = raw_data
        self.index = index
        self.example = example

    def get_index(self):
        return self.index

    def get_example(self):
        return self.example

    def get_device(self):
        return self.get_example().get_device()

    def get_generator(self):
        return self.get_example().get_generator()

class ExampleArgument(ExampleItem):
    def __init__(self, raw_data, index, function, example):
        ExampleItem.__init__(self, raw_data, index, example)

        self.function = function

        if len(raw_data) != 2:
            raise GeneratorError('Invalid ExampleArgument: ' + repr(raw_data))

    def get_function(self): # parent
        return self.function

    def get_element(self):
        function_name = self.get_function().get_name()
        value = self.get_value()

        for packet in self.get_device().get_packets('function'):
            if packet.get_name() == function_name:
                return packet.get_elements('in')[self.get_index()]

        return None

    def get_type(self):
        return self.raw_data[0]

    def get_value(self):
        return self.raw_data[1]

    def get_value_constant(self):
        element = self.get_element()

        if element != None:
            constant_group = element.get_constant_group()

            if constant_group:
                for constant in constant_group.get_constants():
                    if self.get_value() == constant.get_value():
                        return constant

        return None

class ExampleParameter(ExampleItem, NameMixin):
    def __init__(self, raw_data, index, function, example):
        ExampleItem.__init__(self, raw_data, index, example)

        self.function = function

        if len(raw_data) != 6:
            raise GeneratorError('Invalid ExampleParameter: ' + repr(raw_data))

        if len(raw_data[0]) != 2:
            raise GeneratorError('Invalid ExampleParameter: ' + repr(raw_data))

        check_name(raw_data[0][0])

    def get_function(self): # parent
        return self.function

    def _get_name(self): # for NameMixin
        return self.raw_data[0][0]

    def get_label_name(self):
        return self.raw_data[0][1]

    def get_type(self):
        return self.raw_data[1]

    def get_divisor(self):
        return self.raw_data[2]

    def get_formatted_divisor(self, template, cast=float):
        divisor = self.get_divisor()

        if divisor == None:
            return ''
        else:
            return template.format(cast(divisor))

    def get_unit_raw_name(self):
        return self.raw_data[3]

    def get_unit_formatted_raw_name(self, template):
        raw_name = self.get_unit_raw_name()

        if raw_name == None:
            return ''
        else:
            return template.format(raw_name)

    def get_unit_final_name(self):
        return self.raw_data[4]

    def get_unit_formatted_final_name(self, template):
        final_name = self.get_unit_final_name()

        if final_name == None:
            return ''
        else:
            return template.format(final_name)

    def get_range(self):
        return self.raw_data[5]

    def get_formatted_range(self, template):
        range = self.get_range()

        if range == None:
            return ''
        else:
            return template.format(range[0], range[1])

    def get_formatted_comment(self):
        template = '{unit_raw_name}{range}'

        return template.format(unit_raw_name=self.get_unit_formatted_raw_name(' (parameter has unit {0})'),
                               range=self.get_formatted_range(' (parameter has range {0} to {1})'))

class ExampleResult(ExampleItem, NameMixin):
    def __init__(self, raw_data, index, function, example):
        ExampleItem.__init__(self, raw_data, index, example)

        self.function = function

        if len(raw_data) != 6:
            raise GeneratorError('Invalid ExampleResult: ' + repr(raw_data))

        if len(raw_data[0]) != 2:
            raise GeneratorError('Invalid ExampleResult: ' + repr(raw_data))

        check_name(raw_data[0][0])

    def get_function(self): # parent
        return self.function

    def _get_name(self): # for NameMixin
        return self.raw_data[0][0]

    def get_label_name(self):
        return self.raw_data[0][1]

    def get_type(self):
        return self.raw_data[1]

    def get_divisor(self):
        return self.raw_data[2]

    def get_formatted_divisor(self, template, cast=float):
        divisor = self.get_divisor()

        if divisor == None:
            return ''
        else:
            return template.format(cast(divisor))

    def get_unit_raw_name(self):
        return self.raw_data[3]

    def get_unit_formatted_raw_name(self, template):
        raw_name = self.get_unit_raw_name()

        if raw_name == None:
            return ''
        else:
            return template.format(raw_name)

    def get_unit_final_name(self):
        return self.raw_data[4]

    def get_unit_formatted_final_name(self, template):
        final_name = self.get_unit_final_name()

        if final_name == None:
            return ''
        else:
            return template.format(final_name)

    def get_range(self):
        return self.raw_data[5]

    def get_formatted_range(self, template):
        range = self.get_range()

        if range == None:
            return ''
        else:
            return template.format(range[0], range[1])

    def get_formatted_comment(self):
        template = '{unit_raw_name}{range}'

        return template.format(unit_raw_name=self.get_unit_formatted_raw_name(' (unit is {0})'),
                               range=self.get_formatted_range(' (range is {0} to {1})'))

class ExampleGetterFunction(ExampleItem, NameMixin):
    def __init__(self, raw_data, index, example):
        ExampleItem.__init__(self, raw_data, index, example)

        self.results = []
        self.arguments = []

        if len(raw_data) != 3:
            raise GeneratorError('Invalid ExampleGetterFunction: ' + repr(raw_data))

        if len(raw_data[0]) != 2:
            raise GeneratorError('Invalid ExampleGetterFunction: ' + repr(raw_data))

        check_name(raw_data[0][0])

        for index, raw_result in enumerate(raw_data[1]):
            self.results.append(self.get_generator().get_example_result_class()(raw_result, index, self, example))

        for index, raw_argument in enumerate(raw_data[2]):
            self.arguments.append(self.get_generator().get_example_argument_class()(raw_argument, index, self, example))

    def _get_name(self): # for NameMixin
        return self.raw_data[0][0]

    def get_comment_name(self):
        return self.raw_data[0][1]

    def get_results(self):
        return self.results

    def get_arguments(self):
        return self.arguments

class ExampleSetterFunction(ExampleItem, NameMixin):
    def __init__(self, raw_data, index, example):
        ExampleItem.__init__(self, raw_data, index, example)

        if len(raw_data) != 4:
            raise GeneratorError('Invalid ExampleSetterFunction: ' + repr(raw_data))

        check_name(raw_data[0])

        self.arguments = []

        for index, raw_argument in enumerate(raw_data[1]):
            self.arguments.append(self.get_generator().get_example_argument_class()(raw_argument, index, self, example))

    def _get_name(self): # for NameMixin
        return self.raw_data[0]

    def get_arguments(self):
        return self.arguments

    def get_comment1(self):
        return self.raw_data[2]

    def get_formatted_comment1(self, template, empty, linebreak):
        comment1 = self.get_comment1()

        if comment1 == None:
            return empty
        else:
            return template.format(re.sub('[ ]+\n', '\n', comment1.replace('\n', linebreak)))

    def get_comment2(self):
        return self.raw_data[3]

    def get_formatted_comment2(self, template, empty):
        comment2 = self.get_comment2()

        if comment2 == None:
            return empty
        else:
            return template.format(comment2)

class ExampleCallbackFunction(ExampleItem, NameMixin):
    def __init__(self, raw_data, index, example):
        ExampleItem.__init__(self, raw_data, index, example)

        if len(raw_data) != 4:
            raise GeneratorError('Invalid ExampleCallbackFunction: ' + repr(raw_data))

        if len(raw_data[0]) != 2:
            raise GeneratorError('Invalid ExampleCallbackFunction: ' + repr(raw_data))

        check_name(raw_data[0][0])

        self.parameters = []

        for index, raw_parameter in enumerate(raw_data[1]):
            self.parameters.append(self.get_generator().get_example_parameter_class()(raw_parameter, index, self, example))

    def _get_name(self): # for NameMixin
        return self.raw_data[0][0]

    def get_comment_name(self):
        return self.raw_data[0][1]

    def get_parameters(self):
        return self.parameters

    def get_override_comment(self):
        return self.raw_data[2]

    def get_formatted_override_comment(self, template, empty, linebreak):
        comment1 = self.get_override_comment()

        if comment1 == None:
            return empty
        else:
            return template.format(re.sub('[ ]+\n', '\n', comment1.replace('\n', linebreak)))

    def get_extra_message(self):
        return self.raw_data[3]

    def get_formatted_extra_message(self, template):
        extra_message = self.get_extra_message()

        if extra_message == None:
            return ''
        else:
            return template.format(extra_message)

class ExampleCallbackPeriodFunction(ExampleItem, NameMixin):
    def __init__(self, raw_data, index, example):
        ExampleItem.__init__(self, raw_data, index, example)

        if len(raw_data) != 3:
            raise GeneratorError('Invalid ExampleCallbackPeriodFunction: ' + repr(raw_data))

        if len(raw_data[0]) != 2:
            raise GeneratorError('Invalid ExampleCallbackPeriodFunction: ' + repr(raw_data))

        check_name(raw_data[0][0])

        self.arguments = []

        for index, raw_argument in enumerate(raw_data[1]):
            self.arguments.append(self.get_generator().get_example_argument_class()(raw_argument, index, self, example))

    def _get_name(self): # for NameMixin
        return self.raw_data[0][0]

    def get_comment_name(self):
        return self.raw_data[0][1]

    def get_arguments(self):
        return self.arguments

    def get_period(self): # msec
        return self.raw_data[2]

    def get_formatted_period(self):
        period_msec = self.get_period()

        if period_msec == None:
            return None, None, None

        period_sec = round(period_msec / 1000.0, 3)
        period_sec_short = str(period_sec).rstrip('0').rstrip('.') + 's'
        period_sec_long = str(period_sec).rstrip('0').rstrip('.') + ' seconds'

        if period_sec_long == '1 seconds':
            period_sec_long = 'second'

        return period_msec, period_sec_short, period_sec_long

class ExampleCallbackThresholdMinimumMaximum(ExampleItem):
    def __init__(self, raw_data, index, function, example):
        ExampleItem.__init__(self, raw_data, index, example)

        if len(raw_data) != 2:
            raise GeneratorError('Invalid ExampleCallbackThresholdMinimumMaximum: ' + repr(raw_data))

        self.function = function
        self.corresponding_callback = None

        for other in reversed(example.get_functions()):
            if isinstance(other, ExampleCallbackFunction):
                if other.get_name() == function.get_name() + ' Reached':
                    self.corresponding_callback = other

        if self.corresponding_callback == None:
            raise GeneratorError('ExampleThresholdMinimumMaximum without corresponding callback: ' + repr(raw_data))

    def get_function(self): # parent
        return self.function

    def get_corresponding_callback(self):
        return self.corresponding_callback

    def get_corresponding_parameter(self):
        return self.get_corresponding_callback().get_parameters()[len(self.get_function().get_arguments()) + self.get_index()]

    def get_type(self):
        return self.get_corresponding_parameter().get_type()

    def get_minimum(self):
        return self.raw_data[0]

    def get_formatted_minimum(self, template='{minimum}*{divisor}'):
        minimum = self.get_minimum()
        divisor = self.get_corresponding_parameter().get_divisor()

        if minimum == 0 or divisor == None:
            return str(minimum)
        else:
            return template.format(minimum=minimum,
                                   divisor=int(divisor),
                                   result=minimum * int(divisor))

    def get_maximum(self):
        return self.raw_data[1]

    def get_formatted_maximum(self, template='{maximum}*{divisor}'):
        maximum = self.get_maximum()
        divisor = self.get_corresponding_parameter().get_divisor()

        if maximum == 0 or divisor == None:
            return str(maximum)
        else:
            return template.format(maximum=maximum,
                                   divisor=int(divisor),
                                   result=maximum * int(divisor))

    def get_unit_comment(self):
        template = '{unit_raw_name}{range}'
        parameter = self.get_corresponding_parameter()

        return template.format(unit_raw_name=parameter.get_unit_formatted_raw_name(' (unit is {0})'),
                               range=parameter.get_formatted_range(' (range is {0} to {1})'))

class ExampleCallbackThresholdFunction(ExampleItem, NameMixin):
    def __init__(self, raw_data, index, example):
        ExampleItem.__init__(self, raw_data, index, example)

        if len(raw_data) != 4:
            raise GeneratorError('Invalid ExampleCallbackThresholdFunction: ' + repr(raw_data))

        if len(raw_data[0]) != 2:
            raise GeneratorError('Invalid ExampleCallbackThresholdFunction: ' + repr(raw_data))

        check_name(raw_data[0][0])

        self.arguments = []

        for index, raw_argument in enumerate(raw_data[1]):
            self.arguments.append(self.get_generator().get_example_argument_class()(raw_argument, index, self, example))

        self.minimum_maximums = []

        for index, raw_minimum_maximum in enumerate(raw_data[3]):
            self.minimum_maximums.append(self.get_generator().get_example_callback_threshold_minimum_maximum_class()(raw_minimum_maximum, index, self, example))

    def _get_name(self): # for NameMixin
        return self.raw_data[0][0]

    def get_comment_name(self):
        return self.raw_data[0][1]

    def get_arguments(self):
        return self.arguments

    def get_option_char(self):
        return self.raw_data[2]

    def get_option_comment(self):
        option_char = self.get_option_char()
        minimums = []
        minimums_with_unit = []
        maximums_with_unit = []

        for minimum_maximum in self.get_minimum_maximums():
            unit_final_name = minimum_maximum.get_corresponding_parameter().get_unit_formatted_final_name(' {0}')

            minimums.append(str(minimum_maximum.get_minimum()))
            minimums_with_unit.append(str(minimum_maximum.get_minimum()) + unit_final_name)
            maximums_with_unit.append(str(minimum_maximum.get_maximum()) + unit_final_name)

        if option_char == '>':
            return 'greater than {0}'.format(', '.join(minimums_with_unit))
        elif option_char == '<':
            return 'smaller than {0}'.format(', '.join(minimums_with_unit))
        elif option_char == 'o':
            return 'outside of {0} to {1}'.format(', '.join(minimums),
                                                  ', '.join(maximums_with_unit))
        else:
            raise GeneratorError('Unhandled option: ' + option_char)

    def get_minimum_maximums(self):
        return self.minimum_maximums

class ExampleSpecialFunction(ExampleItem):
    def __init__(self, raw_data, index, example):
        ExampleItem.__init__(self, raw_data, index, example)

        if raw_data[0] not in ['empty', 'debounce_period', 'sleep', 'wait', 'loop_header', 'loop_footer']:
            raise GeneratorError('Invalid special function type: ' + raw_data[0])

    def get_type(self):
        return self.raw_data[0]

    def get_debounce_period(self):
        return self.raw_data[1]

    def get_formatted_debounce_period(self):
        period_msec = self.get_debounce_period()
        period_sec = str(round(period_msec / 1000.0, 3)).rstrip('0').rstrip('.') + ' seconds'

        if period_sec == '1 seconds':
            period_sec = '1 second'

        return period_msec, period_sec

    def get_sleep_duration(self): # msec
        return self.raw_data[1]

    def get_sleep_comment1(self):
        return self.raw_data[2]

    def get_formatted_sleep_comment1(self, template, empty, linebreak):
        comment1 = self.get_sleep_comment1()

        if comment1 == None:
            return empty
        else:
            return template.format(re.sub('[ ]+\n', '\n', comment1.replace('\n', linebreak)))

    def get_sleep_comment2(self):
        return self.raw_data[3]

    def get_formatted_sleep_comment2(self, template, empty):
        comment2 = self.get_sleep_comment2()

        if comment2 == None:
            return empty
        else:
            return template.format(comment2)

    def get_loop_header_limit(self):
        return self.raw_data[1]

    def get_loop_header_comment(self):
        return self.raw_data[2]

    def get_formatted_loop_header_comment(self, template, empty, linebreak):
        comment = self.get_loop_header_comment()

        if comment == None:
            return empty
        else:
            return template.format(re.sub('[ ]+\n', '\n', comment.replace('\n', linebreak)))

class Generator:
    check_bindings_root_directory_name = True

    def __init__(self, bindings_root_directory, language):
        self.bindings_root_directory = bindings_root_directory
        self.language = language # en or de
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")

        if self.check_bindings_root_directory_name:
            directory_name = os.path.split(self.get_bindings_root_directory())[1]

            if self.get_bindings_name() != directory_name:
                raise GeneratorError("bindings root directory '{0}' and bindings name '{1}' do not match".format(directory_name, self.get_bindings_name()))

    def get_bindings_name(self):
        raise GeneratorError("get_bindings_name() not implemented")

    def get_bindings_display_name(self):
        raise GeneratorError("get_bindings_display_name() not implemented")

    def get_device_class(self):
        return Device

    def get_packet_class(self):
        return Packet

    def get_element_class(self):
        return Element

    def get_constant_group_class(self):
        return ConstantGroup

    def get_constant_class(self):
        return Constant

    def get_example_class(self):
        return Example

    def get_example_argument_class(self):
        return ExampleArgument

    def get_example_parameter_class(self):
        return ExampleParameter

    def get_example_result_class(self):
        return ExampleResult

    def get_example_getter_function_class(self):
        return ExampleGetterFunction

    def get_example_setter_function_class(self):
        return ExampleSetterFunction

    def get_example_callback_function_class(self):
        return ExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return ExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return ExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return ExampleCallbackThresholdFunction

    def get_example_special_function_class(self):
        return ExampleSpecialFunction

    def get_bindings_root_directory(self):
        return self.bindings_root_directory

    def get_language(self):
        return self.language # en or de

    def get_header_comment(self, kind):
        comment = {
        'asterisk': """/* ***********************************************************
 * This file was automatically generated on {0}.      *
 *                                                           *
 * {1} Bindings Version {2}.{3}.{4}{5}*
 *                                                           *
 * If you have a bugfix for this file and want to commit it, *
 * please fix the bug in the generator. You can find a link  *
 * to the generators git repository on tinkerforge.com       *
 *************************************************************/
""",
        'hash': """#############################################################
# This file was automatically generated on {0}.      #
#                                                           #
# {1} Bindings Version {2}.{3}.{4}{5}#
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generators git repository on tinkerforge.com       #
#############################################################
""",
        'curly': """{{
  This file was automatically generated on {0}.

  {1} Bindings Version {2}.{3}.{4}

  If you have a bugfix for this file and want to commit it,
  please fix the bug in the generator. You can find a link
  to the generator git on tinkerforge.com
}}
""",
        'xml': """<!--
  This file was automatically generated on {0}.

  {1} Bindings Version {2}.{3}.{4}

  If you have a bugfix for this file and want to commit it,
  please fix the bug in the generator. You can find a link
  to the generators git repository on tinkerforge.com
-->
"""
        }

        version = get_changelog_version(self.get_bindings_root_directory())
        display_name = self.get_bindings_display_name()
        delta = 38 - len(display_name) - len(''.join(map(str, version)))

        return comment[kind].format(self.date,
                                    display_name,
                                    version[0],
                                    version[1],
                                    version[2],
                                    ' '*delta)

    def is_doc(self):
        return False

    def compare_examples(self, example1, example2):
        return cmp(example1[2], example2[2])

    def prepare(self):
        pass

    def generate(self, device):
        raise GeneratorError("generate() not implemented")

    def finish(self):
        pass

class DocGenerator(Generator):
    def __init__(self, *args, **kwargs):
        Generator.__init__(self, *args, **kwargs)

        if self.get_bindings_name() != self.get_doc_rst_filename_part().lower():
            raise GeneratorError("bindings name '{0}' and doc rst name '{1}' do not match".format(self.get_bindings_name(), self.get_doc_rst_filename_part()))

    def get_doc_rst_filename_part(self):
        raise GeneratorError("get_doc_rst_filename_part() not implemented")

    def get_doc_example_regex(self):
        raise GeneratorError("get_doc_example_regex() not implemented")

    def is_doc(self):
        return True

    def prepare(self):
        recreate_directory(os.path.join(self.get_bindings_root_directory(), 'doc', self.get_language()))

    def finish(self):
        # Copy IPConnection examples
        example_regex = self.get_doc_example_regex()

        if example_regex != None:
            print(' * ip_connection')

            examples = find_examples(self.get_bindings_root_directory(), example_regex, self.compare_examples)
            copy_files = []

            for example in examples:
                include = 'IPConnection_{0}_{1}'.format(self.get_doc_rst_filename_part(), example[0].replace(' ', '_'))
                copy_files.append((example[1], include))

            copy_examples(copy_files, self.get_bindings_root_directory())

class BindingsGenerator(Generator):
    bindings_subdirectory_name = 'bindings'

    def __init__(self, *args, **kwargs):
        Generator.__init__(self, *args, **kwargs)

        self.released_files = []

    def prepare(self):
        recreate_directory(os.path.join(self.get_bindings_root_directory(), self.bindings_subdirectory_name))

    def finish(self):
        with open(os.path.join(self.get_bindings_root_directory(), self.get_bindings_name() + '_released_files.py'), 'wb') as f:
            f.write('released_files = ' + repr(self.released_files))

class ZipGenerator(Generator):
    def create_zip_file(self, source_path):
        version = get_changelog_version(self.get_bindings_root_directory())
        zipname = 'tinkerforge_{0}_bindings_{1}_{2}_{3}.zip'.format(self.get_bindings_name(), *version)

        with ChangedDirectory(source_path):
            execute(['/usr/bin/zip', '-q', '-r', zipname, '.'])
            shutil.copy(zipname, self.get_bindings_root_directory())

class ExamplesGenerator(Generator):
    skip_existing_incomplete_example = False
    forbid_execution = True

    def __init__(self, *args, **kwargs):
        Generator.__init__(self, *args, **kwargs)

        if self.forbid_execution:
            raise GeneratorError('ExamplesGenerator execution is forbidden')

    def get_examples_directory(self, device):
        return os.path.join(device.get_git_directory(), 'software', 'examples', self.get_bindings_name())

def examples_tester_worker(cookie, args, env):
    try:
        with open(os.devnull) as DEVNULL:
            output = subprocess.check_output(args, env=env, stderr=subprocess.STDOUT, stdin=DEVNULL)
    except subprocess.CalledProcessError as e:
        return cookie, e.output, e.returncode == 0
    except Exception as e:
        return cookie, 'ExamplesTester Exception: ' + str(e), False

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
