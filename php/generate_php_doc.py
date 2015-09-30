#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PHP Documentation Generator
Copyright (C) 2012-2015 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_php_doc.py: Generator for PHP documentation

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

sys.path.append(os.path.split(os.getcwd())[0])
import common
import php_common

class PHPDocDevice(php_common.PHPDevice):
    def replace_php_function_links(self, text):
        cls = self.get_php_class_name()
        for other_packet in self.get_packets():
            name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
            if other_packet.get_type() == 'callback':
                name_upper = other_packet.get_upper_case_name()
                name_right = ':php:member:`CALLBACK_{1} <{0}::CALLBACK_{1}>`'.format(cls, name_upper)
            else:
                name = other_packet.get_headless_camel_case_name()
                name_right = ':php:func:`{1}() <{0}::{1}>`'.format(cls, name)

            text = text.replace(name_false, name_right)

        return text

    def get_php_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('Example', '').replace('.php', '')
            return common.camel_case_to_space(filename)

        return common.make_rst_examples(title_from_filename, self)

    def get_php_methods(self, typ):
        methods = ''
        func_start = '.. php:function:: '
        cls = self.get_php_class_name()
        for packet in self.get_packets('function'):
            if packet.get_doc()[0] != typ:
                continue

            ret_type = packet.get_php_return_type()
            name = packet.get_headless_camel_case_name()
            params = packet.get_php_parameter_list(True)
            desc = packet.get_php_formatted_doc()
            obj_desc = packet.get_php_object_desc()
            func = '{0}{1} {2}::{3}({4})\n{5}{6}'.format(func_start,
                                                         ret_type,
                                                         cls,
                                                         name,
                                                         params,
                                                         desc,
                                                         obj_desc)
            methods += func + '\n'

        return methods

    def get_php_callbacks(self):
        signature_str = {
        'en':  """
 .. code-block:: php

  <?php   void callback({0})   ?>
""",
        'de':  """
 .. code-block:: php

  <?php   void callback({0})   ?>
"""
        }

        cbs = ''
        func_start = '.. php:member:: int '
        cls = self.get_php_class_name()
        for packet in self.get_packets('callback'):
            params = packet.get_php_parameter_list(True)
            if len(params) > 0:
                params += " [, mixed $user_data]"
            else:
                params += "[mixed $user_data]"
            desc = packet.get_php_formatted_doc()
            signature = common.select_lang(signature_str).format(params)
            func = '{0}{1}::CALLBACK_{2}\n{3}{4}'.format(func_start,
                                                         cls,
                                                         packet.get_upper_case_name(),
                                                         signature,
                                                         desc)
            cbs += func + '\n'

        return cbs

    def get_php_api(self):
        create_str = {
        'en': """
.. php:function:: class {1}(string $uid, IPConnection $ipcon)

 Creates an object with the unique device ID ``$uid``:

 .. code-block:: php

    <?php   ${2} = new {1}('YOUR_DEVICE_UID', $ipcon);   ?>

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_php_examples>`).
""",
        'de': """
.. php:function:: class {1}(string $uid, IPConnection $ipcon)

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``$uid``:

 .. code-block:: php

    <?php   ${2} = new {1}('YOUR_DEVICE_UID', $ipcon);   ?>

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_php_examples>`).
"""
        }

        register_str = {
        'en': """
.. php:function:: void {1}::registerCallback(int $id, callable $callback, mixed $user_data = NULL)

 Registers a callback with ID *$id* to the callable *$callback*.
 The *$user_data*  will be given as a parameter of the callback.

 The available  IDs with corresponding function signatures are listed
 :ref:`below <{0}_php_callbacks>`.
""",
        'de': """
.. php:function:: void {1}::registerCallback(int $id, callable $callback, mixed $user_data = NULL)

 Registriert einen Callback mit der ID *$id* zu der Callable *$callback*.
 Der Parameter *$user_data* wird bei jedem Callback wieder mit übergeben.

 Die verfügbaren IDs mit den zugehörigen Funktionssignaturen sind :ref:`unten <{0}_php_callbacks>`
 zu finden.
"""
        }

        c_str = {
        'en': """
.. _{0}_php_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive
time critical or recurring data from the device. The registration is done
with the :php:func:`registerCallback() <{1}::registerCallback>` function of
the device object. The first parameter is the callback ID and the second
parameter the callback function:

.. code-block:: php

    <?php

    function myCallback($param)
    {{
        echo $param . "\\n";
    }}

    ${2}->registerCallback({1}::CALLBACK_EXAMPLE, 'myCallback');

    ?>

The available constants with corresponding function signatures are
described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{3}
""",
        'de': """
.. _{0}_php_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit der Funktion :php:func:`registerCallback() <{1}::registerCallback>` des
Geräte Objektes durchgeführt werden. Der erste Parameter ist der Callback ID
und der zweite die Callback-Funktion:

.. code-block:: php

    <?php

    function myCallback($param)
    {{
        echo $param . "\\n";
    }}

    ${2}->registerCallback({1}::CALLBACK_EXAMPLE, 'myCallback');

    ?>

Die verfügbaren IDs mit den dazugehörigen Funktionssignaturen werden
weiter unten beschrieben.

.. note::
 Callbacks für wiederkehrende Ereignisse zu verwenden ist
 *immer* zu bevorzugen gegenüber der Verwendung von Abfragen.
 Es wird weniger USB-Bandbreite benutzt und die Latenz ist
 erheblich geringer, da es keine Paketumlaufzeit gibt.

{3}
"""
        }

        api = {
        'en': """
.. _{0}_php_api:

API
---

Functions that return multiple values return them in an associative array.

{1}

{2}
""",
        'de': """
.. _{0}_php_api:

API
---

Funktion die mehrere Werte zurückgeben geben diese in einem assoziativen Array
zurück.

{1}

{2}
"""
        }

        const_str = {
        'en': """
.. _{0}_php_constants:

Constants
^^^^^^^^^

.. php:member:: int {1}::DEVICE_IDENTIFIER

 This constant is used to identify a {3}.

 The :php:func:`getIdentity() <{1}::getIdentity>` function and the
 :php:member:`CALLBACK_ENUMERATE <IPConnection::CALLBACK_ENUMERATE>`
 callback of the IP Connection have a ``deviceIdentifier`` parameter to specify
 the Brick's or Bricklet's type.

.. php:member:: string {1}::DEVICE_DISPLAY_NAME

 This constant represents the human readable name of a {3}.
""",
        'de': """
.. _{0}_php_constants:

Konstanten
^^^^^^^^^^

.. php:member:: int {1}::DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {3} zu identifizieren.

 Die :php:func:`getIdentity() <{1}::getIdentity>` Funktion und der
 :php:func:`CALLBACK_ENUMERATE <IPConnection::CALLBACK_ENUMERATE>`
 Callback der IP Connection haben ein ``deviceIdentifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. php:member:: string {1}::DEVICE_DISPLAY_NAME

 Diese Konstante stellt den Anzeigenamen eines {3} dar.
"""
        }

        cre = common.select_lang(create_str).format(self.get_doc_rst_ref_name(),
                                                    self.get_php_class_name(),
                                                    self.get_underscore_name())
        reg = common.select_lang(register_str).format(self.get_doc_rst_ref_name(),
                                                      self.get_php_class_name())

        bf = self.get_php_methods('bf')
        af = self.get_php_methods('af')
        ccf = self.get_php_methods('ccf')
        c = self.get_php_callbacks()
        api_str = ''
        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)
        if af:
            api_str += common.select_lang(common.af_str).format(af)
        if c:
            api_str += common.select_lang(common.ccf_str).format(reg, ccf)
            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_php_class_name(),
                                                        self.get_underscore_name(),
                                                        c)

        article = 'ein'
        if self.get_camel_case_category() == 'Brick':
            article = 'einen'
        api_str += common.select_lang(const_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_php_class_name(),
                                                        article,
                                                        self.get_long_display_name())

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.replace_php_function_links(self.get_api_doc()),
                                              api_str)

    def get_php_doc(self):
        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += self.get_php_examples()
        doc += self.get_php_api()

        return doc

class PHPDocPacket(php_common.PHPPacket):
    def get_php_formatted_doc(self):
        text = common.select_lang(self.get_doc()[1])

        text = self.get_device().replace_php_function_links(text)

        def format_parameter(name):
            return '``${0}``'.format(name)

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = self.get_device().get_php_class_name() + '::'
        if self.get_underscore_name() == 'set_response_expected':
            text += common.format_function_id_constants(prefix, self.get_device())
        else:
            text += common.format_constants(prefix, self)

        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

    def get_php_object_desc(self):
        if len(self.get_elements('out')) < 2:
            return ''

        desc = {
        'en': """
 The returned array has the keys {0}.
""",
        'de': """
 Das zurückgegebene Array enthält die Keys {0}.
"""
        }

        and_ = {
        'en': ' and ',
        'de': ' und '
        }

        var = []
        for element in self.get_elements('out'):
            var.append('``{0}``'.format(element.get_underscore_name()))

        if len(var) == 1:
            return common.select_lang(desc).format(var[0])

        if len(var) == 2:
            return common.select_lang(desc).format(var[0] + common.select_lang(and_) + var[1])

        return common.select_lang(desc).format(', '.join(var[:-1]) + common.select_lang(and_) + var[-1])

class PHPDocGenerator(common.DocGenerator):
    def get_bindings_name(self):
        return 'php'

    def get_bindings_display_name(self):
        return 'PHP'

    def get_doc_rst_filename_part(self):
        return 'PHP'

    def get_doc_example_regex(self):
        return '^Example.*\.php$'

    def get_device_class(self):
        return PHPDocDevice

    def get_packet_class(self):
        return PHPDocPacket

    def get_element_class(self):
        return php_common.PHPElement

    def generate(self, device):
        rst = open(device.get_doc_rst_path(), 'wb')
        rst.write(device.get_php_doc())
        rst.close()

def generate(bindings_root_directory, language):
    common.generate(bindings_root_directory, language, PHPDocGenerator)

if __name__ == "__main__":
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
