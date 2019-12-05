#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C# Documentation Generator
Copyright (C) 2012-2015, 2017-2019 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_csharp_doc.py: Generator for C# documentation

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
import csharp_common

class CSharpDocDevice(csharp_common.CSharpDevice):
    def specialize_csharp_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':csharp:func:`{1}Callback <{0}::{1}Callback>`'.format(packet.get_device().get_csharp_class_name(),
                                                                              packet.get_name(skip=-2 if high_level else 0).camel)
            else:
                return ':csharp:func:`{1}() <{0}::{1}>`'.format(packet.get_device().get_csharp_class_name(),
                                                                packet.get_name(skip=-2 if high_level else 0).camel)

        return self.specialize_doc_rst_links(text, specializer, prefix='csharp')

    def get_csharp_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('Example', '').replace('.cs', '')
            return common.camel_to_space(filename)

        return common.make_rst_examples(title_from_filename, self)

    def get_csharp_functions(self, type_):
        functions = []
        template = '.. csharp:function:: {0}\n\n{1}{2}\n'

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type_:
                continue

            signature = packet.get_csharp_function_signature(print_full_name=True, is_doc=True, high_level=True)
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_csharp_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).headless,
                                                     output_parameter='conditional',
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_csharp_formatted_doc(1)

            functions.append(template.format(signature, meta_table, desc))

        return ''.join(functions)

    def get_csharp_callbacks(self):
        callbacks = []
        template = '.. csharp:function:: event {0}::{1}Callback({0} sender{2})\n\n{3}\n\n{4}\n'

        for packet in self.get_packets('callback'):
            skip = -2 if packet.has_high_level() else 0
            desc = packet.get_csharp_formatted_doc(1)
            params = packet.get_csharp_parameters(high_level=True)
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_csharp_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).headless,
                                                     prefix_elements=[('sender', self.get_csharp_class_name(), 1, 'out')],
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)

            callbacks.append(template.format(self.get_csharp_class_name(),
                                             packet.get_name(skip=skip).camel,
                                             common.wrap_non_empty(', ', params, ''),
                                             meta_table,
                                             desc))

        return ''.join(callbacks)

    def get_csharp_api(self):
        create_str = {
            'en': """
.. csharp:function:: class {1}(String uid, IPConnection ipcon)

{3}

 Creates an object with the unique device ID ``uid``:

 .. code-block:: csharp

  {1} {2} = new {1}("YOUR_DEVICE_UID", ipcon);

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_csharp_examples>`).
""",
            'de': """
.. csharp:function:: class {1}(String uid, IPConnection ipcon)

{3}

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: csharp

  {1} {2} = new {1}("YOUR_DEVICE_UID", ipcon);

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_csharp_examples>`).
"""
        }

        c_str = {
            'en': """
.. _{0}_csharp_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive time critical or recurring data from
the device. The registration is done by appending your callback handler to
the corresponding event:

.. code-block:: csharp

    void MyCallback({1} sender, int value)
    {{
        System.Console.WriteLine("Value: " + value);
    }}

    {2}.ExampleCallback += MyCallback;

The available events are described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{3}
""",
            'de': """
.. _{0}_csharp_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische oder wiederkehrende Daten
vom Gerät zu erhalten. Die Registrierung geschieht durch Anhängen des Callback
Handlers an den passenden Event:

.. code-block:: csharp

    void MyCallback({1} sender, int value)
    {{
        System.Console.WriteLine("Value: " + value);
    }}

    {2}.ExampleCallback += MyCallback;

Die verfügbaren Events werden weiter unten beschrieben.

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
.. _{0}_csharp_api:

API
---

Generally, every method of the C# bindings that returns a value can
throw a ``Tinkerforge.TimeoutException``. This exception gets thrown if the
device did not respond. If a cable based connection is used, it is
unlikely that this exception gets thrown (assuming nobody plugs the
device out). However, if a wireless connection is used, timeouts will occur
if the distance to the device gets too big.

Since C# does not support multiple return values directly, we use the ``out``
keyword to return multiple values from a method.

The namespace for all Brick/Bricklet bindings and the IPConnection is
``Tinkerforge.*``.

All methods listed below are thread-safe.

{1}

{2}
""",
            'de': """
.. _{0}_csharp_api:

API
---

Prinzipiell kann jede Funktion der C# Bindings, welche einen Wert zurück gibt
eine ``Tinkerforge.TimeoutException`` werfen. Diese Exception wird
geworfen wenn das Gerät nicht antwortet. Wenn eine Kabelverbindung genutzt
wird, ist es unwahrscheinlich, dass die Exception geworfen wird (unter der
Annahme, dass das Gerät nicht abgesteckt wird). Bei einer drahtlosen Verbindung
können Zeitüberschreitungen auftreten, sobald die Entfernung zum Gerät zu
groß wird.

Da C# nicht mehrere Rückgabewerte direkt unterstützt, wird das ``out`` Schlüsselwort
genutzt, um mehrere Werte aus einer Funktion zurückzugeben.

Der Namensraum für alle Brick/Bricklet Bindings und die IPConnection ist
``Tinkerforge.*``.

Alle folgend aufgelisteten Methoden sind Thread-sicher.

{1}

{2}
"""
        }

        const_str = {
            'en': """
.. _{0}_csharp_constants:

Constants
^^^^^^^^^

.. csharp:member:: int {1}::DEVICE_IDENTIFIER

 This constant is used to identify a {3}.

 The :csharp:func:`GetIdentity() <{1}::GetIdentity>` function and the
 :csharp:func:`IPConnection.EnumerateCallback <IPConnection::EnumerateCallback>`
 callback of the IP Connection have a ``deviceIdentifier`` parameter to specify
 the Brick's or Bricklet's type.

.. csharp:member:: string {1}::DEVICE_DISPLAY_NAME

 This constant represents the human readable name of a {3}.
""",
            'de': """
.. _{0}_csharp_constants:

Konstanten
^^^^^^^^^^

.. csharp:member:: int {1}::DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {3} zu identifizieren.

 Die :csharp:func:`GetIdentity() <{1}::GetIdentity>` Funktion und der
 :csharp:func:`IPConnection.EnumerateCallback <IPConnection::EnumerateCallback>`
 Callback der IP Connection haben ein ``deviceIdentifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. csharp:member:: string {1}::DEVICE_DISPLAY_NAME

 Diese Konstante stellt den Anzeigenamen eines {3} dar.
"""
        }

        create_meta = common.format_simple_element_meta([('uid', 'String', 1, 'in'),
                                                         ('ipcon', 'IPConnection', 1, 'in'),
                                                         (self.get_name().headless, self.get_csharp_class_name(), 1, 'out')])
        create_meta_table = common.make_rst_meta_table(create_meta)

        cre = common.select_lang(create_str).format(self.get_doc_rst_ref_name(),
                                                    self.get_csharp_class_name(),
                                                    self.get_name().headless,
                                                    create_meta_table)

        bf = self.get_csharp_functions('bf')
        af = self.get_csharp_functions('af')
        ccf = self.get_csharp_functions('ccf')
        c = self.get_csharp_callbacks()
        vf = self.get_csharp_functions('vf')
        api_str = ''

        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)

        if af:
            api_str += common.select_lang(common.af_str).format(af)

        if c:
            if ccf:
                api_str += common.select_lang(common.ccf_str).format('', ccf)

            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_csharp_class_name(),
                                                        self.get_name().headless,
                                                        c)

        if vf:
            api_str += common.select_lang(common.vf_str).format(vf)

        article = 'ein'

        if self.is_brick():
            article = 'einen'

        api_str += common.select_lang(const_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_csharp_class_name(),
                                                        article,
                                                        self.get_long_display_name())

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.specialize_csharp_doc_function_links(common.select_lang(self.get_doc())),
                                              api_str)

    def get_csharp_doc(self):
        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += self.get_csharp_examples()
        doc += self.get_csharp_api()

        return doc

class CSharpDocPacket(csharp_common.CSharpPacket):
    def get_csharp_formatted_doc(self, shift_right):
        text = common.select_lang(self.get_doc_text())
        text = self.get_device().specialize_csharp_doc_function_links(text)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = self.get_device().get_csharp_class_name() + '.'

        def format_element_name(element, index):
            if index == None:
                return element.get_name().headless

            return '{0}[{1}]'.format(element.get_name().headless, index)

        text += common.format_constants(prefix, self, format_element_name)
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, shift_right)

class CSharpDocGenerator(csharp_common.CSharpGeneratorTrait, common.DocGenerator):
    def get_bindings_name(self):
        return 'csharp'

    def get_bindings_display_name(self):
        return 'C#'

    def get_doc_rst_filename_part(self):
        return 'CSharp'

    def get_doc_example_regex(self):
        return r'^Example.*\.cs$'

    def get_device_class(self):
        return CSharpDocDevice

    def get_packet_class(self):
        return CSharpDocPacket

    def get_element_class(self):
        return csharp_common.CSharpElement

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_csharp_doc())

def generate(root_dir, language):
    common.generate(root_dir, language, CSharpDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print('=== Generating %s ===' % language)
        generate(os.getcwd(), language)
