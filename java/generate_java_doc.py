#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java Documentation Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2013 Olaf Lüke <olaf@tinkerforge.com>

generator_java_doc.py: Generator for Java documentation

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

device = None

def format_doc(packet, shift_right):
    text = common.select_lang(packet.get_doc()[1])
    cb_link = ':java:func:`{1}Listener <{0}.{1}Listener>`'
    fu_link = ':java:func:`{1}() <{0}::{1}>`'

    cls = device.get_java_class_name()
    for other_packet in device.get_packets():
        name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
        if other_packet.get_type() == 'callback':
            name = other_packet.get_camel_case_name()
            name_right = cb_link.format(cls, name)
        else:
            name = other_packet.get_headless_camel_case_name()
            name_right = fu_link.format(cls, name)

        text = text.replace(name_false, name_right)

    text = text.replace('Callback ', 'Listener ')
    text = text.replace(' Callback', ' Listener')
    text = text.replace('callback ', 'listener ')
    text = text.replace(' callback', ' listener')

    text = common.handle_rst_word(text)
    text = common.handle_rst_if(text, device)

    prefix = cls + '.'
    if packet.get_underscore_name() == 'set_response_expected':
        text += common.format_function_id_constants(prefix, device)
    else:
        text += common.format_constants(prefix, packet)

    text += common.format_since_firmware(device, packet)

    return common.shift_right(text, shift_right)

def make_examples():
    def title_from_file(f):
        f = f.replace('Example', '')
        f = f.replace('.java', '')
        return common.camel_case_to_space(f)

    return common.make_rst_examples(title_from_file, device, common.path_binding,
                                    'java', 'Example', '.java', 'Java')

def make_object_desc(packet):
    if len(packet.get_elements('out')) < 2:
        return ''

    desc = {
    'en': """
 The returned object has the public member variables {0}.
""",
    'de': """
 Das zurückgegebene Objekt enthält die Public Member Variablen {0}.
"""
    }

    and_ = {
    'en': ' and ',
    'de': ' und '
    }

    var = []
    for element in packet.get_elements('out'):
        var.append('``{0} {1}``'.format(java_common.get_java_type(element.get_type()),
                                        element.get_headless_camel_case_name()))

    if len(var) == 1:
        return common.select_lang(desc).format(var[0])

    if len(var) == 2:
        return common.select_lang(desc).format(var[0] + common.select_lang(and_) + var[1])

    return common.select_lang(desc).format(', '.join(var[:-1]) + common.select_lang(and_) + var[-1])

def make_methods(typ):
    methods = ''
    func_start = '.. java:function:: '
    cls = device.get_java_class_name()
    for packet in device.get_packets('function'):
        if packet.get_doc()[0] != typ:
            continue

        ret_type = java_common.get_return_type(packet, True)
        name = packet.get_headless_camel_case_name()
        params = java_common.make_parameter_list(packet)
        desc = format_doc(packet, 1)
        obj_desc = make_object_desc(packet)
        func = '{0}public {1} {2}::{3}({4})\n{5}{6}'.format(func_start, 
                                                            ret_type,
                                                            cls, 
                                                            name, 
                                                            params, 
                                                            desc,
                                                            obj_desc)
        methods += func + '\n'

    return methods

def make_callbacks():
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
    cls = device.get_java_class_name()
    for packet in device.get_packets('callback'):
        desc = format_doc(packet, 2)
        params = java_common.make_parameter_list(packet)

        cbs += common.select_lang(cb).format(cls,
                                             packet.get_camel_case_name(),
                                             packet.get_headless_camel_case_name(),
                                             params,
                                             desc)

    return cbs

def make_api():
    create_str = {
    'en': """
.. java:function:: class {3}{1}(String uid, IPConnection ipcon)

 Creates an object with the unique device ID ``uid``:

 .. code-block:: java

  {3}{1} {0} = new {3}{1}("YOUR_DEVICE_UID", ipcon);

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{4}_{2}_java_examples>`).
""",
    'de': """
.. java:function:: class {3}{1}(String uid, IPConnection ipcon)

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``uid``:

 .. code-block:: java

  {3}{1} {0} = new {3}{1}("YOUR_DEVICE_UID", ipcon);

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{4}_{2}_java_examples>`).
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
.. _{1}_{2}_java_callbacks:

Listeners
^^^^^^^^^

Listeners can be registered to receive
time critical or recurring data from the device. The registration is done
with "addListener" functions of the device object.

The parameter is a listener class object, for example:

.. code-block:: java

    device.addExampleListener(new {3}{4}.ExampleListener() {{
        public void property(int value) {{
            System.out.println("Value: " + value);
        }}
    }});

The available listener classes with inherent methods to be overwritten
are described below. It is possible to add several listeners and
to remove them with the corresponding "removeListener" function.

.. note::
 Using listeners for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.


{0}
""",
    'de': """
.. _{1}_{2}_java_callbacks:

Listener
^^^^^^^^

Listener können registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit "addListener" Funktionen eines Geräteobjekts durchgeführt werden.

Der Parameter ist ein Listener Klassen Objekt, z.B.:

.. code-block:: java

    device.addExampleListener(new {3}{4}.ExampleListener() {{
        public void property(int value) {{
            System.out.println("Value: " + value);
        }}
    }});

Die verfügbaren Listener Klassen mit den Methoden welche überschrieben
werden können werden unterhalb beschrieben. Es ist möglich mehrere
Listener hinzuzufügen und auch mit einem korrespondierenden
"removeListener" wieder zu entfernen.

.. note::
 Listener für wiederkehrende Ereignisse zu verwenden ist 
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

Generally, every method of the Java bindings that returns a value can
throw a ``TimeoutException``. This exception gets thrown if the
device did not respond. If a cable based connection is used, it is
unlikely that this exception gets thrown (Assuming nobody plugs the 
device out). However, if a wireless connection is used, timeouts will occur
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
{0}
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
nur aus Member Variablen bestehen. Die Member Variablen des zurückgegebenen
Objektes werden in der jeweiligen Methodenbeschreibung erläutert.

Das Package für alle Brick/Bricklet Bindings und die IP Connection ist
``com.tinkerforge.*``

Alle folgend aufgelisteten Methoden sind Thread-sicher.

{1}

{2}
"""
    }

    const_str = {
    'en' : """
Constants
^^^^^^^^^

.. java:member:: public static final int {1}{0}.DEVICE_IDENTIFIER

 This constant is used to identify a {3} {4}.

 The :java:func:`getIdentity() <{4}{3}::getIdentity>` function and the
 :java:func:`EnumerateListener <IPConnection.EnumerateListener>`
 listener of the IP Connection have a ``deviceIdentifier`` parameter to specify
 the Brick's or Bricklet's type.
""",
    'de' : """
Konstanten
^^^^^^^^^^

.. java:member:: public static final int {1}{0}.DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {3} {4} zu identifizieren.

 Die :java:func:`getIdentity() <{4}{3}::getIdentity>` Funktion und der
 :java:func:`EnumerateListener <IPConnection.EnumerateListener>`
 Listener der IP Connection haben ein ``deviceIdentifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.
"""
    }

    cre = common.select_lang(create_str).format(device.get_headless_camel_case_name(),
                                                device.get_camel_case_name(),
                                                device.get_category().lower(),
                                                device.get_category(),
                                                device.get_underscore_name())

    bf = make_methods('bf')
    af = make_methods('af')
    ccf = make_methods('ccf')
    c = make_callbacks()
    api_str = ''
    if bf:
        api_str += common.select_lang(common.bf_str).format(cre, bf)
    if af:
        api_str += common.select_lang(common.af_str).format(af)
    if c:
        api_str += common.select_lang(ccf_str).format(ccf)
        api_str += common.select_lang(c_str).format(c, device.get_underscore_name(),
                                                    device.get_category().lower(),
                                                    device.get_category(),
                                                    device.get_camel_case_name())

    article = 'ein'
    if device.get_category() == 'Brick':
        article = 'einen'
    api_str += common.select_lang(const_str).format(device.get_camel_case_name(),
                                                    device.get_category(),
                                                    article,
                                                    device.get_camel_case_name(),
                                                    device.get_category())

    ref = '.. _{0}_{1}_java_api:\n'.format(device.get_underscore_name(),
                                           device.get_category().lower())

    api_desc = ''
    if 'api' in device.raw_data:
        api_desc = common.select_lang(device.raw_data['api'])

    return common.select_lang(api).format(ref, api_desc, api_str)

class JavaDocGenerator(common.DocGenerator):
    def get_device_class(self):
        return java_common.JavaDevice

    def generate(self, device_):
        global device
        device = device_

        title = { 'en': 'Java bindings', 'de': 'Java Bindings' }
        file_name = '{0}_{1}_Java.rst'.format(device.get_camel_case_name(), device.get_category())

        rst = open(os.path.join(self.get_bindings_root_directory(), 'doc', common.lang, file_name), 'wb')
        rst.write(common.make_rst_header(device, 'java', 'Java'))
        rst.write(common.make_rst_summary(device, common.select_lang(title), 'java'))
        rst.write(make_examples())
        rst.write(make_api())
        rst.close()

def generate(path, lang):
    common.generate(path, lang, JavaDocGenerator, True)

if __name__ == "__main__":
    for lang in ['en', 'de']:
        print("=== Generating %s ===" % lang)
        generate(os.getcwd(), lang)
