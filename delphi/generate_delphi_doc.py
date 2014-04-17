#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Delphi Documentation Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_delphi_doc.py: Generator for Delphi documentation

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
import delphi_common

class DelphiBindingsDevice(delphi_common.DelphiDevice):
    def get_delphi_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('Example', '').replace('.pas', '')
            return common.camel_case_to_space(filename)

        return common.make_rst_examples(title_from_filename, self)

    def get_delphi_methods(self, typ):
        methods = ''
        function = '.. delphi:function:: function {0}.{1}({2}): {3}\n{4}'
        procedure = '.. delphi:function:: procedure {0}.{1}({2})\n{3}'
        cls = self.get_delphi_class_name()
        for packet in self.get_packets('function'):
            if packet.get_doc()[0] != typ:
                continue

            ret_type = packet.get_delphi_return_type(True)
            name = packet.get_camel_case_name()
            params = packet.get_delphi_parameter_list(True)
            desc = packet.get_delphi_formatted_doc()
            if len(ret_type) > 0:
                method = function.format(cls, name, params, ret_type, desc)
            else:
                method = procedure.format(cls, name, params, desc)
            methods += method + '\n'

        return methods

    def get_delphi_callbacks(self):
        cbs = ''
        cb = {
        'en': """.. delphi:function:: property {0}.On{1}

 .. code-block:: delphi

  procedure(sender: {0}{4}{2}) of object;

{3}
""",
        'de': """.. delphi:function:: property {0}.On{1}

 .. code-block:: delphi

  procedure(sender: {0}{4}{2}) of object;

{3}
"""
        }

        cls = self.get_delphi_class_name()
        for packet in self.get_packets('callback'):
            name = packet.get_camel_case_name()
            params = packet.get_delphi_parameter_list(True)
            desc = packet.get_delphi_formatted_doc()
            semi = ''
            if len(params) > 0:
                semi = '; '
            cbs += common.select_lang(cb).format(cls, name, params, desc, semi)

        return cbs

    def get_delphi_api(self):
        create_str = {
        'en': """
.. delphi:function:: constructor T{3}{1}.Create(const uid: string; ipcon: TIPConnection)

 Creates an object with the unique device ID ``uid``:

 .. code-block:: delphi

    {4} := T{3}{1}.Create('YOUR_DEVICE_UID', ipcon);

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_{2}_delphi_examples>`).
""",
        'de': """
.. delphi:function:: constructor T{3}{1}.Create(const uid: string; ipcon: TIPConnection)

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: delphi

    {4} := T{3}{1}.Create('YOUR_DEVICE_UID', ipcon);

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_{2}_delphi_examples>`).
"""
        }

        c_str = {
        'en': """
.. _{1}_{2}_delphi_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive time critical or recurring data from
the device. The registration is done by assigning a procedure to an callback
property of the device object:

 .. code-block:: delphi

  procedure TExample.MyCallback(sender: {3}; const param: word);
  begin
    WriteLn(param);
  end;

  {4}.OnExample := {{$ifdef FPC}}@{{$endif}}example.MyCallback;

The available callback property and their type of parameters are described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{0}
""",
        'de': """
.. _{1}_{2}_delphi_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische oder
wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung erfolgt indem
eine Prozedur einem Callback Property des Geräte Objektes zugewiesen wird:

 .. code-block:: delphi

  procedure TExample.MyCallback(sender: {3}; const param: word);
  begin
    WriteLn(param);
  end;

  {4}.OnExample := {{$ifdef FPC}}@{{$endif}}example.MyCallback;

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

Since Delphi does not support multiple return values directly, we use the
``out`` keyword to return multiple values from a function.

All functions and procedures listed below are thread-safe.

{1}

{2}
""",
        'de': """
{0}
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
        'en' : """
.. _{5}_{6}_delphi_constants:

Constants
^^^^^^^^^

.. delphi:function:: const {1}_{0}_DEVICE_IDENTIFIER

 This constant is used to identify a {3} {4}.

 The :delphi:func:`GetIdentity <T{4}{3}.GetIdentity>` function and the
 :delphi:func:`OnEnumerate <TIPConnection.OnEnumerate>`
 callback of the IP Connection have a ``deviceIdentifier`` parameter to specify
 the Brick's or Bricklet's type.
""",
        'de' : """
.. _{5}_{6}_delphi_constants:

Konstanten
^^^^^^^^^^

.. delphi:function:: const {1}_{0}_DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {3} {4} zu identifizieren.

 Die :delphi:func:`GetIdentity <T{4}{3}.GetIdentity>` Funktion und der
 :delphi:func:`OnEnumerate <TIPConnection.OnEnumerate>`
 Callback der IP Connection haben ein ``deviceIdentifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.
"""
        }

        cre = common.select_lang(create_str).format(self.get_underscore_name(),
                                                    self.get_camel_case_name(),
                                                    self.get_category().lower(),
                                                    self.get_category(),
                                                    self.get_headless_camel_case_name())

        bf = self.get_delphi_methods('bf')
        af = self.get_delphi_methods('af')
        ccf = self.get_delphi_methods('ccf')
        c = self.get_delphi_callbacks()
        api_str = ''
        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)
        if af:
            api_str += common.select_lang(common.af_str).format(af)
        if c:
            api_str += common.select_lang(common.ccf_str).format(ccf, '')
            api_str += common.select_lang(c_str).format(c, self.get_underscore_name(),
                                                        self.get_category().lower(),
                                                        self.get_delphi_class_name(),
                                                        self.get_headless_camel_case_name())

        article = 'ein'
        if self.get_category() == 'Brick':
            article = 'einen'
        api_str += common.select_lang(const_str).format(self.get_upper_case_name(),
                                                        self.get_category().upper(),
                                                        article,
                                                        self.get_camel_case_name(),
                                                        self.get_category(),
                                                        self.get_underscore_name(),
                                                        self.get_category().lower())

        ref = '.. _{0}_{1}_delphi_api:\n'.format(self.get_underscore_name(),
                                                 self.get_category().lower())

        return common.select_lang(api).format(ref, self.get_api_doc(), api_str)

    def get_delphi_doc(self):
        title = { 'en': 'Delphi/Lazarus bindings', 'de': 'Delphi/Lazarus Bindings' }

        doc  = common.make_rst_header(self, self.get_generator().get_bindings_display_name())
        doc += common.make_rst_summary(self, common.select_lang(title))
        doc += self.get_delphi_examples()
        doc += self.get_delphi_api()

        return doc

class DelphiBindingsPacket(delphi_common.DelphiPacket):
    def get_delphi_formatted_doc(self):
        text = common.select_lang(self.get_doc()[1])

        cls = self.get_device().get_delphi_class_name()
        for other_packet in self.get_device().get_packets():
            name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
            name = other_packet.get_camel_case_name()
            if other_packet.get_type() == 'callback':
                name_right = ':delphi:func:`On{1} <{0}.On{1}>`'.format(cls, name)
            else:
                name_right = ':delphi:func:`{1} <{0}.{1}>`'.format(cls, name)
            text = text.replace(name_false, name_right)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = '{0}_{1}_'.format(self.get_device().get_category().upper(),
                                   self.get_device().get_upper_case_name())
        if self.get_underscore_name() == 'set_response_expected':
            text += common.format_function_id_constants(prefix, self.get_device())
        else:
            text += common.format_constants(prefix, self)

        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

class DelphiDocGenerator(common.DocGenerator):
    def get_bindings_name(self):
        return 'delphi'

    def get_bindings_display_name(self):
        return 'Delphi/Lazarus'

    def get_doc_rst_filename_part(self):
        return 'Delphi'

    def get_doc_example_regex(self):
        return '^Example.*\.pas$'

    def get_device_class(self):
        return DelphiBindingsDevice

    def get_packet_class(self):
        return DelphiBindingsPacket

    def get_element_class(self):
        return delphi_common.DelphiElement

    def generate(self, device):
        rst = open(device.get_doc_rst_path(), 'wb')
        rst.write(device.get_delphi_doc())
        rst.close()

def generate(bindings_root_directory, language):
    common.generate(bindings_root_directory, language, DelphiDocGenerator)

if __name__ == "__main__":
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
