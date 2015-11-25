#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C# Documentation Generator
Copyright (C) 2012-2015 Matthias Bolte <matthias@tinkerforge.com>
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
import shutil
import subprocess
import glob
import re

sys.path.append(os.path.split(os.getcwd())[0])
import common
import csharp_common

class CSharpDocDevice(csharp_common.CSharpDevice):
    def replace_csharp_function_links(self, text):
        link = ':csharp:func:`{1}() <{0}::{1}>`'
        link_c = ':csharp:func:`{1} <{0}::{1}>`'

        cls = self.get_csharp_class_name()
        for other_packet in self.get_packets():
            name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
            name = other_packet.get_camel_case_name()
            if other_packet.get_type() == 'callback':
                name_right = link_c.format(cls, name)
            else:
                name_right = link.format(cls, name)

            text = text.replace(name_false, name_right)

        return text

    def get_csharp_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('Example', '').replace('.cs', '')
            return common.camel_case_to_space(filename)

        return common.make_rst_examples(title_from_filename, self)

    def get_csharp_methods(self, typ):
        methods = ''
        func_start = '.. csharp:function:: '
        for packet in self.get_packets('function'):
            if packet.get_doc_type() != typ:
                continue

            signature = packet.get_csharp_method_signature(True, True)
            desc = packet.get_csharp_formatted_doc(1)
            func = '{0}{1}\n{2}'.format(func_start, signature, desc)
            methods += func + '\n'

        return methods

    def get_csharp_callbacks(self):
        cb = {
        'en': """
.. csharp:function:: public event {0}::{1}({0} sender{2})

{3}
""",
        'de': """
.. csharp:function:: public event {0}::{1}({0} sender{2})

{3}
"""
        }

        cbs = ''
        cls = self.get_csharp_class_name()
        for packet in self.get_packets('callback'):
            desc = packet.get_csharp_formatted_doc(2)
            params = packet.get_csharp_parameter_list()
            if len(params) > 0:
                params = ', ' + params

            cbs += common.select_lang(cb).format(cls,
                                                 packet.get_camel_case_name(),
                                                 params,
                                                 desc)

        return cbs

    def get_csharp_api(self):
        create_str = {
        'en': """
.. csharp:function:: class {1}(String uid, IPConnection ipcon)

 Creates an object with the unique device ID ``uid``:

 .. code-block:: csharp

  {1} {2} = new {1}("YOUR_DEVICE_UID", ipcon);

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_csharp_examples>`).
""",
        'de': """
.. csharp:function:: class {1}(String uid, IPConnection ipcon)

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

    void Callback({1} sender, int value)
    {{
        System.Console.WriteLine("Value: " + value);
    }}

    {2}.ExampleCallback += Callback;

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

    void Callback({1} sender, int value)
    {{
        System.Console.WriteLine("Value: " + value);
    }}

    {2}.ExampleCallback += Callback;

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

.. csharp:member:: public int {1}::DEVICE_IDENTIFIER

 This constant is used to identify a {3}.

 The :csharp:func:`GetIdentity() <{1}::GetIdentity>` function and the
 :csharp:func:`EnumerateCallback <IPConnection::EnumerateCallback>`
 callback of the IP Connection have a ``deviceIdentifier`` parameter to specify
 the Brick's or Bricklet's type.

.. csharp:member:: public string {1}::DEVICE_DISPLAY_NAME

 This constant represents the human readable name of a {3}.
""",
        'de': """
.. _{0}_csharp_constants:

Konstanten
^^^^^^^^^^

.. csharp:member:: public int {1}::DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {3} zu identifizieren.

 Die :csharp:func:`GetIdentity() <{1}::GetIdentity>` Funktion und der
 :csharp:func:`EnumerateCallback <IPConnection::EnumerateCallback>`
 Callback der IP Connection haben ein ``deviceIdentifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. csharp:member:: public string {1}::DEVICE_DISPLAY_NAME

 Diese Konstante stellt den Anzeigenamen eines {3} dar.
"""
        }

        cre = common.select_lang(create_str).format(self.get_doc_rst_ref_name(),
                                                    self.get_csharp_class_name(),
                                                    self.get_headless_camel_case_name())

        bf = self.get_csharp_methods('bf')
        af = self.get_csharp_methods('af')
        ccf = self.get_csharp_methods('ccf')
        c = self.get_csharp_callbacks()
        api_str = ''
        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)
        if af:
            api_str += common.select_lang(common.af_str).format(af)
        if ccf:
            api_str += common.select_lang(common.ccf_str).format('', ccf)
        if c:
            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_csharp_class_name(),
                                                        self.get_headless_camel_case_name(),
                                                        c)

        article = 'ein'
        if self.get_camel_case_category() == 'Brick':
            article = 'einen'
        api_str += common.select_lang(const_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_csharp_class_name(),
                                                        article,
                                                        self.get_long_display_name())

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.replace_csharp_function_links(self.get_api_doc()),
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

        text = self.get_device().replace_csharp_function_links(text)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = self.get_device().get_csharp_class_name() + '.'
        if self.get_underscore_name() == 'set_response_expected':
            text += common.format_function_id_constants(prefix, self.get_device())
        else:
            text += common.format_constants(prefix, self)

        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, shift_right)

class CSharpDocGenerator(common.DocGenerator):
    def get_bindings_name(self):
        return 'csharp'

    def get_bindings_display_name(self):
        return 'C#'

    def get_doc_rst_filename_part(self):
        return 'CSharp'

    def get_doc_example_regex(self):
        return '^Example.*\.cs$'

    def get_device_class(self):
        return CSharpDocDevice

    def get_packet_class(self):
        return CSharpDocPacket

    def get_element_class(self):
        return csharp_common.CSharpElement

    def generate(self, device):
        rst = open(device.get_doc_rst_path(), 'wb')
        rst.write(device.get_csharp_doc())
        rst.close()

def generate(bindings_root_directory, language):
    common.generate(bindings_root_directory, language, CSharpDocGenerator)

if __name__ == "__main__":
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
