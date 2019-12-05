#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JavaScript Documentation Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014-2015, 2017-2019 Matthias Bolte <matthias@tinkerforge.com>

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

sys.path.append(os.path.split(os.getcwd())[0])
import common
import javascript_common

class JavaScriptDocDevice(javascript_common.JavaScriptDevice):
    def specialize_javascript_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':javascript:attr:`CALLBACK_{1} <{0}.CALLBACK_{1}>`'.format(packet.get_device().get_javascript_class_name(),
                                                                                   packet.get_name(skip=-2 if high_level else 0).upper)
            else:
                return ':javascript:func:`{1}() <{0}.{1}>`'.format(packet.get_device().get_javascript_class_name(),
                                                                   packet.get_name(skip=-2 if high_level else 0).headless)

        return self.specialize_doc_rst_links(text, specializer, prefix='javascript')

    def get_javascript_examples(self):
        def title_from_filename(filename):
            if filename.endswith('.js'):
                filename = filename.replace('Example', '').replace('.js', '')
                return common.camel_to_space(filename) + ' (Node.js)'
            elif filename.endswith('.html'):
                filename = filename.replace('Example', '').replace('.html', '')
                return common.camel_to_space(filename) + ' (HTML)'
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

    def get_javascript_methods(self, type_):
        methods = ''
        func_start = '.. javascript:function:: '
        cls = self.get_javascript_class_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type_:
                continue

            skip = -2 if packet.has_high_level() else 0
            name = packet.get_name(skip=skip).headless
            params = packet.get_javascript_parameter_list(high_level=True)
            desc = packet.get_javascript_formatted_doc()
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

            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_javascript_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).headless,
                                                     output_parameter='never' if packet.is_virtual() else 'always',
                                                     output_parameter_label_override={'en': 'Callback Parameters', 'de': 'Callback-Parameter'},
                                                     no_out_value={'en': 'undefined', 'de': 'undefined'},
                                                     no_return_value={'en': 'undefined', 'de': 'undefined'},
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)

            func = '{0}{1}.{2}({3}{4})\n\n{5}\n{6}'.format(func_start,
                                                           cls,
                                                           name,
                                                           params,
                                                           callbacks,
                                                           meta_table,
                                                           desc)

            methods += func + '\n'

        return methods

    def get_javascript_callbacks(self):
        cbs = ''
        func_start = '.. javascript:attribute:: '
        cls = self.get_javascript_class_name()

        for packet in self.get_packets('callback'):
            skip = -2 if packet.has_high_level() else 0
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_javascript_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).headless,
                                                     no_out_value={'en': 'undefined', 'de': 'undefined'},
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_javascript_formatted_doc()

            func = '{0}{1}.CALLBACK_{2}\n\n{3}\n{4}'.format(func_start,
                                                            cls,
                                                            packet.get_name(skip=skip).upper,
                                                            meta_table,
                                                            desc)
            cbs += func + '\n'

        return cbs

    def get_javascript_api(self):
        create_str = {
            'en': """
.. javascript:function:: new {1}(uid, ipcon)

{3}

 Creates an object with the unique device ID ``uid``:

 .. code-block:: javascript

    var {2} = new {1}("YOUR_DEVICE_UID", ipcon);

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_javascript_examples>`).
""",
            'de': """
.. javascript:function:: new {1}(uid, ipcon)

{3}

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: javascript

    var {2} = new {1}("YOUR_DEVICE_UID", ipcon)

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_javascript_examples>`).
"""
        }

        register_str = {
            'en': """
.. javascript:function:: {1}.on(callback_id, function)

{2}

 Registers the given ``function`` with the given ``callback_id``.

 The available callback IDs with corresponding function signatures are
 listed :ref:`below <{0}_javascript_callbacks>`.
""",
            'de': """
.. javascript:function:: {1}.on(callback_id, function)

{2}

 Registriert die ``function`` für die gegebene ``callback_id``.

 Die verfügbaren Callback IDs mit den zugehörigen Funktionssignaturen
 sind :ref:`unten <{0}_javascript_callbacks>` zu finden.
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

Generally, every function of the JavaScript bindings can take two optional
parameters, ``returnCallback`` and ``errorCallback``. These are two user
defined callback functions. The ``returnCallback`` function is called with the
results as arguments, if the function returns its results asynchronously. The
``errorCallback`` is called with an error code in case of an error. The error
code can be one of the following values:

* IPConnection.\\ **ERROR**\\ _ALREADY_CONNECTED = 11
* IPConnection.\\ **ERROR**\\ _NOT_CONNECTED = 12
* IPConnection.\\ **ERROR**\\ _CONNECT_FAILED = 13
* IPConnection.\\ **ERROR**\\ _INVALID_FUNCTION_ID = 21
* IPConnection.\\ **ERROR**\\ _TIMEOUT = 31
* IPConnection.\\ **ERROR**\\ _INVALID_PARAMETER = 41
* IPConnection.\\ **ERROR**\\ _FUNCTION_NOT_SUPPORTED = 42
* IPConnection.\\ **ERROR**\\ _UNKNOWN_ERROR = 43
* IPConnection.\\ **ERROR**\\ _STREAM_OUT_OF_SYNC = 51
* IPConnection.\\ **ERROR**\\ _NON_ASCII_CHAR_IN_SECRET = 71

The namespace for the JavaScript bindings is ``Tinkerforge.*``.

{1}

{2}
""",
            'de': """
.. _{0}_javascript_api:

API
---

Allgemein kann jede Funktion der JavaScript Bindings zwei optionale Parameter
haben, ``returnCallback`` und ``errorCallback``. Dies sind benutzerdefinierte
Callback-Funktionen. Die ``returnCallback``-Funktion wird mit dem Ergebnissen
der Funktion als Argumente aufgerufen, falls die Funktion ihre
Ergebnisse asynchron zurückgibt. Die ``errorCallback``-Funktion wird im
Fehlerfall mit einem Fehlercode aufgerufen. Der Fehlercode kann einer der
folgenden Werte sein:

* IPConnection.\\ **ERROR**\\ _ALREADY_CONNECTED = 11
* IPConnection.\\ **ERROR**\\ _NOT_CONNECTED = 12
* IPConnection.\\ **ERROR**\\ _CONNECT_FAILED = 13
* IPConnection.\\ **ERROR**\\ _INVALID_FUNCTION_ID = 21
* IPConnection.\\ **ERROR**\\ _TIMEOUT = 31
* IPConnection.\\ **ERROR**\\ _INVALID_PARAMETER = 41
* IPConnection.\\ **ERROR**\\ _FUNCTION_NOT_SUPPORTED = 42
* IPConnection.\\ **ERROR**\\ _UNKNOWN_ERROR = 43
* IPConnection.\\ **ERROR**\\ _STREAM_OUT_OF_SYNC = 51
* IPConnection.\\ **ERROR**\\ _NON_ASCII_CHAR_IN_SECRET = 71

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
 :javascript:attr:`IPConnection.CALLBACK_ENUMERATE <IPConnection.CALLBACK_ENUMERATE>`
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
 :javascript:attr:`IPConnection.CALLBACK_ENUMERATE <IPConnection.CALLBACK_ENUMERATE>`
 Callback der IP Connection haben ein ``device_identifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. javascript:attribute:: {1}.DEVICE_DISPLAY_NAME

 Diese Konstante stellt den Anzeigenamen eines {3} dar.
"""
        }

        create_meta = common.format_simple_element_meta([('uid', 'string', 1, 'in'),
                                                         ('ipcon', 'IPConnection', 1, 'in'),
                                                         (self.get_name().headless, self.get_javascript_class_name(), 1, 'out')])
        create_meta_table = common.make_rst_meta_table(create_meta)

        cre = common.select_lang(create_str).format(self.get_doc_rst_ref_name(),
                                                    self.get_javascript_class_name(),
                                                    self.get_name().headless,
                                                    create_meta_table)

        reg_meta = common.format_simple_element_meta([('callback_id', 'int', 1, 'in'),
                                                      ('function', 'function', 1, 'in')],
                                                     no_out_value={'en': 'undefined', 'de': 'undefined'})
        reg_meta_table = common.make_rst_meta_table(reg_meta)

        reg = common.select_lang(register_str).format(self.get_doc_rst_ref_name(),
                                                      self.get_javascript_class_name(),
                                                      reg_meta_table)

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
                                                        self.get_name().headless,
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

        def format_element_name(element, index):
            if index == None:
                return element.get_name().under

            return '{0}[{1}]'.format(element.get_name().under, index)

        text += common.format_constants(prefix, self, format_element_name)
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

    def get_javascript_parameter_desc(self, io):
        desc = '\n'
        param = ' :param {0}: {1}\n'

        for element in self.get_elements(direction=io, high_level=True):
            t = element.get_javascript_type()
            desc += param.format(element.get_name().headless, t)

        return desc

    def get_javascript_return_desc(self):
        desc = []
        param = ' :return {0}: {1}'

        for element in self.get_elements(direction='out', high_level=True):
            t = element.get_javascript_type()
            desc.append(param.format(element.get_name().headless, t))

        if len(desc) == 0:
            return '\n :noreturn: undefined\n'
        else:
            return '\n' + '\n'.join(desc) + '\n'

class JavaScriptDocGenerator(javascript_common.JavascriptGeneratorTrait, common.DocGenerator):
    def get_bindings_name(self):
        return 'javascript'

    def get_bindings_display_name(self):
        return 'JavaScript'

    def get_doc_rst_filename_part(self):
        return 'JavaScript'

    def get_doc_example_regex(self):
        return r'^Example.*\.(?:js|html)$'

    def get_device_class(self):
        return JavaScriptDocDevice

    def get_packet_class(self):
        return JavaScriptDocPacket

    def get_element_class(self):
        return javascript_common.JavaScriptElement

    def get_example_sort_key(self, example):
        return 0 if os.path.splitext(example[1])[1] == '.js' else 1, example[2], example[0] # extension, lines, filename

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_javascript_doc())

def generate(root_dir, language):
    common.generate(root_dir, language, JavaScriptDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
