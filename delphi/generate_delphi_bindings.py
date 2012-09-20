#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Delphi Bindings Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
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

sys.path.append(os.path.split(os.getcwd())[0])
import common

device = None

def fix_links(text):
    link = '{0}{1}::{2}()'
    link_c = '{0}{1}::CALLBACK_{2}'

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
            replaced_lines.append('<warning>')
        elif len(line.strip()) == 0 and in_note:
            in_note = False
            replaced_lines.append('</note>')
            replaced_lines.append('')
        elif len(line.strip()) == 0 and in_warning:
            in_warning = False
            replaced_lines.append('</warning>')
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
    for packet in device.get_packets():
        name_false = ':func:`{0}`'.format(packet.get_camel_case_name())
        if packet.get_type() == 'callback':
            name = packet.get_upper_case_name()
            name_right = link_c.format(device.get_category(), cls, name)
        else:
            name = packet.get_headless_camel_case_name()
            name_right = link.format(device.get_category(), cls, name)

        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", "parameter")
    text = text.replace(":word:`parameters`", "parameters")
    text = text.replace('.. note::', '\\note')
    text = text.replace('.. warning::', '\\warning')

    return text

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

def make_unit_header():
    include = """{0}
unit {1}{2};

{{$ifdef FPC}}{{$mode OBJFPC}}{{$H+}}{{$endif}}

interface

uses
  Device, IPConnection, LEConverter;

"""
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    return include.format(common.gen_text_curly.format(date),
                          device.get_category(),
                          device.get_camel_case_name())

def make_function_id_definitions():
    function_ids = 'const\n'
    function_id = '  {0}_{1}_FUNCTION_{2} = {3};\n'
    for packet in device.get_packets('function'):
        function_ids += function_id.format(device.get_category().upper(),
                                           device.get_upper_case_name(),
                                           packet.get_upper_case_name(),
                                           packet.get_function_id())
    return function_ids

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
            arrays += '  {0} = {1};\n'.format(left, right)

        arrays += '\n'

    return arrays

def make_callback_prototypes():
    prototypes = ''
    prototype = '  T{0}{1}Notify{2} = procedure{3} of object;\n'

    for packet in device.get_packets('callback'):
        params = delphi_common.make_parameter_list(packet, False)

        if len(params) > 0:
            params = '(' + params + ')'

        prototypes += prototype.format(device.get_category(),
                                       device.get_camel_case_name(),
                                       packet.get_camel_case_name(),
                                       params)

    if len(prototypes) > 0:
        prototypes += '\n'

    return prototypes

def make_class():
    cls = '  T{0}{1} = class(TDevice)\n'.format(device.get_category(),
                                                device.get_camel_case_name())

    callbacks = ''
    callback = '    {0}Callback: T{1}{2}Notify{3};\n'
    for packet in device.get_packets('callback'):
        callbacks += callback.format(packet.get_headless_camel_case_name(),
                                     device.get_category(),
                                     device.get_camel_case_name(),
                                     packet.get_camel_case_name())

    callback_wrappers = ''
    callback_wrapper = '    procedure CallbackWrapper{0}(const packet: TByteArray); virtual;\n'
    for packet in device.get_packets('callback'):
        callback_wrappers += callback_wrapper.format(packet.get_camel_case_name())

    methods = ''
    function = '    function {0}{1}: {2}; virtual;'
    procedure = '    procedure {0}{1}; virtual;'
    for packet in device.get_packets('function'):
        ret_type = delphi_common.get_return_type(packet, False)
        name = packet.get_camel_case_name()
        params = delphi_common.make_parameter_list(packet, False)
        if len(params) > 0:
            params = '(' + params + ')'
        if len(ret_type) > 0:
            method = function.format(name, params, ret_type)
        else:
            method = procedure.format(name, params)
        methods += method + '\n'

    props = ''
    prop = '    property On{0}: T{1}{2}Notify{0} read {3}Callback write {3}Callback;\n'
    for packet in device.get_packets('callback'):
        props += prop.format(packet.get_camel_case_name(),
                             device.get_category(),
                             device.get_camel_case_name(),
                             packet.get_headless_camel_case_name())

    return  cls + \
            '  private\n' + \
            callbacks + \
            '  protected\n' + \
            callback_wrappers + \
            '  public\n' + \
            '    constructor Create(const uid_: string);\n' + \
            methods + \
            props + \
            '  end;\n\n'

def make_constructor():
    con = """implementation

constructor T{0}{1}.Create(const uid_: string);
begin
  inherited Create(uid_);
  expectedName := '{2} {3}';
  bindingVersion[0] := {4};
  bindingVersion[1] := {5};
  bindingVersion[2] := {6};
"""

    return con.format(device.get_category(),
                      device.get_camel_case_name(),
                      device.get_display_name(),
                      device.get_category(),
                      *device.get_version())

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
            if element[1] != 'string' and element[2] > 1:
                has_array = True
                break

        if has_array:
            method += ' i: longint;'

        method += '\n'
        method += 'begin\n'
        method += '  request := CreateRequestPacket(stackID, {0}, {1});\n'.format(function_id, packet.get_request_length())

        # Serialize request
        offset = 4
        for element in packet.get_elements('in'):
            if element[1] != 'string' and element[2] > 1:
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
            method += '  SetLength(response, 0);\n'
            method += '  SendRequestExpectResponse(request, {0}, response);\n'.format(function_id)
        else:
            method += '  SendRequestNoResponse(request);\n'

        # Deserialize response
        offset = 4
        for element in packet.get_elements('out'):
            if out_count > 1:
                result = common.underscore_to_headless_camel_case(element[0])
            else:
                result = 'result'

            if element[1] != 'string' and element[2] > 1:
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

        offset = 4
        parameter_names = []
        for element in packet.get_elements('out'):
            parameter_names.append(common.underscore_to_headless_camel_case(element[0]))

            if element[1] != 'string' and element[2] > 1:
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



        wrapper += '    {0}Callback({1});\n'.format(packet.get_headless_camel_case_name(), ', '.join(parameter_names))
        wrapper += '  end;\n'
        wrapper += 'end;\n\n'

        wrappers += wrapper

    return wrappers + 'end.\n'

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)

    file_name = '{0}{1}'.format(device.get_category(), device.get_camel_case_name())

    directory += '/bindings'
    if not os.path.exists(directory):
        os.makedirs(directory)

    pas = file('{0}/{1}.pas'.format(directory, file_name), 'w')
    pas.write(make_unit_header())
    pas.write(make_function_id_definitions())
    pas.write(make_callback_id_definitions())
    pas.write(make_arrays())
    pas.write(make_callback_prototypes())
    pas.write(make_class())
    pas.write(make_constructor())
    pas.write(make_callback_wrapper_definitions())
    pas.write(make_methods())
    pas.write(make_callback_wrappers())

if __name__ == "__main__":
    common.generate(os.getcwd(), 'en', make_files)
