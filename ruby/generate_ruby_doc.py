#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ruby Documentation Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_ruby_doc.py: Generator for Ruby documentation

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
import ruby_common

device = None

def format_doc(packet):
    text = common.select_lang(packet.get_doc()[1])

    cls = device.get_ruby_class_name()
    for other_packet in device.get_packets():
        name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
        if other_packet.get_type() == 'callback':
            name_upper = other_packet.get_upper_case_name()
            name_right = ':rb:attr:`::CALLBACK_{1} <{0}::CALLBACK_{1}>`'.format(cls, name_upper)
        else:
            name_right = ':rb:func:`#{1} <{0}#{1}>`'.format(cls, other_packet.get_underscore_name())
        text = text.replace(name_false, name_right)

    text = common.handle_rst_word(text)
    text = common.handle_rst_if(text, device)

    prefix = cls + '::'
    if packet.get_underscore_name() == 'set_response_expected':
        text += common.format_function_id_constants(prefix, device)
    else:
        text += common.format_constants(prefix, packet)

    text += common.format_since_firmware(device, packet)

    return common.shift_right(text, 1)

def make_examples(generator):
    def title_from_file_name(file_name):
        file_name = file_name.replace('example_', '').replace('.rb', '')
        return common.underscore_to_space(file_name)

    return common.make_rst_examples(title_from_file_name, device, generator.get_bindings_root_directory(),
                                    'ruby', 'example_', '.rb', 'Ruby')

def make_parameter_desc(packet, io):
    desc = '\n'
    param = ' :param {0}: {1}\n'
    for element in packet.get_elements(io):
        desc += param.format(element.get_underscore_name(), element.get_ruby_type())

    return desc

def make_return_desc(packet):
    ret = ' -> {0}'
    ret_list = []
    for element in packet.get_elements('out'):
        ret_list.append(element.get_ruby_type())
    if len(ret_list) == 0:
        return ret.format('nil')
    elif len(ret_list) == 1:
        return ret.format(ret_list[0])

    return ret.format('[' + ', '.join(ret_list) + ']')

def make_object_desc(packet):
    if len(packet.get_elements('out')) < 2:
        return ''

    desc = {
    'en': """
 The returned tuple has the values {0}.
""",
    'de': """
 Das zurückgegebene Tupel enthält die Werte {0}.
"""
    }

    and_ = {
    'en': ' and ',
    'de': ' und '
    }

    var = []
    for element in packet.get_elements('out'):
        var.append('``{0}``'.format(element.get_underscore_name()))

    if len(var) == 1:
        return common.select_lang(desc).format(var[0])

    if len(var) == 2:
        return common.select_lang(desc).format(var[0] + common.select_lang(and_) + var[1])

    return common.select_lang(desc).format(', '.join(var[:-1]) + common.select_lang(and_) + var[-1])

def make_methods(typ):
    methods = ''
    func_start = '.. rb:function:: '
    cls = device.get_ruby_class_name()
    for packet in device.get_packets('function'):
        if packet.get_doc()[0] != typ:
            continue
        name = packet.get_underscore_name()
        params = ruby_common.make_parameter_list(packet)
        if len(params) > 0:
            params = '(' + params + ')'
        pd = make_parameter_desc(packet, 'in')
        r = make_return_desc(packet)
        d = format_doc(packet)
        obj_desc = make_object_desc(packet)
        desc = '{0}{1}{2}'.format(pd, d, obj_desc)
        func = '{0}{1}#{2}{3}{5}\n{4}'.format(func_start,
                                              cls,
                                              name,
                                              params,
                                              desc,
                                              r)
        methods += func + '\n'

    return methods

def make_callbacks():
    cbs = ''
    func_start = '.. rb:attribute:: '
    cls = device.get_ruby_class_name()
    for packet in device.get_packets('callback'):
        param_desc = make_parameter_desc(packet, 'out')
        desc = format_doc(packet)

        func = '{0}{1}::CALLBACK_{2}\n{3}\n{4}'.format(func_start,
                                                       cls,
                                                       packet.get_upper_case_name(),
                                                       param_desc,
                                                       desc)
        cbs += func + '\n'

    return cbs

def make_api():
    create_str = {
    'en': """
.. rb:function:: {3}{1}::new(uid, ipcon) -> {0}

 :param uid: str
 :param ipcon: IPConnection

 Creates an object with the unique device ID ``uid``:

 .. code-block:: ruby

    {0} = {3}{1}.new 'YOUR_DEVICE_UID', ipcon

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_{2}_ruby_examples>`).
""",
    'de': """
.. rb:function:: {3}{1}::new(uid, ipcon) -> {0}

 :param uid: str
 :param ipcon: IPConnection

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: ruby

    {0} = {3}{1}.new 'YOUR_DEVICE_UID', ipcon

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_{2}_ruby_examples>`).
"""
    }

    register_str = {
    'en': """
.. rb:function:: {3}{1}#register_callback(id) {{ |param [, ...]| block }} -> nil

 :param id: int

 Registers a callback with ID *id* to the given block. The available
 IDs with corresponding function signatures are listed
 :ref:`below <{0}_{2}_ruby_callbacks>`.
""",
    'de': """
.. rb:function:: {3}{1}#register_callback(id) {{ |param [, ...]| block }} -> nil

 :param id: int

 Registriert einen Callback mit der ID *id* in den gegebenen Block. Die verfügbaren
 IDs mit den zugehörigen Funktionssignaturen sind :ref:`unten <{0}_{2}_ruby_callbacks>`
 zu finden.
"""
    }

    c_str = {
    'en': """
.. _{1}_{2}_ruby_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive time critical or recurring data from
the device. The registration is done with the
:rb:func:`#register_callback <{4}{3}#register_callback>` function of
the device object. The first parameter is the callback ID and the second
parameter is a block:

.. code-block:: ruby

    {1}.register_callback {4}{3}::CALLBACK_EXAMPLE, do |param|
      puts "#{{param}}"
    end

The available constants with inherent number and type of parameters are
described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{0}
""",
    'de': """
.. _{1}_{2}_ruby_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit der Funktion :rb:func:`#register_callback <{4}{3}#register_callback>` des
Geräte Objektes durchgeführt werden. Der erste Parameter ist der Callback ID
und der zweite Parameter der Block:

.. code-block:: ruby

    {1}.register_callback {4}{3}::CALLBACK_EXAMPLE, do |param|
      puts "#{{param}}"
    end

Die verfügbaren Konstanten mit der dazugehörigen Parameteranzahl und -typen werden
weiter unten beschrieben.

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

All methods listed below are thread-safe.

{1}

{2}
""",
    'de': """
{0}
API
---

Alle folgend aufgelisteten Methoden sind Thread-sicher.

{1}

{2}
"""
    }

    const_str = {
    'en' : """
Constants
^^^^^^^^^

.. rb:attribute:: {1}{0}::DEVICE_IDENTIFIER

 This constant is used to identify a {3} {4}.

 The :rb:func:`#get_identity() <{4}{3}#get_identity>` function and the
 :rb:attr:`::CALLBACK_ENUMERATE <IPConnection::CALLBACK_ENUMERATE>`
 callback of the IP Connection have a ``device_identifier`` parameter to specify
 the Brick's or Bricklet's type.
""",
    'de' : """
Konstanten
^^^^^^^^^^

.. rb:attribute:: {1}{0}::DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {3} {4} zu identifizieren.

 Die :rb:func:`#get_identity() <{4}{3}#get_identity>` Funktion und der
 :rb:attr:`::CALLBACK_ENUMERATE <IPConnection::CALLBACK_ENUMERATE>`
 Callback der IP Connection haben ein ``device_identifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.
"""
    }

    cre = common.select_lang(create_str).format(device.get_underscore_name(),
                                                device.get_camel_case_name(),
                                                device.get_category().lower(),
                                                device.get_category())
    reg = common.select_lang(register_str).format(device.get_underscore_name(),
                                                  device.get_camel_case_name(),
                                                  device.get_category().lower(),
                                                  device.get_category())

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
        api_str += common.select_lang(common.ccf_str).format(reg, ccf)
        api_str += common.select_lang(c_str).format(c, device.get_underscore_name(),
                                                    device.get_category().lower(),
                                                    device.get_camel_case_name(),
                                                    device.get_category())

    article = 'ein'
    if device.get_category() == 'Brick':
        article = 'einen'
    api_str += common.select_lang(const_str).format(device.get_camel_case_name(),
                                                    device.get_category(),
                                                    article,
                                                    device.get_camel_case_name(),
                                                    device.get_category())

    ref = '.. _{0}_{1}_ruby_api:\n'.format(device.get_underscore_name(),
                                           device.get_category().lower())

    return common.select_lang(api).format(ref, device.get_api_doc(), api_str)

class RubyDocGenerator(common.DocGenerator):
    def get_device_class(self):
        return ruby_common.RubyDevice

    def get_element_class(self):
        return ruby_common.RubyElement

    def generate(self, device_):
        global device
        device = device_

        title = { 'en': 'Ruby bindings', 'de': 'Ruby Bindings' }
        file_name = '{0}_{1}_Ruby.rst'.format(device.get_camel_case_name(), device.get_category())

        rst = open(os.path.join(self.get_bindings_root_directory(), 'doc', common.lang, file_name), 'wb')
        rst.write(common.make_rst_header(device, 'ruby', 'Ruby'))
        rst.write(common.make_rst_summary(device, common.select_lang(title), 'ruby'))
        rst.write(make_examples(self))
        rst.write(make_api())
        rst.close()

def generate(bindings_root_directory, lang):
    common.generate(bindings_root_directory, lang, RubyDocGenerator, True)

if __name__ == "__main__":
    for lang in ['en', 'de']:
        print("=== Generating %s ===" % lang)
        generate(os.getcwd(), lang)
