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

lang = 'en'

def shift_right(text, n):
    return text.replace('\n', '\n' + ' '*n)

def strip_trailing_whitespace(text):
    lines = []

    for line in text.split('\n'):
        lines.append(line.rstrip())

    return '\n'.join(lines)

def get_changelog_version(root_dir):
    r = re.compile(r'^\S+: (\d+)\.(\d+)\.(\d+) \(\S+\)')
    last = None

    with open(os.path.join(root_dir, 'changelog.txt'), 'r') as f:
        for line in f.readlines():
            m = r.match(line)

            if m is not None:
                last = (m.group(1), m.group(2), m.group(3))

    if last == None:
        raise GeneratorError('no version found in changelog: ' + root_dir)

    return last

def get_image_size(path):
    from PIL import Image

    return Image.open(path).size

def select_lang(d):
    if lang in d:
        return d[lang]

    if 'en' in d:
        return d['en']

    return "Missing '{0}' documentation".format(lang)

def make_rst_header(device, has_device_identifier_constant=True):
    bindings_display_name = device.get_generator().get_bindings_display_name()
    ref_name = device.get_generator().get_bindings_name()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    full_title = '{0} - {1}'.format(bindings_display_name, device.get_long_display_name())
    full_title_underline = '='*len(full_title)
    device_identifier_constant = {'en': '.. |device_identifier_constant| replace:: There is also a :ref:`constant <{0}_{1}_{2}_constants>` for the device identifier of this {3}.\n',
                                  'de': '.. |device_identifier_constant| replace:: Es gibt auch eine :ref:`Konstante <{0}_{1}_{2}_constants>` für den Device Identifier dieses {3}.\n'}

    if device.is_released():
        orphan = ''
    else:
        orphan = ':orphan:\n'

    if has_device_identifier_constant:
        device_identifier_constant = select_lang(device_identifier_constant).format(device.get_name().under,
                                                                                    device.get_category().under,
                                                                                    ref_name,
                                                                                    device.get_category().camel)
    else:
        device_identifier_constant = '.. |device_identifier_constant| unicode:: 0xA0\n   :trim:\n'

    ref = '.. _{0}_{1}_{2}:\n'.format(device.get_name().under, device.get_category().under, ref_name)

    return '{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n'.format(gen_text_rst.format(date),
                                                   orphan,
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
                                     device.get_name().under)

    s = select_lang(summary).format(bindings_name_link,
                                    device_name,
                                    device.get_long_display_name(),
                                    device.get_name().under + '_' + device.get_category().under)

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
<https://creativecommons.org/publicdomain/zero/1.0/>`__.
""",
        'de': """
{0}

Beispiele
---------

Der folgende Beispielcode ist `Public Domain (CC0 1.0)
<https://creativecommons.org/publicdomain/zero/1.0/deed.de>`__.
"""
    }

    imp_code = """
{0}
{1}

{3}

.. literalinclude:: {2}{language} {4}
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

    ref = '.. _{0}_{1}_{2}_examples:\n'.format(device.get_name().under,
                                               device.get_category().under,
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

        include = '{0}_{1}_{2}_{3}'.format(device.get_name().camel, device.get_category().camel, include_name, f[0].replace(' ', '_'))
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
            downloads.append('`Test ({0}) <https://www.tinkerforge.com/{1}/doc/Software/Examples/JavaScript/{2}>`__'.format(display_name, lang, include))

        if add_tvpl_test_link and include.endswith('.tvpl'):
            downloads.append('`Test ({0}) <https://www.tinkerforge.com/{1}/tvpl/editor.html?example={2}/{3}/{4}>`__'
                             .format(display_name, lang, device.get_category().under, device.get_name().under, f[0]))

        lang_placeholder = "\n :language:" if language is not None else ""

        examples += imp.format(title, '^'*len(title), include, ', '.join(downloads), language if language is not None else "", language=lang_placeholder)

    copy_examples(copy_files, device.get_generator().get_root_dir())

    return examples

def default_example_sort_key(example):
    return example[2], example[0] # lines, filename

def find_examples(examples_dir, filename_regex, sort_key=default_example_sort_key):
    compiled_filename_regex = re.compile(filename_regex)
    examples = []

    if os.path.isdir(examples_dir):
        for example_filename in sorted(os.listdir(examples_dir)):
            if compiled_filename_regex.match(example_filename) is not None:
                example_path = os.path.join(examples_dir, example_filename)
                lines = 0

                if example_path.endswith('.vi.png'):
                    size = get_image_size(example_path)
                    lines = size[0] * size[1]
                elif example_path.endswith('.vi'):
                    lines = os.stat(example_path).st_size
                else:
                    with open(example_path, 'r') as f:
                        lines = len(f.readlines())

                examples.append((example_filename, example_path, lines))

        examples.sort(key=sort_key)

    return examples

def find_device_examples(device, filename_regex):
    bindings_name = device.get_generator().get_bindings_name()
    examples_dir = os.path.join(device.get_git_dir(), 'software', 'examples', bindings_name)

    return find_examples(examples_dir, filename_regex, sort_key=device.get_generator().get_example_sort_key)

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

re_camel_to_space = re.compile('([A-Z][A-Z][a-z])|([a-z][A-Z])|([a-zA-Z][0-9])')

def camel_to_space(name):
    return re_camel_to_space.sub(lambda m: m.group()[:1] + " " + m.group()[1:], name)

def format_since_firmware(device, packet):
    since = packet.get_since_firmware()

    if since == None or since <= [2, 0, 0]:
        return ''

    if device.is_brick():
        suffix = 'Firmware'
    else:
        suffix = 'Plugin'

    return '\n.. versionadded:: {1}.{2}.{3}$nbsp;({0})\n'.format(suffix, *since)

def default_constant_format(prefix, constant_group, constant, value):
    return '* {0}{1}_{2} = {3}\n'.format(prefix, constant_group.get_name().upper,
                                         constant.get_name().upper, value)

def format_constants(prefix, packet,
                     constants_name=None,
                     char_format_func="'{0}'".format,
                     bool_format_func=str,
                     constant_format_func=default_constant_format,
                     constants_intro=None,
                     show_constant_group=False,
                     group_format_func=lambda g: "\n" + g.get_name().space + "\n"):
    if constants_name == None:
        constants_name = {'en': 'constants', 'de': 'Konstanten'}

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
        if show_constant_group:
            constants.append(group_format_func(constant_group))
        for constant in constant_group.get_constants():
            if constant_group.get_type() == 'char':
                value = char_format_func(constant.get_value())
            elif constant_group.get_type() == 'bool':
                value = bool_format_func(constant.get_value())
            else:
                value = str(constant.get_value())

            constants.append(constant_format_func(prefix, constant_group, constant, value))

    if len(constants) == 0:
        return ''
    result = select_lang(constants_intro).format(select_lang(constants_name))
    if show_constant_group: # newline before first constant group is redundant
        result = result[:-1]
    return result + ''.join(constants)

def default_function_id_constant_format(prefix, func_name, value):
    return '* {0}FUNCTION_{1} = {2}\n'.format(prefix, func_name.upper, value)

def format_function_id_constants(prefix, device, constants_name=None, constant_format_func=default_function_id_constant_format):
    if constants_name == None:
        constants_name = {'en': 'constants', 'de': 'Konstanten'}

    str_constants = {
        'en': """
The following function ID {0} are available for this function:

""",
        'de': """
Die folgenden Funktions ID {0} sind für diese Funktion verfügbar:

"""
    }
    str_constants = select_lang(str_constants).format(select_lang(constants_name))

    for packet in device.get_packets('function'):
        if len(packet.get_elements(direction='out', high_level=True)) == 0 and packet.get_function_id() >= 0:
            str_constants += constant_format_func(prefix,
                                                 packet.get_name(skip=-2 if packet.has_high_level() else 0),
                                                 packet.get_function_id())

    return str_constants

def handle_rst_word(text, parameter=None, parameters=None, constants=None):
    if parameter == None:
        parameter = {'en': 'parameter', 'de': 'Parameter'}

    if parameters == None:
        parameters = {'en': 'parameters', 'de': 'Parameter'}

    if constants == None:
        constants = {'en': 'constants', 'de': 'Konstanten'}

    text = text.replace(":word:`parameter`", select_lang(parameter))
    text = text.replace(":word:`parameters`", select_lang(parameters))
    text = text.replace(":word:`constants`", select_lang(constants))

    return text

def handle_rst_param(text, format_parameter):
    return re.sub(r'\:param\:\`([^\`]+)\`', lambda match: format_parameter(match.group(1)), text)

def handle_rst_substitutions(text, packet):
    subsitutions = packet.get_doc_substitutions()

    if len(subsitutions) == 0:
        return text

    for key, value in subsitutions.items():
        text = text.replace('|' + key + '|', value)

    return text

def under_to_space(name):
    return ' '.join([part.capitalize() for part in name.split('_')])

def recreate_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)

    os.makedirs(path)

def specialize_template(template_filename, destination_filename, replacements, check_completeness=True):
    lines = []
    replaced = set()

    with open(template_filename, 'r') as f:
        for line in f.readlines():
            for key in replacements:
                replaced_line = line.replace(key, replacements[key])

                if replaced_line != line:
                    replaced.add(key)

                line = replaced_line

            lines.append(line)

    if check_completeness and replaced != set(replacements.keys()):
        raise GeneratorError('Not all replacements for {0} have been applied'.format(template_filename))

    with open(destination_filename, 'w') as f:
        f.writelines(lines)

def make_c_like_bitmask(value, shift='{0} << {1}', combine='({0}) | ({1})'):
    if value == 0:
        return str(value)

    parts = []

    for i in range(64):
        if (value & (1 << i)) != 0:
            parts.append(shift.format(1, i))

    if len(parts) == 1:
        return parts[0]

    if len(parts) == 2:
        return combine.format(parts[0], parts[1])

    raise GeneratorError('More than to bits ware not supported yet')

def wrap_non_empty(prefix, middle, suffix):
    if len(middle) == 0:
        return ''

    return prefix + middle + suffix

def execute(args, **kwargs):
    if subprocess.call(args, **kwargs) != 0:
        raise GeneratorError("Command '{0}' failed".format(' '.join(args) if isinstance(args, list) else args))

def generate(root_dir, language, generator_class):
    # default config
    subgenerate(root_dir, language, generator_class, 'tinkerforge')

    # custom configs
    config_base_path = os.path.join(root_dir, '..', 'configs')

    for config_name in os.listdir(config_base_path):
        if config_name == '__pycache__':
            continue

        config_path = os.path.join(config_base_path, config_name)

        if not os.path.isdir(config_path):
            continue

        if re.match('^[a-z0-9_]+$', config_name) == None:
            raise GeneratorError('Invalid config name: {0}'.format(config_name))

        subgenerate(root_dir, language, generator_class, config_name)

def subgenerate(root_dir, language, generator_class, config_name):
    global lang
    lang = language

    print('--> {0}'.format(config_name))

    config_path_parts = [root_dir, '..', 'configs']

    if config_name != 'tinkerforge':
        config_path_parts.append(config_name)

    config_path = os.path.join(*config_path_parts)

    if config_path not in sys.path:
        sys.path.append(config_path)

    configs = sorted(os.listdir(config_path))

    common_device_packets = copy.deepcopy(__import__('device_commonconfig').common_packets)

    brick_infos = []
    bricklet_infos = []
    device_identifiers = set()

    generator = generator_class(root_dir, config_name, language)
    generator.prepare()

    def prepare_common_packets(com, common_packets):
        features = com['features']

        for common_packet in common_packets:
            if common_packet.get('is_virtual', False):
                continue

            if com['name'] in common_packet['since_firmware']:
                common_packet['since_firmware'] = common_packet['since_firmware'][com['name']]
            else:
                common_packet['since_firmware'] = common_packet['since_firmware']['*']

            if common_packet['since_firmware'] == None:
                common_packet['to_be_removed'] = True

            if common_packet['feature'] not in features:
                common_packet['to_be_removed'] = True

        return filter(lambda x: 'to_be_removed' not in x, common_packets)

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

            if 'common_included' not in com:
                com['packets'].extend(prepare_common_packets(com, copy.deepcopy(common_device_packets)))
                com['common_included'] = True

            device = generator.get_device_class()(com, generator)
            device_identifier = device.get_device_identifier()

            if device_identifier in device_identifiers:
                raise GeneratorError('Device identifier {0} is not unique'.format(device_identifier))

            device_identifiers.add(device_identifier)

            # only collect device_infos for default config
            if config_name == 'tinkerforge':
                if device.is_brick():
                    ref_name = device.get_name().under + '_brick'
                    hardware_doc_name = device.get_short_display_name().replace(' ', '_').replace('/', '_').replace('-', '').replace('2.0', 'V2').replace('3.0', 'V3') + '_Brick'
                    software_doc_prefix = device.get_name().camel + '_Brick'

                    if device.get_device_identifier() != 17:
                        firmware_url_part = device.get_name().under
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
                                   False,
                                   device.is_released(),
                                   device.is_documented(),
                                   device.is_discontinued(),
                                   True,
                                   device.get_description())

                    brick_infos.append(device_info)
                else:
                    ref_name = device.get_name().under + '_bricklet'
                    hardware_doc_name = device.get_short_display_name().replace(' ', '_').replace('/', '_').replace('-', '').replace('2.0', 'V2').replace('3.0', 'V3')
                    software_doc_prefix = device.get_name().camel + '_Bricklet'
                    firmware_url_part = device.get_name().under

                    device_info = (device.get_device_identifier(),
                                   device.get_long_display_name(),
                                   device.get_short_display_name(),
                                   ref_name,
                                   hardware_doc_name,
                                   software_doc_prefix,
                                   device.get_git_name(),
                                   firmware_url_part,
                                   device.has_comcu(),
                                   device.is_released(),
                                   device.is_documented(),
                                   device.is_discontinued(),
                                   True,
                                   device.get_description())

                    bricklet_infos.append(device_info)

            generator.generate(device)

    generator.finish()

    # only update device_infos.py for default config
    if config_name == 'tinkerforge':
        brick_infos.append((None, 'Debug Brick', 'Debug', 'debug_brick', 'Debug_Brick', None, 'debug-brick', None, False, True, True, False, False,
                            {'en': 'For Firmware Developers: JTAG and serial console',
                             'de': 'Für Firmware Entwickler: JTAG und serielle Konsole'}))

        bricklet_infos.append((None, 'Breakout Bricklet', 'Breakout', 'breakout_bricklet', 'Breakout', None, 'breakout-bricklet', None, False, True, True, False, False,
                               {'en': 'Makes all Bricklet signals available',
                                'de': 'Macht alle Bricklet Signale zugänglich'}))

        with open(os.path.join(root_dir, '..', 'device_infos.py'), 'w') as f:
            f.write('# -*- coding: utf-8 -*-\n')
            f.write('from collections import namedtuple\n')
            f.write('\n')
            f.write("DeviceInfo = namedtuple('DeviceInfo', 'identifier long_display_name short_display_name ref_name hardware_doc_name software_doc_prefix git_name firmware_url_part has_comcu is_released is_documented is_discontinued has_bindings description')\n")
            f.write('\n')
            f.write('brick_infos = \\\n')
            f.write('[\n')

            for brick_info in sorted(brick_infos, key=lambda info: info[2].lower()):
                f.write('    DeviceInfo{0},\n'.format(brick_info))

            f.write(']\n')
            f.write('\n')
            f.write('bricklet_infos = \\\n')
            f.write('[\n')

            for bricklet_info in sorted(bricklet_infos, key=lambda info: info[2].lower()):
                f.write('    DeviceInfo{0},\n'.format(bricklet_info))

            f.write(']\n')

check_name_valid_word_head = re.compile('^[A-Z]+[A-Z0-9]*[a-z0-9]*$')
check_name_valid_word_tail = re.compile('^[A-Z0-9]+[a-z0-9]*$')
check_name_valid_word_constant = re.compile('^[A-Z0-9]+[a-z0-9]*$') # constants are allowed to start with numbers
check_name_exceptions_whole_name = ['Industrial Dual 0 20mA', 'Industrial Dual 0 20mA V2']
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
        elif display_name.endswith(' 3.0'):
            display_name_to_check = display_name_to_check.replace(' 3.0', ' V3')

        if display_name in ['IO-4', 'IO-16', 'IO-4 2.0', 'IO-16 2.0']: # exceptions for legacy dash rules
            display_name_to_check = display_name_to_check.replace('-', '')
        else:
            display_name_to_check = display_name_to_check.replace('-', ' ')

        if name != display_name_to_check:
            raise GeneratorError("Name '{0}' and display name '{1}' ({2}) mismatch" \
                                 .format(name, display_name, display_name_to_check))

def break_string(string, indent_marker, space=' ', continuation='', indent_head='',
                 indent_tail='', indent_suffix='', max_length=90, break_point='<BP>'):
    result = string.replace(break_point, space)

    if len(result) > max_length:
        if len(indent_marker) > 0:
            prefix = result.split(indent_marker)[0].split('\n')[-1].lstrip('\r')
            tabs = 0

            for c in prefix:
                if c != '\t':
                    break

                tabs += 1
        else:
            prefix = ''
            tabs = 0

        indent = '\t' * tabs + indent_head + ' ' * (len(prefix) - tabs - len(indent_head) + len(indent_marker) - len(indent_tail)) + indent_tail + indent_suffix
        parts = string.split(break_point)
        result = parts[0]

        for part in parts[1:]:
            line = (result.split('\n')[-1] + space + part.split('\n')[0]).replace('\t', '    ') + continuation

            if len(line) > max_length:
                result += continuation + '\n' + indent + part
            else:
                result += space + part

    return result

def check_output_and_error(*popenargs, **kwargs):
    process = subprocess.Popen(stdout=subprocess.PIPE, stderr=subprocess.PIPE, *popenargs, **kwargs)
    output, error = process.communicate()
    exit_code = process.poll()

    return exit_code, (output + error).decode('utf-8')

class GeneratorError(Exception):
    pass

NameFlavors = namedtuple('NameFlavors', 'space lower camel headless under upper dash camel_abbrv')

class FlavoredName(object):
    def __init__(self, name):
        self.words = name.split(' ')
        self.cache = {}

    def get(self, skip=0, suffix=''):
        key = str(skip) + ',' + suffix

        try:
            return self.cache[key]
        except KeyError:
            if skip < 0:
                words = self.words[:skip]
            else:
                words = self.words[skip:]

            words[-1] += suffix

            self.cache[key] = NameFlavors(' '.join(words), # space
                                          ' '.join(words).lower(), # lower
                                          ''.join(words), # camel
                                          ''.join([words[0].lower()] + words[1:]), # headless
                                          '_'.join(words).lower(), # under
                                          '_'.join(words).upper(), # upper
                                          '-'.join(words).lower(), # dash
                                          ''.join([word.capitalize() for word in words])) # camel_abbrv; like camel, but produces GetSpiTfp... instead of GetSPITFP...

            return self.cache[key]

class Constant(object):
    def __init__(self, raw_data, constant_group):
        self.raw_data = raw_data
        self.constant_group = constant_group

        if len(raw_data) != 2:
            raise GeneratorError('Invalid Constant: ' + repr(raw_data))

        check_name(raw_data[0], is_constant=True)

        self.name = FlavoredName(raw_data[0])

    def get_constant_group(self): # parent
        return self.constant_group

    def get_device(self):
        return self.get_constant_group().get_device()

    def get_generator(self):
        return self.get_constant_group().get_generator()

    def get_name(self, *args, **kwargs):
        return self.name.get(*args, **kwargs)

    def get_value(self):
        return self.raw_data[1]

class ConstantGroup(object):
    def __init__(self, type_, raw_data, device):
        self.type_ = type_
        self.raw_data = raw_data
        self.device = device
        self.elements = []
        self.constants = []

        if len(raw_data) != 2:
            raise GeneratorError('Invalid ConstantGroup: ' + repr(raw_data))

        check_name(raw_data[0])

        self.name = FlavoredName(raw_data[0])

        for raw_constant in raw_data[1]:
            self.constants.append(self.get_generator().get_constant_class()(raw_constant, self))

    def get_elements(self): # parents
        return self.elements

    def get_device(self):
        return self.device

    def get_generator(self):
        return self.get_device().get_generator()

    def get_name(self, *args, **kwargs):
        return self.name.get(*args, **kwargs)

    def get_type(self):
        return self.type_

    def get_constants(self):
        return self.constants

    def add_elements(self, elements):
        self.elements += elements

class Element(object):
    def __init__(self, raw_data, packet, level, role):
        self.raw_data = raw_data
        self.packet = packet
        self.level = level
        self.role = role
        self.constant_group = None

        check_name(raw_data[0])

        self.name = FlavoredName(raw_data[0])

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

    def get_name(self, *args, **kwargs):
        return self.name.get(*args, **kwargs)

    def get_type(self):
        return self.raw_data[1]

    def get_cardinality(self):
        return self.raw_data[2]

    def get_direction(self):
        return self.raw_data[3]

    def get_role(self):
        return self.role

    def get_level(self):
        return self.level

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

        return self.get_item_size() * self.get_cardinality()

class Stream(object):
    def __init__(self, raw_data, data_element, packet, direction):
        self.raw_data = raw_data
        self.data_element = data_element
        self.packet = packet
        self.direction = direction

        check_name(raw_data['name'])

        self.name = FlavoredName(raw_data['name'])

        if raw_data.get('single_chunk', False):
            if 'fixed_length' in raw_data:
                raise GeneratorError("Cannot mix fixed-length and single-chunk for high-level feature 'stream_{0}'".format(direction))

            self.length_element = packet.get_elements(name=self.get_name().space + ' Length', direction=direction)[0]
            self.chunk_offset_element = None
            self.chunk_data_element = packet.get_elements(name=self.get_name().space + ' Data', direction=direction)[0]
        elif 'fixed_length' in raw_data:
            self.length_element = None
            self.chunk_offset_element = packet.get_elements(name=self.get_name().space + ' Chunk Offset', direction=direction)[0]
            self.chunk_data_element = packet.get_elements(name=self.get_name().space + ' Chunk Data', direction=direction)[0]
        else:
            self.length_element = packet.get_elements(name=self.get_name().space + ' Length', direction=direction)[0]
            self.chunk_offset_element = packet.get_elements(name=self.get_name().space + ' Chunk Offset', direction=direction)[0]
            self.chunk_data_element = packet.get_elements(name=self.get_name().space + ' Chunk Data', direction=direction)[0]

        if 'fixed_length' not in raw_data and \
           not raw_data.get('single_chunk', False) \
           and self.length_element == None:
            raise GeneratorError("Missing length element for high-level feature 'stream_{0}'".format(direction))

        if not raw_data.get('single_chunk', False) and \
           self.chunk_offset_element == None:
            raise GeneratorError("Missing chunk-offset element for high-level feature 'stream_{0}'".format(direction))

        if self.chunk_data_element == None:
            raise GeneratorError("Missing chunk-data element for high-level feature 'stream_{0}'".format(direction))

        if 'fixed_length' not in raw_data and \
           not raw_data.get('single_chunk', False) and \
           self.length_element.get_type() != self.chunk_offset_element.get_type():
            raise GeneratorError("Type of length element and chunk-offset are different")

    def get_packet(self): # parent
        return self.packet

    def get_name(self, *args, **kwargs):
        return self.name.get(*args, **kwargs)

    def get_length_element(self):
        return self.length_element

    def get_chunk_offset_element(self):
        return self.chunk_offset_element

    def get_chunk_data_element(self):
        return self.chunk_data_element

    def get_data_element(self):
        return self.data_element

    def get_fixed_length(self, default=None):
        return self.raw_data.get('fixed_length', default)

    def has_single_chunk(self):
        return self.raw_data.get('single_chunk', False)

class StreamIn(Stream):
    def __init__(self, raw_data, data_element, packet):
        Stream.__init__(self, raw_data, data_element, packet, 'in')

    def has_short_write(self):
        return self.raw_data.get('short_write', False)

class StreamOut(Stream):
    def __init__(self, raw_data, data_element, packet):
        Stream.__init__(self, raw_data, data_element, packet, 'out')

class Packet(object):
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
    valid_doc_types = set(['bf',
                           'af',
                           'ccf',
                           'c'])

    def __init__(self, raw_data, device):
        self.raw_data = raw_data
        self.device = device
        self.elements = []
        self.high_level = {}

        check_name(raw_data['name'])

        self.name = FlavoredName(raw_data['name'])

        if raw_data['doc'][0] not in Packet.valid_doc_types:
            raise GeneratorError('Invalid packet doc type: ' + raw_data['doc'][0])

        if 'high_level' in raw_data and not raw_data['name'].endswith(' Low Level'):
            raise GeneratorError("Name of packet with high-level features has to end with 'Low Level'")

        raw_stream_in = raw_data.get('high_level', {}).get('stream_in', None)
        raw_stream_out = raw_data.get('high_level', {}).get('stream_out', None)
        stream_name = None
        stream_fixed_length = None

        if raw_stream_in != None and raw_stream_out != None:
            raise GeneratorError("Cannot combine high-level features 'stream_in' and 'stream_out'")

        if raw_stream_in != None:
            stream_name = raw_stream_in['name']
            stream_fixed_length = raw_stream_in.get('fixed_length', None)
            stream_single_chunk = raw_stream_in.get('single_chunk', False)

        if raw_stream_out != None:
            stream_name = raw_stream_out['name']
            stream_fixed_length = raw_stream_out.get('fixed_length', None)
            stream_single_chunk = raw_stream_out.get('single_chunk', False)

        stream_size_type = None
        stream_data_element = None
        payload_in_size = 0
        payload_out_size = 0

        for raw_element in self.raw_data['elements']:
            raw_element = list(raw_element)
            level = 'normal'
            role = None

            if stream_name != None and raw_element[0].startswith(stream_name + ' '):
                if raw_element[0].endswith(' Length'):
                    level = 'low'
                    role = 'stream_length'
                    stream_size_type = raw_element[1]
                elif raw_element[0].endswith(' Offset'):
                    level = 'low'
                    role = 'stream_chunk_offset'
                    stream_size_type = raw_element[1]
                elif raw_element[0].endswith(' Data'):
                    level = 'low'
                    role = 'stream_chunk_data'
                elif raw_element[0].endswith(' Written'):
                    level = 'low'
                    role = 'stream_chunk_written'

            element = device.get_generator().get_element_class()(raw_element, self, level, role)

            if element.get_type() not in Packet.valid_types:
                raise GeneratorError('Invalid element type: ' + element.get_type())

            if element.get_cardinality() < 1:
                raise GeneratorError('Invalid element cardinality: ' + element.get_cardinality())

            if element.get_direction() not in ['in', 'out']:
                raise GeneratorError('Invalid element direction: ' + element.get_direction())

            if element.get_direction() == 'in' and len(self.elements) > 0 and self.elements[-1].get_direction() == 'out':
                raise GeneratorError("'in' element cannot come after 'out' element")

            if element.get_direction() == 'in':
                payload_in_size += element.get_size()
            else:
                payload_out_size += element.get_size()

            if payload_in_size > 64 or payload_out_size > 64:
                raise GeneratorError('Payload too long: ' + raw_data['name'])

            self.elements.append(element)

            if level == 'low':
                if element.get_name().space.endswith(' Data'):
                    if stream_size_type == None:
                        raise GeneratorError('Missing stream-size-type')

                    if stream_size_type not in ['uint8', 'uint16', 'uint32']:
                        raise GeneratorError('Unsupported stream-size-type: {0}'.format(stream_size_type))

                    raw_element = copy.deepcopy(raw_element)
                    raw_element[0] = stream_name

                    if stream_fixed_length != None:
                        raw_element[2] = stream_fixed_length
                    elif stream_single_chunk:
                        raw_element[2] = -raw_element[2]
                    else:
                        raw_element[2] = -((1 << int(stream_size_type.replace('uint', ''))) - 1)

                    if stream_data_element != None:
                        raise GeneratorError('Multiple stream-data-elements')

                    stream_data_element = device.get_generator().get_element_class()(raw_element, self, 'high', 'stream_data')

                    self.elements.append(stream_data_element)
                elif element.get_name().space.endswith(' Written'):
                    if stream_size_type == None:
                        raise GeneratorError('Missing stream-size-type')

                    raw_element = copy.deepcopy(raw_element)
                    raw_element[0] = stream_name + ' Written'
                    raw_element[1] = stream_size_type

                    self.elements.append(device.get_generator().get_element_class()(raw_element, self, 'high', 'stream_written'))

        if raw_stream_in != None:
            stream_in = StreamIn(raw_stream_in, stream_data_element, self)
            self.high_level['stream_in'] = stream_in

        if raw_stream_out != None:
            stream_out = StreamOut(raw_stream_out, stream_data_element, self)
            self.high_level['stream_out'] = stream_out

        if self.raw_data.get('response_expected') not in [None, 'always_true', 'true', 'false']:
            raise GeneratorError('Invalid response-expected value')

        self.constant_groups = []

        for element in self.elements:
            constant_group = element.get_constant_group()

            if constant_group is None:
                continue

            for known_constant_group in self.constant_groups:
                if constant_group.get_name().under != known_constant_group.get_name().under:
                    continue

                if constant_group.get_type() != known_constant_group.get_type():
                    raise GeneratorError('Multiple instance of constant group {0} with different types' \
                                         .format(constant_group.get_name().under))

                for constant, known_constant in zip(constant_group.get_constants(), known_constant_group.get_constants()):
                    a = known_constant.get_name().under
                    b = constant.get_name().under

                    if a != b:
                        raise GeneratorError('Constant item name ({0} != {1}) mismatch in constant group {2}' \
                                             .format(a, b, constant_group.get_name().under))

                    a = known_constant.get_value()
                    b = constant.get_value()

                    if a != b:
                        raise GeneratorError('Constant item value ({0} != {1}) mismatch in constant group {2}' \
                                             .format(a, b, constant_group.get_name().under))

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

    def get_name(self, *args, **kwargs):
        return self.name.get(*args, **kwargs)

    def get_elements(self, name=None, direction=None, high_level=False, role=None):
        if direction not in [None, 'in', 'out']:
            raise GeneratorError('Invalid element direction ' + direction)

        elements = []

        for element in self.elements:
            if name != None and element.get_name().space != name:
                continue

            if direction != None and element.get_direction() != direction:
                continue

            if high_level and element.get_level() == 'low':
                continue

            if not high_level and element.get_level() == 'high':
                continue

            if role != None and element.get_role() != role:
                continue

            elements.append(element)

        return elements

    def has_high_level(self):
        return len(self.high_level) > 0

    def get_high_level(self, feature):
        if feature == 'stream_*':
            if 'stream_in' in self.high_level:
                return self.high_level['stream_in']

            if 'stream_out' in self.high_level:
                return self.high_level['stream_out']

            return None

        return self.high_level.get(feature)

    def get_since_firmware(self):
        return self.raw_data['since_firmware']

    def get_formatted_since_firmware(self):
        since_firmware = self.get_since_firmware()

        if since_firmware == None:
            return None

        return '.'.join([str(x) for x in self.get_since_firmware()])

    def get_response_expected(self):
        response_expected = self.raw_data.get('response_expected')

        if response_expected == None:
            if len(self.get_elements(direction='out')) > 0:
                response_expected = 'always_true'
            elif self.get_doc_type() == 'ccf' or self.get_high_level('stream_in') != None:
                response_expected = 'true'
            else:
                response_expected = 'false'

        return response_expected

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

    def get_corresponding_callback_value_getter(self):
        for packet in self.device.get_packets():
            if packet.raw_data.get('corresponding_getter') == self.raw_data.get('name'):
                return self

            if self.raw_data.get('corresponding_getter') == packet.raw_data.get('name'):
                return packet

        return None

    def is_part_of_callback_value(self):
        # Packet is for callback value configuration
        if 'corresponding_getter' in self.raw_data:
            return True

        # Check if this packet is the getter of a callback value
        for packet in self.device.get_packets():
            if packet.raw_data.get('corresponding_getter') == self.raw_data['name']:
                return True

        # If packet is not for configuration and not the getter, it is not part of a callback value
        return False

    def get_callback_value_name(self):
        try:
            return self.get_corresponding_callback_value_getter().get_name().under.replace('get_', '')
        except:
            return None

    def get_function_id(self):
        return self.raw_data['function_id']

    def get_request_size(self):
        size = 8 # header

        for element in self.get_elements(direction='in'):
            size += element.get_size()

        return size

    def get_response_size(self):
        size = 8 # header

        for element in self.get_elements(direction='out'):
            size += element.get_size()

        return size

    def get_constant_groups(self):
        return self.constant_groups

    def get_formatted_constants(self, constant_format, char_format_func="'{0}'".format, bool_format_func=str, **extra_value):
        constants = []

        for constant_group in self.get_constant_groups():
            for constant in constant_group.get_constants():
                if constant_group.get_type() == 'char':
                    value = char_format_func(constant.get_value())
                elif constant_group.get_type() == 'bool':
                    value = bool_format_func(constant.get_value())
                else:
                    value = str(constant.get_value())

                constants.append(constant_format.format(constant_group_name_upper=constant_group.get_name().upper,
                                                        constant_group_name_camel=constant_group.get_name().camel,
                                                        constant_name_upper=constant.get_name().upper,
                                                        constant_name_camel=constant.get_name().camel,
                                                        constant_value=value,
                                                        **extra_value))

        return ''.join(constants)

    def has_prototype_in_device(self):
        return self.raw_data.get('prototype_in_device', False)

    def is_virtual(self):
        return self.raw_data.get('is_virtual', False)

class Device(object):
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

        self.category = FlavoredName(raw_data['category'])
        self.name = FlavoredName(raw_data['name'])

        next_function_id = 1

        for raw_packet in raw_data['packets']:
            if not 'function_id' in raw_packet:
                raw_packet['function_id'] = next_function_id
            else:
                next_function_id = raw_packet['function_id']

            next_function_id += 1

            packet = generator.get_packet_class()(raw_packet, self)

            self.all_packets.append(packet)

            if packet.get_function_id() >= 0:
                self.all_packets_without_doc_only.append(packet)

        if not self.is_released() and self.get_api_version() != [2, 0, 0]:
            raise GeneratorError('Unreleased device must have API version 2.0.0')

        since_firmwares = set()

        for packet in self.all_packets:
            since_firmware = packet.get_since_firmware()

            if since_firmware != None and since_firmware > [2, 0, 0]:
                since_firmwares.add(packet.get_formatted_since_firmware())

        since_firmwares = list(since_firmwares)

        if len(since_firmwares) + self.get_api_version_extra() != self.get_api_version()[2]:
            raise GeneratorError('API version mismatch: len({0}) + {1} != {2}'
                                 .format(since_firmwares, self.get_api_version_extra(), self.get_api_version()[2]))

        function_names = set()
        callback_names = set()

        for packet in self.all_packets:
            if packet.get_type() == 'function':
                if packet.get_name().lower in function_names:
                    raise GeneratorError('Function name is not unique: ' + packet.get_name().space)
                else:
                    function_names.add(packet.get_name().lower)

                self.all_function_packets.append(packet)

                if packet.get_function_id() >= 0:
                    self.all_function_packets_without_doc_only.append(packet)
            elif packet.get_type() == 'callback':
                if 'Callback' in packet.get_name().space:
                    raise GeneratorError("Callback name cannot contain 'Callback': " + packet.get_name().space)

                if packet.get_name().lower in callback_names:
                    raise GeneratorError('Callback name is not unique: ' + packet.get_name().space)
                else:
                    callback_names.add(packet.get_name().lower)

                self.callback_packets.append(packet)
            else:
                raise GeneratorError('Invalid packet type ' + packet.get_type())

        self.constant_groups = []

        for packet in self.all_packets:
            for constant_group in packet.get_constant_groups():
                for known_constant_group in self.constant_groups:
                    if constant_group.get_name().under != known_constant_group.get_name().under:
                        continue

                    if constant_group.get_type() != known_constant_group.get_type():
                        raise GeneratorError('Multiple instance of constant group {0} with different types' \
                                             .format(constant_group.get_name().under))

                    for constant, known_constant in zip(constant_group.get_constants(), known_constant_group.get_constants()):
                        a = known_constant.get_name().under
                        b = constant.get_name().under

                        if a != b:
                            raise GeneratorError('Constant name ({0} != {1}) mismatch in constant group {2}' \
                                                 .format(a, b, constant_group.get_name().under))

                        a = known_constant.get_value()
                        b = constant.get_value()

                        if a != b:
                            raise GeneratorError('Constant value ({0} != {1}) mismatch in constant group {2}' \
                                                 .format(a, b, constant_group.get_name().under))

                    constant_group = None
                    break

                if constant_group != None:
                    self.constant_groups.append(constant_group)

        for raw_example in raw_data['examples']:
            self.examples.append(generator.get_example_class()(raw_example, self))

    def get_generator(self): # parent
        return self.generator

    def has_comcu(self):
        return 'comcu_bricklet' in self.raw_data['features']

    def is_released(self):
        return self.raw_data['released']

    def is_documented(self):
        return self.raw_data['documented']

    def is_discontinued(self):
        return self.raw_data['discontinued']

    def get_author(self):
        return self.raw_data['author']

    def get_api_version(self):
        return self.raw_data['api_version']

    def get_api_version_extra(self):
        return self.raw_data.get('api_version_extra', 0)

    def get_doc(self):
        return self.raw_data.get('doc', {'en': '', 'de': ''})

    def get_category(self, *args, **kwargs):
        return self.category.get(*args, **kwargs)

    def is_brick(self):
        return self.get_category().space == 'Brick'

    def is_bricklet(self):
        return self.get_category().space == 'Bricklet'

    def get_device_identifier(self):
        return self.raw_data['device_identifier']

    def has_callback_value(self):
        # If the device has a packet with 'corresponding_getter' field, it has callback values
        for packet in self.all_packets:
            if 'corresponding_getter' in packet.raw_data:
                return True

        return False

    def get_name(self, *args, **kwargs):
        return self.name.get(*args, **kwargs)

    def get_initial_name(self):
        name = self.get_name().space

        if name.endswith(' V2'):
            name = name[:-3]

        if name.endswith(' V3'):
            name = name[:-3]

        if name.endswith('mA'):
            name = name[:-2]

        if name in ['IO4', 'IO16']:
            name = 'IO'

        name = re.sub('[0-9]+x[0-9]+', '', name).replace('  ', ' ').strip()

        if ' ' not in name and (name.isupper() or self.is_brick()):
            return name.replace(' ', '').lower()

        words = name.split(' ')

        def shorten(word):
            if (len(word) < 3 and word.isupper()) or word.isdigit():
                return word.lower()

            return word[0].lower()

        return ''.join(map(shorten, words))

    def get_short_display_name(self):
        return self.raw_data['display_name']

    def get_long_display_name(self):
        display_name = self.raw_data['display_name']

        if display_name.endswith(' 2.0') or display_name.endswith(' 3.0'):
            parts = display_name.split(' ')
            parts.insert(-1, self.get_category().space)

            return ' '.join(parts)

        return display_name + ' ' + self.get_category().space

    def get_manufacturer(self):
        return self.raw_data['manufacturer']

    def get_description(self):
        return self.raw_data['description']

    def get_git_name(self):
        return self.get_name().dash + '-' + self.get_category().dash

    def get_git_dir(self):
        global_root_dir = os.path.normpath(os.path.join(self.get_generator().get_root_dir(), '..', '..'))

        return os.path.join(global_root_dir, self.get_git_name())

    def get_packets(self, type_=None):
        if type_ == None:
            if self.generator.is_doc():
                return self.all_packets

            return self.all_packets_without_doc_only

        if type_ == 'function':
            if self.generator.is_doc():
                return self.all_function_packets

            return self.all_function_packets_without_doc_only

        if type_ == 'callback':
            return self.callback_packets

        raise GeneratorError('Invalid packet type ' + str(type_))

    def get_packet_names(self, type_=None):
        return [packet.get_name().space for packet in self.get_packets(type_)]

    def get_callback_count(self):
        return len(self.callback_packets)

    def get_constant_groups(self):
        return self.constant_groups

    def get_formatted_constants(self, constant_format, char_format_func="'{0}'".format, bool_format_func=str, **extra_value):
        constants = []

        for constant_group in self.get_constant_groups():
            for constant in constant_group.get_constants():
                if constant_group.get_type() == 'char':
                    value = char_format_func(constant.get_value())
                elif constant_group.get_type() == 'bool':
                    value = bool_format_func(constant.get_value())
                else:
                    value = str(constant.get_value())

                constants.append(constant_format.format(constant_group_name_upper=constant_group.get_name().upper,
                                                        constant_group_name_camel=constant_group.get_name().camel,
                                                        constant_name_upper=constant.get_name().upper,
                                                        constant_name_camel=constant.get_name().camel,
                                                        constant_value=value,
                                                        **extra_value))

        return ''.join(constants)

    def get_doc_rst_path(self):
        if not self.get_generator().is_doc():
            raise GeneratorError("Invalid call in non-doc generator")

        filename = '{0}_{1}_{2}.rst'.format(self.get_name().camel,
                                            self.get_category().camel,
                                            self.get_generator().get_doc_rst_filename_part())

        return os.path.join(self.get_generator().get_doc_dir(),
                            self.get_generator().get_language(),
                            filename)

    def get_doc_rst_ref_name(self):
        if not self.get_generator().is_doc():
            raise GeneratorError("Invalid call in non-doc generator")

        return self.get_name().under + '_' + self.get_category().under

    def specialize_doc_rst_links(self, text, specializer, prefix=None):
        for keyword, type_ in [('func', 'function'), ('cb', 'callback')]:
            for packet in self.get_packets(type_):
                names = [packet.get_name().space]

                if packet.has_high_level():
                    names.append(packet.get_name(skip=-2).space)

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

class Example(object):
    def __init__(self, raw_data, device):
        self.raw_data = raw_data
        self.device = device

        check_name(raw_data['name'])

        self.name = FlavoredName(raw_data['name'])

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
                elif raw_function[0] == 'callback_configuration':
                    self.functions.append(self.get_generator().get_example_callback_configuration_function_class()(raw_function[1:], index, self))
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

    def get_name(self, *args, **kwargs):
        return self.name.get(*args, **kwargs)

    def get_description(self):
        return self.raw_data.get('description', None)

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

        return 'XYZ'

class ExampleItem(object):
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
        function_name = self.get_function().get_name().space

        for packet in self.get_device().get_packets('function'):
            if packet.get_name().space == function_name:
                return packet.get_elements(direction='in')[self.get_index()]

        function_name = self.get_function().get_name().space + ' Low Level'

        for packet in self.get_device().get_packets('function'):
            if packet.get_name().space == function_name:
                return packet.get_elements(direction='in', high_level=True)[self.get_index()]

        return None

    def get_type(self):
        return self.raw_data[0]

    def get_value(self):
        return self.raw_data[1]

    def get_value_constant(self, value):
        element = self.get_element()

        if element != None:
            constant_group = element.get_constant_group()

            if constant_group:
                for constant in constant_group.get_constants():
                    if value == constant.get_value():
                        return constant

        return None

class ExampleParameter(ExampleItem):
    def __init__(self, raw_data, index, function, example):
        ExampleItem.__init__(self, raw_data, index, example)

        self.function = function

        if len(raw_data) != 6:
            raise GeneratorError('Invalid ExampleParameter: ' + repr(raw_data))

        if len(raw_data[0]) != 2:
            raise GeneratorError('Invalid ExampleParameter: ' + repr(raw_data))

        check_name(raw_data[0][0])

        self.name = FlavoredName(raw_data[0][0])

    def get_function(self): # parent
        return self.function

    def get_element(self):
        function_type = self.get_function().get_type()
        function_name = self.get_function().get_name().space

        for packet in self.get_device().get_packets(type_=function_type):
            if packet.get_name().space == function_name:
                return packet.get_elements(direction='in' if function_type == 'function' else 'out')[self.get_index()]
            if "LowLevel" in packet.get_name().camel and packet.get_name(skip=-2).space == function_name:
                return packet.get_elements(direction='in' if function_type == 'function' else 'out')[self.get_index()]

        return None

    def get_name(self, *args, **kwargs):
        return self.name.get(*args, **kwargs)

    def get_label_count(self):
        label = self.raw_data[0][1]

        if label == None:
            return 0

        if isinstance(label, str):
            return 1

        if isinstance(label, list):
            if self.get_cardinality() != len(label):
                raise GeneratorError('Invalid label count')

            return len(label)

        raise GeneratorError('Invalid label type: ' + type(label))

    def get_label_name(self, index=0):
        label = self.raw_data[0][1]

        if label == None or isinstance(label, str):
            if index != 0:
                raise GeneratorError('Invalid index: ' + str(index))

            return label

        return label[index]

    def get_type(self):
        return self.raw_data[1]

    def get_cardinality(self):
        return self.raw_data[2]

    def get_divisor(self):
        return self.raw_data[3]

    def get_formatted_divisor(self, template, cast=float):
        divisor = self.get_divisor()

        if divisor == None:
            return ''

        return template.format(cast(divisor))

    def get_unit_name(self):
        return self.raw_data[4]

    def get_formatted_unit_name(self, template):
        unit_name = self.get_unit_name()

        if unit_name == None:
            return ''

        return template.format(unit_name)

    def get_range(self):
        return self.raw_data[5]

    def get_formatted_range(self, template):
        range_ = self.get_range()

        if range_ == None:
            return ''

        return template.format(range_[0], range_[1])

    def get_formatted_comment(self, template):
        formatted_range = self.get_formatted_range('Range: {0} to {1}')

        if len(formatted_range) == 0:
            return ''

        return template.format(formatted_range)

    def get_constant_group(self):
        element = self.get_element()

        if element != None:
            return element.get_constant_group()

        return None

class ExampleResult(ExampleItem):
    def __init__(self, raw_data, index, function, example):
        ExampleItem.__init__(self, raw_data, index, example)

        self.function = function

        if len(raw_data) != 6:
            raise GeneratorError('Invalid ExampleResult: ' + repr(raw_data))

        if len(raw_data[0]) != 2:
            raise GeneratorError('Invalid ExampleResult: ' + repr(raw_data))

        check_name(raw_data[0][0])

        self.name = FlavoredName(raw_data[0][0])

    def get_function(self): # parent
        return self.function

    def get_element(self):
        function_name = self.get_function().get_name().space

        for packet in self.get_device().get_packets(type_='function'):
            if packet.get_name().space == function_name:
                return packet.get_elements(direction='out')[self.get_index()]

        return None

    def get_name(self, *args, **kwargs):
        return self.name.get(*args, **kwargs)

    def get_label_count(self):
        label = self.raw_data[0][1]

        if label == None:
            return 0

        if isinstance(label, str):
            return 1

        if isinstance(label, list):
            if self.get_cardinality() != len(label):
                raise GeneratorError('Invalid label count')

            return len(label)

        raise GeneratorError('Invalid label type: ' + type(label))

    def get_label_name(self, index=0):
        label = self.raw_data[0][1]

        if label == None or isinstance(label, str):
            if index != 0:
                raise GeneratorError('Invalid index: ' + str(index))

            return label

        return label[index]

    def get_type(self):
        return self.raw_data[1]

    def get_cardinality(self):
        return self.raw_data[2]

    def get_divisor(self):
        return self.raw_data[3]

    def get_formatted_divisor(self, template, cast=float):
        divisor = self.get_divisor()

        if divisor == None:
            return ''

        return template.format(cast(divisor))

    def get_unit_name(self):
        return self.raw_data[4]

    def get_formatted_unit_name(self, template):
        unit_name = self.get_unit_name()

        if unit_name == None:
            return ''

        return template.format(unit_name)

    def get_range(self):
        return self.raw_data[5]

    def get_formatted_range(self, template):
        range_ = self.get_range()

        if range_ == None:
            return ''

        return template.format(range_[0], range_[1])

    def get_formatted_comment(self, template):
        formatted_range = self.get_formatted_range('Range: {0} to {1}')

        if len(formatted_range) == 0:
            return ''

        return template.format(formatted_range)

    def get_constant_group(self):
        element = self.get_element()

        if element != None:
            return element.get_constant_group()

        return None

class ExampleGetterFunction(ExampleItem):
    def __init__(self, raw_data, index, example):
        ExampleItem.__init__(self, raw_data, index, example)

        self.results = []
        self.arguments = []

        if len(raw_data) != 3:
            raise GeneratorError('Invalid ExampleGetterFunction: ' + repr(raw_data))

        if len(raw_data[0]) != 2:
            raise GeneratorError('Invalid ExampleGetterFunction: ' + repr(raw_data))

        check_name(raw_data[0][0])

        self.name = FlavoredName(raw_data[0][0])

        for index, raw_result in enumerate(raw_data[1]):
            self.results.append(self.get_generator().get_example_result_class()(raw_result, index, self, example))

        for index, raw_argument in enumerate(raw_data[2]):
            self.arguments.append(self.get_generator().get_example_argument_class()(raw_argument, index, self, example))

    def get_type(self):
        return 'function'

    def get_name(self, *args, **kwargs):
        return self.name.get(*args, **kwargs)

    def get_comment_name(self):
        return self.raw_data[0][1]

    def get_results(self):
        return self.results

    def get_arguments(self):
        return self.arguments

class ExampleSetterFunction(ExampleItem):
    def __init__(self, raw_data, index, example):
        ExampleItem.__init__(self, raw_data, index, example)

        if len(raw_data) != 4:
            raise GeneratorError('Invalid ExampleSetterFunction: ' + repr(raw_data))

        check_name(raw_data[0])

        self.name = FlavoredName(raw_data[0])
        self.arguments = []

        for index, raw_argument in enumerate(raw_data[1]):
            self.arguments.append(self.get_generator().get_example_argument_class()(raw_argument, index, self, example))

    def get_type(self):
        return 'function'

    def get_name(self, *args, **kwargs):
        return self.name.get(*args, **kwargs)

    def get_arguments(self):
        return self.arguments

    def get_comment1(self):
        return self.raw_data[2]

    def get_formatted_comment1(self, template, empty, linebreak):
        comment1 = self.get_comment1()

        if comment1 == None:
            return empty

        return template.format(re.sub('[ ]+\n', '\n', comment1.replace('\n', linebreak)))

    def get_comment2(self):
        return self.raw_data[3]

    def get_formatted_comment2(self, template, empty):
        comment2 = self.get_comment2()

        if comment2 == None:
            return empty

        return template.format(comment2)

class ExampleCallbackFunction(ExampleItem):
    def __init__(self, raw_data, index, example):
        ExampleItem.__init__(self, raw_data, index, example)

        if len(raw_data) != 4:
            raise GeneratorError('Invalid ExampleCallbackFunction: ' + repr(raw_data))

        if len(raw_data[0]) != 2:
            raise GeneratorError('Invalid ExampleCallbackFunction: ' + repr(raw_data))

        check_name(raw_data[0][0])

        self.name = FlavoredName(raw_data[0][0])
        self.parameters = []

        for index, raw_parameter in enumerate(raw_data[1]):
            self.parameters.append(self.get_generator().get_example_parameter_class()(raw_parameter, index, self, example))

    def get_type(self):
        return 'callback'

    def get_name(self, *args, **kwargs):
        return self.name.get(*args, **kwargs)

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

        return template.format(re.sub('[ ]+\n', '\n', comment1.replace('\n', linebreak)))

    def get_extra_message(self):
        return self.raw_data[3]

    def get_formatted_extra_message(self, template):
        extra_message = self.get_extra_message()

        if extra_message == None:
            return ''

        return template.format(extra_message)

class ExampleCallbackPeriodFunction(ExampleItem):
    def __init__(self, raw_data, index, example):
        ExampleItem.__init__(self, raw_data, index, example)

        if len(raw_data) != 3:
            raise GeneratorError('Invalid ExampleCallbackPeriodFunction: ' + repr(raw_data))

        if len(raw_data[0]) != 2:
            raise GeneratorError('Invalid ExampleCallbackPeriodFunction: ' + repr(raw_data))

        check_name(raw_data[0][0])

        self.name = FlavoredName(raw_data[0][0])
        self.arguments = []

        for index, raw_argument in enumerate(raw_data[1]):
            self.arguments.append(self.get_generator().get_example_argument_class()(raw_argument, index, self, example))

    def get_type(self):
        return 'function'

    def get_name(self, *args, **kwargs):
        return self.name.get(*args, **kwargs)

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
                if not example.get_device().has_comcu() and other.get_name().space == function.get_name().space + ' Reached':
                    self.corresponding_callback = other
                    break
                elif example.get_device().has_comcu() and other.get_name().space == function.get_name().space:
                    self.corresponding_callback = other
                    break

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

        return template.format(maximum=maximum,
                               divisor=int(divisor),
                               result=maximum * int(divisor))

class ExampleCallbackThresholdFunction(ExampleItem):
    def __init__(self, raw_data, index, example):
        ExampleItem.__init__(self, raw_data, index, example)

        if len(raw_data) != 4:
            raise GeneratorError('Invalid ExampleCallbackThresholdFunction: ' + repr(raw_data))

        if len(raw_data[0]) != 2:
            raise GeneratorError('Invalid ExampleCallbackThresholdFunction: ' + repr(raw_data))

        check_name(raw_data[0][0])

        self.name = FlavoredName(raw_data[0][0])
        self.arguments = []

        for index, raw_argument in enumerate(raw_data[1]):
            self.arguments.append(self.get_generator().get_example_argument_class()(raw_argument, index, self, example))

        self.minimum_maximums = []

        for index, raw_minimum_maximum in enumerate(raw_data[3]):
            self.minimum_maximums.append(self.get_generator().get_example_callback_threshold_minimum_maximum_class()(raw_minimum_maximum, index, self, example))

    def get_type(self):
        return 'function'

    def get_name(self, *args, **kwargs):
        return self.name.get(*args, **kwargs)

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
            unit_name = minimum_maximum.get_corresponding_parameter().get_formatted_unit_name(' {0}')

            minimums.append(str(minimum_maximum.get_minimum()))
            minimums_with_unit.append(str(minimum_maximum.get_minimum()) + unit_name)
            maximums_with_unit.append(str(minimum_maximum.get_maximum()) + unit_name)

        if option_char == '>':
            return 'greater than {0}'.format(', '.join(minimums_with_unit))

        if option_char == '<':
            return 'smaller than {0}'.format(', '.join(minimums_with_unit))

        if option_char == 'o':
            return 'outside of {0} to {1}'.format(', '.join(minimums),
                                                  ', '.join(maximums_with_unit))

        raise GeneratorError('Unhandled option: ' + option_char)

    def get_minimum_maximums(self):
        return self.minimum_maximums

class ExampleCallbackConfigurationFunction(ExampleItem):
    def __init__(self, raw_data, index, example):
        ExampleItem.__init__(self, raw_data, index, example)

        if len(raw_data) != 6:
            raise GeneratorError('Invalid ExampleCallbackConfigurationFunction: ' + repr(raw_data))

        if len(raw_data[0]) != 2:
            raise GeneratorError('Invalid ExampleCallbackConfigurationFunction: ' + repr(raw_data))

        check_name(raw_data[0][0])

        self.name = FlavoredName(raw_data[0][0])
        self.arguments = []

        for index, raw_argument in enumerate(raw_data[1]):
            self.arguments.append(self.get_generator().get_example_argument_class()(raw_argument, index, self, example))

        self.minimum_maximums = []

        for index, raw_minimum_maximum in enumerate(raw_data[5]):
            self.minimum_maximums.append(self.get_generator().get_example_callback_threshold_minimum_maximum_class()(raw_minimum_maximum, index, self, example))

    def get_type(self):
        return 'function'

    def get_name(self, *args, **kwargs):
        return self.name.get(*args, **kwargs)

    def get_comment_name(self):
        return self.raw_data[0][1]

    def get_arguments(self):
        return self.arguments

    def get_period(self): # msec
        return self.raw_data[2]

    def get_value_has_to_change(self, true, false, none):
        if self.raw_data[3] == None:
            return none

        if self.raw_data[3]:
            return true

        return false

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

    def get_option_char(self):
        return self.raw_data[4]

    def get_option_comment(self):
        option_char = self.get_option_char()
        minimums = []
        minimums_with_unit = []
        maximums_with_unit = []

        for minimum_maximum in self.get_minimum_maximums():
            unit_name = minimum_maximum.get_corresponding_parameter().get_formatted_unit_name(' {0}')

            minimums.append(str(minimum_maximum.get_minimum()))
            minimums_with_unit.append(str(minimum_maximum.get_minimum()) + unit_name)
            maximums_with_unit.append(str(minimum_maximum.get_maximum()) + unit_name)

        if option_char in [None, 'x']:
            return 'FIXME' # this should never be actually outputted into an example

        if option_char == '>':
            return 'greater than {0}'.format(', '.join(minimums_with_unit))

        if option_char == '<':
            return 'smaller than {0}'.format(', '.join(minimums_with_unit))

        if option_char == 'o':
            return 'outside of {0} to {1}'.format(', '.join(minimums),
                                                  ', '.join(maximums_with_unit))

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

        return template.format(re.sub('[ ]+\n', '\n', comment1.replace('\n', linebreak)))

    def get_sleep_comment2(self):
        return self.raw_data[3]

    def get_formatted_sleep_comment2(self, template, empty):
        comment2 = self.get_sleep_comment2()

        if comment2 == None:
            return empty

        return template.format(comment2)

    def get_loop_header_limit(self):
        return self.raw_data[1]

    def get_loop_header_comment(self):
        return self.raw_data[2]

    def get_formatted_loop_header_comment(self, template, empty, linebreak):
        comment = self.get_loop_header_comment()

        if comment == None:
            return empty

        return template.format(re.sub('[ ]+\n', '\n', comment.replace('\n', linebreak)))

class Generator:
    check_root_dir_name = True

    def __init__(self, root_dir, config_name, language):
        self.root_dir = root_dir
        self.config_name = FlavoredName(' '.join([word[0].upper() + word[1:] for word in config_name.split('_')]))
        self.language = language # en or de
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")

        if self.check_root_dir_name:
            root_dir_name = os.path.split(self.get_root_dir())[1]

            if self.get_bindings_name() != root_dir_name:
                raise GeneratorError("root directory '{0}' and bindings name '{1}' do not match".format(root_dir_name, self.get_bindings_name()))

        if self.get_config_name().space == 'Tinkerforge':
            self.bindings_dir_name = 'bindings'
            self.doc_dir_name = 'doc'
        else:
            self.bindings_dir_name = 'bindings_' + self.get_config_name().under
            self.doc_dir_name = 'doc_' + self.get_config_name().under

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

    def get_example_callback_configuration_function_class(self):
        return ExampleCallbackConfigurationFunction

    def get_example_special_function_class(self):
        return ExampleSpecialFunction

    def get_example_sort_key(self, example):
        return example[2], example[0] # lines, filename

    def get_root_dir(self):
        return self.root_dir

    def get_config_name(self, *args, **kwargs):
        return self.config_name.get(*args, **kwargs)

    def get_config_dir(self):
        parts = [self.root_dir, '..', 'configs']
        name = self.get_config_name().under

        if name != 'tinkerforge':
            parts.append(name)

        return os.path.join(*parts)

    def get_language(self):
        return self.language # en or de

    def get_bindings_dir(self):
        return os.path.join(self.get_root_dir(), self.bindings_dir_name)

    def get_doc_dir(self):
        return os.path.join(self.get_root_dir(), self.doc_dir_name)

    def get_changelog_version(self):
        if self.get_config_name().space == 'Tinkerforge':
            root_dir = self.get_root_dir()
        else:
            root_dir = self.get_config_dir()

        return get_changelog_version(root_dir)

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
  to the generators git on tinkerforge.com
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

        version = get_changelog_version(self.get_root_dir())
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
        recreate_dir(os.path.join(self.get_doc_dir(), self.get_language()))

    def finish(self):
        # Copy IPConnection examples
        example_regex = self.get_doc_example_regex()

        if example_regex != None:
            print(' * ip_connection')

            examples = find_examples(self.get_root_dir(), example_regex, sort_key=self.get_example_sort_key)
            copy_files = []

            for example in examples:
                include = 'IPConnection_{0}_{1}'.format(self.get_doc_rst_filename_part(), example[0].replace(' ', '_'))
                copy_files.append((example[1], include))

            copy_examples(copy_files, self.get_root_dir())

class BindingsGenerator(Generator):
    recreate_bindings_dir = True

    def __init__(self, *args, **kwargs):
        Generator.__init__(self, *args, **kwargs)

        self.released_files = []

    def prepare(self):
        if self.recreate_bindings_dir:
            recreate_dir(self.get_bindings_dir())

    def finish(self):
        with open(os.path.join(self.get_bindings_dir(), '__released_files__'), 'w') as f:
            for released_file in self.released_files:
                f.write(released_file + '\n')

class ZipGenerator(Generator):
    def get_tmp_dir(self):
        tmp_dir = os.path.join('/tmp/generators/', self.get_bindings_name())

        if self.get_config_name().space != 'Tinkerforge':
            tmp_dir += '_' + self.get_config_name().under

        return tmp_dir

    def get_released_files(self):
        released_files = []

        with open(os.path.join(self.get_bindings_dir(), '__released_files__'), 'r') as f:
             for line in f.readlines():
                 released_files.append(line.strip())

        return released_files

    def create_zip_file(self, source_path):
        if self.get_config_name().space == 'Tinkerforge':
            version = get_changelog_version(self.get_root_dir())
        else:
            version = get_changelog_version(self.get_config_dir())

        zipname = '{0}_{1}_bindings_{2}_{3}_{4}.zip'.format(self.get_config_name().under, self.get_bindings_name(), *version)

        with ChangedDirectory(source_path):
            execute(['zip', '-q', '-r', zipname, '.'])
            shutil.copy(zipname, self.get_root_dir())

class ExamplesGenerator(Generator):
    skip_existing_incomplete_example = False
    forbid_execution = True

    def __init__(self, *args, **kwargs):
        Generator.__init__(self, *args, **kwargs)

        if self.forbid_execution:
            raise GeneratorError('ExamplesGenerator execution is forbidden')

    def get_examples_dir(self, device, override_git_dir=None):
        if override_git_dir is None:
            git_dir = device.get_git_dir()
        else:
            git_dir = os.path.join(override_git_dir, device.get_git_name())
        return os.path.join(git_dir, 'software', 'examples', self.get_bindings_name())

def tester_worker(cookie, args, env):
    try:
        exit_code, output = check_output_and_error(args, env=env)
    except Exception as e:
        return cookie, None, 'Tester Exception: ' + str(e)

    return cookie, exit_code, output

class Tester(object):
    PROCESSES = 4

    def __init__(self, name, extension, root_dir, subdirs=None, comment=None, extra_paths=None):
        version = get_changelog_version(root_dir)

        self.name = name
        self.extension = extension
        self.root_dir = root_dir
        self.subdirs = subdirs if subdirs != None else ['examples']
        self.comment = comment
        self.extra_paths = extra_paths if extra_paths != None else []
        self.zipname = 'tinkerforge_{0}_bindings_{1}_{2}_{3}.zip'.format(name, *version)
        self.test_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.pool = multiprocessing.dummy.Pool(processes=self.PROCESSES)

    def execute(self, cookie, args, env=None):
        def callback(result):
            self.handle_result(*result)

        self.pool.apply_async(tester_worker, args=(cookie, args, env), callback=callback)

    def handle_source(self, path, extra):
        self.test_count += 1
        self.test((path,), path, extra)

    def handle_result(self, cookie, exit_code, output):
        if exit_code == None: # FIXME: add better handling
            if len(output) > 0:
                print(output)

            sys.exit(1)

        path = cookie[0]
        success = self.check_success(exit_code, output)

        if self.comment != None:
            print('>>> [{0}] testing {1}'.format(self.comment, path))
        else:
            print('>>> testing {0}'.format(path))

        output = output.strip()

        if len(output) > 0:
            print(output)

        if sys.stdout.isatty(): # only print color codes if stdout is not piped
            if success:
                self.success_count += 1
                print('\033[01;32m>>> test succeded\033[0m\n')
            else:
                self.failure_count += 1
                print('\033[01;31m>>> test failed\033[0m\n')
        else:
            if success:
                self.success_count += 1
                print('>>> test succeded\n')
            else:
                self.failure_count += 1
                print('>>> test failed\n')

    def after_unzip(self):
        return True

    def test(self, cookie, path, extra):
        raise NotImplementedError()

    def check_success(self, exit_code, output):
        return exit_code == 0

    def run(self):
        tmp_dir = os.path.join('/tmp/tester', self.name)

        # Make temporary directory
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

        os.makedirs(tmp_dir)

        with ChangedDirectory(tmp_dir):
            shutil.copy(os.path.join(self.root_dir, self.zipname), tmp_dir)

            # unzip
            print('>>> unpacking {0} to {1}'.format(self.zipname, tmp_dir))

            args = ['unzip',
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
                for root, _, files in os.walk(os.path.join(tmp_dir, subdir)):
                    for name in files:
                        if not name.endswith(self.extension):
                            continue

                        self.handle_source(os.path.join(root, name), False)

            for extra_path in self.extra_paths:
                self.handle_source(extra_path, True)

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

# use "with ChangedDirectory('/path/to/abc')" instead of "os.chdir('/path/to/abc')"
class ChangedDirectory(object):
    def __init__(self, path):
        self.path = path
        self.previous_path = None

    def __enter__(self):
        self.previous_path = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, type_, value, traceback):
        os.chdir(self.previous_path)
