#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Delphi Bindings Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_delphi_bindings.py: Generator for Delphi bindings

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
import delphi_common
from xml.sax.saxutils import escape

sys.path.append(os.path.split(os.getcwd())[0])
import common

device = None

def format_doc(packet):
    text = common.select_lang(packet.get_doc()[1])
    link = '<see cref="{0}{1}.T{0}{1}.{2}"/>'

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

    text = common.handle_rst_word(text)
    text = common.handle_rst_if(text, device)
    text += common.format_since_firmware(device, packet)

    return '\n    ///  '.join(text.strip().split('\n'))

def make_parameter_doc(packet):
    param = []
    for element in packet.get_elements():
        if element[3] == 'out' or packet.get_type() != 'function':
            continue

        delphi_type = delphi_common.get_delphi_type(element[1])[0]
        if element[2] > 1 and element[1] != 'string':
            param.append('@param {0}[] ${1}'.format(delphi_type, element[0]))
        else:
            param.append('@param {0} ${1}'.format(delphi_type, element[0]))

    param.append('\n@return ' + delphi_common.get_return_type(packet, True))
    return '\n'.join(param)

def make_unit_header(version):
    include = """{0}
unit {1}{2};

{{$ifdef FPC}}{{$mode OBJFPC}}{{$H+}}{{$endif}}

interface

uses
  Device, IPConnection, LEConverter;

"""
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    return include.format(common.gen_text_curly.format(date, *version),
                          device.get_category(),
                          device.get_camel_case_name())

def make_device_identifier():
    did = """const
  {0}_{1}_DEVICE_IDENTIFIER = {2};

"""

    return did.format(device.get_category().upper(),
                      device.get_upper_case_name(),
                      device.get_device_identifier())

def make_function_id_definitions():
    function_ids = ''
    function_id = '  {0}_{1}_FUNCTION_{2} = {3};\n'
    for packet in device.get_packets('function'):
        function_ids += function_id.format(device.get_category().upper(),
                                           device.get_upper_case_name(),
                                           packet.get_upper_case_name(),
                                           packet.get_function_id())
    return function_ids + '\n'

def make_constants():
    str_constants = ''
    str_constant = '  {0}_{1}_{2}_{3} = {4};\n'
    constants = device.get_constants()
    for constant in constants:
        for definition in constant.definitions:
            if constant.type == 'char':
                value = "'{0}'".format(definition.value)
            else:
                value = str(definition.value)

            str_constants += str_constant.format(device.get_category().upper(),
                                                 device.get_upper_case_name(),
                                                 constant.name_uppercase,
                                                 definition.name_uppercase,
                                                 value)
    return str_constants + '\n'

def make_callback_id_definitions():
    cbs = ''
    cb = '  {0}_{1}_CALLBACK_{2} = {3};\n'
    for packet in device.get_packets('callback'):
        cbs += cb.format(device.get_category().upper(),
                         device.get_upper_case_name(),
                         packet.get_upper_case_name(),
                         packet.get_function_id())
    return cbs + '\n'

def get_object_name(packet):
    name = packet.get_camel_case_name()
    if name.startswith('Get'):
        name = name[3:]

    return name

def make_arrays():
    arrays = 'type\n'
    types = {}

    for packet in device.get_packets('function'):
        for element in packet.get_elements():
            if element[1] == 'string' or element[2] < 2:
                continue

            delphi_type = delphi_common.get_delphi_type(element[1])
            left = 'TArray0To{0}Of{1}'.format(element[2] - 1, delphi_type[1])
            right = 'array [0..{0}] of {1}'.format(element[2] - 1, delphi_type[0])
            types[left] = right

    if len(types) > 0:
        for left in types:
            arrays += '  {0} = {1};\n'.format(left, types[left])

        arrays += '\n'

    return arrays

def make_callback_prototypes():
    prototypes = ''
    prototype = '  T{0}{1}Notify{2} = procedure(sender: T{0}{1}{3}) of object;\n'

    for packet in device.get_packets('callback'):
        params = delphi_common.make_parameter_list(packet, False)

        if len(params) > 0:
            params = '; ' + params

        prototypes += prototype.format(device.get_category(),
                                       device.get_camel_case_name(),
                                       packet.get_camel_case_name(),
                                       params)

    if len(prototypes) > 0:
        forward = '  T{0}{1} = class;\n'.format(device.get_category(),
                                              device.get_camel_case_name())
        prototypes = forward + prototypes + '\n'

    return prototypes

def make_class():
    cls = """  /// <summary>
  ///  {2}
  /// </summary>
  T{0}{1} = class(TDevice)
""".format(device.get_category(),
           device.get_camel_case_name(),
           device.get_description())

    callbacks = ''
    callback = '    {0}Callback: T{1}{2}Notify{3};\n'
    for packet in device.get_packets('callback'):
        callbacks += callback.format(packet.get_headless_camel_case_name(),
                                     device.get_category(),
                                     device.get_camel_case_name(),
                                     packet.get_camel_case_name())

    callback_wrappers = ''
    callback_wrapper = '    procedure CallbackWrapper{0}(const packet: TByteArray); {1};\n'
    for packet in device.get_packets('callback'):
        if packet.has_prototype_in_device():
            modifier = 'override'
        else:
            modifier = 'virtual'

        callback_wrappers += callback_wrapper.format(packet.get_camel_case_name(), modifier)

    methods = []
    function = """    /// <summary>
    ///  {3}
    /// </summary>
    function {0}{1}: {2}; {4};"""
    procedure = """    /// <summary>
    ///  {2}
    /// </summary>
    procedure {0}{1}; {3};"""
    for packet in device.get_packets('function'):
        ret_type = delphi_common.get_return_type(packet, False)
        name = packet.get_camel_case_name()
        doc = format_doc(packet)
        params = delphi_common.make_parameter_list(packet, False)
        if packet.has_prototype_in_device():
            modifier = 'override'
        else:
            modifier = 'virtual'
        if len(params) > 0:
            params = '(' + params + ')'
        if len(ret_type) > 0:
            method = function.format(name, params, ret_type, doc, modifier)
        else:
            method = procedure.format(name, params, doc, modifier)
        methods.append(method)

    props = []
    prop = """    /// <summary>
    ///  {4}
    /// </summary>
    property On{0}: T{1}{2}Notify{0} read {3}Callback write {3}Callback;"""
    for packet in device.get_packets('callback'):
        doc = format_doc(packet)
        props.append(prop.format(packet.get_camel_case_name(),
                                 device.get_category(),
                                 device.get_camel_case_name(),
                                 packet.get_headless_camel_case_name(),
                                 doc))

    return  cls + \
            '  private\n' + \
            callbacks + \
            '  protected\n' + \
            callback_wrappers + \
            '  public\n' + \
            '    /// <summary>\n' + \
            '    ///  Creates an object with the unique device ID <c>uid</c>. This object can\n' + \
            '    ///  then be added to the IP connection.\n' + \
            '    /// </summary>\n' + \
            '    constructor Create(const uid__: string; ipcon_: TIPConnection);\n\n' + \
            '\n\n'.join(methods + props) + '\n' + \
            '  end;\n\n'

def make_constructor():
    con = """implementation

constructor T{0}{1}.Create(const uid__: string; ipcon_: TIPConnection);
begin
  inherited Create(uid__, ipcon_);
  apiVersion[0] := {2};
  apiVersion[1] := {3};
  apiVersion[2] := {4};

"""
    response_expected = ''

    for packet in device.get_packets():
        if packet.get_type() == 'callback':
            prefix = 'CALLBACK_'
            flag = 'DEVICE_RESPONSE_EXPECTED_ALWAYS_FALSE'
        elif len(packet.get_elements('out')) > 0:
            prefix = 'FUNCTION_'
            flag = 'DEVICE_RESPONSE_EXPECTED_ALWAYS_TRUE'
        elif packet.get_doc()[0] == 'ccf':
            prefix = 'FUNCTION_'
            flag = 'DEVICE_RESPONSE_EXPECTED_TRUE'
        else:
            prefix = 'FUNCTION_'
            flag = 'DEVICE_RESPONSE_EXPECTED_FALSE'

        response_expected += '  responseExpected[{0}_{1}_{2}{3}] := {4};\n' \
            .format(device.get_category().upper(),
                    device.get_upper_case_name(),
                    prefix,
                    packet.get_upper_case_name(),
                    flag)

    if len(response_expected) > 0:
        response_expected += '\n'

    return con.format(device.get_category(),
                      device.get_camel_case_name(),
                      *device.get_api_version()) + response_expected

def make_callback_wrapper_definitions():
    cbs = ''
    cb = '  callbackWrappers[{0}_{1}_CALLBACK_{2}] := {{$ifdef FPC}}@{{$endif}}CallbackWrapper{3};\n'
    cbs_end = 'end;\n\n'
    for packet in device.get_packets('callback'):
        cbs += cb.format(device.get_category().upper(),
                         device.get_upper_case_name(),
                         packet.get_upper_case_name(),
                         packet.get_camel_case_name())
    return cbs + cbs_end

def get_convert_type(element):
    types = {
        'int8'   : 'Int8',
        'uint8'  : 'UInt8',
        'int16'  : 'Int16',
        'uint16' : 'UInt16',
        'int32'  : 'Int32',
        'uint32' : 'UInt32',
        'int64'  : 'Int64',
        'uint64' : 'UInt64',
        'float'  : 'Float',
        'bool'   : 'Boolean',
        'string' : 'String',
        'char'   : 'Char'
    }

    return types[element[1]];

def make_methods():
    methods = ''
    function = 'function {0}.{1}{2}: {3};\n'
    procedure = 'procedure {0}.{1}{2};\n'

    cls = 'T{0}{1}'.format(device.get_category(), device.get_camel_case_name())
    for packet in device.get_packets('function'):
        ret_type = delphi_common.get_return_type(packet, False)
        out_count = len(packet.get_elements('out'))
        name = packet.get_camel_case_name()
        params = delphi_common.make_parameter_list(packet, False)
        function_id = '{0}_{1}_FUNCTION_{2}'.format(device.get_category().upper(),
                                                    device.get_upper_case_name(),
                                                    packet.get_upper_case_name())
        if len(params) > 0:
            params = '(' + params + ')'

        if len(ret_type) > 0:
            method = function.format(cls, name, params, ret_type)
        else:
            method = procedure.format(cls, name, params)

        if out_count > 0:
            method += 'var request, response: TByteArray;'
        else:
            method += 'var request: TByteArray;'

        has_array = False
        for element in packet.get_elements():
            if element[2] > 1 and element[1] != 'string':
                has_array = True
                break

        if has_array:
            method += ' i: longint;'

        method += '\n'
        method += 'begin\n'
        method += '  request := (ipcon as TIPConnection).CreateRequestPacket(self, {0}, {1});\n'.format(function_id, packet.get_request_length())

        # Serialize request
        offset = 8
        for element in packet.get_elements('in'):
            if element[2] > 1 and element[1] != 'string':
                prefix = 'for i := 0 to Length({0}) - 1 do '.format(common.underscore_to_headless_camel_case(element[0]))
                method += '  {0}LEConvert{1}To({2}[i], {3} + (i * {4}), request);\n'.format(prefix,
                                                                                            get_convert_type(element),
                                                                                            common.underscore_to_headless_camel_case(element[0]),
                                                                                            offset,
                                                                                            common.get_type_size(element[1]))
            elif element[1] == 'string':
                method += '  LEConvertStringTo({0}, {1}, {2}, request);\n'.format(common.underscore_to_headless_camel_case(element[0]),
                                                                                  offset,
                                                                                  element[2])
            else:
                method += '  LEConvert{0}To({1}, {2}, request);\n'.format(get_convert_type(element),
                                                                          common.underscore_to_headless_camel_case(element[0]),
                                                                          offset)

            offset += common.get_element_size(element)

        if out_count > 0:
            method += '  response := SendRequest(request);\n'
        else:
            method += '  SendRequest(request);\n'

        # Deserialize response
        offset = 8
        for element in packet.get_elements('out'):
            if out_count > 1:
                result = common.underscore_to_headless_camel_case(element[0])
            else:
                result = 'result'

            if element[2] > 1 and element[1] != 'string':
                prefix = 'for i := 0 to {0} do '.format(element[2] - 1)
                method += '  {0}{1}[i] := LEConvert{2}From({3} + (i * {4}), response);\n'.format(prefix,
                                                                                                 result,
                                                                                                 get_convert_type(element),
                                                                                                 offset,
                                                                                                 common.get_type_size(element[1]))
            elif element[1] == 'string':
                method += '  {0} := LEConvertStringFrom({1}, {2}, response);\n'.format(result,
                                                                                       offset,
                                                                                       element[2])
            else:
                method += '  {0} := LEConvert{1}From({2}, response);\n'.format(result,
                                                                               get_convert_type(element),
                                                                               offset)

            offset += common.get_element_size(element)

        method += 'end;\n\n'

        methods += method

    return methods

def make_callback_wrappers():
    wrappers = ''

    for packet in device.get_packets('callback'):
        wrapper = 'procedure T{0}{1}.CallbackWrapper{2}(const packet: TByteArray);\n'.format(device.get_category(),
                                                                                             device.get_camel_case_name(),
                                                                                             packet.get_camel_case_name())

        if len(packet.get_elements('out')) > 0:
            wrapper += 'var ' + delphi_common.make_parameter_list(packet, False, False) + ';\n'

        wrapper += 'begin\n'

        if len(packet.get_elements('out')) == 0:
            wrapper += '  Assert(packet <> nil); { Avoid \'Parameter not used\' warning }\n'

        wrapper += '  if (Assigned({0}Callback)) then begin\n'.format(packet.get_headless_camel_case_name())

        offset = 8
        parameter_names = []
        for element in packet.get_elements('out'):
            parameter_names.append(common.underscore_to_headless_camel_case(element[0]))

            if element[2] > 1 and element[1] != 'string':
                prefix = 'for i := 0 to {0} do '.format(element[2] - 1)
                wrapper += '    {0}{1}[i] := LEConvert{2}From({3} + (i * {4}), packet);\n'.format(prefix,
                                                                                                  common.underscore_to_headless_camel_case(element[0]),
                                                                                                  get_convert_type(element),
                                                                                                  offset,
                                                                                                  common.get_type_size(element[1]))
            else:
                wrapper += '    {0} := LEConvert{1}From({2}, packet);\n'.format(common.underscore_to_headless_camel_case(element[0]),
                                                                                get_convert_type(element),
                                                                                offset)

            offset += common.get_element_size(element)



        wrapper += '    {0}Callback({1});\n'.format(packet.get_headless_camel_case_name(), ', '.join(['self'] + parameter_names))
        wrapper += '  end;\n'
        wrapper += 'end;\n\n'

        wrappers += wrapper

    return wrappers + 'end.\n'

def make_files(device_, directory):
    global device
    device = device_
    file_name = '{0}{1}'.format(device.get_category(), device.get_camel_case_name())
    version = common.get_changelog_version(directory)
    directory += '/bindings'

    pas = file('{0}/{1}.pas'.format(directory, file_name), 'w')
    pas.write(make_unit_header(version))
    pas.write(make_device_identifier())
    pas.write(make_function_id_definitions())
    pas.write(make_callback_id_definitions())
    pas.write(make_constants())
    pas.write(make_arrays())
    pas.write(make_callback_prototypes())
    pas.write(make_class())
    pas.write(make_constructor())
    pas.write(make_callback_wrapper_definitions())
    pas.write(make_methods())
    pas.write(make_callback_wrappers())

if __name__ == "__main__":
    common.generate(os.getcwd(), 'en', make_files, common.prepare_bindings, None, False)
