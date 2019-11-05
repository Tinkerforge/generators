#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Go Documentation Generator
Copyright (C) 2018 Erik Fleckstein <erik@tinkerforge.com>
Copyright (C) 2019 Matthias Bolte <matthias@tinkerforge.com>

generate_go_doc.py: Generator for Go documentation

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
import go_common

class GoDocDevice(go_common.GoDevice):
    def specialize_go_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':go:func:`Register{1}Callback <(*{0}) Register{1}Callback>`' \
                       .format(packet.get_device().get_go_name(),
                               packet.get_name(skip=-2 if high_level else 0).camel)
            else:
                return ':go:func:`{1}() <(*{0}) {1}>`' \
                       .format(packet.get_device().get_go_name(),
                               packet.get_name(skip=-2 if high_level else 0).camel)

        return self.specialize_doc_rst_links(text, specializer, prefix='go')

    def get_go_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('example_', '').replace('.go', '')
            return common.under_to_space(filename).replace('Pwm ', 'PWM ')

        return common.make_rst_examples(title_from_filename, self)

    def get_go_methods(self, type_):
        methods = ''
        func_start = '.. go:function:: '

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type_:
                continue

            skip = -2 if packet.has_high_level() else 0
            name = packet.get_name(skip=skip).camel
            params = packet.get_go_parameters(high_level=True, ignore_constant_group=True)
            meta = packet.get_formatted_element_meta(lambda element: element.get_go_type(ignore_constant_group=True, context='meta'),
                                                     lambda element: element.get_name().headless,
                                                     lambda constant_group: constant_group.get_name().camel,
                                                     suffix_elements=[('err', 'error', 1, 'out')],
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            returns = packet.get_go_return_type(high_level=True, ignore_constant_group=True)
            desc = packet.get_go_formatted_doc()
            func = '{start}func (*{struct_name}) {func_name}({params}) ({returns})\n\n{meta_table}\n{desc}' \
                   .format(start=func_start, struct_name=self.get_go_name(), func_name=name, params=params, returns=returns, meta_table=meta_table, desc=desc)
            methods += func + '\n'

        return methods

    def get_go_callbacks(self):
        cb = {
        'en': """
.. go:function:: func (*{device}) Register{callback_name_camel}Callback(func({result_type})) (registrationId uint64)

{meta}

{desc}
""",
            'de': """
.. go:function:: func (*{device}) Register{callback_name_camel}Callback(func({result_type})) (registrationId uint64)

{meta}

{desc}
"""
        }

        cbs = ''
        device = self.get_go_name()
        for packet in self.get_packets('callback'):
            skip = -2 if packet.has_high_level() else 0
            desc = packet.get_go_formatted_doc()
            result_type = packet.get_go_return_type(high_level=packet.has_high_level(), ignore_constant_group=True)
            meta = packet.get_formatted_element_meta(lambda element: element.get_go_type(ignore_constant_group=True, context='meta'),
                                                     lambda element: element.get_name().headless,
                                                     lambda constant_group: constant_group.get_name().camel,
                                                     suffix_elements=[('registrationId', 'uint64', 1, 'return')],
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     high_level=True)
            meta_table = common.make_rst_meta_table(meta)

            cbs += common.select_lang(cb).format(device=device,
                                                 callback_name_camel=packet.get_name(skip=skip).camel,
                                                 callback_name_space=packet.get_name(skip=skip).space,
                                                 result_type=result_type,
                                                 meta=meta_table,
                                                 desc=desc)
        return cbs
    def get_go_api(self):
        create_str = {
            'en': """
.. go:function:: func {device_name_under}.New{device_name_camel}(uid string, ipcon *IPConnection) (device {device_name_camel}, err error)

{meta}

 Creates a new ``{device_name_camel}`` object with the unique device ID ``uid`` and adds
 it to the IPConnection ``ipcon``:

 .. code-block:: go

    device, err := {device_name_under}.New("YOUR_DEVICE_UID", &ipcon)

 This device object can be used after the IPConnection has been connected
 (see examples :ref:`above <{rst_ref_name}_go_examples>`).
""",
            'de': """
.. go:function:: func {device_name_under}.New{device_name_camel}(uid string, ipcon *IPConnection) (device {device_name_camel}, err error)

{meta}

 Erzeugt ein neues ``{device_name_camel}``-Objekt mit der eindeutigen Geräte ID ``uid`` und
 fügt es der IPConnection ``ipcon`` hinzu:

 .. code-block:: go

    device, err := {device_name_under}.New("YOUR_DEVICE_UID", &ipcon)

 Dieses Geräteobjekt kann benutzt werden, nachdem die IPConnection verbunden
 wurde (siehe Beispiele :ref:`oben <{rst_ref_name}_go_examples>`).
"""
        }

        c_str = {
            'en': """
.. _{0}_go_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive
time critical or recurring data from the device. The registration is done
with the corresponding ``Register*Callback`` function, which returns a unique callback ID.
This ID can be used to deregister the callback later with the corresponding ``Deregister*Callback``
function.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{3}
""",
            'de': """
.. _{0}_go_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit der entsprechenden ``Register*Callback``-Function durchgeführt werden,
welche eine eindeutige Callback-ID zurück gibt. Mit dieser ID kann das Callback
später deregistriert werden.

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
.. _{0}_go_api:

API
---

The {device_name_display} API is defined in the package ``github.com/Tinkerforge/go-api-bindings/{device_name_under}``

Nearly every function of the Go bindings can return an
``ipconnection.DeviceError``, implementing the error interface. The error can have one of the following values:

* ipconnection.\\ **DeviceError**\\ Success = 0
* ipconnection.\\ **DeviceError**\\ InvalidParameter = 1
* ipconnection.\\ **DeviceError**\\ FunctionNotSupported = 2
* ipconnection.\\ **DeviceError**\\ UnknownError = 3

which correspond to the values returned from Bricks and Bricklets.

All functions listed below are thread-safe.

{1}

{2}
""",
            'de': """
.. _{0}_go_api:

API
---

Die API des {device_name_display} ist im Package ``github.com/Tinkerforge/go-api-bindings/{device_name_under}`` definiert.

Fast alle Funktionen der Go Bindings können einen ``ipconnection.DeviceError``, der das error-Interface implementiert,
zurückgeben. Dieser kann folgende Werte annehmen:

* ipconnection.\\ **DeviceError**\\ Success = 0
* ipconnection.\\ **DeviceError**\\ InvalidParameter = 1
* ipconnection.\\ **DeviceError**\\ FunctionNotSupported = 2
* ipconnection.\\ **DeviceError**\\ UnknownError = 3

welche den Werten entsprechen, die der Brick oder das Bricklet zurückgeben.

Alle folgend aufgelisteten Funktionen sind Thread-sicher.

{1}

{2}
"""
        }

        const_str = {
            'en': """
.. _{device_name_ref}_go_constants:

Constants
^^^^^^^^^

.. go:constant:: {device_name_under}.DeviceIdentifier

 This constant is used to identify a {device_name_display}.

 The :go:func:`GetIdentity() <(*{device_name_camel}) GetIdentity>` function and
 the :go:func:`(*IPConnection) RegisterEnumerateCallback`
 callback of the IPConnection have a ``deviceIdentifier`` parameter to specify
 the Brick's or Bricklet's type.

.. go:constant:: {device_name_under}.DeviceDisplayName

 This constant represents the human readable name of a {device_name_display}.
""",
            'de': """
.. _{device_name_ref}_go_constants:

Konstanten
^^^^^^^^^^

.. go:constant:: {device_name_under}.DeviceIdentifier

 Diese Konstante wird verwendet um {article} {device_name_display} zu identifizieren.

 Die :go:func:`GetIdentity() <(*{device_name_camel}) GetIdentity>` Funktion und
 der :go:func:`(*IPConnection) RegisterEnumerateCallback`
 Callback der IPConnection haben ein ``deviceIdentifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.

.. go:constant:: {device_name_under}.DeviceDisplayName

 Diese Konstante stellt den Anzeigenamen eines {device_name_display} dar.
"""
        }

        create_meta = common.format_simple_element_meta([('uid', 'string', 1, 'in'),
                                                         ('ipcon', '*IPConnection', 1, 'in'),
                                                         ('device', self.get_go_name(), 1, 'out'),
                                                         ('err', 'error', 1, 'out')])
        create_meta_table = common.make_rst_meta_table(create_meta)

        cre = common.select_lang(create_str).format(rst_ref_name=self.get_doc_rst_ref_name(),
                                                    device_name_under=self.get_go_package(),
                                                    device_name_camel=self.get_go_name(),
                                                    meta=create_meta_table)
        bf = self.get_go_methods('bf')
        af = self.get_go_methods('af')
        ccf = self.get_go_methods('ccf')
        c = self.get_go_callbacks()
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
                                                        device_name_camel=self.get_go_name(),
                                                        device_name_under=self.get_go_package(),
                                                        article=article,
                                                        device_name_display=self.get_long_display_name())

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.specialize_go_doc_function_links(common.select_lang(self.get_doc())),
                                              api_str,
                                              device_name_display=self.get_long_display_name(),
                                              device_name_under=self.get_go_package())

    def get_go_doc(self):
        docs_rs = {'en': 'Additional documentation can be found on `godoc.org <https://godoc.org/github.com/Tinkerforge/go-api-bindings/{device_name_under}>`_.\n',
                   'de': 'Zusätzliche Dokumentation findet sich auf `godoc.org <https://godoc.org/github.com/Tinkerforge/go-api-bindings/{device_name_under}>`_.\n'}

        doc  = common.make_rst_header(self)
        doc += common.make_rst_summary(self)
        doc += common.select_lang(docs_rs).format(device_name_under=self.get_go_package())
        doc += self.get_go_examples()
        doc += self.get_go_api()

        return doc

class GoDocPacket(go_common.GoPacket):
    def get_go_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())
        text = self.get_device().specialize_go_doc_function_links(text)

        callback_parameter = {'en': 'callback parameter', 'de': 'Parameter des Callbacks'}
        callback_parameters = {'en': 'callback parameters', 'de': 'Parameter des Callbacks'}

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)

        if self.get_type() == 'callback':
            text = common.handle_rst_word(text, parameter=callback_parameter, parameters=callback_parameters)
        else:
            text = common.handle_rst_word(text)

        text = common.handle_rst_substitutions(text, self)

        prefix = self.get_device().get_go_package() + '.'

        def constant_format(prefix, constant_group, constant, value):
            return '* {0}\\ **{1}**\\ {2} = {3}\n'.format(prefix, constant_group.get_name().camel,
                                                          constant.get_name().camel_constant_safe, value)

        text += common.format_constants(prefix, self, constant_format_func=constant_format)
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

class GoDocGenerator(go_common.GoGeneratorTrait, common.DocGenerator):
    def get_bindings_name(self):
        return 'go'

    def get_bindings_display_name(self):
        return 'Go'

    def get_doc_rst_filename_part(self):
        return 'Go'

    def get_doc_example_regex(self):
        return r'^example_.*\.go$'

    def get_device_class(self):
        return GoDocDevice

    def get_packet_class(self):
        return GoDocPacket

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_go_doc())

    def get_doc_null_value_name(self):
        return 'nil'

    def get_doc_formatted_param(self, element):
        return element.get_go_name()

def generate(root_dir, language):
    common.generate(root_dir, language, GoDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print('=== Generating %s ===' % language)
        generate(os.getcwd(), language)
