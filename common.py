# -*- coding: utf-8 -*-

"""
Common Generator Library
Copyright (C) 2012-2017, 2019 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2012-2015, 2019 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>

common.py: Common library for generation of bindings and documentation

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
import functools
from collections import namedtuple
import importlib
import argparse
import shlex

from generators.configs import device_commonconfig

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

vf_str = {
    'en': """
Virtual Functions
^^^^^^^^^^^^^^^^^

Virtual functions don't communicate with the device itself, but operate only on
the API bindings device object. They can be called without the corresponding
IP Connection object being connected.

{0}
""",
    'de': """
Virtuelle Funktionen
^^^^^^^^^^^^^^^^^^^^

Virtuelle Funktionen kommunizieren nicht mit dem Gerät selbst, sie arbeiten nur
auf dem API Bindings Objekt. Dadurch können sie auch aufgerufen werden, ohne das
das dazugehörige IP Connection Objekt verbunden ist.

{0}
"""
}

if_str = {
    'en': """
Internal Functions
^^^^^^^^^^^^^^^^^^

Internal functions are used for maintenance tasks such as flashing a new firmware
of changing the UID of a Bricklet. These task should be performed using
Brick Viewer instead of using the internal functions directly.

{0}
""",
    'de': """
Interne Funktionen
^^^^^^^^^^^^^^^^^^

Interne Funktionen werden für Wartungsaufgaben, wie zum Beispiel das Flashen
einer neuen Firmware oder das Ändern der UID eines Bricklets, verwendet. Diese
Aufgaben sollten mit Brick Viewer durchgeführt werden, anstelle die internen
Funktionen direkt zu verwenden.

{0}
"""
}

lang = 'en'
enable_verbose = False

def print_verbose(*args, **kwargs):
    if enable_verbose:
        print(*args, **kwargs)

def html_escape(text):
    return text.replace("&", "&amp;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;").replace("<", "&lt;")

def shift_right(text, n):
    return text.replace('\n', '\n' + ' '*n)

def strip_trailing_whitespace(text):
    lines = []

    for line in text.split('\n'):
        lines.append(line.rstrip())

    return '\n'.join(lines)

_changelog_version_cache = {}

def get_changelog_version(root_dir):
    global _changelog_version_cache

    version = _changelog_version_cache.get(root_dir)

    if version != None:
        return version

    versions = []

    with open(os.path.join(root_dir, 'changelog.txt'), 'r') as f:
        for i, line in enumerate(f.readlines()):
            line = line.rstrip()

            if len(line) == 0:
                continue

            if re.match(r'^(?:- [A-Z0-9\(]|  ([A-Za-z0-9\(\"]|--hide-payload)).*$', line) != None:
                continue

            m = re.match(r'^(?:<unknown>|20[0-9]{2}-[0-9]{2}-[0-9]{2}): ([1-9][0-9]*)\.([0-9]+)\.([0-9]+) \((?:<unknown>|[a-f0-9]+)\)$', line)

            if m == None:
                raise GeneratorError('invalid line {0} in changelog {1}: {2}'.format(i + 1, root_dir, line))

            version = (int(m.group(1)), int(m.group(2)), int(m.group(3)))

            if version[0] not in [1, 2]:
                raise GeneratorError('invalid major version in changelog {0}: {1}'.format(root_dir, version))

            if len(versions) > 0:
                if versions[-1] >= version:
                    raise GeneratorError('invalid version order in changelog {0}: {1} -> {2}'.format(root_dir, versions[-1], version))

                if versions[-1][0] == version[0] and versions[-1][1] == version[1] and versions[-1][2] + 1 != version[2]:
                    raise GeneratorError('invalid version jump in changelog {0}: {1} -> {2}'.format(root_dir, versions[-1], version))

                if versions[-1][0] == version[0] and versions[-1][1] != version[1] and versions[-1][1] + 1 != version[1]:
                    raise GeneratorError('invalid version jump in changelog {0}: {1} -> {2}'.format(root_dir, versions[-1], version))

                if versions[-1][1] != version[1] and version[2] != 0:
                    if (root_dir == 'javascript' or root_dir.endswith('/javascript')) and versions[-1] == (2, 0, 18) and version == (2, 1, 19):
                        pass # ignore historical glitch
                    else:
                        raise GeneratorError('invalid version jump in changelog {0}: {1} -> {2}'.format(root_dir, versions[-1], version))

                if versions[-1][0] != version[0] and (version[1] != 0 or version[2] != 0):
                    raise GeneratorError('invalid version jump in changelog {0}: {1} -> {2}'.format(root_dir, versions[-1], version))

            versions.append(version)

    if len(versions) == 0:
        raise GeneratorError('no version found in changelog: ' + root_dir)

    version = (str(versions[-1][0]), str(versions[-1][1]), str(versions[-1][2]))
    _changelog_version_cache[root_dir] = version

    return version

def modify_items(kind, active_items, all_items, action, item):
    if item == 'all':
        if action == '+':
            active_items |= set(all_items)
        elif action == '-':
            active_items -= set(all_items)
        else:
            raise Exception('invalid --{0}s item: {1}'.format(kind, action + item))
    else:
        if item not in all_items:
            raise Exception('unknown {0}: {1}'.format(kind, item))

        if action == '+':
            active_items.add(item)
        elif action == '-':
            active_items.remove(item)
        elif action == '>=':
            active_items |= set(all_items[all_items.index(item):])
        elif action == '>':
            active_items |= set(all_items[all_items.index(item) + 1:])
        elif action == '<=':
            active_items |= set(all_items[:all_items.index(item) + 1])
        elif action == '<':
            active_items |= set(all_items[:all_items.index(item)])
        else:
            assert False, action

    return active_items

def apply_item_changes(kind, active_items, all_items, item_changes):
    for item_change in item_changes:
        if len(item_change) == 0:
            raise Exception('empty --{0}s item'.format(kind))

        m = re.match(r'^(\+|-|>=|>|<=|<)(.*)$', item_change)

        if m == None:
            raise Exception('invalid --{0}s item: {1}'.format(kind, item_change))

        action = m.group(1)
        item = m.group(2)
        active_items = modify_items(kind, active_items, all_items, action, item)

    return active_items

def get_image_size(path):
    from PIL import Image

    return Image.open(path).size

def select_lang(d, language=None):
    if language == None:
        language = lang

    return d[language]

def make_rst_header(device, has_device_identifier_constant=True):
    bindings_display_name = device.get_generator().get_bindings_display_name()
    ref_name = device.get_generator().get_bindings_name()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    full_title = '{0} - {1}'.format(bindings_display_name, device.get_long_display_name())
    full_title_underline = '='*len(full_title)

    brick_name = {
        'en': 'this Brick',
        'de': 'dieses Bricks'
    }

    bricklet_name = {
        'en': 'this Bricklet',
        'de': 'dieses Bricklets'
    }

    tng_name = {
        'en': 'this TNG module',
        'de': 'dieses TNG-Moduls'
    }

    if device.is_brick():
        device_name = select_lang(brick_name)
    elif device.is_bricklet():
        device_name = select_lang(bricklet_name)
    elif device.is_tng():
        device_name = select_lang(tng_name)
    else:
        assert False

    device_identifier_constant = {'en': '.. |device_identifier_constant| replace:: There is also a :ref:`constant <{0}_{1}_constants>` for the device identifier of {2}.\n',
                                  'de': '.. |device_identifier_constant| replace:: Es gibt auch eine :ref:`Konstante <{0}_{1}_constants>` für den Device Identifier {2}.\n'}

    if device.is_released():
        orphan = ''
    else:
        orphan = ':orphan:\n'

    if has_device_identifier_constant:
        device_identifier_constant = select_lang(device_identifier_constant).format(device.get_doc_rst_ref_name(),
                                                                                    ref_name,
                                                                                    device_name)
    else:
        device_identifier_constant = '.. |device_identifier_constant| unicode:: 0xA0\n   :trim:\n'

    ref = '.. _{0}_{1}:\n'.format(device.get_doc_rst_ref_name(), ref_name)

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

    tng = {
        'en': 'This TNG module',
        'de': 'Dieses TNG-Modul'
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
        'en': 'the :ref:`{0} <{1}>`',
        'de': 'den :ref:`{0} <{1}>`',
    }

    bricklet_name = {
        'en': 'the :ref:`{0} <{1}>`',
        'de': 'das :ref:`{0} <{1}>`',
    }

    tng_name = {
        'en': 'the :ref:`{0} <{1}>`',
        'de': 'das :ref:`{0} <{1}>`',
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
    elif device.is_bricklet():
        device_name = select_lang(bricklet_name)
    elif device.is_tng():
        device_name = select_lang(tng_name)
    else:
        assert False

    device_name = device_name.format(device.get_long_display_name(),
                                     device.get_doc_rst_ref_name())

    s = select_lang(summary).format(bindings_name_link,
                                    device_name,
                                    device.get_long_display_name(),
                                    device.get_doc_rst_ref_name())

    if is_programming_language:
        s += select_lang(summary_install).format(device.get_generator().get_bindings_name(),
                                                 device.get_generator().get_bindings_display_name())

    if not device.is_released():
        if device.is_brick():
            d = brick
        elif device.is_bricklet():
            d = bricklet
        elif device.is_tng():
            d = tng
        else:
            assert False

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

    ref = '.. _{0}_{1}_examples:\n'.format(device.get_doc_rst_ref_name(),
                                           bindings_name)

    files = find_device_examples(device, filename_regex)
    if len(files) == 0:
        print_verbose('    \033[01;31m! no examples\033[0m')
        return ''

    examples = select_lang(ex).format(ref)
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

        include = '{0}_{1}_{2}'.format(device.get_doc_rst_name(), include_name, f[0].replace(' ', '_'))
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

def format_simple_element_meta(simple_elements, no_out_value=None,
                               parameter_label_override=None,
                               return_label_override=None):
    type_label = select_lang({'en': 'Type', 'de': 'Typ'})

    if parameter_label_override != None:
        parameter_label = select_lang(parameter_label_override)
    else:
        parameter_label = select_lang({'en': 'Parameters', 'de': 'Parameter'})

    if return_label_override != None:
        return_label = select_lang(return_label_override)
    else:
        return_label = select_lang({'en': 'Returns', 'de': 'Rückgabe'})

    formatted_meta_in = []
    formatted_meta_out = []

    for simple_element in simple_elements:
        assert simple_element[2] in [None, 1] # FIXME: no list support yet

        meta = ('plain', simple_element[0], '{0}: {1}'.format(type_label, simple_element[1]))

        if simple_element[3] == 'in':
            formatted_meta_in.append(meta)
        elif simple_element[3] == 'out':
            formatted_meta_out.append(meta)
        else:
            assert False, simple_element[3]

    if len(formatted_meta_out) == 0 and no_out_value != None:
        formatted_meta_out.append(select_lang(no_out_value))

    formatted_meta = []

    if len(formatted_meta_in) > 0:
        formatted_meta.append(('plain', parameter_label, formatted_meta_in))

    if len(formatted_meta_out) > 0:
        formatted_meta.append(('plain', return_label, formatted_meta_out))

    return formatted_meta

def format_full_element_meta(packet_type,
                             selected_elements,
                             all_elements,
                             type_func,
                             name_func,
                             output_parameter='never',
                             return_object='never',
                             callback_object='never',
                             prefix_elements=None,
                             suffix_elements=None,
                             stream_length_suffix=None,
                             parameter_label_override=None,
                             output_parameter_label_override=None,
                             return_label_override=None,
                             return_object_label_override=None,
                             return_object_is_array=False,
                             callback_parameter_label_override=None,
                             callback_object_label_override=None,
                             constants_hint_override=None,
                             no_in_value=None,
                             no_out_value=None,
                             no_return_value=None,
                             explicit_string_cardinality=False,
                             explicit_variable_stream_cardinality=False,
                             explicit_fixed_stream_cardinality=False,
                             explicit_common_cardinality=False,
                             function_id=None):
    assert output_parameter in ['never', 'always', 'conditional']
    assert return_object in ['never', 'always', 'conditional']
    assert callback_object in ['never', 'always', 'conditional']

    type_label = select_lang({'en': 'Type', 'de': 'Typ'})
    length_label = select_lang({'en': 'Length', 'de': 'Länge'})
    up_to_hint = select_lang({'en': 'up to', 'de': 'bis zu'})
    variable_hint = select_lang({'en': 'variable', 'de': 'variabel'})
    unit_label = select_lang({'en': 'Unit', 'de': 'Einheit'})
    to_hint = select_lang({'en': 'to', 'de': 'bis'})
    range_label = select_lang({'en': 'Range', 'de': 'Wertebereich'})
    default_label = select_lang({'en': 'Default', 'de': 'Standardwert'})
    formatted_meta_in = []
    formatted_meta_out = []
    formatted_meta_return = []

    if prefix_elements != None:
        for prefix_element in prefix_elements:
            assert prefix_element[2] == 1 # FIXME: no list support yet

            meta = ('plain', prefix_element[0], '{0}: {1}'.format(type_label, prefix_element[1]))

            if prefix_element[3] == 'in':
                formatted_meta_in.append(meta)
            elif prefix_element[3] == 'out':
                formatted_meta_out.append(meta)
            elif prefix_element[3] == 'return':
                formatted_meta_return.append(meta)
            else:
                assert False, prefix_element[3]

    for element in selected_elements:
        meta = ['{0}: {1}'.format(type_label, type_func(element))]
        cardinality = element.get_cardinality()

        if cardinality != 1:
            if element.get_type() == 'string':
                if explicit_string_cardinality:
                    meta.append('{0}: {1} {2}'.format(length_label, up_to_hint, cardinality))
            elif cardinality < 0:
                if explicit_variable_stream_cardinality:
                    meta.append('{0}: {1}'.format(length_label, variable_hint))
            elif element.get_role() == 'stream_data':
                if explicit_fixed_stream_cardinality:
                    meta.append('{0}: {1}'.format(length_label, cardinality))
            elif explicit_common_cardinality:
                meta.append('{0}: {1}'.format(length_label, cardinality))

        if element.is_struct():
            assert cardinality > 1

            if element.get_direction() == 'in':
                formatted_meta_in.append(('plain', name_func(element), ', '.join(meta)))
            else:
                formatted_meta_out.append(('plain', name_func(element), ', '.join(meta)))

        for index in element.get_indices():
            if index != None:
                meta = ['{0}: {1}'.format(type_label, type_func(element, cardinality=1))]

            type_ = element.get_type()
            scale = element.get_scale(index=index)
            unit = element.get_unit(index=index)

            if scale != (1, 1) and unit == None:
                if scale == 'dynamic':
                    formatted_scale = '?'
                else:
                    formatted_scale = format_fraction(*scale)

                meta.append('{0}: {1}'.format(unit_label, formatted_scale))
            elif scale == (1, 1) and unit != None:
                if unit == 'dynamic':
                    formatted_unit = '?'
                    sequence = '{value} {unit}'
                else:
                    formatted_unit = '⟨abbr title=«{0} ({1})»⟩{2}⟨/abbr⟩'.format(unit.get_title(), unit.get_usage(), unit.get_symbol())
                    sequence = unit.get_sequence()

                meta.append('{0}: {1}'.format(unit_label, sequence.format(value='1', unit=formatted_unit)))
            elif scale != (1, 1) and unit != None:
                if scale == 'dynamic':
                    formatted_scale = '?'

                    if unit == 'dynamic':
                        formatted_unit = '?'
                        sequence = '{value} {unit}'
                    else:
                        formatted_unit = '⟨abbr title=«{0} ({1})»⟩{2}⟨/abbr⟩'.format(unit.get_title(), unit.get_usage(), unit.get_symbol())
                        sequence = unit.get_sequence()
                else:
                    if unit == 'dynamic':
                        formatted_scale = format_fraction(*scale)
                        formatted_unit = '?'
                        sequence = '{value} {unit}'
                    else:
                        normalized_scale, unit_title, unit_symbol = normalize_scale(scale, unit)
                        formatted_scale = format_fraction(*normalized_scale)
                        formatted_unit = '⟨abbr title=«{0} ({1})»⟩{2}⟨/abbr⟩'.format(unit_title, unit.get_usage(), unit_symbol)
                        sequence = unit.get_sequence()

                meta.append('{0}: {1}'.format(unit_label, sequence.format(value=formatted_scale, unit=formatted_unit)))

            if type_ not in ['bool', 'string']:
                if constants_hint_override != None:
                    constants_hint = select_lang(constants_hint_override)
                else:
                    constants_hint = select_lang({'en': ('See constants', 'with constants'), 'de': ('Siehe Konstanten', 'mit Konstanten')})

                range_ = element.get_range(index=index)

                if range_ == 'constants':
                    meta.append('{0}: {1}'.format(range_label, constants_hint[0]))
                elif range_ == 'dynamic':
                    meta.append('{0}: ⟨abbr title=«{1}»⟩?⟨/abbr⟩'.format(range_label, select_lang({'en': 'Dynamic, see documentation', 'de': 'Dynamisch, siehe Dokumentation'})))
                elif range_ != None:
                    if range_ == 'type':
                        range_ = [element.get_type_range()]

                    formatted_range = []

                    for subrange in range_:
                        assert isinstance(subrange, tuple), range_

                        formatted_subrange = [None, None]

                        if type_.startswith('int') or type_.startswith('uint'):
                            for i, value in enumerate(subrange):
                                formatted_subrange[i] = format_value_with_tooltip(element, value, scale, unit)
                        else:
                            for i, value in enumerate(subrange):
                                formatted_subrange[i] = element.format_value(value)

                        if subrange[0] == subrange[1]:
                            formatted_range.append(formatted_subrange[0])
                        else:
                            formatted_range.append('{0} {1} {2}'.format(formatted_subrange[0], to_hint, formatted_subrange[1]))

                    if element.get_constant_group(index=index) != None:
                        meta.append('{0}: [{1}] {2}'.format(range_label, ', '.join(formatted_range), constants_hint[1]))
                    else:
                        meta.append('{0}: [{1}]'.format(range_label, ', '.join(formatted_range)))

            default = element.get_default(index=index)

            if default != None:
                if type_.startswith('int') or type_.startswith('uint'):
                    formatted_default = format_value_with_tooltip(element, default, scale, unit)
                else:
                    formatted_default = element.format_value(default)

                meta.append('{0}: {1}'.format(default_label, formatted_default))

            if index == None:
                style = 'plain'
            else:
                style = 'index'

            name = name_func(element, index=index)

            if element.get_direction() == 'in':
                formatted_meta_in.append((style, name, ', '.join(meta)))
            else:
                formatted_meta_out.append((style, name, ', '.join(meta)))

        if stream_length_suffix != None:
            length_elements = []
            chunk_offset_elements = []

            for other in all_elements:
                if other.get_role() == 'stream_length':
                    length_elements.append(other)
                elif other.get_role() == 'stream_chunk_offset':
                    chunk_offset_elements.append(other)

            if element.get_role() == 'stream_data' and (element.get_direction() == 'out' or len(length_elements) > 0):
                if len(length_elements) > 0:
                    length_type = type_func(length_elements[0])
                elif len(chunk_offset_elements) > 0:
                    length_type = type_func(chunk_offset_elements[0])
                else:
                    raise GeneratorError('Malformed stream config')

                meta = ('plain', name_func(element) + stream_length_suffix, ', '.join(['{0}:  {1}'.format(type_label, length_type)]))

                if element.get_direction() == 'in':
                    formatted_meta_in.append(meta)
                else:
                    formatted_meta_out.append(meta)

    if suffix_elements != None:
        for suffix_element in suffix_elements:
            assert suffix_element[2] == 1 # FIXME: no list support yet

            meta = ('plain', suffix_element[0], '{0}: {1}'.format(type_label, suffix_element[1]))

            if suffix_element[3] == 'in':
                formatted_meta_in.append(meta)
            elif suffix_element[3] == 'out':
                formatted_meta_out.append(meta)
            elif suffix_element[3] == 'return':
                formatted_meta_return.append(meta)
            else:
                assert False, suffix_element[3]

    if len(formatted_meta_in) == 0 and no_in_value != None:
        formatted_meta_in.append(select_lang(no_in_value))

    if len(formatted_meta_out) == 0 and no_out_value != None:
        formatted_meta_out.append(select_lang(no_out_value))

    function_id_label = select_lang({'en': 'Function ID', 'de': 'Funktions-ID'})

    if parameter_label_override != None:
        parameter_label = select_lang(parameter_label_override)
    else:
        parameter_label = select_lang({'en': 'Parameters', 'de': 'Parameter'})

    if output_parameter_label_override != None:
        output_parameter_label = select_lang(output_parameter_label_override)
    else:
        output_parameter_label = select_lang({'en': 'Output Parameters', 'de': 'Ausgabeparameter'})

    if return_label_override != None:
        return_label = select_lang(return_label_override)
    else:
        return_label = select_lang({'en': 'Returns', 'de': 'Rückgabe'})

    if return_object_label_override != None:
        return_object_label = select_lang(return_object_label_override)
    else:
        return_object_label = select_lang({'en': 'Return Object', 'de': 'Rückgabeobjekt'})

    if callback_parameter_label_override != None:
        callback_parameter_label = select_lang(callback_parameter_label_override)
    else:
        callback_parameter_label = select_lang({'en': 'Callback Parameters', 'de': 'Callback-Parameter'})

    if callback_object_label_override != None:
        callback_object_label = select_lang(callback_object_label_override)
    else:
        callback_object_label = select_lang({'en': 'Callback Object', 'de': 'Callback-Objekt'})

    formatted_meta = []

    if function_id != None:
        formatted_meta.append(('plain', function_id_label, str(function_id)))

    if len(formatted_meta_in) > 0:
        formatted_meta.append(('plain', parameter_label, formatted_meta_in))

    has_return = False

    if len(formatted_meta_out) > 0:
        if packet_type == 'function':
            if output_parameter == 'never':
                if return_object == 'never':
                    formatted_meta.append(('plain', return_label, formatted_meta_out))
                    has_return = True
                elif return_object == 'always':
                    formatted_meta.append(('index' if return_object_is_array else 'plain', return_object_label, formatted_meta_out))
                elif return_object == 'conditional':
                    if len(formatted_meta_out) == 1:
                        formatted_meta.append(('plain', return_label, formatted_meta_out))
                        has_return = True
                    else:
                        formatted_meta.append(('index' if return_object_is_array else 'plain', return_object_label, formatted_meta_out))
                else:
                    assert False, return_object
            elif output_parameter == 'always':
                formatted_meta.append(('plain', output_parameter_label, formatted_meta_out))
            elif output_parameter == 'conditional':
                if len(formatted_meta_out) == 1:
                    formatted_meta.append(('plain', return_label, formatted_meta_out))
                    has_return = True
                else:
                    formatted_meta.append(('plain', output_parameter_label, formatted_meta_out))
            else:
                assert False, output_parameter
        elif packet_type == 'callback':
            if callback_object == 'never':
                formatted_meta.append(('plain', callback_parameter_label, formatted_meta_out))
            elif callback_object == 'always':
                formatted_meta.append(('plain', callback_object_label, formatted_meta_out))
            elif callback_object == 'conditional':
                if len(formatted_meta_out) == 1:
                    formatted_meta.append(('plain', callback_parameter_label, formatted_meta_out))
                else:
                    formatted_meta.append(('plain', callback_object_label, formatted_meta_out))
            else:
                assert False, output_parameter
        else:
            assert False, packet_type

    if len(formatted_meta_return) > 0:
        formatted_meta.append(('plain', return_label, formatted_meta_return))
        has_return = True

    if not has_return and no_return_value != None:
        formatted_meta.append(('plain', return_label, select_lang(no_return_value)))

    return formatted_meta

def merge_meta_sections(items):
    merged_items = []

    for style, label, values in items:
        merged = False

        for merged_style, merged_label, merged_values in merged_items:
            if merged_style == style and merged_label == label:
                merged_values += values
                merged = True
                break

        if merged:
            continue

        merged_items.append((style, label, values[:]))

    return merged_items

def make_rst_meta_table(items, indent_level=1, index_format_func=str):
    table_template = '''.. raw:: html

 <table class="docutils field-list" frame="void" rules="none">
 <col class="field-name" /><col class="field-body" />
 <tbody valign="top">
 {rows}
 </tbody>
 </table>
'''
    row_template = '<tr class="field"><th class="field-name">{label}:</th><td class="field-body"><ul class="simple">{values}</ul></td></tr>'
    named_value_template = '<li>{index}<strong>{name}</strong> &#8211; {value}</li>'
    value_template = '<li>{index}{value}</li>'
    formatted_rows = []

    for style, label, values in items:
        if not isinstance(values, list):
            values = [values]

        formatted_values = []
        outer_i = 0
        inner_i = 0

        for value in values:
            if style == 'index':
                index = '{0}: '.format(index_format_func(outer_i))
            else:
                index = ''

            if isinstance(value, tuple):
                if value[0] == 'index':
                    assert outer_i > 0, outer_i

                    if inner_i == 0:
                        formatted_values.append('<ul class="simple-inner">')

                    index = '{0}: '.format(index_format_func(inner_i))
                    inner_i += 1
                else:
                    if inner_i != 0:
                        formatted_values.append('</ul>')

                    inner_i = 0

                formatted_values.append(named_value_template.format(index=index, name=html_escape(value[1]), value=html_escape(value[2])))
            else:
                formatted_values.append(value_template.format(index=index, value=html_escape(value)))

            if not isinstance(value, tuple) or value[0] != 'index':
                outer_i += 1

        formatted_rows.append(row_template.format(label=label, values='\n  '.join(formatted_values)))

    if len(formatted_rows) == 0:
        return ''

    return (' ' * indent_level + ('\n' + ' ' * indent_level).join(table_template.format(rows='\n  '.join(formatted_rows)).split('\n'))).replace('⟨', '<').replace('⟩', '>').replace('«', '"').replace('»', '"')

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

    print_verbose('    * examples')

    for copy_file in copy_files:
        doc_dest = os.path.join(doc_path, copy_file[1])
        doc_src = copy_file[0]
        shutil.copy(doc_src, doc_dest)
        print_verbose('      - {0}'.format(copy_file[1]))

    if len(copy_files) == 0:
        print_verbose('      \033[01;31m! no examples\033[0m')

re_camel_to_space = re.compile('([A-Z][A-Z][a-z])|([a-z][A-Z])|([a-zA-Z][0-9])')

def camel_to_space(name):
    return re_camel_to_space.sub(lambda m: m.group()[:1] + " " + m.group()[1:], name)

def format_float(value):
    assert isinstance(value, float), value

    string = '{0:.20f}'.format(value).rstrip('0')

    if string.endswith('.'):
        string += '0'

    return string

def format_value_hint(value, scale, unit):
    if scale == (1, 1) and unit == None:
        return ''

    if sys.hexversion < 0x03000000:
        assert isinstance(value, (int, long)), value
    else:
        assert isinstance(value, int), value

    if scale not in [(1, 1), 'dynamic']:
        assert isinstance(scale, tuple), scale
        assert isinstance(scale[0], int), scale
        assert isinstance(scale[1], int), scale

    assert unit == None or unit == 'dynamic' or isinstance(unit, Unit), unit

    if value == 0:
        scaled_value = 0
        modified_scale = scale

        if unit not in [None, 'dynamic']:
            unit_symbol = unit.get_symbol()
    elif unit in [None, 'dynamic']:
        if scale == 'dynamic':
            scaled_value = value
            modified_scale = 'dynamic'
        else:
            scaled_value = float(value) * scale[0] / scale[1]
            modified_scale = scale
    elif scale == 'dynamic':
        scaled_value = value
        modified_scale = 'dynamic'

        if unit not in [None, 'dynamic']:
            unit_symbol = unit.get_symbol()
    else:
        # find the scale that results in a scaled value with the minimum number of leading digits
        candidate = {unit.get_symbol(): (float(value) * scale[0] / scale[1], scale)}
        unit_allowed_prefixes = unit.get_allowed_prefixes()
        unit_allowed_inverse_prefixes = unit.get_allowed_inverse_prefixes()
        unit_numerator_exponent = unit.get_numerator_exponent()
        unit_denominator_exponent = unit.get_denominator_exponent()

        if unit.get_prefix() == None:
            for unit_prefix in unit_prefixes:
                if unit_prefix.symbol not in unit_allowed_prefixes:
                    continue

                divided_scale = list(scale)
                divided_scale[1 - unit_prefix.index] *= unit_prefix.divisor ** unit_numerator_exponent
                prefixed_symbol = unit.get_symbol(prefix=unit_prefix)

                assert prefixed_symbol not in candidate

                candidate[prefixed_symbol] = (float(value) * divided_scale[0] / divided_scale[1], divided_scale)

                if unit.get_inverse_prefix() == None:
                    for unit_inverse_prefix in unit_prefixes:
                        if unit_inverse_prefix.symbol not in unit_allowed_inverse_prefixes:
                            continue

                        divided_scale = list(divided_scale)
                        divided_scale[unit_inverse_prefix.index] *= unit_inverse_prefix.divisor ** unit_denominator_exponent
                        prefixed_symbol = unit.get_symbol(prefix=unit_prefix, inverse_prefix=unit_inverse_prefix)

                        assert prefixed_symbol not in candidate

                        candidate[prefixed_symbol] = (float(value) * divided_scale[0] / divided_scale[1], divided_scale)

        if unit.get_inverse_prefix() == None:
            for unit_inverse_prefix in unit_prefixes:
                if unit_inverse_prefix.symbol not in unit_allowed_inverse_prefixes:
                    continue

                divided_scale = list(scale)
                divided_scale[unit_inverse_prefix.index] *= unit_inverse_prefix.divisor ** unit_denominator_exponent
                prefixed_symbol = unit.get_symbol(inverse_prefix=unit_inverse_prefix)

                assert prefixed_symbol not in candidate

                candidate[prefixed_symbol] = (float(value) * divided_scale[0] / divided_scale[1], divided_scale)

        scaled_value = None
        modified_scale = None
        unit_symbol = None

        for unit_symbol_candidate in candidate:
            scaled_value_candidate, modified_scale_candidate = candidate[unit_symbol_candidate]

            if abs(scaled_value_candidate) >= 1 and (scaled_value == None or abs(scaled_value_candidate) < abs(scaled_value)):
                scaled_value = scaled_value_candidate
                modified_scale = modified_scale_candidate
                unit_symbol = unit_symbol_candidate

        if scaled_value == None: # no abs(scaled_value) >= 1 exists
            for unit_symbol_candidate in candidate:
                scaled_value_candidate, modified_scale_candidate = candidate[unit_symbol_candidate]

                if scaled_value == None or abs(scaled_value_candidate) > abs(scaled_value):
                    scaled_value = scaled_value_candidate
                    modified_scale = modified_scale_candidate
                    unit_symbol = unit_symbol_candidate

    if modified_scale == 'dynamic':
        if unit in [None, 'dynamic']:
            formatted_value = '?'
        else:
            formatted_value = unit.get_sequence().format(value='?', unit=unit_symbol)
    else:
        digits = int(math.ceil(math.log10(modified_scale[1]) - math.log10(modified_scale[0])))

        if digits >= 1:
            formatted_value = '{{0:.{0}f}}'.format(digits).format(round(scaled_value, digits))
        else:
            formatted_value = str(int(scaled_value))

        if lang == 'de':
            formatted_value = formatted_value.replace('.', ',')

        if unit == 'dynamic':
            formatted_value = '{value} {unit}'.format(value=formatted_value, unit='?')
        elif unit != None:
            formatted_value = unit.get_sequence().format(value=formatted_value, unit=unit_symbol)

    return formatted_value

_exponent_tooltip_format_1_cache = None
_exponent_tooltip_format_2_cache = None

def format_value_with_tooltip(element, value, scale, unit):
    global _exponent_tooltip_format_1_cache
    global _exponent_tooltip_format_2_cache

    formatted_value = element.format_value(value)
    formatted_value_hint = format_value_hint(value, scale, unit)
    result = None

    if isinstance(value, int):
        if _exponent_tooltip_format_1_cache == None:
            _exponent_tooltip_format_1_cache = {}

            for exponent in [16, 32, 64]:
                _exponent_tooltip_format_1_cache[-2 ** (exponent - 1)] = ('⟨abbr title=«{0}{1} (Int{2} Min)»⟩-2⟨sup⟩{3}⟨/sup⟩⟨/abbr⟩', exponent)
                _exponent_tooltip_format_1_cache[2 ** (exponent - 1) - 1] = ('⟨abbr title=«{0}{1} (Int{2} Max)»⟩2⟨sup⟩{3}⟨/sup⟩ - 1⟨/abbr⟩', exponent)
                _exponent_tooltip_format_1_cache[2 ** exponent - 1] = ('⟨abbr title=«{0}{1} (UInt{2} Max)»⟩2⟨sup⟩{2}⟨/sup⟩ - 1⟨/abbr⟩', exponent)

        format_, exponent = _exponent_tooltip_format_1_cache.get(value, (None, None))

        if format_ != None:
            result = format_.format(wrap_non_empty('', formatted_value_hint, ' | '), formatted_value, exponent, exponent - 1)
        else:
            if _exponent_tooltip_format_2_cache == None:
                _exponent_tooltip_format_2_cache = {}

                for exponent in range(9, 65):
                    _exponent_tooltip_format_2_cache[-2 ** exponent] = ('⟨abbr title=«{0}{1}»⟩-2⟨sup⟩{2}⟨/sup⟩⟨/abbr⟩', exponent)
                    _exponent_tooltip_format_2_cache[2 ** exponent] = ('⟨abbr title=«{0}{1}»⟩2⟨sup⟩{2}⟨/sup⟩⟨/abbr⟩', exponent)
                    _exponent_tooltip_format_2_cache[-2 ** exponent + 1] = ('⟨abbr title=«{0}{1}»⟩-2⟨sup⟩{2}⟨/sup⟩ + 1⟨/abbr⟩', exponent)
                    _exponent_tooltip_format_2_cache[2 ** exponent - 1] = ('⟨abbr title=«{0}{1}»⟩2⟨sup⟩{2}⟨/sup⟩ - 1⟨/abbr⟩', exponent)

            format_, exponent = _exponent_tooltip_format_2_cache.get(value, (None, None))

            if format_ != None:
                result = format_.format(wrap_non_empty('', formatted_value_hint, ' | '), formatted_value, exponent, exponent - 1)

    if result == None:
        if len(formatted_value_hint) > 0:
            result = '⟨abbr title=«{0}»⟩{1}⟨/abbr⟩'.format(formatted_value_hint, formatted_value)
        else:
            result = formatted_value

    return result

def normalize_scale(scale, unit):
    scale = list(scale)
    prefix_override = None
    inverse_prefix_override = None

    if unit.get_prefix() == None:
        unit_allowed_prefixes = unit.get_allowed_prefixes()

        for unit_prefix in unit_prefixes:
            if unit_prefix.symbol not in unit_allowed_prefixes:
                continue

            divisor = unit_prefix.divisor ** unit.get_numerator_exponent()

            if scale[unit_prefix.index] % divisor == 0:
                scale[unit_prefix.index] //= divisor
                prefix_override = unit_prefix
                break

    if unit.get_inverse_prefix() == None:
        unit_allowed_inverse_prefixes = unit.get_allowed_inverse_prefixes()

        for unit_inverse_prefix in unit_prefixes:
            if unit_inverse_prefix.symbol not in unit_allowed_inverse_prefixes:
                continue

            divisor = unit_inverse_prefix.divisor ** unit.get_denominator_exponent()

            if scale[1 - unit_inverse_prefix.index] % divisor == 0:
                scale[1 - unit_inverse_prefix.index] //= divisor
                inverse_prefix_override = unit_inverse_prefix
                break

    unit_title = unit.get_title(prefix=prefix_override, inverse_prefix=inverse_prefix_override)
    unit_symbol = unit.get_symbol(prefix=prefix_override, inverse_prefix=inverse_prefix_override)

    return tuple(scale), unit_title, unit_symbol

def format_since_firmware(device, packet):
    since = packet.get_since_firmware()

    if since == None or since <= [2, 0, 0]:
        return ''

    if device.is_brick():
        suffix = 'Firmware'
    elif device.is_bricklet():
        suffix = 'Plugin'
    elif device.is_tng():
        suffix = 'Firmware'
    else:
        assert False

    return '\n.. versionadded:: {1}.{2}.{3}$nbsp;({0})\n'.format(suffix, *since)

def format_constant_default(prefix, constant_group, constant, value):
    if prefix.endswith('_'):
        # sphinx interprets trailing underscores as link markers, escape trailing underscores
        prefix = prefix[:-1] + '\\_'

    return '* {0}\\ **{1}**\\ _{2} = {3}\n'.format(prefix, constant_group.get_name().upper,
                                                   constant.get_name().upper, value)

def format_constants(prefix, packet, element_name_func,
                     constants_intro=None,
                     constants_name=None,
                     constant_format_func=format_constant_default):
    if constants_intro == None:
        constants_intro = {
            'en': """
The following **{0}** are available for this function:

""",
            'de': """
Die folgenden **{0}** sind für diese Funktion verfügbar:

"""
        }

    if constants_name == None:
        constants_name = {'en': 'constants', 'de': 'Konstanten'}

    constants = []

    for element in packet.get_elements():
        for index in element.get_indices():
            constant_group = element.get_constant_group(index=index)

            if constant_group == None:
                continue

            constants.append(select_lang({'en': '\nFor **{0}**:\n\n', 'de': '\nFür **{0}**:\n\n'}).format(element_name_func(element, index)))

            for constant in constant_group.get_constants():
                value = element.format_value(constant.get_value())

                constants.append(constant_format_func(prefix, constant_group, constant, value))

    if len(constants) == 0:
        return ''

    return select_lang(constants_intro).format(select_lang(constants_name)) + ''.join(constants)

def format_fraction(numerator, denominator):
    assert isinstance(numerator, int), numerator
    assert isinstance(denominator, int), denominator
    assert numerator >= 1, numerator
    assert denominator >= 1, denominator

    if numerator > 1 and denominator > 1:
        return '{0}/{1}'.format(numerator, denominator)

    if denominator > 1:
        return '1/{0}'.format(denominator)

    return str(numerator)

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

def flatten(list_of_lists):
    return sum(list_of_lists, [])

def recreate_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)

    os.makedirs(path)

def specialize_template(template_filename, destination_filename, replacements, check_completeness=True, remove_template=False):
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

    if remove_template:
        os.remove(template_filename)

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
    error = 'command failed: {0}'.format(' '.join(args) if isinstance(args, list) else args)

    try:
        if subprocess.call(args, **kwargs) != 0:
            sys.exit(1)
    except Exception as e:
        print(error + '\n' + str(e))
        sys.exit(1)

def generate(root_dir, language, internal, generator_class):
    print('=== language: {0}'.format(language))

    # default config
    subgenerate(root_dir, language, internal, generator_class, 'tinkerforge')

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

        subgenerate(root_dir, language, internal, generator_class, config_name)

def subgenerate(root_dir, language, internal, generator_class, config_name):
    global lang
    lang = language

    print('--> {0}'.format(config_name))

    config_path_parts = [root_dir, '..', 'configs']

    if config_name != 'tinkerforge':
        config_subdir = '.' + config_name
        config_path_parts.append(config_name)
    else:
        config_subdir = ''

    config_path = os.path.join(*config_path_parts)

    common_constant_groups = copy.deepcopy(device_commonconfig.common_constant_groups)
    common_packets = copy.deepcopy(device_commonconfig.common_packets)

    brick_infos = []
    bricklet_infos = []
    tng_infos = []
    device_identifiers = set()

    generator = generator_class(root_dir, language, internal, config_name)
    generator.prepare()

    def prepare_common_constant_groups(com, common_constant_groups):
        features = com['features']

        for common_constant_group in common_constant_groups:
            if common_constant_group['feature'] not in features:
                common_constant_group['to_be_removed'] = True

        return filter(lambda x: 'to_be_removed' not in x, common_constant_groups)

    def prepare_common_packets(com, common_packets):
        features = com['features']

        for common_packet in common_packets:
            if not common_packet.get('is_virtual', False):
                if com['name'] in common_packet['since_firmware']:
                    common_packet['since_firmware'] = common_packet['since_firmware'][com['name']]
                else:
                    common_packet['since_firmware'] = common_packet['since_firmware']['*']

                if common_packet['since_firmware'] == None:
                    common_packet['to_be_removed'] = True

            if common_packet['feature'] not in features:
                common_packet['to_be_removed'] = True

        return filter(lambda x: 'to_be_removed' not in x, common_packets)

    for config in sorted(os.listdir(config_path)):
        if not config.endswith('_config.py'):
            continue

        com = copy.deepcopy(importlib.import_module('generators.configs{0}.{1}'.format(config_subdir, config[:-3])).com)

        if com['documented'] and not com['released']:
            raise GeneratorError('{0} is marked as documented, but as not released'.format(config[:-10]))

        if not com['released'] and not com['documented']:
            print_verbose('  * {0} \033[01;36m(not released, not documented)\033[0m'.format(config[:-10]))
        elif not com['released']:
            print_verbose('  * {0} \033[01;36m(not released)\033[0m'.format(config[:-10]))
        elif not com['documented']:
            print_verbose('  * {0} \033[01;36m(not documented)\033[0m'.format(config[:-10]))
        else:
            print_verbose('  * {0}'.format(config[:-10]))

        if 'common_included' not in com:
            com['constant_groups'].extend(prepare_common_constant_groups(com, copy.deepcopy(common_constant_groups)))
            com['packets'].extend(prepare_common_packets(com, copy.deepcopy(common_packets)))
            com['common_included'] = True

        if generator.is_openhab_doc_generator:
            com['packets'] = [x for x in com['packets'] if 'openhab_doc' not in x or x['openhab_doc']]
        else:
            com['packets'] = [x for x in com['packets'] if 'openhab_doc' not in x or not x['openhab_doc']]

        device = generator.get_device_class()(com, generator)
        device_identifier = device.get_device_identifier()

        if device_identifier in device_identifiers:
            raise GeneratorError('Device identifier {0} is not unique'.format(device_identifier))

        device_identifiers.add(device_identifier)

        generator.generate(device)

        # only collect device_infos for default config
        if config_name != 'tinkerforge':
            continue

        if device.is_brick():
            ref_name = device.get_name().under + '_brick'
            hardware_doc_name = device.get_short_display_name().replace(' ', '_').replace('/', '_').replace('-', '').replace('2.0', 'V2').replace('3.0', 'V3') + '_Brick'
            software_doc_prefix = device.get_name().camel + '_Brick'

            if device.get_device_identifier() != 17:
                firmware_url_part = device.get_name().under
            else:
                firmware_url_part = None

            device_info = (device.get_device_identifier(),
                           'Brick',
                           device.get_long_display_name(),
                           device.get_short_display_name(),
                           ref_name,
                           hardware_doc_name,
                           software_doc_prefix,
                           device.get_git_name(),
                           firmware_url_part,
                           device.has_comcu(),
                           device.has_openhab(),
                           device.is_released(),
                           device.is_documented(),
                           device.is_discontinued(),
                           True,
                           device.get_esp32_firmware(),
                           device.get_description())

            brick_infos.append(device_info)
        elif device.is_bricklet():
            ref_name = device.get_name().under + '_bricklet'
            hardware_doc_name = device.get_short_display_name().replace(' ', '_').replace('/', '_').replace('-', '').replace('2.0', 'V2').replace('3.0', 'V3')
            software_doc_prefix = device.get_name().camel + '_Bricklet'
            firmware_url_part = device.get_name().under

            device_info = (device.get_device_identifier(),
                           'Bricklet',
                           device.get_long_display_name(),
                           device.get_short_display_name(),
                           ref_name,
                           hardware_doc_name,
                           software_doc_prefix,
                           device.get_git_name(),
                           firmware_url_part,
                           device.has_comcu(),
                           device.has_openhab(),
                           device.is_released(),
                           device.is_documented(),
                           device.is_discontinued(),
                           True,
                           device.get_esp32_firmware(),
                           device.get_description())

            bricklet_infos.append(device_info)
        elif device.is_tng():
            ref_name = 'tng_' + device.get_name().under
            hardware_doc_name = device.get_short_display_name().replace(' ', '_').replace('/', '_').replace('-', '').replace('2.0', 'V2').replace('3.0', 'V3')
            software_doc_prefix = 'TNG_' + device.get_name().camel
            firmware_url_part = device.get_name().under

            device_info = (device.get_device_identifier(),
                           'TNG',
                           device.get_long_display_name(),
                           device.get_short_display_name(),
                           ref_name,
                           hardware_doc_name,
                           software_doc_prefix,
                           device.get_git_name(),
                           firmware_url_part,
                           False,
                           device.has_openhab(),
                           device.is_released(),
                           device.is_documented(),
                           device.is_discontinued(),
                           True,
                           device.get_esp32_firmware(),
                           device.get_description())

            tng_infos.append(device_info)
        else:
            assert False

    generator.finish()

    # only update device_infos.py for default config
    if config_name == 'tinkerforge':
        brick_infos.append((None, 'Brick', 'Debug Brick', 'Debug', 'debug_brick', 'Debug_Brick', None, 'debug-brick', None, False, False, True, True, False, False, None,
                            {'en': 'For Firmware Developers: JTAG and serial console',
                             'de': 'Für Firmware Entwickler: JTAG und serielle Konsole'}))

        bricklet_infos.append((None, 'Bricklet', 'Breakout Bricklet', 'Breakout', 'breakout_bricklet', 'Breakout', None, 'breakout-bricklet', None, False, False, True, True, False, False, None,
                               {'en': 'Makes all Bricklet signals available',
                                'de': 'Macht alle Bricklet Signale zugänglich'}))

        with open(os.path.join(root_dir, '..', 'device_infos.py'), 'w') as f:
            f.write('# -*- coding: utf-8 -*-\n')
            f.write('from collections import namedtuple\n')
            f.write('\n')
            f.write("DeviceInfo = namedtuple('DeviceInfo', 'identifier category long_display_name short_display_name ref_name hardware_doc_name software_doc_prefix git_name firmware_url_part has_comcu has_openhab is_released is_documented is_discontinued has_bindings esp32_firmware description')\n")
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
check_name_exceptions_word_in_constant = ['20mA', '24mA', 'EtOH']

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

def gcd(a, b):
    while b != 0:
        a, b = b, a % b

    return a

class GeneratorError(Exception):
    pass

NameFlavors = namedtuple('NameFlavors', 'space lower camel headless under upper dash camel_abbrv lower_no_space camel_constant_safe')

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
                                          ''.join([word.capitalize() for word in words]),  # camel_abbrv; like camel, but produces GetSpiTfp... instead of GetSPITFP...
                                          ''.join(words).lower(),
                                          # camel_constant_safe; inserts '_' between digit-words to disambiguate between 1,1ms and 11ms
                                          functools.reduce(lambda l, r: l + '_' + r if (l[-1].isdigit() and r[0].isdigit()) else l + r, words))

            return self.cache[key]

class Unit(object):
    def __init__(self, name, title, symbol, usage, allowed_prefixes, allowed_inverse_prefixes,
                 sequence={'en': '{value} {unit}', 'de': '{value} {unit}'},
                 numerator_exponent=1, denominator_exponent=1, prefix=None, inverse_prefix=None):
        assert len(allowed_prefixes) == 0 or ('{prefix}' in name and '{prefix}' in title['en'] and '{prefix}' in title['en'] and '{prefix}' in symbol), (name, title, symbol)
        assert len(allowed_inverse_prefixes) == 0 or ('{inverse_prefix}' in name and '{inverse_prefix}' in title['en'] and '{inverse_prefix}' in title['en'] and '{inverse_prefix}' in symbol), (name, title, symbol)
        assert '{prefix}' not in name or len(allowed_prefixes) > 0, name
        assert '{inverse_prefix}' not in name or len(allowed_inverse_prefixes) > 0, name
        assert '{prefix}' not in title['en'] or len(allowed_prefixes) > 0, title['en']
        assert '{prefix}' not in title['de'] or len(allowed_prefixes) > 0, title['de']
        assert '{inverse_prefix}' not in title or len(allowed_inverse_prefixes) > 0, title
        assert '{prefix}' not in symbol or len(allowed_prefixes) > 0, symbol
        assert '{inverse_prefix}' not in symbol or len(allowed_inverse_prefixes) > 0, symbol
        assert '{value}' in sequence['en'] and '{value}' in sequence['de'], sequence
        assert '{unit}' in sequence['en'] and '{unit}' in sequence['de'], sequence
        assert isinstance(numerator_exponent, int) and numerator_exponent >= 1, numerator_exponent
        assert isinstance(denominator_exponent, int) and denominator_exponent >= 1, denominator_exponent

        check_name(name.format(prefix='', inverse_prefix=''))

        self._name = name
        self._name_cache = {}
        self._title = title
        self._symbol = symbol
        self._usage = usage
        self._allowed_prefixes = allowed_prefixes
        self._allowed_inverse_prefixes = allowed_inverse_prefixes
        self._sequence = sequence
        self._numerator_exponent = numerator_exponent
        self._denominator_exponent = denominator_exponent
        self._prefix = prefix
        self._inverse_prefix = inverse_prefix

    def _inject_prefix(self, text, prefix, inverse_prefix, language, space_case=False):
        if language == None:
            language = lang

        if prefix != None:
            prefix_name = select_lang(prefix.name, language=language)
        elif self._prefix != None:
            prefix_name = select_lang(self._prefix.name, language=language)
        else:
            prefix_name = ''

        if inverse_prefix != None:
            inverse_prefix_name = select_lang(inverse_prefix.name, language=language)
        elif self._inverse_prefix != None:
            inverse_prefix_name = select_lang(self._inverse_prefix.name, language=language)
        else:
            inverse_prefix_name = ''

        text = select_lang(text, language=language)

        for placeholder, replacement in [('{prefix}', prefix_name), ('{inverse_prefix}', inverse_prefix_name)]:
            if placeholder not in text:
                continue

            text_parts = text.split(placeholder)

            assert len(text_parts) == 2, text_parts
            assert len(text_parts[1]) > 0, text_parts
            assert text_parts[1][0] >= 'A' and text_parts[1][0] <= 'z', text_parts

            if len(text_parts[0]) > 0:
                assert (text_parts[0][-1] >= 'a' and text_parts[0][-1] <= 'z') or text_parts[0][-1] == ' ', text_parts

                if text_parts[0][-1] != ' ' or (not space_case and language == 'en'):
                    replacement = replacement.lower()

            if len(replacement) > 0:
                text_parts[1] = text_parts[1][0].lower() + text_parts[1][1:]

            text = replacement.join(text_parts)

        return text

    def get_name(self, prefix=None, inverse_prefix=None):
        if prefix == None:
            prefix_key = None
        else:
            prefix_key = prefix.symbol

        cache = self._name_cache.get(prefix_key)

        if cache == None:
            cache = {}
            self._name_cache[prefix_key] = cache

        if inverse_prefix == None:
            inverse_prefix_key = None
        else:
            inverse_prefix_key = inverse_prefix.symbol

        name = cache.get(inverse_prefix_key)

        if name == None:
            name = self._inject_prefix({'en': self._name}, prefix, inverse_prefix, 'en', space_case=True)
            cache[inverse_prefix_key] = name

        return name

    def get_base_title(self, language=None):
        return select_lang(self._title, language=language).format(prefix='', inverse_prefix='')

    def get_title(self, prefix=None, inverse_prefix=None, language=None):
        return self._inject_prefix(self._title, prefix, inverse_prefix, language)

    def get_base_symbol(self):
        return self._symbol.format(prefix='', inverse_prefix='')

    def get_symbol(self, prefix=None, inverse_prefix=None):
        if prefix != None:
            prefix_symbol = prefix.symbol
        elif self._prefix != None:
            prefix_symbol = self._prefix.symbol
        else:
            prefix_symbol = ''

        if inverse_prefix != None:
            inverse_prefix_symbol = inverse_prefix.symbol
        elif self._inverse_prefix != None:
            inverse_prefix_symbol = self._inverse_prefix.symbol
        else:
            inverse_prefix_symbol = ''

        return self._symbol.format(prefix=prefix_symbol, inverse_prefix=inverse_prefix_symbol)

    def get_usage(self, language=None):
        return select_lang(self._usage, language=language)

    def get_sequence(self, language=None):
        return select_lang(self._sequence, language=language)

    def get_numerator_exponent(self):
        return self._numerator_exponent

    def get_denominator_exponent(self):
        return self._denominator_exponent

    def get_allowed_prefixes(self):
        return self._allowed_prefixes

    def get_allowed_inverse_prefixes(self):
        return self._allowed_inverse_prefixes

    def get_prefix(self):
        return self._prefix

    def get_inverse_prefix(self):
        return self._inverse_prefix

    def clone(self, prefix=None, inverse_prefix=None):
        assert prefix == None or prefix.symbol in self._allowed_prefixes, prefix
        assert inverse_prefix == None or inverse_prefix.symbol in self._allowed_inverse_prefixes, inverse_prefix

        return Unit(self._name,
                    self._title,
                    self._symbol,
                    self._usage,
                    self._allowed_prefixes,
                    self._allowed_inverse_prefixes,
                    sequence=self._sequence,
                    numerator_exponent=self._numerator_exponent,
                    denominator_exponent=self._denominator_exponent,
                    prefix=prefix,
                    inverse_prefix=inverse_prefix)

    def __eq__(self, other):
        return isinstance(other, Unit) \
            and self._name == other._name \
            and self._title == other._title \
            and self._symbol == other._symbol \
            and self._usage == other._usage \
            and self._allowed_prefixes == other._allowed_prefixes \
            and self._allowed_inverse_prefixes == other._allowed_inverse_prefixes \
            and self._sequence == other._sequence \
            and self._numerator_exponent == other._numerator_exponent \
            and self._denominator_exponent == other._denominator_exponent \
            and self._prefix == other._prefix \
            and self._inverse_prefix == other._inverse_prefix \

    def __ne__(self, other):
        return not self == other

units = [
    Unit('{prefix}Ampere',
         {'en': '{prefix}Ampere', 'de': '{prefix}Ampere'},
         '{prefix}A',
         {'en': 'Electric current', 'de': 'Elektrische Stromstärke'},
         ['n', 'µ', 'm', 'k'],
         []),

    Unit('{prefix}Baud',
         {'en': '{prefix}Baud', 'de': '{prefix}Baud'},
         '{prefix}Bd',
         {'en': 'Symbol rate', 'de': 'Symbolrate'},
         ['k', 'M'],
         []),

    Unit('{prefix}Bit Per Second',
         {'en': '{prefix}Bit per second', 'de': '{prefix}Bit pro Sekunde'},
         '{prefix}bit/s',
         {'en': 'Data Rate', 'de': 'Datenrate'},
         ['k', 'M'],
         []),

    Unit('{prefix}Byte',
         {'en': '{prefix}Byte', 'de': '{prefix}Byte'},
         '{prefix}B',
         {'en': 'Data Size', 'de': 'Datenmenge'},
         ['Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei'],
         []),

    Unit('Decibel',
         {'en': 'Decibel', 'de': 'Dezibel'},
         'dB',
         {'en': 'Level', 'de': 'Pegel'},
         [],
         []),

    Unit('Degree',
         {'en': 'Degree', 'de': 'Grad'},
         '°',
         {'en': 'Angle', 'de': 'Winkel'},
         [],
         []),

    Unit('Degree Celsius',
         {'en': 'Degree Celsius', 'de': 'Grad Celsius'},
         '°C',
         {'en': 'Temperature', 'de': 'Temperatur'},
         [],
         []),

    Unit('Degree Per {inverse_prefix}Second',
         {'en': 'Degree per {inverse_prefix}second', 'de': 'Grad pro {inverse_prefix}Sekunde'},
         '°/{inverse_prefix}s',
         {'en': 'Angular velocity', 'de': 'Winkelgeschwindigkeit'},
         [],
         ['n', 'µ', 'm']),

    Unit('Degree Per {inverse_prefix}Second Squared',
         {'en': 'Degree per {inverse_prefix}second squared', 'de': 'Grad pro {inverse_prefix}Sekunde Quadrat'},
         '°/{inverse_prefix}s²',
         {'en': 'Angular acceleration', 'de': 'Winkelbeschleunigung'},
         [],
         ['n', 'µ', 'm'],
         denominator_exponent=2),

    Unit('{prefix}Gram',
         {'en': '{prefix}Gram', 'de': '{prefix}Gramm'},
         '{prefix}g',
         {'en': 'Mass', 'de': 'Masse'},
         ['n', 'µ', 'm', 'k'],
         []),

    Unit('{prefix}Gram Per Cubic Meter',
         {'en': '{prefix}Gram per cubic meter', 'de': '{prefix}Gramm pro Kubikmeter'},
         '{prefix}g/m³',
         {'en': 'Density', 'de': 'Dichte'},
         ['n', 'µ', 'm', 'k'],
         []),

    Unit('{prefix}Hertz',
         {'en': '{prefix}Hertz', 'de': '{prefix}Hertz'},
         '{prefix}Hz',
         {'en': 'Frequency', 'de': 'Frequenz'},
         ['k', 'M'],
         []),

    Unit('Kelvin',
         {'en': 'Kelvin', 'de': 'Kelvin'},
         'K',
         {'en': 'Temperature', 'de': 'Temperatur'},
         [],
         []),

    Unit('Lux',
         {'en': 'Lux', 'de': 'Lux'},
         'lx',
         {'en': 'Illuminance', 'de': 'Beleuchtungsstärke'},
         [],
         []),

    Unit('{prefix}Meter',
         {'en': '{prefix}Meter', 'de': '{prefix}Meter'},
         '{prefix}m',
         {'en': 'Length', 'de': 'Länge'},
         ['n', 'µ', 'm', 'c', 'k'],
         []),

    Unit('{prefix}Meter Per Hour',
         {'en': '{prefix}Meter per hour', 'de': '{prefix}Meter pro Stunde'},
         '{prefix}m/h',
         {'en': 'Speed', 'de': 'Geschwindigkeit'},
         ['n', 'µ', 'm', 'c', 'k'],
         []),

    Unit('{prefix}Meter Per Second',
         {'en': '{prefix}Meter per second', 'de': '{prefix}Meter pro Sekunde'},
         '{prefix}m/s',
         {'en': 'Speed', 'de': 'Geschwindigkeit'},
         ['n', 'µ', 'm', 'c', 'k'],
         []),

    Unit('{prefix}Meter Per Second Squared',
         {'en': '{prefix}Meter per second squared', 'de': '{prefix}Meter pro Sekunde Quadrat'},
         '{prefix}m/s²',
         {'en': 'Acceleration', 'de': 'Beschleunigung'},
         ['n', 'µ', 'm', 'c', 'k'],
         []),

    Unit('{prefix}Ohm',
         {'en': '{prefix}Ohm', 'de': '{prefix}Ohm'},
         '{prefix}Ω',
         {'en': 'Electrical Resistance', 'de': 'Elektrischer Widerstand'},
         ['n', 'µ', 'm', 'k', 'M'],
         []),

    Unit('Particles Per Cubic {inverse_prefix}Meter',
         {'en': 'Particles per cubic {inverse_prefix}meter', 'de': 'Partikel pro Kubik{inverse_prefix}meter'},
         '1/{inverse_prefix}m³',
         {'en': 'Particle number density', 'de': 'Teilchendichte'},
         [],
         ['n', 'µ', 'm', 'c'],
         denominator_exponent=3),

    Unit('Parts Per Million',
         {'en': 'Parts per million', 'de': 'Parts per million'},
         'ppm',
         {'en': 'Fraction', 'de': 'Anteil'},
         [],
         []),

    Unit('{prefix}Pascal',
         {'en': '{prefix}Pascal', 'de': '{prefix}Pascal'},
         '{prefix}Pa',
         {'en': 'Pressure', 'de': 'Druck'},
         ['n', 'µ', 'm', 'h', 'k', 'M'],
         []),

    Unit('Percent',
         {'en': 'Percent', 'de': 'Prozent'},
         '%',
         {'en': 'Fraction', 'de': 'Anteil'},
         [],
         []),

    Unit('Percent Per Second',
         {'en': 'Percent Per Second', 'de': 'Prozent pro Sekunde'},
         '%/s',
         {'en': 'Duty Cycle Change', 'de': 'Tastverhältnisänderung'},
         [],
         []),

    Unit('Percent Relative Humidity',
         {'en': 'Percent relative humidity', 'de': 'Prozent relative Luftfeuchtigkeit'},
         '%',
         {'en': 'Relative Humidity', 'de': 'Relative Luftfeuchtigkeit'},
         [],
         []),

    Unit('{prefix}Second',
         {'en': '{prefix}Second', 'de': '{prefix}Sekunde'},
         '{prefix}s',
         {'en': 'Time', 'de': 'Zeit'},
         ['n', 'µ', 'm'],
         []),

    Unit('Standard Gravity',
         {'en': 'Standard gravity', 'de': 'Normfallbeschleunigung'},
         'gₙ',
         {'en': 'Gravitational acceleration', 'de': 'Fallbeschleunigung'},
         [],
         []),

    Unit('Steps Per {inverse_prefix}Second',
         {'en': 'Steps per {inverse_prefix}second', 'de': 'Schritte pro {inverse_prefix}Sekunde'},
         '1/{inverse_prefix}s',
         {'en': 'Velocity', 'de': 'Geschwindigkeit'},
         [],
         ['n', 'µ', 'm']),

     Unit('Steps Per {inverse_prefix}Second Squared',
         {'en': 'Steps per {inverse_prefix}second squared', 'de': 'Schritte pro {inverse_prefix}Sekunde Quadrat'},
         '1/{inverse_prefix}s²',
         {'en': 'Acceleration', 'de': 'Beschleunigung'},
         [],
         ['n', 'µ', 'm'],
         denominator_exponent=2),

    Unit('{prefix}Tesla',
         {'en': '{prefix}Tesla', 'de': '{prefix}Tesla'},
         '{prefix}T',
         {'en': 'Magnetic flux density', 'de': 'Magnetische Flussdichte'},
         ['n', 'µ', 'm', 'k', 'M'],
         []),

    Unit('UV Index',
         {'en': 'UV Index', 'de': 'UV-Index'},
         '',
         {'en': 'Strength of sunburn-producing ultraviolet radiation', 'de': 'Sonnenbrandwirksame solare Bestrahlungsstärke'},
         [],
         []),

    Unit('{prefix}Volt',
         {'en': '{prefix}Volt', 'de': '{prefix}Volt'},
         '{prefix}V',
         {'en': 'Electric potential', 'de': 'Elektrische Spannung'},
         ['n', 'µ', 'm', 'k', 'M'],
         []),

    Unit('{prefix}Volt Ampere',
         {'en': '{prefix}Volt-ampere', 'de': '{prefix}Voltampere'},
         '{prefix}VA',
         {'en': 'Apparent power', 'de': 'Scheinleistung'},
         ['n', 'µ', 'm', 'k', 'M'],
         []),

    Unit('Volt Ampere Reactive',
         {'en': 'Volt-ampere reactive', 'de': 'Voltampere reaktiv'},
         'var',
         {'en': 'Reactive power', 'de': 'Blindleistung'},
         [],
         []),

    Unit('{prefix}Watt',
         {'en': '{prefix}Watt', 'de': '{prefix}Watt'},
         '{prefix}W',
         {'en': 'Power', 'de': 'Leistung'},
         ['n', 'µ', 'm', 'k', 'M'],
         []),

    Unit('{prefix}Watt Hour',
         {'en': '{prefix}Watt-hour', 'de': '{prefix}Wattstunde'},
         '{prefix}Wh',
         {'en': 'Energy', 'de': 'Energie'},
         ['n', 'µ', 'm', 'k', 'M'],
         []),

    Unit('{prefix}Watt Per Square Meter',
         {'en': '{prefix}Watt per square meter', 'de': '{prefix}Watt pro Quadratmeter'},
         '{prefix}W/m²',
         {'en': 'Irradiance', 'de': 'Bestrahlungsstärke'},
         ['n', 'µ', 'm', 'k', 'M'],
         [])
]

UnitPrefix = namedtuple('UnitPrefix', 'symbol name index divisor')

unit_prefixes = [
    # denominator prefixes must come first, ordered from biggest to smallest denominator
    UnitPrefix('n', {'en': 'Nano',  'de': 'Nano'},  1, 1000000000),
    UnitPrefix('µ', {'en': 'Micro', 'de': 'Mikro'}, 1, 1000000),
    UnitPrefix('m', {'en': 'Milli', 'de': 'Milli'}, 1, 1000),
    UnitPrefix('c', {'en': 'Centi', 'de': 'Zenti'}, 1, 100),

    # numerator prefixes must come second, ordered from biggest to smallest numerator
    UnitPrefix('Ei', {'en': 'Exbi',  'de': 'Exbi'},  0, 2**60),
    UnitPrefix('Pi', {'en': 'Pebi',  'de': 'Pebi'},  0, 2**50),
    UnitPrefix('Ti', {'en': 'Tebi',  'de': 'Tebi'},  0, 2**40),
    UnitPrefix('Gi', {'en': 'Gibi',  'de': 'Gibi'},  0, 2**30),
    UnitPrefix('G',  {'en': 'Giga',  'de': 'Giga'},  0, 1000000000),
    UnitPrefix('Mi', {'en': 'Mebi',  'de': 'Mebi'},  0, 2**20),
    UnitPrefix('M',  {'en': 'Mega',  'de': 'Mega'},  0, 1000000),
    UnitPrefix('Ki', {'en': 'Kibi',  'de': 'Kibi'},  0, 2**10),
    UnitPrefix('k',  {'en': 'Kilo',  'de': 'Kilo'},  0, 1000),
    UnitPrefix('h',  {'en': 'Hecto', 'de': 'Hekto'}, 0, 100)
]

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
    def __init__(self, raw_data, device):
        assert isinstance(raw_data, dict)

        check_name(raw_data['name'])

        self.raw_data = raw_data
        self.device = device
        self.name = FlavoredName(raw_data['name'])
        self.constants = []

        for raw_constant in raw_data['constants']:
            self.constants.append(self.get_generator().get_constant_class()(raw_constant, self))

    def get_device(self): # parent
        return self.device

    def get_generator(self):
        return self.get_device().get_generator()

    def get_name(self, *args, **kwargs):
        return self.name.get(*args, **kwargs)

    def get_type(self):
        return self.raw_data['type']

    def get_constants(self):
        return self.constants

    def get_elements(self, packet):
        elements = []

        for element in packet.get_elements():
            constant_group = element.get_constant_group()

            if constant_group != None and constant_group.get_name().space == self.get_name().space:
                elements.append(element)

        return elements

    def is_virtual(self):
        return self.raw_data.get('is_virtual', False)

class Element(object):
    def __init__(self, raw_data, packet, level, role):
        self.raw_data = raw_data
        self.packet = packet
        self.level = level
        self.role = role
        self._extra = []

        check_name(raw_data[0])

        self.name = FlavoredName(raw_data[0])

        assert len(raw_data) == 4 or len(raw_data) == 5, raw_data

        if len(self.raw_data) > 4:
            raw_data_extra = self.raw_data[4]
        else:
            raw_data_extra = {}

        assert isinstance(raw_data_extra, (dict, list)), raw_data

        if isinstance(raw_data_extra, list):
            assert len(raw_data_extra) == self.get_cardinality(), raw_data
            assert self.get_cardinality() > 1, raw_data
            assert self.get_type() != 'string', raw_data
        else:
            raw_data_extra = [raw_data_extra]

        constant_group_names = set()

        for extra in raw_data_extra:
            # possible extra config, all values are optional
            #
            # name:           non-empty string following the general name rules, allowed for indexed extra config only
            # scale:          2-tuple of int values representing a fraction, or 'dynamic', or 'unknown'
            # unit:           non-empty string representing an optionally prefixed unit name, or 'dynamic', or 'unknown'
            # range:          2-tuple of int values representing an inclusive min/max range, or a list of non-overlapping 2-tuples, or 'dynamic', or 'constants', or 'unknown'
            # constant_group: non-empty string representing a constant group name
            # default:        default value
            #
            # 'dynamic':      this value should be used when a scale/unit/range is not fixed, but depends some other runtime config
            # 'unknown':      this value must only be used during development, as a reminder to insert a proper value in the future

            assert len(set(extra.keys()) - set(['name', 'scale', 'unit', 'range', 'constant_group', 'default'])) == 0, raw_data

            name = extra.get('name')

            if name != None:
                assert isinstance(name, str), raw_data
                assert len(raw_data_extra) > 1, raw_data

                check_name(name)

            if 'scale' not in extra:
                scale = (1, 1)
            else:
                scale = extra['scale']

                if scale == 'unknown':
                    scale = (1, 1)
                elif scale == 'dynamic':
                    assert self.get_type() not in ['float', 'bool', 'char', 'string'], raw_data
                else:
                    assert isinstance(scale, tuple), raw_data
                    assert len(scale) == 2, raw_data
                    assert isinstance(scale[0], int), raw_data
                    assert isinstance(scale[1], int), raw_data
                    assert scale[0] >= 1, raw_data
                    assert scale[1] >= 1, raw_data
                    assert scale[0] != scale[1], raw_data
                    assert gcd(*scale) == 1, raw_data
                    assert self.get_type() not in ['float', 'bool', 'char', 'string'], raw_data

            unit_name = extra.get('unit')

            if unit_name == 'unknown':
                unit_name = None

            if unit_name == None:
                unit = None
            elif unit_name == 'dynamic':
                unit = 'dynamic'
            else:
                assert self.get_type() not in ['float', 'bool', 'char', 'string'], raw_data

                unit = None

                for candidate in units:
                    if unit_name == candidate.get_name():
                        unit = candidate
                        break

                    candidate_allowed_prefixes = candidate.get_allowed_prefixes()
                    candidate_allowed_inverse_prefixes = candidate.get_allowed_inverse_prefixes()

                    for unit_prefix in unit_prefixes:
                        if unit_prefix.symbol not in candidate_allowed_prefixes:
                            continue

                        if unit_name == candidate.get_name(prefix=unit_prefix):
                            unit = candidate.clone(prefix=unit_prefix)
                            break

                        for unit_inverse_prefix in unit_prefixes:
                            if unit_inverse_prefix.symbol not in candidate_allowed_inverse_prefixes:
                                continue

                            if unit_name == candidate.get_name(prefix=unit_prefix, inverse_prefix=unit_inverse_prefix):
                                unit = candidate.clone(prefix=unit_prefix, inverse_prefix=unit_inverse_prefix)
                                break

                        if unit != None:
                            break

                    if unit != None:
                        break

                    for unit_inverse_prefix in unit_prefixes:
                        if unit_inverse_prefix.symbol not in candidate_allowed_inverse_prefixes:
                            continue

                        if unit_name == candidate.get_name(inverse_prefix=unit_inverse_prefix):
                            unit = candidate.clone(inverse_prefix=unit_inverse_prefix)
                            break

                    if unit != None:
                        break

                assert unit != None, unit_name

            if 'constant_group' in extra:
                range_default = 'constants'
            elif self.get_type() not in ['float', 'bool', 'char', 'string']:
                range_default = 'type'
            else:
                range_default = None

            range_ = extra.get('range')

            if range_ == 'unknown':
                range_ = None

            if range_ == None:
                if 'constant_group' in extra:
                    range_ = 'constants'
                elif self.get_type() not in ['float', 'bool', 'char', 'string']:
                    range_ = 'type'

            if range_ not in [None, 'type', 'constants', 'dynamic']:
                if isinstance(range_, tuple):
                    range_ = [range_]

                assert self.get_type() not in ['bool', 'string'], raw_data
                assert isinstance(range_, list), raw_data
                assert len(range_) > 0, raw_data

                for i, subrange in enumerate(list(range_)):
                    assert isinstance(subrange, tuple), raw_data
                    assert len(subrange) == 2, raw_data
                    assert subrange != (None, None), raw_data

                    if subrange[0] == None:
                        assert i == 0, raw_data

                        subrange = (self.get_type_range()[0], subrange[1])

                    if subrange[1] == None:
                        assert i == len(range_) - 1, raw_data

                        subrange = (subrange[0], self.get_type_range()[1])

                    assert subrange[0] <= subrange[1], raw_data

                    if i > 0:
                        assert range_[i - 1][1] < subrange[0], raw_data

                    if i < len(range_) - 1:
                        assert subrange[1] < range_[i + 1][0], raw_data

                    if self.get_type() not in ['float', 'string']:
                        assert subrange != self.get_type_range(), raw_data

                    if self.get_type() == 'char':
                        assert isinstance(subrange[0], str), raw_data
                        assert isinstance(subrange[1], str), raw_data
                        assert len(subrange[0]) == 1, raw_data
                        assert len(subrange[1]) == 1, raw_data
                        assert ord(subrange[0]) <= 255, raw_data
                        assert ord(subrange[1]) <= 255, raw_data
                    elif self.get_type() == 'float':
                        assert isinstance(subrange[0], float), raw_data
                        assert isinstance(subrange[1], float), raw_data
                    else:
                        assert isinstance(subrange[0], int), raw_data
                        assert isinstance(subrange[1], int), raw_data

                    range_[i] = subrange

            constant_group_name = extra.get('constant_group')

            constant_group_names.add(constant_group_name)

            if constant_group_name == None:
                constant_group = None
            else:
                assert range_ != None, raw_data
                assert self.get_type() not in ['string'], raw_data
                assert isinstance(constant_group_name, str), raw_data

                constant_group = self.get_device().get_constant_group(constant_group_name)

                assert constant_group.get_type() == self.get_type(), raw_data

            default = extra.get('default')

            if default != None:
                assert packet.get_type() == 'function', raw_data

                if self.get_cardinality() != 1 and len(raw_data_extra) == 1:
                    if self.get_type() == 'string':
                        assert isinstance(default, str) and len(default) <= self.get_cardinality(), raw_data
                    else:
                        assert isinstance(default, list) and \
                               ((self.get_role() == 'stream_chunk_data' and len(default) <= self.get_cardinality()) or
                                (self.get_role() == 'stream_data' and len(default) <= abs(self.get_cardinality())) or
                                len(default) == self.get_cardinality()), raw_data

                assert len(raw_data_extra) == 1 or not isinstance(default, list), raw_data

                if not isinstance(default, list):
                    default = [default]

                for subdefault in default:
                    if self.get_type().startswith('uint') or self.get_type().startswith('int'):
                        if sys.hexversion < 0x03000000:
                            assert isinstance(subdefault, (int, long)), raw_data
                        else:
                            assert isinstance(subdefault, int), raw_data
                    elif self.get_type() == 'float':
                        assert isinstance(subdefault, float), raw_data
                    elif self.get_type() == 'bool':
                        assert isinstance(subdefault, bool), raw_data
                    elif self.get_type() == 'char':
                        assert isinstance(subdefault, str), raw_data
                        assert len(subdefault) == 1, raw_data
                        assert ord(subdefault) <= 255, raw_data

                    assert range_ != 'dynamic', raw_data

                    if range_ == 'constants':
                        pass # FIXME: check if default value is in range
                    elif range_ != None:
                        if range_ == 'type':
                            actual_range = [self.get_type_range()]
                        else:
                            actual_range = range_

                        found = False

                        for subrange in actual_range:
                            if subdefault >= subrange[0] and subdefault <= subrange[1]:
                                found = True
                                break

                        assert found, raw_data

                if len(default) == 1:
                    default = default[0]

                # FIXME: add tooltip for contants

            self._extra.append({'name': name, 'scale': scale, 'unit': unit, 'range': range_, 'constant_group': constant_group, 'default': default})

        # FIXME: enforce that there is at most one contant group per element and
        #        not one per index, because some generators cannot handle that yet
        assert len(constant_group_names) <= 1, constant_group_names

        if len(self._extra) == 0:
            self._extra = {}
        elif len(self._extra) == 1:
            self._extra = self._extra[0]

    def get_packet(self): # parent
        return self.packet

    def get_device(self):
        return self.packet.get_device()

    def get_generator(self):
        return self.packet.get_generator()

    def is_struct(self):
        return isinstance(self._extra, list)

    def get_indices(self):
        if self.is_struct():
            indices = list(range(self.get_cardinality()))
        else:
            indices = [None]

        return indices

    def get_name(self, *args, **kwargs):
        if 'index' in kwargs:
            index = kwargs['index']

            del kwargs['index']

            if index != None:
                name = self._get_extra(index).get('name')

                if name == None:
                    return None

                return FlavoredName(name).get(*args, **kwargs)

        return self.name.get(*args, **kwargs)

    def get_type(self):
        return self.raw_data[1]

    def get_type_range(self):
        type_ = self.get_type()

        assert type_ not in ['float', 'string'], self.raw_data

        if type_ == 'bool':
            minimum = False
            maximum = True
        elif type_ == 'char':
            minimum = chr(0)
            maximum = chr(255)
        else:
            bits = int(type_.replace('uint', '').replace('int', ''), base=10)
            minimum = 0
            maximum = (2 ** bits) - 1

            if not type_.startswith('u'):
                minimum = -maximum // 2
                maximum = maximum // 2

        return (minimum, maximum)

    def get_cardinality(self):
        return self.raw_data[2]

    def get_direction(self):
        return self.raw_data[3]

    def get_role(self):
        return self.role

    def get_level(self):
        return self.level

    def _get_extra(self, index):
        assert not self.is_struct() or isinstance(index, int), index

        if index == None:
            return self._extra

        return self._extra[index]

    def get_scale(self, index=None):
        return self._get_extra(index).get('scale')

    def get_unit(self, index=None):
        return self._get_extra(index).get('unit')

    def get_range(self, index=None):
        return self._get_extra(index).get('range')

    def get_constant_group(self, index=None):
        return self._get_extra(index).get('constant_group')

    def get_default(self, index=None):
        return self._get_extra(index).get('default')

    def get_item_size(self):
        if self.level == 'high':
            raise GeneratorError('Invalid call for high-level element')

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
        if self.get_level() == 'high':
            raise GeneratorError('Invalid call for high-level element')

        cardinality = self.get_cardinality()

        if self.get_type() == 'bool':
            return int(math.ceil(cardinality / 8.0))

        return self.get_item_size() * cardinality

    def format_value(self, value):
        raise GeneratorError("format_value() not implemented")

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
                           'c',
                           'vf',
                           'if'])

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
            raise GeneratorError("Name of packet {} with high-level features has to end with 'Low Level'".format(raw_data['name']))

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
                raise GeneratorError('Invalid element type: {}'.format(element.get_type()))

            if not isinstance(element.get_cardinality(), int) or element.get_cardinality() < 1:
                raise GeneratorError('Invalid element cardinality: {}'.format(element.get_cardinality()))

            if element.get_direction() not in ['in', 'out']:
                raise GeneratorError('Invalid element direction: {}'.format(element.get_direction()))

            if element.get_direction() == 'in' and len(self.elements) > 0 and self.elements[-1].get_direction() == 'out':
                raise GeneratorError("'in' element cannot come after 'out' element")

            if element.get_direction() == 'in':
                if self.get_type() == 'callback':
                    raise GeneratorError("'in' element not allowed for callback")

                payload_in_size += element.get_size()
            else:
                payload_out_size += element.get_size()

            if not self.is_virtual() and (payload_in_size > 64 or payload_out_size > 64):
                raise GeneratorError('Payload too long (in {0}, out {1}): '.format(payload_in_size, payload_out_size) + raw_data['name'])

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
            for index in element.get_indices():
                constant_group = element.get_constant_group(index=index)

                if constant_group != None and constant_group not in self.constant_groups:
                    self.constant_groups.append(constant_group)

        self.add_high_level_callback_note()

    def add_high_level_callback_note(self):
        if not self.get_generator().generates_high_level_callbacks():
            return

        if self.get_type() != 'callback' or not self.has_high_level():
            return

        null = self.get_generator().get_doc_null_value_name()
        param = self.get_generator().get_doc_formatted_param(self.get_high_level('stream_*').get_data_element())
        doc = self.raw_data['doc'][1]
        doc['de'] += """
.. note::
 Falls das Rekonstruieren des Wertes fehlschlägt, wird der Callback mit {} für {} ausgelöst.
""".format(null, param)
        doc['en'] += """
.. note::
 If reconstructing the value fails, the callback is triggered with {} for {}.
""".format(null, param)

    def get_device(self): # parent
        return self.device

    def get_generator(self):
        return self.device.get_generator()

    def get_type(self):
        return self.raw_data['type']

    def get_name(self, *args, **kwargs):
        return self.name.get(*args, **kwargs)

    def get_elements(self, name=None, direction=None, high_level=False, role='all'):
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

            if role != 'all' and element.get_role() != role:
                continue

            elements.append(element)

        return elements

    def get_formatted_element_meta(self, type_func, name_func, include_function_id=False, high_level=False, **kwargs):
        if include_function_id:
            function_id = self.get_function_id()
        else:
            function_id = None

        return format_full_element_meta(self.get_type(),
                                        self.get_elements(high_level=high_level),
                                        self.get_elements(),
                                        type_func,
                                        name_func,
                                        function_id=function_id,
                                        **kwargs)

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
        if len(self.get_elements(direction='out')) > 0:
            assert 'response_expected' not in self.raw_data, 'cannot change response_expected away from always_true'

            response_expected = 'always_true'
        elif self.get_doc_type() == 'ccf' or self.get_high_level('stream_in') != None:
            assert 'response_expected' not in self.raw_data, 'cannot change response_expected away from true'

            response_expected = 'true'
        else:
            response_expected = self.raw_data.get('response_expected', 'false')

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
            if constant_group.is_virtual():
                continue

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
        self.constant_groups = []
        self.all_packets = []
        self.all_packets_without_doc_only = []
        self.all_function_packets = []
        self.all_function_packets_without_doc_only = []
        self.callback_packets = []
        self.examples = []
        self._doc_rst_links_cache = {}

        check_name(raw_data['name'], display_name=raw_data['display_name'])

        self.category = FlavoredName(raw_data['category'])
        self.name = FlavoredName(raw_data['name'])

        raw_function_constant_group = {
            'is_virtual': True,
            'name': 'Function',
            'type': 'uint8',
            'constants': []
        }

        function_constant_group = generator.get_constant_group_class()(raw_function_constant_group, self)

        self.constant_groups.append(function_constant_group)

        for raw_constant_group in raw_data['constant_groups']:
            constant_group = generator.get_constant_group_class()(raw_constant_group, self)
            constant_group_name = constant_group.get_name().space

            for other_constant_group in self.constant_groups:
                if other_constant_group.get_name().space == constant_group_name:
                    raise GeneratorError('Constant Group {0} is not unique'.format(constant_group_name))

            self.constant_groups.append(constant_group)

        next_function_id = 1

        for raw_packet in raw_data['packets']:
            if not 'function_id' in raw_packet:
                raw_packet['function_id'] = next_function_id
                next_function_id += 1
            elif raw_packet['function_id'] >= 0:
                next_function_id = raw_packet['function_id'] + 1

            packet = generator.get_packet_class()(raw_packet, self)

            self.all_packets.append(packet)

            if packet.get_function_id() >= 0:
                self.all_packets_without_doc_only.append(packet)

        self.all_packets = sorted(self.all_packets, key=lambda packet: packet.get_function_id() if packet.get_function_id() > 0 else 1000)
        self.all_packets_without_doc_only = sorted(self.all_packets_without_doc_only, key=lambda packet: packet.get_function_id() if packet.get_function_id() > 0 else 1000)

        # Skip this check for the EVSE bricklet: The API was broken several times while the (unreleased) EVSE Bricklets
        # were already in the field as part of the WARP charger. This is save, because the Charger flashes a matching
        # firmware when updating itself.
        if not self.is_released() and self.get_api_version() != [2, 0, 0] and self.get_device_identifier() != 2159:
            raise GeneratorError('Unreleased device must have API version 2.0.0')

        since_firmwares = set()

        for packet in self.all_packets:
            since_firmware = packet.get_since_firmware()

            if since_firmware != None and since_firmware > [2, 0, 0]:
                since_firmwares.add(packet.get_formatted_since_firmware())

        since_firmwares = list(since_firmwares)

        if len(since_firmwares) + self.get_api_version_extra() != self.get_api_version()[2]:
            raise GeneratorError('API version mismatch: API version is 2.0.{}, expected was 2.0.{}, i.e. len(set(since_firmwares)) (= {}) + api_versions_extra (= {})'
                                 .format(self.get_api_version()[2], len(since_firmwares) + self.get_api_version_extra(), len(since_firmwares), self.get_api_version_extra()))

        function_names = set()
        callback_names = set()

        for packet in self.all_packets:
            packet_type = packet.get_type()
            packet_name = packet.get_name()

            if packet_type == 'function':
                if packet_name.lower in function_names:
                    raise GeneratorError('Function name is not unique: ' + packet_name.space)
                else:
                    function_names.add(packet_name.lower)

                self.all_function_packets.append(packet)

                if packet.get_function_id() >= 0:
                    self.all_function_packets_without_doc_only.append(packet)
            elif packet_type == 'callback':
                if 'Callback' in packet_name.space:
                    raise GeneratorError("Callback name cannot contain 'Callback': " + packet_name.space)

                if packet_name.lower in callback_names:
                    raise GeneratorError('Callback name is not unique: ' + packet_name.space)
                else:
                    callback_names.add(packet_name.lower)

                self.callback_packets.append(packet)
            else:
                raise GeneratorError('Invalid packet type ' + packet_type)

        for raw_example in raw_data['examples']:
            self.examples.append(generator.get_example_class()(raw_example, self))

        for packet in self.get_packets('function'):
            if len(packet.get_elements(direction='out', high_level=True)) == 0 and packet.get_function_id() >= 0:
                raw_constant = (packet.get_name(skip=-2 if packet.has_high_level() else 0).space, packet.get_function_id())

                function_constant_group.constants.append(generator.get_constant_class()(raw_constant, self))

    def get_generator(self): # parent
        return self.generator

    def has_comcu(self):
        return self.has_feature('comcu_bricklet')

    def has_openhab(self):
        return 'openhab' in self.raw_data

    def has_feature(self, feature):
        return feature in self.raw_data['features']

    def is_released(self):
        return self.raw_data['released'] or self.generator.internal

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

    def is_tng(self):
        return self.get_category().space == 'TNG'

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

        if name == 'Industrial PTC':
            name = 'PTC'

        name = re.sub('[0-9]+x[0-9]+', '', name).replace('  ', ' ').strip()

        if ' ' not in name and (name.isupper() or self.is_brick()):
            return name.lower()

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

        if self.is_tng():
            return self.get_category().space + ' ' + display_name

        if display_name.endswith(' 2.0') or display_name.endswith(' 3.0'):
            parts = display_name.split(' ')
            parts.insert(-1, self.get_category().space)

            return ' '.join(parts)

        return display_name + ' ' + self.get_category().space

    def get_manufacturer(self):
        return self.raw_data['manufacturer']

    def get_description(self):
        return self.raw_data['description']

    def get_esp32_firmware(self):
        return self.raw_data.get('esp32_firmware')

    def get_git_name(self):
        if self.is_tng():
            return self.get_category().dash + '-' + self.get_name().dash

        return self.get_name().dash + '-' + self.get_category().dash

    def get_git_dir(self):
        global_root_dir = os.path.normpath(os.path.join(self.get_generator().get_root_dir(), '..', '..'))

        return os.path.join(global_root_dir, self.get_git_name())

    def get_constant_group(self, name):
        for constant_group in self.constant_groups:
            if constant_group.get_name().space == name:
                return constant_group

        raise GeneratorError("Unknown Constant Group '{0}'".format(name))

    def get_packets(self, type_=None):
        if type_ == None:
            if self.generator.is_doc_generator:
                return self.all_packets

            return self.all_packets_without_doc_only

        if type_ == 'function':
            if self.generator.is_doc_generator:
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
            if constant_group.is_virtual():
                continue

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

    def get_doc_rst_name(self):
        if self.is_tng():
            return self.get_category().camel + '_' + self.get_name().camel

        return self.get_name().camel + '_' + self.get_category().camel

    def get_doc_rst_path(self):
        if not self.get_generator().is_doc_generator:
            raise GeneratorError("Invalid call in non-doc generator")

        filename = self.get_doc_rst_name() + '_' + self.get_generator().get_doc_rst_filename_part() + '.rst'

        return os.path.join(self.get_generator().get_doc_dir(),
                            self.get_generator().get_language(),
                            filename)

    def get_doc_rst_ref_name(self):
        if not self.get_generator().is_doc_generator:
            raise GeneratorError("Invalid call in non-doc generator")

        if self.is_tng():
            return self.get_category().under + '_' + self.get_name().under

        return self.get_name().under + '_' + self.get_category().under

    def specialize_doc_rst_links(self, text, specializer, prefix=None):
        for keyword, type_ in [('func', 'function'), ('cb', 'callback')]:
            if type_ not in self._doc_rst_links_cache:
                cache = []

                for packet in self.get_packets(type_):
                    names = [packet.get_name().space]

                    if packet.has_high_level():
                        names.append(packet.get_name(skip=-2).space)

                    for name in names:
                        generic_name = ':{0}:`{1}`'.format(keyword, name)
                        special_name = specializer(packet, packet.has_high_level() and not name.endswith(' Low Level'))

                        cache.append((generic_name, special_name))

                self._doc_rst_links_cache[type_] = cache

            for generic_name, special_name in self._doc_rst_links_cache[type_]:
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
                elif raw_cleanup[0] == 'sleep':
                    self.cleanups.append(self.get_generator().get_example_special_function_class()(raw_cleanup, -index, self))
                else:
                    raise GeneratorError('only setter and sleep are allowed as cleanup functions')

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
    is_doc_generator = False
    is_openhab_doc_generator = False

    def __init__(self, root_dir, language, internal, config_name):
        self.root_dir = root_dir
        self.language = language # en or de
        self.internal = internal
        self.config_name = FlavoredName(' '.join([word[0].upper() + word[1:] for word in config_name.split('_')]))
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")

        if self.check_root_dir_name:
            root_dir_name = os.path.split(self.get_root_dir())[1]

            if self.get_bindings_name() != root_dir_name:
                raise GeneratorError("root directory '{0}' and bindings name '{1}' do not match".format(root_dir_name, self.get_bindings_name()))

        if self.get_config_name().space == 'Tinkerforge':
            self.bindings_dir_name = 'bindings'
            self.doc_dir_name = 'doc'
            self.zip_dir_name = 'zip'
        else:
            config_name = self.get_config_name().under

            self.bindings_dir_name = 'bindings_' + config_name
            self.doc_dir_name = 'doc_' + config_name
            self.zip_dir_name = 'zip_' + config_name

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

    def get_doc_null_value_name(self):
        raise GeneratorError("get_doc_null_value_name() not implemented")

    def get_doc_formatted_param(self, element):
        raise GeneratorError("get_doc_formatted_param() not implemented")

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

    def get_zip_dir(self):
        return os.path.join(self.get_root_dir(), self.zip_dir_name)

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

    def prepare(self):
        pass

    def generate(self, device):
        raise GeneratorError("generate() not implemented")

    def finish(self):
        pass

class DocGenerator(Generator):
    is_doc_generator = True

    def __init__(self, *args, **kwargs):
        Generator.__init__(self, *args, **kwargs)

        if self.get_bindings_name() != self.get_doc_rst_filename_part().lower():
            raise GeneratorError("bindings name '{0}' and doc rst name '{1}' do not match".format(self.get_bindings_name(), self.get_doc_rst_filename_part()))

    def get_doc_rst_filename_part(self):
        raise GeneratorError("get_doc_rst_filename_part() not implemented")

    def get_doc_example_regex(self):
        raise GeneratorError("get_doc_example_regex() not implemented")

    def prepare(self):
        recreate_dir(os.path.join(self.get_doc_dir(), self.get_language()))

    def finish(self):
        # Copy IPConnection examples
        example_regex = self.get_doc_example_regex()

        if example_regex != None:
            print_verbose('  * ip_connection')

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
    recreate_zip_dir = True

    def prepare(self):
        if self.recreate_zip_dir:
            recreate_dir(self.get_zip_dir())

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
            os.replace(zipname, os.path.join(self.get_root_dir(), zipname))

class ExamplesGenerator(Generator):
    skip_existing_incomplete_example = True
    forbid_execution = False

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

def tester_worker(cookie, args, env, cwd, setup, teardown):
    if setup != None:
        setup()

    try:
        exit_code, output = check_output_and_error(args, env=env, cwd=cwd)
    except Exception as e:
        return cookie, None, 'Tester Exception: ' + str(e)
    finally:
        if teardown != None:
            teardown()

    return cookie, exit_code, output

class Tester(object):
    PROCESSES = 8

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

    def execute(self, cookie, args, env=None, cwd=None, setup=None, teardown=None):
        def callback(result):
            self.handle_result(*result)

        self.pool.apply_async(tester_worker, args=(cookie, args, env, cwd, setup, teardown), callback=callback)

    def handle_source(self, tmp_dir, scratch_dir, path, extra):
        self.test_count += 1
        self.test((path,), tmp_dir, scratch_dir, path, extra)

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
                print('\033[01;32m>>> test succeeded\033[0m\n')
            else:
                self.failure_count += 1
                print('\033[01;31m>>> test failed\033[0m\n')
        else:
            if success:
                self.success_count += 1
                print('>>> test succeeded\n')
            else:
                self.failure_count += 1
                print('>>> test failed\n')

    def after_unzip(self, tmp_dir):
        return True

    def test(self, cookie, tmp_dir, scratch_dir, path, extra):
        raise NotImplementedError()

    def check_success(self, exit_code, output):
        return exit_code == 0

    def run(self):
        tmp_dir = os.path.join('/tmp/tester/unpack', self.name)
        scratch_base = os.path.join('/tmp/tester/scratch', self.name)

        # Make temporary directory
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

        if os.path.exists(scratch_base):
            shutil.rmtree(scratch_base)

        os.makedirs(tmp_dir)
        os.makedirs(scratch_base)

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

            if not self.after_unzip(tmp_dir):
                return False

            # test
            counter = 1

            for subdir in self.subdirs:
                for root, _, files in os.walk(os.path.join(tmp_dir, subdir)):
                    for name in files:
                        if not name.endswith(self.extension):
                            continue

                        scratch_dir = os.path.join(scratch_base, '{0:04}_{1}'.format(counter, name))
                        counter += 1

                        if os.path.exists(scratch_dir):
                            shutil.rmtree(scratch_dir)

                        os.makedirs(scratch_dir)
                        self.handle_source(tmp_dir, scratch_dir, os.path.join(root, name), False)

            for extra_path in self.extra_paths:
                scratch_dir = os.path.join(scratch_base, '{0:04}_{1}'.format(counter, os.path.split(extra_path)[-1]))
                counter += 1

                if os.path.exists(scratch_dir):
                    shutil.rmtree(scratch_dir)

                os.makedirs(scratch_dir)
                self.handle_source(tmp_dir, scratch_dir, extra_path, True)

            self.pool.close()
            self.pool.join()

        # report
        if self.comment != None:
            print('### [{0}] {1} file(s) tested, {2} test(s) succeeded, {3} failure(s) occurred'
                  .format(self.comment, self.test_count, self.success_count, self.failure_count))
        else:
            print('### {0} file(s) tested, {1} test(s) succeeded, {2} failure(s) occurred'
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

def dockerize(bindings_name, script_path, add_internal_argument=False, add_arguments=None, mount_m2_volume=False, mount_gnupg_volume=False):
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--docker', action='store_true', help='run this script in docker container')
    parser.add_argument('-D', '--no-docker', action='store_false', help='run this script normally [default]', dest='docker')
    parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose prints')
    parser.add_argument('-V', '--no-verbose', action='store_false', help='disable verbose prints [default]', dest='verbose')

    if add_internal_argument:
        parser.add_argument('-i', '--internal', action='store_true', help='handle all devices as if they were released')
        parser.add_argument('-I', '--no-internal', action='store_false', help='handle all devices according to their released marker [default]', dest='internal')

    if add_arguments != None:
        add_arguments(parser)

    args = parser.parse_args()

    global enable_verbose
    enable_verbose = args.verbose

    if args.docker:
        if shutil.which('docker') == None:
            print('error: docker is not installed')
            sys.exit(1)

        image_name = 'tinkerforge/builder-generators-debian:1.2.0'

        if len(subprocess.check_output(['docker', 'images', '-q', image_name]).strip()) == 0:
            print('error: docker image {0} is missing'.format(image_name))
            sys.exit(1)

        script_name = os.path.split(script_path)[-1]

        print('\033[01;35m>>> running {0} in docker container\033[0m'.format(script_name))

        generators_host_dir = os.path.dirname(os.path.realpath(__file__))
        generators_container_dir = generators_host_dir

        root_host_dir = os.path.realpath(os.path.join(generators_host_dir, '..'))
        root_container_dir = root_host_dir

        command = [
            'docker',
            'run',
            '--rm',
            '-it',
            '-v',
            '{0}:{1}'.format(root_host_dir, root_container_dir)
        ]

        if mount_m2_volume:
            m2_host_dir = os.path.join(generators_host_dir, '.m2')
            m2_container_dir = '/home/foobar/.m2'

            os.makedirs(m2_host_dir, exist_ok=True)

            command += [
                '-v',
                '{0}:{1}'.format(m2_host_dir, m2_container_dir)
            ]

        if mount_gnupg_volume:
            gnupg_host_dir = os.path.expanduser('~/.gnupg')
            gnupg_container_dir = '/home/foobar/.gnupg'

            command += [
                '-v',
                '{0}:{1}'.format(gnupg_host_dir, gnupg_container_dir)
            ]

        command += [
            '-u',
            '{0}:{1}'.format(os.getuid(), os.getgid()),
            image_name,
            'bash',
            '-c',
            'cd {0}; python3 -u {1} {2}'.format(os.path.join(generators_container_dir, bindings_name),
                                                script_name,
                                                shlex.join(sys.argv[1:] + ['--no-docker']))
        ]

        sys.exit(subprocess.call(command))

    return args
