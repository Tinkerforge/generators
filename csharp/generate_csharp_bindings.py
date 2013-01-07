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
import csharp_common
from xml.sax.saxutils import escape

sys.path.append(os.path.split(os.getcwd())[0])
import common

device = None

def format_doc(packet):
    text = common.select_lang(packet.get_doc()[1])
    link = '<see cref="Tinkerforge.{0}{1}.{2}"/>'

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

    cls = device.get_camel_case_name()
    for other_packet in device.get_packets():
        name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
        name = other_packet.get_camel_case_name()
        name_right = link.format(device.get_category(), cls, name)

        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", "parameter")
    text = text.replace(":word:`parameters`", "parameters")

    text = common.handle_rst_if(text, device)
    text = common.handle_since_firmware(text, device, packet)

    return '\n\t\t///  '.join(text.strip().split('\n'))

def make_import():
    include = """{0}
using System;

namespace Tinkerforge
{{"""
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    return include.format(common.gen_text_star.format(date))

def make_class():
    class_str = """
\t/// <summary>
\t///  {2}
\t/// </summary>
\tpublic class {0}{1} : Device 
\t{{
"""
        
    return class_str.format(device.get_category(),
                            device.get_camel_case_name(),
                            device.get_description())

def make_delegates():
    cbs = '\n'
    cb = """
\t\t/// <summary>
\t\t///  {2}
\t\t/// </summary>
\t\tpublic event {0}EventHandler {0};
\t\tpublic delegate void {0}EventHandler(object sender{1});
"""
    for packet in device.get_packets('callback'):
        name = packet.get_camel_case_name()
        parameter = csharp_common.make_parameter_list(packet)
        doc = format_doc(packet)
        if parameter != '':
            parameter = ', ' + parameter
        cbs += cb.format(name, parameter, doc)
    return cbs

def make_function_id_definitions():
    function_ids = ''
    function_id = """
\t\t/// <summary>
\t\t///  Function ID to be used with
\t\t///  <see cref="Tinkerforge.{3}{4}.GetResponseExpected"/>,
\t\t///  <see cref="Tinkerforge.{3}{4}.SetResponseExpected"/> and
\t\t///  <see cref="Tinkerforge.{3}{4}.SetResponseExpectedAll"/>.
\t\t/// </summary>
\t\tpublic static byte {2}_{0} = {1};
"""
    for packet in device.get_packets():
        function_ids += function_id.format(packet.get_upper_case_name(),
                                           packet.get_function_id(),
                                           packet.get_type().upper(),
                                           device.get_category(),
                                           device.get_camel_case_name())
    return function_ids

def make_constructor():
    cbs = []
    cb = '\t\t\tmessageCallbacks[CALLBACK_{0}] = new MessageCallback(On{1});'
    con = """
\t\t/// <summary>
\t\t///  Creates an object with the unique device ID <c>uid</c>. This object can
\t\t///  then be added to the IP connection.
\t\t/// </summary>
\t\tpublic {0}{1}(string uid, IPConnection ipcon) : base(uid, ipcon) 
\t\t{{
\t\t\tthis.apiVersion[0] = {3};
\t\t\tthis.apiVersion[1] = {4};
\t\t\tthis.apiVersion[2] = {5};
{2}
"""

    for packet in device.get_packets('callback'):
        name_upper = packet.get_upper_case_name()
        name_pascal = packet.get_camel_case_name()
        cbs.append(cb.format(name_upper, name_pascal))

    v = device.get_api_version()

    return con.format(device.get_category(),
                      device.get_camel_case_name(),
                      '\n'.join(cbs),
                      v[0], v[1], v[2],
                      device.get_display_name(),
                      device.get_category())

def make_response_expected():
    res = '\n'
    re = "\t\t\tresponseExpected[{0}] = {1}\n"

    for packet in device.get_packets('function'):
        name_upper = 'FUNCTION_' + packet.get_upper_case_name()
        setto = 'ResponseExpectedFlag.FALSE;'
        if len(packet.get_elements('out')) > 0:
            setto = 'ResponseExpectedFlag.ALWAYS_TRUE;'
        elif packet.get_doc()[0] == 'ccf':
            setto = 'ResponseExpectedFlag.TRUE;'

        res += re.format(name_upper, setto)

    for packet in device.get_packets('callback'):
        name_upper = 'CALLBACK_' + packet.get_upper_case_name()
        setto = 'ResponseExpectedFlag.ALWAYS_FALSE;'
        res += re.format(name_upper, setto)

    return res + '\t\t}\n'

def get_from_type(element):
    forms = {
        'int8' : 'SByteFrom',
        'uint8' : 'ByteFrom',
        'int16' : 'ShortFrom',
        'uint16' : 'UShortFrom',
        'int32' : 'IntFrom',
        'uint32' : 'UIntFrom',
        'int64' : 'LongFrom',
        'uint64' : 'ULongFrom',
        'float' : 'FloatFrom',
        'bool' : 'BoolFrom',
        'string' : 'StringFrom',
        'char' : 'CharFrom'
    }

    if element[1] in forms:
        from_type = forms[element[1]]
        if from_type != 'StringFrom' and element[2] > 1:
            from_type = from_type.replace('From', 'ArrayFrom')

        return from_type

    return ''

def make_callbacks():
    cbs = ''
    cb = """
\t\t/// <summary>
\t\t/// </summary>
\t\tprotected void On{0}(byte[] data_)
\t\t{{
{1}\t\t\tvar handler = {0};
\t\t\tif(handler != null)
\t\t\t{{
\t\t\t\thandler(this{3});
\t\t\t}}
\t\t}}
"""
    cls = device.get_camel_case_name()
    for packet in device.get_packets('callback'):
        name = packet.get_camel_case_name()
        name_upper = packet.get_upper_case_name()
        eles = []
        for element in packet.get_elements('out'):
            eles.append(common.underscore_to_headless_camel_case(element[0]))
        callParams = ", ".join(eles)
        signatureParams = csharp_common.make_parameter_list(packet)
        size = str(get_data_size(packet))

        convs = ''
        conv = '\t\t\t{0} {1} = LEConverter.{2}({3}, data_{4});\n'

        pos = 8
        for element in packet.get_elements('out'):
            csharp_type = csharp_common.get_csharp_type(element)
            cname = common.underscore_to_headless_camel_case(element[0])
            from_type = get_from_type(element)
            length = ''
            if element[2] > 1:
                length = ', ' + str(element[2])
            convs += conv.format(csharp_type, 
                                 cname, 
                                 from_type,
                                 pos,
                                 length)

            pos += common.get_element_size(element)

        if convs != '':
            convs += '\n'

        if callParams != '':
            callParams = ', ' + callParams
        
        cbs += cb.format(name, convs, name_upper, callParams, pos, signatureParams)

    return cbs + "\t}\n}"

def make_methods():
    methods = ''
    method = """
\t\t/// <summary>
\t\t///  {5}
\t\t/// </summary>
\t\t{0}
\t\t{{
\t\t\tbyte[] data_ = MakePacketHeader({1}, FUNCTION_{2});
{3}
{4}
\t\t}}
"""
    method_oneway = """\t\t\tif(responseExpected[FUNCTION_{0}] == ResponseExpectedFlag.ALWAYS_TRUE || responseExpected[FUNCTION_{0}] == ResponseExpectedFlag.TRUE) 
\t\t\t{{
\t\t\t\tbyte[] response;
\t\t\t\tSendRequestExpectResponse(data_, FUNCTION_{0}, out response);
\t\t\t}}
\t\t\telse
\t\t\t{{
\t\t\t\tSendRequestNoResponse(data_);
\t\t\t}}"""
    method_response = """\t\t\tbyte[] response;
\t\t\tSendRequestExpectResponse(data_, FUNCTION_{0}, out response);
{1}"""

    cls = device.get_camel_case_name()
    for packet in device.get_packets('function'):
        ret_count = len(packet.get_elements('out'))
        size = str(get_data_size(packet))
        name_upper = packet.get_upper_case_name()
        doc = format_doc(packet)

        write_convs = ''
        write_conv = '\t\t\tLEConverter.To(({2}){0}, {1}, data_);\n'
        write_conv_length = '\t\t\tLEConverter.To(({3}){0}, {1}, {2}, data_);\n'

        pos = 8
        for element in packet.get_elements('in'):
            wname = common.underscore_to_headless_camel_case(element[0])
            csharp_type = csharp_common.get_csharp_type_for_to_convert(element)
            if element[2] > 1:
                write_convs += write_conv_length.format(wname, pos, element[2], csharp_type)
            else:
                write_convs += write_conv.format(wname, pos, csharp_type)
            pos += common.get_element_size(element)

        method_tail = ''
        read_convs = ''
        read_conv = '\n\t\t\t{0} = LEConverter.{1}({2}, response{3});'

        pos = 8
        for element in packet.get_elements('out'):
            aname = common.underscore_to_headless_camel_case(element[0])
            from_type = get_from_type(element)
            length = ''
            if element[2] > 1:
                length = ', ' + str(element[2])

            if ret_count == 1:
                read_convs = '\n\t\t\treturn LEConverter.{0}({1}, response{2});'.format(from_type, pos, length)
            else:
                read_convs += read_conv.format(aname, from_type, pos, length)
            pos += common.get_element_size(element)

        if ret_count > 0:
            method_tail = method_response.format(name_upper, read_convs)
        else:
            method_tail = method_oneway.format(name_upper)

        signature = csharp_common.make_method_signature(packet)
        methods += method.format(signature,
                                 size,
                                 name_upper,
                                 write_convs,
                                 method_tail,
                                 doc)

    return methods

def get_data_size(packet):
    size = 0
    for element in packet.get_elements('in'):
        size += common.get_element_size(element)
    return size + 8

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)
    file_name = '{0}{1}'.format(device.get_category(), device.get_camel_case_name())
    directory += '/bindings'
    csharp = file('{0}/{1}.cs'.format(directory, file_name), "w")
    csharp.write(make_import())
    csharp.write(make_class())
    csharp.write(make_function_id_definitions())
    csharp.write(make_delegates())
    csharp.write(make_constructor())
    csharp.write(make_response_expected())
    csharp.write(make_methods())
    csharp.write(make_callbacks())

if __name__ == "__main__":
    common.generate(os.getcwd(), 'en', make_files, common.prepare_bindings, False)
