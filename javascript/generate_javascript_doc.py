#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JavaScript Documentation Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014-2015, 2017 Matthias Bolte <matthias@tinkerforge.com>

generate_javascript_doc.py: Generator for JavaScript documentation

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
    def specialize_javascript_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':javascript:attr:`CALLBACK_{1} <{0}.CALLBACK_{1}>`'.format(packet.get_device().get_javascript_class_name(),
                                                                                   packet.get_upper_case_name(skip=-2 if high_level else 0))
            else:
                return ':javascript:func:`{1}() <{0}.{1}>`'.format(packet.get_device().get_javascript_class_name(),
                                                       packet.get_headless_camel_case_name(skip=-2 if high_level else 0))

        return self.specialize_doc_rst_links(text, specializer, prefix='javascript')

    def get_javascript_examples(self):
        def title_from_filename(filename):
            if filename.endswith('.js'):
                filename = filename.replace('Example', '').replace('.js', '')
                return common.camel_case_to_space(filename) + ' (Node.js)'
            elif filename.endswith('.html'):
                filename = filename.replace('Example', '').replace('.html', '')
                return common.camel_case_to_space(filename) + ' (HTML)'
            else:
                raise common.GeneratorError('Invalid filename ' + filename)

        def language_from_filename(filename):
            if filename.endswith('.js'):
                return 'javascript'
            elif filename.endswith('.html'):
                return 'html'
            else:
                raise common.GeneratorError('Invalid filename ' + filename)

        return common.make_rst_examples(title_from_filename, self,
                                        language_from_filename=language_from_filename,
                                        add_html_test_link=True)

    def get_javascript_methods(self, typ):
        methods = ''
        func_start = '.. javascript:function:: '
        cls = self.get_javascript_class_name()
        for packet in self.get_packets('function'):
            if packet.get_doc_type() != typ:
                continue
            name = packet.get_headless_camel_case_name()
            params = packet.get_javascript_parameter_list()
            pd = packet.get_javascript_parameter_desc('in')
            r = packet.get_javascript_return_desc()

            if name == 'getAPIVersion':
                r = ' :rtype: [int, int, int]\n'
            elif name == 'getResponseExpected':
                r = ' :rtype: boolean\n'
            elif name == 'setResponseExpected':
                r = ''
            elif name == 'setResponseExpectedAll':
                r = ''

            d = packet.get_javascript_formatted_doc()
            desc = '{0}{1}{2}'.format(pd, r, d)
            callbacks = '[returnCallback], [errorCallback]'

            if name == 'getAPIVersion':
                callbacks = ''
            elif name == 'getResponseExpected':
                callbacks = '[errorCallback]'
            elif name == 'setResponseExpected':
                callbacks = '[errorCallback]'
            elif name == 'setResponseExpectedAll':
                callbacks = ''

            if len(params) > 0 and len(callbacks) > 0:
                params += ", "

            func = '{0}{1}.{2}({3}{4})\n{5}'.format(func_start,
                                                    cls,
                                                    name,
                                                    params,
                                                    callbacks,
                                                    desc)

            methods += func + '\n'

        return methods

    def get_javascript_callbacks(self):
        cbs = ''
        func_start = '.. javascript:attribute:: '
        cls = self.get_javascript_class_name()
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
.. javascript:function:: new {1}(uid, ipcon)

 :param uid: string
 :param ipcon: IPConnection

 Creates an object with the unique device ID ``uid``:

 .. code-block:: javascript

    var {2} = new {1}("YOUR_DEVICE_UID", ipcon);

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_javascript_examples>`).
""",
        'de': """
.. javascript:function:: new {1}(uid, ipcon)

 :param uid: string
 :param ipcon: IPConnection

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: javascript

    var {2} = new {1}("YOUR_DEVICE_UID", ipcon)

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_javascript_examples>`).
"""
        }

        register_str = {
        'en': """
.. javascript:function:: {1}.on(id, callback)

 :param id: int
 :param callback: function

 Registers a callback with ID *id* to the function *callback*. The available
 IDs with corresponding function signatures are listed
 :ref:`below <{0}_javascript_callbacks>`.
""",
        'de': """
.. javascript:function:: {1}.on(id, callback)

 :param id: int
 :param callback: function

 Registriert einen Callback mit der ID *id* mit der Funktion *callback*. Die
 verfügbaren IDs mit den zugehörigen Funktionssignaturen sind
 :ref:`unten <{0}_javascript_callbacks>` zu finden.
"""
        }

        c_str = {
        'en': """
.. _{0}_javascript_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive
time critical or recurring data from the device. The registration is done
with the :javascript:func:`on() <{1}.on>` function of
the device object. The first parameter is the callback ID and the second
parameter the callback function:

.. code-block:: javascript

    {2}.on({1}.CALLBACK_EXAMPLE,
        function (param) {{
            console.log(param);
        }}
    );

The available constants with inherent number and type of parameters are
described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{3}
""",
        'de': """
.. _{0}_javascript_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit der Funktion :javascript:func:`on() <{1}.on>` des
Geräte Objektes durchgeführt werden. Der erste Parameter ist die Callback ID
und der zweite Parameter die Callback-Funktion:

.. code-block:: javascript

    {2}.on({1}.CALLBACK_EXAMPLE,
        function (param) {{
            console.log(param);
        }}
    );

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
.. _{0}_javascript_api:

API
---

Generally, every method of the JavaScript bindings can take two optional
parameters, ``returnCallback`` and ``errorCallback``. These are two user
defined callback functions. The ``returnCallback`` is called with the return
values as parameters, if the method returns something. The ``errorCallback``
is called with an error code in case of an error. The error code can be one
of the following values:

* IPConnection.ERROR_ALREADY_CONNECTED = 11
* IPConnection.ERROR_NOT_CONNECTED = 12
* IPConnection.ERROR_CONNECT_FAILED = 13
* IPConnection.ERROR_INVALID_FUNCTION_ID = 21
* IPConnection.ERROR_TIMEOUT = 31
* IPConnection.ERROR_INVALID_PARAMETER = 41
* IPConnection.ERROR_FUNCTION_NOT_SUPPORTED = 42
* IPConnection.ERROR_UNKNOWN_ERROR = 43

The namespace for the JavaScript bindings is ``Tinkerforge.*``.

{1}

{2}
""",
        'de': """
.. _{0}_javascript_api:

API
---

Allgemein kann jede Methode der JavaScript Bindings zwei optionale Parameter
haben, ``returnCallback`` und ``errorCallback``. Dies sind benutzerdefinierte
Callback-Funktionen. Der ``returnCallback`` wird aufgerufen mit den
Rückgabewerten der Methode, sofern vorhanden. Der ``errorCallback`` wird im
Fehlerfall mit einem Fehlercode aufgerufen. Der Fehlercode kann einer der
folgenden Werte sein:

* IPConnection.ERROR_ALREADY_CONNECTED = 11
* IPConnection.ERROR_NOT_CONNECTED = 12
* IPConnection.ERROR_CONNECT_FAILED = 13
* IPConnection.ERROR_INVALID_FUNCTION_ID = 21
* IPConnection.ERROR_TIMEOUT = 31
* IPConnection.ERROR_INVALID_PARAMETER = 41
* IPConnection.ERROR_FUNCTION_NOT_SUPPORTED = 42
* IPConnection.ERROR_UNKNOWN_ERROR = 43

Der Namespace der JavaScript Bindings ist ``Tinkerforge.*``.

{1}

{2}
"""
        }

        const_str = {
        'en': """
.. _{0}_javascript_constants:

Constants
^^^^^^^^^

.. javascript:attribute:: {1}.DEVICE_IDENTIFIER

 This constant is used to identify a {3}.

 The :javascript:func:`getIdentity() <{1}.getIdentity>` function and the
 :javascript:attr:`CALLBACK_ENUMERATE <IPConnection.CALLBACK_ENUMERATE>`
 callback of the IP Connection have a ``device_identifier`` parameter to specify
 the Brick's or Bricklet's type.

.. javascript:attribute:: {1}.DEVICE_DISPLAY_NAME

 This constant represents the human readable name of a {3}.
""",
        'de': """
.. _{0}_javascript_constants:

Konstanten
^^^^^^^^^^

.. javascript:attribute:: {1}.DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {3} zu identifizieren.

 Die :javascript:func:`getIdentity() <{1}.getIdentity>` Funktion und der
 :javascript:attr:`CALLBACK_ENUMERATE <IPConnection.CALLBACK_ENUMERATE>`
 Callback der IP Connection haben ein ``device_identifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. javascript:attribute:: {1}.DEVICE_DISPLAY_NAME

 Diese Konstante stellt den Anzeigenamen eines {3} dar.
"""
        }

        cre = common.select_lang(create_str).format(self.get_doc_rst_ref_name(),
                                                    self.get_javascript_class_name(),
                                                    self.get_headless_camel_case_name())
        reg = common.select_lang(register_str).format(self.get_doc_rst_ref_name(),
                                                      self.get_javascript_class_name())

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
            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_javascript_class_name(),
                                                        self.get_headless_camel_case_name(),
                                                        c)

        article = 'ein'
        if self.is_brick():
            article = 'einen'
        api_str += common.select_lang(const_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_javascript_class_name(),
                                                        article,
                                                        self.get_long_display_name())

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.specialize_javascript_doc_function_links(common.select_lang(self.get_doc())),
                                              api_str)

    def get_javascript_doc(self):
        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += self.get_javascript_examples()
        doc += self.get_javascript_api()

        return doc

class JavaScriptDocPacket(javascript_common.JavaScriptPacket):
    def get_javascript_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())
        text = self.get_device().specialize_javascript_doc_function_links(text)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = self.get_device().get_javascript_class_name() + '.'
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
            desc += param.format(element.get_headless_camel_case_name(), t)

        return desc

    def get_javascript_return_desc(self):
        desc = []
        param = ' :return {0}: {1}'
        for element in self.get_elements('out'):
            t = element.get_javascript_type()
            desc.append(param.format(element.get_headless_camel_case_name(), t))

        if len(desc) == 0:
            return '\n :noreturn: undefined\n'

        return '\n' + '\n'.join(desc) + '\n'

class JavaScriptDocGenerator(common.DocGenerator):
    def get_bindings_name(self):
        return 'javascript'

    def get_bindings_display_name(self):
        return 'JavaScript'

    def get_doc_rst_filename_part(self):
        return 'JavaScript'

    def get_doc_example_regex(self):
        return '^Example.*\.(?:js|html)$'

    def get_device_class(self):
        return JavaScriptDocDevice

    def get_packet_class(self):
        return JavaScriptDocPacket

    def get_element_class(self):
        return javascript_common.JavaScriptElement

    def compare_examples(self, example1, example2):
        ext1 = os.path.splitext(example1[1])[1]
        ext2 = os.path.splitext(example2[1])[1]

        if ext1 == ext2:
            return common.DocGenerator.compare_examples(self, example1, example2)
        elif ext1 == '.js':
            return -1
        else:
            return 1

    def generate(self, device):
        rst = open(device.get_doc_rst_path(), 'wb')
        rst.write(device.get_javascript_doc())
        rst.close()

def generate(bindings_root_directory, language):
    common.generate(bindings_root_directory, language, JavaScriptDocGenerator)

if __name__ == "__main__":
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
