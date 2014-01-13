#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Visual Basic .NET Documentation Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_vbnet_doc.py: Generator for Visual Basic .NET documentation

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

class VBNETDocDevice(common.Device):
    def get_vbnet_class_name(self):
        return self.get_category() + self.get_camel_case_name()

    def get_vbnet_examples(self):
        def title_from_file_name(file_name):
            file_name = file_name.replace('Example', '').replace('.vb', '')
            return common.camel_case_to_space(file_name)

        return common.make_rst_examples(title_from_file_name, self, self.get_generator().get_bindings_root_directory(),
                                        'vbnet', 'Example', '.vb', 'VBNET')

    def get_vbnet_methods(self, typ):
        methods = ''
        function = '.. vbnet:function:: Function {0}.{1}({2}) As {3}\n{4}'
        sub = '.. vbnet:function:: Sub {0}.{1}({2})\n{3}'
        cls = self.get_vbnet_class_name()

        for packet in self.get_packets('function'):
            if packet.get_doc()[0] != typ:
                continue

            ret_type = packet.get_vbnet_return_type()
            name = packet.get_camel_case_name()
            params = packet.get_vbnet_parameter_list()
            desc = packet.get_vbnet_formatted_doc()

            if len(ret_type) > 0:
                method = function.format(cls, name, params, ret_type, desc)
            else:
                method = sub.format(cls, name, params, desc)

            methods += method + '\n'

        return methods

    def get_vbnet_callbacks(self):
        cb = {
        'en': """
.. vbnet:function:: Event {0}.{1}(ByVal sender As {0}{2})

{3}
""",
        'de': """
.. vbnet:function:: Event {0}.{1}(ByVal sender As {0}{2})

{3}
"""
        }

        cbs = ''
        for packet in self.get_packets('callback'):
            desc = packet.get_vbnet_formatted_doc()
            params = packet.get_vbnet_parameter_list()
            if len(params) > 0:
                params = ', ' + params

            cbs += common.select_lang(cb).format(self.get_vbnet_class_name(),
                                                 packet.get_camel_case_name(),
                                                 params,
                                                 desc)

        return cbs

    def get_vbnet_api(self):
        create_str = {
        'en': """
.. vbnet:function:: Class {3}{1}(ByVal uid As String, ByVal ipcon As IPConnection)

 Creates an object with the unique device ID ``uid``:

 .. code-block:: vbnet

    Dim {4} As New {3}{1}("YOUR_DEVICE_UID", ipcon)

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_{2}_vbnet_examples>`).
""",
        'de': """
.. vbnet:function:: Class {3}{1}(ByVal uid As String, ByVal ipcon As IPConnection)

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: vbnet

    Dim {4} As New {3}{1}("YOUR_DEVICE_UID", ipcon)

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_{2}_vbnet_examples>`).
"""
        }

        c_str = {
        'en': """
.. _{1}_{2}_vbnet_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive time critical or recurring data from
the device. The registration is done by assigning a procedure to an callback
property of the device object:

 .. code-block:: vbnet

    Sub Callback(ByVal sender As {3}{4}, ByVal value As Short)
        Console.WriteLine("Value: {{0}}", value)
    End Sub

    AddHandler {5}.Example, AddressOf Callback

The available callback property and their type of parameters are described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{0}
""",
        'de': """
.. _{1}_{2}_vbnet_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische oder
wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung erfolgt indem
eine Prozedur einem Callback Property des Geräte Objektes zugewiesen wird:

 .. code-block:: vbnet

    Sub Callback(ByVal sender As {3}{4}, ByVal value As Short)
        Console.WriteLine("Value: {{0}}", value)
    End Sub

    AddHandler {5}.Example, AddressOf Callback

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

Since Visual Basic .NET does not support multiple return values directly, we
use the ``ByRef`` keyword to return multiple values from a function.

All functions and procedures listed below are thread-safe.

{1}

{2}
""",
        'de': """
{0}
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
        'en' : """
Constants
^^^^^^^^^

.. vbnet:attribute:: Const {1}{0}.DEVICE_IDENTIFIER

 This constant is used to identify a {0} {1}.

 The :vbnet:func:`GetIdentity() <{1}{0}.GetIdentity>` function and the
 :vbnet:func:`EnumerateCallback <IPConnection.EnumerateCallback>`
 callback of the IP Connection have a ``deviceIdentifier`` parameter to specify
 the Brick's or Bricklet's type.
""",
        'de' : """
Konstanten
^^^^^^^^^^

.. vbnet:attribute:: Const {1}{0}.DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {0} {1} zu identifizieren.

 Die :vbnet:func:`GetIdentity() <{1}{0}.GetIdentity>` Funktion und der
 :vbnet:func:`EnumerateCallback <IPConnection.EnumerateCallback>`
 Callback der IP Connection haben ein ``deviceIdentifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.
"""
        }

        cre = common.select_lang(create_str).format(self.get_underscore_name(),
                                                    self.get_camel_case_name(),
                                                    self.get_category().lower(),
                                                    self.get_category(),
                                                    self.get_headless_camel_case_name())

        bf = self.get_vbnet_methods('bf')
        af = self.get_vbnet_methods('af')
        ccf = self.get_vbnet_methods('ccf')
        c = self.get_vbnet_callbacks()
        api_str = ''
        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)
        if af:
            api_str += common.select_lang(common.af_str).format(af)
        if c:
            api_str += common.select_lang(common.ccf_str).format(ccf, '')
            api_str += common.select_lang(c_str).format(c, self.get_underscore_name(),
                                                        self.get_category().lower(),
                                                        self.get_category(),
                                                        self.get_camel_case_name(),
                                                        self.get_headless_camel_case_name())

        article = 'ein'
        if self.get_category() == 'Brick':
            article = 'einen'
        api_str += common.select_lang(const_str).format(self.get_camel_case_name(),
                                                        self.get_category(),
                                                        article)

        ref = '.. _{0}_{1}_vbnet_api:\n'.format(self.get_underscore_name(),
                                                self.get_category().lower())

        return common.select_lang(api).format(ref, self.get_api_doc(), api_str)

    def get_vbnet_doc(self):
        title = { 'en': 'Visual Basic .NET bindings', 'de': 'Visual Basic .NET Bindings' }

        doc  = common.make_rst_header(self, 'vbnet', 'Visual Basic .NET')
        doc += common.make_rst_summary(self, common.select_lang(title), 'vbnet')
        doc += self.get_vbnet_examples()
        doc += self.get_vbnet_api()

        return doc

class VBNETDocPacket(common.Packet):
    def get_vbnet_class_name(self):
        return self.get_category() + self.get_camel_case_name()

    def get_vbnet_formatted_doc(self):
        text = common.select_lang(self.get_doc()[1])

        cls = self.get_device().get_vbnet_class_name()
        for other_packet in self.get_device().get_packets():
            name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
            name = other_packet.get_camel_case_name()
            if other_packet.get_type() == 'callback':
                name_right = ':vbnet:func:`{1} <{0}.{1}>`'.format(cls, name)
            else:
                name_right = ':vbnet:func:`{1}() <{0}.{1}>`'.format(cls, name)
            text = text.replace(name_false, name_right)

        # FIXME: add something similar for :char:`c`
        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = cls + '.'
        if self.get_underscore_name() == 'set_response_expected':
            text += common.format_function_id_constants(prefix, self.get_device())
        else:
            text += common.format_constants(prefix, self, char_format='"{0}"C')

        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

    def get_vbnet_return_type(self):
        elements = self.get_elements('out')

        if len(elements) == 1:
            vbnet_type = elements[0].get_vbnet_type()

            if elements[0].get_cardinality() > 1 and elements[0].get_type() != 'string':
                vbnet_type += '[]'

            return vbnet_type
        else:
            return ''

    def get_vbnet_parameter_list(self):
        param = []

        if len(self.get_elements('out')) > 1 or self.get_type() == 'callback':
            for element in self.get_elements():
                vbnet_type = element.get_vbnet_type()

                if element.get_direction() == 'in' or self.get_type() == 'callback':
                    modifier = 'ByVal '
                else:
                    modifier = 'ByRef '

                name = element.get_headless_camel_case_name()

                if element.get_cardinality() > 1 and element.get_type() != 'string':
                    name += '[]'

                param.append('{0}{1} As {2}'.format(modifier, name, vbnet_type))
        else:
            for element in self.get_elements('in'):
                vbnet_type = element.get_vbnet_type()
                name = element.get_headless_camel_case_name()

                if element.get_cardinality() > 1 and element.get_type() != 'string':
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

    def get_device_class(self):
        return VBNETDocDevice

    def get_packet_class(self):
        return VBNETDocPacket

    def get_element_class(self):
        return VBNETDocElement

    def generate(self, device):
        file_name = '{0}_{1}_VBNET.rst'.format(device.get_camel_case_name(), device.get_category())

        rst = open(os.path.join(self.get_bindings_root_directory(), 'doc', common.lang, file_name), 'wb')
        rst.write(device.get_vbnet_doc())
        rst.close()

def generate(bindings_root_directory, language):
    common.generate(bindings_root_directory, language, VBNETDocGenerator)

if __name__ == "__main__":
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
