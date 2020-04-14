#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl Documentation Generator
Copyright (C) 2013-2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2012-2015, 2017-2020 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2013 Olaf Lüke <olaf@tinkerforge.com>

generate_perl_doc.py: Generator for Perl documentation

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

sys.path.append(os.path.split(os.getcwd())[0])
import common
import perl_common

class PerlDocDevice(perl_common.PerlDevice):
    def specialize_perl_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':perl:attr:`CALLBACK_{1} <{0}->CALLBACK_{1}>`'.format(packet.get_device().get_perl_class_name(),
                                                                              packet.get_name(skip=-2 if high_level else 0).upper)
            else:
                return ':perl:func:`{1}() <{0}->{1}>`'.format(packet.get_device().get_perl_class_name(),
                                                              packet.get_name(skip=-2 if high_level else 0).under)

        return self.specialize_doc_rst_links(text, specializer, prefix='perl')

    def get_perl_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('example_', '').replace('.pl', '')
            return common.under_to_space(filename)

        return common.make_rst_examples(title_from_filename, self)

    def get_perl_functions(self, type_):
        functions = []
        template = '.. perl:function:: {0}->{1}({2})\n\n{3}{4}\n'
        cls = self.get_perl_class_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type_:
                continue

            skip = -2 if packet.has_high_level() else 0
            name = packet.get_name(skip=skip).under
            params = packet.get_perl_parameters(high_level=True)
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_perl_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_perl_doc_name(index=index),
                                                     return_object='conditional',
                                                     return_object_label_override={'en': 'Return Array', 'de': 'Rückgabe-Array'},
                                                     return_object_is_array=True,
                                                     no_out_value={'en': 'undef', 'de': 'undef'},
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_perl_formatted_doc()

            functions.append(template.format(cls, name, params, meta_table, desc))

        return ''.join(functions)

    def get_perl_callbacks(self):
        callbacks = []
        template = '.. perl:attribute:: {0}->CALLBACK_{1}\n\n{2}{3}\n'
        cls = self.get_perl_class_name()

        for packet in self.get_packets('callback'):
            skip = -2 if packet.has_high_level() else 0
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_perl_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_perl_doc_name(index=index),
                                                     no_out_value={'en': 'no parameters', 'de': 'keine Parameter'},
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_perl_formatted_doc()

            callbacks.append(template.format(cls, packet.get_name(skip=skip).upper, meta_table, desc))

        return ''.join(callbacks)

    def get_perl_api(self):
        create_str = {
            'en': """
.. perl:function:: {0}->new($uid, $ipcon)

{2}

 Creates an object with the unique device ID ``$uid``:

 .. code-block:: perl

    ${1} = {0}->new("YOUR_DEVICE_UID", $ipcon);

 This object can then be used after the IP Connection is connected.
""",
            'de': """
.. perl:function:: {0}->new($uid, $ipcon)

{2}

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``$uid``:

 .. code-block:: perl

    ${1} = {0}->new("YOUR_DEVICE_UID", $ipcon);

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist.
"""
        }

        register_str = {
            'en': """
.. perl:function:: {1}->register_callback($callback_id, $function)

{2}

 Registers the given ``$function`` name with the given ``$callback_id``.

 The available callback IDs with corresponding function signatures are listed
 :ref:`below <{0}_perl_callbacks>`.
""",
            'de': """
.. perl:function:: {1}->register_callback($callback_id, $function)

{2}

 Registriert den ``$function`` Namen für die gegebene ``$callback_id``.

 Die verfügbaren Callback IDs mit den zugehörigen Funktionssignaturen
 sind :ref:`unten <{0}_perl_callbacks>` zu finden.
"""
        }

        c_str = {
            'en': """
.. _{0}_perl_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive
time critical or recurring data from the device. The registration is done
with the :perl:func:`register_callback() <{1}->register_callback>` function of
the device object. The first parameter is the callback ID and the second
parameter the callback function name:

.. code-block:: perl

    sub my_callback
    {{
        print "@_[0]";
    }}

    ${2}->register_callback({1}->CALLBACK_EXAMPLE, 'my_callback')

The callback function will be called from an internal thread of the
IP Connection. In contrast to many other programming languages, variables are
not automatically shared between threads in Perl. If you want to share a global
variable between a callback function and the rest for your program it has to be
marked as ``:shared``. See the documentation of the `threads::shared
<https://perldoc.perl.org/threads/shared.html>`__ Perl module for more details.

The available constants with inherent number and type of parameters are
described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{3}
""",
            'de': """
.. _{0}_perl_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit der Funktion :perl:func:`register_callback() <{1}->register_callback>` des
Geräte Objektes durchgeführt werden. Der erste Parameter ist die Callback ID
und der zweite Parameter ist der Name der Callback-Funktion:

.. code-block:: perl

    sub my_callback
    {{
        print "@_[0]";
    }}

    ${2}->register_callback({1}->CALLBACK_EXAMPLE, 'my_callback')

Die Callback Funktion wird dann von einem internen Thread der IP Connection
aufgerufen werden. Im Gegensatz zu vielen anderen Programmiersprachen werden
Variablen nicht automatisch zwischen Threads geteilt. Wenn eine Variable
gleichzeitig in einer Callback Funktion und dem Rest des Programms genutzt
werden soll, dann muss diese als ``:shared`` markiert werden. Siehe dazu auch
die Dokumentation des `threads::shared
<https://perldoc.perl.org/threads/shared.html>`__ Perl Moduls für weitere
Details.

Die verfügbaren IDs mit der dazugehörigen Parameteranzahl und -typen werden
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
.. _{0}_perl_api:

API
---

Generally, every subroutine of the Perl bindings can report an error as
``Tinkerforge::Error`` object via ``croak()``. The object has a
``get_code()`` and a ``get_message()`` subroutine. There are different
error code:

* Error->ALREADY_CONNECTED = 11
* Error->NOT_CONNECTED = 12
* Error->CONNECT_FAILED = 13
* Error->INVALID_FUNCTION_ID = 21
* Error->TIMEOUT = 31
* Error->INVALID_PARAMETER = 41
* Error->FUNCTION_NOT_SUPPORTED = 42
* Error->UNKNOWN_ERROR = 43
* Error->STREAM_OUT_OF_SYNC = 51
* Error->INVALID_UID = 61
* Error->NON_ASCII_CHAR_IN_SECRET = 71
* Error->WRONG_DEVICE_TYPE = 81
* Error->DEVICE_REPLACED = 82

All functions listed below are thread-safe.

{1}

{2}
""",
            'de': """
.. _{0}_perl_api:

API
---

Allgemein kann jede Subroutine der Perl Bindings Fehler als
``Tinkerforge::Error`` Objekt mittels ``croak()`` melden. Das Objekt hat eine
``get_code()`` und eine ``get_message()`` Subroutine. Es sind verschiedene
Fehlercodes definiert:

* Error->ALREADY_CONNECTED = 11
* Error->NOT_CONNECTED = 12
* Error->CONNECT_FAILED = 13
* Error->INVALID_FUNCTION_ID = 21
* Error->TIMEOUT = 31
* Error->INVALID_PARAMETER = 41
* Error->FUNCTION_NOT_SUPPORTED = 42
* Error->UNKNOWN_ERROR = 43
* Error->STREAM_OUT_OF_SYNC = 51
* Error->INVALID_UID = 61
* Error->NON_ASCII_CHAR_IN_SECRET = 71
* Error->WRONG_DEVICE_TYPE = 81
* Error->DEVICE_REPLACED = 82

Alle folgend aufgelisteten Funktionen sind Thread-sicher.

{1}

{2}
"""
        }

        const_str = {
            'en': """
.. _{0}_perl_constants:

Constants
^^^^^^^^^

.. perl:attribute:: {1}->DEVICE_IDENTIFIER

 This constant is used to identify a {3}.

 The :perl:func:`get_identity() <{1}->get_identity>` function and the
 :perl:attr:`IPConnection->CALLBACK_ENUMERATE <IPConnection->CALLBACK_ENUMERATE>`
 callback of the IP Connection have a ``device_identifier`` parameter to specify
 the Brick's or Bricklet's type.

.. perl:attribute:: {1}->DEVICE_DISPLAY_NAME

 This constant represents the human readable name of a {3}.
""",
            'de': """
.. _{0}_perl_constants:

Konstanten
^^^^^^^^^^

.. perl:attribute:: {1}->DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {3} zu identifizieren.

 Die :perl:func:`get_identity() <{1}->get_identity>` Funktion und der
 :perl:attr:`IPConnection->CALLBACK_ENUMERATE <IPConnection->CALLBACK_ENUMERATE>`
 Callback der IP Connection haben ein ``device_identifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. perl:attribute:: {1}->DEVICE_DISPLAY_NAME

 Diese Konstante stellt den Anzeigenamen eines {3} dar.
"""
        }

        create_meta = common.format_simple_element_meta([('$uid', 'string', 1, 'in'),
                                                         ('$ipcon', 'IPConnection', 1, 'in'),
                                                         ('$' + self.get_name().under, self.get_perl_class_name(), 1, 'out')])
        create_meta_table = common.make_rst_meta_table(create_meta)

        cre = common.select_lang(create_str).format(self.get_perl_class_name(),
                                                    self.get_name().under,
                                                    create_meta_table)

        reg_meta = common.format_simple_element_meta([('$callback_id', 'int', 1, 'in'),
                                                      ('$function', 'string', 1, 'in')],
                                                     no_out_value={'en': 'undef', 'de': 'undef'})
        reg_meta_table = common.make_rst_meta_table(reg_meta)

        reg = common.select_lang(register_str).format(self.get_doc_rst_ref_name(),
                                                      self.get_perl_class_name(),
                                                      reg_meta_table)

        bf = self.get_perl_functions('bf')
        af = self.get_perl_functions('af')
        ccf = self.get_perl_functions('ccf')
        c = self.get_perl_callbacks()
        vf = self.get_perl_functions('vf')
        if_ = self.get_perl_functions('if')
        api_str = ''

        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)

        if af:
            api_str += common.select_lang(common.af_str).format(af)

        if c:
            api_str += common.select_lang(common.ccf_str).format(reg, ccf)
            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_perl_class_name(),
                                                        self.get_name().under,
                                                        c)

        if vf:
            api_str += common.select_lang(common.vf_str).format(vf)

        if if_:
            api_str += common.select_lang(common.if_str).format(if_)

        article = 'ein'

        if self.is_brick():
            article = 'einen'

        api_str += common.select_lang(const_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_perl_class_name(),
                                                        article,
                                                        self.get_long_display_name())

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.specialize_perl_doc_function_links(common.select_lang(self.get_doc())),
                                              api_str)

    def get_perl_doc(self):
        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += self.get_perl_examples()
        doc += self.get_perl_api()

        return doc

class PerlDocPacket(common.Packet):
    def get_perl_parameters(self, high_level=False):
        params = []

        for element in self.get_elements(direction='in', high_level=high_level):
            params.append(element.get_perl_doc_name())

        return ', '.join(params)

    def get_perl_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())
        text = self.get_device().specialize_perl_doc_function_links(text)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = self.get_device().get_perl_class_name() + '->'

        def format_element_name(element, index):
            if index == None:
                return element.get_perl_doc_name()

            return '{0}[{1}]'.format(element.get_perl_doc_name(), index)

        text += common.format_constants(prefix, self, format_element_name)
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

class PerlDocGenerator(perl_common.PerlGeneratorTrait, common.DocGenerator):
    def get_doc_rst_filename_part(self):
        return 'Perl'

    def get_doc_example_regex(self):
        return r'^example_.*\.pl$'

    def get_device_class(self):
        return PerlDocDevice

    def get_packet_class(self):
        return PerlDocPacket

    def get_element_class(self):
        return perl_common.PerlElement

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_perl_doc())

def generate(root_dir, language):
    common.generate(root_dir, language, PerlDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
