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

class DelphiBindingsDevice(delphi_common.DelphiDevice):
    def get_delphi_unit_header(self):
        include = """{0}
unit {1}{2};

{{$ifdef FPC}}{{$mode OBJFPC}}{{$H+}}{{$endif}}

interface

uses
  Device, IPConnection, LEConverter;

"""
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        version = common.get_changelog_version(self.get_generator().get_bindings_root_directory())

        return include.format(common.gen_text_curly.format(date, *version),
                              self.get_category(),
                              self.get_camel_case_name())

    def get_delphi_device_identifier(self):
        did = """const
  {0}_{1}_DEVICE_IDENTIFIER = {2};

"""

        return did.format(self.get_category().upper(),
                          self.get_upper_case_name(),
                          self.get_device_identifier())

    def get_delphi_function_id_definitions(self):
        function_ids = ''
        function_id = '  {0}_{1}_FUNCTION_{2} = {3};\n'
        for packet in self.get_packets('function'):
            function_ids += function_id.format(self.get_category().upper(),
                                               self.get_upper_case_name(),
                                               packet.get_upper_case_name(),
                                               packet.get_function_id())
        return function_ids + '\n'

    def get_delphi_constants(self):
        str_constants = ''
        str_constant = '  {0}_{1}_{2}_{3} = {4};\n'
        constants = self.get_constants()
        for constant in constants:
            for definition in constant.definitions:
                if constant.type == 'char':
                    value = "'{0}'".format(definition.value)
                else:
                    value = str(definition.value)

                str_constants += str_constant.format(self.get_category().upper(),
                                                     self.get_upper_case_name(),
                                                     constant.name_uppercase,
                                                     definition.name_uppercase,
                                                     value)
        return str_constants + '\n'

    def get_delphi_callback_id_definitions(self):
        cbs = ''
        cb = '  {0}_{1}_CALLBACK_{2} = {3};\n'
        for packet in self.get_packets('callback'):
            cbs += cb.format(self.get_category().upper(),
                             self.get_upper_case_name(),
                             packet.get_upper_case_name(),
                             packet.get_function_id())
        return cbs + '\n'

    def get_delphi_arrays(self):
        arrays = 'type\n'
        types = {}

        for packet in self.get_packets('function'):
            for element in packet.get_elements():
                if element.get_type() == 'string' or element.get_cardinality() < 2:
                    continue

                delphi_type = element.get_delphi_type()
                left = 'TArray0To{0}Of{1}'.format(element.get_cardinality() - 1, delphi_type[1])
                right = 'array [0..{0}] of {1}'.format(element.get_cardinality() - 1, delphi_type[0])
                types[left] = right

        if len(types) > 0:
            for left in types:
                arrays += '  {0} = {1};\n'.format(left, types[left])

            arrays += '\n'

        return arrays

    def get_delphi_callback_prototypes(self):
        prototypes = ''
        prototype = '  {0}Notify{1} = procedure(sender: {0}{2}) of object;\n'

        for packet in self.get_packets('callback'):
            params = packet.get_delphi_parameter_list(False)

            if len(params) > 0:
                params = '; ' + params

            prototypes += prototype.format(self.get_delphi_class_name(),
                                           packet.get_camel_case_name(),
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
""".format(self.get_delphi_class_name(), self.get_description())

        callbacks = ''
        callback = '    {0}Callback: {1}Notify{2};\n'
        for packet in self.get_packets('callback'):
            callbacks += callback.format(packet.get_headless_camel_case_name(),
                                         self.get_delphi_class_name(),
                                         packet.get_camel_case_name())

        callback_wrappers = ''
        callback_wrapper = '    procedure CallbackWrapper{0}(const packet: TByteArray); {1};\n'
        for packet in self.get_packets('callback'):
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
        for packet in self.get_packets('function'):
            ret_type = packet.get_delphi_return_type(False)
            name = packet.get_camel_case_name()
            doc = packet.get_delphi_formatted_doc()
            params = packet.get_delphi_parameter_list(False)
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
    ///  {3}
    /// </summary>
    property On{0}: {1}Notify{0} read {2}Callback write {2}Callback;"""
        for packet in self.get_packets('callback'):
            doc = packet.get_delphi_formatted_doc()
            props.append(prop.format(packet.get_camel_case_name(),
                                     self.get_delphi_class_name(),
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

        for packet in self.get_packets():
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
                .format(self.get_category().upper(),
                        self.get_upper_case_name(),
                        prefix,
                        packet.get_upper_case_name(),
                        flag)

        if len(response_expected) > 0:
            response_expected += '\n'

        return con.format(self.get_delphi_class_name(),
                          *self.get_api_version()) + response_expected

    def get_delphi_callback_wrapper_definitions(self):
        cbs = ''
        cb = '  callbackWrappers[{0}_{1}_CALLBACK_{2}] := {{$ifdef FPC}}@{{$endif}}CallbackWrapper{3};\n'
        cbs_end = 'end;\n\n'
        for packet in self.get_packets('callback'):
            cbs += cb.format(self.get_category().upper(),
                             self.get_upper_case_name(),
                             packet.get_upper_case_name(),
                             packet.get_camel_case_name())
        return cbs + cbs_end

    def get_delphi_methods(self):
        methods = ''
        function = 'function {0}.{1}{2}: {3};\n'
        procedure = 'procedure {0}.{1}{2};\n'

        cls = self.get_delphi_class_name()
        for packet in self.get_packets('function'):
            ret_type = packet.get_delphi_return_type(False)
            out_count = len(packet.get_elements('out'))
            name = packet.get_camel_case_name()
            params = packet.get_delphi_parameter_list(False)
            function_id = '{0}_{1}_FUNCTION_{2}'.format(self.get_category().upper(),
                                                        self.get_upper_case_name(),
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
                if element.get_cardinality() > 1 and element.get_type() != 'string':
                    has_array = True
                    break

            if has_array:
                method += ' i: longint;'

            method += '\n'
            method += 'begin\n'
            method += '  request := (ipcon as TIPConnection).CreateRequestPacket(self, {0}, {1});\n'.format(function_id, packet.get_request_size())

            # Serialize request
            offset = 8
            for element in packet.get_elements('in'):
                if element.get_cardinality() > 1 and element.get_type() != 'string':
                    prefix = 'for i := 0 to Length({0}) - 1 do '.format(element.get_headless_camel_case_name())
                    method += '  {0}LEConvert{1}To({2}[i], {3} + (i * {4}), request);\n'.format(prefix,
                                                                                                element.get_delphi_le_convert_type(),
                                                                                                element.get_headless_camel_case_name(),
                                                                                                offset,
                                                                                                element.get_item_size())
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
            for element in packet.get_elements('out'):
                if out_count > 1:
                    result = element.get_headless_camel_case_name()
                else:
                    result = 'result'

                if element.get_cardinality() > 1 and element.get_type() != 'string':
                    prefix = 'for i := 0 to {0} do '.format(element.get_cardinality() - 1)
                    method += '  {0}{1}[i] := LEConvert{2}From({3} + (i * {4}), response);\n'.format(prefix,
                                                                                                     result,
                                                                                                     element.get_delphi_le_convert_type(),
                                                                                                     offset,
                                                                                                     element.get_item_size())
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

        return methods

    def get_delphi_callback_wrappers(self):
        wrappers = ''

        for packet in self.get_packets('callback'):
            wrapper = 'procedure {0}.CallbackWrapper{1}(const packet: TByteArray);\n'.format(self.get_delphi_class_name(),
                                                                                             packet.get_camel_case_name())

            if len(packet.get_elements('out')) > 0:
                wrapper += 'var ' + packet.get_delphi_parameter_list(False, False) + ';\n'

            wrapper += 'begin\n'

            if len(packet.get_elements('out')) == 0:
                wrapper += '  Assert(packet <> nil); { Avoid \'Parameter not used\' warning }\n'

            wrapper += '  if (Assigned({0}Callback)) then begin\n'.format(packet.get_headless_camel_case_name())

            offset = 8
            parameter_names = []
            for element in packet.get_elements('out'):
                parameter_names.append(element.get_headless_camel_case_name())

                if element.get_cardinality() > 1 and element.get_type() != 'string':
                    prefix = 'for i := 0 to {0} do '.format(element.get_cardinality() - 1)
                    wrapper += '    {0}{1}[i] := LEConvert{2}From({3} + (i * {4}), packet);\n'.format(prefix,
                                                                                                      element.get_headless_camel_case_name(),
                                                                                                      element.get_delphi_le_convert_type(),
                                                                                                      offset,
                                                                                                      element.get_item_size())
                else:
                    wrapper += '    {0} := LEConvert{1}From({2}, packet);\n'.format(element.get_headless_camel_case_name(),
                                                                                    element.get_delphi_le_convert_type(),
                                                                                    offset)

                offset += element.get_size()

            wrapper += '    {0}Callback({1});\n'.format(packet.get_headless_camel_case_name(), ', '.join(['self'] + parameter_names))
            wrapper += '  end;\n'
            wrapper += 'end;\n\n'

            wrappers += wrapper

        return wrappers + 'end.\n'

    def get_delphi_source(self):
        source  = self.get_delphi_unit_header()
        source += self.get_delphi_device_identifier()
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
        text = common.select_lang(self.get_doc()[1])
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

        cls = self.get_device().get_camel_case_name()
        for other_packet in self.get_device().get_packets():
            name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
            name = other_packet.get_camel_case_name()
            name_right = link.format(self.get_device().get_category(), cls, name)

            text = text.replace(name_false, name_right)

        text = common.handle_rst_word(text)
        text = common.handle_rst_if(text, self.get_device())
        text += common.format_since_firmware(self.get_device(), self)

        return '\n    ///  '.join(text.strip().split('\n'))

class DelphiBindingsElement(delphi_common.DelphiElement):
    def get_underscore_name(self):
        name = common.Element.get_underscore_name(self)

        # length is a keyword in delphi
        if name == 'length':
            name += '2'

        return name

class DelphiBindingsGenerator(common.BindingsGenerator):
    def __init__(self, *args, **kwargs):
        common.BindingsGenerator.__init__(self, *args, **kwargs)

        self.released_files_name_prefix = 'delphi'

    def get_device_class(self):
        return DelphiBindingsDevice

    def get_packet_class(self):
        return DelphiBindingsPacket

    def get_element_class(self):
        return DelphiBindingsElement

    def generate(self, device):
        file_name = '{0}{1}.pas'.format(device.get_category(), device.get_camel_case_name())

        pas = open(os.path.join(self.get_bindings_root_directory(), 'bindings', file_name), 'wb')
        pas.write(device.get_delphi_source())
        pas.close()

        if device.is_released():
            self.released_files.append(file_name)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', DelphiBindingsGenerator, False)

if __name__ == "__main__":
    generate(os.getcwd())
