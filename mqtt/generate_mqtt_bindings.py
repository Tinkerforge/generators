#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MQTT Bindings Generator
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>

generate_mqtt_bindings.py: Generator for MQTT bindings

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
import mqtt_common

getter_patterns = []
setter_patterns = []
callback_patterns = []



class MQTTBindingsPacket(mqtt_common.MQTTPacket):
    def get_mqtt_format_list(self, direction):
        formats = []

        for element in self.get_elements(direction=direction):
            formats.append(element.get_mqtt_struct_format())

        return ' '.join(formats)

class MQTTBindingsDevice(mqtt_common.MQTTDevice):
    def get_mqtt_class(self):
        template = """
class {0}(Device):
"""

        return template.format(self.get_python_class_name())

    def get_mqtt_init_method(self):
        template = """
	def __init__(self, uid, ipcon):
		Device.__init__(self, uid, ipcon)

{0}
"""
        response_expected = []
        mapping = {'always_true': 1, 'true': 2, 'false': 3}

        for packet in self.get_packets('function'):
            response_expected.append('re[{0}] = {1}'.format(packet.get_function_id(),
                                                            mapping[packet.get_response_expected()]))

        if len(response_expected) > 0:
            return template.format('\t\tre = self.response_expected\n\t\t' + '; '.join(response_expected))
        else:
            return template.format('')

    def get_mqtt_function_map(self):
        template = "\tfunctions = {{\n\t\t{entries}\n\t}}\n"
        entries = []
        for packet in self.get_packets('function'):
            entries.append("'{mqtt_name}': FunctionInfo({id}, {arg_names}, {arg_types}, {arg_symbols}, '{payload_fmt}', {result_names}, {result_symbols}, '{response_fmt}')".format(
                 mqtt_name=packet.get_mqtt_name(), 
                 id=packet.get_function_id(),
                 arg_names=[elem.get_name().under for elem in packet.get_elements(direction='in')],
                 arg_types=[elem.get_mqtt_type() for elem in packet.get_elements(direction='in')],
                 arg_symbols=[elem.get_symbols() for elem in packet.get_elements(direction='in')],
                 result_names=[elem.get_name().under for elem in packet.get_elements(direction='out')],
                 result_symbols=[elem.get_symbols() for elem in packet.get_elements(direction='out')],
                 payload_fmt=packet.get_mqtt_format_list('in'),
                 response_fmt=packet.get_mqtt_format_list('out')))

            if packet.has_high_level():
                stream_in = packet.get_high_level('stream_in')
                stream_out = packet.get_high_level('stream_out')

                if stream_in == None and stream_out == None:
                    continue

                if stream_in != None:
                    direction = 'in'
                else:
                    direction = 'out'

                input_names = []
                input_types = []
                input_symbols = []
                high_level_roles_in = []
                low_level_roles_in = []

                for element in packet.get_elements(direction='in', high_level=True):
                    input_names.append('{0}'.format(element.get_name().under))
                    input_types.append(element.get_mqtt_type())
                    high_level_roles_in.append(element.get_role())                    
                    constant_group = element.get_constant_group()

                    symbols = {}

                    if constant_group != None:
                        for constant in constant_group.get_constants():
                            symbols[constant.get_value()] = constant.get_name().under

                    input_symbols.append(symbols)

                for element in packet.get_elements(direction='in'):
                    low_level_roles_in.append(element.get_role())

                output_names = []
                output_symbols = []
                high_level_roles_out = []
                low_level_roles_out = []

                for element in packet.get_elements(direction='out', high_level=True):
                    output_names.append('{0}'.format(element.get_name().dash))
                    high_level_roles_out.append(element.get_role())
                    constant_group = element.get_constant_group()

                    symbols = {}

                    if constant_group != None:
                        for constant in constant_group.get_constants():
                            symbols[constant.get_value()] =  constant.get_name().under

                    output_symbols.append(symbols)                   

                for element in packet.get_elements(direction='out'):
                    low_level_roles_out.append(element.get_role())

                if stream_in != None:
                    chunk_padding = stream_in.get_chunk_data_element().get_mqtt_default_item_value()
                    chunk_cardinality = stream_in.get_chunk_data_element().get_cardinality()

                    if stream_in.get_fixed_length() != None:
                        chunk_max_offset = (1 << int(stream_in.get_chunk_offset_element().get_type().replace('uint', ''))) - 1
                    else:
                        chunk_max_offset = None

                    short_write = stream_in.has_short_write()
                    single_read = False
                    fixed_length = stream_in.get_fixed_length()
                else:
                    chunk_padding = None
                    chunk_cardinality = stream_out.get_chunk_data_element().get_cardinality()

                    if stream_out.get_fixed_length() != None:
                        chunk_max_offset = (1 << int(stream_out.get_chunk_offset_element().get_type().replace('uint', ''))) - 1
                    else:
                        chunk_max_offset = None

                    short_write = False
                    single_read = stream_out.has_single_chunk()
                    fixed_length = stream_out.get_fixed_length()

                entries.append("'{mqtt_name}': HighLevelFunctionInfo({low_level_id}, '{direction}', {high_level_roles_in}, {high_level_roles_out}, {low_level_roles_in}, {low_level_roles_out}, {arg_names}, {arg_types}, {arg_symbols}, '{format_in}', {result_names}, {result_symbols}, '{format_out}',{chunk_padding}, {chunk_cardinality}, {chunk_max_offset},{short_write}, {single_read}, {fixed_length})".format(                    
                    mqtt_name=packet.get_mqtt_name(skip=-2), 
                    low_level_id=packet.get_function_id(),
                    direction=direction,
                    high_level_roles_in=high_level_roles_in,
                    high_level_roles_out=high_level_roles_out,
                    low_level_roles_in=low_level_roles_in,
                    low_level_roles_out=low_level_roles_out,
                    arg_names=input_names,
                    arg_types=input_types,
                    arg_symbols=input_symbols,
                    format_in=packet.get_mqtt_format_list('in'),
                    result_names=output_names,
                    result_symbols=output_symbols,
                    format_out=packet.get_mqtt_format_list('out'),
                    chunk_padding=chunk_padding,
                    chunk_cardinality=chunk_cardinality,
                    chunk_max_offset=chunk_max_offset,
                    short_write=short_write,
                    single_read=single_read,
                    fixed_length=fixed_length
                ))
        return template.format(entries = ",\n\t\t".join(entries))

    def get_mqtt_callback_map(self):
        template = "\tcallbacks = {{\n\t\t{entries}\n\t}}\n"
        entry_template = "'{mqtt_name}': CallbackInfo({id}, {names}, {symbols}, '{fmt}', {hl_info})"
        hl_template = "[{2}, {{'fixed_length': {0}, 'single_chunk': {1}}}, None]"

        entries = []

        for packet in self.get_packets('callback'):
            hl_info="None"
            callback_id=packet.get_function_id()
            stream = packet.get_high_level('stream_*')
            skip=0
            if stream != None:
                roles = []

                for element in packet.get_elements(direction='out'):
                    roles.append(element.get_role())                
                skip=-2
                hl_info = hl_template.format(stream.get_fixed_length(),
                                            stream.has_single_chunk(),
                                            repr(tuple(roles)))
            entries.append(entry_template.format(mqtt_name=packet.get_mqtt_name(skip),
                                                id=callback_id,
                                                names=[elem.get_name().under for elem in packet.get_elements(direction='out')],
                                                symbols=[elem.get_symbols() for elem in packet.get_elements(direction='out')],
                                                fmt=packet.get_mqtt_format_list('out'),
                                                hl_info=hl_info))
        return template.format(entries=",\n\t\t".join(entries))

#     def get_mqtt_functions(self):
#         template = """
# """
#         for packet in self.get_packets('function'):
#             template.format(fn_name=packet.get_python_name(),
#                             payload_fmt=packet.get_mqtt_format_list('in'),
#                             response_fmt=packet.get_mqtt_format_list('out'),



#     def get_mqtt_callback_formats(self):
#         callbacks = []
#         template = "cf[{0}] = '{1}'"

#         for packet in self.get_packets('callback'):
#             callbacks.append(template.format(packet.get_function_id(),
#                                              packet.get_mqtt_format_list('out')))

#         if len(callbacks) > 0:
#             return '\t\tcf = self.callback_formats\n\t\t' + '; '.join(callbacks) + '\n'
#         else:
#             return '\n'

#     def get_mqtt_high_level_callbacks(self):
#         high_level_callbacks = []
#         template = "hlc[{0}] = [{3}, {{'fixed_length': {1}, 'single_chunk': {2}}}, None]"

#         for packet in self.get_packets('callback'):
#             stream = packet.get_high_level('stream_*')

#             if stream != None:
#                 roles = []

#                 for element in packet.get_elements(direction='out'):
#                     roles.append(element.get_role())

#                 high_level_callbacks.append(template.format(-packet.get_function_id(),
#                                                             stream.get_fixed_length(),
#                                                             stream.has_single_chunk(),
#                                                             repr(tuple(roles))))

#         if len(high_level_callbacks) > 0:
#             return '\t\thlc = self.high_level_callbacks\n\t\t' + '; '.join(high_level_callbacks) + '\n'
#         else:
#             return '\n'

#     def get_mqtt_call_header(self):
#         template = """
# def call_{0}_{1}(ctx, argv):
# 	prog_prefix = 'call {2} <uid>'

# """

#         return template.format(self.get_name().under,
#                                self.get_category().under,
#                                self.get_mqtt_device_name())

#     def get_mqtt_call_functions(self):
#         functions = []
#         entries = []

#         template_setter = """	def {0}(ctx, argv):
# 		parser = ParserWithExpectResponse(ctx, prog_prefix + ' {1}')
# {2}
# 		args = parser.parse_args(argv)

# 		device_call(ctx, {7}{8}, {3}, ({4}), '{5}', '{6}', None, args.expect_response, [], [])
# """
#         template_getter = """	def {0}(ctx, argv):
# 		parser = ParserWithExecute(ctx, prog_prefix + ' {1}')
# {2}
# 		args = parser.parse_args(argv)

# 		device_call(ctx, {7}{8}, {3}, ({4}), '{5}', '{6}', args.execute, False, [{9}], [{10}])
# """
#         template_get_identity = """	def get_identity(ctx, argv):
# 		common_get_identity(ctx, prog_prefix, {0}, argv)
# """
#         template_stream_setter = """	def {name_under}(ctx, argv):
# 		parser = ParserWithExpectResponse(ctx, prog_prefix + ' {name_dash}')
# {params}
# 		args = parser.parse_args(argv)

# 		device_stream_call(ctx, {class_name}, {function_id}, '{direction}', ({request_data}), {high_level_roles_in}, {high_level_roles_out}, {low_level_roles_in}, {low_level_roles_out}, '{format_in}', '{format_out}', None, args.expect_response, [], [], {chunk_padding}, {chunk_cardinality}, {chunk_max_offset}, {short_write}, {single_read}, {fixed_length})
# """
#         template_stream_getter = """	def {name_under}(ctx, argv):
# 		parser = ParserWithExecute(ctx, prog_prefix + ' {name_dash}')
# {params}
# 		args = parser.parse_args(argv)

# 		device_stream_call(ctx, {class_name}, {function_id}, '{direction}', ({request_data}), {high_level_roles_in}, {high_level_roles_out}, {low_level_roles_in}, {low_level_roles_out}, '{format_in}', '{format_out}', args.execute, False, [{output_names}], [{output_symbols}], {chunk_padding}, {chunk_cardinality}, {chunk_max_offset}, {short_write}, {single_read}, {fixed_length})
# """

#         for packet in self.get_packets('function'):
#             # normal and low-level
#             name_under = packet.get_name().under
#             name_dash = packet.get_name().dash

#             if packet.get_function_id() == 255:
#                 function = template_get_identity.format(self.get_mqtt_class_name())
#             else:
#                 params = []
#                 request_data = []

#                 for element in packet.get_elements(direction='in'):
#                     name = element.get_name().under
#                     type_converter = element.get_mqtt_type_converter()
#                     help_ = element.get_mqtt_help()
#                     metavar = "'<{0}>'".format(element.get_name().dash)

#                     params.append("\t\tparser.add_argument('{0}', type={1}, help={2}, metavar={3})".format(name, type_converter, help_, metavar))
#                     request_data.append('args.{0}'.format(name))

#                 comma = ''

#                 if len(request_data) == 1:
#                     comma = ','

#                 if len(params) > 0:
#                     params = [''] + params + ['']

#                 output_names = []
#                 output_symbols = []

#                 for element in packet.get_elements(direction='out'):
#                     output_names.append("'{0}'".format(element.get_name().dash))

#                     constant_group = element.get_constant_group()

#                     if constant_group != None:
#                         symbols = {}

#                         for constant in constant_group.get_constants():
#                             symbols[constant.get_value()] = '{0}-{1}'.format(constant_group.get_name().dash, constant.get_name().dash)

#                         output_symbols.append(str(symbols))
#                     else:
#                         output_symbols.append('None')

#                 if len(output_names) > 0:
#                     if not name_under.startswith('get_') and \
#                        not name_under.startswith('is_') and \
#                        not name_under.startswith('are_'):
#                         getter_patterns.append(name_dash)

#                     function = template_getter.format(name_under,
#                                                       name_dash,
#                                                       '\n'.join(params),
#                                                       packet.get_function_id(),
#                                                       ', '.join(request_data) + comma,
#                                                       packet.get_mqtt_format_list('in'),
#                                                       packet.get_mqtt_format_list('out'),
#                                                       self.get_name().camel,
#                                                       self.get_category().camel,
#                                                       ', '.join(output_names),
#                                                       ', '.join(output_symbols))
#                 else:
#                     if not name_under.startswith('set_'):
#                         setter_patterns.append(name_dash)

#                     function = template_setter.format(name_under,
#                                                       name_dash,
#                                                       '\n'.join(params),
#                                                       packet.get_function_id(),
#                                                       ', '.join(request_data) + comma,
#                                                       packet.get_mqtt_format_list('in'),
#                                                       packet.get_mqtt_format_list('out'),
#                                                       self.get_name().camel,
#                                                       self.get_category().camel)

#             functions.append(function)
#             entries.append("'{0}': {1}".format(name_dash, name_under))

#             # high-level
#             stream_in = packet.get_high_level('stream_in')
#             stream_out = packet.get_high_level('stream_out')

#             if stream_in == None and stream_out == None:
#                 continue

#             if stream_in != None:
#                 direction = 'in'
#             else:
#                 direction = 'out'

#             params = []
#             request_data = []
#             high_level_roles_in = []
#             low_level_roles_in = []

#             for element in packet.get_elements(direction='in', high_level=True):
#                 name = element.get_name().under
#                 type_converter = element.get_mqtt_type_converter()
#                 help_ = element.get_mqtt_help()
#                 metavar = "'<{0}>'".format(element.get_name().dash)

#                 params.append("\t\tparser.add_argument('{0}', type={1}, help={2}, metavar={3})".format(name, type_converter, help_, metavar))
#                 request_data.append('args.{0}'.format(name))
#                 high_level_roles_in.append(element.get_role())

#             for element in packet.get_elements(direction='in'):
#                 low_level_roles_in.append(element.get_role())

#             comma = ''

#             if len(request_data) == 1:
#                 comma = ','

#             if len(params) > 0:
#                 params = [''] + params + ['']

#             output_names = []
#             output_symbols = []
#             high_level_roles_out = []
#             low_level_roles_out = []

#             for element in packet.get_elements(direction='out', high_level=True):
#                 output_names.append("'{0}'".format(element.get_name().dash))

#                 constant_group = element.get_constant_group()

#                 if constant_group != None:
#                     symbols = {}

#                     for constant in constant_group.get_constants():
#                         symbols[constant.get_value()] = '{0}-{1}'.format(constant_group.get_name().dash, constant.get_name().dash)

#                     output_symbols.append(str(symbols))
#                 else:
#                     output_symbols.append('None')

#                 high_level_roles_out.append(element.get_role())

#             for element in packet.get_elements(direction='out'):
#                 low_level_roles_out.append(element.get_role())

#             name_under = packet.get_name(skip=-2).under
#             name_dash = packet.get_name(skip=-2).dash

#             if stream_in != None:
#                 chunk_padding = stream_in.get_chunk_data_element().get_mqtt_default_item_value()
#                 chunk_cardinality = stream_in.get_chunk_data_element().get_cardinality()

#                 if stream_in.get_fixed_length() != None:
#                     chunk_max_offset = (1 << int(stream_in.get_chunk_offset_element().get_type().replace('uint', ''))) - 1
#                 else:
#                     chunk_max_offset = None

#                 short_write = stream_in.has_short_write()
#                 single_read = False
#                 fixed_length = stream_in.get_fixed_length()
#             else:
#                 chunk_padding = None
#                 chunk_cardinality = stream_out.get_chunk_data_element().get_cardinality()

#                 if stream_out.get_fixed_length() != None:
#                     chunk_max_offset = (1 << int(stream_out.get_chunk_offset_element().get_type().replace('uint', ''))) - 1
#                 else:
#                     chunk_max_offset = None

#                 short_write = False
#                 single_read = stream_out.has_single_chunk()
#                 fixed_length = stream_out.get_fixed_length()

#             if len(output_names) > 0:
#                 if not name_under.startswith('get_') and \
#                    not name_under.startswith('is_') and \
#                    not name_under.startswith('are_'):
#                     getter_patterns.append(name_dash)

#                 function = template_stream_getter.format(name_under=name_under,
#                                                          name_dash=name_dash,
#                                                          params='\n'.join(params),
#                                                          function_id=packet.get_function_id(),
#                                                          direction=direction,
#                                                          request_data=', '.join(request_data) + comma,
#                                                          high_level_roles_in=repr(tuple(high_level_roles_in)),
#                                                          high_level_roles_out=repr(tuple(high_level_roles_out)),
#                                                          low_level_roles_in=repr(tuple(low_level_roles_in)),
#                                                          low_level_roles_out=repr(tuple(low_level_roles_out)),
#                                                          format_in=packet.get_mqtt_format_list('in'),
#                                                          format_out=packet.get_mqtt_format_list('out'),
#                                                          class_name=self.get_name().camel + self.get_category().camel,
#                                                          output_names=', '.join(output_names),
#                                                          output_symbols=', '.join(output_symbols),
#                                                          chunk_padding=chunk_padding,
#                                                          chunk_cardinality=chunk_cardinality,
#                                                          chunk_max_offset=chunk_max_offset,
#                                                          short_write=short_write,
#                                                          single_read=single_read,
#                                                          fixed_length=fixed_length)
#             else:
#                 if not name_under.startswith('set_'):
#                     setter_patterns.append(name_dash)

#                 function = template_stream_setter.format(name_under=name_under,
#                                                          name_dash=name_dash,
#                                                          params='\n'.join(params),
#                                                          function_id=packet.get_function_id(),
#                                                          direction=direction,
#                                                          request_data=', '.join(request_data) + comma,
#                                                          high_level_roles_in=repr(tuple(high_level_roles_in)),
#                                                          high_level_roles_out=repr(tuple(high_level_roles_out)),
#                                                          low_level_roles_in=repr(tuple(low_level_roles_in)),
#                                                          low_level_roles_out=repr(tuple(low_level_roles_out)),
#                                                          format_in=packet.get_mqtt_format_list('in'),
#                                                          format_out=packet.get_mqtt_format_list('out'),
#                                                          class_name=self.get_name().camel + self.get_category().camel,
#                                                          chunk_padding=chunk_padding,
#                                                          chunk_cardinality=chunk_cardinality,
#                                                          chunk_max_offset=chunk_max_offset,
#                                                          short_write=short_write,
#                                                          single_read=single_read,
#                                                          fixed_length=fixed_length)

#             functions.append(function)
#             entries.append("'{0}': {1}".format(name_dash, name_under))

#         return '\n'.join(functions) + '\n\tfunctions = {\n\t' + ',\n\t'.join(entries) + '\n\t}'

#     def get_mqtt_call_footer(self):
#         template = """

# 	call_generic(ctx, '{0}', functions, argv)
# """

#         return template.format(self.get_mqtt_device_name())

#     def get_mqtt_dispatch_header(self):
#         template = """
# def dispatch_{0}_{1}(ctx, argv):
# 	prog_prefix = 'dispatch {2} <uid>'

# """

#         return template.format(self.get_name().under,
#                                self.get_category().under,
#                                self.get_mqtt_device_name())

#     def get_mqtt_dispatch_functions(self):
#         template = """	def {0}(ctx, argv):
# 		parser = ParserWithExecute(ctx, prog_prefix + ' {1}')

# 		args = parser.parse_args(argv)

# 		device_dispatch(ctx, {2}{3}, {4}, args.execute, [{5}], [{6}])
# """

#         functions = []
#         entries = []

#         for packet in self.get_packets('callback'):
#             # normal and low-level
#             output_names = []
#             output_symbols = []

#             for element in packet.get_elements(direction='out'):
#                 output_names.append("'{0}'".format(element.get_name().dash))

#                 constant_group = element.get_constant_group()

#                 if constant_group != None:
#                     symbols = {}

#                     for constant in constant_group.get_constants():
#                         symbols[constant.get_value()] = '{0}-{1}'.format(constant_group.get_name().dash, constant.get_name().dash)

#                     output_symbols.append(str(symbols))
#                 else:
#                     output_symbols.append('None')

#             name_under = packet.get_name().under
#             name_dash = packet.get_name().dash

#             function = template.format(name_under,
#                                        name_dash,
#                                        self.get_name().camel,
#                                        self.get_category().camel,
#                                        packet.get_function_id(),
#                                        ', '.join(output_names),
#                                        ', '.join(output_symbols))

#             entries.append("'{0}': {1}".format(name_dash,
#                                                name_under))

#             callback_patterns.append(name_dash)

#             functions.append(function)

#             # high-level
#             if packet.get_high_level('stream_*') == None:
#                 continue

#             output_names = []
#             output_symbols = []

#             for element in packet.get_elements(direction='out', high_level=True):
#                 output_names.append("'{0}'".format(element.get_name().dash))

#                 constant_group = element.get_constant_group()

#                 if constant_group != None:
#                     symbols = {}

#                     for constant in constant_group.get_constants():
#                         symbols[constant.get_value()] = '{0}-{1}'.format(constant_group.get_name().dash, constant.get_name().dash)

#                     output_symbols.append(str(symbols))
#                 else:
#                     output_symbols.append('None')

#             name_under = packet.get_name(skip=-2).under
#             name_dash = packet.get_name(skip=-2).dash

#             function = template.format(name_under,
#                                        name_dash,
#                                        self.get_name().camel,
#                                        self.get_category().camel,
#                                        -packet.get_function_id(),
#                                        ', '.join(output_names),
#                                        ', '.join(output_symbols))

#             entries.append("'{0}': {1}".format(name_dash,
#                                                name_under))

#             callback_patterns.append(name_dash)

#             functions.append(function)

#         if self.get_long_display_name() == 'RS232 Bricklet':
#             entries.append("'read-callback': read")
#             callback_patterns.append('read-callback')

#             entries.append("'error-callback': error")
#             callback_patterns.append('error-callback')

#         return '\n'.join(functions) + '\n\tcallbacks = {\n\t' + ',\n\t'.join(entries) + '\n\t}'

#     def get_mqtt_dispatch_footer(self):
#         template = """

# 	dispatch_generic(ctx, '{0}', callbacks, argv)
# """

#         return template.format(self.get_mqtt_device_name())

    def get_mqtt_source(self):
        source  = self.get_mqtt_class()
        source += self.get_mqtt_function_map()
        source += self.get_mqtt_callback_map()
        source += self.get_mqtt_init_method()        
        #source += self.get_mqtt_callback_formats()
        #source += self.get_mqtt_high_level_callbacks()
        #source += self.get_mqtt_call_header()
        #source += self.get_mqtt_call_functions()
        #source += self.get_mqtt_call_footer()
        #source += self.get_mqtt_dispatch_header()
        #source += self.get_mqtt_dispatch_functions()
        #source += self.get_mqtt_dispatch_footer()

        return source

class MQTTBindingsGenerator(common.BindingsGenerator):
    def __init__(self, *args, **kwargs):
        common.BindingsGenerator.__init__(self, *args, **kwargs)

        self.call_devices = []
        self.dispatch_devices = []
        self.device_identifier_symbols = []
        self.completion_devices = []
        self.part_files = []
        self.devices = []

    def get_bindings_name(self):
        return 'mqtt'

    def get_bindings_display_name(self):
        return 'MQTT'

    def get_device_class(self):
        return MQTTBindingsDevice

    def get_packet_class(self):
        return MQTTBindingsPacket

    def get_element_class(self):
        return mqtt_common.MQTTElement

    def generate(self, device):
        #if not device.is_released():
        #    return

        self.devices.append("'{mqtt_dev_name}': {py_dev_name}".format(mqtt_dev_name=device.get_mqtt_device_name(), py_dev_name=device.get_python_class_name()))

        # self.call_devices.append("'{0}': call_{1}_{2}".format(device.get_mqtt_device_name(),
        #                                                       device.get_name().under,
        #                                                       device.get_category().under))

        # self.dispatch_devices.append("'{0}': dispatch_{1}_{2}".format(device.get_mqtt_device_name(),
        #                                                               device.get_name().under,
        #                                                               device.get_category().under))

        # self.device_identifier_symbols.append("{0}: '{1}'".format(device.get_device_identifier(),
        #                                                           device.get_mqtt_device_name()))

        # self.completion_devices.append(device.get_mqtt_device_name())

        filename = '{0}.part'.format(device.get_mqtt_device_name())

        with open(os.path.join(self.get_bindings_dir(), filename), 'w') as f:
            f.write(device.get_mqtt_source())

        self.part_files.append(filename)

    def finish(self):
        common.BindingsGenerator.finish(self)

        root_dir = self.get_root_dir()
        bindings_dir = self.get_bindings_dir()
        version = self.get_changelog_version()
        mqtt = open(os.path.join(bindings_dir, 'tinkerforge'), 'w')

        with open(os.path.join(root_dir, 'tinkerforge.header'), 'r') as f:
            header = f.read().replace('<<VERSION>>', '.'.join(version))

        with open(os.path.join(root_dir, 'tinkerforge.footer'), 'r') as f:
            footer = f.read().replace('<<VERSION>>', '.'.join(version))

        mqtt.write(header)

        with open(os.path.join(root_dir, '..', 'python', 'ip_connection.py'), 'r') as f:
            ipcon = f.read()

        mqtt.write('\n\n\n' + ipcon + '\n\n\n')

        for filename in sorted(self.part_files):
            if filename.endswith('.part'):
                with open(os.path.join(bindings_dir, filename), 'r') as f:
                    mqtt.write(f.read())

        mqtt.write('\fdevices = {\n' + ',\n'.join(self.devices) + '\n}\n')
        #mqtt.write('\ncall_devices = {\n' + ',\n'.join(self.call_devices) + '\n}\n')
        #mqtt.write('\ndispatch_devices = {\n' + ',\n'.join(self.dispatch_devices) + '\n}\n')
        #mqtt.write('\ndevice_identifier_symbols = {\n' + ',\n'.join(self.device_identifier_symbols) + '\n}\n')
        mqtt.write(footer)
        mqtt.close()

def generate(root_dir):
    common.generate(root_dir, 'en', MQTTBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
