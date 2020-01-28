#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Delphi/Lazarus Bindings Generator
Copyright (C) 2012-2015, 2017-2018, 2020 Matthias Bolte <matthias@tinkerforge.com>
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
                                                            packet.get_name(skip=-2 if high_level else 0).camel)
            else:
                return '<see cref="{0}.{1}.{2}"/>'.format(packet.get_device().get_delphi_class_name()[1:],
                                                          packet.get_device().get_delphi_class_name(),
                                                          packet.get_name(skip=-2 if high_level else 0).camel)

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
                               self.get_category().camel,
                               self.get_name().camel)

    def get_delphi_device_identifier(self):
        template = """const
  {0}_{1}_DEVICE_IDENTIFIER = {2};
"""

        return template.format(self.get_category().upper,
                               self.get_name().upper,
                               self.get_device_identifier())

    def get_delphi_device_display_name(self):
        template = """  {0}_{1}_DEVICE_DISPLAY_NAME = '{2}';

"""

        return template.format(self.get_category().upper,
                               self.get_name().upper,
                               self.get_long_display_name())

    def get_delphi_function_id_definitions(self):
        function_ids = ''
        template = '  {0}_{1}_FUNCTION_{2} = {3};\n'

        for packet in self.get_packets('function'):
            function_ids += template.format(self.get_category().upper,
                                            self.get_name().upper,
                                            packet.get_name().upper,
                                            packet.get_function_id())

        return function_ids + '\n'

    def get_delphi_constants(self):
        constant_format = '  {device_name}_{constant_group_name_upper}_{constant_name_upper} = {constant_value};\n'

        return self.get_formatted_constants(constant_format,
                                            bool_format_func=lambda value: str(value).lower(),
                                            device_name=self.get_category().upper + '_' + self.get_name().upper) + '\n'

    def get_delphi_callback_id_definitions(self):
        callback_ids = ''
        template = '  {0}_{1}_CALLBACK_{2} = {3};\n'

        for packet in self.get_packets('callback'):
            callback_ids += template.format(self.get_category().upper,
                                            self.get_name().upper,
                                            packet.get_name().upper,
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

            for element in packet.get_elements():
                if not packet.has_high_level() or \
                   element.get_type() == 'string' or \
                   element.get_cardinality() < 2:
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

                if role == None:
                    continue

                if role.endswith('length'):
                    callback_state_length_delphi_type = element.get_delphi_type()[0]

                if role.endswith('data'):
                    callback_state_data_delphi_type = element.get_delphi_type()[1]

                    if stream_out.get_fixed_length():
                        callback_state_length_delphi_type = self.get_fixed_stream_length_type(abs(stream_out.get_data_element().get_cardinality()))

            arrays += '  T{0}HighLevelCallbackState = record data: TArrayOf{1}; length: {2}; end;\n' \
                      .format(packet.get_name(skip=-2).camel,
                              callback_state_data_delphi_type,
                              callback_state_length_delphi_type)

        if has_high_level_callback_states:
            arrays += '\n'

        return arrays

    def get_delphi_callback_prototypes(self):
        prototypes = ''
        template = '  {0}Notify{1} = procedure(sender: {0}{2}) of object;\n'

        for packet in self.get_packets('callback'):
            params = common.wrap_non_empty('; ', '; '.join(packet.get_delphi_parameters('signature')), '')
            prototypes += template.format(self.get_delphi_class_name(),
                                          packet.get_name().camel,
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
                    high_level_parameters.append('const ' + element.get_name().headless + ': ' + element.get_delphi_type()[0])
                else:
                    if role.endswith('data'):
                        high_level_parameters.append('const ' + stream_out.get_name().headless + ': TArrayOf' + element.get_delphi_type()[1])

            params = '; '.join(high_level_parameters)

            if len(params) > 0:
                params = '; ' + params

            prototypes += template.format(self.get_delphi_class_name(),
                                          packet.get_name(skip=-2).camel,
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
            callbacks += template.format(packet.get_name().headless,
                                         self.get_delphi_class_name(),
                                         packet.get_name().camel)

            if not packet.has_high_level():
                continue

            stream_out = packet.get_high_level('stream_out')

            if not stream_out:
                continue

            callbacks += template.format(packet.get_name(skip=-2).headless,
                                         self.get_delphi_class_name(),
                                         packet.get_name(skip=-2).camel)

        callback_wrappers = ''
        template_wrapper = '    procedure CallbackWrapper{0}(const packet: TByteArray); {1};\n'

        for packet in self.get_packets('callback'):
            if packet.has_prototype_in_device():
                modifier = 'override'
            else:
                modifier = 'virtual'

            callback_wrappers += template_wrapper.format(packet.get_name().camel, modifier)

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
            output_count = len(packet.get_elements(direction='out'))
            name = packet.get_name().camel
            doc = packet.get_delphi_formatted_doc()
            ret_type = packet.get_delphi_return_type('signature')
            params = common.wrap_non_empty('(', '; '.join(packet.get_delphi_parameters('signature')), ')')

            if packet.has_prototype_in_device():
                modifier = 'override'
            else:
                modifier = 'virtual'

            if output_count == 1:
                method = function.format(name, params, ret_type, doc, modifier)
            else:
                method = procedure.format(name, params, doc, modifier)

            methods.append(method)

            if packet.has_high_level():
                e_params = []
                output_count = len(packet.get_elements(direction='out', high_level=True))
                name = packet.get_name(skip=-2).camel
                stream_in = packet.get_high_level('stream_in')
                stream_out = packet.get_high_level('stream_out')

                for e in packet.get_elements():
                    e_param = None
                    ret_type, e_param = self.get_high_level_method_parameter(e,
                                                                             ret_type,
                                                                             stream_in,
                                                                             stream_out,
                                                                             output_count)

                    if e_param:
                        e_params.append(e_param)

                if len(e_params) > 0:
                    params = '(' + '; '.join(e_params) + ')'
                else:
                    params = ''

                if output_count == 1:
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
            if packet.has_high_level():
                doc = '<see cref="{}.{}.On{}"/>'.format(self.get_delphi_class_name()[1:],
                                                              self.get_delphi_class_name(),
                                                              packet.get_name(skip=-2).camel)
            else:
                doc = packet.get_delphi_formatted_doc()

            props.append(prop.format(packet.get_name().camel,
                                     self.get_delphi_class_name(),
                                     packet.get_name().headless,
                                     doc))

            stream_out = packet.get_high_level('stream_out')

            if stream_out == None:
                continue

            high_level_callback_data_variables += \
                '    {0}HighLevelCallbackState: T{1}HighLevelCallbackState;\n'.format(packet.get_name(skip=-2).headless,
                                                                                      packet.get_name(skip=-2).camel)

            props.append(prop.format(packet.get_name(skip=-2).camel,
                                     self.get_delphi_class_name(),
                                     packet.get_name(skip=-2).headless,
                                     packet.get_delphi_formatted_doc()))

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
                '    constructor Create(const uid: string; ipcon_: TIPConnection);\n\n' + \
                '\n\n'.join(methods + props) + '\n' + \
                '  end;\n\n'

    def get_delphi_constructor(self):
        con = """implementation

constructor {0}.Create(const uid: string; ipcon_: TIPConnection);
begin
  inherited Create(uid, ipcon_, {1}_{2}_DEVICE_IDENTIFIER, {1}_{2}_DEVICE_DISPLAY_NAME);
  apiVersion[0] := {3};
  apiVersion[1] := {4};
  apiVersion[2] := {5};

"""
        stream_mutex = ''
        response_expected = ''

        for packet in self.get_packets('function'):
            if packet.has_high_level():
                stream_mutex = '  streamMutex := TCriticalSection.Create;\n\n'

            response_expected += '  responseExpected[{0}_{1}_FUNCTION_{2}] := DEVICE_RESPONSE_EXPECTED_{3};\n' \
                                 .format(self.get_category().upper,
                                         self.get_name().upper,
                                         packet.get_name().upper,
                                         packet.get_response_expected().upper())

        if len(response_expected) > 0:
            response_expected += '\n'

        high_level_callback_state = ''

        for packet in self.get_packets('callback'):
            if not packet.has_high_level():
                continue

            stream_mutex = '  streamMutex := TCriticalSection.Create;\n\n'
            stream_out = packet.get_high_level('stream_out')

            if not stream_out:
                continue

            high_level_callback_state += \
                '  SetLength({0}HighLevelCallbackState.data, 0);\n\
  {0}HighLevelCallbackState.data := nil;\n\
  {0}HighLevelCallbackState.length := 0;\n\n'.format(packet.get_name(skip=-2).headless)

        return con.format(self.get_delphi_class_name(),
                          self.get_category().upper,
                          self.get_name().upper,
                          *self.get_api_version()) + response_expected + stream_mutex + high_level_callback_state

    def get_delphi_callback_wrapper_definitions(self):
        callbacks = ''
        template = '  callbackWrappers[{0}_{1}_CALLBACK_{2}] := {{$ifdef FPC}}@{{$endif}}CallbackWrapper{3};\n'

        for packet in self.get_packets('callback'):
            callbacks += template.format(self.get_category().upper,
                                         self.get_name().upper,
                                         packet.get_name().upper,
                                         packet.get_name().camel)

        return callbacks + '\n  (ipcon as TIPConnection).AddDevice(self);\nend;\n\n'

    def get_high_level_method_parameter(self, e, ret_type, stream_in, stream_out, output_count):
        e_param = None

        if not e:
            return ret_type, e_param

        role = e.get_role()

        if stream_in:
            if output_count == 1:
                if e.get_direction() == 'out' and role and role.endswith('written'):
                    ret_type = 'word'
                else:
                    if e.get_direction() == 'out' and e.get_cardinality() > 1:
                        ret_type = 'TArrayOf' + e.get_delphi_type()[1]

                if e.get_direction() == 'in':
                    if role:
                        if stream_in.has_short_write() and role.endswith('length'):
                            ret_type = e.get_delphi_type()[0]

                        if role.endswith('data'):
                            if e.get_cardinality() > 1:
                                e_param = 'const ' + stream_in.get_name().headless + ': array of ' + e.get_delphi_type()[0]
                            else:
                                e_param = 'const ' + stream_in.get_name().headless + ': ' + e.get_delphi_type()[0]
                    else:
                        if e.get_cardinality() > 1:
                            e_param = 'const ' + e.get_name().headless + ': array of ' + e.get_delphi_type()[0]
                        else:
                            e_param = 'const ' + e.get_name().headless + ': ' + e.get_delphi_type()[0]
            else:
                if e.get_direction() == 'out':
                    if role and role.endswith('written'):
                        e_param = 'out ' + stream_in.get_name().headless + 'Written: word'
                    else:
                        if e.get_cardinality() > 1:
                            e_param = 'out ' + e.get_name().headless + ': array of ' + e.get_delphi_type()[0]
                        else:
                            e_param = 'out ' + e.get_name().headless + ': ' + e.get_delphi_type()[0]
                elif e.get_direction() == 'in':
                    if role:
                        if stream_in.has_short_write() and role.endswith('length'):
                            ret_type = e.get_delphi_type()[0]

                        if role.endswith('data'):
                            if e.get_cardinality() > 1:
                                e_param = 'const ' + stream_in.get_name().headless + ': array of ' + e.get_delphi_type()[0]
                            else:
                                e_param = 'const ' + stream_in.get_name().headless + ': ' + e.get_delphi_type()[0]
                    else:
                        if e.get_cardinality() > 1:
                            e_param = 'const ' + e.get_name().headless + ': array of ' + e.get_delphi_type()[0]
                        else:
                            e_param = 'const ' + e.get_name().headless + ': ' + e.get_delphi_type()[0]

        elif stream_out:
            if output_count == 1:
                if e.get_direction() == 'out' and e.get_cardinality() > 1:
                    ret_type = 'TArrayOf' + e.get_delphi_type()[1]

                if e.get_direction() == 'in':
                    if e.get_cardinality() > 1:
                        e_param = 'const ' + e.get_name().headless + ': TArrayOf' + e.get_delphi_type()[1]
                    else:
                        e_param = 'const ' + e.get_name().headless + ': ' + e.get_delphi_type()[0]
            else:
                if e.get_direction() == 'out':
                    if role:
                        if role.endswith('data'):
                            if e.get_cardinality() > 1:
                                e_param = 'out ' + stream_out.get_name().headless + ': TArrayOf' + e.get_delphi_type()[1]
                            else:
                                e_param = 'out ' + stream_out.get_name().headless + ': ' + e.get_delphi_type()[0]
                    else:
                        if e.get_cardinality() > 1:
                            e_param = 'out ' + e.get_name().headless + ': TArrayOf' + e.get_delphi_type()[1]
                        else:
                            e_param = 'out ' + e.get_name().headless + ': ' + e.get_delphi_type()[0]
                elif e.get_direction() == 'in':
                    if e.get_cardinality() > 1:
                        e_param = 'const ' + e.get_name().headless + ': TArrayOf' + e.get_delphi_type()[1]
                    else:
                        e_param = 'const ' + e.get_name().headless + ': ' + e.get_delphi_type()[0]

        return ret_type, e_param

    def get_delphi_methods(self):
        methods = ''
        function = 'function {0}.{1}{2}: {3};\n'
        procedure = 'procedure {0}.{1}{2};\n'
        cls = self.get_delphi_class_name()

        for packet in self.get_packets('function'):
            name = packet.get_name().camel
            ret_type = packet.get_delphi_return_type('signature')
            out_count = len(packet.get_elements(direction='out'))
            params = common.wrap_non_empty('(', '; '.join(packet.get_delphi_parameters('signature')), ')')
            function_id = '{0}_{1}_FUNCTION_{2}'.format(self.get_category().upper,
                                                        self.get_name().upper,
                                                        packet.get_name().upper)

            if out_count == 1:
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
                    method += ' {0}Bits: array [0..{1}] of byte;'.format(element.get_name().headless,
                                                                         int(math.ceil(element.get_cardinality() / 8.0) - 1))

            method += '\n'
            method += 'begin\n'

            if function_id != 255: # <device>.GetIdentity
                method += '  CheckDeviceIdentifier;\n'

            method += '  request := (ipcon as TIPConnection).CreateRequestPacket(self, {0}, {1});\n'.format(function_id, packet.get_request_size())

            method_bool_array_fmt = """  FillChar({0}[0], Length({0}) * SizeOf({0}[0]), 0);
  for i := 0 to {1} do if {2}[i] then {0}[Floor(i/8)] := {0}[Floor(i/8)] or (1 shl (i mod 8));
  for i := 0 to {3} do LEConvertUInt8To({0}[i], {4} + (i * 1), request);
"""

            # Serialize request
            offset = 8

            for element in packet.get_elements(direction='in'):
                if element.get_cardinality() > 1 and element.get_type() != 'string' and element.get_level() != 'low':
                    method += "  if (Length({0}) <> {2}) then raise EInvalidParameterException.Create('{1} has to be exactly {2} items long');\n" \
                              .format(element.get_name().headless,
                                      element.get_name().space.rstrip('_'),
                                      element.get_cardinality())

                if element.get_cardinality() > 1 and element.get_type() != 'string' and element.get_type() != 'bool':
                    prefix = 'for i := 0 to Length({0}) - 1 do '.format(element.get_name().headless)
                    method += '  {0}LEConvert{1}To({2}[i], {3} + (i * {4}), request);\n'.format(prefix,
                                                                                                element.get_delphi_le_convert_type(),
                                                                                                element.get_name().headless,
                                                                                                offset,
                                                                                                element.get_item_size())
                elif element.get_cardinality() > 1 and element.get_type() == 'bool':
                    method += method_bool_array_fmt.format(element.get_name().headless + 'Bits',
                                                           element.get_cardinality() - 1,
                                                           element.get_name().headless,
                                                           str(int(math.ceil(element.get_cardinality() / 8.0) - 1)),
                                                           offset)
                elif element.get_type() == 'string':
                    method += '  LEConvertStringTo({0}, {1}, {2}, request);\n'.format(element.get_name().headless,
                                                                                      offset,
                                                                                      element.get_cardinality())

                else:
                    method += '  LEConvert{0}To({1}, {2}, request);\n'.format(element.get_delphi_le_convert_type(),
                                                                              element.get_name().headless,
                                                                              offset)

                offset += element.get_size()

            if out_count > 0:
                method += '  response := SendRequest(request);\n'
            else:
                method += '  SendRequest(request);\n'

            # Deserialize response
            offset = 8

            method_bool_array_fmt = """  FillChar({0}[0], Length({0}) * SizeOf({0}[0]), 0);
  for i := 0 to {1} do {0}[i] := LEConvertUInt8From({2} + (i * 1), response);
  for i := 0 to {3} do {4}[i] := (({0}[Floor(i / 8)] and (1 shl (i mod 8))) <> 0);
"""

            for element in packet.get_elements(direction='out'):
                if out_count > 1:
                    result = element.get_name().headless
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
                    method += method_bool_array_fmt.format(element.get_name().headless + 'Bits',
                                                           str(int(math.ceil(element.get_cardinality() / 8.0) - 1)),
                                                           offset,
                                                           element.get_cardinality() - 1,
                                                           result)
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
                # Following templates are used to ultimately
                # get "ll_function_call" and "ll_function_written_inc".
                template_ll_function_call_no_or_more_output_stream_in = """{camel_name}LowLevel({parameters_low_level});"""
                template_ll_function_call_one_output_written_stream_in = """{current_written_value_variable} := {camel_name}LowLevel({parameters_low_level});"""
                template_ll_function_call_inc_written_stream_in = """Inc({accumulated_written_value_variable}, {current_written_value_variable});"""

                template_high_level_stream_in = """{method_signature}var
  {stream_name_headless}ChunkOffset: {stream_length_type};
  {stream_name_headless}ChunkData: TArray0To{chunk_cardinality_minus_1}Of{chunk_data_type_capitalized};
  {stream_name_headless}ChunkLength: {stream_length_type};
  {stream_name_headless}Length: {stream_length_type};{ll_function_call_define_current_written_variables}
begin
  if (Length({stream_name_headless}) > {stream_max_length}) then begin
    raise EInvalidParameterException.Create('{stream_name_space} can be at most {stream_max_length} items long');
  end;

  {stream_name_headless}Length := Length({stream_name_headless});
  {stream_name_headless}ChunkOffset := 0;{ll_function_call_init_written_variables}

  if ({stream_name_headless}Length = 0) then begin
    FillChar({stream_name_headless}ChunkData[0], SizeOf({chunk_data_type}) * {chunk_cardinality}, 0);{ll_function_call_zero}
  end
  else begin
    streamMutex.Acquire;
    try
      while ({stream_name_headless}ChunkOffset < {stream_name_headless}Length) do begin
        {stream_name_headless}ChunkLength := {stream_name_headless}Length - {stream_name_headless}ChunkOffset;

        if ({stream_name_headless}ChunkLength > {chunk_cardinality}) then {stream_name_headless}ChunkLength := {chunk_cardinality};

        FillChar({stream_name_headless}ChunkData[0], SizeOf({chunk_data_type}) * {chunk_cardinality}, 0);
        Move({stream_name_headless}[{stream_name_headless}ChunkOffset], {stream_name_headless}ChunkData[0], SizeOf({chunk_data_type}) * {stream_name_headless}ChunkLength);{ll_function_call}
        Inc({stream_name_headless}ChunkOffset, {chunk_cardinality});{ll_function_written_inc}
      end;
    finally
      streamMutex.Release;
    end;
  end;
end;

"""

                template_high_level_stream_in_fixed_length = """{method_signature}var
  {stream_name_headless}ChunkOffset: word;
  {stream_name_headless}ChunkData: TArray0To{chunk_cardinality_minus_1}Of{chunk_data_type_capitalized};
  {stream_name_headless}ChunkLength: word;
  {stream_name_headless}Length: {stream_length_type};{ll_function_call_define_current_written_variables}
begin
  {stream_name_headless}Length := {fixed_length};
  {stream_name_headless}ChunkOffset := 0;{ll_function_call_init_written_variables}

  if (Length({stream_name_headless}) <> {stream_name_headless}Length) then begin
    raise EInvalidParameterException.Create(Format('{stream_name_space} has to be exactly %d items long', [{stream_name_headless}Length]));
  end;

  streamMutex.Acquire;
  try
    while ({stream_name_headless}ChunkOffset < {stream_name_headless}Length) do begin
      {stream_name_headless}ChunkLength := {stream_name_headless}Length - {stream_name_headless}ChunkOffset;

      if ({stream_name_headless}ChunkLength > {chunk_cardinality}) then begin
        {stream_name_headless}ChunkLength := {chunk_cardinality};
      end;

      FillChar({stream_name_headless}ChunkData[0], SizeOf({chunk_data_type}) * {chunk_cardinality}, 0);
      Move({stream_name_headless}[{stream_name_headless}ChunkOffset], {stream_name_headless}ChunkData[0], SizeOf({chunk_data_type}) * {stream_name_headless}ChunkLength);{ll_function_call}
      Inc({stream_name_headless}ChunkOffset, {chunk_cardinality});{ll_function_written_inc}
    end;
  finally
    streamMutex.Release;
  end;
end;

"""

                template_high_level_stream_in_short_write = """{method_signature}var
  {stream_name_headless}Length: {stream_length_type};
  {stream_name_headless}ChunkOffset: {stream_length_type};
  {stream_name_headless}ChunkLength: {stream_length_type};
  {stream_name_headless}ChunkData: TArray0To{chunk_cardinality_minus_1}Of{chunk_data_type_capitalized};{ll_function_call_define_current_written_variables}
begin
  if (Length({stream_name_headless}) > {stream_max_length}) then begin
    raise EInvalidParameterException.Create('{stream_name_space} can be at most {stream_max_length} items long');
  end;

  {stream_name_headless}Length := Length({stream_name_headless});
  {stream_name_headless}ChunkOffset := 0;{ll_function_call_init_written_variables}

  if ({stream_name_headless}Length = 0) then begin
    FillChar({stream_name_headless}ChunkData[0], SizeOf({chunk_data_type}) * {chunk_cardinality}, 0);{ll_function_call_zero}
  end
  else begin
    streamMutex.Acquire;
    try
      while ({stream_name_headless}ChunkOffset < {stream_name_headless}Length) do begin
        {stream_name_headless}ChunkLength := {stream_name_headless}Length - {stream_name_headless}ChunkOffset;

        if ({stream_name_headless}ChunkLength > {chunk_cardinality}) then {stream_name_headless}ChunkLength := {chunk_cardinality};

        FillChar({stream_name_headless}ChunkData[0], SizeOf({chunk_data_type}) * {chunk_cardinality}, 0);
        Move({stream_name_headless}[{stream_name_headless}ChunkOffset], {stream_name_headless}ChunkData[0], SizeOf({chunk_data_type}) * {stream_name_headless}ChunkLength);{ll_function_call}{ll_function_written_inc}

        if ({current_written_value_variable} < {chunk_cardinality}) then break; {{ Either last chunk or short write }}

        Inc({stream_name_headless}ChunkOffset, {chunk_cardinality});
      end;
    finally
      streamMutex.Release;
    end;
  end;
end;

"""

                template_high_level_stream_in_single_chunk = """{method_signature}var
  {stream_name_headless}Length: byte;
  {stream_name_headless}Data: TArray0To{chunk_cardinality_minus_1}Of{chunk_data_type_capitalized};{ll_function_call_define_current_written_variables}
begin{ll_function_call_init_written_variables}
  if (Length({stream_name_headless}) > {chunk_cardinality}) then begin
    raise EInvalidParameterException.Create('{stream_name_space} can be at most {chunk_cardinality} items long');
  end;

  {stream_name_headless}Length := Length({stream_name_headless});

  FillChar({stream_name_headless}Data[0], SizeOf({chunk_data_type}) * {chunk_cardinality}, 0);
  Move({stream_name_headless}[0], {stream_name_headless}Data[0], SizeOf({chunk_data_type}) * {stream_name_headless}Length);{ll_function_call}{ll_function_written_inc}
end;

"""

                template_high_level_stream_in_short_write_single_chunk = """{method_signature}var
  {stream_name_headless}Length: byte;
  {stream_name_headless}Data: TArray0To{chunk_cardinality_minus_1}Of{chunk_data_type_capitalized};{ll_function_call_define_current_written_variables}
begin{ll_function_call_init_written_variables}

  if (Length({stream_name_headless}) > {chunk_cardinality}) then begin
    raise EInvalidParameterException.Create('{stream_name_space} can be at most {chunk_cardinality} items long');
  end;

  {stream_name_headless}Length := Length({stream_name_headless});

  FillChar({stream_name_headless}Data[0], SizeOf({chunk_data_type}) * {chunk_cardinality}, 0);
  Move({stream_name_headless}[0], {stream_name_headless}Data[0], SizeOf({chunk_data_type}) * {stream_name_headless}Length);{ll_function_call}{ll_function_written_inc}
end;

"""

                template_stream_out_chunk_offset_check = """

    if ({stream_name_headless}ChunkOffset = ((1 shl {shift_size}) - 1)) then begin {{ Maximum chunk offset -> stream has no data }}
      SetLength({stream_name_headless}, 0);
      exit;
    end;
"""

                template_high_level_stream_out = """{method_signature}var{output_declaration}
  {stream_name_headless}CurrentLength: {stream_length_type};
  {stream_name_headless}Length: {stream_length_type};
  {stream_name_headless}ChunkOffset: {stream_length_type};
  {stream_name_headless}ChunkData: TArray0To{chunk_cardinality_minus_1}Of{chunk_data_type_capitalized};
  {stream_name_headless}OutOfSync: boolean;
  {stream_name_headless}ChunkLength: {stream_length_type};
begin{output_prepare}
  streamMutex.Acquire;
  try
    {stream_name_headless}Length := {fixed_length};
    {camel_name}LowLevel({parameters_low_level});
    SetLength({stream_name_headless}, {stream_name_headless}Length);{chunk_offset_check}
    {stream_name_headless}OutOfSync := ({stream_name_headless}ChunkOffset <> 0);

    if ((not {stream_name_headless}OutOfSync) and ({stream_name_headless}Length > 0)) then begin
      {stream_name_headless}ChunkLength := {stream_name_headless}Length - {stream_name_headless}ChunkOffset;
      if ({stream_name_headless}ChunkLength > {chunk_cardinality}) then {stream_name_headless}ChunkLength := {chunk_cardinality};
      Move({stream_name_headless}ChunkData, {stream_name_headless}[0], SizeOf({chunk_data_type}) * {stream_name_headless}ChunkLength);
      {stream_name_headless}CurrentLength := {stream_name_headless}ChunkLength;

      while ((not {stream_name_headless}OutOfSync) and ({stream_name_headless}CurrentLength < {stream_name_headless}Length)) do begin
        {camel_name}LowLevel({parameters_low_level});
        {stream_name_headless}OutOfSync := {stream_name_headless}ChunkOffset <> {stream_name_headless}CurrentLength;
        {stream_name_headless}ChunkLength := {stream_name_headless}Length - {stream_name_headless}ChunkOffset;
        if ({stream_name_headless}ChunkLength > {chunk_cardinality}) then {stream_name_headless}ChunkLength := {chunk_cardinality};
        Move({stream_name_headless}ChunkData, {stream_name_headless}[{stream_name_headless}CurrentLength], SizeOf({chunk_data_type}) * {stream_name_headless}ChunkLength);
        Inc({stream_name_headless}CurrentLength, {stream_name_headless}ChunkLength);
      end;
    end;

    if ({stream_name_headless}OutOfSync) then begin
      {{ Discard remaining stream to bring it back in-sync }}
      while ({stream_name_headless}ChunkOffset + {chunk_cardinality} < {stream_name_headless}Length) do begin
        {camel_name}LowLevel({parameters_low_level});
      end;

      raise EStreamOutOfSyncException.Create('{stream_name_space} stream out-of-sync');
    end;
  finally
    streamMutex.Release;
  end;{output_finish}
end;

"""

                template_high_level_stream_out_single_chunk = """{method_signature}var{output_declaration}
  {stream_name_headless}Length: {stream_length_type};
  {stream_name_headless}Data: TArray0To{chunk_cardinality_minus_1}Of{chunk_data_type_capitalized};
begin{output_prepare}
  {camel_name}LowLevel({parameters_low_level});
  SetLength({stream_name_headless}, {stream_name_headless}Length);
  Move({stream_name_headless}Data, {stream_name_headless}[0], SizeOf({chunk_data_type}) * {stream_name_headless}Length);{output_finish}
end;

"""

                e_params = []
                stream_name = ''
                output_count = len(packet.get_elements(direction='out', high_level=True))
                chunk_data_type = ''
                ll_function_call = ''
                stream_max_length = ''
                chunk_cardinality = ''
                stream_length_type = ''
                chunk_offset_check = ''
                parameters_low_level = []
                stream_in_output_count = 0
                ll_function_call_zero = ''
                no_output_stream_in = False
                ll_function_written_inc = ''
                chunk_cardinality_minus_1 = ''
                multi_output_stream_in = False
                single_output_stream_in = False
                chunk_data_type_capitalized = ''
                current_written_value_variable = ''
                stream_name_headless = ''
                accumulated_written_value_variable = ''
                written_with_multi_output_stream_in = False
                written_with_single_output_stream_in = False
                ll_function_call_init_written_variables = ''
                stream_in = packet.get_high_level('stream_in')
                stream_out = packet.get_high_level('stream_out')
                camel_name = packet.get_name(skip=-2).camel
                name_high_level = packet.get_name(skip=-2).camel
                ll_function_call_define_current_written_variables = ''

                if stream_in:
                    for e in packet.get_elements():
                        if e.get_direction() != 'out':
                            continue

                        stream_in_output_count += 1

                    if stream_in_output_count == 0:
                        no_output_stream_in = True
                    elif stream_in_output_count == 1:
                        single_output_stream_in = True
                    else:
                        multi_output_stream_in = True

                    for e in packet.get_elements():
                        if e.get_direction() != 'out':
                            continue

                        role = e.get_role()

                        if role and role.endswith('written'):
                            if single_output_stream_in:
                                written_with_single_output_stream_in = True

                                break
                            elif multi_output_stream_in:
                                written_with_multi_output_stream_in = True

                                break

                for e in packet.get_elements():
                    e_param = ''
                    role = e.get_role()

                    if stream_in:
                        if no_output_stream_in:
                            parameters_low_level.append(e.get_name().headless)
                        elif single_output_stream_in:
                            if e.get_direction() != 'out':
                                parameters_low_level.append(e.get_name().headless)
                        elif multi_output_stream_in:
                            if written_with_multi_output_stream_in and \
                               e.get_direction() == 'out' and \
                               role and \
                               role.endswith('written'):
                                    parameters_low_level.append(stream_in.get_name().headless + 'ChunkWritten')
                            else:
                                parameters_low_level.append(e.get_name().headless)
                    else:
                        parameters_low_level.append(e.get_name().headless)

                    ret_type, e_param = self.get_high_level_method_parameter(e,
                                                                             ret_type,
                                                                             stream_in,
                                                                             stream_out,
                                                                             output_count)

                    if e_param != None:
                        e_params.append(e_param)

                    if role and role.endswith('data'):
                        chunk_cardinality = str(e.get_cardinality())
                        chunk_cardinality_minus_1 = str(e.get_cardinality() - 1)
                        chunk_data_type = e.get_delphi_type()[0]
                        chunk_data_type_capitalized = e.get_delphi_type()[1]

                        if e.get_direction() == 'out':
                            stream_name_space = stream_out.get_name().space
                            stream_name_headless = stream_out.get_name().headless
                        elif e.get_direction() == 'in':
                            stream_name_space = stream_in.get_name().space
                            stream_name_headless = stream_in.get_name().headless

                    if stream_in and e.get_direction() == 'out':
                        if single_output_stream_in:
                            if written_with_single_output_stream_in:
                                if role and role.endswith('written'):
                                    current_written_value_variable = stream_name_headless + 'ChunkWritten'
                                    accumulated_written_value_variable = 'result'
                                    ll_function_call_define_current_written_variables += \
                                        '\n  ' + current_written_value_variable + ': ' + e.get_delphi_type()[0] + ';'
                                    ll_function_call_init_written_variables += '\n  result := 0;'
                            else:
                                accumulated_written_value_variable = 'result'
                                current_written_value_variable = 'result'
                        elif multi_output_stream_in:
                            if written_with_multi_output_stream_in:
                                if role and role.endswith('written'):
                                    if stream_in.has_single_chunk():
                                        current_written_value_variable = stream_name_headless + 'ChunkWritten'
                                    else:
                                        current_written_value_variable = e.get_name().headless

                                    accumulated_written_value_variable = stream_name_headless + 'Written'
                                    ll_function_call_define_current_written_variables += \
                                        '\n  ' + current_written_value_variable + ': ' + e.get_delphi_type()[0] + ';'
                                    ll_function_call_init_written_variables += \
                                        '\n  ' + accumulated_written_value_variable + ' := 0;'

                if len(e_params) > 0:
                    params = '(' + '; '.join(e_params) + ')'
                else:
                    params = ''

                if output_count == 1:
                    method_signature = function.format(cls, name_high_level, params, ret_type)
                else:
                    method_signature = procedure.format(cls, name_high_level, params)

                parameters_low_level = ', '.join(parameters_low_level)

                if no_output_stream_in:
                    ll_function_call_zero = '\n    '
                    ll_function_call_zero += \
                        template_ll_function_call_no_or_more_output_stream_in.format(camel_name = camel_name,
                                                                                     parameters_low_level = parameters_low_level)

                    if stream_in.get_fixed_length():
                        ll_function_call = '\n\n      '
                    elif stream_in.has_single_chunk():
                        ll_function_call = '\n\n  '
                    else:
                        ll_function_call = '\n\n        '

                    ll_function_call += \
                        template_ll_function_call_no_or_more_output_stream_in.format(camel_name = camel_name,
                                                                                     parameters_low_level = parameters_low_level)


                elif single_output_stream_in:
                    # Here we set current_written_value_variable = accumulated_written_value_variable
                    # so that the return value actually contains whatever the low-level
                    # function has returned.
                    ll_function_call_zero = '\n    '
                    ll_function_call_zero += \
                        template_ll_function_call_one_output_written_stream_in.format(current_written_value_variable = accumulated_written_value_variable,
                                                                                      camel_name = camel_name,
                                                                                      parameters_low_level = parameters_low_level)

                    if stream_in.get_fixed_length():
                        ll_function_call = '\n\n      '
                    elif stream_in.has_single_chunk():
                        ll_function_call = '\n\n  '
                    else:
                        ll_function_call = '\n\n        '

                    ll_function_call += \
                        template_ll_function_call_one_output_written_stream_in.format(current_written_value_variable = current_written_value_variable,
                                                                                      camel_name = camel_name,
                                                                                      parameters_low_level = parameters_low_level)

                    if written_with_single_output_stream_in:
                        if stream_in.has_short_write() and stream_in.has_single_chunk():
                            ll_function_written_inc = '\n  '
                        else:
                            ll_function_written_inc = '\n        '

                        ll_function_written_inc += \
                            template_ll_function_call_inc_written_stream_in.format(accumulated_written_value_variable = accumulated_written_value_variable,
                                                                                   current_written_value_variable = current_written_value_variable)
                elif multi_output_stream_in:
                    ll_function_call_zero = '\n    '
                    ll_function_call_zero += \
                        template_ll_function_call_no_or_more_output_stream_in.format(camel_name = camel_name,
                                                                                     parameters_low_level = parameters_low_level)

                    if stream_in.get_fixed_length():
                        ll_function_call = '\n\n      '
                    elif stream_in.has_single_chunk():
                        ll_function_call = '\n\n  '
                    else:
                        ll_function_call = '\n\n        '

                    ll_function_call += \
                        template_ll_function_call_no_or_more_output_stream_in.format(camel_name = camel_name,
                                                                                     parameters_low_level = parameters_low_level)

                    if written_with_multi_output_stream_in:
                        if stream_in.has_short_write() and stream_in.has_single_chunk():
                            ll_function_written_inc = '\n  '
                        else:
                            ll_function_written_inc = '\n        '

                        ll_function_written_inc += \
                            template_ll_function_call_inc_written_stream_in.format(accumulated_written_value_variable = accumulated_written_value_variable,
                                                                                   current_written_value_variable = current_written_value_variable)

                if stream_in:
                    fixed_length = str(stream_in.get_fixed_length(default='0'))
                    stream_max_length = str(abs(stream_in.get_data_element().get_cardinality()))
                    stream_length_type = self.get_fixed_stream_length_type(int(stream_max_length))

                    if stream_in.get_fixed_length() != None:
                        method = template_high_level_stream_in_fixed_length.format(method_signature = method_signature,
                                                                                   stream_name_space = stream_name_space,
                                                                                   stream_name_headless = stream_name_headless,
                                                                                   chunk_cardinality_minus_1 = chunk_cardinality_minus_1,
                                                                                   chunk_data_type_capitalized = chunk_data_type_capitalized,
                                                                                   stream_length_type = stream_length_type,
                                                                                   fixed_length = str(stream_in.get_fixed_length()),
                                                                                   stream_max_length = stream_max_length,
                                                                                   chunk_cardinality = chunk_cardinality,
                                                                                   chunk_data_type = chunk_data_type,
                                                                                   camel_name = camel_name,
                                                                                   parameters_low_level = parameters_low_level,
                                                                                   ll_function_call_define_current_written_variables = ll_function_call_define_current_written_variables,
                                                                                   ll_function_call_init_written_variables = ll_function_call_init_written_variables,
                                                                                   ll_function_call = ll_function_call,
                                                                                   ll_function_written_inc = ll_function_written_inc)
                    elif stream_in.has_short_write() and stream_in.has_single_chunk():
                        method = template_high_level_stream_in_short_write_single_chunk.format(method_signature = method_signature,
                                                                                               stream_name_space = stream_name_space,
                                                                                               stream_name_headless = stream_name_headless,
                                                                                               chunk_cardinality_minus_1 = chunk_cardinality_minus_1,
                                                                                               chunk_data_type_capitalized = chunk_data_type_capitalized,
                                                                                               chunk_cardinality = chunk_cardinality,
                                                                                               stream_max_length = stream_max_length,
                                                                                               chunk_data_type = chunk_data_type,
                                                                                               camel_name = camel_name,
                                                                                               parameters_low_level = parameters_low_level,
                                                                                               ll_function_call_define_current_written_variables = ll_function_call_define_current_written_variables,
                                                                                               ll_function_call_init_written_variables = ll_function_call_init_written_variables,
                                                                                               ll_function_call = ll_function_call,
                                                                                               ll_function_written_inc = ll_function_written_inc)
                    elif stream_in.has_short_write():
                        method = template_high_level_stream_in_short_write.format(method_signature = method_signature,
                                                                                  stream_name_space = stream_name_space,
                                                                                  stream_name_headless = stream_name_headless,
                                                                                  stream_length_type = stream_length_type,
                                                                                  chunk_cardinality_minus_1 = chunk_cardinality_minus_1,
                                                                                  chunk_data_type_capitalized = chunk_data_type_capitalized,
                                                                                  stream_max_length = stream_max_length,
                                                                                  chunk_cardinality = chunk_cardinality,
                                                                                  chunk_data_type = chunk_data_type,
                                                                                  camel_name = camel_name,
                                                                                  parameters_low_level = parameters_low_level,
                                                                                  ll_function_call_define_current_written_variables = ll_function_call_define_current_written_variables,
                                                                                  ll_function_call_init_written_variables = ll_function_call_init_written_variables,
                                                                                  ll_function_call_zero = ll_function_call_zero,
                                                                                  ll_function_call = ll_function_call,
                                                                                  current_written_value_variable = current_written_value_variable,
                                                                                  ll_function_written_inc = ll_function_written_inc)
                    elif stream_in.has_single_chunk():
                        method = template_high_level_stream_in_single_chunk.format(method_signature = method_signature,
                                                                                   stream_name_space = stream_name_space,
                                                                                   stream_name_headless = stream_name_headless,
                                                                                   chunk_cardinality_minus_1 = chunk_cardinality_minus_1,
                                                                                   chunk_data_type_capitalized = chunk_data_type_capitalized,
                                                                                   chunk_cardinality = chunk_cardinality,
                                                                                   stream_max_length = stream_max_length,
                                                                                   chunk_data_type = chunk_data_type,
                                                                                   camel_name = camel_name,
                                                                                   parameters_low_level = parameters_low_level,
                                                                                   ll_function_call_define_current_written_variables = ll_function_call_define_current_written_variables,
                                                                                   ll_function_call_init_written_variables = ll_function_call_init_written_variables,
                                                                                   ll_function_call = ll_function_call,
                                                                                   ll_function_written_inc = ll_function_written_inc)
                    else:
                        method = template_high_level_stream_in.format(method_signature = method_signature,
                                                                      stream_name_space = stream_name_space,
                                                                      stream_name_headless = stream_name_headless,
                                                                      stream_length_type = stream_length_type,
                                                                      chunk_cardinality_minus_1 = chunk_cardinality_minus_1,
                                                                      chunk_data_type_capitalized = chunk_data_type_capitalized,
                                                                      stream_max_length = stream_max_length,
                                                                      chunk_cardinality = chunk_cardinality,
                                                                      chunk_data_type = chunk_data_type,
                                                                      camel_name = camel_name,
                                                                      parameters_low_level = parameters_low_level,
                                                                      ll_function_call_define_current_written_variables = ll_function_call_define_current_written_variables,
                                                                      ll_function_call_init_written_variables = ll_function_call_init_written_variables,
                                                                      ll_function_call_zero = ll_function_call_zero,
                                                                      ll_function_call = ll_function_call,
                                                                      ll_function_written_inc = ll_function_written_inc)

                elif stream_out:
                    fixed_length = str(stream_out.get_fixed_length(default='0'))
                    stream_length_type = self.get_fixed_stream_length_type(abs(stream_out.get_data_element().get_cardinality()))

                    if stream_out.get_fixed_length() != None:
                        chunk_offset_check = template_stream_out_chunk_offset_check.format(stream_name_headless = stream_out.get_name().headless,
                                                                                           shift_size=int(stream_out.get_chunk_offset_element().get_type().replace('uint', '')))

                    if output_count == 1:
                        output_declaration = '\n  {0}: TArrayOf{1};'.format(stream_name_headless, chunk_data_type_capitalized)
                        output_prepare = '\n  SetLength(result, 0);\n  SetLength({0}, 0);'.format(stream_name_headless)
                        output_finish = '\n  result := {0};'.format(stream_name_headless)
                    else:
                        output_declaration = ''
                        output_prepare = ''
                        output_finish = ''

                    if stream_out.has_single_chunk():
                        method = template_high_level_stream_out_single_chunk.format(method_signature = method_signature,
                                                                                    stream_name_space = stream_name_space,
                                                                                    stream_name_headless = stream_name_headless,
                                                                                    stream_length_type = stream_length_type,
                                                                                    chunk_cardinality_minus_1 = chunk_cardinality_minus_1,
                                                                                    chunk_data_type_capitalized = chunk_data_type_capitalized,
                                                                                    camel_name = camel_name,
                                                                                    parameters_low_level = parameters_low_level,
                                                                                    chunk_data_type = chunk_data_type,
                                                                                    output_declaration = output_declaration,
                                                                                    output_prepare = output_prepare,
                                                                                    output_finish = output_finish)
                    else:
                        method = template_high_level_stream_out.format(method_signature = method_signature,
                                                                       stream_name_space = stream_name_space,
                                                                       stream_name_headless = stream_name_headless,
                                                                       stream_length_type = stream_length_type,
                                                                       chunk_cardinality_minus_1 = chunk_cardinality_minus_1,
                                                                       chunk_data_type = chunk_data_type,
                                                                       chunk_data_type_capitalized = chunk_data_type_capitalized,
                                                                       fixed_length = fixed_length,
                                                                       camel_name = camel_name,
                                                                       parameters_low_level = parameters_low_level,
                                                                       chunk_offset_check = chunk_offset_check,
                                                                       chunk_cardinality = chunk_cardinality,
                                                                       output_declaration = output_declaration,
                                                                       output_prepare = output_prepare,
                                                                       output_finish = output_finish)

                methods += method

        return methods

    def get_delphi_callback_wrappers(self):
        wrappers = ''

        for packet in self.get_packets('callback'):
            wrapper = 'procedure {0}.CallbackWrapper{1}(const packet: TByteArray);\n'.format(self.get_delphi_class_name(),
                                                                                             packet.get_name().camel)

            variables = []

            if len(packet.get_elements(direction='out')) > 0:
                variables += packet.get_delphi_parameters('variables')

            has_array = False

            for element in packet.get_elements():
                if element.get_cardinality() > 1 and element.get_type() != 'string':
                    has_array = True
                    break

            stream_out = packet.get_high_level('stream_out')

            if stream_out != None and not stream_out.has_single_chunk():
                variables.append('{0}ChunkLength: {1}'.format(stream_out.get_name().headless,
                                                              self.get_fixed_stream_length_type(abs(stream_out.get_data_element().get_cardinality()))))

            if has_array:
                variables.append('i: longint')

            for element in packet.get_elements():
                if element.get_cardinality() > 1 and element.get_type() == 'bool':
                    variables.append('{0}Bits: array [0..{1}] of byte'.format(element.get_name().headless,
                                                                              int(math.ceil(element.get_cardinality() / 8.0) - 1)))

            wrapper += common.wrap_non_empty('var ', '; '.join(variables), ';\n')
            wrapper += 'begin\n'

            if len(packet.get_elements(direction='out')) == 0:
                wrapper += '  Assert(packet <> nil); { Avoid \'Parameter not used\' warning }\n'

            has_high_level_callback = False

            if packet.has_high_level() and packet.get_high_level('stream_out'):
                has_high_level_callback = True

            offset = 8
            parameter_names = []

            wrapper_bool_array_fmt = '''  FillChar({0}[0], Length({0}) * SizeOf({0}[0]), 0);
  for i := 0 to {1} do {0}[i] := LEConvertUInt8From({2} + (i * 1), packet);
  for i := 0 to {3} do {4}[i] := (({0}[Floor(i / 8)] and (1 shl (i mod 8))) <> 0);
'''

            for element in packet.get_elements(direction='out'):
                parameter_names.append(element.get_name().headless)

                if element.get_cardinality() > 1 and element.get_type() != 'string' and element.get_type() != 'bool':
                    prefix = 'for i := 0 to {0} do '.format(element.get_cardinality() - 1)
                    wrapper += '  {0}{1}[i] := LEConvert{2}From({3} + (i * {4}), packet);\n'.format(prefix,
                                                                                                    element.get_name().headless,
                                                                                                    element.get_delphi_le_convert_type(),
                                                                                                    offset,
                                                                                                    element.get_item_size())
                elif element.get_cardinality() > 1 and element.get_type() == 'bool':
                    wrapper += wrapper_bool_array_fmt.format(element.get_name().headless + 'Bits',
                                                             str(int(math.ceil(element.get_cardinality() / 8.0) - 1)),
                                                             offset,
                                                             element.get_cardinality() - 1,
                                                             element.get_name().headless)
                elif element.get_type() == 'string':
                    wrapper += '  {0} := LEConvertStringFrom({1}, {2}, packet);\n'.format(element.get_name().headless,
                                                                                          offset,
                                                                                          element.get_cardinality())
                else:
                    wrapper += '  {0} := LEConvert{1}From({2}, packet);\n'.format(element.get_name().headless,
                                                                                  element.get_delphi_le_convert_type(),
                                                                                  offset)

                offset += element.get_size()

            if has_high_level_callback:
                stream_out = packet.get_high_level('stream_out')

                if stream_out:
                    template_high_level_callback_stream_out = '''
  {stream_name_headless}ChunkLength := {stream_chunk_length_calc}
  if ({stream_name_headless}ChunkLength > {chunk_cardinality}) then begin
    {stream_name_headless}ChunkLength := {chunk_cardinality};
  end;
  if ({high_level_callback_name}HighLevelCallbackState.data = nil) then begin {{ No stream in-progress }}
    if ({stream_name_headless}ChunkOffset = 0) then begin {{ Stream starts }}
      SetLength({high_level_callback_name}HighLevelCallbackState.data, {stream_length});
      Move({stream_name_headless}ChunkData[0], {high_level_callback_name}HighLevelCallbackState.data[0], SizeOf({chunk_data_type}) * {stream_name_headless}ChunkLength);
      {high_level_callback_name}HighLevelCallbackState.length := {stream_name_headless}ChunkLength;

      if ({high_level_callback_name}HighLevelCallbackState.length >= {stream_length}) then begin {{ Stream complete }}
        if (Assigned({high_level_callback_name}Callback)) then begin
          {high_level_callback_name}Callback({high_level_callback_parameters});
        end;
        SetLength({high_level_callback_name}HighLevelCallbackState.data, 0);
        {high_level_callback_name}HighLevelCallbackState.data := nil;
        {high_level_callback_name}HighLevelCallbackState.length := 0;
      end;
    end;
  end
  else begin {{ Stream in-progress }}
    if ({stream_name_headless}ChunkOffset <> {high_level_callback_name}HighLevelCallbackState.length) then begin {{ Stream out-of-sync }}
      SetLength({high_level_callback_name}HighLevelCallbackState.data, 0);
      {high_level_callback_name}HighLevelCallbackState.data := nil;
      {high_level_callback_name}HighLevelCallbackState.length := 0;
      if (Assigned({high_level_callback_name}Callback)) then begin
        {high_level_callback_name}Callback({high_level_callback_parameters});
      end;
    end
    else begin {{ Stream in-sync }}
      Move({stream_name_headless}ChunkData[0], {high_level_callback_name}HighLevelCallbackState.data[{high_level_callback_name}HighLevelCallbackState.length], SizeOf({chunk_data_type}) * {stream_name_headless}ChunkLength);
      Inc({high_level_callback_name}HighLevelCallbackState.length, {stream_name_headless}ChunkLength);

      if {high_level_callback_name}HighLevelCallbackState.length >= {stream_length} then begin {{ Stream complete }}
        if (Assigned({high_level_callback_name}Callback)) then begin
          {high_level_callback_name}Callback({high_level_callback_parameters});
        end;
        SetLength({high_level_callback_name}HighLevelCallbackState.data, 0);
        {high_level_callback_name}HighLevelCallbackState.data := nil;
        {high_level_callback_name}HighLevelCallbackState.length := 0;
      end;
    end;
  end;
'''

                    template_high_level_callback_stream_out_single_chunk = '''
  SetLength({high_level_callback_name}HighLevelCallbackState.data, {stream_length});
  Move({stream_name_headless}Data[0], {high_level_callback_name}HighLevelCallbackState.data[0], SizeOf({chunk_data_type}) * {stream_length});
  if (Assigned({high_level_callback_name}Callback)) then begin
    {high_level_callback_name}Callback({high_level_callback_parameters});
  end;
  SetLength({high_level_callback_name}HighLevelCallbackState.data, 0);
  {high_level_callback_name}HighLevelCallbackState.data := nil;
  {high_level_callback_name}HighLevelCallbackState.length := 0;
'''

                    high_level_callback_parameters = ['self']
                    high_level_callback_name = packet.get_name(skip=-2).headless

                    for element in packet.get_elements(direction='out'):
                        role = element.get_role()

                        if not role:
                            high_level_callback_parameters.append(element.get_name().headless)
                            continue

                        if role.endswith('data'):
                            chunk_data_type = element.get_delphi_type()[0]
                            chunk_cardinality = element.get_cardinality()
                            stream_name_headless = stream_out.get_name().headless

                            if stream_out.get_fixed_length():
                                stream_length = '{0}'.format(str(stream_out.get_fixed_length()))
                            else:
                                stream_length = '{0}Length'.format(stream_name_headless)

                            high_level_callback_parameters.append('{0}HighLevelCallbackState.data'.format(high_level_callback_name))

                    if not stream_out.has_single_chunk():
                        if stream_out.get_fixed_length():
                            stream_chunk_length_calc = str(stream_out.get_fixed_length()) + ' - ' + stream_name_headless + 'ChunkOffset;'
                        else:
                            stream_chunk_length_calc = stream_name_headless + 'Length - ' + stream_name_headless + 'ChunkOffset;'

                        wrapper_code = \
                            template_high_level_callback_stream_out.format(stream_name_headless = stream_name_headless,
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
                                                                                        stream_name_headless = stream_name_headless,
                                                                                        chunk_data_type = chunk_data_type,
                                                                                        high_level_callback_parameters = ', '.join(high_level_callback_parameters))

                    wrapper += wrapper_code

            wrapper += '\n  if (Assigned({0}Callback)) then begin\n  '.format(packet.get_name().headless)
            wrapper += '  {0}Callback({1});'.format(packet.get_name().headless,
                                                    ', '.join(['self'] + parameter_names))
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
    def get_name(self, *args, **kwargs):
        name = delphi_common.DelphiElement.get_name(self, *args, **kwargs)

        # avoid keywords, check as lower because Delphi is caseless
        if name.lower in ['length', 'unit', 'type', 'message']:
            name = delphi_common.DelphiElement.get_name(self, *args, suffix='_', **kwargs)

        return name

class DelphiBindingsGenerator(delphi_common.DelphiGeneratorTrait, common.BindingsGenerator):
    def get_device_class(self):
        return DelphiBindingsDevice

    def get_packet_class(self):
        return DelphiBindingsPacket

    def get_element_class(self):
        return DelphiBindingsElement

    def prepare(self):
        common.BindingsGenerator.prepare(self)

        self.device_display_names = []

    def generate(self, device):
        filename = '{0}{1}.pas'.format(device.get_category().camel, device.get_name().camel)

        with open(os.path.join(self.get_bindings_dir(), filename), 'w') as f:
            f.write(device.get_delphi_source())

        if device.is_released():
            self.device_display_names.append((device.get_device_identifier(), device.get_long_display_name()))
            self.released_files.append(filename)

    def finish(self):
        template = """{header}
unit DeviceDisplayNames;

{{$ifdef FPC}}{{$mode OBJFPC}}{{$H+}}{{$endif}}

interface

uses
  SysUtils;

function GetDeviceDisplayName(const deviceIdentifier: word): string;

implementation

function GetDeviceDisplayName(const deviceIdentifier: word): string;
begin
  case deviceIdentifier of
{cases}
  else result := 'Unknown Device [' + IntToStr(deviceIdentifier) + ']';
  end;
end;

end.
"""

        cases = []

        for device_identifier, device_display_name in sorted(self.device_display_names):
            cases.append("  {0}: result := '{1}';".format(device_identifier, device_display_name))

        with open(os.path.join(self.get_bindings_dir(), 'DeviceDisplayNames.pas'), 'w') as f:
            f.write(template.format(header=self.get_header_comment('curly'),
                                    cases='\n'.join(cases)))

        self.released_files.append('DeviceDisplayNames.pas')

        common.BindingsGenerator.finish(self)

def generate(root_dir):
    common.generate(root_dir, 'en', DelphiBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
