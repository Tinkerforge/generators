#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Documentation Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2013 Olaf Lüke <olaf@tinkerforge.com>

generator_python_doc.py: Generator for Python documentation

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
import python_common

device = None

def type_to_pytype(element):
    type_dict = {
        'int8': 'int',
        'uint8': 'int',
        'int16': 'int',
        'uint16': 'int',
        'int32': 'int',
        'uint32': 'int',
        'int64': 'int',
        'uint64': 'int',
        'bool': 'bool',
        'char': 'chr',
        'string': 'str',
        'float': 'float'
    }

    t = type_dict[element.get_type()]
    
    if element.get_cardinality() == 1 or t == 'str':
        return t

    return '[' + ', '.join([t]*element.get_cardinality()) + ']'

def format_doc(packet):
    text = common.select_lang(packet.get_doc()[1])
    cls = device.get_camel_case_name()
    for other_packet in device.get_packets():
        name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
        if other_packet.get_type() == 'callback':
            name_upper = other_packet.get_upper_case_name()
            name_right = ':py:attr:`CALLBACK_{1} <{0}.CALLBACK_{1}>`'.format(cls, name_upper)
        else:
            name_right = ':py:func:`{1}() <{0}.{1}>`'.format(cls, other_packet.get_underscore_name())
        text = text.replace(name_false, name_right)

    text = common.handle_rst_word(text)
    text = common.handle_rst_if(text, device)

    prefix = device.get_category() + device.get_camel_case_name() + '.'
    if packet.get_underscore_name() == 'set_response_expected':
        text += common.format_function_id_constants(prefix, device)
    else:
        text += common.format_constants(prefix, packet)

    text += common.format_since_firmware(device, packet)

    return common.shift_right(text, 1)

def make_examples():
    def title_from_file(f):
        f = f.replace('example_', '')
        f = f.replace('.py', '')
        s = ''
        for l in f.split('_'):
            s += l[0].upper() + l[1:] + ' '
        return s[:-1]

    return common.make_rst_examples(title_from_file, device, common.path_binding,
                                    'python', 'example_', '.py', 'Python')

def make_parameter_desc(packet, io):
    desc = '\n'
    param = ' :param {0}: {1}\n'
    for element in packet.get_elements(io):
        t = type_to_pytype(element)
        desc += param.format(element.get_underscore_name(), t)

    return desc

def make_return_desc(packet):
    ret = ' :rtype: {0}\n'
    ret_list = []
    for element in packet.get_elements('out'):
        ret_list.append(type_to_pytype(element))
    if len(ret_list) == 0:
        return ret.format(None)
    elif len(ret_list) == 1:
        return ret.format(ret_list[0])
    
    return ret.format('(' + ', '.join(ret_list) + ')')

def make_object_desc(packet):
    if len(packet.get_elements('out')) < 2:
        return ''

    desc = {
    'en': """
 The returned namedtuple has the variables {0}.
""",
    'de': """
 Das zurückgegebene namedtuple enthält die Variablen {0}.
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
    func_start = '.. py:function:: '
    cls = device.get_camel_case_name()
    for packet in device.get_packets('function'):
        if packet.get_doc()[0] != typ:
            continue
        name = packet.get_underscore_name()
        params = python_common.make_parameter_list(packet)
        pd = make_parameter_desc(packet, 'in')
        r = make_return_desc(packet)
        d = format_doc(packet)
        obj_desc = make_object_desc(packet)
        desc = '{0}{1}{2}{3}'.format(pd, r, d, obj_desc)
        func = '{0}{1}.{2}({3})\n{4}'.format(func_start, 
                                             cls, 
                                             name, 
                                             params, 
                                             desc)
        methods += func + '\n'

    return methods 

def make_callbacks():
    cbs = ''
    func_start = '.. py:attribute:: '
    cls = device.get_camel_case_name()
    for packet in device.get_packets('callback'):
        param_desc = make_parameter_desc(packet, 'out')
        desc = format_doc(packet)

        func = '{0}{1}.CALLBACK_{2}\n{3}\n{4}'.format(func_start,
                                                      cls,
                                                      packet.get_upper_case_name(),
                                                      param_desc,
                                                      desc)
        cbs += func + '\n'

    return cbs

def make_api():
    create_str = {
    'en': """
.. py:function:: {1}(uid, ipcon)

 :param uid: string
 :param ipcon: IPConnection

 Creates an object with the unique device ID ``uid``:

 .. code-block:: python

    {0} = {1}("YOUR_DEVICE_UID", ipcon)

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_{2}_python_examples>`).
""",
    'de': """
.. py:function:: {1}(uid, ipcon)

 :param uid: string
 :param ipcon: IPConnection

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: python

    {0} = {1}("YOUR_DEVICE_UID", ipcon)

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_{2}_python_examples>`).
"""
    }

    register_str = {
    'en': """
.. py:function:: {1}.register_callback(id, callback)

 :param id: int
 :param callback: callable
 :rtype: None

 Registers a callback with ID *id* to the function *callback*. The available
 IDs with corresponding function signatures are listed 
 :ref:`below <{0}_{2}_python_callbacks>`.
""",
    'de': """
.. py:function:: {1}.register_callback(id, callback)

 :param id: int
 :param callback: callable
 :rtype: None

 Registriert einen Callback mit der ID *id* mit der Funktion *callback*. Die
 verfügbaren IDs mit den zugehörigen Funktionssignaturen sind
 :ref:`unten <{0}_{2}_python_callbacks>` zu finden.
"""
    }

    c_str = {
    'en': """
.. _{1}_{2}_python_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive
time critical or recurring data from the device. The registration is done
with the :py:func:`register_callback() <{3}.register_callback>` function of
the device object. The first parameter is the callback ID and the second
parameter the callback function:

.. code-block:: python

    def my_callback(param):
        print(param)

    {1}.register_callback({3}.CALLBACK_EXAMPLE, my_callback)

The available constants with inherent number and type of parameters are 
described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{0}
""",
    'de': """
.. _{1}_{2}_python_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit der Funktion :py:func:`register_callback() <{3}.register_callback>` des
Geräte Objektes durchgeführt werden. Der erste Parameter ist die Callback ID
und der zweite Parameter die Callback-Funktion:

.. code-block:: python

    def my_callback(param):
        print(param)

    {1}.register_callback({3}.CALLBACK_EXAMPLE, my_callback)

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

Alle folgend aufgelisteten Funktionen sind Thread-sicher.

{1}

{2}
"""
    }

    const_str = {
    'en' : """
Constants
^^^^^^^^^

.. py:attribute:: {0}.DEVICE_IDENTIFIER

 This constant is used to identify a {3} {4}.

 The :py:func:`get_identity() <{3}.get_identity>` function and the
 :py:attr:`CALLBACK_ENUMERATE <IPConnection.CALLBACK_ENUMERATE>`
 callback of the IP Connection have a ``device_identifier`` parameter to specify
 the Brick's or Bricklet's type.
""",
    'de' : """
Konstanten
^^^^^^^^^^

.. py:attribute:: {0}.DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {3} {4} zu identifizieren.

 Die :py:func:`get_identity() <{3}.get_identity>` Funktion und der
 :py:attr:`CALLBACK_ENUMERATE <IPConnection.CALLBACK_ENUMERATE>`
 Callback der IP Connection haben ein ``device_identifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.
"""
    }

    cre = common.select_lang(create_str).format(device.get_underscore_name(),
                                                device.get_camel_case_name(),
                                                device.get_category().lower())
    reg = common.select_lang(register_str).format(device.get_underscore_name(),
                                                  device.get_camel_case_name(),
                                                  device.get_category().lower())

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
                                                    device.get_camel_case_name())

    article = 'ein'
    if device.get_category() == 'Brick':
        article = 'einen'
    api_str += common.select_lang(const_str).format(device.get_camel_case_name(),
                                                    device.get_category(),
                                                    article,
                                                    device.get_camel_case_name(),
                                                    device.get_category())

    ref = '.. _{0}_{1}_python_api:\n'.format(device.get_underscore_name(),
                                             device.get_category().lower())

    api_desc = ''
    if 'api' in device.raw_data:
        api_desc = common.select_lang(device.raw_data['api'])

    return common.select_lang(api).format(ref, api_desc, api_str)

def make_files(device_, directory):
    global device
    device = device_
    file_name = '{0}_{1}_Python'.format(device.get_camel_case_name(), device.get_category())
    title = {
    'en': 'Python bindings',
    'de': 'Python Bindings'
    }
    directory = os.path.join(directory, 'doc', common.lang)
    f = file('{0}/{1}.rst'.format(directory, file_name), "w")
    f.write(common.make_rst_header(device, 'python', 'Python'))
    f.write(common.make_rst_summary(device, common.select_lang(title), 'python'))
    f.write(make_examples())
    f.write(make_api())

class PythonDocGenerator(common.Generator):
    def prepare(self):
        common.recreate_directory(os.path.join(self.get_bindings_root_directory(), 'doc', self.get_language()))

    def generate(self, device):
        make_files(device, self.get_bindings_root_directory())

    def finish(self):
        pass

def generate(path, lang):
    common.generate(path, lang, PythonDocGenerator, True)

if __name__ == "__main__":
    for lang in ['en', 'de']:
        print("=== Generating %s ===" % lang)
        generate(os.getcwd(), lang)
