#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Visual Basic .NET Documentation Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_vbnet_doc.py: Generator for Visual Basic .NET documentation

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

device = None

def format_doc(packet):
    text = common.select_lang(packet.get_doc()[1])

    cls = device.get_category() + device.get_camel_case_name()
    for other_packet in device.get_packets():
        name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
        name = other_packet.get_camel_case_name()
        if other_packet.get_type() == 'callback':
            name_right = ':vbnet:func:`{1} <{0}.{1}>`'.format(cls, name)
        else:
            name_right = ':vbnet:func:`{1}() <{0}.{1}>`'.format(cls, name)
        text = text.replace(name_false, name_right)

    text = common.handle_rst_word(text)
    text = common.handle_rst_if(text, device)

    prefix = '{0}{1}.'.format(device.get_category(), device.get_camel_case_name())
    if packet.get_underscore_name() == 'set_response_expected':
        text += common.format_function_id_constants(prefix, device)
    else:
        text += common.format_constants(prefix, packet, char_format='"{0}"C')

    text += common.format_since_firmware(device, packet)

    return common.shift_right(text, 1)

def get_vbnet_type(element):
    types = {
        'int8'   : 'Short',
        'uint8'  : 'Byte',
        'int16'  : 'Short',
        'uint16' : 'Integer',
        'int32'  : 'Integer',
        'uint32' : 'Long',
        'int64'  : 'Long',
        'uint64' : 'Long',
        'float'  : 'Single',
        'bool'   : 'Boolean',
        'string' : 'String',
        'char'   : 'Char',
    }

    return types[element[1]]

def get_return_type(packet):
    elements = packet.get_elements('out')

    if len(elements) == 1:
        vbnet_type = get_vbnet_type(elements[0])

        if elements[0][2] > 1 and elements[0][1] != 'string':
            vbnet_type += '[]'

        return vbnet_type
    else:
        return ''

def make_parameter_list(packet):
    param = []
    if len(packet.get_elements('out')) > 1 or packet.get_type() == 'callback':
        for element in packet.get_elements():
            vbnet_type = get_vbnet_type(element)

            if element[3] == 'in' or packet.get_type() == 'callback':
                modifier = 'ByVal '
            else:
                modifier = 'ByRef '

            name = common.underscore_to_headless_camel_case(element[0])

            if element[2] > 1 and element[1] != 'string':
                name += '[]'

            param.append('{0}{1} As {2}'.format(modifier, name, vbnet_type))
    else:
        for element in packet.get_elements('in'):
            vbnet_type = get_vbnet_type(element)
            name = common.underscore_to_headless_camel_case(element[0])

            if element[2] > 1 and element[1] != 'string':
                name += '[]'

            param.append('ByVal {0} As {1}'.format(name, vbnet_type))
    return ', '.join(param)

def make_examples():
    def title_from_file(f):
        f = f.replace('Example', '')
        f = f.replace('.vb', '')
        return common.camel_case_to_space(f)

    return common.make_rst_examples(title_from_file, device, common.path_binding,
                                    'vbnet', 'Example', '.vb', 'VBNET')

def make_methods(typ):
    methods = ''
    function = '.. vbnet:function:: Function {0}.{1}({2}) As {3}\n{4}'
    sub = '.. vbnet:function:: Sub {0}.{1}({2})\n{3}'
    cls = device.get_category() + device.get_camel_case_name()
    for packet in device.get_packets('function'):
        if packet.get_doc()[0] != typ:
            continue

        ret_type = get_return_type(packet)
        name = packet.get_camel_case_name()
        params = make_parameter_list(packet)
        desc = format_doc(packet)
        if len(ret_type) > 0:
            method = function.format(cls, name, params, ret_type, desc)
        else:
            method = sub.format(cls, name, params, desc)
        methods += method + '\n'

    return methods

def make_callbacks_x():
    cbs = ''
    cb = {
    'en': """.. vbnet:function:: event {0}.On{1}

 .. code-block:: vbnet

  procedure({2}) of object;

{3}
""",
    'de': """.. vbnet:function:: event {0}.On{1}

 .. code-block:: vbnet

  procedure({2}) of object;

{3}
"""
    }

    cls = device.get_category() + device.get_camel_case_name()
    for packet in device.get_packets('callback'):
        name = packet.get_camel_case_name()
        params = make_parameter_list(packet)
        desc = format_doc(packet)
        cbs += common.select_lang(cb).format(cls, name, params, desc)

    return cbs

def make_callbacks():
    cb = {
    'en': """
.. vbnet:function:: Event {0}.{1}(ByVal sender As {0}{2})

{3}
""",
    'de': """
.. vbnet:function:: Event {0}.{1}(ByVal sender As {0}{2})

{3}
"""
    }

    cbs = ''
    for packet in device.get_packets('callback'):
        desc = format_doc(packet)
        params = make_parameter_list(packet)
        if len(params) > 0:
            params = ', ' + params

        cbs += common.select_lang(cb).format(device.get_category() + device.get_camel_case_name(),
                                             packet.get_camel_case_name(),
                                             params,
                                             desc)

    return cbs

def make_api():
    create_str = {
    'en': """
.. vbnet:function:: Class {3}{1}(ByVal uid As String, ByVal ipcon As IPConnection)

 Creates an object with the unique device ID ``uid``:

 .. code-block:: vbnet

    Dim {4} As New {3}{1}("YOUR_DEVICE_UID", ipcon)

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_{2}_vbnet_examples>`).
""",
    'de': """
.. vbnet:function:: Class {3}{1}(ByVal uid As String, ByVal ipcon As IPConnection)

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: vbnet

    Dim {4} As New {3}{1}("YOUR_DEVICE_UID", ipcon)

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_{2}_vbnet_examples>`).
"""
    }

    c_str = {
    'en': """
.. _{1}_{2}_vbnet_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive time critical or recurring data from
the device. The registration is done by assigning a procedure to an callback
property of the device object:

 .. code-block:: vbnet

    Sub Callback(ByVal sender As {3}{4}, ByVal value As Short)
        Console.WriteLine("Value: {{0}}", value)
    End Sub

    AddHandler {5}.Example, AddressOf Callback

The available callback property and their type of parameters are described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{0}
""",
    'de': """
.. _{1}_{2}_vbnet_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische oder
wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung erfolgt indem
eine Prozedur einem Callback Property des Geräte Objektes zugewiesen wird:

 .. code-block:: vbnet

    Sub Callback(ByVal sender As {3}{4}, ByVal value As Short)
        Console.WriteLine("Value: {{0}}", value)
    End Sub

    AddHandler {5}.Example, AddressOf Callback

Die verfügbaren Callback Properties und ihre Parametertypen werden weiter
unten beschrieben.

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

Since Visual Basic .NET does not support multiple return values directly, we
use the ``ByRef`` keyword to return multiple values from a function.

All functions and procedures listed below are thread-safe.

{1}

{2}
""",
    'de': """
{0}
API
---

Da Visual Basic .NET nicht mehrere Rückgabewerte direkt unterstützt, wird das
``ByRef`` Schlüsselwort genutzt um mehrere Werte von einer Funktion zurückzugeben.

Alle folgend aufgelisteten Funktionen und Prozeduren sind Thread-sicher.

{1}

{2}
"""
    }

    const_str = {
    'en' : """
Constants
^^^^^^^^^

.. vbnet:attribute:: Const {1}{0}.DEVICE_IDENTIFIER

 This constant is used to identify a {0} {1}.

 The :vbnet:func:`GetIdentity() <{1}{0}.GetIdentity>` function and the
 :vbnet:func:`EnumerateCallback <IPConnection.EnumerateCallback>`
 callback of the IP Connection have a ``deviceIdentifier`` parameter to specify
 the Brick's or Bricklet's type.
""",
    'de' : """
Konstanten
^^^^^^^^^^

.. vbnet:attribute:: Const {1}{0}.DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {0} {1} zu identifizieren.

 Die :vbnet:func:`GetIdentity() <{1}{0}.GetIdentity>` Funktion und der
 :vbnet:func:`EnumerateCallback <IPConnection.EnumerateCallback>`
 Callback der IP Connection haben ein ``deviceIdentifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.
"""
    }

    cre = common.select_lang(create_str).format(device.get_underscore_name(),
                                                device.get_camel_case_name(),
                                                device.get_category().lower(),
                                                device.get_category(),
                                                device.get_headless_camel_case_name())

    bf = make_methods('bf')
    af = make_methods('af')
    ccf = make_methods('ccf')
    c = make_callbacks()
    api_str = ''
    if bf:
        api_str += common.select_lang(common.bf_str).format(cre, bf)
    if af:
        api_str += common.select_lang(common.af_str).format(af)
    if c:
        api_str += common.select_lang(common.ccf_str).format(ccf, '')
        api_str += common.select_lang(c_str).format(c, device.get_underscore_name(),
                                                    device.get_category().lower(),
                                                    device.get_category(),
                                                    device.get_camel_case_name(),
                                                    device.get_headless_camel_case_name())

    article = 'ein'
    if device.get_category() == 'Brick':
        article = 'einen'
    api_str += common.select_lang(const_str).format(device.get_camel_case_name(),
                                                    device.get_category(),
                                                    article)

    ref = '.. _{0}_{1}_vbnet_api:\n'.format(device.get_underscore_name(),
                                             device.get_category().lower())

    api_desc = ''
    if 'api' in device.com:
        api_desc = common.select_lang(device.com['api'])

    return common.select_lang(api).format(ref, api_desc, api_str)

def make_files(device_, directory):
    global device
    device = device_
    file_name = '{0}_{1}_VBNET'.format(device.get_camel_case_name(),
                                        device.get_category())
    title = {
    'en': 'Visual Basic .NET bindings',
    'de': 'Visual Basic .NET Bindings'
    }
    directory = os.path.join(directory, 'doc', common.lang)
    f = file('{0}/{1}.rst'.format(directory, file_name), "w")
    f.write(common.make_rst_header(device, 'vbnet', 'Visual Basic .NET'))
    f.write(common.make_rst_summary(device, common.select_lang(title)))
    f.write(make_examples())
    f.write(make_api())

def generate(path, lang):
    common.generate(path, lang, make_files, common.prepare_doc, None, True)

if __name__ == "__main__":
    for lang in ['en', 'de']:
        print("=== Generating %s ===" % lang)
        generate(os.getcwd(), lang)
