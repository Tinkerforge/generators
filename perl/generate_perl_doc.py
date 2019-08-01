#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl Documentation Generator
Copyright (C) 2013-2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2012-2015, 2017-2018 Matthias Bolte <matthias@tinkerforge.com>
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

    def get_perl_methods(self, type_):
        methods = ''
        func_start = '.. perl:function:: '
        cls = self.get_perl_class_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type_:
                continue

            skip = -2 if packet.has_high_level() else 0
            name = packet.get_name(skip=skip).under
            params = packet.get_perl_parameters(high_level=True)
            pd = packet.get_perl_parameter_desc('in', high_level=True)
            r = packet.get_perl_return_desc(high_level=True)
            d = packet.get_perl_formatted_doc()
            obj_desc = packet.get_perl_object_desc(high_level=True)
            desc = '{0}{1}{2}{3}'.format(pd, r, d, obj_desc)
            func = '{0}{1}->{2}({3})\n{4}'.format(func_start,
                                                  cls,
                                                  name,
                                                  params,
                                                  desc)
            methods += func + '\n'

        return methods

    def get_perl_callbacks(self):
        cbs = ''
        func_start = '.. perl:attribute:: '
        cls = self.get_perl_class_name()

        for packet in self.get_packets('callback'):
            skip = -2 if packet.has_high_level() else 0
            param_desc = packet.get_perl_parameter_desc('out', high_level=True)
            desc = packet.get_perl_formatted_doc()

            func = '{0}{1}->CALLBACK_{2}\n{3}\n{4}'.format(func_start,
                                                           cls,
                                                           packet.get_name(skip=skip).upper,
                                                           param_desc,
                                                           desc)
            cbs += func + '\n'

        return cbs

    def get_perl_api(self):
        create_str = {
            'en': """
.. perl:function:: {1}->new($uid, $ipcon)

 :param $uid: string
 :param $ipcon: IPConnection
 :rtype: {1}

 Creates an object with the unique device ID ``$uid``:

 .. code-block:: perl

    ${2} = {1}->new("YOUR_DEVICE_UID", $ipcon);

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_perl_examples>`).
""",
            'de': """
.. perl:function:: {1}->new($uid, $ipcon)

 :param $uid: string
 :param $ipcon: IPConnection
 :rtype: {1}

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``$uid``:

 .. code-block:: perl

    ${2} = {1}->new("YOUR_DEVICE_UID", $ipcon);

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_perl_examples>`).
"""
        }

        register_str = {
            'en': """
.. perl:function:: {1}->register_callback($id, $callback)

 :param $id: int
 :param $callback: string
 :rtype: undef

 Registers the given ``$function`` name with the given ``$callback_id``.

 The available callback IDs with corresponding function signatures are listed
 :ref:`below <{0}_perl_callbacks>`.
""",
            'de': """
.. perl:function:: {1}->register_callback($id, $callback)

 :param $id: int
 :param $callback: string
 :rtype: undef

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

All methods listed below are thread-safe.

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

        cre = common.select_lang(create_str).format(self.get_doc_rst_ref_name(),
                                                    self.get_perl_class_name(),
                                                    self.get_name().under)
        reg = common.select_lang(register_str).format(self.get_doc_rst_ref_name(),
                                                      self.get_perl_class_name())

        bf = self.get_perl_methods('bf')
        af = self.get_perl_methods('af')
        ccf = self.get_perl_methods('ccf')
        c = self.get_perl_callbacks()
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

        if self.get_name().space == 'Set Response Expected':
            text += common.format_function_id_constants(prefix, self.get_device())
        else:
            text += common.format_constants(prefix, self, bool_format_func=lambda value: str(int(value)))

        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

    def get_perl_parameter_desc(self, direction, high_level=False):
        desc = '\n'
        param = ' :param {0}: {1}\n'

        for element in self.get_elements(direction=direction, high_level=high_level):
            t = element.get_perl_type()
            desc += param.format(element.get_perl_doc_name(), t)

        return desc

    def get_perl_return_desc(self, high_level=False):
        ret = ' :rtype: {0}\n'
        ret_list = []

        for element in self.get_elements(direction='out', high_level=high_level):
            ret_list.append(element.get_perl_type())

        if len(ret_list) == 0:
            return ret.format('undef')
        elif len(ret_list) == 1:
            return ret.format(ret_list[0])
        else:
            return ret.format('[' + ', '.join(ret_list) + ']')

    def get_perl_object_desc(self, high_level=False):
        if len(self.get_elements(direction='out', high_level=high_level)) < 2:
            return ''

        desc = {
            'en': """
 The returned array contains the elements {0}.
""",
            'de': """
 Das zurückgegebene Array enthält die Elemente {0}.
"""
        }

        and_ = {
            'en': ' and ',
            'de': ' und '
        }

        var = []

        for element in self.get_elements(direction='out', high_level=high_level):
            var.append('``{0}``'.format(element.get_name().under))

        if len(var) == 1:
            return common.select_lang(desc).format(var[0])

        if len(var) == 2:
            return common.select_lang(desc).format(var[0] + common.select_lang(and_) + var[1])

        return common.select_lang(desc).format(', '.join(var[:-1]) + common.select_lang(and_) + var[-1])

class PerlDocGenerator(common.DocGenerator):
    def get_bindings_name(self):
        return 'perl'

    def get_bindings_display_name(self):
        return 'Perl'

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
