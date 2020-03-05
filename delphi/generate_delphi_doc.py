#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Delphi/Lazarus Documentation Generator
Copyright (C) 2012-2015, 2017-2020 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_delphi_doc.py: Generator for Delphi/Lazarus documentation

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
import delphi_common

class DelphiBindingsDevice(delphi_common.DelphiDevice):
    def specialize_delphi_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':delphi:func:`On{1} <{0}.On{1}>`'.format(packet.get_device().get_delphi_class_name(),
                                                                 packet.get_name(skip=-2 if high_level else 0).camel)
            else:
                return ':delphi:func:`{1} <{0}.{1}>`'.format(packet.get_device().get_delphi_class_name(),
                                                             packet.get_name(skip=-2 if high_level else 0).camel)

        return self.specialize_doc_rst_links(text, specializer, prefix='delphi')

    def get_delphi_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('Example', '').replace('.pas', '')
            return common.camel_to_space(filename)

        return common.make_rst_examples(title_from_filename, self)

    def get_delphi_functions(self, type_):
        functions = []
        template_function = '.. delphi:function:: function {0}.{1}({2}): {3}\n\n{4}\n{5}\n'
        template_procedure = '.. delphi:function:: procedure {0}.{1}({2})\n\n{3}\n{4}\n'
        cls = self.get_delphi_class_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type_:
                continue

            ret_type = packet.get_delphi_return_type('doc', high_level=True)
            skip = -2 if packet.has_high_level() else 0
            name = packet.get_name(skip=skip).camel
            params = '; '.join(packet.get_delphi_parameters('doc', high_level=True))
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_delphi_type(context='meta', cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).headless,
                                                     output_parameter='conditional',
                                                     explicit_string_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_delphi_formatted_doc()

            if len(ret_type) > 0:
                function = template_function.format(cls, name, params, ret_type, meta_table, desc)
            else:
                function = template_procedure.format(cls, name, params, meta_table, desc)

            functions.append(function)

        return ''.join(functions)

    def get_delphi_callbacks(self):
        callbacks = []
        template = """.. delphi:function:: property {0}.On{1}

 .. code-block:: delphi

  procedure(sender: {0}{2}) of object;

{3}

{4}
"""
        cls = self.get_delphi_class_name()

        for packet in self.get_packets('callback'):
            skip = -2 if packet.has_high_level() else 0
            name = packet.get_name(skip=skip).camel
            params = '; '.join(packet.get_delphi_parameters('doc', high_level=True))
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_delphi_type(context='meta', cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).headless,
                                                     prefix_elements=[('sender', cls, 1, 'out')],
                                                     explicit_string_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_delphi_formatted_doc()

            callbacks.append(template.format(cls, name, common.wrap_non_empty('; ', params, ''), meta_table, desc))

        return ''.join(callbacks)

    def get_delphi_api(self):
        create_str = {
            'en': """
.. delphi:function:: constructor {1}.Create(const uid: string; ipcon: TIPConnection)

{3}

 Creates an object with the unique device ID ``uid``:

 .. code-block:: delphi

    {2} := {1}.Create('YOUR_DEVICE_UID', ipcon);

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_delphi_examples>`).
""",
            'de': """
.. delphi:function:: constructor {1}.Create(const uid: string; ipcon: TIPConnection)

{3}

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: delphi

    {2} := {1}.Create('YOUR_DEVICE_UID', ipcon);

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_delphi_examples>`).
"""
        }

        c_str = {
            'en': """
.. _{0}_delphi_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive time critical or recurring data from
the device. The registration is done by assigning a procedure to an callback
property of the device object:

 .. code-block:: delphi

  procedure TExample.MyCallback(sender: {1}; const value: longint);
  begin
    WriteLn(Format('Value: %d', [value]));
  end;

  {2}.OnExample := {{$ifdef FPC}}@{{$endif}}example.MyCallback;

The available callback properties and their parameter types are described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{3}
""",
            'de': """
.. _{0}_delphi_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische oder
wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung erfolgt indem
eine Prozedur einem Callback Property des Geräte Objektes zugewiesen wird:

 .. code-block:: delphi

  procedure TExample.MyCallback(sender: {1}; const value: longint);
  begin
    WriteLn(Format('Value: %d', [value]));
  end;

  {2}.OnExample := {{$ifdef FPC}}@{{$endif}}example.MyCallback;

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
.. _{0}_delphi_api:

API
---

Since Delphi does not support multiple return values directly, we use the
``out`` keyword to return multiple values from a function.

All functions and procedures listed below are thread-safe.

{1}

{2}
""",
            'de': """
.. _{0}_delphi_api:

API
---

Da Delphi nicht mehrere Rückgabewerte direkt unterstützt, wird das ``out``
Schlüsselwort genutzt um mehrere Werte von einer Funktion zurückzugeben.

Alle folgend aufgelisteten Funktionen und Prozeduren sind Thread-sicher.

{1}

{2}
"""
        }

        const_str = {
            'en': """
.. _{0}_delphi_constants:

Constants
^^^^^^^^^

.. delphi:function:: const {1}_{2}_DEVICE_IDENTIFIER

 This constant is used to identify a {4}.

 The :delphi:func:`GetIdentity <{5}.GetIdentity>` function and the
 :delphi:func:`TIPConnection.OnEnumerate <TIPConnection.OnEnumerate>`
 callback of the IP Connection have a ``deviceIdentifier`` parameter to specify
 the Brick's or Bricklet's type.

.. delphi:function:: const {1}_{2}_DEVICE_DISPLAY_NAME

 This constant represents the human readable name of a {4}.
""",
            'de': """
.. _{0}_delphi_constants:

Konstanten
^^^^^^^^^^

.. delphi:function:: const {1}_{2}_DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {3} {4} zu identifizieren.

 Die :delphi:func:`GetIdentity <{5}.GetIdentity>` Funktion und der
 :delphi:func:`TIPConnection.OnEnumerate <TIPConnection.OnEnumerate>`
 Callback der IP Connection haben ein ``deviceIdentifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. delphi:function:: const {1}_{2}_DEVICE_DISPLAY_NAME

 Diese Konstante stellt den Anzeigenamen eines {4} dar.
"""
        }

        create_meta = common.format_simple_element_meta([('uid', 'string', 1, 'in'),
                                                         ('ipcon', 'TIPConnection', 1, 'in'),
                                                         (self.get_name().headless, self.get_delphi_class_name(), 1, 'out')])
        create_meta_table = common.make_rst_meta_table(create_meta)

        cre = common.select_lang(create_str).format(self.get_doc_rst_ref_name(),
                                                    self.get_delphi_class_name(),
                                                    self.get_name().headless,
                                                    create_meta_table)

        bf = self.get_delphi_functions('bf')
        af = self.get_delphi_functions('af')
        ccf = self.get_delphi_functions('ccf')
        c = self.get_delphi_callbacks()
        vf = self.get_delphi_functions('vf')
        if_ = self.get_delphi_functions('if')
        api_str = ''

        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)

        if af:
            api_str += common.select_lang(common.af_str).format(af)

        if c:
            if ccf:
                api_str += common.select_lang(common.ccf_str).format('', ccf)

            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_delphi_class_name(),
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
                                                        self.get_category().upper,
                                                        self.get_name().upper,
                                                        article,
                                                        self.get_long_display_name(),
                                                        self.get_delphi_class_name())

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.specialize_delphi_doc_function_links(common.select_lang(self.get_doc())),
                                              api_str)

    def get_delphi_doc(self):
        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += self.get_delphi_examples()
        doc += self.get_delphi_api()

        return doc

class DelphiBindingsPacket(delphi_common.DelphiPacket):
    def get_delphi_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())
        text = self.get_device().specialize_delphi_doc_function_links(text)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = '{0}_{1}_'.format(self.get_device().get_category().upper,
                                   self.get_device().get_name().upper)

        def format_element_name(element, index):
            if index == None:
                return element.get_name().headless

            return '{0}[{1}]'.format(element.get_name().headless, index)

        text += common.format_constants(prefix, self, format_element_name)
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

class DelphiDocGenerator(delphi_common.DelphiGeneratorTrait, common.DocGenerator):
    def get_doc_rst_filename_part(self):
        return 'Delphi'

    def get_doc_example_regex(self):
        return r'^Example.*\.pas$'

    def get_device_class(self):
        return DelphiBindingsDevice

    def get_packet_class(self):
        return DelphiBindingsPacket

    def get_element_class(self):
        return delphi_common.DelphiElement

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_delphi_doc())

def generate(root_dir, language):
    common.generate(root_dir, language, DelphiDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print('=== Generating %s ===' % language)
        generate(os.getcwd(), language)
