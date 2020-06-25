#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Shell Documentation Generator
Copyright (C) 2012-2015, 2017-2018, 2020 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2013 Olaf Lüke <olaf@tinkerforge.com>

generate_shell_doc.py: Generator for Shell documentation

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
import importlib.util
import importlib.machinery

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

    if sys.hexversion < 0x3050000:
        generators_module = importlib.machinery.SourceFileLoader('generators', os.path.join(generators_dir, '__init__.py')).load_module()
    else:
        generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
        generators_module = importlib.util.module_from_spec(generators_spec)

        generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common
from generators.shell import shell_common

class ShellDocDevice(shell_common.ShellDevice):
    def specialize_shell_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':sh:cb:`{1} <{0} {1}>`'.format(packet.get_device().get_shell_device_name(),
                                                       packet.get_name(skip=-2 if high_level else 0).dash)
            else:
                return ':sh:func:`{1} <{0} {1}>`'.format(packet.get_device().get_shell_device_name(),
                                                         packet.get_name(skip=-2 if high_level else 0).dash)

        return self.specialize_doc_rst_links(text, specializer, prefix='sh')

    def get_shell_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('example-', '').replace('.sh', '').replace('-', '_')
            return common.under_to_space(filename)

        def language_from_filename(filename):
            return 'bash'

        return common.make_rst_examples(title_from_filename, self,
                                        language_from_filename=language_from_filename)

    def get_shell_functions(self, type_):
        functions = []
        template = '.. sh:function:: tinkerforge call {0} <uid> {1} {2}\n\n{3}{4}\n'
        device_name = self.get_shell_device_name()

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type_ or packet.is_virtual():
                continue

            skip = -2 if packet.has_high_level() else 0
            name = packet.get_name(skip=skip).dash
            params = packet.get_shell_parameter_list(high_level=True)
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_shell_doc_type(cardinality=cardinality),
                                                     lambda element, index=None: '<{0}>'.format(element.get_name(index=index).dash) if element.get_direction() == 'in' else element.get_name(index=index).dash,
                                                     return_label_override={'en': 'Output', 'de': 'Ausgabe'},
                                                     constants_hint_override={'en': ('See symbols', 'with symbols'), 'de': ('Siehe Symbole', 'mit Symbolen')},
                                                     no_out_value={'en': 'no output', 'de': 'keine Ausgabe'},
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_shell_formatted_doc()

            functions.append(template.format(device_name, name, params, meta_table, desc))

        return ''.join(functions)

    def get_shell_callbacks(self):
        callbacks = []
        template = '.. sh:callback:: tinkerforge dispatch {0} <uid> {1}\n\n{2}{3}\n'
        device_name = self.get_shell_device_name()

        for packet in self.get_packets('callback'):
            if packet.is_virtual():
                continue

            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_shell_doc_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).dash,
                                                     callback_parameter_label_override={'en': 'Output', 'de': 'Ausgabe'},
                                                     constants_hint_override={'en': ('See symbols', 'with symbols'), 'de': ('Siehe Symbole', 'mit Symbolen')},
                                                     no_out_value={'en': 'no output', 'de': 'keine Ausgabe'},
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_shell_formatted_doc()
            skip = -2 if packet.has_high_level() else 0

            callbacks.append(template.format(device_name, packet.get_name(skip).dash, meta_table, desc))

        return ''.join(callbacks)

    def get_shell_api(self):
        c_str = {
            'en': """
.. _{0}_shell_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be used to receive time critical or recurring data from the
device:

.. code-block:: bash

    tinkerforge dispatch {1} <uid> example

The available callbacks are described below.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{2}
""",
            'de': """
.. _{0}_shell_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische oder wiederkehrende Daten
vom Gerät zu erhalten:

.. code-block:: bash

    tinkerforge dispatch {1} <uid> example

Die verfügbaren Callbacks werden weiter unten beschrieben.

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
.. _{0}_shell_api:

API
---

Possible exit codes for all ``tinkerforge`` commands are:

* 1: interrupted (ctrl+c)
* 2: syntax error
* 21: Python 2.5 or newer is required
* 22: Python ``argparse`` module is missing
* 23: socket error
* 24: other exception
* 25: invalid placeholder in format string
* 26: authentication error
* 201: timeout occurred
* 209: invalid argument value
* 210: function is not supported
* 211: unknown error

{1}

Command Structure
^^^^^^^^^^^^^^^^^

The common options of the ``call`` and ``dispatch`` commands are documented
:ref:`here <ipcon_shell_api>`. The specific command structure is shown below.

.. sh:function:: X Stinkerforge Pcall N{3} A[<option>..] L<uid> L<function> L[<argument>..]

{5}

 The ``call`` command is used to call a function of the {4}. It can take several
 options:

 * ``--help`` shows help for the specific ``call`` command and exits
 * ``--list-functions`` shows a list of known functions of the {4} and exits


.. sh:callback:: X Stinkerforge Pdispatch N{3} A[<option>..] L<uid> L<callback>

{6}

 The ``dispatch`` command is used to dispatch a callback of the {4}. It can
 take several options:

 * ``--help`` shows help for the specific ``dispatch`` command and exits
 * ``--list-callbacks`` shows a list of known callbacks of the {4} and exits


.. sh:function:: X Stinkerforge Scall P{3} L<uid> N<function> A[<option>..] L[<argument>..]

{5}

 The ``<function>`` to be called can take different options depending of its
 kind. All functions can take the following options:

 * ``--help`` shows help for the specific function and exits

 Getter functions can take the following options:

 * ``--execute <command>`` shell command line to execute for each incoming
   response (see section about :ref:`output formatting <ipcon_shell_output>`
   for details)

 Setter functions can take the following options:

 * ``--expect-response`` requests response and waits for it

 The ``--expect-response`` option for setter functions allows to detect
 timeouts and other error conditions calls of setters as well. The device will
 then send a response for this purpose. If this option is not given for a
 setter function then no response is sent and errors are silently ignored,
 because they cannot be detected.


.. sh:callback:: X Stinkerforge Sdispatch P{3} L<uid> N<callback> A[<option>..]

{6}

 The ``<callback>`` to be dispatched can take several options:

 * ``--help`` shows help for the specific callback and exits
 * ``--execute <command>`` shell command line to execute for each incoming
   response (see section about :ref:`output formatting <ipcon_shell_output>`
   for details)


{2}
""",
            'de': """
.. _{0}_shell_api:

API
---

Mögliche Exit Codes für alle ``tinkerforge`` Befehle sind:

* 1: Unterbrochen (Ctrl+C)
* 2: Syntaxfehler
* 21: Python 2.5 oder neuer wird benötigt
* 22: Python ``argparse`` Modul fehlt
* 23: Socket-Fehler
* 24: Andere Exception
* 25: Ungültiger Platzhalter in Format-String
* 26: Authentifizierungsfehler
* 201: Timeout ist aufgetreten
* 209: Ungültiger Argumentwert
* 210: Funktion wird nicht unterstützt
* 211: Unbekannter Fehler

{1}

Befehlsstruktur
^^^^^^^^^^^^^^^

Allgemeine Optionen des ``call`` und des ``dispatch`` Befehls sind
:ref:`hier <ipcon_shell_api>` zu finden. Im Folgenden wird die spezifische
Befehlsstruktur dargestellt.

.. sh:function:: X Stinkerforge Pcall N{3} A[<option>..] L<uid> L<function> L[<argument>..]

{5}

 Der ``call`` Befehl wird verwendet um eine Funktion des {4} aufzurufen. Der
 Befehl kennt mehrere Optionen:

 * ``--help`` zeigt Hilfe für den spezifischen ``call`` Befehl an und endet dann
 * ``--list-functions`` zeigt eine Liste der bekannten Funktionen des {4} an
   und endet dann


.. sh:callback:: X Stinkerforge Pdispatch N{3} A[<option>..] L<uid> L<callback>

{6}

 Der ``dispatch`` Befehl wird verwendet um eingehende Callbacks des {4}
 abzufertigen. Der Befehl kennt mehrere Optionen:

 * ``--help`` zeigt Hilfe für den spezifischen ``dispatch`` Befehl an und endet
   dann
 * ``--list-callbacks`` zeigt eine Liste der bekannten Callbacks des {4} an
   und endet dann


.. sh:function:: X Stinkerforge Scall P{3} L<uid> N<function> A[<option>..] L[<argument>..]

{5}

 Abhängig von der Art der aufzurufenden ``<function>`` kennt diese verschiedene
 Optionen. Alle Funktionen kennen die folgenden Optionen:

 * ``--help`` zeigt Hilfe für die spezifische ``<function>`` an und endet dann

 Getter-Funktionen kennen zusätzlich die folgenden Optionen:

 * ``--execute <command>`` Shell-Befehl der für jede eingehende Antwort
   ausgeführt wird (siehe den Abschnitt über :ref:`Ausgabeformatierung
   <ipcon_shell_output>` für Details)

 Setter-Funktionen kennen zusätzlich die folgenden Optionen:

 * ``--expect-response`` fragt Antwort an und wartet auf diese

 Mit der ``--expect-response`` Option für Setter-Funktionen können Timeouts und
 andere Fehlerfälle auch für Aufrufe von Setter-Funktionen detektiert werden.
 Das Gerät sendet dann eine Antwort extra für diesen Zweck. Wenn diese Option
 für eine Setter-Funktion nicht angegeben ist, dann wird keine Antwort vom
 Gerät gesendet und Fehler werden stillschweigend ignoriert, da sie nicht
 detektiert werden können.


.. sh:callback:: X Stinkerforge Sdispatch P{3} L<uid> N<callback> A[<option>..]

{6}

 Der abzufertigende ``<callback>`` kennt mehrere Optionen:

 * ``--help`` zeigt Hilfe für den spezifische ``<callback>`` an und endet dann
 * ``--execute <command>`` Shell-Befehlszeile der für jede eingehende Antwort
   ausgeführt wird (siehe den Abschnitt über :ref:`Ausgabeformatierung
   <ipcon_shell_output>` für Details)

{2}
"""
        }

        bf = self.get_shell_functions('bf')
        af = self.get_shell_functions('af')
        ccf = self.get_shell_functions('ccf')
        c = self.get_shell_callbacks()
        vf = self.get_shell_functions('vf')
        if_ = self.get_shell_functions('if')
        api_str = ''

        if bf:
            api_str += common.select_lang(common.bf_str).format('', bf)

        if af:
            api_str += common.select_lang(common.af_str).format(af)

        if c:
            if ccf:
                api_str += common.select_lang(common.ccf_str).format('', ccf)

            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_shell_device_name(),
                                                        c)

        if vf:
            api_str += common.select_lang(common.vf_str).format(vf)

        if if_:
            api_str += common.select_lang(common.if_str).format(if_)

        call_meta = common.format_simple_element_meta([('<uid>', 'String', 1, 'in'),
                                                       ('<function>', 'String', 1, 'in')])
        call_meta_table = common.make_rst_meta_table(call_meta)

        dispatch_meta = common.format_simple_element_meta([('<uid>', 'String', 1, 'in'),
                                                           ('<callback>', 'String', 1, 'in')])
        dispatch_meta_table = common.make_rst_meta_table(dispatch_meta)

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.specialize_shell_doc_function_links(common.select_lang(self.get_doc())),
                                              api_str,
                                              self.get_shell_device_name(),
                                              self.get_long_display_name(),
                                              call_meta_table,
                                              dispatch_meta_table)

    def get_shell_doc(self):
        doc  = common.make_rst_header(self, has_device_identifier_constant=False)
        doc += common.make_rst_summary(self)
        doc += self.get_shell_examples()
        doc += self.get_shell_api()

        return doc

class ShellDocPacket(shell_common.ShellPacket):
    def get_shell_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())
        text = self.get_device().specialize_shell_doc_function_links(text)

        constants = {'en': 'symbols', 'de': 'Symbole'}

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        def format_element_name(element, index):
            if element.get_direction() == 'in':
                template = '<{0}>'
            else:
                template = '{0}'

            if index == None:
                return template.format(element.get_name().dash)

            return template.format(element.get_name().dash) + '[{0}]'.format(index)

        def format_constant(prefix, constant_group, constant, value):
            return '* **{0}**-{1} = {2}\n'.format(constant_group.get_name().dash, constant.get_name().dash, value)

        text += common.format_constants('', self, format_element_name,
                                        constants_name=constants,
                                        constant_format_func=format_constant)

        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

class ShellDocGenerator(shell_common.ShellGeneratorTrait, common.DocGenerator):
    def get_doc_rst_filename_part(self):
        return 'Shell'

    def get_doc_example_regex(self):
        return r'^example-.*\.sh$'

    def get_device_class(self):
        return ShellDocDevice

    def get_packet_class(self):
        return ShellDocPacket

    def get_element_class(self):
        return shell_common.ShellElement

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_shell_doc())

def generate(root_dir, language):
    common.generate(root_dir, language, ShellDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print('=== Generating %s ===' % language)
        generate(os.getcwd(), language)
