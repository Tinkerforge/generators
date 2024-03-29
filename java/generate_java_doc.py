#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Java Documentation Generator
Copyright (C) 2012-2015, 2017-2020 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2013 Olaf Lüke <olaf@tinkerforge.com>

generate_java_doc.py: Generator for Java documentation

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
from generators.java import java_common

class JavaDocDevice(java_common.JavaDevice):
    def specialize_java_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':java:func:`{1}Listener <{0}::{1}Listener>`'.format(packet.get_device().get_java_class_name(),
                                                                            packet.get_name(skip=-2 if high_level else 0).camel)
            else:
                return ':java:func:`{1}() <{0}::{1}>`'.format(packet.get_device().get_java_class_name(),
                                                              packet.get_name(skip=-2 if high_level else 0).headless)

        return self.specialize_doc_rst_links(text, specializer, prefix='java')

    def get_java_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('Example', '').replace('.java', '')
            return common.camel_to_space(filename)

        return common.make_rst_examples(title_from_filename, self)

    def get_java_functions(self, type_):
        functions = []
        template = '.. java:function:: {0} {1}::{2}({3})\n\n{4}\n{5}\n'
        cls = self.get_java_class_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type_:
                continue

            skip = -2 if packet.has_high_level() else 0
            ret_type = packet.get_java_return_type(True, high_level=True)
            name = packet.get_name(skip=skip).headless
            params = packet.get_java_parameters(high_level=True)
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_java_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).headless,
                                                     return_object='conditional',
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_java_formatted_doc(1)

            functions.append(template.format(ret_type, cls, name, params, meta_table, desc))

        return ''.join(functions)

    def get_java_callbacks(self):
        callbacks = []
        template = {
            'en': """
.. java:function:: class {0}::{1}Listener()

 This listener can be added with the ``add{1}Listener()`` function.
 An added listener can be removed with the ``remove{1}Listener()`` function.

 .. java:function:: void {2}({3})
  :noindex:

{4}

{5}
""",
            'de': """
.. java:function:: class {0}::{1}Listener()

 Dieser Listener kann mit der Funktion ``add{1}Listener()`` hinzugefügt werden.
 Ein hinzugefügter Listener kann mit der Funktion ``remove{1}Listener()`` wieder
 entfernt werden.

 .. java:function:: void {2}({3})
  :noindex:

{4}

{5}
"""
        }
        cls = self.get_java_class_name()

        for packet in self.get_packets('callback'):
            desc = packet.get_java_formatted_doc(2)
            params = packet.get_java_parameters(high_level=True)
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_java_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).headless,
                                                     callback_parameter_label_override={'en': 'Parameters', 'de': 'Parameter'},
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta, indent_level=2)
            skip = -2 if packet.has_high_level() else 0

            callbacks.append(common.select_lang(template).format(cls,
                                                                 packet.get_name(skip=skip).camel,
                                                                 packet.get_name(skip=skip).headless,
                                                                 params,
                                                                 meta_table,
                                                                 desc))

        return ''.join(callbacks)

    def get_java_api(self):
        create_str = {
            'en': """
.. java:function:: class {0}(String uid, IPConnection ipcon)

{2}

 Creates an object with the unique device ID ``uid``:

 .. code-block:: java

  {0} {1} = new {0}("YOUR_DEVICE_UID", ipcon);

 This object can then be used after the IP Connection is connected.
""",
            'de': """
.. java:function:: class {0}(String uid, IPConnection ipcon)

{2}

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: java

  {0} {1} = new {0}("YOUR_DEVICE_UID", ipcon);

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist.
"""
        }

        ccf_str = {
            'en': """
Listener Configuration Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{0}
""",
            'de': """
Konfigurationsfunktionen für Listener
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{0}
"""
        }

        c_str = {
            'en': """
.. _{0}_java_callbacks:

Listeners
^^^^^^^^^

Listeners can be registered to receive
time critical or recurring data from the device. The registration is done
with ``add*Listener()`` functions of the device object.

The parameter is a listener class object, for example:

.. code-block:: java

    device.addExampleListener(new {1}.ExampleListener() {{
        public void property(int value) {{
            System.out.println("Value: " + value);
        }}
    }});

The available listener classes with inherent methods to be overwritten
are described below. It is possible to add several listeners and
to remove them with the corresponding ``remove*Listener()`` function.

.. note::
 Using listeners for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{2}
""",
            'de': """
.. _{0}_java_callbacks:

Listener
^^^^^^^^

Listener können registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit ``add*Listener()`` Funktionen eines Geräteobjekts durchgeführt werden.

Der Parameter ist ein Listener Klassen Objekt, z.B.:

.. code-block:: java

    device.addExampleListener(new {1}.ExampleListener() {{
        public void property(int value) {{
            System.out.println("Value: " + value);
        }}
    }});

Die verfügbaren Listener Klassen mit den Methoden welche überschrieben
werden können werden unterhalb beschrieben. Es ist möglich mehrere
Listener hinzuzufügen und auch mit einem korrespondierenden
``remove*Listener()`` wieder zu entfernen.

.. note::
 Listener für wiederkehrende Ereignisse zu verwenden ist
 *immer* zu bevorzugen gegenüber der Verwendung von Abfragen.
 Es wird weniger USB-Bandbreite benutzt und die Latenz ist
 erheblich geringer, da es keine Paketumlaufzeit gibt.

{2}
"""
        }

        api = {
            'en': """
.. _{0}_java_api:

API
---

Generally, every method of the Java bindings that returns a value can
throw a ``TimeoutException``. This exception gets thrown if the
device did not respond. If a cable based connection is used, it is
unlikely that this exception gets thrown (assuming nobody unplugs the
device). However, if a wireless connection is used, timeouts will occur
if the distance to the device gets too big.

Beside the ``TimeoutException`` there is also a ``NotConnectedException`` that
is thrown if a method needs to communicate with the device while the
IP Connection is not connected.

Since Java does not support multiple return values and return by reference
is not possible for primitive types, we use small classes that
only consist of member variables. The member variables of the returned objects
are described in the corresponding method descriptions.

The package for all Brick/Bricklet bindings and the IP Connection is
``com.tinkerforge.*``

All methods listed below are thread-safe.

{1}

{2}
""",
            'de': """
.. _{0}_java_api:

API
---

Prinzipiell kann jede Methode der Java Bindings eine ``TimeoutException``
werfen. Diese Exception wird
geworfen wenn das Gerät nicht antwortet. Wenn eine Kabelverbindung genutzt
wird, ist es unwahrscheinlich, dass die Exception geworfen wird (unter der
Annahme, dass das Gerät nicht abgesteckt wird). Bei einer drahtlosen Verbindung
können Zeitüberschreitungen auftreten, sobald die Entfernung zum Gerät zu
groß wird.

Neben der ``TimeoutException`` kann auch noch eine ``NotConnectedException``
geworfen werden, wenn versucht wird mit einem Brick oder Bricklet zu
kommunizieren, aber die IP Connection nicht verbunden ist.

Da Java nicht mehrere Rückgabewerte unterstützt und eine Referenzrückgabe
für elementare Type nicht möglich ist, werden kleine Klassen verwendet, die
nur aus Member-Variablen bestehen. Die Member-Variablen des zurückgegebenen
Objektes werden in der jeweiligen Methodenbeschreibung erläutert.

Das Package für alle Brick/Bricklet Bindings und die IP Connection ist
``com.tinkerforge.*``

Alle folgend aufgelisteten Methoden sind Thread-sicher.

{1}

{2}
"""
        }

        const_str = {
            'en': """
.. _{0}_java_constants:

Constants
^^^^^^^^^

.. java:member:: int {1}::DEVICE_IDENTIFIER

 This constant is used to identify a {3}.

 The :java:func:`getIdentity() <{1}::getIdentity>` function and the
 :java:func:`IPConnection.EnumerateListener <IPConnection::EnumerateListener>`
 listener of the IP Connection have a ``deviceIdentifier`` parameter to specify
 the Brick's or Bricklet's type.

.. java:member:: String {1}::DEVICE_DISPLAY_NAME

 This constant represents the human readable name of a {3}.
""",
            'de': """
.. _{0}_java_constants:

Konstanten
^^^^^^^^^^

.. java:member:: int {1}::DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {3} zu identifizieren.

 Die :java:func:`getIdentity() <{1}::getIdentity>` Funktion und der
 :java:func:`IPConnection.EnumerateListener <IPConnection::EnumerateListener>`
 Listener der IP Connection haben ein ``deviceIdentifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. java:member:: String {1}::DEVICE_DISPLAY_NAME

 Diese Konstante stellt den Anzeigenamen eines {3} dar.
"""
        }

        create_meta = common.format_simple_element_meta([('uid', 'String', 1, 'in'),
                                                         ('ipcon', 'IPConnection', 1, 'in'),
                                                         (self.get_name().headless, self.get_java_class_name(), 1, 'out')])
        create_meta_table = common.make_rst_meta_table(create_meta)

        cre = common.select_lang(create_str).format(self.get_java_class_name(),
                                                    self.get_name().headless,
                                                    create_meta_table)

        bf = self.get_java_functions('bf')
        af = self.get_java_functions('af')
        ccf = self.get_java_functions('ccf')
        c = self.get_java_callbacks()
        vf = self.get_java_functions('vf')
        if_ = self.get_java_functions('if')
        api_str = ''

        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)

        if af:
            api_str += common.select_lang(common.af_str).format(af)

        if c:
            if ccf:
                api_str += common.select_lang(ccf_str).format(ccf)

            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_java_class_name(),
                                                        c)

        if vf:
            api_str += common.select_lang(common.vf_str).format(vf)

        if if_:
            api_str += common.select_lang(common.if_str).format(if_)

        article = 'ein'

        if self.is_brick():
            article = 'einen'

        api_str += common.select_lang(const_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_java_class_name(),
                                                        article,
                                                        self.get_long_display_name())

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.specialize_java_doc_function_links(common.select_lang(self.get_doc())),
                                              api_str)

    def get_java_doc(self):
        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += self.get_java_examples()
        doc += self.get_java_api()

        return doc

class JavaDocPacket(java_common.JavaPacket):
    def get_java_formatted_doc(self, shift_right):
        text = common.select_lang(self.get_doc_text())
        text = self.get_device().specialize_java_doc_function_links(text)

        text = text.replace('Callback ', 'Listener ')
        text = text.replace(' Callback', ' Listener')
        text = text.replace('callback ', 'listener ')
        text = text.replace(' callback', ' listener')

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = self.get_device().get_java_class_name() + '.'

        def format_element_name(element, index):
            if index == None:
                return element.get_name().headless

            return '{0}[{1}]'.format(element.get_name().headless, index)

        text += common.format_constants(prefix, self, format_element_name)
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, shift_right)

class JavaDocGenerator(java_common.JavaGeneratorTrait, common.DocGenerator):
    def get_doc_rst_filename_part(self):
        return 'Java'

    def get_doc_example_regex(self):
        return r'^Example.*\.java$'

    def get_device_class(self):
        return JavaDocDevice

    def get_packet_class(self):
        return JavaDocPacket

    def get_element_class(self):
        return java_common.JavaElement

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_java_doc())

    def is_matlab(self):
        return False

    def is_octave(self):
        return False

def generate(root_dir, language, internal):
    common.generate(root_dir, language, internal, JavaDocGenerator)

if __name__ == '__main__':
    args = common.dockerize('java', __file__, add_internal_argument=True)

    for language in ['en', 'de']:
        generate(os.getcwd(), language, args.internal)
