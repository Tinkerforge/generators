#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JavaScript Documentation Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2013 Olaf Lüke <olaf@tinkerforge.com>

generator_javascript_doc.py: Generator for JavaScript documentation

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
import javascript_common

class JavaScriptDocDevice(javascript_common.JavaScriptDevice):
    def get_javascript_examples(self):
        def title_from_file_name(file_name):
            file_name = file_name.replace('example_', '').replace('.js', '')
            return common.underscore_to_space(file_name)

        return common.make_rst_examples(title_from_file_name, self, self.get_generator().get_bindings_root_directory(),
                                        'javascript', 'example_', '.js', 'JavaScript')

    def get_javascript_methods(self, typ):
        methods = ''
        func_start = '.. py:function:: '
        cls = self.get_camel_case_name()
        for packet in self.get_packets('function'):
            if packet.get_doc()[0] != typ:
                continue
            name = packet.get_underscore_name()
            params = packet.get_javascript_parameter_list()
            pd = packet.get_javascript_parameter_desc('in')
            r = packet.get_javascript_return_desc()
            d = packet.get_javascript_formatted_doc()
            obj_desc = packet.get_javascript_object_desc()
            desc = '{0}{1}{2}{3}'.format(pd, r, d, obj_desc)
            func = '{0}{1}.{2}({3})\n{4}'.format(func_start,
                                                 cls,
                                                 name,
                                                 params,
                                                 desc)
            methods += func + '\n'

        return methods

    def get_javascript_callbacks(self):
        cbs = ''
        func_start = '.. py:attribute:: '
        cls = self.get_camel_case_name()
        for packet in self.get_packets('callback'):
            param_desc = packet.get_javascript_parameter_desc('out')
            desc = packet.get_javascript_formatted_doc()

            func = '{0}{1}.CALLBACK_{2}\n{3}\n{4}'.format(func_start,
                                                          cls,
                                                          packet.get_upper_case_name(),
                                                          param_desc,
                                                          desc)
            cbs += func + '\n'

        return cbs

    def get_javascript_api(self):
        create_str = {
        'en': """
.. py:function:: {1}(uid, ipcon)

 :param uid: string
 :param ipcon: IPConnection

 Creates an object with the unique device ID ``uid``:

 .. code-block:: javascript

    {0} = {1}("YOUR_DEVICE_UID", ipcon)

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_{2}_javascript_examples>`).
""",
        'de': """
.. py:function:: {1}(uid, ipcon)

 :param uid: string
 :param ipcon: IPConnection

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: javascript

    {0} = {1}("YOUR_DEVICE_UID", ipcon)

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_{2}_javascript_examples>`).
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
 :ref:`below <{0}_{2}_javascript_callbacks>`.
""",
        'de': """
.. py:function:: {1}.register_callback(id, callback)

 :param id: int
 :param callback: callable
 :rtype: None

 Registriert einen Callback mit der ID *id* mit der Funktion *callback*. Die
 verfügbaren IDs mit den zugehörigen Funktionssignaturen sind
 :ref:`unten <{0}_{2}_javascript_callbacks>` zu finden.
"""
        }

        c_str = {
        'en': """
.. _{1}_{2}_javascript_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive
time critical or recurring data from the device. The registration is done
with the :py:func:`register_callback() <{3}.register_callback>` function of
the device object. The first parameter is the callback ID and the second
parameter the callback function:

.. code-block:: javascript

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
.. _{1}_{2}_javascript_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit der Funktion :py:func:`register_callback() <{3}.register_callback>` des
Geräte Objektes durchgeführt werden. Der erste Parameter ist die Callback ID
und der zweite Parameter die Callback-Funktion:

.. code-block:: javascript

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
.. _{5}_{6}_javascript_constants:

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
.. _{5}_{6}_javascript_constants:

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

        bf = self.get_javascript_methods('bf')
        af = self.get_javascript_methods('af')
        ccf = self.get_javascript_methods('ccf')
        c = self.get_javascript_callbacks()
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

        ref = '.. _{0}_{1}_javascript_api:\n'.format(self.get_underscore_name(),
                                                 self.get_category().lower())

        return common.select_lang(api).format(ref, self.get_api_doc(), api_str)

    def get_javascript_doc(self):
        title = { 'en': 'JavaScript bindings', 'de': 'JavaScript Bindings' }

        doc  = common.make_rst_header(self, 'javascript', 'JavaScript')
        doc += common.make_rst_summary(self, common.select_lang(title), 'javascript')
        doc += self.get_javascript_examples()
        doc += self.get_javascript_api()

        return doc

class JavaScriptDocPacket(javascript_common.JavaScriptPacket):
    def get_javascript_formatted_doc(self):
        text = common.select_lang(self.get_doc()[1])
        cls = self.get_device().get_camel_case_name()
        for other_packet in self.get_device().get_packets():
            name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
            if other_packet.get_type() == 'callback':
                name_upper = other_packet.get_upper_case_name()
                name_right = ':py:attr:`CALLBACK_{1} <{0}.CALLBACK_{1}>`'.format(cls, name_upper)
            else:
                name_right = ':py:func:`{1}() <{0}.{1}>`'.format(cls, other_packet.get_underscore_name())
            text = text.replace(name_false, name_right)

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

    def get_javascript_parameter_desc(self, io):
        desc = '\n'
        param = ' :param {0}: {1}\n'
        for element in self.get_elements(io):
            t = element.get_javascript_type()
            desc += param.format(element.get_underscore_name(), t)

        return desc

    def get_javascript_return_desc(self):
        ret = ' :rtype: {0}\n'
        ret_list = []
        for element in self.get_elements('out'):
            ret_list.append(element.get_javascript_type())
        if len(ret_list) == 0:
            return ret.format(None)
        elif len(ret_list) == 1:
            return ret.format(ret_list[0])

        return ret.format('(' + ', '.join(ret_list) + ')')

    def get_javascript_object_desc(self):
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

class JavaScriptDocGenerator(common.DocGenerator):
    def get_bindings_name(self):
        return 'javascript'

    def get_device_class(self):
        return JavaScriptDocDevice

    def get_packet_class(self):
        return JavaScriptDocPacket

    def get_element_class(self):
        return javascript_common.JavaScriptElement

    def generate(self, device):
        return

        file_name = '{0}_{1}_JavaScript.rst'.format(device.get_camel_case_name(), device.get_category())

        rst = open(os.path.join(self.get_bindings_root_directory(), 'doc', common.lang, file_name), 'wb')
        rst.write(device.get_javascript_doc())
        rst.close()

def generate(bindings_root_directory, language):
    common.generate(bindings_root_directory, language, JavaScriptDocGenerator)

if __name__ == "__main__":
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
