#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Documentation Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_c_doc.py: Generator for C/C++ documentation

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

def get_c_type(py_type):
    if py_type == 'string':
        return 'char'
    if py_type in ( 'int8',  'int16',  'int32' , 'int64', \
                   'uint8', 'uint16', 'uint32', 'uint64'):
        return "{0}_t".format(py_type)
    return py_type

def fix_links(text):
    parameter = {
    'en': 'parameter',
    'de': 'Parameter'
    }
    parameters = {
    'en': 'parameters',
    'de': 'Parameter'
    }

    for packet in device.get_packets():
        name_false = ':func:`{0}`'.format(packet.get_camel_case_name())
        if packet.get_type() == 'callback':
            name_upper = packet.get_upper_case_name()
            pre_upper = device.get_upper_case_name()
            name_right = ':c:data:`{0}_CALLBACK_{1}`'.format(pre_upper,
                                                             name_upper)
        else:
            name_right = ':c:func:`{0}_{1}`'.format(device.get_underscore_name(),
                                                    packet.get_underscore_name())
        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", common.select_lang(parameter))
    text = text.replace(":word:`parameters`", common.select_lang(parameters))

    return text

def make_parameter_list(packet):
    param = ''
    for element in packet.get_elements():
        c_type = get_c_type(element[1])
        name = element[0]
        pointer = ''
        arr = ''
        if element[3] == 'out':
            pointer = '*'
            name = "ret_{0}".format(name)
        if element[2] > 1:
            arr = '[{0}]'.format(element[2])
            pointer = ''
       
        param += ', {0} {1}{2}{3}'.format(c_type, pointer, name, arr)
    return param

def make_examples():
    def title_from_file(f):
        f = f.replace('example_', '')
        f = f.replace('.c', '')
        s = ''
        for l in f.split('_'):
            s += l[0].upper() + l[1:] + ' '
        return s[:-1]

    return common.make_rst_examples(title_from_file, device, common.path_binding,
                                    'c', 'example_', '.c', 'C')

def make_methods(typ):
    version_method = {
    'en': """
.. c:function:: int {0}_get_version({1} *{0}, char ret_name[40], uint8_t ret_firmware_version[3], uint8_t ret_binding_version[3])

 Returns the name (including the hardware version), the firmware version 
 and the binding version of the device. The firmware and binding versions are
 given in arrays of size 3 with the syntax [major, minor, revision].
""",
    'de': """
.. c:function:: int {0}_get_version({1} *{0}, char ret_name[40], uint8_t ret_firmware_version[3], uint8_t ret_binding_version[3])

 Gibt den Namen (inklusive Hardwareversion), die Firmwareversion 
 und die Bindingsversion des Gerätes zurück. Die Firmware- und Bindingsversionen werden
 als Array der Größe 3 mit der Syntax [Major, Minor, Revision] zurückgegeben.
"""
    }

    methods = ''
    func_start = '.. c:function:: int '
    for packet in device.get_packets('function'):
        if packet.get_doc()[0] != typ:
            continue
        name = '{0}_{1}'.format(device.get_underscore_name(), packet.get_underscore_name())
        plist = make_parameter_list(packet)
        params = '{0} *{1}{2}'.format(device.get_camel_case_name(), device.get_underscore_name(), plist)
        desc = fix_links(common.shift_right(common.select_lang(packet.get_doc()[1]), 1))
        func = '{0}{1}({2})\n{3}'.format(func_start, name, params, desc)
        methods += func + '\n'

    if typ == 'af':
        methods += common.select_lang(version_method).format(device.get_underscore_name(),
                                                             device.get_camel_case_name())

    return methods

def make_callbacks():
    param_format = {
    'en': """
 .. code-block:: c

  void callback({0})
""",
    'de': """
 .. code-block:: c

  void callback({0})
"""
    }

    cbs = ''
    func_start = '.. c:var:: '
    for packet in device.get_packets('callback'):
        plist = make_parameter_list(packet)[2:].replace('*ret_', '')
        if not plist:
            plist = 'void'
        params = common.select_lang(param_format).format(plist)
        desc = fix_links(common.shift_right(common.select_lang(packet.get_doc()[1]), 1))
        name = '{0}_{1}'.format(device.get_upper_case_name(),
                                packet.get_upper_case_name())

        func = '{0}{1}_CALLBACK_{2}\n{3}\n{4}'.format(func_start,
                                                      device.get_upper_case_name(),
                                                      packet.get_upper_case_name(),
                                                      params,
                                                      desc)
        cbs += func + '\n'

    return cbs

def make_api():
    create_str = {
    'en': """
.. c:function:: void {0}_create({1} *{0}, const char *uid)

 Creates an object with the unique device ID *uid*:

 .. code-block:: c

    {1} {0};
    {0}_create(&{0}, "YOUR_DEVICE_UID");

 This object can then be added to the IP connection (see examples 
 :ref:`above <{0}_{2}_c_examples>`).
""",
    'de': """
.. c:function:: void {0}_create({1} *{0}, const char *uid)

 Erzeugt ein Objekt mit der eindeutigen Geräte ID *uid*:

 .. code-block:: c

    {1} {0};
    {0}_create(&{0}, "YOUR_DEVICE_UID");

 Dieses Objekt kann danach der IP Connection hinzugefügt werden (siehe Beispiele
 :ref:`oben <{0}_{2}_c_examples>`).
"""
    }

    register_str = {
    'en': """
.. c:function:: void {0}_register_callback({1} *{0}, uint8_t id, void *callback)

 Registers a callback with ID *id* to the function *callback*. The available
 IDs with corresponding function signatures are listed 
 :ref:`below <{0}_{2}_c_callbacks>`.
""",
    'de': """
.. c:function:: void {0}_register_callback({1} *{0}, uint8_t id, void *callback)

 Registriert einen Callback mit der ID *id* mit der Funktion *callback*. Die verfügbaren
 IDs mit den zugehörigen Funktionssignaturen sind :ref:`unten <{0}_{2}_c_callbacks>`
 zu finden.
"""
    }

    c_str = {
    'en': """
.. _{0}_{3}_c_callbacks:

Callbacks
^^^^^^^^^

*Callbacks* can be registered with *callback IDs* to receive
time critical or recurring data from the device. The registration is done
with the :c:func:`{0}_register_callback` function. The parameters consist of
the device object, the callback ID and the callback function:

 .. code-block:: c

    void my_callback(int p) {{
        printf("parameter: %d\\n", p);
    }}

    {0}_register_callback(&{0}, {1}_CALLBACK_EXAMPLE, (void*)my_callback);

The available constants with corresponding callback function signatures 
are described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{2}
""",
    'de': """
.. _{0}_{3}_c_callbacks:

Callbacks
^^^^^^^^^

*Callbacks* können mit *callback IDs* registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit der Funktion :c:func:`{0}_register_callback` durchgeführt werden. Die
Parameter bestehen aus dem Geräteobjekt, der Callback ID und der Callbackfunktion:

 .. code-block:: c

    void my_callback(int p) {{
        printf("parameter: %d\\n", p);
    }}

    {0}_register_callback(&{0}, {1}_CALLBACK_EXAMPLE, (void*)my_callback);

Die verfügbaren Konstanten mit den zugehörigen Callback Funktionssignaturen
werden weiter unten beschrieben.

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
{0}
API
---

Every function of the C/C++ bindings returns an integer which describes an
error code. Data returned from the device, when a getter is called,
is handled via call by reference. These parameters are labeled with the
``ret_`` prefix.

Possible error codes are:

* E_OK = 0
* E_TIMEOUT = -1
* E_NO_STREAM_SOCKET = -2
* E_HOSTNAME_INVALID = -3
* E_NO_CONNECT = -4
* E_NO_THREAD = -5
* E_NOT_ADDED = -6

as defined in :file:`ip_connection.h`.

All functions listed below are thread-safe.

{1}

{2}
""",
    'de': """
{0}
API
---

Jede Funktion der C/C++ Bindings gibt einen Integer zurück, welcher einen
Fehlercode beschreibt. Vom Gerät zurückgegebene Daten werden, wenn eine
Abfrage aufgerufen wurde, über Referenzparameter gehandhabt. Diese Parameter
sind mit dem ``ret_`` Präfix gekennzeichnet.

Mögliche Fehlercodes sind:

* E_OK = 0
* E_TIMEOUT = -1
* E_NO_STREAM_SOCKET = -2
* E_HOSTNAME_INVALID = -3
* E_NO_CONNECT = -4
* E_NO_THREAD = -5
* E_NOT_ADDED = -6

wie in :file:`ip_connection.h` definiert.

Alle folgend aufgelisteten Funktionen sind Thread-sicher.

{1}

{2}
"""
    }

    cre = common.select_lang(create_str).format(device.get_underscore_name(),
                                                device.get_camel_case_name(),
                                                device.get_category().lower())
    reg = common.select_lang(register_str).format(device.get_underscore_name(),
                                                  device.get_camel_case_name(),
                                                  device.get_category().lower())
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
        api_str += common.select_lang(c_str).format(device.get_underscore_name(),
                                                    device.get_upper_case_name(),
                                                    c,
                                                    device.get_category().lower())

    ref = '.. _{0}_{1}_c_api:\n'.format(device.get_underscore_name(),
                                        device.get_category().lower())

    api_desc = ''
    if 'api' in device.com:
        api_desc = common.select_lang(device.com['api'])

    return common.select_lang(api).format(ref, api_desc, api_str)

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)
    file_name = '{0}_{1}_C'.format(device.get_camel_case_name(), device.get_category())
    title = {
    'en': 'C/C++ bindings',
    'de': 'C/C++ Bindings'
    }
    directory = os.path.join(directory, 'doc', common.lang)
    f = file('{0}/{1}.rst'.format(directory, file_name), "w")
    f.write(common.make_rst_header(device, 'c', 'C/C++'))
    f.write(common.make_rst_summary(device, common.select_lang(title)))
    f.write(make_examples())
    f.write(make_api())

if __name__ == "__main__":
    for lang in ['en', 'de']:
        common.generate(os.getcwd(), lang, make_files, common.prepare_doc, True)
