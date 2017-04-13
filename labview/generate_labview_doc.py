#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LabVIEW Documentation Generator
Copyright (C) 2012-2015 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_labview_doc.py: Generator for LabVIEW documentation

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

class LabVIEWDocDevice(common.Device):
    def get_labview_class_name(self):
        return self.get_camel_case_category() + self.get_camel_case_name()

    def specialize_labview_doc_function_links(self, text):
        def specializer(packet):
            if packet.get_type() == 'callback':
                return ':labview:func:`{1}Callback <{0}.{1}Callback>`'.format(packet.get_device().get_labview_class_name(),
                                                                              packet.get_camel_case_name())
            else:
                return ':labview:func:`{1}() <{0}.{1}>`'.format(packet.get_device().get_labview_class_name(),
                                                                packet.get_camel_case_name())

        return self.specialize_doc_rst_links(text, specializer, prefix='labview')

    def get_labview_examples(self):
        def title_from_filename(filename):
            return filename.replace('Example ', '').replace('.vi.png', '')

        def url_fixer(url):
            return url.replace('.vi.png', '.vi')

        def display_name_fixer(display_name):
            return display_name.replace('.vi.png', '.vi')

        def additional_download_finder(file_path):
            # if file name is "Example Callback - Event Callback.vi" then
            # glob for "Example Callback - *"

            dir_name, filename = os.path.split(file_path)
            additional_downloads = []
            pattern = os.path.join(dir_name, filename.replace('.vi.png', '') + ' - *')

            for additional_file_path in glob.glob(pattern):
                additional_downloads.append(os.path.split(additional_file_path)[1])
            return additional_downloads

        return common.make_rst_examples(title_from_filename, self,
                                        url_fixer=url_fixer, is_picture=True,
                                        additional_download_finder=additional_download_finder,
                                        display_name_fixer=display_name_fixer)

    def get_labview_functions(self, type):
        function = '.. labview:function:: {0}.{1}({2}){3}\n{4}{5}{6}\n'
        functions = []
        cls = self.get_labview_class_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type:
                continue

            name = packet.get_camel_case_name()
            inputs = packet.get_labview_input_list()
            input_desc = packet.get_labview_input_description()
            outputs = packet.get_labview_output_list()
            output_desc = packet.get_labview_output_description()
            doc = packet.get_labview_formatted_doc()

            if len(outputs) > 0:
                outputs = ' -> ' + outputs

            functions.append(function.format(cls, name, inputs, outputs, input_desc, output_desc, doc))

        return ''.join(functions)

    def get_labview_callbacks(self):
        callback = """
.. labview:function:: event {0}.{1}Callback(sender{2})

 :input sender: .NET Refnum ({0}){3}{4}
"""
        callbacks = []

        for packet in self.get_packets('callback'):
            inputs = packet.get_labview_input_list()
            input_desc = packet.get_labview_input_description()
            doc = packet.get_labview_formatted_doc()

            if len(inputs) > 0:
                inputs = ', ' + inputs

            callbacks.append(callback.format(self.get_labview_class_name(),
                                             packet.get_camel_case_name(),
                                             inputs,
                                             input_desc,
                                             doc))

        return ''.join(callbacks)

    def get_labview_api(self):
        create_str = {
        'en': """
.. labview:function:: {1}(uid, ipcon) -> {2}

 :input uid: String
 :input ipcon: .NET Refnum (IPConnection)
 :output {2}: .NET Refnum ({1})

 Creates an object with the unique device ID ``uid``.
 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_labview_examples>`).
""",
        'de': """
.. labview:function:: {1}(uid, ipcon) -> {2}

 :input uid: String
 :input ipcon: .NET Refnum (IPConnection)
 :output {2}: .NET Refnum ({1})

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``.
 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_labview_examples>`).
"""
        }

        c_str = {
        'en': """
.. _{0}_labview_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive time critical or recurring data from
the device. The registration is done by assigning a function to a callback
property of the device object. The available callback property and their type
of parameters are described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{1}
""",
        'de': """
.. _{0}_labview_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische oder
wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung erfolgt indem
eine Funktion einem Callback Property des Geräte Objektes zugewiesen wird.
Die verfügbaren Callback Properties und ihre Parametertypen werden weiter
unten beschrieben.

.. note::
 Callbacks für wiederkehrende Ereignisse zu verwenden ist
 *immer* zu bevorzugen gegenüber der Verwendung von Abfragen.
 Es wird weniger USB-Bandbreite benutzt und die Latenz ist
 erheblich geringer, da es keine Paketumlaufzeit gibt.

{1}
"""
        }

        api = {
        'en': """
.. _{0}_labview_api:

API
---

Generally, every method of the LabVIEW bindings that outputs a value can
report a ``Tinkerforge.TimeoutException``. This error gets reported if the
device did not respond. If a cable based connection is used, it is
unlikely that this exception gets thrown (assuming nobody plugs the
device out). However, if a wireless connection is used, timeouts will occur
if the distance to the device gets too big.

The namespace for all Brick/Bricklet bindings and the IPConnection is
``Tinkerforge.*``.

{1}

{2}
""",
        'de': """
.. _{0}_labview_api:

API
---

Prinzipiell kann jede Funktion der LabVIEW Bindings, welche einen Wert ausgibt
eine ``Tinkerforge.TimeoutException`` melden. Dieser Fehler wird
gemeldet wenn das Gerät nicht antwortet. Wenn eine Kabelverbindung genutzt
wird, ist es unwahrscheinlich, dass die Exception geworfen wird (unter der
Annahme, dass das Gerät nicht abgesteckt wird). Bei einer drahtlosen Verbindung
können Zeitüberschreitungen auftreten, sobald die Entfernung zum Gerät zu
groß wird.

Der Namensraum für alle Brick/Bricklet Bindings und die IPConnection ist
``Tinkerforge.*``.

{1}

{2}
"""
        }

        const_str = {
        'en': """
.. _{0}_labview_constants:

Constants
^^^^^^^^^

.. labview:symbol:: {1}.DEVICE_IDENTIFIER

 This constant is used to identify a {3}.

 The :labview:func:`GetIdentity() <{1}.GetIdentity>` function and the
 :labview:func:`EnumerateCallback <IPConnection.EnumerateCallback>`
 callback of the IP Connection have a ``deviceIdentifier`` parameter to specify
 the Brick's or Bricklet's type.

.. labview:symbol:: {1}.DEVICE_DISPLAY_NAME

 This constant represents the human readable name of a {3}.
""",
        'de': """
.. _{0}_labview_constants:

Konstanten
^^^^^^^^^^

.. labview:symbol:: {1}.DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {3} zu identifizieren.

 Die :labview:func:`GetIdentity() <{1}.GetIdentity>` Funktion und der
 :labview:func:`EnumerateCallback <IPConnection.EnumerateCallback>`
 Callback der IP Connection haben ein ``deviceIdentifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. labview:symbol:: {1}.DEVICE_DISPLAY_NAME

 Diese Konstante stellt den Anzeigenamen eines {3} dar.
"""
        }

        cre = common.select_lang(create_str).format(self.get_doc_rst_ref_name(),
                                                    self.get_labview_class_name(),
                                                    self.get_headless_camel_case_name())

        bf = self.get_labview_functions('bf')
        af = self.get_labview_functions('af')
        ccf = self.get_labview_functions('ccf')
        c = self.get_labview_callbacks()
        api_str = ''
        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)
        if af:
            api_str += common.select_lang(common.af_str).format(af)
        if ccf:
            api_str += common.select_lang(common.ccf_str).format('', ccf)
        if c:
            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        c)

        article = 'ein'
        if self.is_brick():
            article = 'einen'
        api_str += common.select_lang(const_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_labview_class_name(),
                                                        article,
                                                        self.get_long_display_name())

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.specialize_labview_doc_function_links(common.select_lang(self.get_doc())),
                                              api_str)

    def get_labview_doc(self):
        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += self.get_labview_examples()
        doc += self.get_labview_api()

        return doc

class LabVIEWDocPacket(common.Packet):
    def get_labview_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())
        text = self.get_device().specialize_labview_doc_function_links(text)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = self.get_device().get_labview_class_name() + '.'
        if self.get_underscore_name() == 'set_response_expected':
            text += common.format_function_id_constants(prefix, self.get_device())
        else:
            text += common.format_constants(prefix, self)

        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

    def get_labview_input_list(self):
        inputs = []

        if self.get_type() == 'callback':
            direction = 'out'
        else:
            direction = 'in'

        for element in self.get_elements(direction):
            inputs.append(element.get_headless_camel_case_name())

        return ', '.join(inputs)

    def get_labview_input_description(self):
        descriptions = []

        if self.get_type() == 'callback':
            direction = 'out'
        else:
            direction = 'in'

        for element in self.get_elements(direction):
            name = element.get_headless_camel_case_name()
            type = element.get_labview_type()

            descriptions.append(' :input {0}: {1}\n'.format(name, type))

        return '\n' + ''.join(descriptions)

    def get_labview_output_list(self):
        outputs = []

        if self.get_type() == 'function':
            for element in self.get_elements('out'):
                outputs.append(element.get_headless_camel_case_name())

        return ', '.join(outputs)

    def get_labview_output_description(self):
        descriptions = []

        if self.get_type() == 'function':
            for element in self.get_elements('out'):
                name = element.get_headless_camel_case_name()
                type = element.get_labview_type()

                descriptions.append(' :output {0}: {1}\n'.format(name, type))

        if len(descriptions) > 0:
            return '\n' + ''.join(descriptions)
        else:
            return ''

class LabVIEWDocElement(common.Element):
    labview_types = {
        'int8':   'Int16',
        'uint8':  'Byte',
        'int16':  'Int16',
        'uint16': 'Int32',
        'int32':  'Int32',
        'uint32': 'Int64',
        'int64':  'Int64',
        'uint64': 'Int64',
        'float':  'Single',
        'bool':   'Boolean',
        'char':   'Char',
        'string': 'String'
    }

    def get_labview_type(self):
        t = LabVIEWDocElement.labview_types[self.get_type()]
        c = self.get_cardinality()

        if c > 1 and t != 'String':
            t += '[{0}]'.format(c)

        return t

class LabVIEWDocGenerator(common.DocGenerator):
    def get_bindings_name(self):
        return 'labview'

    def get_bindings_display_name(self):
        return 'LabVIEW'

    def get_doc_rst_filename_part(self):
        return 'LabVIEW'

    def get_doc_example_regex(self):
        return '^Example .*\.vi.png$'

    def get_device_class(self):
        return LabVIEWDocDevice

    def get_packet_class(self):
        return LabVIEWDocPacket

    def get_element_class(self):
        return LabVIEWDocElement

    def generate(self, device):
        rst = open(device.get_doc_rst_path(), 'wb')
        rst.write(device.get_labview_doc())
        rst.close()

def generate(bindings_root_directory, language):
    common.generate(bindings_root_directory, language, LabVIEWDocGenerator)

if __name__ == "__main__":
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
