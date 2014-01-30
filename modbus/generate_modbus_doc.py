#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modbus Documentation Generator
Copyright (C) 2012-2013 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2012-2014 Matthias Bolte <matthias@tinkerforge.com>

generator_modbus_doc.py: Generator for Modbus documentation

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

sys.path.append(os.path.split(os.getcwd())[0])
import common

class ModbusDocDevice(common.Device):
    def get_modbus_name(self):
        return self.get_category() + self.get_camel_case_name()

    def get_modbus_methods(self, typ):
        methods = ''
        func_start = '.. modbus:function:: '
        cls = self.get_modbus_name()

        for packet in self.get_packets('function'):
            if packet.get_doc()[0] != typ or packet.get_function_id() < 0:
                continue

            name = packet.get_underscore_name()
            fid = '\n :functionid: {0}'.format(packet.get_function_id())
            request = packet.get_modbus_request_desc()
            response = packet.get_modbus_response_desc()
            d = packet.get_modbus_formatted_doc()
            desc = '{0}{1}{2}{3}'.format(fid, request, response, d)
            func = '{0}{1}.{2}\n{3}'.format(func_start, cls, name, desc)
            methods += func + '\n'

        return methods

    def get_modbus_callbacks(self):
        cbs = ''
        func_start = '.. modbus:function:: '
        cls = self.get_modbus_name()
        for packet in self.get_packets('callback'):
            fid = '\n :functionid: {0}'.format(packet.get_function_id())
            response = packet.get_modbus_response_desc()
            desc = packet.get_modbus_formatted_doc()

            func = '{0}{1}.CALLBACK_{2}\n{3}\n{4}\n{5}'.format(func_start,
                                                               cls,
                                                               packet.get_upper_case_name(),
                                                               fid,
                                                               response,
                                                               desc)
            cbs += func + '\n'

        return cbs

    def get_modbus_api(self):
        c_str = {
        'en': """
.. _{1}_{2}_modbus_callbacks:

Callbacks
^^^^^^^^^

{0}
""",
        'de': """
.. _{1}_{2}_modbus_callbacks:

Callbacks
^^^^^^^^^

{0}
"""
        }

        api = {
        'en': """
{0}

API
---

A general description of the Modbus protocol structure can be found
:ref:`here <llproto_modbus>`.

{1}

{2}
""",
        'de': """
{0}

API
---

Eine allgemeine Beschreibung der Modbus Protokollstruktur findet sich
:ref:`hier <llproto_modbus>`.

{1}

{2}
"""
        }

        const_str = {
        'en' : """
Constants
^^^^^^^^^

.. modbus:attribute:: {0}.DEVICE_IDENTIFIER

 :value: {3}

 This constant is used to identify a {0} {1}.

 The :modbus:func:`get_identity <{0}.get_identity>` function and the
 :modbus:func:`CALLBACK_ENUMERATE <CALLBACK_ENUMERATE>`
 callback of the IP Connection have a ``device_identifier`` parameter to specify
 the Brick's or Bricklet's type.
""",
        'de' : """
Konstanten
^^^^^^^^^^

.. modbus:attribute:: {0}.DEVICE_IDENTIFIER

 :value: {3}

 Diese Konstante wird verwendet um {2} {0} {1} zu identifizieren.

 Die :modbus:func:`get_identity <{0}.get_identity>` Funktion und der
 :modbus:func:`CALLBACK_ENUMERATE <CALLBACK_ENUMERATE>`
 Callback der IP Connection haben ein ``device_identifier`` Parameter um den Typ
 des Bricks oder Bricklets anzugeben.
"""
        }

        bf = self.get_modbus_methods('bf')
        af = self.get_modbus_methods('af')
        ccf = self.get_modbus_methods('ccf')
        c = self.get_modbus_callbacks()
        api_str = ''
        if bf:
            api_str += common.select_lang(common.bf_str).format(bf, '')
        if af:
            api_str += common.select_lang(common.af_str).format(af)
        if ccf:
            api_str += common.select_lang(common.ccf_str).format(ccf, '')
        if c:
            api_str += common.select_lang(c_str).format(c, self.get_underscore_name(),
                                                        self.get_category().lower())

        article = 'ein'
        if self.get_category() == 'Brick':
            article = 'einen'
        api_str += common.select_lang(const_str).format(self.get_camel_case_name(),
                                                        self.get_category(),
                                                        article,
                                                        self.get_device_identifier())

        ref = '.. _{0}_{1}_modbus_api:\n'.format(self.get_underscore_name(),
                                                 self.get_category().lower())

        return common.select_lang(api).format(ref, self.get_api_doc(), api_str)

    def get_modbus_doc(self):
        title = { 'en': 'Modbus protocol', 'de': 'Modbus Protokoll' }

        doc  = common.make_rst_header(self, 'modbus', 'Modbus')
        doc += common.make_rst_summary(self, common.select_lang(title), None)
        doc += self.get_modbus_api()

        return doc

class ModbusDocPacket(common.Packet):
    def get_modbus_formatted_doc(self):
        text = common.select_lang(self.get_doc()[1])
        parameter = {
        'en': 'response value',
        'de': 'Rückgabewert'
        }
        parameters = {
        'en': 'response values',
        'de': 'Rückgabewerte'
        }

        cls = self.get_device().get_modbus_name()
        for other_packet in self.get_device().get_packets():
            name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
            if other_packet.get_type() == 'callback':
                name_upper = other_packet.get_upper_case_name()
                name_right = ':modbus:func:`CALLBACK_{1} <{0}.CALLBACK_{1}>`'.format(cls, name_upper)
            else:
                name_right = ':modbus:func:`{1} <{0}.{1}>`'.format(cls, other_packet.get_underscore_name())
            text = text.replace(name_false, name_right)

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text, parameter, parameters)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, 1)

    def get_modbus_request_desc(self):
        empty_payload = {
        'en': 'empty payload',
        'de': 'keine Nutzdaten'
        }
        desc = '\n'
        param = ' :request {0}: {1}\n'
        for element in self.get_elements('in'):
            desc += param.format(element.get_underscore_name(), element.get_modbus_type())

        if desc == '\n':
            desc += ' :emptyrequest: {0}\n'.format(common.select_lang(empty_payload))

        return desc

    def get_modbus_response_desc(self):
        empty_payload = {
        'en': 'empty payload',
        'de': 'keine Nutzdaten'
        }
        no_response = {
        'en': 'no response',
        'de': 'keine Antwort'
        }
        desc = '\n'
        returns = ' :response {0}: {1}\n'
        for element in self.get_elements('out'):
            desc += returns.format(element.get_underscore_name(), element.get_modbus_type())

        if desc == '\n':
            if self.get_type() == 'callback':
                desc += ' :emptyresponse: {0}\n'.format(common.select_lang(empty_payload))
            else:
                desc += ' :noresponse: {0}\n'.format(common.select_lang(no_response))

        return desc

class ModbusDocElement(common.Element):
    def get_modbus_type(self):
        t = self.get_type()

        if t == 'string':
            t = 'char'

        if self.get_cardinality() == 1:
            return t

        return t + '[' + str(self.get_cardinality()) + ']'

class ModbusDocGenerator(common.DocGenerator):
    def get_bindings_name(self):
        return 'modbus'

    def get_device_class(self):
        return ModbusDocDevice

    def get_packet_class(self):
        return ModbusDocPacket

    def get_element_class(self):
        return ModbusDocElement

    def generate(self, device):
        file_name = '{0}_{1}_Modbus.rst'.format(device.get_camel_case_name(), device.get_category())

        rst = open(os.path.join(self.get_bindings_root_directory(), 'doc', common.lang, file_name), 'wb')
        rst.write(device.get_modbus_doc())
        rst.close()

def generate(bindings_root_directory, language):
    common.generate(bindings_root_directory, language, ModbusDocGenerator)

if __name__ == "__main__":
    for language in ['en', 'de']:
        print("=== Generating %s ===" % language)
        generate(os.getcwd(), language)
