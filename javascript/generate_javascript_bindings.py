#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JavaScript Bindings Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_javascript.py: Generator for JavaScript bindings

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

import datetime
import sys
import os

sys.path.append(os.path.split(os.getcwd())[0])
import common
import javascript_common

class JavaScriptBindingsDevice(javascript_common.JavaScriptDevice):
    def get_javascript_require(self):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        version = common.get_changelog_version(self.get_generator().get_bindings_root_directory())
        return """{0}
var Device = require('./Device');\n
{1}.DEVICE_IDENTIFIER = {2};\n""".format(common.gen_text_star.format(date, *version),
                                         self.get_javascript_class_name(),
                                         self.get_device_identifier())
    
    def get_javascript_constants(self):
        callback_constants = ''
        callback_constant_statement = self.get_javascript_class_name()+'.CALLBACK_{0} = {1};\n'
        for packet in self.get_packets('callback'):
            callback_constants += callback_constant_statement.format(packet.get_upper_case_name(),
                                                                     packet.get_function_id())
        function_constants = ''
        function_constant_statement = self.get_javascript_class_name()+'.FUNCTION_{0} = {1}\n'
        for packet in self.get_packets('function'):
            function_constants += function_constant_statement.format(packet.get_upper_case_name(),
                                                                     packet.get_function_id())
        constant_statement = self.get_javascript_class_name()+\
        '.{constant_group_upper_case_name}_{constant_item_upper_case_name} = {constant_item_value};\n'
        constants = self.get_formatted_constants(constant_statement) + '\n'
        return callback_constants+function_constants+constants

    def get_javascript_class_opening(self):
        return """function {0}(uid, ipcon) {{
    //{1}
    
    /*
    Creates an object with the unique device ID *uid* and adds it to
    the IP Connection *ipcon*.
    */
    Device.call(this, this, uid, ipcon);
    {2}.prototype = Object.create(Device);
    this.APIVersion = [{3}, {4}, {5}];\n""".format(self.get_javascript_class_name(),self.get_description(),
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
            elif packet.get_doc()[0] == 'ccf':
                prefix = 'FUNCTION_'
                flag = 'RESPONSE_EXPECTED_TRUE'
            else:
                prefix = 'FUNCTION_'
                flag = 'RESPONSE_EXPECTED_FALSE'

            response_expected += '    this.responseExpected[{0}.{1}{2}] = Device.{3};\n' \
                .format(self.get_javascript_class_name(), prefix, packet.get_upper_case_name(), flag)

        return response_expected

    def get_javascript_callback_formats(self):
        callback_format = ''
        callback_format_statement = "    this.callbackFormats[{0}.CALLBACK_{1}] = '{2}';\n"

        for index, packet in enumerate(self.get_packets('callback')):
            if(index == len(self.get_packets('callback')) - 1):
                callback_format += "    this.callbackFormats[{0}.CALLBACK_{1}] = '{2}';\n\n"\
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
            camel_case_name = packet.get_camel_case_name()
            camel_case_name_js_mod = camel_case_name[0].lower()+camel_case_name[1:]
            under_score_name = packet.get_underscore_name()
            param_list = packet.get_javascript_parameter_list()
            pack_format = packet.get_javascript_format_list('in')
            unpack_format = packet.get_javascript_format_list('out')
            doc = packet.get_javascript_formatted_doc()
            
            no_param_method_code = """    this.{0} = function(returnCallback, errorCallback) {{
        /*
        {1}
        */
        this.ipcon.sendRequest(this, {2}.FUNCTION_{3}, [{4}], '{5}', '{6}', returnCallback, errorCallback);
    }};   
"""
            param_method_code = """    this.{0} = function({1}, returnCallback, errorCallback) {{
        /*
        {2}
        */
        this.ipcon.sendRequest(this, {3}.FUNCTION_{4}, [{5}], '{6}', '{7}', returnCallback, errorCallback);
    }};
"""            
            if(len(param_list) == 0):
                method_code += no_param_method_code.format(camel_case_name_js_mod, doc, self.get_javascript_class_name(), under_score_name.upper(), param_list, pack_format, unpack_format)
            if(len(param_list) > 0):
                method_code += param_method_code.format(camel_case_name_js_mod, param_list, doc, self.get_javascript_class_name(), under_score_name.upper(), param_list, pack_format, unpack_format)

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
        text = common.select_lang(self.get_doc()[1])

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return '\n        '.join(text.strip().split('\n'))

    def get_javascript_format_list(self, io):
        forms = []

        for element in self.get_elements(io):
            forms.append(element.get_javascript_struct_format())

        return ' '.join(forms)

class JavaScriptBindingsGenerator(common.BindingsGenerator):
    released_files_name_prefix = 'javascript'
    browser_api_file = None

    def prepare(self):
        ret = common.BindingsGenerator.prepare(self)

        browser_api_filename = os.path.join(self.get_bindings_root_directory(), 'bindings', 'BrowserAPI.js')
        self.browser_api_file = open(browser_api_filename, 'wb')
        self.released_files.append(browser_api_filename)

        self.browser_api_file.write("""function Tinkerforge() {
    this.IPConnection = require('./IPConnection');
""")

        return ret

    def finish(self):
        self.browser_api_file.write("""}

global.window.Tinkerforge = new Tinkerforge();""")
        self.browser_api_file.close()
        return common.BindingsGenerator.finish(self)

    def add_browser_api_function(self, device):
        if device.is_released():
            api = """    this.{0}{1} = require('./{0}{1}');
"""
            api_format = api.format(device.get_category(), device.get_camel_case_name())
            self.browser_api_file.write(api_format)

    def get_bindings_name(self):
        return 'javascript'

    def get_device_class(self):
        return JavaScriptBindingsDevice

    def get_packet_class(self):
        return JavaScriptBindingsPacket

    def get_element_class(self):
        return javascript_common.JavaScriptElement

    def generate(self, device):
        self.add_browser_api_function(device)

        file_name = '{0}{1}.js'.format(device.get_category(), device.get_camel_case_name())

        py = open(os.path.join(self.get_bindings_root_directory(), 'bindings', file_name), 'wb')
        py.write(device.get_javascript_source())
        py.close()

        if device.is_released():
            self.released_files.append(file_name)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', JavaScriptBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
