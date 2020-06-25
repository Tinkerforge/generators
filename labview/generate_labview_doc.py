#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LabVIEW Documentation Generator
Copyright (C) 2012-2015, 2017-2019 Matthias Bolte <matthias@tinkerforge.com>
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

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import shutil
import subprocess
import glob
import re
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

class LabVIEWDocDevice(common.Device):
    def get_labview_class_name(self):
        return self.get_category().camel + self.get_name().camel

    def specialize_labview_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':labview:func:`{1}Callback <{0}.{1}Callback>`'.format(packet.get_device().get_labview_class_name(),
                                                                              packet.get_name(skip=-2 if high_level else 0).camel)
            else:
                return ':labview:func:`{1}() <{0}.{1}>`'.format(packet.get_device().get_labview_class_name(),
                                                                packet.get_name(skip=-2 if high_level else 0).camel)

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

    def get_labview_functions(self, type_):
        functions = []
        template = '.. labview:function:: {0}.{1}({2}){3}\n\n{4}{5}\n'
        cls = self.get_labview_class_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type_:
                continue

            skip = -2 if packet.has_high_level() else 0
            name = packet.get_name(skip=skip).camel
            inputs = packet.get_labview_parameter_list('in', high_level=True)
            outputs = packet.get_labview_parameter_list('out', high_level=True)
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_labview_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).headless,
                                                     parameter_label_override={'en': 'Input', 'de': 'Eingabe'},
                                                     return_label_override={'en': 'Output', 'de': 'Ausgabe'},
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            doc = packet.get_labview_formatted_doc()

            functions.append(template.format(cls, name, inputs, common.wrap_non_empty(' ->  ', outputs, ''), meta_table, doc))

        return ''.join(functions)

    def get_labview_callbacks(self):
        callbacks = []
        template = '.. labview:function:: event {0}.{1}Callback -> sender{2}\n\n{3}{4}\n'

        for packet in self.get_packets('callback'):
            skip = -2 if packet.has_high_level() else 0
            outputs = packet.get_labview_parameter_list('out', high_level=True)
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_labview_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).headless,
                                                     prefix_elements=[('sender', '.NET Refnum ({0})'.format(self.get_labview_class_name()), 1, 'out')],
                                                     callback_parameter_label_override={'en': 'Callback Output', 'de': 'Callback-Ausgabe'},
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            doc = packet.get_labview_formatted_doc()

            callbacks.append(template.format(self.get_labview_class_name(),
                                             packet.get_name(skip=skip).camel,
                                             common.wrap_non_empty(', ', outputs, ''),
                                             meta_table,
                                             doc))

        return ''.join(callbacks)

    def get_labview_api(self):
        create_str = {
        'en': """
.. labview:function:: {0}(uid, ipcon) -> {1}

{2}

 Creates an object with the unique device ID ``uid``.
 This object can then be used after the IP Connection is connected.
""",
        'de': """
.. labview:function:: {0}(uid, ipcon) -> {1}

{2}

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``.
 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist.
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

Generally, every function of the LabVIEW bindings that outputs a value can
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
 :labview:func:`IPConnection.EnumerateCallback <IPConnection.EnumerateCallback>`
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
 :labview:func:`IPConnection.EnumerateCallback <IPConnection.EnumerateCallback>`
 Callback der IP Connection haben ein ``deviceIdentifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. labview:symbol:: {1}.DEVICE_DISPLAY_NAME

 Diese Konstante stellt den Anzeigenamen eines {3} dar.
"""
        }

        create_meta = common.format_simple_element_meta([('uid', 'String', 1, 'in'),
                                                         ('ipcon', '.NET Refnum (IPConnection)', 1, 'in'),
                                                         (self.get_name().headless, '.NET Refnum ({0})'.format(self.get_labview_class_name()), 1, 'out')],
                                                        parameter_label_override={'en': 'Input', 'de': 'Eingabe'},
                                                        return_label_override={'en': 'Output', 'de': 'Ausgabe'})
        create_meta_table = common.make_rst_meta_table(create_meta)

        cre = common.select_lang(create_str).format(self.get_labview_class_name(),
                                                    self.get_name().headless,
                                                    create_meta_table)

        bf = self.get_labview_functions('bf')
        af = self.get_labview_functions('af')
        ccf = self.get_labview_functions('ccf')
        c = self.get_labview_callbacks()
        vf = self.get_labview_functions('vf')
        if_ = self.get_labview_functions('if')
        api_str = ''

        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)

        if af:
            api_str += common.select_lang(common.af_str).format(af)

        if c:
            if ccf:
                api_str += common.select_lang(common.ccf_str).format('', ccf)

            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        c)

        if vf:
            api_str += common.select_lang(common.vf_str).format(vf)

        if if_:
            api_str += common.select_lang(common.if_str).format(if_)

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

        def format_element_name(element, index):
            if index == None:
                return element.get_name().headless

            return '{0}[{1}]'.format(element.get_name().headless, index)

        text += common.format_constants(prefix, self, format_element_name)
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

    def get_labview_parameter_list(self, direction, high_level=False):
        parameter = []

        for element in self.get_elements(direction=direction, high_level=high_level):
            parameter.append(element.get_name().headless)

        return ', '.join(parameter)

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
            return str(bool(value))[0]

        if type_ in ['char', 'string']:
            return '"{0}"'.format(value.replace('"', '\\"'))

        return str(value)

    def get_labview_type(self, cardinality=None):
        assert cardinality == None or (isinstance(cardinality, int) and cardinality > 0), cardinality

        labview_type = LabVIEWDocElement.labview_types[self.get_type()]

        if cardinality == None:
            cardinality = self.get_cardinality()

        if cardinality > 1 and labview_type != 'String':
            labview_type += '[{0}]'.format(cardinality)
        elif cardinality < 0:
            labview_type += '[]'

        return labview_type

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

    def get_doc_null_value_name(self):
        return 'null'

    def get_doc_formatted_param(self, element):
        return element.get_name().headless

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_labview_doc())

def generate(root_dir, language):
    common.generate(root_dir, language, LabVIEWDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print('=== Generating %s ===' % language)
        generate(os.getcwd(), language)
