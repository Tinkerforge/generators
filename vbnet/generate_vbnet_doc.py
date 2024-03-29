#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Visual Basic .NET Documentation Generator
Copyright (C) 2012-2014, 2017-2019 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>

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

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import importlib.util
import importlib.machinery

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

    if sys.hexversion < 0x3050000:
        generators_module = importlib.machinery.SourceFileLoader('generators', os.path.join(generators_dir, '__init__.py')).load_module()
    else:
        generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
        generators_module = importlib.util.module_from_spec(generators_spec)

        generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common
from generators.vbnet import vbnet_common

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

    def get_vbnet_functions(self, type_):
        functions = []
        template_function = '.. vbnet:function:: Function {0}.{1}({2}) As {3}\n\n{4}{5}\n'
        template_sub = '.. vbnet:function:: Sub {0}.{1}({2})\n\n{3}{4}\n'
        cls = self.get_vbnet_class_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type_:
                continue

            skip = -2 if packet.has_high_level() else 0
            ret_type = packet.get_vbnet_return_type(high_level=True)
            name = packet.get_name(skip=skip).camel
            params = packet.get_vbnet_parameter_list(high_level=True)
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_vbnet_type(context='meta', cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).headless,
                                                     output_parameter='conditional',
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_vbnet_formatted_doc()

            if len(ret_type) > 0:
                function = template_function.format(cls, name, params, ret_type, meta_table, desc)
            else:
                function = template_sub.format(cls, name, params, meta_table, desc)

            functions.append(function)

        return ''.join(functions)

    def get_vbnet_callbacks(self):
        callbacks = []
        template = '.. vbnet:function:: Event {0}.{1}Callback(ByVal sender As {0}{2})\n\n{3}{4}\n'

        for packet in self.get_packets('callback'):
            skip = -2 if packet.has_high_level() else 0
            desc = packet.get_vbnet_formatted_doc()
            params = packet.get_vbnet_parameter_list(high_level=True)
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_vbnet_type(context='meta', cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).headless,
                                                     prefix_elements=[('sender', self.get_vbnet_class_name(), 1, 'out')],
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)

            callbacks.append(template.format(self.get_vbnet_class_name(),
                                             packet.get_name(skip=skip).camel,
                                             common.wrap_non_empty(', ', params, ''),
                                             meta_table,
                                             desc))

        return ''.join(callbacks)

    def get_vbnet_api(self):
        create_str = {
            'en': """
.. vbnet:function:: Class {0}(ByVal uid As String, ByVal ipcon As IPConnection)

 Creates an object with the unique device ID ``uid``:

 .. code-block:: vbnet

    Dim {1} As New {0}("YOUR_DEVICE_UID", ipcon)

 This object can then be used after the IP Connection is connected.
""",
            'de': """
.. vbnet:function:: Class {0}(ByVal uid As String, ByVal ipcon As IPConnection)

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: vbnet

    Dim {1} As New {0}("YOUR_DEVICE_UID", ipcon)

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist.
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

        cre = common.select_lang(create_str).format(self.get_vbnet_class_name(),
                                                    self.get_name().headless)

        bf = self.get_vbnet_functions('bf')
        af = self.get_vbnet_functions('af')
        ccf = self.get_vbnet_functions('ccf')
        c = self.get_vbnet_callbacks()
        vf = self.get_vbnet_functions('vf')
        if_ = self.get_vbnet_functions('if')
        api_str = ''

        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)

        if af:
            api_str += common.select_lang(common.af_str).format(af)

        if c:
            if ccf:
                api_str += common.select_lang(common.ccf_str).format('', ccf)

            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_vbnet_class_name(),
                                                        self.get_name().headless,
                                                        c)

        if vf:
            api_str += common.select_lang(common.vf_str).format(vf)

        if if_:
            api_str += common.select_lang(common.if_str).format(if_)

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

        def format_element_name(element, index):
            if index == None:
                return element.get_name().headless

            return '{0}({1})'.format(element.get_name().headless, index)

        text += common.format_constants(prefix, self, format_element_name)
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

    def format_value(self, value):
        if isinstance(value, list):
            result = []

            for subvalue in value:
                result.append(self.format_value(subvalue))

            return '{{{0}}}'.format(', '.join(result))

        type_ = self.get_type()

        if type_ == 'float':
            return common.format_float(value)

        if type_ == 'bool':
            return str(bool(value)).lower()

        if type_ == 'char':
            return '"{0}"C'.format(value.replace('"', '""'))

        if type_ == 'string':
            return '"{0}"'.format(value.replace('"', '""'))

        return str(value)

    def get_vbnet_type(self, context='default', cardinality=None):
        assert context in ['default', 'meta'], context
        assert cardinality == None or (isinstance(cardinality, int) and cardinality > 0), cardinality

        vbnet_type = VBNETDocElement.vbnet_types[self.get_type()]

        if cardinality == None:
            cardinality = self.get_cardinality()

        if context == 'meta' and cardinality != 1 and self.get_type() != 'string':
            vbnet_type += ' Array'

        return vbnet_type

class VBNETDocGenerator(vbnet_common.VBNETGeneratorTrait, common.DocGenerator):
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

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_vbnet_doc())

def generate(root_dir, language, internal):
    common.generate(root_dir, language, internal, VBNETDocGenerator)

if __name__ == '__main__':
    args = common.dockerize('vbnet', __file__, add_internal_argument=True)

    for language in ['en', 'de']:
        generate(os.getcwd(), language, args.internal)
