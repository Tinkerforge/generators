#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PHP Documentation Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_php_doc.py: Generator for PHP documentation

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

import datetime
import sys
import os
import shutil
import subprocess
import glob
import re
import php_common

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

    cls = device.get_category() + device.get_camel_case_name()
    for packet in device.get_packets():
        name_false = ':func:`{0}`'.format(packet.get_camel_case_name())
        if packet.get_type() == 'callback':
            name_upper = packet.get_upper_case_name()
            name_right = ':php:member:`CALLBACK_{1} <{0}::CALLBACK_{1}>`'.format(cls, name_upper)
        else:
            name = packet.get_headless_camel_case_name()
            name_right = ':php:func:`{1} <{0}::{1}>`'.format(cls, name)
        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", common.select_lang(parameter))
    text = text.replace(":word:`parameters`", common.select_lang(parameters))

    return text

def make_examples():
    def title_from_file(f):
        f = f.replace('Example', '')
        f = f.replace('.php', '')
        return common.camel_case_to_space(f)

    return common.make_rst_examples(title_from_file, device, common.path_binding,
                                    'php', 'Example', '.php', 'PHP')

def make_parameter_list(packet):
    param = []
    for element in packet.get_elements():
        if element[3] == 'out' and packet.get_type() == 'function':
            continue
        php_type = php_common.get_php_type(element[1])
        name = element[0]
        if element[2] > 1 and element[1] != 'string':
            php_type = 'array'
       
        param.append('{0} ${1}'.format(php_type, name))
    return ', '.join(param)

def make_methods(typ):
    version_method = {
    'en': """
.. php:function:: array {0}::getVersion()

 Returns the name (including the hardware version), the firmware version
 and the binding version of the device. The firmware and binding versions
 are given in arrays of size 3 with the syntax (major, minor, revision).

 The returned array contains ``name``, ``firmwareVersion`` and ``bindingVersion``.
""",
    'de': """
.. php:function:: array {0}::getVersion()

 Gibt den Namen (inklusive Hardwareversion), die Firmwareversion 
 und die Bindingsversion des Gerätes zurück. Die Firmware- und Bindingsversionen werden
 als Feld der Größe 3 mit der Syntax [Major, Minor, Revision] zurückgegeben.

 Das zurückgegebene Array enthält ``name``, ``firmwareVersion`` und ``bindingVersion``.
"""
    }

    methods = ''
    func_start = '.. php:function:: '
    cls = device.get_category() + device.get_camel_case_name()
    for packet in device.get_packets('function'):
        if packet.get_doc()[0] != typ:
            continue

        ret_type = php_common.get_return_type(packet)
        name = packet.get_headless_camel_case_name()
        params = make_parameter_list(packet)
        desc = fix_links(common.shift_right(common.select_lang(packet.get_doc()[1]), 1))
        func = '{0}{1} {2}::{3}({4})\n{5}'.format(func_start,
                                                  ret_type,
                                                  cls,
                                                  name,
                                                  params,
                                                  desc)
        methods += func + '\n'

    if typ == 'af':
        methods += common.select_lang(version_method).format(cls)

    return methods

def make_callbacks():
    signature_str = {
    'en':  """
 .. code-block:: php

  void callback({0})
""",
    'de':  """
 .. code-block:: php

  void callback({0})
"""
    }

    cbs = ''
    func_start = '.. php:member:: int '
    cls = device.get_category() + device.get_camel_case_name()
    for packet in device.get_packets('callback'):
        params = make_parameter_list(packet)
        desc = fix_links(common.shift_right(common.select_lang(packet.get_doc()[1]), 1))
        signature = common.select_lang(signature_str).format(params)
        func = '{0}{1}::CALLBACK_{2}\n{3}{4}'.format(func_start,
                                                     cls,
                                                     packet.get_upper_case_name(),
                                                     signature,
                                                     desc)
        cbs += func + '\n'

    return cbs

def make_api():
    create_str = {
    'en': """
.. php:function:: class {3}{1}(string $uid)

 Creates an object with the unique device ID *$uid*:

 .. code-block:: php

    ${0} = new {3}{1}('YOUR_DEVICE_UID');

 This object can then be added to the IP connection (see examples
 :ref:`above <{0}_{2}_php_examples>`).
""",
    'de': """
.. php:function:: class {3}{1}(string $uid)

 Erzeugt ein Objekt mit der eindeutigen Geräte ID *uid*:

 .. code-block:: php

    ${0} = new {3}{1}('YOUR_DEVICE_UID');

 Dieses Objekt kann danach der IP Connection hinzugefügt werden (siehe Beispiele
 :ref:`oben <{0}_{2}_php_examples>`).
"""
    }

    register_str = {
    'en': """
.. php:function:: void {3}{1}::registerCallback(int $id, callable $callback)

 Registers a callback with ID *$id* to the callable *$callback*. The available
 IDs with corresponding function signatures are listed
 :ref:`below <{0}_{2}_php_callbacks>`.
""",
    'de': """
.. php:function:: void {3}{1}::registerCallback(int $id, callable $callback)

 Registriert einen Callback mit der ID *$id* zu der Callable *$callback*. Die verfügbaren
 IDs mit den zugehörigen Funktionssignaturen sind :ref:`unten <{0}_{2}_php_callbacks>`
 zu finden.
"""
    }

    c_str = {
    'en': """
.. _{1}_{2}_php_callbacks:

Callbacks
^^^^^^^^^

*Callbacks* can be registered with *callback IDs* to receive
time critical or recurring data from the device. The registration is done
with the :php:func:`registerCallback <{3}{4}::registerCallback>` function of
the device object. The first parameter is the callback ID and the second
parameter the callback function:

.. code-block:: php

    function my_callback($param)
    {{
        echo $param . "\\n";
    }}

    ${1}->registerCallback({3}{4}::CALLBACK_EXAMPLE, 'my_callback');

The available constants with inherent number and type of parameters are
described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{0}
""",
    'de': """
.. _{1}_{2}_php_callbacks:

Callbacks
^^^^^^^^^

*Callbacks* können mit *callback IDs* registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit der Funktion :php:func:`registerCallback <{3}{4}::registerCallback>` des
Geräte Objektes durchgeführt werden. Der erste Parameter ist der Callback ID
und der zweite die Callbackfunktion:

.. code-block:: php

    function my_callback($param)
    {{
        echo $param . "\\n";
    }}

    ${1}->registerCallback({3}{4}::CALLBACK_EXAMPLE, 'my_callback');

Die verfügbaren Konstanten mit der dazugehörigen Parameteranzahl und -typen werden
weiter unten beschrieben.

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

{1}

{2}
""",
    'de': """
{0}
API
---

{1}

{2}
"""
    }

    cre = common.select_lang(create_str).format(device.get_underscore_name(),
                                                device.get_camel_case_name(),
                                                device.get_category().lower(),
                                                device.get_category())
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

    ref = '.. _{0}_{1}_php_api:\n'.format(device.get_underscore_name(),
                                          device.get_category().lower())

    api_desc = ''
    if 'api' in device.com:
        api_desc = common.select_lang(device.com['api'])

    return common.select_lang(api).format(ref, api_desc, api_str)

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)
    file_name = '{0}_{1}_PHP'.format(device.get_camel_case_name(), device.get_category())
    title = {
    'en': 'PHP bindings',
    'de': 'PHP Bindings'
    }
    directory = os.path.join(directory, 'doc', common.lang)
    f = file('{0}/{1}.rst'.format(directory, file_name), "w")
    f.write(common.make_rst_header(device, 'php', 'PHP'))
    f.write(common.make_rst_summary(device, common.select_lang(title)))
    f.write(make_examples())
    f.write(make_api())

if __name__ == "__main__":
    for lang in ['en', 'de']:
        common.generate(os.getcwd(), lang, make_files, common.prepare_doc)
