#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Documentation Generator
Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2013 Olaf Lüke <olaf@tinkerforge.com>

generate_python_doc.py: Generator for Python documentation

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

class PythonDocDevice(python_common.PythonDevice):
    def replace_python_function_links(self, text):
        cls = self.get_camel_case_name()
        for other_packet in self.get_packets():
            name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
            if other_packet.get_type() == 'callback':
                name_upper = other_packet.get_upper_case_name()
                name_right = ':py:attr:`CALLBACK_{1} <{0}.CALLBACK_{1}>`'.format(cls, name_upper)
            else:
                name_right = ':py:func:`{1}() <{0}.{1}>`'.format(cls, other_packet.get_underscore_name())

            text = text.replace(name_false, name_right)

        return text

    def get_python_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('example_', '').replace('.py', '')
            return common.underscore_to_space(filename)

        return common.make_rst_examples(title_from_filename, self)

    def get_python_methods(self, type):
        methods = []
        func_start = '.. py:function:: '
        cls = self.get_camel_case_name()
        for packet in self.get_packets('function'):
            if packet.get_doc()[0] != type:
                continue
            name = packet.get_underscore_name()
            params = packet.get_python_parameter_list()
            pd = packet.get_python_parameter_desc('in')
            r = packet.get_python_return_desc()
            d = packet.get_python_formatted_doc()
            obj_desc = packet.get_python_object_desc()
            desc = '{0}{1}{2}{3}'.format(pd, r, d, obj_desc)
            func = '{0}{1}.{2}({3})\n{4}\n'.format(func_start,
                                                   cls,
                                                   name,
                                                   params,
                                                   desc)
            methods.append(func)

        return ''.join(methods)

    def get_python_callbacks(self):
        cbs = ''
        func_start = '.. py:attribute:: '
        cls = self.get_camel_case_name()
        for packet in self.get_packets('callback'):
            param_desc = packet.get_python_parameter_desc('out')
            desc = packet.get_python_formatted_doc()

            func = '{0}{1}.CALLBACK_{2}\n{3}\n{4}'.format(func_start,
                                                          cls,
                                                          packet.get_upper_case_name(),
                                                          param_desc,
                                                          desc)
            cbs += func + '\n'

        return cbs

    def get_python_api(self):
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

Die verfügbaren IDs mit der dazugehörigen Parameteranzahl und -typen werden
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

Generally, every method of the Python bindings can throw an
``tinkerforge.ip_connection.Error`` exception that has a ``value`` and a
``description`` property. ``value`` can have different values:

* Error.TIMEOUT = -1
* Error.ALREADY_CONNECTED = -7
* Error.NOT_CONNECTED = -8
* Error.INVALID_PARAMETER = -9
* Error.NOT_SUPPORTED = -10
* Error.UNKNOWN_ERROR_CODE = -11

All methods listed below are thread-safe.

{1}

{2}
""",
        'de': """
{0}
API
---

Prinzipiell kann jede Funktion der Python Bindings
``tinkerforge.ip_connection.Error`` Exception werfen, welche ein ``value`` und
eine ``description`` Property hat. ``value`` kann verschiende Werte haben:

* Error.TIMEOUT = -1
* Error.ALREADY_CONNECTED = -7
* Error.NOT_CONNECTED = -8
* Error.INVALID_PARAMETER = -9
* Error.NOT_SUPPORTED = -10
* Error.UNKNOWN_ERROR_CODE = -11

Alle folgend aufgelisteten Funktionen sind Thread-sicher.

{1}

{2}
"""
        }

        const_str = {
        'en' : """
.. _{5}_{6}_python_constants:

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
.. _{5}_{6}_python_constants:

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

        cre = common.select_lang(create_str).format(self.get_underscore_name(),
                                                    self.get_camel_case_name(),
                                                    self.get_category().lower())
        reg = common.select_lang(register_str).format(self.get_underscore_name(),
                                                      self.get_camel_case_name(),
                                                      self.get_category().lower())

        bf = self.get_python_methods('bf')
        af = self.get_python_methods('af')
        ccf = self.get_python_methods('ccf')
        c = self.get_python_callbacks()
        api_str = ''
        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)
        if af:
            api_str += common.select_lang(common.af_str).format(af)
        if c:
            api_str += common.select_lang(common.ccf_str).format(reg, ccf)
            api_str += common.select_lang(c_str).format(c, self.get_underscore_name(),
                                                        self.get_category().lower(),
                                                        self.get_camel_case_name())

        article = 'ein'
        if self.get_category() == 'Brick':
            article = 'einen'
        api_str += common.select_lang(const_str).format(self.get_camel_case_name(),
                                                        self.get_category(),
                                                        article,
                                                        self.get_camel_case_name(),
                                                        self.get_category(),
                                                        self.get_underscore_name(),
                                                        self.get_category().lower())

        ref = '.. _{0}_{1}_python_api:\n'.format(self.get_underscore_name(),
                                                 self.get_category().lower())

        return common.select_lang(api).format(ref, self.replace_python_function_links(self.get_api_doc()), api_str)

    def get_python_doc(self):
        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += self.get_python_examples()
        doc += self.get_python_api()

        return doc

class PythonDocPacket(python_common.PythonPacket):
    def get_python_formatted_doc(self):
        text = common.select_lang(self.get_doc()[1])

        text = self.get_device().replace_python_function_links(text)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = self.get_device().get_camel_case_name() + '.'
        if self.get_underscore_name() == 'set_response_expected':
            text += common.format_function_id_constants(prefix, self.get_device())
        else:
            text += common.format_constants(prefix, self)

        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

    def get_python_parameter_desc(self, io):
        desc = '\n'
        param = ' :param {0}: {1}\n'
        for element in self.get_elements(io):
            t = element.get_python_type()
            desc += param.format(element.get_underscore_name(), t)

        return desc

    def get_python_return_desc(self):
        ret = ' :rtype: {0}\n'
        ret_list = []
        for element in self.get_elements('out'):
            ret_list.append(element.get_python_type())
        if len(ret_list) == 0:
            return ret.format(None)
        elif len(ret_list) == 1:
            return ret.format(ret_list[0])

        return ret.format('(' + ', '.join(ret_list) + ')')

    def get_python_object_desc(self):
        if len(self.get_elements('out')) < 2:
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
        for element in self.get_elements('out'):
            var.append('``{0}``'.format(element.get_underscore_name()))

        if len(var) == 1:
            return common.select_lang(desc).format(var[0])

        if len(var) == 2:
            return common.select_lang(desc).format(var[0] + common.select_lang(and_) + var[1])

        return common.select_lang(desc).format(', '.join(var[:-1]) + common.select_lang(and_) + var[-1])

class PythonDocGenerator(common.DocGenerator):
    def get_bindings_name(self):
        return 'python'

    def get_bindings_display_name(self):
        return 'Python'

    def get_doc_rst_filename_part(self):
        return 'Python'

    def get_doc_example_regex(self):
        return '^example_.*\.py$'

    def get_device_class(self):
        return PythonDocDevice

    def get_packet_class(self):
        return PythonDocPacket

    def get_element_class(self):
        return python_common.PythonElement

    def generate(self, device):
        rst = open(device.get_doc_rst_path(), 'wb')
        rst.write(device.get_python_doc())
        rst.close()

def generate(bindings_root_directory, language):
    common.generate(bindings_root_directory, language, PythonDocGenerator)

if __name__ == "__main__":
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
