#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Documentation Generator
Copyright (C) 2012-2015, 2017-2019 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_c_doc.py: Generator for C/C++ documentation

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

sys.path.append(os.path.split(os.getcwd())[0])
import common
import c_common

class CDocDevice(common.Device):
    def specialize_c_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':c:data:`{0}_CALLBACK_{1}`'.format(packet.get_device().get_name().upper,
                                                           packet.get_name(skip=-2 if high_level else 0).upper)
            else:
                return ':c:func:`{0}_{1}`'.format(packet.get_device().get_name().under,
                                                  packet.get_name(skip=-2 if high_level else 0).under)

        return self.specialize_doc_rst_links(text, specializer, prefix='c')

    def get_c_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('example_', '').replace('.c', '')
            return common.under_to_space(filename).replace('Pwm ', 'PWM ')

        return common.make_rst_examples(title_from_filename, self)

    def get_c_methods(self, type_):
        methods = ''

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type_:
                continue

            skip = -2 if packet.has_high_level() else 0
            name = '{0}_{1}'.format(self.get_name().under, packet.get_name(skip=skip).under)
            plist = common.wrap_non_empty(', ', packet.get_c_parameters(high_level=True), '')
            params = '{0} *{1}{2}'.format(self.get_name().camel, self.get_name().under, plist)

            meta = packet.get_formatted_element_meta(lambda element: element.get_c_type('meta'),
                                                     lambda element: element.get_c_name(),
                                                     output_parameter='always',
                                                     prefix_elements=[(self.get_name().under, self.get_name().camel + ' *', 1, 'in')],
                                                     suffix_elements=[('error_code', 'int', 1, 'return')],
                                                     stream_length_suffix='_length',
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_c_formatted_doc()
            func = '.. c:function:: int {0}({1})\n\n{2}{3}'.format(name, params, meta_table, desc)
            methods += func + '\n'

        return methods

    def get_c_callbacks(self):
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

        for packet in self.get_packets('callback'):
            plist = packet.get_c_parameters(high_level=True)

            if len(plist) == 0:
                plist = 'void *user_data'
            else:
                plist += ', void *user_data'

            params = common.select_lang(param_format).format(plist)
            meta = packet.get_formatted_element_meta(lambda element: element.get_c_type('meta'),
                                                     lambda element: element.get_c_name(),
                                                     suffix_elements=[('user_data', 'void *', 1, 'out')],
                                                     stream_length_suffix='_length',
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_c_formatted_doc()
            skip = -2 if packet.has_high_level() else 0
            func = '.. c:var:: {0}_CALLBACK_{1}\n{2}\n{3}\n{4}'.format(self.get_name().upper,
                                                                       packet.get_name(skip=skip).upper,
                                                                       params,
                                                                       meta_table,
                                                                       desc)
            cbs += func + '\n'

        return cbs

    def get_c_api(self):
        create_str = {
            'en': """
.. c:function:: void {1}_create({2} *{1}, const char *uid, IPConnection *ipcon)

{3}

 Creates the device object ``{1}`` with the unique device ID ``uid`` and adds
 it to the IPConnection ``ipcon``:

 .. code-block:: c

    {2} {1};
    {1}_create(&{1}, "YOUR_DEVICE_UID", &ipcon);

 This device object can be used after the IP connection has been connected
 (see examples :ref:`above <{0}_c_examples>`).
""",
            'de': """
.. c:function:: void {1}_create({2} *{1}, const char *uid, IPConnection *ipcon)

{3}

 Erzeugt ein Geräteobjekt ``{1}`` mit der eindeutigen Geräte ID ``uid`` und
 fügt es der IP Connection ``ipcon`` hinzu:

 .. code-block:: c

    {2} {1};
    {1}_create(&{1}, "YOUR_DEVICE_UID", &ipcon);

 Dieses Geräteobjekt kann benutzt werden, nachdem die IP Connection verbunden
 wurde (siehe Beispiele :ref:`oben <{0}_c_examples>`).
"""
        }

        destroy_str = {
            'en': """
.. c:function:: void {0}_destroy({1} *{0})

{2}

 Removes the device object ``{0}`` from its IPConnection and destroys it.
 The device object cannot be used anymore afterwards.
""",
            'de': """
.. c:function:: void {0}_destroy({1} *{0})

{2}

 Entfernt das Geräteobjekt ``{0}`` von dessen IP Connection und zerstört es.
 Das Geräteobjekt kann hiernach nicht mehr verwendet werden.
"""
        }

        register_str = {
            'en': """
.. c:function:: void {1}_register_callback({2} *{1}, int16_t callback_id, void (*function)(void), void *user_data)

{3}

 Registers the given ``function`` with the given ``callback_id``. The
 ``user_data`` will be passed as the last parameter to the ``function``.

 The available callback IDs with corresponding function signatures are
 listed :ref:`below <{0}_c_callbacks>`.
""",
            'de': """
.. c:function:: void {1}_register_callback({2} *{1}, int16_t callback_id, void (*function)(void), void *user_data)

{3}

 Registriert die ``function`` für die gegebene ``callback_id``. Die ``user_data``
 werden der Funktion als letztes Parameter mit übergeben.

 Die verfügbaren Callback IDs mit den zugehörigen Funktionssignaturen
 sind :ref:`unten <{0}_c_callbacks>` zu finden.
"""
        }

        c_str = {
            'en': """
.. _{0}_c_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive time critical or recurring data from the
device. The registration is done with the :c:func:`{1}_register_callback` function:

 .. code-block:: c

    void my_callback(int p, void *user_data) {{
        printf("parameter: %d\\n", p);
    }}

    {1}_register_callback(&{1}, {2}_CALLBACK_EXAMPLE, (void (*)(void))my_callback, NULL);

The available constants with corresponding function signatures are described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{3}
""",
            'de': """
.. _{0}_c_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische oder wiederkehrende Daten
vom Gerät zu erhalten. Die Registrierung kann mit der :c:func:`{1}_register_callback`
Funktion durchgeführt werden:

 .. code-block:: c

    void my_callback(int p, void *user_data) {{
        printf("parameter: %d\\n", p);
    }}

    {1}_register_callback(&{1}, {2}_CALLBACK_EXAMPLE, (void (*)(void))my_callback, NULL);

Die verfügbaren Konstanten mit den zugehörigen Funktionssignaturen werden weiter
unten beschrieben.

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
.. _{0}_c_api:

API
---

Every function of the C/C++ bindings returns an integer which describes an
error code. Data returned from the device, when a getter is called,
is handled via output parameters. These parameters are labeled with the
``ret_`` prefix.

Possible error codes are:

* **E**\\ _OK = 0
* **E**\\ _TIMEOUT = -1
* **E**\\ _NO_STREAM_SOCKET = -2
* **E**\\ _HOSTNAME_INVALID = -3
* **E**\\ _NO_CONNECT = -4
* **E**\\ _NO_THREAD = -5
* **E**\\ _NOT_ADDED = -6 (unused since C/C++ bindings version 2.0.0)
* **E**\\ _ALREADY_CONNECTED = -7
* **E**\\ _NOT_CONNECTED = -8
* **E**\\ _INVALID_PARAMETER = -9
* **E**\\ _NOT_SUPPORTED = -10
* **E**\\ _UNKNOWN_ERROR_CODE = -11
* **E**\\ _STREAM_OUT_OF_SYNC = -12
* **E**\\ _INVALID_UID = -13
* **E**\\ _NON_ASCII_CHAR_IN_SECRET = -14

as defined in :file:`ip_connection.h`.

All functions listed below are thread-safe.

{1}

{2}
""",
            'de': """
.. _{0}_c_api:

API
---

Jede Funktion der C/C++ Bindings gibt einen Integer zurück, welcher einen
Fehlercode beschreibt. Vom Gerät zurückgegebene Daten werden, wenn eine
Abfrage aufgerufen wurde, über Ausgabeparameter gehandhabt. Diese Parameter
sind mit dem ``ret_`` Präfix gekennzeichnet.

Mögliche Fehlercodes sind:

* **E**\\ _OK = 0
* **E**\\ _TIMEOUT = -1
* **E**\\ _NO_STREAM_SOCKET = -2
* **E**\\ _HOSTNAME_INVALID = -3
* **E**\\ _NO_CONNECT = -4
* **E**\\ _NO_THREAD = -5
* **E**\\ _NOT_ADDED = -6 (wird seit C/C++ Bindings Version 2.0.0 nicht mehr verwendet)
* **E**\\ _ALREADY_CONNECTED = -7
* **E**\\ _NOT_CONNECTED = -8
* **E**\\ _INVALID_PARAMETER = -9
* **E**\\ _NOT_SUPPORTED = -10
* **E**\\ _UNKNOWN_ERROR_CODE = -11
* **E**\\ _STREAM_OUT_OF_SYNC = -12
* **E**\\ _INVALID_UID = -13
* **E**\\ _NON_ASCII_CHAR_IN_SECRET = -14

wie in :file:`ip_connection.h` definiert.

Alle folgend aufgelisteten Funktionen sind Thread-sicher.

{1}

{2}
"""
        }

        const_str = {
            'en': """
.. _{0}_c_constants:

Constants
^^^^^^^^^

.. c:var:: {1}_DEVICE_IDENTIFIER

 This constant is used to identify a {4}.

 The :c:func:`{2}_get_identity` function and the :c:data:`IPCON_CALLBACK_ENUMERATE`
 callback of the IP Connection have a ``device_identifier`` parameter to specify
 the Brick's or Bricklet's type.

.. c:var:: {1}_DEVICE_DISPLAY_NAME

 This constant represents the human readable name of a {4}.
""",
            'de': """
.. _{0}_c_constants:

Konstanten
^^^^^^^^^^

.. c:var:: {1}_DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {3} {4} zu identifizieren.

 Die :c:func:`{2}_get_identity` Funktion und der :c:data:`IPCON_CALLBACK_ENUMERATE`
 Callback der IP Connection haben ein ``device_identifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. c:var:: {1}_DEVICE_DISPLAY_NAME

 Diese Konstante stellt den Anzeigenamen eines {4} dar.
"""
        }

        create_meta = common.format_simple_element_meta([(self.get_name().under, self.get_name().camel + ' *', 1, 'in'),
                                                         ('uid', 'const char *', 1, 'in'),
                                                         ('ipcon', 'IPConnection *', 1, 'in')])
        create_meta_table = common.make_rst_meta_table(create_meta)

        cre = common.select_lang(create_str).format(self.get_doc_rst_ref_name(),
                                                    self.get_name().under,
                                                    self.get_name().camel,
                                                    create_meta_table)

        destroy_meta = common.format_simple_element_meta([(self.get_name().under, self.get_name().camel + ' *', 1, 'in')])
        destroy_meta_table = common.make_rst_meta_table(destroy_meta)

        des = common.select_lang(destroy_str).format(self.get_name().under,
                                                     self.get_name().camel,
                                                     destroy_meta_table)

        reg_meta = common.format_simple_element_meta([(self.get_name().under, self.get_name().camel + ' *', 1, 'in'),
                                                      ('callback_id', 'int16_t', 1, 'in'),
                                                      ('function', 'void (*)(void)', 1, 'in'),
                                                      ('user_data', 'void *', 1, 'in')])
        red_meta_table = common.make_rst_meta_table(reg_meta)

        reg = common.select_lang(register_str).format(self.get_doc_rst_ref_name(),
                                                      self.get_name().under,
                                                      self.get_name().camel,
                                                      red_meta_table)
        bf = self.get_c_methods('bf')
        af = self.get_c_methods('af')
        ccf = self.get_c_methods('ccf')
        c = self.get_c_callbacks()
        api_str = ''

        if bf:
            api_str += common.select_lang(common.bf_str).format(cre + des, bf)

        if af:
            api_str += common.select_lang(common.af_str).format(af)

        if c:
            api_str += common.select_lang(common.ccf_str).format(reg, ccf)
            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_name().under,
                                                        self.get_name().upper,
                                                        c)

        article = 'ein'

        if self.is_brick():
            article = 'einen'

        api_str += common.select_lang(const_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_name().upper,
                                                        self.get_name().under,
                                                        article,
                                                        self.get_long_display_name())

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.specialize_c_doc_function_links(common.select_lang(self.get_doc())),
                                              api_str)

    def get_c_doc(self):
        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += self.get_c_examples()
        doc += self.get_c_api()

        return doc

class CDocPacket(c_common.CPacket):
    def get_c_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())
        text = self.get_device().specialize_c_doc_function_links(text)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = self.get_device().get_name().upper + '_'

        text += common.format_constants(prefix, self, lambda element: element.get_c_name())
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

class CDocGenerator(c_common.CGeneratorTrait, common.DocGenerator):
    def get_bindings_name(self):
        return 'c'

    def get_bindings_display_name(self):
        return 'C/C++'

    def get_doc_rst_filename_part(self):
        return 'C'

    def get_doc_example_regex(self):
        return r'^example_.*\.c$'

    def get_device_class(self):
        return CDocDevice

    def get_packet_class(self):
        return CDocPacket

    def get_element_class(self):
        return c_common.CElement

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_c_doc())

def generate(root_dir, language):
    common.generate(root_dir, language, CDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print('=== Generating %s ===' % language)
        generate(os.getcwd(), language)
