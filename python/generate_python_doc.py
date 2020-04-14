#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Documentation Generator
Copyright (C) 2012-2015, 2017-2020 Matthias Bolte <matthias@tinkerforge.com>
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

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os

sys.path.append(os.path.split(os.getcwd())[0])
import common
import python_common

class PythonDocDevice(python_common.PythonDevice):
    def specialize_python_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':py:attr:`CALLBACK_{1} <{0}.CALLBACK_{1}>`'.format(packet.get_device().get_python_class_name(),
                                                                           packet.get_name(skip=-2 if high_level else 0).upper)
            else:
                return ':py:func:`{1}() <{0}.{1}>`'.format(packet.get_device().get_python_class_name(),
                                                           packet.get_name(skip=-2 if high_level else 0).under)

        return self.specialize_doc_rst_links(text, specializer, prefix='py')

    def get_python_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('example_', '').replace('.py', '')
            return common.under_to_space(filename)

        return common.make_rst_examples(title_from_filename, self)

    def get_python_functions(self, type_):
        functions = []
        template = '.. py:function:: {0}.{1}({2})\n\n{3}{4}\n'
        cls = self.get_python_class_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type_:
                continue

            skip = -2 if packet.has_high_level() else 0
            name = packet.get_name(skip=skip).under
            params = packet.get_python_parameters(high_level=True)
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_python_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_python_name(index=index),
                                                     return_object='conditional',
                                                     no_out_value={'en': 'None', 'de': 'None'},
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_python_formatted_doc()

            functions.append(template.format(cls, name, params, meta_table, desc))

        return ''.join(functions)

    def get_python_callbacks(self):
        callbacks = []
        template = '.. py:attribute:: {0}.CALLBACK_{1}\n\n{2}{3}\n'
        cls = self.get_python_class_name()

        for packet in self.get_packets('callback'):
            skip = -2 if packet.has_high_level() else 0
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_python_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_python_name(index=index),
                                                     no_out_value={'en': 'no parameters', 'de': 'keine Parameter'},
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_python_formatted_doc()

            callbacks.append(template.format(cls, packet.get_name(skip=skip).upper, meta_table, desc))

        return ''.join(callbacks)

    def get_python_api(self):
        create_str = {
            'en': """
.. py:function:: {0}(uid, ipcon)

{2}

 Creates an object with the unique device ID ``uid``:

 .. code-block:: python

    {1} = {0}("YOUR_DEVICE_UID", ipcon)

 This object can then be used after the IP Connection is connected.
""",
            'de': """
.. py:function:: {0}(uid, ipcon)

{2}

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: python

    {1} = {0}("YOUR_DEVICE_UID", ipcon)

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist.
"""
        }

        register_str = {
            'en': """
.. py:function:: {2}{1}.register_callback(callback_id, function)

{3}

 Registers the given ``function`` with the given ``callback_id``.

 The available callback IDs with corresponding function signatures are listed
 :ref:`below <{0}_python_callbacks>`.
""",
            'de': """
.. py:function:: {2}{1}.register_callback(callback_id, function)

{3}

 Registriert die ``function`` für die gegebene ``callback_id``.

 Die verfügbaren Callback IDs mit den zugehörigen Funktionssignaturen sind
 :ref:`unten <{0}_python_callbacks>` zu finden.
"""
        }

        c_str = {
            'en': """
.. _{0}_python_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive
time critical or recurring data from the device. The registration is done
with the :py:func:`register_callback() <{1}.register_callback>` function of
the device object. The first parameter is the callback ID and the second
parameter the callback function:

.. code-block:: python

    def my_callback(param):
        print(param)

    {2}.register_callback({1}.CALLBACK_EXAMPLE, my_callback)

The available constants with inherent number and type of parameters are
described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{3}
""",
            'de': """
.. _{0}_python_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit der Funktion :py:func:`register_callback() <{1}.register_callback>` des
Geräte Objektes durchgeführt werden. Der erste Parameter ist die Callback ID
und der zweite Parameter die Callback-Funktion:

.. code-block:: python

    def my_callback(param):
        print(param)

    {2}.register_callback({1}.CALLBACK_EXAMPLE, my_callback)

Die verfügbaren IDs mit der dazugehörigen Parameteranzahl und -typen werden
weiter unten beschrieben.

.. note::
 Callbacks für wiederkehrende Ereignisse zu verwenden ist
 *immer* zu bevorzugen gegenüber der Verwendung von Abfragen.
 Es wird weniger USB-Bandbreite benutzt und die Latenz ist
 erheblich geringer, da es keine Paketumlaufzeit gibt.

{3}
"""
        }

        api = {
            'en': """
.. _{0}_python_api:

API
---

Generally, every function of the Python bindings can throw an
``tinkerforge.ip_connection.Error`` exception that has a ``value`` and a
``description`` property. ``value`` can have different values:

* Error.TIMEOUT = -1
* Error.NOT_ADDED = -6 (unused since Python bindings version 2.0.0)
* Error.ALREADY_CONNECTED = -7
* Error.NOT_CONNECTED = -8
* Error.INVALID_PARAMETER = -9
* Error.NOT_SUPPORTED = -10
* Error.UNKNOWN_ERROR_CODE = -11
* Error.STREAM_OUT_OF_SYNC = -12
* Error.INVALID_UID = -13
* Error.NON_ASCII_CHAR_IN_SECRET = -14
* Error.WRONG_DEVICE_TYPE = -15
* Error.DEVICE_REPLACED = -16
* Error.WRONG_RESPONSE_LENGTH = -17

All functions listed below are thread-safe.

{1}

{2}
""",
            'de': """
.. _{0}_python_api:

API
---

Prinzipiell kann jede Funktion der Python Bindings
``tinkerforge.ip_connection.Error`` Exception werfen, welche ein ``value`` und
eine ``description`` Property hat. ``value`` kann verschiende Werte haben:

* Error.TIMEOUT = -1
* Error.NOT_ADDED = -6 (seit Python Bindings Version 2.0.0 nicht mehr verwendet)
* Error.ALREADY_CONNECTED = -7
* Error.NOT_CONNECTED = -8
* Error.INVALID_PARAMETER = -9
* Error.NOT_SUPPORTED = -10
* Error.UNKNOWN_ERROR_CODE = -11
* Error.STREAM_OUT_OF_SYNC = -12
* Error.INVALID_UID = -13
* Error.NON_ASCII_CHAR_IN_SECRET = -14
* Error.WRONG_DEVICE_TYPE = -15
* Error.DEVICE_REPLACED = -16
* Error.WRONG_RESPONSE_LENGTH = -17

Alle folgend aufgelisteten Funktionen sind Thread-sicher.

{1}

{2}
"""
        }

        const_str = {
            'en': """
.. _{0}_python_constants:

Constants
^^^^^^^^^

.. py:attribute:: {1}.DEVICE_IDENTIFIER

 This constant is used to identify a {3}.

 The :py:func:`get_identity() <{1}.get_identity>` function and the
 :py:attr:`IPConnection.CALLBACK_ENUMERATE <IPConnection.CALLBACK_ENUMERATE>`
 callback of the IP Connection have a ``device_identifier`` parameter to specify
 the Brick's or Bricklet's type.

.. py:attribute:: {1}.DEVICE_DISPLAY_NAME

 This constant represents the human readable name of a {3}.
""",
            'de': """
.. _{0}_python_constants:

Konstanten
^^^^^^^^^^

.. py:attribute:: {1}.DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {3} zu identifizieren.

 Die :py:func:`get_identity() <{1}.get_identity>` Funktion und der
 :py:attr:`IPConnection.CALLBACK_ENUMERATE <IPConnection.CALLBACK_ENUMERATE>`
 Callback der IP Connection haben ein ``device_identifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. py:attribute:: {1}.DEVICE_DISPLAY_NAME

 Diese Konstante stellt den Anzeigenamen eines {3} dar.
"""
        }

        create_meta = common.format_simple_element_meta([('uid', 'str', 1, 'in'),
                                                         ('ipcon', 'IPConnection', 1, 'in'),
                                                         (self.get_name().under, self.get_python_class_name(), 1, 'out')])
        create_meta_table = common.make_rst_meta_table(create_meta)

        cre = common.select_lang(create_str).format(self.get_python_class_name(),
                                                    self.get_name().under,
                                                    create_meta_table)

        reg_meta = common.format_simple_element_meta([('callback_id', 'int', 1, 'in'),
                                                      ('function', 'callable', 1, 'in')],
                                                     no_out_value={'en': 'None', 'de': 'None'})
        reg_meta_table = common.make_rst_meta_table(reg_meta)

        reg = common.select_lang(register_str).format(self.get_doc_rst_ref_name(),
                                                      self.get_name().camel,
                                                      self.get_category().camel,
                                                      reg_meta_table)

        bf = self.get_python_functions('bf')
        af = self.get_python_functions('af')
        ccf = self.get_python_functions('ccf')
        c = self.get_python_callbacks()
        vf = self.get_python_functions('vf')
        if_ = self.get_python_functions('if')
        api_str = ''

        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)

        if af:
            api_str += common.select_lang(common.af_str).format(af)

        if c:
            api_str += common.select_lang(common.ccf_str).format(reg, ccf)
            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_python_class_name(),
                                                        self.get_name().under,
                                                        c)

        if vf:
            api_str += common.select_lang(common.vf_str).format(vf)

        if if_:
            api_str += common.select_lang(common.if_str).format(if_)

        article = 'ein'

        if self.is_brick():
            article = 'einen'

        api_str += common.select_lang(const_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_python_class_name(),
                                                        article,
                                                        self.get_long_display_name())

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.specialize_python_doc_function_links(common.select_lang(self.get_doc())),
                                              api_str)

    def get_python_doc(self):
        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += self.get_python_examples()
        doc += self.get_python_api()

        return doc

class PythonDocPacket(python_common.PythonPacket):
    def get_python_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())
        text = self.get_device().specialize_python_doc_function_links(text)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = self.get_device().get_python_class_name() + '.'

        def format_element_name(element, index):
            if index == None:
                return element.get_name().under

            return '{0}[{1}]'.format(element.get_name().under, index)

        text += common.format_constants(prefix, self, format_element_name)
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

class PythonDocGenerator(python_common.PythonGeneratorTrait, common.DocGenerator):
    def get_doc_rst_filename_part(self):
        return 'Python'

    def get_doc_example_regex(self):
        return r'^example_.*\.py$'

    def get_device_class(self):
        return PythonDocDevice

    def get_packet_class(self):
        return PythonDocPacket

    def get_element_class(self):
        return python_common.PythonElement

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_python_doc())

def generate(root_dir, language):
    common.generate(root_dir, language, PythonDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
