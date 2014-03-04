#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl Documentation Generator
Copyright (C) 2013-2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>
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
import shutil
import subprocess
import glob
import re

sys.path.append(os.path.split(os.getcwd())[0])
import common
import perl_common

class PerlDocDevice(perl_common.PerlDevice):
    def get_perl_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('example_', '').replace('.pl', '')
            return common.underscore_to_space(filename)

        return common.make_rst_examples(title_from_filename, self)

    def get_perl_methods(self, typ):
        methods = ''
        func_start = '.. perl:function:: '
        cls = self.get_perl_class_name()
        for packet in self.get_packets('function'):
            if packet.get_doc()[0] != typ:
                continue
            name = packet.get_underscore_name()
            params = packet.get_perl_parameter_list()
            pd = packet.get_perl_parameter_desc('in')
            r = packet.get_perl_return_desc()
            d = packet.get_perl_formatted_doc()
            obj_desc = packet.get_perl_object_desc()
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
            param_desc = packet.get_perl_parameter_desc('out')
            desc = packet.get_perl_formatted_doc()

            func = '{0}{1}->CALLBACK_{2}\n{3}\n{4}'.format(func_start,
                                                           cls,
                                                           packet.get_upper_case_name(),
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

    ${0} = {1}->new("YOUR_DEVICE_UID", $ipcon);

 This object can then be used after the IP Connection is connected
 (see examples :ref:`above <{0}_{2}_perl_examples>`).
""",
        'de': """
.. perl:function:: {1}->new($uid, $ipcon)

 :param $uid: string
 :param $ipcon: IPConnection
 :rtype: {1}

 Erzeugt ein Objekt mit der eindeutigen Geräte ID ``$uid``:

 .. code-block:: perl

    ${0} = {1}->new("YOUR_DEVICE_UID", $ipcon);

 Dieses Objekt kann benutzt werden, nachdem die IP Connection verbunden ist
 (siehe Beispiele :ref:`oben <{0}_{2}_perl_examples>`).
"""
        }

        register_str = {
        'en': """
.. perl:function:: {1}->register_callback($id, $callback)

 :param $id: int
 :param $callback: string
 :rtype: undef

 Registers a callback with ID ``$id`` to the function named ``$callback``. The
 available IDs with corresponding function signatures are listed
 :ref:`below <{0}_{2}_perl_callbacks>`.
""",
        'de': """
.. perl:function:: {1}->register_callback($id, $callback)

 :param $id: int
 :param $callback: string
 :rtype: undef

 Registriert einen Callback mit der ID ``$id`` mit der Funktion namens ``$callback``.
 Die verfügbaren IDs mit den zugehörigen Funktionssignaturen sind
 :ref:`unten <{0}_{2}_perl_callbacks>` zu finden.
"""
        }

        c_str = {
        'en': """
.. _{1}_{2}_perl_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive
time critical or recurring data from the device. The registration is done
with the :perl:func:`register_callback() <{3}->register_callback>` function of
the device object. The first parameter is the callback ID and the second
parameter the callback function name:

.. code-block:: perl

    sub my_callback
    {{
        print "@_[0]";
    }}

    ${1}->register_callback({3}->CALLBACK_EXAMPLE, 'my_callback')

The callback function will be called from an internal thread of the
IP Connection. In contrast to many other programming languages, variables are
not automatically shared between threads in Perl. If you want to share a global
variable between a callback function and the rest for your program it has to be
marked as ``:shared``. See the documentation of the `threads::shared
<http://perldoc.perl.org/threads/shared.html>`__ Perl module for more details.

The available constants with inherent number and type of parameters are
described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{0}
""",
        'de': """
.. _{1}_{2}_perl_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit der Funktion :perl:func:`register_callback() <{3}->register_callback>` des
Geräte Objektes durchgeführt werden. Der erste Parameter ist die Callback ID
und der zweite Parameter ist der Name der Callback-Funktion:

.. code-block:: perl

    sub my_callback
    {{
        print "@_[0]";
    }}

    ${1}->register_callback({3}->CALLBACK_EXAMPLE, 'my_callback')

Die Callback Funktion wird dann von einem internen Thread der IP Connection
aufgerufen werden. Im Gegensatz zu vielen anderen Programmiersprachen werden
Variablen nicht automatisch zwischen Threads geteilt. Wenn eine Variable
gleichzeitig in einer Callback Funktion und dem Rest des Programms genutzt
werden soll, dann muss diese als ``:shared`` markiert werden. Siehe dazu auch
die Dokumentation des `threads::shared
<http://perldoc.perl.org/threads/shared.html>`__ Perl Moduls für weitere
Details.

Die verfügbaren IDs mit der dazugehörigen Parameteranzahl und -typen werden
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

All methods listed below are thread-safe.

{1}

{2}
""",
        'de': """
{0}
API
---

Alle folgend aufgelisteten Funktionen sind Thread-sicher.

{1}

{2}
"""
        }

        const_str = {
        'en' : """
.. _{5}_{6}_perl_constants:

Constants
^^^^^^^^^

.. perl:attribute:: {0}->DEVICE_IDENTIFIER

 This constant is used to identify a {3} {4}.

 The :perl:func:`get_identity() <{4}{3}->get_identity>` function and the
 :perl:attr:`CALLBACK_ENUMERATE <IPConnection.CALLBACK_ENUMERATE>`
 callback of the IP Connection have a ``device_identifier`` parameter to specify
 the Brick's or Bricklet's type.
""",
        'de' : """
.. _{5}_{6}_perl_constants:

Konstanten
^^^^^^^^^^

.. perl:attribute:: {0}->DEVICE_IDENTIFIER

 Diese Konstante wird verwendet um {2} {3} {4} zu identifizieren.

 Die :perl:func:`get_identity() <{4}{3}->get_identity>` Funktion und der
 :perl:attr:`CALLBACK_ENUMERATE <IPConnection.CALLBACK_ENUMERATE>`
 Callback der IP Connection haben ein ``device_identifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.
"""
        }

        cre = common.select_lang(create_str).format(self.get_underscore_name(),
                                                    self.get_perl_class_name(),
                                                    self.get_category().lower())
        reg = common.select_lang(register_str).format(self.get_underscore_name(),
                                                      self.get_perl_class_name(),
                                                      self.get_category().lower())

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
            api_str += common.select_lang(c_str).format(c, self.get_underscore_name(),
                                                        self.get_category().lower(),
                                                        self.get_perl_class_name())

        article = 'ein'
        if self.get_category() == 'Brick':
            article = 'einen'
        api_str += common.select_lang(const_str).format(self.get_perl_class_name(),
                                                        self.get_category(),
                                                        article,
                                                        self.get_camel_case_name(),
                                                        self.get_category(),
                                                        self.get_underscore_name(),
                                                        self.get_category().lower())

        ref = '.. _{0}_{1}_perl_api:\n'.format(self.get_underscore_name(),
                                               self.get_category().lower())

        return common.select_lang(api).format(ref, self.get_api_doc(), api_str)

    def get_perl_doc(self):
        title = { 'en': 'Perl bindings', 'de': 'Perl Bindings' }

        doc  = common.make_rst_header(self, 'Perl')
        doc += common.make_rst_summary(self, common.select_lang(title))
        doc += self.get_perl_examples()
        doc += self.get_perl_api()

        return doc

class PerlDocPacket(common.Packet):
    def get_perl_parameter_list(self):
        params = []

        for element in self.get_elements('in'):
            params.append(element.get_perl_doc_name())

        return ', '.join(params)

    def get_perl_formatted_doc(self):
        text = common.select_lang(self.get_doc()[1])
        cls = self.get_device().get_perl_class_name()
        for other_packet in self.get_device().get_packets():
            name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
            if other_packet.get_type() == 'callback':
                name_upper = other_packet.get_upper_case_name()
                name_right = ':perl:attr:`CALLBACK_{1} <{0}->CALLBACK_{1}>`'.format(cls, name_upper)
            else:
                name_right = ':perl:func:`{1}() <{0}->{1}>`'.format(cls, other_packet.get_underscore_name())
            text = text.replace(name_false, name_right)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = self.get_device().get_perl_class_name() + '->'
        if self.get_underscore_name() == 'set_response_expected':
            text += common.format_function_id_constants(prefix, self.get_device())
        else:
            text += common.format_constants(prefix, self)

        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

    def get_perl_parameter_desc(self, io):
        desc = '\n'
        param = ' :param {0}: {1}\n'
        for element in self.get_elements(io):
            t = element.get_perl_type()
            desc += param.format(element.get_perl_doc_name(), t)

        return desc

    def get_perl_return_desc(self):
        ret = ' :rtype: {0}\n'
        ret_list = []
        for element in self.get_elements('out'):
            ret_list.append(element.get_perl_type())
        if len(ret_list) == 0:
            return ret.format('undef')
        elif len(ret_list) == 1:
            return ret.format(ret_list[0])

        return ret.format('[' + ', '.join(ret_list) + ']')

    def get_perl_object_desc(self):
        if len(self.get_elements('out')) < 2:
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
        for element in self.get_elements('out'):
            var.append('``{0}``'.format(element.get_underscore_name()))

        if len(var) == 1:
            return common.select_lang(desc).format(var[0])

        if len(var) == 2:
            return common.select_lang(desc).format(var[0] + common.select_lang(and_) + var[1])

        return common.select_lang(desc).format(', '.join(var[:-1]) + common.select_lang(and_) + var[-1])

class PerlDocGenerator(common.DocGenerator):
    def get_bindings_name(self):
        return 'perl'

    def get_doc_rst_name(self):
        return 'Perl'

    def get_doc_example_regex(self):
        return '^example_.*\.pl$'

    def get_device_class(self):
        return PerlDocDevice

    def get_packet_class(self):
        return PerlDocPacket

    def get_element_class(self):
        return perl_common.PerlElement

    def generate(self, device):
        rst = open(device.get_doc_rst_path(), 'wb')
        rst.write(device.get_perl_doc())
        rst.close()

def generate(bindings_root_directory, language):
    common.generate(bindings_root_directory, language, PerlDocGenerator)

if __name__ == "__main__":
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
