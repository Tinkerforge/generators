#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JavaScript Bindings Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2014-2015 Matthias Bolte <matthias@tinkerforge.com>

generate_javascript_bindings.py: Generator for JavaScript bindings

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
import javascript_common

class JavaScriptBindingsDevice(javascript_common.JavaScriptDevice):
    def get_javascript_require(self):
        require = """{0}
var Device = require('./Device');

{1}.DEVICE_IDENTIFIER = {2};
{1}.DEVICE_DISPLAY_NAME = '{3}';
"""

        return require.format(self.get_generator().get_header_comment('asterisk'),
                              self.get_javascript_class_name(),
                              self.get_device_identifier(),
                              self.get_long_display_name())

    def get_javascript_constants(self):
        callback_constants = ''
        callback_constant_statement = self.get_javascript_class_name()+'.CALLBACK_{0} = {1};\n'
        for packet in self.get_packets('callback'):
            callback_constants += callback_constant_statement.format(packet.get_upper_case_name(),
                                                                     packet.get_function_id())
        function_constants = ''
        function_constant_statement = self.get_javascript_class_name()+'.FUNCTION_{0} = {1};\n'
        for packet in self.get_packets('function'):
            function_constants += function_constant_statement.format(packet.get_upper_case_name(),
                                                                     packet.get_function_id())
        constant_statement = self.get_javascript_class_name()+\
        '.{constant_group_upper_case_name}_{constant_upper_case_name} = {constant_value};\n'
        constants = self.get_formatted_constants(constant_statement) + '\n'
        return callback_constants+function_constants+constants

    def get_javascript_class_opening(self):
        return """function {0}(uid, ipcon) {{
\t//{1}

\t/*
\tCreates an object with the unique device ID *uid* and adds it to
\tthe IP Connection *ipcon*.
\t*/
\tDevice.call(this, this, uid, ipcon);
\t{2}.prototype = Object.create(Device);
\tthis.responseExpected = {{}};
\tthis.callbackFormats = {{}};
\tthis.APIVersion = [{3}, {4}, {5}];\n""".format(self.get_javascript_class_name(),self.get_description(),
                                                 self.get_javascript_class_name(), *self.get_api_version())

    def get_javascript_response_expecteds(self):
        response_expected = ''

        for packet in self.get_packets():
            if packet.get_type() == 'callback':
                prefix = 'CALLBACK_'
                flag = 'RESPONSE_EXPECTED_ALWAYS_FALSE'
            elif len(packet.get_elements('out')) > 0:
                prefix = 'FUNCTION_'
                flag = 'RESPONSE_EXPECTED_ALWAYS_TRUE'
            elif packet.get_doc_type() == 'ccf':
                prefix = 'FUNCTION_'
                flag = 'RESPONSE_EXPECTED_TRUE'
            else:
                prefix = 'FUNCTION_'
                flag = 'RESPONSE_EXPECTED_FALSE'

            response_expected += '\tthis.responseExpected[{0}.{1}{2}] = Device.{3};\n' \
                .format(self.get_javascript_class_name(), prefix, packet.get_upper_case_name(), flag)

        return response_expected

    def get_javascript_callback_formats(self):
        callback_format = ''
        callback_format_statement = "\tthis.callbackFormats[{0}.CALLBACK_{1}] = '{2}';\n"

        for index, packet in enumerate(self.get_packets('callback')):
            if(index == len(self.get_packets('callback')) - 1):
                callback_format += "\tthis.callbackFormats[{0}.CALLBACK_{1}] = '{2}';\n\n"\
                                                                .format(self.get_javascript_class_name(),
                                                                        packet.get_upper_case_name(),
                                                                        packet.get_javascript_format_list('out'))
                continue;
            callback_format += callback_format_statement.format(self.get_javascript_class_name(),
                                                                packet.get_upper_case_name(),
                                                                packet.get_javascript_format_list('out'))

        return callback_format

    def get_javascript_methods(self):
        method_code = ''
        for packet in self.get_packets('function'):
            name = packet.get_headless_camel_case_name()
            underscore_name = packet.get_underscore_name()
            param_list = packet.get_javascript_parameter_list()
            pack_format = packet.get_javascript_format_list('in')
            unpack_format = packet.get_javascript_format_list('out')
            doc = packet.get_javascript_formatted_doc()

            no_param_method_code = """\tthis.{0} = function(returnCallback, errorCallback) {{
\t\t/*
\t\t{1}
\t\t*/
\t\tthis.ipcon.sendRequest(this, {2}.FUNCTION_{3}, [{4}], '{5}', '{6}', returnCallback, errorCallback);
\t}};
"""
            param_method_code = """\tthis.{0} = function({1}, returnCallback, errorCallback) {{
\t\t/*
\t\t{2}
\t\t*/
\t\tthis.ipcon.sendRequest(this, {3}.FUNCTION_{4}, [{5}], '{6}', '{7}', returnCallback, errorCallback);
\t}};
"""
            if(len(param_list) == 0):
                method_code += no_param_method_code.format(name, doc, self.get_javascript_class_name(), underscore_name.upper(), param_list, pack_format, unpack_format)
            if(len(param_list) > 0):
                method_code += param_method_code.format(name, param_list, doc, self.get_javascript_class_name(), underscore_name.upper(), param_list, pack_format, unpack_format)

        return method_code

    def get_javascript_class_closing(self):
        return """}}

module.exports = {0};
""".format(self.get_javascript_class_name())

    def get_javascript_source(self):
        source = self.get_javascript_require()
        source += self.get_javascript_constants()
        source += self.get_javascript_class_opening()
        source += self.get_javascript_response_expecteds()
        source += self.get_javascript_callback_formats()
        source += self.get_javascript_methods()
        source += self.get_javascript_class_closing()
        return source

class JavaScriptBindingsPacket(javascript_common.JavaScriptPacket):
    def get_javascript_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return '\n\t\t'.join(text.strip().split('\n'))

    def get_javascript_format_list(self, io):
        forms = []

        for element in self.get_elements(io):
            forms.append(element.get_javascript_struct_format())

        return ' '.join(forms)

class JavaScriptBindingsGenerator(common.BindingsGenerator):
    def get_bindings_name(self):
        return 'javascript'

    def get_bindings_display_name(self):
        return 'JavaScript'

    def get_device_class(self):
        return JavaScriptBindingsDevice

    def get_packet_class(self):
        return JavaScriptBindingsPacket

    def get_element_class(self):
        return javascript_common.JavaScriptElement

    def prepare(self):
        ret = common.BindingsGenerator.prepare(self)

        browser_api_filename = os.path.join(self.get_bindings_root_directory(), 'bindings', 'BrowserAPI.js')
        npm_main_filename = os.path.join(self.get_bindings_root_directory(), 'bindings', 'TinkerforgeNPM.js')
        source_main_filename = os.path.join(self.get_bindings_root_directory(), 'bindings', 'TinkerforgeSource.js')

        self.browser_api_file = open(browser_api_filename, 'wb')
        self.npm_main_file = open(npm_main_filename, 'wb')
        self.source_main_file = open(source_main_filename, 'wb')

        self.released_files.append('BrowserAPI.js')
        self.released_files.append('TinkerforgeNPM.js')
        self.released_files.append('TinkerforgeSource.js')

        self.browser_api_file.write("""function Tinkerforge() {
\tthis.IPConnection = require('./IPConnection');
""")

        self.npm_main_file.write("""function Tinkerforge() {
\tthis.IPConnection = require('./lib/IPConnection');
""")

        self.source_main_file.write("""function Tinkerforge() {
\tthis.IPConnection = require('./Tinkerforge/IPConnection');
""")

        return ret

    def add_browser_api_function(self, device):
        if device.is_released():
            api = """\tthis.{0}{1} = require('./{0}{1}');
"""
            api_format = api.format(device.get_camel_case_category(), device.get_camel_case_name())
            self.browser_api_file.write(api_format)

    def add_npm_main_function(self, device):
        if device.is_released():
            npm_main = """\tthis.{0}{1} = require('./lib/{0}{1}');
"""
            npm_main_format = npm_main.format(device.get_camel_case_category(), device.get_camel_case_name())
            self.npm_main_file.write(npm_main_format)

    def add_source_main_function(self, device):
        if device.is_released():
            source_main = """\tthis.{0}{1} = require('./Tinkerforge/{0}{1}');
"""
            source_main_format = source_main.format(device.get_camel_case_category(), device.get_camel_case_name())
            self.source_main_file.write(source_main_format)

    def generate(self, device):
        self.add_browser_api_function(device)
        self.add_npm_main_function(device)
        self.add_source_main_function(device)

        filename = '{0}{1}.js'.format(device.get_camel_case_category(), device.get_camel_case_name())

        js = open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename), 'wb')
        js.write(device.get_javascript_source())
        js.close()

        if device.is_released():
            self.released_files.append(filename)

    def finish(self):
        self.browser_api_file.write("""}

global.Tinkerforge = new Tinkerforge();""")
        self.browser_api_file.close()

        self.npm_main_file.write("""}

module.exports = new Tinkerforge();""")
        self.npm_main_file.close()

        self.source_main_file.write("""}

module.exports = new Tinkerforge();""")
        self.source_main_file.close()

        return common.BindingsGenerator.finish(self)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', JavaScriptBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
