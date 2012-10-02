#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java Documentation Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

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

device = None

def fix_links(text):
    cb_link = ':java:func:`{2}Listener <{0}{1}.{2}Listener>`'
    fu_link = ':java:func:`{2}() <{0}{1}::{2}>`'
    parameter = {
    'en': 'parameter',
    'de': 'Parameter'
    }
    parameters = {
    'en': 'parameters',
    'de': 'Parameter'
    }

    cls = device.get_camel_case_name()
    for packet in device.get_packets():
        name_false = ':func:`{0}`'.format(packet.get_camel_case_name())
        if packet.get_type() == 'callback':
            name = packet.get_camel_case_name()
            name_right = cb_link.format(device.get_category(), cls, name)
        else:
            name = packet.get_headless_camel_case_name()
            name_right = fu_link.format(device.get_category(), cls, name)

        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", common.select_lang(parameter))
    text = text.replace(":word:`parameters`", common.select_lang(parameters))
    text = text.replace('Callback ', 'Listener ')
    text = text.replace(' Callback', ' Listener')
    text = text.replace('callback ', 'listener ')
    text = text.replace(' callback', ' listener')

    return text

def make_examples():
    def title_from_file(f):
        f = f.replace('Example', '')
        f = f.replace('.java', '')
        return common.camel_case_to_space(f)

    return common.make_rst_examples(title_from_file, device, common.path_binding,
                                    'java', 'Example', '.java', 'Java')

def get_java_type(typ):
    forms = {
        'int8' : 'byte',
        'uint8' : 'short',
        'int16' : 'short',
        'uint16' : 'int',
        'int32' : 'int',
        'uint32' : 'long',
        'int64' : 'long',
        'uint64' : 'long',
        'float' : 'float',
        'bool' : 'boolean',
        'string' : 'String',
        'char' : 'char'
    }

    if typ in forms:
        return forms[typ]

    return ''

def get_object_name(packet):
    name = packet.get_camel_case_name()
    if name.startswith('Get'):
        name = name[3:]

    return name

def get_return_type(packet):
    if len(packet.get_elements('out')) == 0:
        return 'void'
    if len(packet.get_elements('out')) > 1:
        return device.get_category() + device.get_camel_case_name() + '.' + get_object_name(packet)
    
    for element in packet.get_elements('out'):
        return get_java_type(element[1])

def make_parameter_list(packet):
    param = []
    for element in packet.get_elements():
        if element[3] == 'out' and packet.get_type() == 'function':
            continue
        java_type = get_java_type(element[1])
        name = common.underscore_to_headless_camel_case(element[0])
        arr = ''
        if element[2] > 1 and element[1] != 'string':
            arr = '[]'
       
        param.append('{0}{1} {2}'.format(java_type, arr, name))
    return ', '.join(param)

def make_obj_desc(packet):
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

    var = []
    for element in packet.get_elements('out'):
        var.append('``{0} {1}``'.format(get_java_type(element[1]),
                                        common.underscore_to_headless_camel_case(element[0])))

    if len(var) == 1:
        return common.select_lang(desc).format(var[0])

    if len(var) == 2:
        return common.select_lang(desc).format(var[0] + ' and ' + var[1])

    return common.select_lang(desc).format(', '.join(var[:-1]) + ' and ' + var[-1])

def make_methods(typ):
    version_method = {
    'en': """
.. java:function:: public {0}.Version {0}::getVersion()

 Returns the name (including the hardware version), the firmware version 
 and the binding version of the device. The firmware and binding versions are
 given in arrays of size 3 with the syntax [major, minor, revision].

 The returned object has the public member variables ``String name``, 
 ``short[3] firmwareVersion`` and ``short[3] bindingVersion``.
""",
    'de': """
.. java:function:: public {0}.Version {0}::getVersion()

 Gibt den Namen (inklusive Hardwareversion), die Firmwareversion 
 und die Bindingsversion des Gerätes zurück. Die Firmware- und Bindingsversionen werden
 als Array der Größe 3 mit der Syntax [Major, Minor, Revision] zurückgegeben.

 Das zurückgegebene Objekt hat die Public Member Variablen ``String name``, 
 ``short[3] firmwareVersion`` und ``short[3] bindingVersion``.
"""
    }

    methods = ''
    func_start = '.. java:function:: '
    cls = device.get_category() + device.get_camel_case_name()
    for packet in device.get_packets('function'):
        if packet.get_doc()[0] != typ:
            continue

        ret_type = get_return_type(packet)
        name = packet.get_headless_camel_case_name()
        params = make_parameter_list(packet)
        desc = fix_links(common.shift_right(common.select_lang(packet.get_doc()[1]), 1))
        obj_desc = make_obj_desc(packet)
        func = '{0}public {1} {2}::{3}({4})\n{5}{6}'.format(func_start, 
                                                            ret_type,
                                                            cls, 
                                                            name, 
                                                            params, 
                                                            desc,
                                                            obj_desc)
        methods += func + '\n'

    if typ == 'af':
        methods += common.select_lang(version_method).format(cls)

    return methods

def make_callbacks():
    cb = {
    'en': """
.. java:function:: public class {0}{1}.{2}Listener()

 .. java:function:: public void {3}({4})
  :noindex:

{5}
""",
    'de': """
.. java:function:: public class {0}{1}.{2}Listener()

 .. java:function:: public void {3}({4})
  :noindex:

{5}
"""
    }

    cbs = ''
    cls = device.get_camel_case_name()
    for packet in device.get_packets('callback'):
        desc = fix_links(common.shift_right(common.select_lang(packet.get_doc()[1]), 2))
        params = make_parameter_list(packet)

        cbs += common.select_lang(cb).format(device.get_category(),
                                             cls,
                                             packet.get_camel_case_name(),
                                             packet.get_headless_camel_case_name(),
                                             params,
                                             desc)

    return cbs

def make_api():
    create_str = {
    'en': """
.. java:function:: class {3}{1}(String uid)

 Creates an object with the unique device ID *uid*:

 .. code-block:: java

  {3}{1} {0} = new {3}{1}("YOUR_DEVICE_UID");

 This object can then be added to the IP connection (see examples 
 :ref:`above <{4}_{2}_java_examples>`).
""",
    'de': """
.. java:function:: class {3}{1}(String uid)

 Erzeugt ein Objekt mit der eindeutigen Geräte ID *uid*:

 .. code-block:: java

  {3}{1} {0} = new {3}{1}("YOUR_DEVICE_UID");

 Dieses Objekt kann danach der IP Connection hinzugefügt werden (siehe Beispiele
 :ref:`oben <{4}_{2}_java_examples>`).
"""
    }

    register_str = {
    'en': """
.. java:function:: public void {3}{1}::addListener(Object o)

 Registers a listener object. The available listeners are listed 
 :ref:`below <{0}_{2}_java_callbacks>`.
""",
    'de': """
.. java:function:: public void {3}{1}::addListener(Object o)

 Registriert ein Listener Objekt. Die verfügbaren Listener werden
 :ref:`unten <{0}_{2}_java_callbacks>` aufgelistet.
"""
    }

    ccf_str = {
    'en': """
Listener Configuration Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{0}

{1}
""",
    'de': """
Konfigurationsfunktionen für Listener
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{0}

{1}
"""
    }

    c_str = {
    'en': """
.. _{1}_{2}_java_callbacks:

Listeners
^^^^^^^^^

*Listeners* can be registered to receive
time critical or recurring data from the device. The registration is done
with the :java:func:`addListener <{3}{4}::addListener>` function of the device object.

The parameter is a listener class object, for example:

.. code-block:: java

    device.addListener(new BrickDevice.PropertyListener() {{
        public void property(int value) {{
            System.out.println("Value: " + value);
        }}
    }});

The available listener classes with inherent methods to be overwritten
are described below.

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

*Listener* können registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit der Funktion :java:func:`addListener <{3}{4}::addListener>` des Geräte Objekts
durchgeführt werden.

Der Parameter ist ein Listener Klassen Objekt, z.B.:

.. code-block:: java

    device.addListener(new BrickDevice.PropertyListener() {{
        public void property(int value) {{
            System.out.println("Value: " + value);
        }}
    }});

Die verfügbaren Listener Klassen mit den Methoden welche überschrieben
werden können werden unterhalb beschrieben.

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
throw a ``IPConnection.TimeoutException``. This exception gets thrown if the
device did not respond. If a cable based connection is used, it is
unlikely that this exception gets thrown (Assuming nobody plugs the 
device out). However, if a wireless connection is used, timeouts will occur
if the distance to the device gets too big.

Since Java does not support multiple return values and return by reference
is not possible for primitive types, we use small classes that 
only consist of member variables (comparable to structs in C). The member
variables of the returned objects are described in the corresponding method 
descriptions.

The package for all Brick/Bricklet bindings and the IPConnection is
``com.tinkerforge.*``

All methods listed below are thread-safe.

{1}

{2}
""",
    'de': """
{0}
API
---

Prinzipiell kann jede Methode der Java Bindings, welche einen Wert zurückgibt
eine ``IPConnection.TimeoutException`` werfen. Diese Exception wird
geworfen wenn das Gerät nicht antwortet. Wenn eine Kabelverbindung genutzt
wird, ist es unwahrscheinlich, dass die Exception geworfen wird (unter der
Annahme, dass das Gerät nicht abgesteckt wird). Bei einer drahtlosen Verbindung
können Zeitüberschreitungen auftreten, sobald die Entfernung zum Gerät zu
groß wird.

Da Java nicht mehrere Rückgabewerte unterstützt und eine Referenzrückgabe
für elementare Type nicht möglich ist, werden kleine Klassen verwendet, die
nur aus Member Variablen bestehen (Vergleichbar mit Structs in C). Die Member
Variablen des zurückgegebenen Objektes werden in der jeweiligen Methodenbeschreibung
erläutert.

Das Package für alle Brick/Bricklet Bindings und die IPConnection ist
``com.tinkerforge.*``

Alle folgend aufgelisteten Methoden sind Thread-sicher.

{1}

{2}
"""
    }

    cre = common.select_lang(create_str).format(device.get_headless_camel_case_name(),
                                                device.get_camel_case_name(),
                                                device.get_category().lower(),
                                                device.get_category(),
                                                device.get_underscore_name())
    reg = common.select_lang(register_str).format(device.get_underscore_name(),
                                                  device.get_camel_case_name(),
                                                  device.get_category().lower(),
                                                  device.get_category())

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
        api_str += common.select_lang(ccf_str).format(reg, ccf)
        api_str += common.select_lang(c_str).format(c, device.get_underscore_name(),
                                                    device.get_category().lower(),
                                                    device.get_category(),
                                                    device.get_camel_case_name())

    ref = '.. _{0}_{1}_java_api:\n'.format(device.get_underscore_name(),
                                           device.get_category().lower())

    api_desc = ''
    if 'api' in device.com:
        api_desc = common.select_lang(device.com['api'])

    return common.select_lang(api).format(ref, api_desc, api_str)

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)
    file_name = '{0}_{1}_Java'.format(device.get_camel_case_name(), device.get_category())
    title = {
    'en': 'Java bindings',
    'de': 'Java Bindings'
    }
    directory = os.path.join(directory, 'doc', common.lang)
    f = file('{0}/{1}.rst'.format(directory, file_name), "w")
    f.write(common.make_rst_header(device, 'java', 'Java'))
    f.write(common.make_rst_summary(device, common.select_lang(title)))
    f.write(make_examples())
    f.write(make_api())

if __name__ == "__main__":
    for lang in ['en', 'de']:
        common.generate(os.getcwd(), lang, make_files, common.prepare_doc)
