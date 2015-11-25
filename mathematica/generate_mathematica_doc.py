#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mathematica Documentation Generator
Copyright (C) 2012-2015 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_mathematica_doc.py: Generator for Mathematica documentation

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

class MathematicaDocDevice(common.Device):
    def get_mathematica_class_name(self):
        return self.get_camel_case_category() + self.get_camel_case_name()

    def replace_mathematica_function_links(self, text):
        cls = self.get_mathematica_class_name()
        for other_packet in self.get_packets():
            name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
            name = other_packet.get_camel_case_name()
            if other_packet.get_type() == 'callback':
                name_right = ':mathematica:func:`{1} <{0}@{1}>`'.format(cls, name)
            else:
                name_right = ':mathematica:func:`{1}[] <{0}@{1}>`'.format(cls, name)

            text = text.replace(name_false, name_right)

        return text

    def get_mathematica_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('Example', '').replace('.nb.txt', '')
            return common.camel_case_to_space(filename)

        def url_fixer(url):
            return url.replace('.nb.txt', '.nb')

        def display_name_fixer(url):
            return url.replace('.nb.txt', '.nb')

        return common.make_rst_examples(title_from_filename, self,
                                        url_fixer=url_fixer, display_name_fixer=display_name_fixer)

    def get_mathematica_functions(self, type):
        function = '.. mathematica:function:: {0}@{1}[{2}] -> {3}\n{4}{5}{6}\n'
        functions = []
        cls = self.get_mathematica_class_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type:
                continue

            name = packet.get_camel_case_name()
            params = packet.get_mathematica_parameter_list()
            param_desc = packet.get_mathematica_parameter_description()
            ret = packet.get_mathematica_return()
            ret_desc = packet.get_mathematica_return_description()
            doc = packet.get_mathematica_formatted_doc()

            functions.append(function.format(cls, name, params, ret, param_desc, ret_desc, doc))

        return ''.join(functions)

    def get_mathematica_callbacks(self):
        callback = """
.. mathematica:function:: event {0}@{1}[sender{2}]

 :param sender: NETObject[{0}]{3}{4}
"""
        callbacks = []

        for packet in self.get_packets('callback'):
            params = packet.get_mathematica_parameter_list()
            params_desc = packet.get_mathematica_parameter_description()
            doc = packet.get_mathematica_formatted_doc()

            if len(params) > 0:
                params = ', ' + params

            callbacks.append(callback.format(self.get_mathematica_class_name(),
                                             packet.get_camel_case_name(),
                                             params,
                                             params_desc,
                                             doc))

        return ''.join(callbacks)

    def get_mathematica_api(self):
        create_str = {
        'en': """
.. mathematica:function:: {1}[uid, ipcon] -> {2}

 :param uid: String
 :param ipcon: NETObject[IPConnection]
 :ret {2}: NETObject[{1}]

 Creates an object with the unique device ID ``uid``:

 .. code-block:: mathematica

    {2}=NETNew["Tinkerforge.{1}","YOUR_DEVICE_UID",ipcon]

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_mathematica_examples>`).

 The .NET runtime has built-in garbage collection that frees objects that are
 no longer in use by a program. But because Mathematica can not automatically
 tell when a Mathematica "program" doesn't use a .NET object anymore, this has
 to be done by the program. For this the `ReleaseNETObject[]
 <http://reference.wolfram.com/language/NETLink/ref/ReleaseNETObject.html>`__
 function is used in the examples.

 For further information about object management in .NET/Link see the
 corresponding Mathematica `.NET/Link documentation
 <http://reference.wolfram.com/language/NETLink/tutorial/CallingNETFromTheWolframLanguage.html#14400>`__.
""",
        'de': """
.. mathematica:function:: {1}[uid, ipcon] -> {2}

 :param uid: String
 :param ipcon: NETObject[IPConnection]
 :ret {2}: NETObject[{1}]

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: mathematica

    {2}=NETNew["Tinkerforge.{1}","YOUR_DEVICE_UID",ipcon]

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_mathematica_examples>`).

 Die .NET Runtime hat eingebauten Garbage Collection welche Objekte wieder
 freigibt, wenn sie vom Programm nicht mehr verwendet werden. Da Mathematica
 aber selbst nicht automatisch feststellen kann, wann ein Mathematica "Programm"
 ein .NET Objekt nicht mehr verwendet, muss sich das Programm selbst darum
 kümmern. Für diesen Zweck wird die `ReleaseNETObject[]
 <http://reference.wolfram.com/language/NETLink/ref/ReleaseNETObject.html>`__
 Funktion in den Beispielen verwendet.

 Weitere Informationen über Objekt-Verwaltung mittels .NET/Link sind in der
 entsprechende Mathematica `.NET/Link Dokumentation
 <http://reference.wolfram.com/language/NETLink/tutorial/CallingNETFromTheWolframLanguage.html#14400>`__
 zu finden.
"""
        }

        c_str = {
        'en': """
.. _{0}_mathematica_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive time critical or recurring data from
the device. The registration is done by assigning a function to a callback
property of the device object:

 .. code-block:: mathematica

    Callback[sender_,value_]:=Print["Value: "<>ToString[value]]

    AddEventHandler[{1}@Example,Callback]

For further information about event handling using .NET/Link see the
corresponding Mathematica `.NET/Link documentation
<http://reference.wolfram.com/language/NETLink/tutorial/CallingNETFromTheWolframLanguage.html#17034>`__.

The available callback property and their type of parameters are described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{2}
""",
        'de': """
.. _{0}_mathematica_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische oder
wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung erfolgt indem
eine Funktion einem Callback Property des Geräte Objektes zugewiesen wird:

 .. code-block:: mathematica

    Callback[sender_,value_]:=Print["Value: "<>ToString[value]]

    AddEventHandler[{1}@Example,Callback]

Weitere Informationen über Event-Behandlung mittels .NET/Link sind in der
entsprechende Mathematica `.NET/Link Dokumentation
<http://reference.wolfram.com/language/NETLink/tutorial/CallingNETFromTheWolframLanguage.html#17034>`__
zu finden.

Die verfügbaren Callback Properties und ihre Parametertypen werden weiter
unten beschrieben.

.. note::
 Callbacks für wiederkehrende Ereignisse zu verwenden ist
 *immer* zu bevorzugen gegenüber der Verwendung von Abfragen.
 Es wird weniger USB-Bandbreite benutzt und die Latenz ist
 erheblich geringer, da es keine Paketumlaufzeit gibt.

{2}
"""
        }

        api = {
        'en': """
.. _{0}_mathematica_api:

API
---

Generally, every method of the Mathematica bindings that returns a value can
throw a ``Tinkerforge.TimeoutException``. This exception gets thrown if the
device did not respond. If a cable based connection is used, it is
unlikely that this exception gets thrown (assuming nobody plugs the
device out). However, if a wireless connection is used, timeouts will occur
if the distance to the device gets too big.

Since .NET/Link does not support multiple return values directly, we use the
``out`` keyword to return multiple values from a method. For further
information about the ``out`` keyword in .NET/Link see the corresponding
Mathematica `.NET/Link documentation
<http://reference.wolfram.com/language/NETLink/tutorial/CallingNETFromTheWolframLanguage.html#15993>`__.

The namespace for all Brick/Bricklet bindings and the IPConnection is
``Tinkerforge.*``.

{1}

{2}
""",
        'de': """
.. _{0}_mathematica_api:

API
---

Prinzipiell kann jede Funktion der Mathematica Bindings, welche einen Wert zurück gibt
eine ``Tinkerforge.TimeoutException`` werfen. Diese Exception wird
geworfen wenn das Gerät nicht antwortet. Wenn eine Kabelverbindung genutzt
wird, ist es unwahrscheinlich, dass die Exception geworfen wird (unter der
Annahme, dass das Gerät nicht abgesteckt wird). Bei einer drahtlosen Verbindung
können Zeitüberschreitungen auftreten, sobald die Entfernung zum Gerät zu
groß wird.

Da .NET/Link nicht mehrere Rückgabewerte direkt unterstützt, wird das ``out``
Schlüsselwort genutzt, um mehrere Werte aus einer Funktion zurückzugeben.
Weitere Informationen über das ``out`` Schlüsselwort in .NET/Link sind in der
entsprechende Mathematica `.NET/Link Dokumentation
<http://reference.wolfram.com/language/NETLink/tutorial/CallingNETFromTheWolframLanguage.html#15993>`__
zu finden.

Der Namensraum für alle Brick/Bricklet Bindings und die IPConnection ist
``Tinkerforge.*``.

{1}

{2}
"""
        }

        const_str = {
        'en': """
.. _{0}_mathematica_constants:

Constants
^^^^^^^^^

.. mathematica:symbol:: {1}`DEVICEUIDENTIFIER

 This constant is used to identify a {3}.

 The :mathematica:func:`GetIdentity[] <{1}@GetIdentity>` function and the
 :mathematica:func:`EnumerateCallback <IPConnection@EnumerateCallback>`
 callback of the IP Connection have a ``deviceIdentifier`` parameter to specify
 the Brick's or Bricklet's type.

.. mathematica:symbol:: {1}`DEVICEDISPLAYNAME

 This constant represents the human readable name of a {3}.
""",
        'de': """
.. _{0}_mathematica_constants:

Konstanten
^^^^^^^^^^

.. mathematica:symbol:: {1}`DEVICEUIDENTIFIER

 Diese Konstante wird verwendet um {2} {3} zu identifizieren.

 Die :mathematica:func:`GetIdentity[] <{1}@GetIdentity>` Funktion und der
 :mathematica:func:`EnumerateCallback <IPConnection@EnumerateCallback>`
 Callback der IP Connection haben ein ``deviceIdentifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. mathematica:symbol:: {1}`DEVICEDISPLAYNAME

 Diese Konstante stellt den Anzeigenamen eines {3} dar.
"""
        }

        cre = common.select_lang(create_str).format(self.get_doc_rst_ref_name(),
                                                    self.get_mathematica_class_name(),
                                                    self.get_headless_camel_case_name())

        bf = self.get_mathematica_functions('bf')
        af = self.get_mathematica_functions('af')
        ccf = self.get_mathematica_functions('ccf')
        c = self.get_mathematica_callbacks()
        api_str = ''
        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)
        if af:
            api_str += common.select_lang(common.af_str).format(af)
        if ccf:
            api_str += common.select_lang(common.ccf_str).format('', ccf)
        if c:
            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_headless_camel_case_name(),
                                                        c)

        article = 'ein'
        if self.is_brick():
            article = 'einen'
        api_str += common.select_lang(const_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_mathematica_class_name(),
                                                        article,
                                                        self.get_long_display_name())

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.replace_mathematica_function_links(self.get_api_doc()),
                                              api_str)

    def get_mathematica_doc(self):
        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += self.get_mathematica_examples()
        doc += self.get_mathematica_api()

        return doc

class MathematicaDocPacket(common.Packet):
    def get_mathematica_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())

        text = self.get_device().replace_mathematica_function_links(text)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = self.get_device().get_mathematica_class_name() + '`'
        if self.get_underscore_name() == 'set_response_expected':
            text += common.format_function_id_constants(prefix, self.get_device()).replace('_', 'U')
        else:
            def constant_format(prefix, constant_group, constant, value):
                return '* {0}{1}U{2} = {3}\n'.format(prefix, constant_group.get_upper_case_name().replace('_', 'U'),
                                                     constant.get_upper_case_name().replace('_', 'U'), value)

            text += common.format_constants(prefix, self, char_format='``ToCharacterCode["{0}"][[0]]``',
                                            constant_format_func=constant_format)

        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

    def get_mathematica_parameter_list(self):
        params = []

        if len(self.get_elements('out')) > 1 or self.get_type() == 'callback':
            for element in self.get_elements():
                if element.get_direction() == 'in' or self.get_type() == 'callback':
                    modifier = ''
                else:
                    modifier = 'out '

                params.append(modifier + element.get_mathematica_signature_name())
        else:
            for element in self.get_elements('in'):
                params.append(element.get_mathematica_signature_name())

        return ', '.join(params)

    def get_mathematica_parameter_description(self):
        descriptions = []
        normal_return = len(self.get_elements('out')) <= 1

        for element in self.get_elements():
            if self.get_type() == 'function' and normal_return and element.get_direction() == 'out':
                continue

            name = element.get_mathematica_description_name()
            type = element.get_mathematica_type()

            descriptions.append(' :param {0}: {1}\n'.format(name, type))

        return '\n' + ''.join(descriptions)

    def get_mathematica_return(self):
        if len(self.get_elements('out')) == 1 and self.get_type() == 'function':
            element = self.get_elements('out')[0]

            return element.get_mathematica_signature_name()
        else:
            return 'Null'

    def get_mathematica_return_description(self):
        if len(self.get_elements('out')) == 1 and self.get_type() == 'function':
            element = self.get_elements('out')[0]
            name = element.get_mathematica_description_name()
            type = element.get_mathematica_type()

            return ' :ret {0}: {1}\n'.format(name, type)
        else:
            return ''

class MathematicaDocElement(common.Element):
    mathematica_types = {
        'int8':   'Integer',
        'uint8':  'Integer',
        'int16':  'Integer',
        'uint16': 'Integer',
        'int32':  'Integer',
        'uint32': 'Integer',
        'int64':  'Integer',
        'uint64': 'Integer',
        'float':  'Real',
        'bool':   'True/False',
        'char':   'Integer',
        'string': 'String'
    }

    def get_mathematica_type(self):
        return MathematicaDocElement.mathematica_types[self.get_type()]

    def get_mathematica_signature_name(self):
        name = self.get_headless_camel_case_name()

        if self.get_cardinality() > 1 and self.get_type() != 'string':
            items = []

            for i in range(self.get_cardinality()):
                items.append(name + str(i + 1))

            if len(items) > 3:
                items = [items[0]] + [items[1]] + ['...'] + [items[-1]]

            name = '{' + ', '.join(items) + '}'

        return name

    def get_mathematica_description_name(self):
        name = self.get_headless_camel_case_name()

        if self.get_cardinality() > 1 and self.get_type() != 'string':
            name += 'i'

        return name

class MathematicaDocGenerator(common.DocGenerator):
    def get_bindings_name(self):
        return 'mathematica'

    def get_bindings_display_name(self):
        return 'Mathematica'

    def get_doc_rst_filename_part(self):
        return 'Mathematica'

    def get_doc_example_regex(self):
        return '^Example.*\.nb.txt$'

    def get_device_class(self):
        return MathematicaDocDevice

    def get_packet_class(self):
        return MathematicaDocPacket

    def get_element_class(self):
        return MathematicaDocElement

    def generate(self, device):
        rst = open(device.get_doc_rst_path(), 'wb')
        rst.write(device.get_mathematica_doc())
        rst.close()

def generate(bindings_root_directory, language):
    common.generate(bindings_root_directory, language, MathematicaDocGenerator)

if __name__ == "__main__":
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
