#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java Documentation Generator
Copyright (C) 2012-2015 Matthias Bolte <matthias@tinkerforge.com>
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
import os
import shutil
import subprocess
import glob
import re

sys.path.append(os.path.split(os.getcwd())[0])
import common
import java_common

class JavaDocDevice(java_common.JavaDevice):
    def replace_java_function_links(self, text):
        cb_link = ':java:func:`{1}Listener <{0}.{1}Listener>`'
        fu_link = ':java:func:`{1}() <{0}::{1}>`'

        cls = self.get_java_class_name()
        for other_packet in self.get_packets():
            name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
            if other_packet.get_type() == 'callback':
                name = other_packet.get_camel_case_name()
                name_right = cb_link.format(cls, name)
            else:
                name = other_packet.get_headless_camel_case_name()
                name_right = fu_link.format(cls, name)

            text = text.replace(name_false, name_right)

        return text

    def get_java_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('Example', '').replace('.java', '')
            return common.camel_case_to_space(filename)

        return common.make_rst_examples(title_from_filename, self)

    def get_java_methods(self, typ):
        methods = ''
        func_start = '.. java:function:: '
        cls = self.get_java_class_name()
        for packet in self.get_packets('function'):
            if packet.get_doc()[0] != typ:
                continue

            ret_type = packet.get_java_return_type(True)
            name = packet.get_headless_camel_case_name()
            params = packet.get_java_parameter_list()
            desc = packet.get_java_formatted_doc(1)
            obj_desc = packet.get_java_object_desc()
            func = '{0}public {1} {2}::{3}({4})\n{5}{6}'.format(func_start,
                                                                ret_type,
                                                                cls,
                                                                name,
                                                                params,
                                                                desc,
                                                                obj_desc)
            methods += func + '\n'

        return methods

    def get_java_callbacks(self):
        cb = {
        'en': """
.. java:function:: public class {0}.{1}Listener()

 This listener can be added with the ``add{1}Listener()`` function.
 An added listener can be removed with the ``remove{1}Listener()`` function.

 .. java:function:: public void {2}({3})
  :noindex:

{4}
""",
        'de': """
.. java:function:: public class {0}.{1}Listener()

 Dieser Listener kann mit der Funktion ``add{1}Listener()`` hinzugefügt werde.
 Ein hinzugefügter Listener kann mit der Funktion ``remove{1}Listener()`` wieder
 entfernt werden.

 .. java:function:: public void {2}({3})
  :noindex:

{4}
"""
        }

        cbs = ''
        cls = self.get_java_class_name()
        for packet in self.get_packets('callback'):
            desc = packet.get_java_formatted_doc(2)
            params = packet.get_java_parameter_list()

            cbs += common.select_lang(cb).format(cls,
                                                 packet.get_camel_case_name(),
                                                 packet.get_headless_camel_case_name(),
                                                 params,
                                                 desc)

        return cbs

    def get_java_api(self):
        create_str = {
        'en': """
.. java:function:: class {1}(String uid, IPConnection ipcon)

 Creates an object with the unique device ID ``uid``:

 .. code-block:: java

  {1} {2} = new {1}("YOUR_DEVICE_UID", ipcon);

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_java_examples>`).
""",
        'de': """
.. java:function:: class {1}(String uid, IPConnection ipcon)

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: java

  {1} {2} = new {1}("YOUR_DEVICE_UID", ipcon);

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_java_examples>`).
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
with "add*Listener" functions of the device object.

The parameter is a listener class object, for example:

.. code-block:: java

    device.addExampleListener(new {1}.ExampleListener() {{
        public void property(int value) {{
            System.out.println("Value: " + value);
        }}
    }});

The available listener classes with inherent methods to be overwritten
are described below. It is possible to add several listeners and
to remove them with the corresponding "remove*Listener" function.

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
mit "add*Listener" Funktionen eines Geräteobjekts durchgeführt werden.

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
"remove*Listener" wieder zu entfernen.

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

.. java:member:: public static final int {1}.DEVICE_IDENTIFIER

 This constant is used to identify a {3}.

 The :java:func:`getIdentity() <{1}::getIdentity>` function and the
 :java:func:`EnumerateListener <IPConnection.EnumerateListener>`
 listener of the IP Connection have a ``deviceIdentifier`` parameter to specify
 the Brick's or Bricklet's type.
""",
        'de': """
.. _{0}_java_constants:

Konstanten
^^^^^^^^^^

.. java:member:: public static final int {1}.DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {3} zu identifizieren.

 Die :java:func:`getIdentity() <{1}::getIdentity>` Funktion und der
 :java:func:`EnumerateListener <IPConnection.EnumerateListener>`
 Listener der IP Connection haben ein ``deviceIdentifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.
"""
        }

        cre = common.select_lang(create_str).format(self.get_doc_rst_ref_name(),
                                                    self.get_java_class_name(),
                                                    self.get_headless_camel_case_name())

        bf = self.get_java_methods('bf')
        af = self.get_java_methods('af')
        ccf = self.get_java_methods('ccf')
        c = self.get_java_callbacks()
        api_str = ''
        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)
        if af:
            api_str += common.select_lang(common.af_str).format(af)
        if ccf:
            api_str += common.select_lang(ccf_str).format(ccf)
        if c:
            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_java_class_name(),
                                                        c)

        article = 'ein'
        if self.get_category() == 'Brick':
            article = 'einen'
        api_str += common.select_lang(const_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_java_class_name(),
                                                        article,
                                                        self.get_long_display_name())

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.replace_java_function_links(self.get_api_doc()),
                                              api_str)

    def get_java_doc(self):
        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += self.get_java_examples()
        doc += self.get_java_api()

        return doc

class JavaDocPacket(java_common.JavaPacket):
    def get_java_formatted_doc(self, shift_right):
        text = common.select_lang(self.get_doc()[1])

        text = self.get_device().replace_java_function_links(text)

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
        if self.get_underscore_name() == 'set_response_expected':
            text += common.format_function_id_constants(prefix, self.get_device())
        else:
            text += common.format_constants(prefix, self)

        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, shift_right)

    def get_java_object_desc(self):
        if len(self.get_elements('out')) < 2:
            return ''

        desc = {
        'en': """
 The returned object has the public member variables {0}.
""",
        'de': """
 Das zurückgegebene Objekt enthält die Public-Member-Variablen {0}.
"""
        }

        and_ = {
        'en': ' and ',
        'de': ' und '
        }

        var = []
        for element in self.get_elements('out'):
            typ = element.get_java_type()

            if element.get_cardinality() > 1 and element.get_type() != 'string':
                typ += '[]'

            var.append('``{0} {1}``'.format(typ,
                                            element.get_headless_camel_case_name()))

        if len(var) == 1:
            return common.select_lang(desc).format(var[0])

        if len(var) == 2:
            return common.select_lang(desc).format(var[0] + common.select_lang(and_) + var[1])

        return common.select_lang(desc).format(', '.join(var[:-1]) + common.select_lang(and_) + var[-1])

class JavaDocGenerator(common.DocGenerator):
    def get_bindings_name(self):
        return 'java'

    def get_bindings_display_name(self):
        return 'Java'

    def get_doc_rst_filename_part(self):
        return 'Java'

    def get_doc_example_regex(self):
        return '^Example.*\.java$'

    def get_device_class(self):
        return JavaDocDevice

    def get_packet_class(self):
        return JavaDocPacket

    def get_element_class(self):
        return java_common.JavaElement

    def generate(self, device):
        rst = open(device.get_doc_rst_path(), 'wb')
        rst.write(device.get_java_doc())
        rst.close()

def generate(bindings_root_directory, language):
    common.generate(bindings_root_directory, language, JavaDocGenerator)

if __name__ == "__main__":
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
