#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MQTT Documentation Generator
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>
Copyright (C) 2019 Matthias Bolte <matthias@tinkerforge.com>

generate_mqtt_doc.py: Generator for MQTT documentation

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
import mqtt_common

class MQTTDocDevice(mqtt_common.MQTTDevice):
    def specialize_mqtt_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return ':mqtt:func:`register/{0}/<UID>/{1}`'.format(packet.get_device().get_mqtt_device_name(),
                                                                    packet.get_mqtt_name(skip=-2 if high_level else 0))
            else:
                return ':mqtt:func:`request/{0}/<UID>/{1}`'.format(packet.get_device().get_mqtt_device_name(),
                                                                   packet.get_mqtt_name(skip=-2 if high_level else 0))

        return self.specialize_doc_rst_links(text, specializer, prefix='mqtt')

    def get_mqtt_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('example-', '').replace('.txt', '').replace('-','_')
            return common.under_to_space(filename).replace('Pwm ', 'PWM ')

        return common.make_rst_examples(title_from_filename, self, language_from_filename=lambda f: None)

    def get_mqtt_methods(self, type_):
        methods = ''
        func_start = '.. mqtt:function:: '

        for packet in self.get_packets('function'):
            if packet.get_doc_type() != type_:
                continue

            if packet.is_virtual():
                continue

            skip = -2 if packet.has_high_level() else 0
            name = packet.get_mqtt_name(skip=skip)
            meta = packet.get_formatted_element_meta(lambda element: element.get_mqtt_type(for_doc=True),
                                                     lambda element: element.get_name().under,
                                                     lambda constant_group: constant_group.get_name().upper,
                                                     parameter_title_override={'en': 'Request', 'de': 'Anfrage'},
                                                     return_title_override={'en': 'Response', 'de': 'Antwort'},
                                                     no_in_value={'en': 'empty payload', 'de': 'keine Nutzdaten'},
                                                     no_out_value={'en': 'no response', 'de': 'keine Antwort'},
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     include_constants=False,
                                                     high_level=True)

            if packet.get_name().space == 'Get Identity':
                meta += common.format_simple_element_meta([('_display_name', 'string', None, 'out')],
                                                          return_title_override={'en': 'Response', 'de': 'Antwort'})

            meta_table = common.make_rst_meta_table(common.merge_meta_sections(meta))
            desc = packet.get_mqtt_formatted_doc()

            if packet.get_name().under == 'get_identity':
                get_id_desc = {
                    'en': """If symbolic output is not disabled, the device identifier is mapped to the corresponding name in the format used in topics.

 The display name contains the {}'s name in a human readable form.""",
                    'de': """Falls die symbolische Ausgabe nicht deaktiviert wurde, wird der Device Identifier auf den entsprechenden Namen im Format, welches die Topics verwenden, abgebildet.

 Der Display Name enthält den Anzeigenamen des {}."""}
                desc += common.select_lang(get_id_desc).format(self.get_short_display_name())

            func = '{start}request/{struct_name}/<UID>/{func_name}\n\n{meta_table}{desc}'.format(start=func_start, struct_name=self.get_mqtt_device_name(), func_name=name, meta_table=meta_table, desc=desc)
            methods += func + '\n'

        return methods

    def get_mqtt_callbacks(self):
        cb = {
        'en': """
.. mqtt:function:: register/{device}/<UID>/{callback_name_under}\n\n{meta_table}\n

 A callback can be registered for this event by publishing to the ``.../register/{device}/<UID>/{callback_name_under}[/<SUFFIX>]`` topic with the payload "true".
 An added callback can be removed by publishing to the same topic with the payload "false".
 To support multiple (de)registrations, e.g. for message filtering, an optional suffix can be used.

 If the callback is triggered, a message with it's payload is published under the corresponding ``.../callback/{device}/<UID>/{callback_name_under}[/<SUFFIX>]`` topic for each registered suffix.

{desc}
""",
            'de': """
.. mqtt:function:: register/{device}/<UID>/{callback_name_under}\n\n{meta_table}\n

 Ein Callback für dieses Event kann durch Senden des Payloads "true" an das ``.../register/{device}/<UID>/{callback_name_under}[/<SUFFIX>]``-Topic hinzugefügt werden.
 Ein hinzugefügtes Callback kann durch Senden des Payloads "false" an das selbe Topic wieder entfernt werden.
 Um mehrere (De-)Registrierungen zu unterstützen, z.B. um Nachrichten filtern zu können, kann ein optionaler Suffix verwendet werden.

 Wenn das Callback ausgelöst wird, wird dessen Payload für jeden Suffix auf dem entsprechenden ``.../callback/{device}/<UID>/{callback_name_under}[/<SUFFIX>]``-Topic veröffentlicht.

{desc}
"""
        }

        cbs = ''
        device = self.get_mqtt_device_name()
        for packet in self.get_packets('callback'):

            meta = common.format_simple_element_meta([('register', 'bool', 1, 'in')],
                                                      parameter_title_override={'en': 'Register Request', 'de': 'Registrierungsanfrage'})
            meta += packet.get_formatted_element_meta(lambda element: element.get_mqtt_type(for_doc=True),
                                                      lambda element: element.get_name().under,
                                                      lambda constant_group: constant_group.get_name().upper,
                                                      callback_parameter_title_override={'en': 'Callback Response', 'de': 'Callback-Antwort'},
                                                      no_out_value={'en': 'empty payload', 'de': 'keine Nutzdaten'},
                                                      explicit_string_cardinality=True,
                                                      explicit_variable_stream_cardinality=True,
                                                      explicit_fixed_stream_cardinality=True,
                                                      explicit_common_cardinality=True,
                                                      include_constants=False,
                                                      high_level=True)
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_mqtt_formatted_doc()

            if packet.has_high_level():
                skip = -2
            else:
                skip = 0

            cbs += common.select_lang(cb).format(device=device,
                                                 callback_name_under=packet.get_mqtt_name(skip=skip),
                                                 meta_table=meta_table,
                                                 desc=desc)
        return cbs
    def get_mqtt_api(self):
        c_str = {
            'en': """
.. _{0}_mqtt_callbacks:

Callbacks
^^^^^^^^^

Callbacks can be registered to receive
time critical or recurring data from the device. The registration is done
with the corresponding ``.../register/...`` topic and an optional suffix.
This suffix can be used to deregister the callback later.

.. note::
 Using callbacks for recurring events is *always* preferred
 compared to using getters. It will use less USB bandwidth and the latency
 will be a lot better, since there is no round trip time.

{3}
""",
            'de': """
.. _{0}_mqtt_callbacks:

Callbacks
^^^^^^^^^

Callbacks können registriert werden um zeitkritische
oder wiederkehrende Daten vom Gerät zu erhalten. Die Registrierung kann
mit dem entsprechenden ``.../register/...``-Topic und einem optionalen Suffix durchgeführt werden.
Mit diesem Suffix kann das Callback später deregistriert werden.

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
.. _{0}_mqtt_api:

API
---

All published payloads to and from the MQTT bindings are in JSON format.

If an error occures, the bindings publish a JSON object containing the error message as member ``_ERROR``.
It is published on the corresponding response topic: ``.../response/...`` for ``.../request/...`` and ``.../callback/...`` for ``.../register/...``.
{1}

{2}
""",
            'de': """
.. _{0}_mqtt_api:

API
---

Alle veröffentlichten Payloads an die und von den MQTT-Bindings sind im JSON Format.

Falls ein Fehler auftritt, veröffentlichen die Bindings ein JSON-Objekt, das die Fehlermeldung als ``_ERROR``-Member enthält.
Das Objekt wird auf dem zugehörigen Antwort-Topic veröffentlicht: ``.../response/...`` für ``.../request/...`` und ``.../callback/...`` für ``.../register/...``.

{1}

{2}
"""
        }

        bf = self.get_mqtt_methods('bf')
        af = self.get_mqtt_methods('af')
        ccf = self.get_mqtt_methods('ccf')
        c = self.get_mqtt_callbacks()
        api_str = ''

        if bf:
            api_str += common.select_lang(common.bf_str).format("", bf)

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

        return common.select_lang(api).format(self.get_doc_rst_ref_name(),
                                              self.specialize_mqtt_doc_function_links(common.select_lang(self.get_doc())),
                                              api_str,
                                              device_name_display=self.get_long_display_name(),
                                              device_name_under = self.get_mqtt_device_name())

    def get_mqtt_doc(self):
        doc  = common.make_rst_header(self, False)
        doc += common.make_rst_summary(self)
        doc += self.get_mqtt_examples()
        doc += self.get_mqtt_api()

        return doc

class MQTTDocPacket(mqtt_common.MQTTPacket):
    def get_mqtt_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())
        text = self.get_device().specialize_mqtt_doc_function_links(text)

        constants = {'en': 'symbols', 'de': 'Symbole'}

        callback_parameter = {'en': 'callback payload', 'de': 'Payload des Callbacks'}
        callback_parameters = {'en': 'callback payload members', 'de': 'Payload-Member des Callbacks'}

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)

        if self.get_type() == 'callback':
            text = common.handle_rst_word(text, parameter=callback_parameter, parameters=callback_parameters, constants=constants)
        else:
            text = common.handle_rst_word(text, constants=constants)

        text = common.handle_rst_substitutions(text, self)

        def element_format(element):
            return common.select_lang({'en': '\nFor **{0}** field:\n\n', 'de': '\nFür **{0}** Feld:\n\n'}).format(element.get_name().under)

        def constant_format(prefix, constant_group, constant, value):
            return '* "{0}" = {1}\n'.format(constant.get_name().camel, value)

        text += common.format_constants('', self,
                                        constants_name=constants,
                                        element_format_func=element_format,
                                        constant_format_func=constant_format)

        text += common.format_since_firmware(self.get_device(), self)
        text = text.replace('|device_identifier_constant|\n', '')

        return common.shift_right(text, 1)

class MQTTDocGenerator(mqtt_common.MQTTGeneratorTrait, common.DocGenerator):
    def get_bindings_name(self):
        return 'mqtt'

    def get_bindings_display_name(self):
        return 'MQTT'

    def get_doc_rst_filename_part(self):
        return 'MQTT'

    def get_doc_example_regex(self):
        return r'^example-.*\.txt$'

    def get_device_class(self):
        return MQTTDocDevice

    def get_packet_class(self):
        return MQTTDocPacket

    def get_element_class(self):
        return mqtt_common.MQTTElement

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_mqtt_doc())

def generate(root_dir, language):
    common.generate(root_dir, language, MQTTDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print('=== Generating %s ===' % language)
        generate(os.getcwd(), language)
