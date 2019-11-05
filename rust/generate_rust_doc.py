#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Rust Documentation Generator
Copyright (C) 2018 Erik Fleckstein <erik@tinkerforge.com>
Copyright (C) 2019 Matthias Bolte <matthias@tinkerforge.com>

generate_rust_doc.py: Generator for Rust documentation

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
import rust_common

class RustDocDevice(rust_common.RustDevice):
    def specialize_rust_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':rust:func:`{0}::get_{1}_callback_receiver`'.format(packet.get_device().get_rust_name(),
                                                            packet.get_name(skip=-2 if high_level else 0).under)
            else:
                return ':rust:func:`{0}::{1}`'.format(packet.get_device().get_rust_name(),
                                                   packet.get_name(skip=-2 if high_level else 0).under)

        return self.specialize_doc_rst_links(text, specializer, prefix='rust')

    def get_rust_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('example_', '').replace('.rs', '')
            return common.under_to_space(filename).replace('Pwm ', 'PWM ')

        return common.make_rst_examples(title_from_filename, self)

    def get_rust_methods(self, type_):
        methods = ''
        func_start = '.. rust:function:: '

        synchronous_methods = ["get_api_version", "get_response_expected", "set_response_expected", "set_response_expected_all"]

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type_:
                continue

            skip = -2 if packet.has_high_level() else 0
            name = packet.get_name(skip=skip).under
            plist = common.wrap_non_empty(', ', packet.get_rust_parameters(high_level=True), '')
            returns = packet.get_rust_return_type(high_level=packet.has_high_level())

            if not packet.has_high_level() and name not in synchronous_methods:
                returns = "ConvertingReceiver<" + returns + ">"
            if "et_response_expected" in name:
                params = '&mut self{}'.format(plist)
            else:
                params = '&self{}'.format(plist)

            meta = packet.get_formatted_element_meta(lambda element: element.get_rust_type(for_doc=True),
                                                     lambda element: element.get_name().under,
                                                     lambda constant_group: constant_group.get_name().upper,
                                                     return_object='conditional',
                                                     explicit_string_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_rust_formatted_doc()
            func = '{start}{struct_name}::{func_name}({params})-> {returns}\n\n{meta_table}{desc}'.format(start=func_start, struct_name=self.get_rust_name(), func_name=name, params=params, returns=returns, meta_table=meta_table, desc=desc)
            methods += func + '\n'

        return methods

    def get_rust_callbacks(self):
        cb = {
        'en': """
.. rust:function:: {device}::get_{callback_name_under}_callback_receiver(&self) -> {receiver_type}<{result_type}>

{meta_table}

 Receivers created with this function receive {callback_name_space} events.

{desc}
""",
            'de': """
.. rust:function:: {device}::get_{callback_name_under}_callback_receiver(&self) -> {receiver_type}<{result_type}>

{meta_table}

 Receiver die mit dieser Funktion erstellt werden, empfangen {callback_name_space}-Events.

{desc}
"""
        }

        cbs = ''
        device = self.get_rust_name()

        for packet in self.get_packets('callback'):
            meta = packet.get_formatted_element_meta(lambda element: element.get_rust_type(for_doc=True),
                                                     lambda element: element.get_name().under,
                                                     lambda constant_group: constant_group.get_name().upper,
                                                     callback_object='conditional',
                                                     callback_parameter_title_override={'en': 'Event', 'de': 'Event'},
                                                     callback_object_title_override={'en': 'Event Object', 'de': 'Event-Objekt'},
                                                     explicit_string_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_rust_formatted_doc()

            if packet.has_high_level():
                skip = -2
                receiver_type = "ConvertingHighLevelCallbackReceiver"
                result_type = ", ".join([packet.get_high_level_payload_type(), packet.get_name(skip=-2).camel_abbrv+"Result", packet.get_rust_return_type()])
            else:
                skip = 0
                receiver_type = "ConvertingCallbackReceiver"
                result_type = packet.get_rust_return_type()

            cbs += common.select_lang(cb).format(device=device,
                                                 callback_name_under=packet.get_name(skip=skip).under,
                                                 callback_name_space=packet.get_name(skip=skip).space,
                                                 receiver_type=receiver_type,
                                                 result_type=result_type,
                                                 meta_table=meta_table,
                                                 desc=desc)

        return cbs

    def get_rust_api(self):
        create_str = {
            'en': """
.. rust:function:: {device_camel}::new(uid: &str, ip_connection: &IpConnection) -> {device_camel}

{meta_table}

 Creates a new ``{device_camel}`` object with the unique device ID ``uid`` and adds
 it to the IPConnection ``ip_connection``:

 .. code-block:: rust

    let {device_under} = {device_camel}::new("YOUR_DEVICE_UID", &ip_connection);

 This device object can be used after the IP connection has been connected
 (see examples :ref:`above <{rst_ref_name}_rust_examples>`).
""",
            'de': """
.. rust:function:: {device_camel}::new(uid: &str, ip_connection: &IpConnection) -> {device_camel}

{meta_table}

 Erzeugt ein neues ``{device_camel}``-Objekt mit der eindeutigen Geräte ID ``uid`` und
 fügt es der IP-Connection ``ip_connection`` hinzu:

 .. code-block:: rust

    let {device_under} = {device_camel}::new("YOUR_DEVICE_UID", &ip_connection);

 Dieses Geräteobjekt kann benutzt werden, nachdem die IP-Connection verbunden
 wurde (siehe Beispiele :ref:`oben <{rst_ref_name}_rust_examples>`).
"""
        }

        c_str = {
            'en': """
.. _{0}_rust_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive
time critical or recurring data from the device. The registration is done
with the corresponding `get_*_callback_receiver` function, which returns a receiver
for callback events.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{3}
""",
            'de': """
.. _{0}_rust_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit der entsprechenden `get_*_callback_receiver`-Function durchgeführt werden,
welche einen Receiver für Callback-Events zurück gibt.

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
.. _{0}_rust_api:

API
---

To allow non-blocking usage, nearly every function of the Rust bindings returns
a wrapper around a mpsc::Receiver. To block until the function has finished and
get your result, call one of the receiver's recv variants. Those return either
the result sent by the device, or any error occured.

Functions returning a result directly will block until the device has finished
processing the request.

All functions listed below are thread-safe, those which return a receiver are lock-free.

{1}

{2}
""",
            'de': """
.. _{0}_rust_api:

API
---
Um eine nicht-blockierende Verwendung zu erlauben, gibt fast jede Funktion der Rust-Bindings
einen Wrapper um einen mpsc::Receiver zurück. Um das Ergebnis eines Funktionsaufrufs zu erhalten
und zu blockieren, bis das Gerät die Anfrage verarbeitet hat, können die recv-Varianten des
Receivers verwendet werden. Diese geben entweder das vom Gerät gesendete Ergebnis, oder einen
aufgetretenen Fehler zurück.

Funktionen die direkt ein Result zurückgeben, blockieren bis das Gerät die Anfrage verarbeitet hat.

Alle folgend aufgelisteten Funktionen sind Thread-sicher, diese, die einen Receiver zurückgeben, sind
Lock-frei.

{1}

{2}
"""
        }

        const_str = {
            'en': """
.. _{device_name_ref}_rust_constants:

Constants
^^^^^^^^^

.. rust:constant:: {device_name_camel}::DEVICE_IDENTIFIER: u16

 This constant is used to identify a {device_name_display}.

 The :rust:func:`{device_name_camel}::get_identity()` function and the :rust:func:`IpConnection::get_enumerate_callback_receiver()`
 callback of the IP Connection have a ``device_identifier`` parameter to specify
 the Brick's or Bricklet's type.

.. rust:constant:: {device_name_camel}::DEVICE_DISPLAY_NAME: &str

 This constant represents the human readable name of a {device_name_display}.
""",
            'de': """
.. _{device_name_ref}_rust_constants:

Konstanten
^^^^^^^^^^

.. rust:constant:: {device_name_camel}::DEVICE_IDENTIFIER: u16

 Diese Konstante wird verwendet um {article} {device_name_display} zu identifizieren.

 Die :rust:func:`{device_name_camel}::get_identity()` Funktion und der :rust:func:`IpConnection::get_enumerate_callback_receiver()`
 Callback der IP Connection haben ein ``device_identifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. rust:constant:: {device_name_camel}::DEVICE_DISPLAY_NAME: &str

 Diese Konstante stellt den Anzeigenamen eines {device_name_display} dar.
"""
        }

        create_meta = common.format_simple_element_meta([('uid', '&str', 1, 'in'),
                                                         ('ip_connection', '&IPConnection', 1, 'in'),
                                                         (self.get_name().under, self.get_rust_name(), 1, 'out')])
        create_meta_table = common.make_rst_meta_table(create_meta)

        cre = common.select_lang(create_str).format(rst_ref_name=self.get_doc_rst_ref_name(),
                                                    device_camel=self.get_rust_name(),
                                                    device_under=self.get_name().under,
                                                    meta_table=create_meta_table)
        bf = self.get_rust_methods('bf')
        af = self.get_rust_methods('af')
        ccf = self.get_rust_methods('ccf')
        c = self.get_rust_callbacks()
        api_str = ''
        if bf:
            api_str += common.select_lang(common.bf_str).format(cre, bf)
        if af:
            api_str += common.select_lang(common.af_str).format(af)
        if c:
            if len(ccf) > 0:
                api_str += common.select_lang(common.ccf_str).format("", ccf)
            api_str += common.select_lang(c_str).format(self.get_doc_rst_ref_name(),
                                                        self.get_name().under,
                                                        self.get_name().upper,
                                                        c)

        article = 'ein'
        if self.is_brick():
            article = 'einen'
        api_str += common.select_lang(const_str).format(device_name_ref=self.get_doc_rst_ref_name(),
                                                        device_name_camel=self.get_rust_name(),
                                                        article=article,
                                                        device_name_display=self.get_long_display_name())

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.specialize_rust_doc_function_links(common.select_lang(self.get_doc())),
                                              api_str)

    def get_rust_doc(self):
        docs_rs = {'en': 'Additional documentation can be found on `docs.rs <https://docs.rs/tinkerforge/latest/tinkerforge/{module_name}/index.html>`_.\n',
                   'de': 'Zusätzliche Dokumentation findet sich auf `docs.rs <https://docs.rs/tinkerforge/latest/tinkerforge/{module_name}/index.html>`_.\n'}

        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += common.select_lang(docs_rs).format(module_name=self.get_rust_module_name())
        doc += self.get_rust_examples()
        doc += self.get_rust_api()

        return doc

class RustDocPacket(rust_common.RustPacket):
    def get_rust_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())
        text = self.get_device().specialize_rust_doc_function_links(text)

        callback_parameter = {'en': 'received variable', 'de': 'empfangene Variable'}
        callback_parameters = {'en': 'members of the received struct', 'de': 'Felder der empfangenen Struktur'}

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)

        if self.get_type() == 'callback':
            text = common.handle_rst_word(text, parameter=callback_parameter, parameters=callback_parameters)
        else:
            text = common.handle_rst_word(text)

        text = common.handle_rst_substitutions(text, self)

        prefix = self.get_device().get_rust_module_name().upper() + '_'

        text += common.format_constants(prefix, self, bool_format_func=lambda value: str(value).lower())
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

class RustDocGenerator(rust_common.RustGeneratorTrait, common.DocGenerator):
    def get_bindings_name(self):
        return 'rust'

    def get_bindings_display_name(self):
        return 'Rust'

    def get_doc_rst_filename_part(self):
        return 'Rust'

    def get_doc_example_regex(self):
        return r'^example_.*\.rs$'

    def get_device_class(self):
        return RustDocDevice

    def get_packet_class(self):
        return RustDocPacket

    def get_element_class(self):
        return rust_common.RustElement

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_rust_doc())

def generate(root_dir, language):
    common.generate(root_dir, language, RustDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print('=== Generating %s ===' % language)
        generate(os.getcwd(), language)
