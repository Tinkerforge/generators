#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Visual Basic .NET Documentation Generator
Copyright (C) 2012-2014, 2017-2018 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_vbnet_doc.py: Generator for Visual Basic .NET documentation

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

class VBNETDocDevice(common.Device):
    def get_vbnet_class_name(self):
        return self.get_category().camel + self.get_name().camel

    def specialize_vbnet_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':vbnet:func:`{1}Callback <{0}.{1}Callback>`'.format(packet.get_device().get_vbnet_class_name(),
                                                                            packet.get_name(skip=-2 if high_level else 0).camel)
            else:
                return ':vbnet:func:`{1}() <{0}.{1}>`'.format(packet.get_device().get_vbnet_class_name(),
                                                              packet.get_name(skip=-2 if high_level else 0).camel)

        return self.specialize_doc_rst_links(text, specializer, prefix='vbnet')

    def get_vbnet_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('Example', '').replace('.vb', '')
            return common.camel_to_space(filename)

        return common.make_rst_examples(title_from_filename, self)

    def get_vbnet_methods(self, typ):
        methods = ''
        function = '.. vbnet:function:: Function {0}.{1}({2}) As {3}\n{4}'
        sub = '.. vbnet:function:: Sub {0}.{1}({2})\n{3}'
        cls = self.get_vbnet_class_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != typ:
                continue

            skip = -2 if packet.has_high_level() else 0
            ret_type = packet.get_vbnet_return_type(high_level=True)
            name = packet.get_name(skip=skip).camel
            params = packet.get_vbnet_parameter_list(high_level=True)
            desc = packet.get_vbnet_formatted_doc()

            if len(ret_type) > 0:
                method = function.format(cls, name, params, ret_type, desc)
            else:
                method = sub.format(cls, name, params, desc)

            methods += method + '\n'

        return methods

    def get_vbnet_callbacks(self):
        cb = """
.. vbnet:function:: Event {0}.{1}Callback(ByVal sender As {0}{2})

{3}
"""
        cbs = ''

        for packet in self.get_packets('callback'):
            skip = -2 if packet.has_high_level() else 0
            desc = packet.get_vbnet_formatted_doc()
            params = packet.get_vbnet_parameter_list(high_level=True)

            if len(params) > 0:
                params = ', ' + params

            cbs += cb.format(self.get_vbnet_class_name(),
                             packet.get_name(skip=skip).camel,
                             params,
                             desc)

        return cbs

    def get_vbnet_api(self):
        create_str = {
            'en': """
.. vbnet:function:: Class {1}(ByVal uid As String, ByVal ipcon As IPConnection)

 Creates an object with the unique device ID ``uid``:

 .. code-block:: vbnet

    Dim {2} As New {1}("YOUR_DEVICE_UID", ipcon)

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_vbnet_examples>`).
""",
            'de': """
.. vbnet:function:: Class {1}(ByVal uid As String, ByVal ipcon As IPConnection)

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: vbnet

    Dim {2} As New {1}("YOUR_DEVICE_UID", ipcon)

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_vbnet_examples>`).
"""
        }

        c_str = {
            'en': """
.. _{0}_vbnet_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive time critical or recurring data from
the device. The registration is done by assigning a procedure to an callback
property of the device object:

 .. code-block:: vbnet

    Sub MyCallback(ByVal sender As {1}, ByVal value As Short)
        Console.WriteLine("Value: {{0}}", value)
    End Sub

    AddHandler {2}.ExampleCallback, AddressOf MyCallback

The available callback property and their type of parameters are described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{3}
""",
            'de': """
.. _{0}_vbnet_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische oder
wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung erfolgt indem
eine Prozedur einem Callback Property des Geräte Objektes zugewiesen wird:

 .. code-block:: vbnet

    Sub MyCallback(ByVal sender As {1}, ByVal value As Short)
        Console.WriteLine("Value: {{0}}", value)
    End Sub

    AddHandler {2}.ExampleCallback, AddressOf MyCallback

Die verfügbaren Callback Properties und ihre Parametertypen werden weiter
unten beschrieben.

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
.. _{0}_vbnet_api:

API
---

Since Visual Basic .NET does not support multiple return values directly, we
use the ``ByRef`` keyword to return multiple values from a function.

All functions and procedures listed below are thread-safe.

{1}

{2}
""",
            'de': """
.. _{0}_vbnet_api:

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
            'en': """
.. _{0}_vbnet_constants:

Constants
^^^^^^^^^

.. vbnet:attribute:: Const {1}.DEVICE_IDENTIFIER

 This constant is used to identify a {3}.

 The :vbnet:func:`GetIdentity() <{1}.GetIdentity>` function and the
 :vbnet:func:`IPConnection.EnumerateCallback <IPConnection.EnumerateCallback>`
 callback of the IP Connection have a ``deviceIdentifier`` parameter to specify
 the Brick's or Bricklet's type.

.. vbnet:attribute:: Const {1}.DEVICE_DISPLAY_NAME

 This constant represents the human readable name of a {3}.
""",
            'de': """
.. _{0}_vbnet_constants:

Konstanten
^^^^^^^^^^

.. vbnet:attribute:: Const {1}.DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {3} zu identifizieren.

 Die :vbnet:func:`GetIdentity() <{1}.GetIdentity>` Funktion und der
 :vbnet:func:`IPConnection.EnumerateCallback <IPConnection.EnumerateCallback>`
 Callback der IP Connection haben ein ``deviceIdentifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. vbnet:attribute:: Const {1}.DEVICE_DISPLAY_NAME

 Diese Konstante stellt den Anzeigenamen eines {3} dar.
"""
        }

        cre = common.select_lang(create_str).format(self.get_doc_rst_ref_name(),
                                                    self.get_vbnet_class_name(),
                                                    self.get_name().headless)

        bf = self.get_vbnet_methods('bf')
        af = self.get_vbnet_methods('af')
        ccf = self.get_vbnet_methods('ccf')
        c = self.get_vbnet_callbacks()
        api_str = ''
        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)
        if af:
            api_str += common.select_lang(common.af_str).format(af)
        if ccf:
            api_str += common.select_lang(common.ccf_str).format('', ccf)
        if c:
            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_vbnet_class_name(),
                                                        self.get_name().headless,
                                                        c)

        article = 'ein'
        if self.is_brick():
            article = 'einen'
        api_str += common.select_lang(const_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_vbnet_class_name(),
                                                        article,
                                                        self.get_long_display_name())

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.specialize_vbnet_doc_function_links(common.select_lang(self.get_doc())),
                                              api_str)

    def get_vbnet_doc(self):
        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += self.get_vbnet_examples()
        doc += self.get_vbnet_api()

        return doc

class VBNETDocPacket(common.Packet):
    def get_vbnet_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())
        text = self.get_device().specialize_vbnet_doc_function_links(text)

        # FIXME: add something similar for :char:`c`
        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = self.get_device().get_vbnet_class_name() + '.'

        text += common.format_constants(prefix, self, char_format_func='"{0}"C'.format)
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

    def get_vbnet_return_type(self, high_level=False):
        elements = self.get_elements(direction='out', high_level=high_level)

        if len(elements) == 1:
            vbnet_type = elements[0].get_vbnet_type()

            if elements[0].get_cardinality() != 1 and elements[0].get_type() != 'string':
                vbnet_type += '[]'

            return vbnet_type
        else:
            return ''

    def get_vbnet_parameter_list(self, high_level=False):
        param = []

        if len(self.get_elements(direction='out', high_level=high_level)) > 1 or self.get_type() == 'callback':
            for element in self.get_elements(high_level=high_level):
                vbnet_type = element.get_vbnet_type()

                if element.get_direction() == 'in' or self.get_type() == 'callback':
                    modifier = 'ByVal '
                else:
                    modifier = 'ByRef '

                name = element.get_name().headless

                if element.get_cardinality() != 1 and element.get_type() != 'string':
                    name += '[]'

                param.append('{0}{1} As {2}'.format(modifier, name, vbnet_type))
        else:
            for element in self.get_elements(direction='in', high_level=high_level):
                vbnet_type = element.get_vbnet_type()
                name = element.get_name().headless

                if element.get_cardinality() != 1 and element.get_type() != 'string':
                    name += '[]'

                param.append('ByVal {0} As {1}'.format(name, vbnet_type))

        return ', '.join(param)

class VBNETDocElement(common.Element):
    vbnet_types = {
        'int8':   'Short',
        'uint8':  'Byte',
        'int16':  'Short',
        'uint16': 'Integer',
        'int32':  'Integer',
        'uint32': 'Long',
        'int64':  'Long',
        'uint64': 'Long',
        'float':  'Single',
        'bool':   'Boolean',
        'char':   'Char',
        'string': 'String'
    }

    def get_vbnet_type(self):
        return VBNETDocElement.vbnet_types[self.get_type()]

class VBNETDocGenerator(common.DocGenerator):
    def get_bindings_name(self):
        return 'vbnet'

    def get_bindings_display_name(self):
        return 'Visual Basic .NET'

    def get_doc_rst_filename_part(self):
        return 'VBNET'

    def get_doc_example_regex(self):
        return r'^Example.*\.vb$'

    def get_device_class(self):
        return VBNETDocDevice

    def get_packet_class(self):
        return VBNETDocPacket

    def get_element_class(self):
        return VBNETDocElement

    def get_doc_null_value_name(self):
        return 'Nothing'

    def get_doc_formatted_param(self, element):
        return element.get_name().headless

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_vbnet_doc())

def generate(root_dir, language):
    common.generate(root_dir, language, VBNETDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print('=== Generating %s ===' % language)
        generate(os.getcwd(), language)
