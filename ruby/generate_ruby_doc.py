#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ruby Documentation Generator
Copyright (C) 2012-2014, 2017-2019 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_ruby_doc.py: Generator for Ruby documentation

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
import ruby_common

class RubyDocDevice(ruby_common.RubyDevice):
    def specialize_ruby_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':rb:attr:`::CALLBACK_{1} <{0}::CALLBACK_{1}>`'.format(packet.get_device().get_ruby_class_name(),
                                                                              packet.get_name(skip=-2 if high_level else 0).upper)
            else:
                return ':rb:func:`#{1} <{0}#{1}>`'.format(packet.get_device().get_ruby_class_name(),
                                                          packet.get_name(skip=-2 if high_level else 0).under)

        return self.specialize_doc_rst_links(text, specializer, prefix='rb')

    def get_ruby_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('example_', '').replace('.rb', '')
            return common.under_to_space(filename)

        return common.make_rst_examples(title_from_filename, self)

    def get_ruby_methods(self, typ):
        methods = ''
        func_start = '.. rb:function:: '
        cls = self.get_ruby_class_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != typ:
                continue

            skip = -2 if packet.has_high_level() else 0
            name = packet.get_name(skip=skip).under
            params = packet.get_ruby_parameters(high_level=True)

            if len(params) > 0:
                params = '(' + params + ')'

            ret_desc = packet.get_ruby_return_desc(high_level=True)
            meta = packet.get_formatted_element_meta(lambda element: element.get_ruby_type(),
                                                     lambda element: element.get_name().under,
                                                     return_object='conditional',
                                                     return_object_label_override={'en': 'Return Array', 'de': 'Rückgabe-Array'},
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta, index_label_match={'en': 'Return Array', 'de': 'Rückgabe-Array'})
            desc = packet.get_ruby_formatted_doc()
            func = '.. rb:function:: {0}#{1}{2}{3}\n\n{4}{5}'.format(cls,
                                                                     name,
                                                                     params,
                                                                     ret_desc,
                                                                     meta_table,
                                                                     desc)
            methods += func + '\n'

        return methods

    def get_ruby_callbacks(self):
        cbs = ''
        func_start = '.. rb:attribute:: '
        cls = self.get_ruby_class_name()

        for packet in self.get_packets('callback'):
            skip = -2 if packet.has_high_level() else 0
            meta = packet.get_formatted_element_meta(lambda element: element.get_ruby_type(),
                                                     lambda element: element.get_name().under,
                                                     no_out_value={'en': 'no parameters', 'de': 'keine Parameter'},
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_ruby_formatted_doc()

            func = '.. rb:attribute:: {0}::CALLBACK_{1}\n\n{2}{3}'.format(cls,
                                                                          packet.get_name(skip=skip).upper,
                                                                          meta_table,
                                                                          desc)
            cbs += func + '\n'

        return cbs

    def get_ruby_api(self):
        create_str = {
            'en': """
.. rb:function:: {1}::new(uid, ipcon) -> {2}

{3}

 Creates an object with the unique device ID ``uid``:

 .. code-block:: ruby

    {2} = {1}.new 'YOUR_DEVICE_UID', ipcon

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_ruby_examples>`).
""",
            'de': """
.. rb:function:: {1}::new(uid, ipcon) -> {2}

{3}

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: ruby

    {2} = {1}.new 'YOUR_DEVICE_UID', ipcon

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_ruby_examples>`).
"""
        }

        register_str = {
            'en': """
.. rb:function:: {1}#register_callback(callback_id) {{ |param [, ...]| block }} -> nil

{2}

 Registers the given ``block`` with the given ``callback_id``.

 The available callback IDs with corresponding function signatures are listed
 :ref:`below <{0}_ruby_callbacks>`.
""",
            'de': """
.. rb:function:: {1}#register_callback(callback_id) {{ |param [, ...]| block }} -> nil

{2}

 Registriert den ``block`` für die gegebene ``callback_id``.

 Die verfügbaren Callback IDs mit den zugehörigen Funktionssignaturen sind
 :ref:`unten <{0}_ruby_callbacks>` zu finden.
"""
        }

        c_str = {
            'en': """
.. _{0}_ruby_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive time critical or recurring data from
the device. The registration is done with the
:rb:func:`#register_callback <{1}#register_callback>` function of
the device object. The first parameter is the callback ID and the second
parameter is a block:

.. code-block:: ruby

    {2}.register_callback {1}::CALLBACK_EXAMPLE, do |param|
      puts "#{{param}}"
    end

The available constants with inherent number and type of parameters are
described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{3}
""",
            'de': """
.. _{0}_ruby_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit der Funktion :rb:func:`#register_callback <{1}#register_callback>` des
Geräte Objektes durchgeführt werden. Der erste Parameter ist der Callback ID
und der zweite Parameter der Block:

.. code-block:: ruby

    {2}.register_callback {1}::CALLBACK_EXAMPLE, do |param|
      puts "#{{param}}"
    end

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
.. _{0}_ruby_api:

API
---

All methods listed below are thread-safe.

{1}

{2}
""",
            'de': """
.. _{0}_ruby_api:

API
---

Alle folgend aufgelisteten Methoden sind Thread-sicher.

{1}

{2}
"""
        }

        const_str = {
            'en': """
.. _{0}_ruby_constants:

Constants
^^^^^^^^^

.. rb:attribute:: {1}::DEVICE_IDENTIFIER

 This constant is used to identify a {3}.

 The :rb:func:`#get_identity() <{1}#get_identity>` function and the
 :rb:attr:`IPConnection::CALLBACK_ENUMERATE <IPConnection::CALLBACK_ENUMERATE>`
 callback of the IP Connection have a ``device_identifier`` parameter to specify
 the Brick's or Bricklet's type.

.. rb:attribute:: {1}::DEVICE_DISPLAY_NAME

 This constant represents the human readable name of a {3}.
""",
            'de': """
.. _{0}_ruby_constants:

Konstanten
^^^^^^^^^^

.. rb:attribute:: {1}::DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {3} zu identifizieren.

 Die :rb:func:`#get_identity() <{1}#get_identity>` Funktion und der
 :rb:attr:`IPConnection::CALLBACK_ENUMERATE <IPConnection::CALLBACK_ENUMERATE>`
 Callback der IP Connection haben ein ``device_identifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. rb:attribute:: {1}::DEVICE_DISPLAY_NAME

 Diese Konstante stellt den Anzeigenamen eines {3} dar.
"""
        }

        create_meta = common.format_simple_element_meta([('uid', 'str', 1, 'in'),
                                                         ('ipcon', 'IPConnection', 1, 'in'),
                                                         (self.get_name().under, self.get_ruby_class_name(), 1, 'out')])
        create_meta_table = common.make_rst_meta_table(create_meta)

        cre = common.select_lang(create_str).format(self.get_doc_rst_ref_name(),
                                                    self.get_ruby_class_name(),
                                                    self.get_name().under,
                                                    create_meta_table)

        reg_meta = common.format_simple_element_meta([('callback_id', 'int', 1, 'in')])
        reg_meta_table = common.make_rst_meta_table(reg_meta)

        reg = common.select_lang(register_str).format(self.get_doc_rst_ref_name(),
                                                      self.get_ruby_class_name(),
                                                      reg_meta_table)

        bf = self.get_ruby_methods('bf')
        af = self.get_ruby_methods('af')
        ccf = self.get_ruby_methods('ccf')
        c = self.get_ruby_callbacks()
        api_str = ''

        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)

        if af:
            api_str += common.select_lang(common.af_str).format(af)

        if c:
            api_str += common.select_lang(common.ccf_str).format(reg, ccf)
            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_ruby_class_name(),
                                                        self.get_name().under,
                                                        c)

        article = 'ein'

        if self.is_brick():
            article = 'einen'

        api_str += common.select_lang(const_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_ruby_class_name(),
                                                        article,
                                                        self.get_long_display_name())

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.specialize_ruby_doc_function_links(common.select_lang(self.get_doc())),
                                              api_str)

    def get_ruby_doc(self):
        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += self.get_ruby_examples()
        doc += self.get_ruby_api()

        return doc

class RubyDocPacket(ruby_common.RubyPacket):
    def get_ruby_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())
        text = self.get_device().specialize_ruby_doc_function_links(text)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = self.get_device().get_ruby_class_name() + '::'

        text += common.format_constants(prefix, self, lambda element: element.get_name().under)
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

    def get_ruby_return_desc(self, high_level=False):
        ret = ' -> {0}'
        ret_list = []

        for element in self.get_elements(direction='out', high_level=high_level):
            ret_list.append(element.get_ruby_type())

        if len(ret_list) == 0:
            return ret.format('nil')
        elif len(ret_list) == 1:
            return ret.format(ret_list[0])

        return ret.format('[' + ', '.join(ret_list) + ']')

class RubyDocGenerator(ruby_common.RubyGeneratorTrait, common.DocGenerator):
    def get_bindings_name(self):
        return 'ruby'

    def get_bindings_display_name(self):
        return 'Ruby'

    def get_doc_rst_filename_part(self):
        return 'Ruby'

    def get_doc_example_regex(self):
        return r'^example_.*\.rb$'

    def get_device_class(self):
        return RubyDocDevice

    def get_packet_class(self):
        return RubyDocPacket

    def get_element_class(self):
        return ruby_common.RubyElement

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_ruby_doc())

def generate(root_dir, language):
    common.generate(root_dir, language, RubyDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
