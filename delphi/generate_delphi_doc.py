#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Delphi Documentation Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_delphi_doc.py: Generator for Delphi documentation

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
import delphi_common

device = None

def format_doc(packet):
    text = common.select_lang(packet.get_doc()[1])
    parameter = {
    'en': 'parameter',
    'de': 'Parameter'
    }
    parameters = {
    'en': 'parameters',
    'de': 'Parameter'
    }

    cls = device.get_category() + device.get_camel_case_name()
    for other_packet in device.get_packets():
        name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
        name = other_packet.get_camel_case_name()
        if other_packet.get_type() == 'callback':
            name_right = ':delphi:func:`On{1} <T{0}.On{1}>`'.format(cls, name)
        else:
            name_right = ':delphi:func:`{1} <T{0}.{1}>`'.format(cls, name)
        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", common.select_lang(parameter))
    text = text.replace(":word:`parameters`", common.select_lang(parameters))

    text = common.handle_rst_if(text, device)
    prefix = '{0}_{1}_'.format(device.get_category().upper(), 
                               device.get_upper_case_name())
    text = common.handle_constants(text, 
                                   prefix, 
                                   packet)
    text = common.handle_since_firmware(text, device, packet)

    return common.shift_right(text, 1)

def make_examples():
    def title_from_file(f):
        f = f.replace('Example', '')
        f = f.replace('.pas', '')
        return common.camel_case_to_space(f)

    return common.make_rst_examples(title_from_file, device, common.path_binding,
                                    'delphi', 'Example', '.pas', 'Delphi')

def make_methods(typ):
    methods = ''
    function = '.. delphi:function:: function T{0}.{1}({2}): {3}\n{4}'
    procedure = '.. delphi:function:: procedure T{0}.{1}({2})\n{3}'
    cls = device.get_category() + device.get_camel_case_name()
    for packet in device.get_packets('function'):
        if packet.get_doc()[0] != typ:
            continue

        ret_type = delphi_common.get_return_type(packet, True)
        name = packet.get_camel_case_name()
        params = delphi_common.make_parameter_list(packet, True)
        desc = format_doc(packet)
        if len(ret_type) > 0:
            method = function.format(cls, name, params, ret_type, desc)
        else:
            method = procedure.format(cls, name, params, desc)
        methods += method + '\n'

    return methods

def make_callbacks():
    cbs = ''
    cb = {
    'en': """.. delphi:function:: property T{0}.On{1}

 .. code-block:: delphi

  procedure({2}) of object;

{3}
""",
    'de': """.. delphi:function:: property T{0}.On{1}

 .. code-block:: delphi

  procedure({2}) of object;

{3}
"""
    }

    cls = device.get_category() + device.get_camel_case_name()
    for packet in device.get_packets('callback'):
        name = packet.get_camel_case_name()
        params = delphi_common.make_parameter_list(packet, True)
        desc = format_doc(packet)
        cbs += common.select_lang(cb).format(cls, name, params, desc)

    return cbs

def make_api():
    create_str = {
    'en': """
.. delphi:function:: constructor T{3}{1}.Create(const uid: string; ipcon: TIPConnection)

 Creates an object with the unique device ID *uid*:

 .. code-block:: delphi

    {4} := T{3}{1}.Create('YOUR_DEVICE_UID', ipcon);

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_{2}_delphi_examples>`).
""",
    'de': """
.. delphi:function:: constructor T{3}{1}.Create(const uid: string; ipcon: TIPConnection)

 Erzeugt ein Objekt mit der eindeutigen Geräte ID *uid*:

 .. code-block:: delphi

    {4} := T{3}{1}.Create('YOUR_DEVICE_UID', ipcon);

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_{2}_delphi_examples>`).
"""
    }

    c_str = {
    'en': """
.. _{1}_{2}_delphi_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive time critical or recurring data from
the device. The registration is done by assigning a procedure to an callback
property of the device object:

 .. code-block:: delphi

  procedure TExample.MyCallback(sender: T{3}{4}; const param: word);
  begin
    WriteLn(param);
  end;

  {1}.OnExample := {{$ifdef FPC}}@{{$endif}}example.MyCallback;

The available callback property and their type of parameters are described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{0}
""",
    'de': """
.. _{1}_{2}_delphi_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische oder
wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung erfolgt indem
eine Prozedur einem Callback Property des Geräte Objektes zugewiesen wird:

 .. code-block:: delphi

  procedure TExample.MyCallback(sender: T{3}{4}; const param: word);
  begin
    WriteLn(param);
  end;

  {5}.OnExample := {{$ifdef FPC}}@{{$endif}}example.MyCallback;

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

Since Delphi does not support multiple return values directly, we use the
``out`` keyword to return multiple values from a function.

All functions and procedures listed below are thread-safe.

{1}

{2}
""",
    'de': """
{0}
API
---

Da Delphi nicht mehrere Rückgabewerte direkt unterstützt, wird das ``out``
Keyword genutzt um mehrere Werte von einer Funktion zurückzugeben.

Alle folgend aufgelisteten Funktionen und Prozeduren sind Thread-sicher.

{1}

{2}
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

    ref = '.. _{0}_{1}_delphi_api:\n'.format(device.get_underscore_name(),
                                             device.get_category().lower())

    api_desc = ''
    if 'api' in device.com:
        api_desc = common.select_lang(device.com['api'])

    return common.select_lang(api).format(ref, api_desc, api_str)

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)
    file_name = '{0}_{1}_Delphi'.format(device.get_camel_case_name(),
                                        device.get_category())
    title = {
    'en': 'Delphi bindings',
    'de': 'Delphi Bindings'
    }
    directory = os.path.join(directory, 'doc', common.lang)
    f = file('{0}/{1}.rst'.format(directory, file_name), "w")
    f.write(common.make_rst_header(device, 'delphi', 'Delphi'))
    f.write(common.make_rst_summary(device, common.select_lang(title)))
    f.write(make_examples())
    f.write(make_api())

if __name__ == "__main__":
    for lang in ['en', 'de']:
        print("=== Generating %s ===" % lang)
        common.generate(os.getcwd(), lang, make_files, common.prepare_doc, True)
