#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C# Documentation Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_csharp_doc.py: Generator for C# documentation

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
import csharp_common

sys.path.append(os.path.split(os.getcwd())[0])
import common

device = None

def fix_links(text):
    parameter = {
    'en': 'parameter',
    'de': 'Parameter'
    }
    parameters = {
    'en': 'parameters',
    'de': 'Parameter'
    }
    link = ':csharp:func:`{2}() <{0}{1}::{2}>`' 

    cls = device.get_camel_case_name()
    for packet in device.get_packets():
        name_false = ':func:`{0}`'.format(packet.get_camel_case_name())
        name = packet.get_camel_case_name()
        name_right = link.format(device.get_category(), cls, name)

        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", common.select_lang(parameter))
    text = text.replace(":word:`parameters`", common.select_lang(parameters))

    return text

def make_examples():
    def title_from_file(f):
        f = f.replace('Example', '')
        f = f.replace('.cs', '')
        return common.camel_case_to_space(f)

    return common.make_rst_examples(title_from_file, device, common.path_binding,
                                    'csharp', 'Example', '.cs', 'CSharp')

def make_methods(typ):
    method_version = {
    'en': """
.. csharp:function:: public void {0}::GetVersion(out string name, out byte[] firmwareVersion, out byte[] bindingVersion)

 Returns the name (including the hardware version), the firmware version 
 and the binding version of the device. The firmware and binding versions are
 given in arrays of size 3 with the syntax [major, minor, revision].
""",
    'de': """
.. csharp:function:: public void {0}::GetVersion(out string name, out byte[] firmwareVersion, out byte[] bindingVersion)

 Gibt den Namen (inklusive Hardwareversion), die Firmwareversion 
 und die Bindingsversion des Gerätes zurück. Die Firmware- und Bindingsversionen werden
 als Array der Größe 3 mit der Syntax [Major, Minor, Revision] zurückgegeben.
"""
    }
    version_changed = {
    'en': """
 .. versionchanged:: 1.1.0
    Result is returned. Previously it was passed as ``out`` parameter.
""",
    'de': """
 .. versionchanged:: 1.1.0
    Das Ergebnis wird zurückgegeben. In vorherigen Versionen wurde es als ``out`` Parameter übergeben.
"""
    }

    methods = ''
    func_start = '.. csharp:function:: '
    cls = device.get_category() + device.get_camel_case_name()
    for packet in device.get_packets('function'):
        if packet.get_doc()[0] != typ:
            continue

        signature = csharp_common.make_method_signature(packet, True, device)
        desc = fix_links(common.shift_right(common.select_lang(packet.get_doc()[1]), 1))
        func = '{0}{1}\n{2}'.format(func_start, 
                                    signature, 
                                    desc)
        methods += func + '\n'

        if len(packet.get_elements('out')) == 1:
            methods += common.select_lang(version_changed) + '\n'

    if typ == 'af':
        methods += common.select_lang(method_version).format(cls)

    return methods

def make_callbacks():
    cb = {
    'en': """
.. csharp:function:: public event {0}EventHandler {0}::{1}({2})

{3}
""",
    'de': """
.. csharp:function:: public event {0}EventHandler {0}::{1}({2})

{3}
"""
    }

    cbs = ''
    cls = device.get_camel_case_name()
    for packet in device.get_packets('callback'):
        desc = fix_links(common.shift_right(common.select_lang(packet.get_doc()[1]), 2))
        params = csharp_common.make_parameter_list(packet)

        cbs += common.select_lang(cb).format(device.get_category() + device.get_camel_case_name(),
                                             packet.get_camel_case_name(),
                                             params,
                                             desc)

    return cbs

def make_api():
    create_str = {
    'en': """
.. csharp:function:: class {3}{1}(String uid)

 Creates an object with the unique device ID *uid*:

 .. code-block:: csharp

  {3}{1} {0} = new {3}{1}("YOUR_DEVICE_UID");

 This object can then be added to the IP connection (see examples 
 :ref:`above <{4}_{2}_csharp_examples>`).
""",
    'de': """
.. csharp:function:: class {3}{1}(String uid)

 Erzeugt ein Objekt mit der eindeutigen Geräte ID *uid*:

 .. code-block:: csharp

  {3}{1} {0} = new {3}{1}("YOUR_DEVICE_UID");

 Dieses Objekt kann danach der IP Connection hinzugefügt werden (siehe Beispiele
 :ref:`oben <{4}_{2}_csharp_examples>`).
"""
    }

    register_str = {
    'en': """
.. csharp:function:: public void {3}{1}::RegisterCallback(Delegate d)

 Registers a callback function. The available callbacks are listed 
 :ref:`below <{0}_{2}_csharp_callbacks>`.
""",
    'de': """
.. csharp:function:: public void {3}{1}::RegisterCallback(Delegate d)

 Registriert einen Callback. Die verfügbaren Callbacks sind 
 :ref:`unten <{0}_{2}_csharp_callbacks>` aufgelistet.
"""
    }

    c_str = {
    'en': """
.. _{1}_{2}_csharp_callbacks:

Callbacks
^^^^^^^^^

*Callbacks* can be registered to receive
time critical or recurring data from the device. The registration is done
by appending your Callback-Handler to the corresponding event:

.. code-block:: csharp
    
    void Callback(int value)
    {{
        System.Console.WriteLine("Value: " + value);
    }}

    device.Event += Callback;

The available events are described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{0}
""",
    'de': """
.. _{1}_{2}_csharp_callbacks:

Callbacks
^^^^^^^^^

*Callbacks* können registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit der Methode :csharp:func:`RegisterCallback <{3}{4}::RegisterCallback>` des Geräteobjekts
durchgeführt werden.

Der Parameter ist ein Delegate Objekt der zugehörigen Methode, z.B.:

.. code-block:: csharp
    
    void Callback(int value)
    {{
        System.Console.WriteLine("Value: " + value);
    }}

    device.RegisterCallback(new BrickDevice.Property(Callback));

Die verfügbaren Delegates werden weiter unten beschrieben.

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

Generally, every method of the C# bindings that returns a value can
throw a ``Tinkerforge.TimeoutException``. This exception gets thrown if the
device did not respond. If a cable based connection is used, it is
unlikely that this exception gets thrown (Assuming nobody plugs the 
device out). However, if a wireless connection is used, timeouts will occur
if the distance to the device gets too big.

Since C# does not support multiple return values directly, we use the out
keyword to return multiple values from a method.

The namespace for all Brick/Bricklet bindings and the IPConnection is
``Tinkerforge.*``

All methods listed below are thread-safe.

{1}

{2}
""",
    'de': """
{0}
API
---

Prinzipiell kann jede Funktion der C# Bindings, welche einen Wert zurück gibt
eine ``Tinkerforge.TimeoutException`` werfen. Diese Exception wird
geworfen wenn das Gerät nicht antwortet. Wenn eine Kabelverbindung genutzt
wird, ist es unwahrscheinlich, dass die Exception geworfen wird (unter der
Annahme, dass das Gerät nicht abgesteckt wird). Bei einer drahtlosen Verbindung
können Zeitüberschreitungen auftreten, sobald die Entfernung zum Gerät zu
groß wird.

Da C# nicht mehrere Rückgabewerte direkt unterstützt, wird das out Keyword genutzt
um mehrere Werte von einer Funktion zurückzugeben.

Der Namensraum für alle Brick/Bricklet Bindings und die IPConnection ist
``Tinkerforge.*``

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
        api_str += common.select_lang(common.ccf_str).format(reg, ccf)
        api_str += common.select_lang(c_str).format(c, device.get_underscore_name(),
                                                    device.get_category().lower(),
                                                    device.get_category(),
                                                    device.get_camel_case_name())

    ref = '.. _{0}_{1}_csharp_api:\n'.format(device.get_underscore_name(),
                                             device.get_category().lower())

    api_desc = ''
    if 'api' in device.com:
        api_desc = common.select_lang(device.com['api'])

    return common.select_lang(api).format(ref, api_desc, api_str)

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)
    file_name = '{0}_{1}_CSharp'.format(device.get_camel_case_name(), device.get_category())
    title = {
    'en': 'C# bindings',
    'de': 'C# Bindings'
    }
    
    directory = os.path.join(directory, 'doc', common.lang)
    if not os.path.exists(directory):
        os.makedirs(directory)

    f = file('{0}/{1}.rst'.format(directory, file_name), "w")
    f.write(common.make_rst_header(device, 'csharp', 'C#'))
    f.write(common.make_rst_summary(device, common.select_lang(title)))
    f.write(make_examples())
    f.write(make_api())

if __name__ == "__main__":
    for lang in ['en', 'de']:
        common.generate(os.getcwd(), lang, make_files)
