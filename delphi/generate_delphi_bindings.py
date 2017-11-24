#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Delphi/Lazarus Bindings Generator
Copyright (C) 2012-2015, 2017 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_delphi_bindings.py: Generator for Delphi/Lazarus bindings

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
import math
import delphi_common
from xml.sax.saxutils import escape

sys.path.append(os.path.split(os.getcwd())[0])
import common

class DelphiBindingsDevice(delphi_common.DelphiDevice):
    def get_fixed_stream_length_type(self, stream_max_length):
        if stream_max_length < 256:
            return 'byte'
        elif stream_max_length > 255 and stream_max_length < 65536:
            return 'word'
        elif stream_max_length > 65535 and stream_max_length < 4294967296:
            return 'word'
        else:
            return ''

    def specialize_delphi_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return '<see cref="{0}.{1}.On{2}"/>'.format(packet.get_device().get_delphi_class_name()[1:],
                                                            packet.get_device().get_delphi_class_name(),
                                                            packet.get_camel_case_name(skip=-2 if high_level else 0))
            else:
                return '<see cref="{0}.{1}.{2}"/>'.format(packet.get_device().get_delphi_class_name()[1:],
                                                          packet.get_device().get_delphi_class_name(),
                                                          packet.get_camel_case_name(skip=-2 if high_level else 0))

        return self.specialize_doc_rst_links(text, specializer)

    def get_delphi_unit_header(self):
        template = """{0}
unit {1}{2};

{{$ifdef FPC}}{{$mode OBJFPC}}{{$H+}}{{$endif}}

interface

uses
  Device, IPConnection, LEConverter, Math, SyncObjs;

"""

        return template.format(self.get_generator().get_header_comment('curly'),
                               self.get_camel_case_category(),
                               self.get_camel_case_name())

    def get_delphi_device_identifier(self):
        template = """const
  {0}_{1}_DEVICE_IDENTIFIER = {2};
"""

        return template.format(self.get_upper_case_category(),
                               self.get_upper_case_name(),
                               self.get_device_identifier())

    def get_delphi_device_display_name(self):
        template = """  {0}_{1}_DEVICE_DISPLAY_NAME = '{2}';

"""

        return template.format(self.get_upper_case_category(),
                               self.get_upper_case_name(),
                               self.get_long_display_name())

    def get_delphi_function_id_definitions(self):
        function_ids = ''
        template = '  {0}_{1}_FUNCTION_{2} = {3};\n'

        for packet in self.get_packets('function'):
            function_ids += template.format(self.get_upper_case_category(),
                                            self.get_upper_case_name(),
                                            packet.get_upper_case_name(),
                                            packet.get_function_id())

        return function_ids + '\n'

    def get_delphi_constants(self):
        constant_format = '  {prefix}_{constant_group_upper_case_name}_{constant_upper_case_name} = {constant_value};\n'

        return self.get_formatted_constants(constant_format, prefix=self.get_upper_case_category()+'_'+self.get_upper_case_name()) + '\n'

    def get_delphi_callback_id_definitions(self):
        callback_ids = ''
        template = '  {0}_{1}_CALLBACK_{2} = {3};\n'

        for packet in self.get_packets('callback'):
            callback_ids += template.format(self.get_upper_case_category(),
                                            self.get_upper_case_name(),
                                            packet.get_upper_case_name(),
                                            packet.get_function_id())

        return callback_ids + '\n'

    def get_delphi_arrays(self):
        arrays = 'type\n'
        types = {}

        for packet in self.get_packets():
            for element in packet.get_elements():
                if element.get_type() == 'string' or element.get_cardinality() < 2:
                    continue

                delphi_type = element.get_delphi_type()
                left = 'TArray0To{0}Of{1}'.format(element.get_cardinality() - 1, delphi_type[1])
                right = 'array [0..{0}] of {1}'.format(element.get_cardinality() - 1, delphi_type[0])
                types[left] = right

            for element in packet.get_elements(high_level=True):
                if element.get_cardinality() > 0:
                    continue

                delphi_type = element.get_delphi_type()
                left = 'TArrayOf{0}'.format(delphi_type[1])
                right = 'array of {0}'.format(delphi_type[0])
                types[left] = right

        if len(types) > 0:
            for left in sorted(types):
                arrays += '  {0} = {1};\n'.format(left, types[left])

            arrays += '\n'

        has_high_level_callback_states = False

        for packet in self.get_packets('callback'):
            if not packet.has_high_level():
                continue

            stream_out = packet.get_high_level('stream_out')

            if not stream_out:
                continue

            has_high_level_callback_states = True
            callback_state_data_delphi_type = None
            callback_state_length_delphi_type = None

            for element in packet.get_elements(direction='out'):
                role = element.get_role()

                if not role:
                    continue

                if role.endswith('length'):
                    callback_state_length_delphi_type = element.get_delphi_type()[0]

                if role.endswith('data'):
                    callback_state_data_delphi_type = element.get_delphi_type()[0]

                    if stream_out.get_fixed_length():
                        callback_state_length_delphi_type = self.get_fixed_stream_length_type(abs(stream_out.get_data_element().get_cardinality()))

            arrays += '  T{0}HighLevelCallbackState = record data: array of {1}; length: {2}; end;\n' \
                      .format(packet.get_camel_case_name(skip=-2),
                              callback_state_data_delphi_type,
                              callback_state_length_delphi_type)

        if has_high_level_callback_states:
            arrays += '\n'

        return arrays

    def get_delphi_callback_prototypes(self):
        prototypes = ''
        template = '  {0}Notify{1} = procedure(sender: {0}{2}) of object;\n'

        for packet in self.get_packets('callback'):
            params = common.wrap_non_empty('; ', '; '.join(packet.get_delphi_parameters(False)), '')
            prototypes += template.format(self.get_delphi_class_name(),
                                          packet.get_camel_case_name(),
                                          params)

            if not packet.has_high_level():
                continue

            stream_out = packet.get_high_level('stream_out')

            if not stream_out:
                continue

            high_level_parameters = []

            for element in packet.get_elements(direction='out'):
                role = element.get_role()

                if not role:
                    high_level_parameters.append('const ' + element.get_headless_camel_case_name() + ': ' + element.get_delphi_type()[0])
                else:
                    if role.endswith('data'):
                        high_level_parameters.append('const ' + stream_out.get_headless_camel_case_name() + ': array of ' + element.get_delphi_type()[0])

            params = '; '.join(high_level_parameters)

            if len(params) > 0:
                params = '; ' + params

            prototypes += template.format(self.get_delphi_class_name(),
                                          packet.get_camel_case_name(skip=-2),
                                          params)

        if len(prototypes) > 0:
            forward = '  {0} = class;\n'.format(self.get_delphi_class_name())
            prototypes = forward + prototypes + '\n'

        return prototypes

    def get_delphi_class(self):
        cls = """  /// <summary>
  ///  {1}
  /// </summary>
  {0} = class(TDevice)
""".format(self.get_delphi_class_name(), common.select_lang(self.get_description()))

        callbacks = ''
        template = '    {0}Callback: {1}Notify{2};\n'

        for packet in self.get_packets('callback'):
            callbacks += template.format(packet.get_headless_camel_case_name(),
                                         self.get_delphi_class_name(),
                                         packet.get_camel_case_name())

            if not packet.has_high_level():
                continue

            stream_out = packet.get_high_level('stream_out')

            if not stream_out:
                continue

            callbacks += template.format(packet.get_headless_camel_case_name(skip=-2),
                                         self.get_delphi_class_name(),
                                         packet.get_camel_case_name(skip=-2))

        callback_wrappers = ''
        template_wrapper = '    procedure CallbackWrapper{0}(const packet: TByteArray); {1};\n'

        for packet in self.get_packets('callback'):
            if packet.has_prototype_in_device():
                modifier = 'override'
            else:
                modifier = 'virtual'

            callback_wrappers += template_wrapper.format(packet.get_camel_case_name(), modifier)

        methods = []
        function = """    /// <summary>
    ///  {3}
    /// </summary>
    function {0}{1}: {2}; {4};"""
        procedure = """    /// <summary>
    ///  {2}
    /// </summary>
    procedure {0}{1}; {3};"""

        for packet in self.get_packets('function'):
            ret_type = packet.get_delphi_return_type(False)
            name = packet.get_camel_case_name()
            doc = packet.get_delphi_formatted_doc()
            params = common.wrap_non_empty('(', '; '.join(packet.get_delphi_parameters(False)), ')')

            if packet.has_prototype_in_device():
                modifier = 'override'
            else:
                modifier = 'virtual'

            if len(ret_type) > 0:
                method = function.format(name, params, ret_type, doc, modifier)
            else:
                method = procedure.format(name, params, doc, modifier)

            methods.append(method)

            if packet.has_high_level():
                e_params = []
                name = packet.get_camel_case_name(skip=-2)
                stream_in = packet.get_high_level('stream_in')
                stream_out = packet.get_high_level('stream_out')

                for e in packet.get_elements():
                    e_param = None
                    ret_type, e_param = self.get_high_level_method_parameters(e, ret_type, stream_in, stream_out)

                    if e_param:
                        e_params.append(e_param)

                if stream_out:
                    if len(e_params) > 0:
                        params = '(' + '; '.join(e_params) + ')'
                    else:
                        params = '()'

                    if len(ret_type) > 0:
                        method = function.format(name, params, ret_type, doc, modifier)
                    else:
                        method = procedure.format(name, params, doc, modifier)

                    methods.append(method)
                elif stream_in:
                    if len(e_params) > 0:
                        params = '(' + '; '.join(e_params) + ')'
                    else:
                        params = '()'

                    if len(ret_type) > 0:
                        method = function.format(name, params, ret_type, doc, modifier)
                    else:
                        method = procedure.format(name, params, doc, modifier)

                    methods.append(method)

        props = []
        prop = """    /// <summary>
    ///  {3}
    /// </summary>
    property On{0}: {1}Notify{0} read {2}Callback write {2}Callback;"""

        has_stream = False

        for packet in self.get_packets():
            if packet.get_high_level('stream_*') != None:
                has_stream = True
                break

        high_level_callback_data_variables = ''

        for packet in self.get_packets('callback'):
            doc = packet.get_delphi_formatted_doc()
            props.append(prop.format(packet.get_camel_case_name(),
                                     self.get_delphi_class_name(),
                                     packet.get_headless_camel_case_name(),
                                     doc))

            stream_out = packet.get_high_level('stream_out')

            if stream_out == None:
                continue

            high_level_callback_data_variables += \
                '    {0}HighLevelCallbackState: T{1}HighLevelCallbackState;\n'.format(packet.get_headless_camel_case_name(skip=-2),
                                                                                      packet.get_camel_case_name(skip=-2))

            props.append(prop.format(packet.get_camel_case_name(skip=-2),
                                     self.get_delphi_class_name(),
                                     packet.get_headless_camel_case_name(skip=-2),
                                     doc))

        if self.get_long_display_name() == 'RS232 Bricklet':
            props.append("""
    /// <summary>
    ///  This callback is called if new data is available. The message has
    ///  a maximum size of 60 characters. The actual length of the message
    ///  is given in addition.
    ///
    ///  To enable this callback, use <see cref="BrickletRS232.TBrickletRS232.EnableReadCallback"/>.
    /// </summary>
    property OnReadCallback: TBrickletRS232NotifyRead read readCallback write readCallback; { for backward compatibility }

    /// <summary>
    ///  This callback is called if an error occurs.
    ///  Possible errors are overrun, parity or framing error.
    ///
    ///  .. versionadded:: 2.0.1$nbsp;(Plugin)
    /// </summary>
    property OnErrorCallback: TBrickletRS232NotifyError read errorCallback write errorCallback; { for backward compatibility }
""")

        return  cls + \
                '  private\n' + \
                ('    streamMutex: TCriticalSection;\n' if has_stream else '') + \
                high_level_callback_data_variables + \
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

    def get_delphi_constructor(self):
        con = """implementation

constructor {0}.Create(const uid__: string; ipcon_: TIPConnection);
begin
  inherited Create(uid__, ipcon_);
  apiVersion[0] := {1};
  apiVersion[1] := {2};
  apiVersion[2] := {3};

"""
        response_expected = ''

        for packet in self.get_packets('function'):
            if len(packet.get_elements(direction='out')) > 0:
                flag = 'DEVICE_RESPONSE_EXPECTED_ALWAYS_TRUE'
            elif packet.get_doc_type() == 'ccf' or packet.get_high_level('stream_in') != None:
                flag = 'DEVICE_RESPONSE_EXPECTED_TRUE'
            else:
                flag = 'DEVICE_RESPONSE_EXPECTED_FALSE'

            response_expected += '  responseExpected[{0}_{1}_FUNCTION_{2}] := {3};\n' \
                                 .format(self.get_upper_case_category(),
                                         self.get_upper_case_name(),
                                         packet.get_upper_case_name(),
                                         flag)

        if len(response_expected) > 0:
            response_expected += '\n'

        stream_mutex = ''
        high_level_callback_state = ''

        for packet in self.get_packets('callback'):
            if not packet.has_high_level():
                continue

            stream_out = packet.get_high_level('stream_out')

            if not stream_out:
                continue

            stream_mutex = '  streamMutex := TCriticalSection.Create;\n\n'
            high_level_callback_state += \
                '  SetLength({0}HighLevelCallbackState.data, 0);\n\
  {0}HighLevelCallbackState.data := nil;\n\
  {0}HighLevelCallbackState.length := 0;\n\n'.format(packet.get_headless_camel_case_name(skip=-2))

        return con.format(self.get_delphi_class_name(),
                          *self.get_api_version()) + response_expected + stream_mutex + high_level_callback_state

    def get_delphi_callback_wrapper_definitions(self):
        callbacks = ''
        template = '  callbackWrappers[{0}_{1}_CALLBACK_{2}] := {{$ifdef FPC}}@{{$endif}}CallbackWrapper{3};\n'

        for packet in self.get_packets('callback'):
            callbacks += template.format(self.get_upper_case_category(),
                                         self.get_upper_case_name(),
                                         packet.get_upper_case_name(),
                                         packet.get_camel_case_name())

        return callbacks + 'end;\n\n'

    def get_high_level_method_parameters(self, e, ret_type, stream_in, stream_out):
        e_param = None

        if not e:
            return ret_type, e_param

        role = e.get_role()

        if stream_in:
            if ret_type and len(ret_type) > 0:
                if e.get_direction() == 'out' and e.get_cardinality() > 1:
                    ret_type = 'array of ' + e.get_delphi_type()[0]

                if e.get_direction() == 'in':
                    if role:
                        if stream_in.has_short_write() and role.endswith('length'):
                            ret_type = e.get_delphi_type()[0]

                        if role.endswith('data'):
                            if e.get_cardinality() > 1:
                                e_param = 'const ' + stream_in.get_headless_camel_case_name() + ': array of ' + e.get_delphi_type()[0]
                            else:
                                e_param = 'const ' + stream_in.get_headless_camel_case_name() + ': ' + e.get_delphi_type()[0]
                    else:
                        if e.get_cardinality() > 1:
                            e_param = 'const ' + e.get_headless_camel_case_name() + ': array of ' + e.get_delphi_type()[0]
                        else:
                            e_param = 'const ' + e.get_headless_camel_case_name() + ': ' + e.get_delphi_type()[0]
            else:
                if e.get_direction() == 'out':
                    if e.get_cardinality() > 1:
                        e_param = 'out ' + e.get_headless_camel_case_name() + ': array of ' + e.get_delphi_type()[0]
                    else:
                        e_param = 'out ' + e.get_headless_camel_case_name() + ': ' + e.get_delphi_type()[0]
                elif e.get_direction() == 'in':
                    if role:
                        if stream_in.has_short_write() and role.endswith('length'):
                            ret_type = e.get_delphi_type()[0]

                        if role.endswith('data'):
                            if e.get_cardinality() > 1:
                                e_param = 'const ' + stream_in.get_headless_camel_case_name() + ': array of ' + e.get_delphi_type()[0]
                            else:
                                e_param = 'const ' + stream_in.get_headless_camel_case_name() + ': ' + e.get_delphi_type()[0]
                    else:
                        if e.get_cardinality() > 1:
                            e_param = 'const ' + e.get_headless_camel_case_name() + ': array of ' + e.get_delphi_type()[0]
                        else:
                            e_param = 'const ' + e.get_headless_camel_case_name() + ': ' + e.get_delphi_type()[0]

        elif stream_out:
            if ret_type and len(ret_type) > 0:
                if e.get_direction() == 'out' and e.get_cardinality() > 1:
                    ret_type = 'array of ' + e.get_delphi_type()[0]

                if e.get_direction() == 'in':
                    if e.get_cardinality() > 1:
                        e_param = 'const ' + e.get_headless_camel_case_name() + ': TArrayOf' + e.get_delphi_type()[1]
                    else:
                        e_param = 'const ' + e.get_headless_camel_case_name() + ': ' + e.get_delphi_type()[0]
            else:
                if e.get_direction() == 'out':
                    if role:
                        if role.endswith('data'):
                            if e.get_cardinality() > 1:
                                e_param = 'out ' + stream_out.get_headless_camel_case_name() + ': TArrayOf' + e.get_delphi_type()[1]
                            else:
                                e_param = 'out ' + stream_out.get_headless_camel_case_name() + ': ' + e.get_delphi_type()[0]
                    else:
                        if e.get_cardinality() > 1:
                            e_param = 'out ' + e.get_headless_camel_case_name() + ': TArrayOf' + e.get_delphi_type()[1]
                        else:
                            e_param = 'out ' + e.get_headless_camel_case_name() + ': ' + e.get_delphi_type()[0]
                elif e.get_direction() == 'in':
                    if e.get_cardinality() > 1:
                        e_param = 'const ' + e.get_headless_camel_case_name() + ': TArrayOf' + e.get_delphi_type()[1]
                    else:
                        e_param = 'const ' + e.get_headless_camel_case_name() + ': ' + e.get_delphi_type()[0]

        return ret_type, e_param

    def get_delphi_methods(self):
        methods = ''
        function = 'function {0}.{1}{2}: {3};\n'
        procedure = 'procedure {0}.{1}{2};\n'
        cls = self.get_delphi_class_name()

        for packet in self.get_packets('function'):
            ret_type = packet.get_delphi_return_type(False)
            out_count = len(packet.get_elements(direction='out'))
            name = packet.get_camel_case_name()
            params = common.wrap_non_empty('(', '; '.join(packet.get_delphi_parameters(False)), ')')
            function_id = '{0}_{1}_FUNCTION_{2}'.format(self.get_upper_case_category(),
                                                        self.get_upper_case_name(),
                                                        packet.get_upper_case_name())

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
                if element.get_cardinality() > 1 and element.get_type() != 'string':
                    has_array = True
                    break

            if has_array:
                method += ' i: longint;'

            for element in packet.get_elements():
                if element.get_cardinality() > 1 and element.get_type() == 'bool':
                    method += ' {0}Bits: array [0..{1}] of byte;'.format(element.get_headless_camel_case_name(),
                                                                         int(math.ceil(element.get_cardinality() / 8.0) - 1))

            method += '\n'
            method += 'begin\n'
            method += '  request := (ipcon as TIPConnection).CreateRequestPacket(self, {0}, {1});\n'.format(function_id, packet.get_request_size())

            method_bool_array_fmt = """  FillChar({0}[0], Length({0}) * SizeOf({0}[0]), 0);
  for i := 0 to {1} do if {2}[i] then {0}[Floor(i/8)] := {0}[Floor(i/8)] or (1 shl (i mod 8));
  for i := 0 to {3} do LEConvertUInt8To({0}[i], {4} + (i * 1), request);
"""

            # Serialize request
            offset = 8

            for element in packet.get_elements(direction='in'):
                if element.get_cardinality() > 1 and element.get_type() != 'string' and element.get_type() != 'bool':
                    prefix = 'for i := 0 to Length({0}) - 1 do '.format(element.get_headless_camel_case_name())
                    method += '  {0}LEConvert{1}To({2}[i], {3} + (i * {4}), request);\n'.format(prefix,
                                                                                                element.get_delphi_le_convert_type(),
                                                                                                element.get_headless_camel_case_name(),
                                                                                                offset,
                                                                                                element.get_item_size())
                elif element.get_cardinality() > 1 and element.get_type() == 'bool':
                    method += method_bool_array_fmt.format(element.get_headless_camel_case_name() + 'Bits',
                                                           element.get_cardinality() - 1,
                                                           element.get_headless_camel_case_name(),
                                                           str(int(math.ceil(element.get_cardinality() / 8.0) - 1)),
                                                           offset)
                elif element.get_type() == 'string':
                    method += '  LEConvertStringTo({0}, {1}, {2}, request);\n'.format(element.get_headless_camel_case_name(),
                                                                                      offset,
                                                                                      element.get_cardinality())

                else:
                    method += '  LEConvert{0}To({1}, {2}, request);\n'.format(element.get_delphi_le_convert_type(),
                                                                              element.get_headless_camel_case_name(),
                                                                              offset)

                offset += element.get_size()

            if out_count > 0:
                method += '  response := SendRequest(request);\n'
            else:
                method += '  SendRequest(request);\n'

            # Deserialize response
            offset = 8

            method_bool_array_fmt = """  FillChar({0}[0], Length({0}) * SizeOf({0}[0]), 0);
  for i := 0 to {1} do {0}[i] := LEConvertUInt8From({2} + (i * 1), packet);
  for i := 0 to {3} do {4}[i] := (({0}[Floor(i / 8)] and (1 shl (i mod 8))) <> 0);
"""

            for element in packet.get_elements(direction='out'):
                if out_count > 1:
                    result = element.get_headless_camel_case_name()
                else:
                    result = 'result'

                if element.get_cardinality() > 1 and element.get_type() != 'string' and element.get_type() != 'bool':
                    prefix = 'for i := 0 to {0} do '.format(element.get_cardinality() - 1)
                    method += '  {0}{1}[i] := LEConvert{2}From({3} + (i * {4}), response);\n'.format(prefix,
                                                                                                     result,
                                                                                                     element.get_delphi_le_convert_type(),
                                                                                                     offset,
                                                                                                     element.get_item_size())
                elif element.get_cardinality() > 1 and element.get_type() == 'bool':
                    method += method_bool_array_fmt.format(element.get_headless_camel_case_name() + 'Bits',
                                                           str(int(math.ceil(element.get_cardinality() / 8.0) - 1)),
                                                           offset,
                                                           element.get_cardinality() - 1,
                                                           element.get_headless_camel_case_name())
                elif element.get_type() == 'string':
                    method += '  {0} := LEConvertStringFrom({1}, {2}, response);\n'.format(result,
                                                                                           offset,
                                                                                           element.get_cardinality())
                else:
                    method += '  {0} := LEConvert{1}From({2}, response);\n'.format(result,
                                                                                   element.get_delphi_le_convert_type(),
                                                                                   offset)

                offset += element.get_size()

            method += 'end;\n\n'

            methods += method

            if packet.has_high_level():
                template_high_level_stream_in = """{method_signature}var {stream_headless_camel_case_name}ChunkOffset: {stream_length_type}; {stream_headless_camel_case_name}ChunkData: TArray0To{chunk_cardinality_minus_1}Of{chunk_data_type_capitalized}; {stream_headless_camel_case_name}ChunkLength: {stream_length_type}; {stream_headless_camel_case_name}Length: {stream_length_type};
begin
  if (Length({stream_headless_camel_case_name}) > {stream_max_length}) then begin
    raise EInvalidParameterException.Create('{stream_name} can be at most {stream_max_length} items long');
  end;

  {stream_headless_camel_case_name}Length := Length({stream_headless_camel_case_name});
  {stream_headless_camel_case_name}ChunkOffset := 0;

  if ({stream_headless_camel_case_name}Length = 0) then begin
    FillChar({stream_headless_camel_case_name}ChunkData[0], SizeOf({chunk_data_type}) * {chunk_cardinality}, 0);
    {camel_case_name}LowLevel({parameters_low_level});
  end
  else begin
    streamMutex.Acquire;
    try
      while ({stream_headless_camel_case_name}ChunkOffset < Length({stream_headless_camel_case_name})) do begin
        {stream_headless_camel_case_name}ChunkLength := Length({stream_headless_camel_case_name}) - {stream_headless_camel_case_name}ChunkOffset;

        if ({stream_headless_camel_case_name}ChunkLength > {chunk_cardinality}) then {stream_headless_camel_case_name}ChunkLength := {chunk_cardinality};

        FillChar({stream_headless_camel_case_name}ChunkData[0], SizeOf({chunk_data_type}) * {stream_headless_camel_case_name}ChunkLength, 0);
        Move({stream_headless_camel_case_name}[Low({stream_headless_camel_case_name}) + {stream_headless_camel_case_name}ChunkOffset], {stream_headless_camel_case_name}ChunkData[0], SizeOf({chunk_data_type}) * {stream_headless_camel_case_name}ChunkLength);

        {camel_case_name}LowLevel({parameters_low_level});

        Inc({stream_headless_camel_case_name}ChunkOffset, {chunk_cardinality});
      end;
    finally
      streamMutex.Release;
    end;
  end;
end;

"""

                template_high_level_stream_in_fixed_length = """{method_signature}var {stream_headless_camel_case_name}ChunkOffset: word; {stream_headless_camel_case_name}ChunkData: TArray0To{chunk_cardinality_minus_1}Of{chunk_data_type_capitalized}; {stream_headless_camel_case_name}ChunkLength: word; {stream_headless_camel_case_name}Length: {stream_length_type};
begin
  {stream_headless_camel_case_name}Length := {fixed_length};
  {stream_headless_camel_case_name}ChunkOffset := 0;

  if (Length({stream_headless_camel_case_name}) <> {stream_headless_camel_case_name}Length) then begin
    raise EInvalidParameterException.Create(Format('{stream_name} has to be exactly %d items long', [{stream_headless_camel_case_name}Length]));
  end;

  streamMutex.Acquire;
  try
    while ({stream_headless_camel_case_name}ChunkOffset < {stream_headless_camel_case_name}Length) do begin
      {stream_headless_camel_case_name}ChunkLength := {stream_headless_camel_case_name}Length - {stream_headless_camel_case_name}ChunkOffset;

      if ({stream_headless_camel_case_name}ChunkLength > {chunk_cardinality}) then begin
        {stream_headless_camel_case_name}ChunkLength := {chunk_cardinality};
      end;

      FillChar({stream_headless_camel_case_name}ChunkData[0], SizeOf({chunk_data_type}) * {stream_headless_camel_case_name}ChunkLength, 0);
      Move({stream_headless_camel_case_name}[Low({stream_headless_camel_case_name}) + {stream_headless_camel_case_name}ChunkOffset], {stream_headless_camel_case_name}ChunkData[0], SizeOf({chunk_data_type}) * {stream_headless_camel_case_name}ChunkLength);

      {camel_case_name}LowLevel({parameters_low_level});

      Inc({stream_headless_camel_case_name}ChunkOffset, {chunk_cardinality});
    end;
  finally
    streamMutex.Release;
  end;
end;

"""

                template_high_level_stream_in_short_write = """{method_signature}var {stream_headless_camel_case_name}Length: {stream_length_type}; {stream_headless_camel_case_name}ChunkOffset: {stream_length_type}; {stream_headless_camel_case_name}ChunkLength: {stream_length_type}; {stream_headless_camel_case_name}ChunkWritten: {stream_length_type}; {stream_headless_camel_case_name}ChunkData: TArray0To{chunk_cardinality_minus_1}Of{chunk_data_type_capitalized};
begin
  result := 0;

  if (Length({stream_headless_camel_case_name}) > {stream_max_length}) then begin
    raise EInvalidParameterException.Create('{stream_name} can be at most {stream_max_length} items long');
  end;

  {stream_headless_camel_case_name}Length := Length({stream_headless_camel_case_name});
  {stream_headless_camel_case_name}ChunkOffset := 0;

  if ({stream_headless_camel_case_name}Length = 0) then begin
    FillChar({stream_headless_camel_case_name}ChunkData[0], SizeOf({chunk_data_type}) * {chunk_cardinality}, 0);
    result := {camel_case_name}LowLevel({parameters_low_level});
  end
  else begin
    streamMutex.Acquire;
    try
      while ({stream_headless_camel_case_name}ChunkOffset < Length({stream_headless_camel_case_name})) do begin
        {stream_headless_camel_case_name}ChunkLength := Length({stream_headless_camel_case_name}) - {stream_headless_camel_case_name}ChunkOffset;

        if ({stream_headless_camel_case_name}ChunkLength > {chunk_cardinality}) then {stream_headless_camel_case_name}ChunkLength := {chunk_cardinality};

        FillChar({stream_headless_camel_case_name}ChunkData[0], SizeOf({chunk_data_type}) * {stream_headless_camel_case_name}ChunkLength, 0);
        Move({stream_headless_camel_case_name}[Low({stream_headless_camel_case_name}) + {stream_headless_camel_case_name}ChunkOffset], {stream_headless_camel_case_name}ChunkData[0], SizeOf({chunk_data_type}) * {stream_headless_camel_case_name}ChunkLength);

        {stream_headless_camel_case_name}ChunkWritten := {camel_case_name}LowLevel({parameters_low_level});

        if ({stream_headless_camel_case_name}ChunkWritten <= 0) then break;

        Inc(result, {stream_headless_camel_case_name}ChunkWritten);

        if ({stream_headless_camel_case_name}ChunkWritten < {chunk_cardinality}) then break; {{ either last chunk or short write }}

        Inc({stream_headless_camel_case_name}ChunkOffset, {chunk_cardinality});
      end;
    finally
      streamMutex.Release;
    end;
  end;
end;

"""

                template_high_level_stream_in_single_chunk = """{method_signature}var {stream_headless_camel_case_name}Data: TArray0To{chunk_cardinality_minus_1}Of{chunk_data_type_capitalized};
begin

  if (Length({stream_headless_camel_case_name}) > {chunk_cardinality}) then begin
    raise EInvalidParameterException.Create('{stream_name} can be at most {chunk_cardinality} items long');
  end;

  FillChar({stream_headless_camel_case_name}Data[0], SizeOf({chunk_data_type}) * Length({stream_headless_camel_case_name}), 0);
  Move({stream_headless_camel_case_name}[Low({stream_headless_camel_case_name})], {stream_headless_camel_case_name}Data[0], SizeOf({chunk_data_type}) * Length({stream_headless_camel_case_name}));

  {camel_case_name}LowLevel({parameters_low_level});
end;

"""

                template_high_level_stream_in_short_write_single_chunk = """{method_signature}var {stream_headless_camel_case_name}Data: TArray0To{chunk_cardinality_minus_1}Of{chunk_data_type_capitalized};
begin
  result := 0;

  if (Length({stream_headless_camel_case_name}) > {chunk_cardinality}) then begin
    raise EInvalidParameterException.Create('{stream_name} can be at most {chunk_cardinality} items long');
  end;

  FillChar({stream_headless_camel_case_name}Data[0], SizeOf({chunk_data_type}) * Length({stream_headless_camel_case_name}), 0);
  Move({stream_headless_camel_case_name}[Low({stream_headless_camel_case_name})], {stream_headless_camel_case_name}Data[0], SizeOf({chunk_data_type}) * Length({stream_headless_camel_case_name}));

  result := {camel_case_name}LowLevel({parameters_low_level});
end;

"""

                template_stream_out_chunk_offset_check = """

  if ({stream_headless_camel_case_name}ChunkOffset = {chunk_max_offset}) then exit; {{ maximum chunk offset -> stream has no data }}"""

                template_high_level_stream_out = """{method_signature}var streamOutCurrentLength: integer; {stream_headless_camel_case_name}Length: {stream_length_type}; {stream_headless_camel_case_name}ChunkOffset: {stream_length_type}; {stream_headless_camel_case_name}ChunkData: TArray0To{chunk_cardinality_minus_1}Of{chunk_data_type_capitalized}; {stream_headless_camel_case_name}OutOfSync: boolean; {stream_headless_camel_case_name}ChunkLength: {stream_length_type};
begin
  streamMutex.Acquire;
  try
    streamOutCurrentLength := 0;
    {stream_headless_camel_case_name}Length := {fixed_length};
    {camel_case_name}LowLevel({parameters_low_level});
    if ({stream_headless_camel_case_name}Length <= 0) then exit;{chunk_offset_check}
    {stream_headless_camel_case_name}OutOfSync := ({stream_headless_camel_case_name}ChunkOffset <> 0);

    if not {stream_headless_camel_case_name}OutOfSync then begin
      SetLength({stream_headless_camel_case_name}, {stream_headless_camel_case_name}Length);
      {stream_headless_camel_case_name}ChunkLength := {stream_headless_camel_case_name}Length - {stream_headless_camel_case_name}ChunkOffset;
      if ({stream_headless_camel_case_name}ChunkLength > {chunk_cardinality}) then {stream_headless_camel_case_name}ChunkLength := {chunk_cardinality};
      Move({stream_headless_camel_case_name}ChunkData, {stream_headless_camel_case_name}[streamOutCurrentLength], SizeOf({chunk_data_type}) * {stream_headless_camel_case_name}ChunkLength);
      streamOutCurrentLength := {stream_headless_camel_case_name}ChunkLength;

      while (streamOutCurrentLength < {stream_headless_camel_case_name}Length) do begin
        {camel_case_name}LowLevel({parameters_low_level});
        if ({stream_headless_camel_case_name}Length <= 0) then exit;
        {stream_headless_camel_case_name}OutOfSync := {stream_headless_camel_case_name}ChunkOffset <> streamOutCurrentLength;
        if ({stream_headless_camel_case_name}OutOfSync) then break;
        {stream_headless_camel_case_name}ChunkLength := {stream_headless_camel_case_name}Length - {stream_headless_camel_case_name}ChunkOffset;
        if ({stream_headless_camel_case_name}ChunkLength > {chunk_cardinality}) then {stream_headless_camel_case_name}ChunkLength := {chunk_cardinality};
        Move({stream_headless_camel_case_name}ChunkData, {stream_headless_camel_case_name}[streamOutCurrentLength], SizeOf({chunk_data_type}) * {stream_headless_camel_case_name}ChunkLength);
        Inc(streamOutCurrentLength, {stream_headless_camel_case_name}ChunkLength);
      end;
    end;

    if ({stream_headless_camel_case_name}OutOfSync) then begin
      {{ discard remaining stream to bring it back in-sync }}
      SetLength({stream_headless_camel_case_name}, 0);

      while ({stream_headless_camel_case_name}ChunkOffset + {chunk_cardinality} < {stream_headless_camel_case_name}Length) do begin
        {camel_case_name}LowLevel({parameters_low_level});
        if ({stream_headless_camel_case_name}Length <= 0) then break;
      end;

      raise EStreamOutOfSyncException.Create('Stream out-of-sync');
    end;
  finally
    streamMutex.Release;
  end;
end;

"""

                template_high_level_stream_out_single_chunk = """{method_signature}var {stream_headless_camel_case_name}Length: {stream_length_type}; {stream_headless_camel_case_name}Data: TArray0To{chunk_cardinality_minus_1}Of{chunk_data_type_capitalized};
begin
  streamMutex.Acquire;
  try
    {camel_case_name}LowLevel({parameters_low_level});
    SetLength({stream_headless_camel_case_name}, {stream_headless_camel_case_name}Length);
    Move({stream_headless_camel_case_name}Data, {stream_headless_camel_case_name}[0], SizeOf({chunk_data_type}) * {stream_headless_camel_case_name}Length);
  finally
    streamMutex.Release;
  end;
end;

"""

                e_params = []
                chunk_data_type = ''
                stream_max_length = ''
                chunk_cardinality = ''
                stream_length_type = ''
                chunk_offset_check = ''
                parameters_low_level = []
                chunk_cardinality_minus_1 = ''
                chunk_data_type_capitalized = ''
                stream_name = ''
                stream_headless_camel_case_name = ''
                stream_in = packet.get_high_level('stream_in')
                stream_out = packet.get_high_level('stream_out')
                camel_case_name = packet.get_camel_case_name(skip=-2)
                name_high_level = packet.get_camel_case_name(skip=-2)

                for e in packet.get_elements():
                    e_param = ''
                    role = e.get_role()

                    if not (stream_in and ret_type != '' and e.get_direction() == 'out'):
                        parameters_low_level.append(e.get_headless_camel_case_name())

                    ret_type, e_param = self.get_high_level_method_parameters(e, ret_type, stream_in, stream_out)

                    if e_param != None:
                        e_params.append(e_param)

                    if role and role.endswith('data'):
                        chunk_cardinality = str(e.get_cardinality())
                        chunk_cardinality_minus_1 = str(e.get_cardinality() - 1)
                        chunk_data_type = e.get_delphi_type()[0]
                        chunk_data_type_capitalized = e.get_delphi_type()[1]

                        if e.get_direction() == 'out':
                            stream_name = stream_out.get_name()
                            stream_headless_camel_case_name = stream_out.get_headless_camel_case_name()
                        elif e.get_direction() == 'in':
                            stream_name = stream_in.get_name()
                            stream_headless_camel_case_name = stream_in.get_headless_camel_case_name()

                if len(e_params) > 0:
                    params = '(' + '; '.join(e_params) + ')'
                else:
                    params = '()'

                if len(ret_type) > 0:
                    method_signature = function.format(cls, name_high_level, params, ret_type)
                else:
                    method_signature = procedure.format(cls, name_high_level, params)

                parameters_low_level = ', '.join(parameters_low_level)

                if stream_in:
                    fixed_length = str(stream_in.get_fixed_length(default='0'))
                    stream_max_length = str(abs(stream_in.get_data_element().get_cardinality()))
                    stream_length_type = self.get_fixed_stream_length_type(int(stream_max_length))

                    if stream_in.get_fixed_length() != None:
                        method = template_high_level_stream_in_fixed_length.format(method_signature = method_signature,
                                                                                   stream_name = stream_name,
                                                                                   stream_headless_camel_case_name = stream_headless_camel_case_name,
                                                                                   chunk_cardinality_minus_1 = chunk_cardinality_minus_1,
                                                                                   chunk_data_type_capitalized = chunk_data_type_capitalized,
                                                                                   stream_length_type = stream_length_type,
                                                                                   fixed_length = str(stream_in.get_fixed_length()),
                                                                                   stream_max_length = stream_max_length,
                                                                                   chunk_cardinality = chunk_cardinality,
                                                                                   chunk_data_type = chunk_data_type,
                                                                                   camel_case_name = camel_case_name,
                                                                                   parameters_low_level = parameters_low_level)
                    elif stream_in.has_short_write() and stream_in.has_single_chunk():
                        method = template_high_level_stream_in_short_write_single_chunk.format(method_signature = method_signature,
                                                                                               stream_name = stream_name,
                                                                                               stream_headless_camel_case_name = stream_headless_camel_case_name,
                                                                                               chunk_cardinality_minus_1 = chunk_cardinality_minus_1,
                                                                                               chunk_data_type_capitalized = chunk_data_type_capitalized,
                                                                                               chunk_cardinality = chunk_cardinality,
                                                                                               stream_max_length = stream_max_length,
                                                                                               chunk_data_type = chunk_data_type,
                                                                                               camel_case_name = camel_case_name,
                                                                                               parameters_low_level = parameters_low_level)
                    elif stream_in.has_short_write():
                        method = template_high_level_stream_in_short_write.format(method_signature = method_signature,
                                                                                  stream_name = stream_name,
                                                                                  stream_headless_camel_case_name = stream_headless_camel_case_name,
                                                                                  stream_length_type = stream_length_type,
                                                                                  chunk_cardinality_minus_1 = chunk_cardinality_minus_1,
                                                                                  chunk_data_type_capitalized = chunk_data_type_capitalized,
                                                                                  stream_max_length = stream_max_length,
                                                                                  chunk_cardinality = chunk_cardinality,
                                                                                  chunk_data_type = chunk_data_type,
                                                                                  camel_case_name = camel_case_name,
                                                                                  parameters_low_level = parameters_low_level)
                    elif stream_in.has_single_chunk():
                        method = template_high_level_stream_in_single_chunk.format(method_signature = method_signature,
                                                                                   stream_name = stream_name,
                                                                                   stream_headless_camel_case_name = stream_headless_camel_case_name,
                                                                                   chunk_cardinality_minus_1 = chunk_cardinality_minus_1,
                                                                                   chunk_data_type_capitalized = chunk_data_type_capitalized,
                                                                                   chunk_cardinality = chunk_cardinality,
                                                                                   stream_max_length = stream_max_length,
                                                                                   chunk_data_type = chunk_data_type,
                                                                                   camel_case_name = camel_case_name,
                                                                                   parameters_low_level = parameters_low_level)
                    else:
                        method = template_high_level_stream_in.format(method_signature = method_signature,
                                                                      stream_name = stream_name,
                                                                      stream_headless_camel_case_name = stream_headless_camel_case_name,
                                                                      stream_length_type = stream_length_type,
                                                                      chunk_cardinality_minus_1 = chunk_cardinality_minus_1,
                                                                      chunk_data_type_capitalized = chunk_data_type_capitalized,
                                                                      stream_max_length = stream_max_length,
                                                                      chunk_cardinality = chunk_cardinality,
                                                                      chunk_data_type = chunk_data_type,
                                                                      camel_case_name = camel_case_name,
                                                                      parameters_low_level = parameters_low_level)

                elif stream_out:
                    fixed_length = str(stream_out.get_fixed_length(default='0'))
                    stream_length_type = self.get_fixed_stream_length_type(abs(stream_out.get_data_element().get_cardinality()))

                    if stream_out.get_fixed_length() != None:
                        chunk_offset_check = template_stream_out_chunk_offset_check.format(stream_headless_camel_case_name = stream_out.get_headless_camel_case_name(),
                                                                                           chunk_max_offset = str(abs(stream_out.get_data_element().get_cardinality())))

                    if stream_out.has_single_chunk():
                        method = template_high_level_stream_out_single_chunk.format(method_signature = method_signature,
                                                                                    stream_name = stream_name,
                                                                                    stream_headless_camel_case_name = stream_headless_camel_case_name,
                                                                                    stream_length_type = stream_length_type,
                                                                                    chunk_cardinality_minus_1 = chunk_cardinality_minus_1,
                                                                                    chunk_data_type_capitalized = chunk_data_type_capitalized,
                                                                                    camel_case_name = camel_case_name,
                                                                                    parameters_low_level = parameters_low_level,
                                                                                    chunk_data_type = chunk_data_type)
                    else:
                        method = template_high_level_stream_out.format(method_signature = method_signature,
                                                                       stream_name = stream_name,
                                                                       stream_headless_camel_case_name = stream_headless_camel_case_name,
                                                                       stream_length_type = stream_length_type,
                                                                       chunk_cardinality_minus_1 = chunk_cardinality_minus_1,
                                                                       chunk_data_type = chunk_data_type,
                                                                       chunk_data_type_capitalized = chunk_data_type_capitalized,
                                                                       fixed_length = fixed_length,
                                                                       camel_case_name = camel_case_name,
                                                                       parameters_low_level = parameters_low_level,
                                                                       chunk_offset_check = chunk_offset_check,
                                                                       chunk_cardinality = chunk_cardinality)

                methods += method

        return methods

    def get_delphi_callback_wrappers(self):
        wrappers = ''

        for packet in self.get_packets('callback'):
            wrapper = 'procedure {0}.CallbackWrapper{1}(const packet: TByteArray);\n'.format(self.get_delphi_class_name(),
                                                                                             packet.get_camel_case_name())

            variables = []

            if len(packet.get_elements(direction='out')) > 0:
                variables += packet.get_delphi_parameters(False, with_modifiers=False)

            has_array = False

            for element in packet.get_elements():
                if element.get_cardinality() > 1 and element.get_type() != 'string':
                    has_array = True
                    break

            stream_out = packet.get_high_level('stream_out')

            if stream_out != None and not stream_out.has_single_chunk():
                variables.append('{0}ChunkLength: {1}'.format(stream_out.get_headless_camel_case_name(),
                                                              self.get_fixed_stream_length_type(abs(stream_out.get_data_element().get_cardinality()))))

            if has_array:
                variables.append('i: longint')

            for element in packet.get_elements():
                if element.get_cardinality() > 1 and element.get_type() == 'bool':
                    variables.append('{0}Bits: array [0..{1}] of byte'.format(element.get_headless_camel_case_name(),
                                                                              int(math.ceil(element.get_cardinality() / 8.0) - 1)))

            wrapper += common.wrap_non_empty('var ', '; '.join(variables), ';\n')
            wrapper += 'begin\n'

            if len(packet.get_elements(direction='out')) == 0:
                wrapper += '  Assert(packet <> nil); { Avoid \'Parameter not used\' warning }\n'

            has_high_level_callback = False

            if packet.has_high_level():
                stream_out = packet.get_high_level('stream_out')

                if stream_out:
                    has_high_level_callback = True
                    wrapper += '  if (Assigned({0}Callback) or Assigned({1}Callback)) then begin\n' \
                               .format(packet.get_headless_camel_case_name(),
                                       packet.get_headless_camel_case_name(skip=-2))
                else:
                    wrapper += '  if (Assigned({0}Callback)) then begin\n'.format(packet.get_headless_camel_case_name())
            else:
                wrapper += '  if (Assigned({0}Callback)) then begin\n'.format(packet.get_headless_camel_case_name())

            offset = 8
            parameter_names = []

            wrapper_bool_array_fmt = '''    FillChar({0}[0], Length({0}) * SizeOf({0}[0]), 0);
    for i := 0 to {1} do {0}[i] := LEConvertUInt8From({2} + (i * 1), packet);
    for i := 0 to {3} do {4}[i] := (({0}[Floor(i / 8)] and (1 shl (i mod 8))) <> 0);
'''

            for element in packet.get_elements(direction='out'):
                parameter_names.append(element.get_headless_camel_case_name())

                if element.get_cardinality() > 1 and element.get_type() != 'string' and element.get_type() != 'bool':
                    prefix = 'for i := 0 to {0} do '.format(element.get_cardinality() - 1)
                    wrapper += '    {0}{1}[i] := LEConvert{2}From({3} + (i * {4}), packet);\n'.format(prefix,
                                                                                                      element.get_headless_camel_case_name(),
                                                                                                      element.get_delphi_le_convert_type(),
                                                                                                      offset,
                                                                                                      element.get_item_size())
                elif element.get_cardinality() > 1 and element.get_type() == 'bool':
                    wrapper += wrapper_bool_array_fmt.format(element.get_headless_camel_case_name() + 'Bits',
                                                             str(int(math.ceil(element.get_cardinality() / 8.0) - 1)),
                                                             offset,
                                                             element.get_cardinality() - 1,
                                                             element.get_headless_camel_case_name())
                else:
                    wrapper += '    {0} := LEConvert{1}From({2}, packet);\n'.format(element.get_headless_camel_case_name(),
                                                                                    element.get_delphi_le_convert_type(),
                                                                                    offset)

                offset += element.get_size()

            if stream_out != None:
                wrapper += '\n    if (Assigned({0}Callback)) then begin\n  '.format(packet.get_headless_camel_case_name())

            wrapper += '    {0}Callback({1});'.format(packet.get_headless_camel_case_name(),
                                                      ', '.join(['self'] + parameter_names))

            if stream_out != None:
                wrapper += '\n    end;'

            if has_high_level_callback:
                stream_out = packet.get_high_level('stream_out')

                if stream_out:
                    template_high_level_callback_stream_out = '''      {stream_headless_camel_case_name}ChunkLength := {stream_chunk_length_calc}
      if ({stream_headless_camel_case_name}ChunkLength > {chunk_cardinality}) then begin
        {stream_headless_camel_case_name}ChunkLength := {chunk_cardinality};
      end;

      if ({high_level_callback_name}HighLevelCallbackState.data = nil) then begin {{ no stream in-progress }}
        if ({stream_headless_camel_case_name}ChunkOffset = 0) then begin {{ stream starts }}
          SetLength({high_level_callback_name}HighLevelCallbackState.data, {stream_length});
          Move({stream_headless_camel_case_name}ChunkData[0], {high_level_callback_name}HighLevelCallbackState.data[{high_level_callback_name}HighLevelCallbackState.length], SizeOf({chunk_data_type}) * {stream_headless_camel_case_name}ChunkLength);
          {high_level_callback_name}HighLevelCallbackState.length := {stream_headless_camel_case_name}ChunkLength;

          if ({high_level_callback_name}HighLevelCallbackState.length >= {stream_length}) then begin {{ stream complete }}
            {high_level_callback_name}Callback({high_level_callback_parameters});
            SetLength({high_level_callback_name}HighLevelCallbackState.data, 0);
            {high_level_callback_name}HighLevelCallbackState.data := nil;
            {high_level_callback_name}HighLevelCallbackState.length := 0;
          end;
        end;
      end
      else begin {{ stream in-progress }}
        if ({stream_headless_camel_case_name}ChunkOffset <> {high_level_callback_name}HighLevelCallbackState.length) then begin {{ stream out-of-sync }}
          SetLength({high_level_callback_name}HighLevelCallbackState.data, 0);
          {high_level_callback_name}HighLevelCallbackState.data := nil;
          {high_level_callback_name}HighLevelCallbackState.length := 0;
          {high_level_callback_name}Callback({high_level_callback_parameters});
        end
        else begin {{ stream in-sync }}
          Move({stream_headless_camel_case_name}ChunkData[0], {high_level_callback_name}HighLevelCallbackState.data[{high_level_callback_name}HighLevelCallbackState.length], SizeOf({chunk_data_type}) * {stream_headless_camel_case_name}ChunkLength);
          Inc({high_level_callback_name}HighLevelCallbackState.length, {stream_headless_camel_case_name}ChunkLength);

          if {high_level_callback_name}HighLevelCallbackState.length >= {stream_length} then begin {{ stream complete }}
            {high_level_callback_name}Callback({high_level_callback_parameters});
            SetLength({high_level_callback_name}HighLevelCallbackState.data, 0);
            {high_level_callback_name}HighLevelCallbackState.data := nil;
            {high_level_callback_name}HighLevelCallbackState.length := 0;
          end;
        end;
      end;
'''

                    template_high_level_callback_stream_out_single_chunk = '''      SetLength({high_level_callback_name}HighLevelCallbackState.data, {stream_length});
      Move({stream_headless_camel_case_name}Data[0], {high_level_callback_name}HighLevelCallbackState.data[0], SizeOf({chunk_data_type}) * {stream_length});
      {high_level_callback_name}Callback({high_level_callback_parameters});
      SetLength({high_level_callback_name}HighLevelCallbackState.data, 0);
      {high_level_callback_name}HighLevelCallbackState.data := nil;
      {high_level_callback_name}HighLevelCallbackState.length := 0;
'''

                    high_level_callback_parameters = ['self']
                    high_level_callback_name = packet.get_headless_camel_case_name(skip=-2)

                    for element in packet.get_elements(direction='out'):
                        role = element.get_role()

                        if not role:
                            high_level_callback_parameters.append(element.get_headless_camel_case_name())
                            continue

                        if role.endswith('data'):
                            chunk_data_type = element.get_delphi_type()[0]
                            chunk_cardinality = element.get_cardinality()
                            stream_headless_camel_case_name = stream_out.get_headless_camel_case_name()

                            if stream_out.get_fixed_length():
                                stream_length = '{0}'.format(str(stream_out.get_fixed_length()))
                            else:
                                stream_length = '{0}Length'.format(stream_headless_camel_case_name)

                            high_level_callback_parameters.append('{0}HighLevelCallbackState.data'.format(high_level_callback_name))

                    if not stream_out.has_single_chunk():
                        if stream_out.get_fixed_length():
                            stream_chunk_length_calc = str(stream_out.get_fixed_length()) + ' - ' + stream_headless_camel_case_name + 'ChunkOffset;'
                        else:
                            stream_chunk_length_calc = stream_headless_camel_case_name + 'Length - ' + stream_headless_camel_case_name + 'ChunkOffset;'

                        wrapper_code = \
                            template_high_level_callback_stream_out.format(stream_headless_camel_case_name = stream_headless_camel_case_name,
                                                                           stream_chunk_length_calc = stream_chunk_length_calc,
                                                                           chunk_cardinality = chunk_cardinality,
                                                                           high_level_callback_name = high_level_callback_name,
                                                                           stream_length = stream_length,
                                                                           chunk_data_type = chunk_data_type,
                                                                           high_level_callback_parameters = ', '.join(high_level_callback_parameters))
                    else:
                        wrapper_code = \
                            template_high_level_callback_stream_out_single_chunk.format(high_level_callback_name = high_level_callback_name,
                                                                                        stream_length = stream_length,
                                                                                        stream_headless_camel_case_name = stream_headless_camel_case_name,
                                                                                        chunk_data_type = chunk_data_type,
                                                                                        high_level_callback_parameters = ', '.join(high_level_callback_parameters))

                    wrapper += '\n\n    if (Assigned({0}Callback)) then begin\n'.format(packet.get_headless_camel_case_name(skip=-2))
                    wrapper += wrapper_code
                    wrapper += '    end;\n'
                    wrapper += '  end;\n'
            else:
                wrapper += '\n  end;\n'

            wrapper += 'end;\n\n'

            wrappers += wrapper

        return wrappers + 'end.\n'

    def get_delphi_source(self):
        function_names = self.get_packet_names('function')
        callback_names = self.get_packet_names('callback')

        for callback_name in callback_names:
            if 'On ' + callback_name in function_names:
                raise common.GeneratorError("Generated callback name '[On ]{0}' collides with function name 'On {0}'".format(callback_name))

        source  = self.get_delphi_unit_header()
        source += self.get_delphi_device_identifier()
        source += self.get_delphi_device_display_name()
        source += self.get_delphi_function_id_definitions()
        source += self.get_delphi_callback_id_definitions()
        source += self.get_delphi_constants()
        source += self.get_delphi_arrays()
        source += self.get_delphi_callback_prototypes()
        source += self.get_delphi_class()
        source += self.get_delphi_constructor()
        source += self.get_delphi_callback_wrapper_definitions()
        source += self.get_delphi_methods()
        source += self.get_delphi_callback_wrappers()

        return source

class DelphiBindingsPacket(delphi_common.DelphiPacket):
    def get_delphi_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())

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
        text = self.get_device().specialize_delphi_doc_function_links(text)

        def format_parameter(name):
            return name # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return '\n    ///  '.join(text.strip().split('\n'))

class DelphiBindingsElement(delphi_common.DelphiElement):
    def _get_name(self): # for NameMixin
        name = common.Element._get_name(self)

        # avoid keywords
        if name.lower() in ['length', 'unit', 'type', 'message']:
            name += '2'

        return name

class DelphiBindingsGenerator(common.BindingsGenerator):
    def get_bindings_name(self):
        return 'delphi'

    def get_bindings_display_name(self):
        return 'Delphi/Lazarus'

    def get_device_class(self):
        return DelphiBindingsDevice

    def get_packet_class(self):
        return DelphiBindingsPacket

    def get_element_class(self):
        return DelphiBindingsElement

    def generate(self, device):
        filename = '{0}{1}.pas'.format(device.get_camel_case_category(), device.get_camel_case_name())

        with open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename), 'w') as f:
            f.write(device.get_delphi_source())

        if device.is_released():
            self.released_files.append(filename)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', DelphiBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
