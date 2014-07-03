#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C# Bindings Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2012 Olaf Lüke <olaf@tinkerforge.com>

generate_csharp_bindings.py: Generator for C# bindings

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
from xml.sax.saxutils import escape

sys.path.append(os.path.split(os.getcwd())[0])
import common
import csharp_common

class CSharpBindingsDevice(csharp_common.CSharpDevice):
    def get_csharp_import(self):
        include = """{0}
using System;

namespace Tinkerforge
{{"""
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        version = common.get_changelog_version(self.get_generator().get_bindings_root_directory())

        return include.format(common.gen_text_star.format(date, *version))

    def get_csharp_class(self):
        class_str = """
\t/// <summary>
\t///  {1}
\t/// </summary>
\tpublic class {0} : Device
\t{{
\t\t/// <summary>
\t\t///  Used to identify this device type in
\t\t///  <see cref="Tinkerforge.IPConnection.EnumerateCallback"/>
\t\t/// </summary>
\t\tpublic static int DEVICE_IDENTIFIER = {2};
"""

        return class_str.format(self.get_csharp_class_name(),
                                self.get_description(),
                                self.get_device_identifier())

    def get_csharp_delegates(self):
        cbs = '\n'
        cb = """
\t\t/// <summary>
\t\t///  {2}
\t\t/// </summary>
\t\tpublic event {0}EventHandler {0};
\t\t/// <summary>
\t\t/// </summary>
\t\tpublic delegate void {0}EventHandler({3} sender{1});
"""
        for packet in self.get_packets('callback'):
            name = packet.get_camel_case_name()
            parameter = packet.get_csharp_parameter_list()
            doc = packet.get_csharp_formatted_doc()
            if parameter != '':
                parameter = ', ' + parameter
            cbs += cb.format(name, parameter, doc, self.get_csharp_class_name())

        return cbs

    def get_csharp_function_id_definitions(self):
        function_ids = ''
        function_id = """
\t\t/// <summary>
\t\t///  Function ID to be used with
\t\t///  <see cref="Tinkerforge.Device.GetResponseExpected"/>,
\t\t///  <see cref="Tinkerforge.Device.SetResponseExpected"/> and
\t\t///  <see cref="Tinkerforge.Device.SetResponseExpectedAll"/>.
\t\t/// </summary>
\t\tpublic const byte {2}_{0} = {1};
"""
        for packet in self.get_packets():
            function_ids += function_id.format(packet.get_upper_case_name(),
                                               packet.get_function_id(),
                                               packet.get_type().upper())
        return function_ids

    def get_csharp_constants(self):
        constant = """
\t\t/// <summary>
\t\t/// </summary>
\t\tpublic const {0} {1}_{2} = {3};
"""
        constants = []
        for constant_group in self.get_constant_groups():
            for constant_item in constant_group.get_items():
                if constant_group.get_type() == 'char':
                    value = "'{0}'".format(constant_item.get_value())
                else:
                    value = str(constant_item.get_value())

                constants.append(constant.format(csharp_common.get_csharp_type(constant_group.get_type(), 1),
                                                 constant_group.get_upper_case_name(),
                                                 constant_item.get_upper_case_name(),
                                                 value))
        return '\n' + ''.join(constants)

    def get_csharp_constructor(self):
        cbs = []
        cb = '\t\t\tcallbackWrappers[CALLBACK_{0}] = new CallbackWrapper(On{1});'
        con = """
\t\t/// <summary>
\t\t///  Creates an object with the unique device ID <c>uid</c> and adds  it to
\t\t///  the IPConnection <c>ipcon</c>.
\t\t/// </summary>
\t\tpublic {0}(string uid, IPConnection ipcon) : base(uid, ipcon)
\t\t{{
\t\t\tthis.apiVersion[0] = {2};
\t\t\tthis.apiVersion[1] = {3};
\t\t\tthis.apiVersion[2] = {4};
{1}
"""

        for packet in self.get_packets('callback'):
            name_upper = packet.get_upper_case_name()
            name_pascal = packet.get_camel_case_name()
            cbs.append(cb.format(name_upper, name_pascal))

        return con.format(self.get_csharp_class_name(), '\n'.join(cbs),
                          *self.get_api_version())

    def get_csharp_response_expected(self):
        res = '\n'
        re = "\t\t\tresponseExpected[{0}] = {1}\n"

        for packet in self.get_packets('function'):
            name_upper = 'FUNCTION_' + packet.get_upper_case_name()
            setto = 'ResponseExpectedFlag.FALSE;'
            if len(packet.get_elements('out')) > 0:
                setto = 'ResponseExpectedFlag.ALWAYS_TRUE;'
            elif packet.get_doc()[0] == 'ccf':
                setto = 'ResponseExpectedFlag.TRUE;'

            res += re.format(name_upper, setto)

        for packet in self.get_packets('callback'):
            name_upper = 'CALLBACK_' + packet.get_upper_case_name()
            setto = 'ResponseExpectedFlag.ALWAYS_FALSE;'
            res += re.format(name_upper, setto)

        return res + '\t\t}\n'

    def get_csharp_callbacks(self):
        cbs = ''
        cb = """
\t\t/// <summary>
\t\t/// </summary>
\t\tprotected void On{0}(byte[] response)
\t\t{{
{1}\t\t\tvar handler = {0};
\t\t\tif(handler != null)
\t\t\t{{
\t\t\t\thandler(this{3});
\t\t\t}}
\t\t}}
"""

        for packet in self.get_packets('callback'):
            name = packet.get_camel_case_name()
            name_upper = packet.get_upper_case_name()
            eles = []
            for element in packet.get_elements('out'):
                eles.append(element.get_headless_camel_case_name())
            callParams = ", ".join(eles)
            signatureParams = packet.get_csharp_parameter_list()
            size = str(packet.get_request_size())

            convs = ''
            conv = '\t\t\t{0} {1} = LEConverter.{2}({3}, response{4});\n'

            pos = 8
            for element in packet.get_elements('out'):
                csharp_type = element.get_csharp_type()
                cname = element.get_headless_camel_case_name()
                from_method = element.get_csharp_le_converter_from_method()
                length = ''
                if element.get_cardinality() > 1:
                    length = ', ' + str(element.get_cardinality())
                convs += conv.format(csharp_type,
                                     cname,
                                     from_method,
                                     pos,
                                     length)

                pos += element.get_size()

            if convs != '':
                convs += '\n'

            if callParams != '':
                callParams = ', ' + callParams

            cbs += cb.format(name, convs, name_upper, callParams, pos, signatureParams)

        return cbs + "\t}\n}"

    def get_csharp_methods(self):
        methods = ''
        method = """
\t\t/// <summary>
\t\t///  {5}
\t\t/// </summary>
\t\t{0}
\t\t{{
\t\t\tbyte[] request = CreateRequestPacket({1}, FUNCTION_{2});
{3}
{4}
\t\t}}
"""

        method_noresponse = """\t\t\tSendRequest(request);
"""

        method_response = """\t\t\tbyte[] response = SendRequest(request);
{0}"""

        for packet in self.get_packets('function'):
            ret_count = len(packet.get_elements('out'))
            size = str(packet.get_request_size())
            name_upper = packet.get_upper_case_name()
            doc = packet.get_csharp_formatted_doc()

            write_convs = ''
            write_conv = '\t\t\tLEConverter.To(({2}){0}, {1}, request);\n'
            write_conv_length = '\t\t\tLEConverter.To(({3}){0}, {1}, {2}, request);\n'

            pos = 8
            for element in packet.get_elements('in'):
                wname = element.get_headless_camel_case_name()
                csharp_type = element.get_csharp_le_converter_type()
                if element.get_cardinality() > 1:
                    write_convs += write_conv_length.format(wname, pos, element.get_cardinality(), csharp_type)
                else:
                    write_convs += write_conv.format(wname, pos, csharp_type)
                pos += element.get_size()

            method_tail = ''
            read_convs = ''
            read_conv = '\n\t\t\t{0} = LEConverter.{1}({2}, response{3});'

            pos = 8
            for element in packet.get_elements('out'):
                aname = element.get_headless_camel_case_name()
                from_method = element.get_csharp_le_converter_from_method()
                length = ''
                if element.get_cardinality() > 1:
                    length = ', ' + str(element.get_cardinality())

                if ret_count == 1:
                    read_convs = '\n\t\t\treturn LEConverter.{0}({1}, response{2});'.format(from_method, pos, length)
                else:
                    read_convs += read_conv.format(aname, from_method, pos, length)
                pos += element.get_size()

            if ret_count > 0:
                method_tail = method_response.format(read_convs)
            else:
                method_tail = method_noresponse

            signature = packet.get_csharp_method_signature()
            methods += method.format(signature,
                                     size,
                                     name_upper,
                                     write_convs,
                                     method_tail,
                                     doc)

        return methods

    def get_csharp_source(self):
        source  = self.get_csharp_import()
        source += self.get_csharp_class()
        source += self.get_csharp_function_id_definitions()
        source += self.get_csharp_constants()
        source += self.get_csharp_delegates()
        source += self.get_csharp_constructor()
        source += self.get_csharp_response_expected()
        source += self.get_csharp_methods()
        source += self.get_csharp_callbacks()

        return source

class CSharpBindingsPacket(csharp_common.CSharpPacket):
    def get_csharp_formatted_doc(self):
        text = common.select_lang(self.get_doc()[1])
        link = '<see cref="Tinkerforge.{0}.{1}"/>'

        # escape XML special chars
        text = escape(text)

        # handle notes and warnings
        lines = text.split('\n')
        replaced_lines = []
        in_note = False
        in_warning = False
        in_table_head = False
        in_table_body = False

        for line in lines:
            if line.strip() == '.. note::':
                in_note = True
                replaced_lines.append('<note>')
            elif line.strip() == '.. warning::':
                in_warning = True
                replaced_lines.append('<note type="caution">')
            elif len(line.strip()) == 0 and (in_note or in_warning):
                if in_note:
                    in_note = False
                if in_warning:
                    in_warning = False

                replaced_lines.append('</note>')
                replaced_lines.append('')
            elif line.strip() == '.. csv-table::':
                in_table_head = True
                replaced_lines.append('<code>')
            elif line.strip().startswith(':header: ') and in_table_head:
                replaced_lines.append(line[len(':header: '):])
            elif line.strip().startswith(':widths:') and in_table_head:
                pass
            elif len(line.strip()) == 0 and in_table_head:
                in_table_head = False
                in_table_body = True

                replaced_lines.append('')
            elif len(line.strip()) == 0 and in_table_body:
                in_table_body = False

                replaced_lines.append('</code>')
                replaced_lines.append('')
            else:
                replaced_lines.append(line)

        text = '\n'.join(replaced_lines)

        cls = self.get_device().get_csharp_class_name()
        for other_packet in self.get_device().get_packets():
            name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
            name = other_packet.get_camel_case_name()
            name_right = link.format(cls, name)
            text = text.replace(name_false, name_right)

        def format_parameter(name):
            return name # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return '\n\t\t///  '.join(text.strip().split('\n'))

class CSharpBindingsGenerator(common.BindingsGenerator):
    released_files_name_prefix = 'csharp'

    def get_bindings_name(self):
        return 'csharp'

    def get_device_class(self):
        return CSharpBindingsDevice

    def get_packet_class(self):
        return CSharpBindingsPacket

    def get_element_class(self):
        return csharp_common.CSharpElement

    def generate(self, device):
        filename = '{0}.cs'.format(device.get_csharp_class_name())

        cs = open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename), 'wb')
        cs.write(device.get_csharp_source())
        cs.close()

        if device.is_released():
            self.released_files.append(filename)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', CSharpBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
