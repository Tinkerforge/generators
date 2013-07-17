#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Shell Documentation Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2013 Olaf Lüke <olaf@tinkerforge.com>

generator_shell_doc.py: Generator for Shell documentation

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
import re

sys.path.append(os.path.split(os.getcwd())[0])
import common
import shell_common

device = None

def get_element_type(element):
    types = {
        'int8': 'integer',
        'uint8': 'unsigned integer',
        'int16': 'integer',
        'uint16': 'unsigned integer',
        'int32': 'integer',
        'uint32': 'unsigned integer',
        'int64': 'integer',
        'uint64': 'unsigned integer',
        'bool': 'bool',
        'char': 'character',
        'string': 'string',
        'float': 'float'
    }

    t = types[element[1]]

    if element[2] == 1 or element[1] == 'string':
        return t
    else:
        return '{0}[{1}]'.format(t, element[2])

def get_device_name(device):
    return device.get_underscore_name().replace('_', '-') + '-' + device.get_category().lower()

def format_doc(packet):
    text = common.select_lang(packet.get_doc()[1])
    cls = get_device_name(device)
    for other_packet in device.get_packets():
        name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
        name_right = ':sh:func:`{1} <{0} {1}>`'.format(cls, other_packet.get_underscore_name().replace('_', '-'))
        text = text.replace(name_false, name_right)

    text = common.handle_rst_word(text)
    text = common.handle_rst_if(text, device)

    text += common.format_since_firmware(device, packet)

    return common.shift_right(text, 1)

def make_examples():
    def title_from_file(f):
        f = f.replace('example_', '')
        f = f.replace('.sh', '')
        s = ''
        for l in f.split('_'):
            s += l[0].upper() + l[1:] + ' '
        return s[:-1]

    return common.make_rst_examples(title_from_file, device, common.path_binding,
                                    'shell', 'example_', '.sh', 'Shell', 'bash')

def make_parameter_desc(packet):
    desc = '\n'
    param = ' :param <{0}>: {1}\n'
    for element in packet.get_elements('in'):
        t = get_element_type(element)
        desc += param.format(element[0].replace('_', '-'), t)

    return desc

def make_return_desc(packet):
    nothing = {
    'en': 'no output',
    'de': 'keine Ausgabe'
    }
    elements = packet.get_elements('out')

    if len(elements) == 0:
        return '\n :noreturn: {0}\n'.format(common.select_lang(nothing))

    ret = '\n'
    for element in elements:
        t = get_element_type(element)
        ret += ' :returns {0}: {1}\n'.format(element[0].replace('_', '-'), t)

    return ret

def make_methods(typ):
    methods = ''
    func_start = '.. sh:function:: '
    cls = get_device_name(device)
    for packet in device.get_packets('function'):
        if packet.is_virtual():
            continue

        if packet.get_doc()[0] != typ:
            continue
        name = packet.get_underscore_name().replace('_', '-')
        params = shell_common.make_parameter_list(packet)
        pd = make_parameter_desc(packet)
        r = make_return_desc(packet)
        d = format_doc(packet)
        desc = '{0}{1}{2}'.format(pd, r, d)
        func = '{0}tinkerforge call {1} {2} {3} \n{4}'.format(func_start,
                                                              cls,
                                                              name,
                                                              params,
                                                              desc)
        methods += func + '\n'

    return methods

def make_callbacks():
    cbs = ''
    func_start = '.. sh:function:: '
    cls = get_device_name(device)
    for packet in device.get_packets('callback'):
        if packet.is_virtual():
            continue

        param_desc = make_return_desc(packet)
        desc = format_doc(packet)

        func = '{0} tinkerforge dispatch {1} {2}\n{3}\n{4}'.format(func_start,
                                                                   cls,
                                                                   packet.get_underscore_name().replace('_', '-'),
                                                                   param_desc,
                                                                   desc)
        cbs += func + '\n'

    return cbs

def make_api():
    c_str = {
    'en': """
.. _{1}_{2}_shell_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be used to receive time critical or recurring data from the
device:

.. code-block:: bash

    tinkerforge dispatch {3} example

The available callbacks are described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{0}
""",
    'de': """
.. _{1}_{2}_shell_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische oder wiederkehrende Daten
vom Gerät zu erhalten:

.. code-block:: bash

    tinkerforge dispatch {3} example

Die verfügbaren Callbacks werden weiter unten beschrieben.

.. note::
 Callbacks für wiederkehrende Ereignisse zu verwenden ist
 *immer* zu bevorzugen gegenüber der Verwendung von Abfragen.
 Es wird weniger USB-Bandbreite benutzt und die Latenz ist
 erheblich geringer, da es keine Paketumlaufzeit gibt.

{0}
"""
    }

    api = {
    'en': """
{0}
API
---

{1}

{2}
""",
    'de': """
{0}
API
---

{1}

{2}
"""
    }

    bf = make_methods('bf')
    af = make_methods('af')
    ccf = make_methods('ccf')
    c = make_callbacks()
    api_str = ''
    if bf:
        api_str += common.select_lang(common.bf_str).format('', bf)
    if af:
        api_str += common.select_lang(common.af_str).format(af)
    if c:
        api_str += common.select_lang(common.ccf_str).format('', ccf)
        api_str += common.select_lang(c_str).format(c, device.get_underscore_name(),
                                                    device.get_category().lower(),
                                                    get_device_name(device))

    ref = '.. _{0}_{1}_shell_api:\n'.format(device.get_underscore_name(),
                                            device.get_category().lower())

    api_desc = ''
    if 'api' in device.com:
        api_desc = common.select_lang(device.com['api'])

    return common.select_lang(api).format(ref, api_desc, api_str)

def make_files(device_, directory):
    global device
    device = device_
    file_name = '{0}_{1}_Shell'.format(device.get_camel_case_name(), device.get_category())
    title = {
    'en': 'Shell bindings',
    'de': 'Shell Bindings'
    }
    directory = os.path.join(directory, 'doc', common.lang)
    f = file('{0}/{1}.rst'.format(directory, file_name), "w")
    f.write(common.make_rst_header(device, 'shell', 'Shell'))
    f.write(common.make_rst_summary(device, common.select_lang(title)))
    f.write(make_examples())
    f.write(make_api())

if __name__ == "__main__":
    for lang in ['en', 'de']:
        print("=== Generating %s ===" % lang)
        common.generate(os.getcwd(), lang, make_files, common.prepare_doc, None, True)
