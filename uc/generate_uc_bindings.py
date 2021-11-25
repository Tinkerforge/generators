#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
C/C++ for Microcontrollers Bindings Generator
Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>

generate_uc_bindings.py: Generator for C/C++ bindings for Microcontrollers

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

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import math
import importlib.util
import importlib.machinery

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

    if sys.hexversion < 0x3050000:
        generators_module = importlib.machinery.SourceFileLoader('generators', os.path.join(generators_dir, '__init__.py')).load_module()
    else:
        generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
        generators_module = importlib.util.module_from_spec(generators_spec)

        generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common
from generators.uc import uc_common
from generators.uc.uc_common import format

class UCBindingsDevice(common.Device):
    def specialize_c_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return format('{{@link tf_{device_under}_register_{packet_under}_callback}}', packet.get_device(), packet, -2 if high_level else 0)
            else:
                return format('{{@link tf_{device_under}_{packet_under}}}', packet.get_device(), packet, -2 if high_level else 0)

        return self.specialize_doc_rst_links(text, specializer)

    def get_c_include_c(self):
        template = """{header_comment}

#include "{category_under}_{device_under}.h"
#include "base58.h"
#include "endian_convert.h"
#include "errors.h"

#include <string.h>

#ifdef __cplusplus
extern "C" {{
#endif

"""

        return format(template, self, header_comment=self.get_generator().get_header_comment('asterisk'))

    def get_c_function_id_defines(self):
        defines = ''
        template = """
/**
 * \\ingroup TF_{device_camel}
 */
#define TF_{device_upper}_FUNCTION_{packet_upper} {fid}
"""

        for packet in self.get_packets('function'):
            defines += format(template, self, packet, fid=packet.get_function_id())

        return common.wrap_non_empty('', defines, '\n')

    def get_c_callback_defines(self):
        defines = '#if TF_IMPLEMENT_CALLBACKS != 0\n'
        template = """
/**
 * \\ingroup TF_{device_camel}
 */
#define TF_{device_upper}_CALLBACK_{packet_upper} {fid}
"""

        for packet in self.get_packets('callback'):
            defines += format(template, self, packet, fid=packet.get_function_id())

        defines += '\n#endif'
        return defines

    def get_c_constants(self):
        constant_format = """
/**
 * \\ingroup TF_{device_camel}
 */
#define TF_{device_upper}_{constant_group_name_upper}_{constant_name_upper} {constant_value}
"""

        return '\n' + self.get_formatted_constants(constant_format,
                                                   bool_format_func=lambda value: str(value).lower(),
                                                   category_camel=self.get_category().camel,
                                                   device_camel=self.get_name().camel,
                                                   device_upper=self.get_name().upper)

    def get_c_device_identifier_define(self):
        template = """
/**
 * \\ingroup TF_{device_camel}
 *
 * This constant is used to identify a {device_display}.
 *
 * The {{@link {device_under}_get_identity}} function and the
 * {{@link IPCON_CALLBACK_ENUMERATE}} callback of the IP Connection have a
 * \\c device_identifier parameter to specify the Brick's or Bricklet's type.
 */
#define TF_{device_upper}_DEVICE_IDENTIFIER {did}
"""

        return format(template, self, did=self.get_device_identifier())

    def get_c_device_display_name_define(self):
        template = """
/**
 * \\ingroup TF_{device_camel}
 *
 * This constant represents the display name of a {device_display}.
 */
#define TF_{device_upper}_DEVICE_DISPLAY_NAME "{device_display}"
"""

        return format(template, self)

    def get_c_create_function(self):
        template = """
int tf_{device_under}_create(TF_{device_camel} *{device_under}, const char *uid, TF_HAL *hal) {{
    if ({device_under} == NULL || uid == NULL || hal == NULL) {{
        return TF_E_NULL;
    }}

    memset({device_under}, 0, sizeof(TF_{device_camel}));

    uint32_t numeric_uid;
    int rc = tf_base58_decode(uid, &numeric_uid);

    if (rc != TF_E_OK) {{
        return rc;
    }}

    uint8_t port_id;
    uint8_t inventory_index;
    rc = tf_hal_get_port_id(hal, numeric_uid, &port_id, &inventory_index);

    if (rc < 0) {{
        return rc;
    }}

    rc = tf_hal_get_tfp(hal, &{device_under}->tfp, TF_{device_upper}_DEVICE_IDENTIFIER, inventory_index);

    if (rc != TF_E_OK) {{
        return rc;
    }}

    {device_under}->tfp->device = {device_under};
    {device_under}->tfp->uid = numeric_uid;
    {device_under}->tfp->cb_handler = tf_{device_under}_callback_handler;{response_expected_init}

    return TF_E_OK;
}}
"""

        unknown_template = """
int tf_{device_under}_create(TF_{device_camel} *{device_under}, const char *uid, TF_HAL *hal, uint8_t port_id, uint8_t inventory_index) {{
    if ({device_under} == NULL || uid == NULL || hal == NULL) {{
        return TF_E_NULL;
    }}

    memset({device_under}, 0, sizeof(TF_{device_camel}));

    uint32_t numeric_uid;
    int rc = tf_base58_decode(uid, &numeric_uid);

    if (rc != TF_E_OK) {{
        return rc;
    }}

    rc = tf_hal_get_tfp(hal, &{device_under}->tfp, 0, inventory_index);

    if (rc != TF_E_OK) {{
        return rc;
    }}

    {device_under}->tfp->device = {device_under};
    {device_under}->tfp->uid = numeric_uid;
    {device_under}->tfp->cb_handler = tf_{device_under}_callback_handler;
    TF_PortCommon *port_common = tf_hal_get_port_common(hal, port_id);
    rc = tf_spitfp_create(&port_common->spitfp, hal, port_id);

    if (rc != TF_E_OK) {{
        return rc;
    }}

    {device_under}->tfp->spitfp = &port_common->spitfp;{response_expected_init}

    return TF_E_OK;
}}
"""

        mapped_bytes, response_dict = self.get_c_response_expected_info()

        response_expected_bytes = [0] * mapped_bytes

        for packet in self.get_packets('function'):
            if packet.get_function_id() not in response_dict:
                continue
            if packet.get_response_expected() != 'true':
                continue
            mapped_id = response_dict[packet.get_function_id()]
            response_expected_bytes[mapped_id // 8] |= 1 << (mapped_id % 8)

        response_expected_assigns = []
        for i, b in enumerate(response_expected_bytes):
            response_expected_assigns.append(format("{device_under}->response_expected[{i}] = 0x{b:02X};", self, i=i, b=b))

        response_expected_init = common.wrap_non_empty('\n    ', '\n    '.join(response_expected_assigns), '')

        if self.get_name().under == 'unknown':
            template = unknown_template

        return format(template, self, response_expected_init=response_expected_init)

    def get_c_destroy_function(self):
        template = """
int tf_{device_under}_destroy(TF_{device_camel} *{device_under}) {{
    if ({device_under} == NULL) {{
        return TF_E_NULL;
    }}

    int result = tf_tfp_destroy({device_under}->tfp);
    {device_under}->tfp = NULL;

    return result;
}}
"""
        return format(template, self)

    def get_c_callback_tick_function(self):
        template = """
int tf_{device_under}_callback_tick(TF_{device_camel} *{device_under}, uint32_t timeout_us) {{
    if ({device_under} == NULL) {{
        return TF_E_NULL;
    }}

    return tf_tfp_callback_tick({device_under}->tfp, tf_hal_current_time_us((TF_HAL *){device_under}->tfp->hal) + timeout_us);
}}
"""
        return format(template, self)

    def get_c_response_expected_info(self):
        mapped_id = 0
        d = {}
        for packet in self.get_packets('function'):
            if packet.get_response_expected() == 'always_true':
                continue
            d[packet.get_function_id()] = mapped_id
            mapped_id += 1

        return math.ceil(mapped_id / 8.0), d

    def get_c_response_expected_functions(self):
        template = """
int tf_{device_under}_get_response_expected(TF_{device_camel} *{device_under}, uint8_t function_id, bool *ret_response_expected) {{
    if ({device_under} == NULL) {{
        return TF_E_NULL;
    }}

    switch (function_id) {{
{getter_cases}
        default:
            return TF_E_INVALID_PARAMETER;
    }}

    return TF_E_OK;
}}

int tf_{device_under}_set_response_expected(TF_{device_camel} *{device_under}, uint8_t function_id, bool response_expected) {{
    if ({device_under} == NULL) {{
        return TF_E_NULL;
    }}

    switch (function_id) {{
{setter_cases}
        default:
            return TF_E_INVALID_PARAMETER;
    }}

    return TF_E_OK;
}}

int tf_{device_under}_set_response_expected_all(TF_{device_camel} *{device_under}, bool response_expected) {{
    if ({device_under} == NULL) {{
        return TF_E_NULL;
    }}

    memset({device_under}->response_expected, response_expected ? 0xFF : 0, {mapped_bytes});

    return TF_E_OK;
}}
"""

        getter_template = """        case TF_{device_upper}_FUNCTION_{packet_upper}:
            if (ret_response_expected != NULL) {{
                *ret_response_expected = ({device_under}->response_expected[{byte}] & (1 << {bit})) != 0;
            }}
            break;"""

        setter_template = """        case TF_{device_upper}_FUNCTION_{packet_upper}:
            if (response_expected) {{
                {device_under}->response_expected[{byte}] |= (1 << {bit});
            }} else {{
                {device_under}->response_expected[{byte}] &= ~(1 << {bit});
            }}
            break;"""

        getters = []
        setters = []

        mapped_bytes, response_map = self.get_c_response_expected_info()

        for packet in self.get_packets('function'):
            if packet.get_function_id() not in response_map:
                continue

            mapped_id = response_map[packet.get_function_id()]
            byte = mapped_id // 8
            bit = mapped_id % 8

            getters.append(format(getter_template, self, packet, byte=byte, bit=bit))
            setters.append(format(setter_template, self, packet, byte=byte, bit=bit))

        return format(template, self, setter_cases='\n'.join(setters),
                                      getter_cases='\n'.join(getters),
                                      mapped_bytes=mapped_bytes)


    def get_c_functions(self):
        functions = ''

        # normal and low-level
        template = """
int tf_{device_under}_{packet_under}(TF_{device_camel} *{device_under}{params}) {{
    if ({device_under} == NULL) {{
        return TF_E_NULL;
    }}

    if (tf_hal_get_common((TF_HAL *){device_under}->tfp->hal)->locked) {{
        return TF_E_LOCKED;
    }}

    bool response_expected = true;{response_expected}
    tf_tfp_prepare_send({device_under}->tfp, TF_{fid}, {request_size}, {response_size}, response_expected);
{loop_counter_def}{request_assignments}
    uint32_t deadline = tf_hal_current_time_us((TF_HAL *){device_under}->tfp->hal) + tf_hal_get_common((TF_HAL *){device_under}->tfp->hal)->timeout;

    uint8_t error_code = 0;
    int result = tf_tfp_send_packet({device_under}->tfp, response_expected, deadline, &error_code);

    if (result < 0) {{
        return result;
    }}

    if (result & TF_TICK_TIMEOUT) {{
        return TF_E_TIMEOUT;
    }}
{extract_response}
    result = tf_tfp_finish_send({device_under}->tfp, result, deadline);

    if (result < 0) {{
        return result;
    }}

    return tf_tfp_get_error(error_code);
}}
"""
        template_response_expected = """
    tf_{device_under}_get_response_expected({device_under}, TF_{fid}, &response_expected);"""

        template_extract_response = """
    if (result & TF_TICK_PACKET_RECEIVED && error_code == 0) {{
        {response_assignments}
        tf_tfp_packet_processed({device_under}->tfp);
    }}
"""

        for packet in self.get_packets('function'):
            params = common.wrap_non_empty(', ', packet.get_c_parameters(), '')
            fid = format('{device_upper}_FUNCTION_{packet_upper}', self, packet)

            packet_camel = packet.get_name().camel
            request_assignments, needs_i = packet.get_c_struct_list()

            request_size = sum(e.get_size() for e in packet.get_elements(direction='in'))
            response_size = sum(e.get_size() for e in packet.get_elements(direction='out'))

            if len(request_assignments) > 0:
                request_assignments = format('\n    uint8_t *buf = tf_tfp_get_payload_buffer({device_under}->tfp);\n{req_assign}\n', self, req_assign=request_assignments)

            if len(packet.get_elements(direction='out')) > 0:
                response_struct_def = '\n    ' + packet_camel + '_Response response;'
                return_list, needs_i2 = packet.get_c_return_list(format('&{device_under}->tfp->spitfp->recv_buf', self), context='getter')
                response_assignments = format(template_extract_response, self, response_assignments='\n        '.join(return_list))

                reponse_ptr = '(Packet *)&response'
            else:
                response_struct_def = ''
                response_assignments = ''
                needs_i2 = False
                reponse_ptr = 'NULL'

            if needs_i or needs_i2:
                loop_counter_def = '\n    size_t i;'
            else:
                loop_counter_def = ''

            if packet.get_response_expected() != 'always_true':
                response_expected = format(template_response_expected, self, fid=fid)
            else:
                response_expected = ''

            functions += format(template, self, packet, params=params,
                                                        fid=fid,
                                                        response_struct_def=response_struct_def,
                                                        request_assignments=request_assignments,
                                                        response_expected=response_expected,
                                                        extract_response=response_assignments,
                                                        loop_counter_def=loop_counter_def,
                                                        reponse_ptr=reponse_ptr,
                                                        request_size=request_size,
                                                        response_size=response_size)

        template_stream_wrapper_struct = """
typedef struct TF_{device_camel}_{packet_camel}LLWrapperData {{
    {extra_param_decls}
}} TF_{device_camel}_{packet_camel}LLWrapperData;

"""
        template_stream_wrapper_struct_cast = """TF_{device_camel}_{packet_camel}LLWrapperData *data = (TF_{device_camel}_{packet_camel}LLWrapperData *) wrapper_data;
    """
        template_stream_wrapper_creation = """
    TF_{device_camel}_{packet_camel}LLWrapperData wrapper_data;
    memset(&wrapper_data, 0, sizeof(wrapper_data));
"""

        template_stream_in_wrapper_chunk_offset_assignment = """{stream_length_type} {stream_name_under}_chunk_offset = ({stream_length_type})chunk_offset;
    """
        template_stream_in_wrapper_fixed_length_assignment = """{stream_length_type} {stream_name_under}_length = ({stream_length_type})stream_length;
    """
        template_stream_in = """{wrapper_struct}
static int tf_{device_under}_{packet_under}_ll_wrapper(void *device, void *wrapper_data, uint32_t stream_length, uint32_t chunk_offset, void *chunk_data, uint32_t *ret_chunk_written) {{
    {wrapper_cast}{wrapper_chunk_offset_assignment}{wrapper_fixed_length_assignment}{chunk_written_type} {stream_name_under}{maybe_chunk}_written = {chunk_cardinality};

    {chunk_data_type} *{stream_name_under}{maybe_chunk}_data = ({chunk_data_type} *) chunk_data;
    int ret = tf_{device_under}_{packet_under}_low_level((TF_{device_camel} *)device, {wrapped_arguments});

    *ret_chunk_written = (uint32_t) {stream_name_under}{maybe_chunk}_written;
    return ret;
}}

int tf_{device_under}_{packet_under}(TF_{device_camel} *{device_under}{high_level_parameters}) {{
    if ({device_under} == NULL) {{
        return TF_E_NULL;
    }}
    {wrapper_creation}{fill_extra_params}

    uint32_t stream_length = {fixed_length_or_param_assignment};
    uint32_t {stream_name_under}_written = 0;
    {chunk_data_type} chunk_data[{chunk_cardinality}];

    int ret = tf_stream_in({device_under}, tf_{device_under}_{packet_under}_ll_wrapper, {wrapper_arg}, {stream_name_under}, stream_length, chunk_data, &{stream_name_under}_written, {chunk_cardinality}, tf_copy_items_{chunk_data_type});

{short_write_assignment}

    return ret;
}}

"""

        template_stream_out = """{wrapper_struct}
static int tf_{device_under}_{packet_under}_ll_wrapper(void *device, void *wrapper_data, uint32_t *ret_stream_length, uint32_t *ret_chunk_offset, void *chunk_data) {{
    {wrapper_cast}{stream_length_type} {stream_name_under}_length = {fixed_length};
    {stream_length_type} {stream_name_under}_chunk_offset = 0;
    {chunk_data_type} *{stream_name_under}_chunk_data = ({chunk_data_type} *) chunk_data;
    int ret = tf_{device_under}_{packet_under}_low_level((TF_{device_camel} *)device, {wrapped_arguments});{chunk_offset_check}

    *ret_stream_length = (uint32_t){stream_name_under}_length;
    *ret_chunk_offset = (uint32_t){stream_name_under}_chunk_offset;
    return ret;
}}

int tf_{device_under}_{packet_under}(TF_{device_camel} *{device_under}{high_level_parameters}) {{
    if ({device_under} == NULL) {{
        return TF_E_NULL;
    }}
    {wrapper_creation}{fill_extra_params}
    uint32_t {stream_name_under}_length = 0;
    {chunk_data_type} {stream_name_under}_chunk_data[{chunk_cardinality}];

    int ret = tf_stream_out({device_under}, tf_{device_under}_{packet_under}_ll_wrapper, {wrapper_arg}, ret_{stream_name_under}, &{stream_name_under}_length, {stream_name_under}_chunk_data, {chunk_cardinality}, tf_copy_items_{chunk_data_type});

    if (ret_{stream_name_under}_length != NULL) {{
        *ret_{stream_name_under}_length = ({stream_length_type}){stream_name_under}_length;
    }}
    return ret;
}}
"""

        template_stream_out_chunk_offset_check = """

    if ({stream_name_under}_chunk_offset == (1 << {shift_size}) - 1) {{ // maximum chunk offset -> stream has no data
        return TF_E_INTERNAL_STREAM_HAS_NO_DATA;
    }}"""
        template_stream_out_single_chunk = """
int tf_{device_under}_{packet_under}(TF_{device_camel} *{device_under}{high_level_parameters}) {{
    if ({device_under} == NULL) {{
        return TF_E_NULL;
    }}

    int ret = TF_E_OK;
    {stream_length_type} {stream_name_under}_length = 0;
    {chunk_data_type} {stream_name_under}_data[{chunk_cardinality}];

    if (ret_{stream_name_under}_length != NULL) {{
        *ret_{stream_name_under}_length = 0;
    }}

    ret = tf_{device_under}_{packet_under}_low_level({device_under}{parameters});

    if (ret != TF_E_OK) {{
        return ret;
    }}

    if (ret_{stream_name_under} != NULL) {{
        memcpy(ret_{stream_name_under}, {stream_name_under}_data, sizeof({chunk_data_type}) * {stream_name_under}_length);
        memset(&ret_{stream_name_under}[{stream_name_under}_length], 0, sizeof({chunk_data_type}) * ({chunk_cardinality} - {stream_name_under}_length));
    }}

    if (ret_{stream_name_under}_length != NULL) {{
        *ret_{stream_name_under}_length = {stream_name_under}_length;
    }}

    return ret;
}}
"""

        for packet in self.get_packets('function'):
            stream_in = packet.get_high_level('stream_in')
            stream_out = packet.get_high_level('stream_out')

            if stream_in is None and stream_out is None:
                continue

            extra_param_decls = common.wrap_non_empty("", packet.get_c_parameters(role=None).replace(", ", ";\n    "), ";")
            fill_extra_params = ""
            if len(packet.get_c_arguments('default', role=None)) > 0:
                fill_extra_params = "    " + "\n    ".join("wrapper_data.{0} = {0};".format(x) for x in packet.get_c_arguments('default', role=None).split(", "))


            roleless_args = packet.get_c_arguments('default', role=None).split(", ")
            wrapped_args = []
            for arg in packet.get_c_arguments('default').split(", "):
                if arg not in roleless_args:
                    wrapped_args.append(arg)
                    continue

                wrapped_args.append("data->" + arg)

            wrapper_struct = ""
            wrapper_cast = "(void)wrapper_data;\n    "
            wrapper_creation = ""
            wrapper_arg = "NULL"
            if len(extra_param_decls) > 0:
                wrapper_struct = format(template_stream_wrapper_struct, self, packet, -2,
                                        extra_param_decls=extra_param_decls)
                wrapper_cast = format(template_stream_wrapper_struct_cast, self, packet, -2)
                wrapper_creation = format(template_stream_wrapper_creation, self, packet, -2)
                wrapper_arg = "&wrapper_data"

            if stream_in != None:
                length_element = stream_in.get_length_element()
                chunk_offset_element = stream_in.get_chunk_offset_element()

                if length_element != None:
                    stream_length_type = length_element.get_c_type('default')
                elif chunk_offset_element != None:
                    stream_length_type = chunk_offset_element.get_c_type('default')

                fixed_length_or_param_assignment = stream_in.get_name().under + "_length"
                wrapper_fixed_length_assignment = template_stream_in_wrapper_fixed_length_assignment.format(stream_name_under=stream_in.get_name().under, stream_length_type=stream_length_type)
                if stream_in.get_fixed_length() is not None:
                    fixed_length_or_param_assignment = stream_in.get_fixed_length()
                    wrapper_fixed_length_assignment = "(void)stream_length;"

                # If we don't have a short write, the low level function will not take a pointer to _written.
                # We can then just use uint32_t as it is casted to this later anyway.
                chunk_written_type = "uint32_t"
                short_write_assignment = ""
                if stream_in.has_short_write():
                    chunk_written_type = packet.get_elements(role='stream_chunk_written')[0].get_c_type('default')
                    short_write_assignment = """    if (ret_{stream_name_under}_written != NULL) {{
        *ret_{stream_name_under}_written = ({stream_length_type}) {stream_name_under}_written;
    }}""".format(stream_name_under=stream_in.get_name().under, stream_length_type=stream_length_type)

                maybe_chunk = ""
                wrapper_chunk_offset_assignment = "(void) chunk_offset;"
                if not stream_in.has_single_chunk():
                    maybe_chunk = "_chunk"
                    wrapper_chunk_offset_assignment = template_stream_in_wrapper_chunk_offset_assignment.format(stream_name_under=stream_in.get_name().under, stream_length_type=stream_length_type)

                functions += format(template_stream_in, self, packet, -2,
                                    parameters=common.wrap_non_empty(', ', packet.get_c_arguments('default'), ''),
                                    high_level_parameters=common.wrap_non_empty(', ', packet.get_c_parameters(high_level=True), ''),
                                    stream_name_under=stream_in.get_name().under,
                                    stream_length_type=stream_length_type,
                                    fixed_length=stream_in.get_fixed_length(),
                                    chunk_data_type=stream_in.get_chunk_data_element().get_c_type('default'),
                                    chunk_cardinality=stream_in.get_chunk_data_element().get_cardinality(),

                                    fill_extra_params=fill_extra_params,
                                    wrapped_arguments=", ".join(wrapped_args),
                                    wrapper_struct=wrapper_struct,
                                    wrapper_cast=wrapper_cast,
                                    wrapper_creation=wrapper_creation,
                                    wrapper_arg=wrapper_arg,
                                    fixed_length_or_param_assignment=fixed_length_or_param_assignment,
                                    short_write_assignment=short_write_assignment,
                                    maybe_chunk=maybe_chunk,
                                    wrapper_chunk_offset_assignment=wrapper_chunk_offset_assignment,
                                    wrapper_fixed_length_assignment=wrapper_fixed_length_assignment,
                                    chunk_written_type=chunk_written_type)

            elif stream_out != None:
                length_element = stream_out.get_length_element()
                chunk_offset_element = stream_out.get_chunk_offset_element()

                if length_element != None:
                    stream_length_type = length_element.get_c_type('default')
                elif chunk_offset_element != None:
                    stream_length_type = chunk_offset_element.get_c_type('default')

                if stream_out.has_single_chunk():
                    template = template_stream_out_single_chunk
                else:
                    template = template_stream_out

                if stream_out.get_fixed_length() != None:
                    chunk_offset_check = format(template_stream_out_chunk_offset_check,
                                                stream_name_under=stream_out.get_name().under,
                                                shift_size=int(stream_out.get_chunk_offset_element().get_type().replace('uint', '')))
                else:
                    chunk_offset_check = ''

                functions += format(template, self, packet, -2,
                                    parameters=common.wrap_non_empty(', ', packet.get_c_arguments('default'), ''),
                                    high_level_parameters=common.wrap_non_empty(', ', packet.get_c_parameters(high_level=True), ''),
                                    stream_name_under=stream_out.get_name().under,
                                    stream_length_type=stream_length_type,
                                    fixed_length=stream_out.get_fixed_length(default='0'),
                                    chunk_offset_check=chunk_offset_check,
                                    chunk_data_type=stream_out.get_chunk_data_element().get_c_type('default'),
                                    chunk_cardinality=stream_out.get_chunk_data_element().get_cardinality(),

                                    fill_extra_params=fill_extra_params,
                                    wrapped_arguments=", ".join(wrapped_args),
                                    wrapper_struct=wrapper_struct,
                                    wrapper_cast=wrapper_cast,
                                    wrapper_creation=wrapper_creation,
                                    wrapper_arg=wrapper_arg)

        return functions

    def get_c_register_callback_functions(self):
        if self.get_callback_count() == 0:
            return '\n'

        result = []

        template = """
int tf_{device_under}_register_{packet_under}_callback(TF_{device_camel} *{device_under}, TF_{device_camel}_{packet_camel}Handler handler, void *user_data) {{
    if ({device_under} == NULL) {{
        return TF_E_NULL;
    }}

    if (handler == NULL) {{
        {device_under}->tfp->needs_callback_tick = false;{other_handler_checks}
    }} else {{
        {device_under}->tfp->needs_callback_tick = true;
    }}

    {device_under}->{packet_under}_handler = handler;
    {device_under}->{packet_under}_user_data = user_data;

    return TF_E_OK;
}}
"""

        template_high_level = """
static void tf_{device_under}_{packet_under}_wrapper(TF_{device_camel} *{device_under}, {low_level_params}void *user_data) {{
    {fixed_length_declaration}uint32_t stream_length = (uint32_t) {stream_name_under}_length;
    uint32_t chunk_offset = (uint32_t) {chunk_offset_or_zero};
    if (!tf_stream_out_callback(&{device_under}->{packet_under}_hlc, stream_length, chunk_offset, {stream_name_under}{maybe_chunk}_data, {chunk_cardinality}, tf_copy_items_{chunk_data_type})) {{
        return;
    }}

    // Stream is either complete or out of sync
    {stream_data_type} *{stream_name_under} = ({stream_data_type} *) ({device_under}->{packet_under}_hlc.length == 0 ? NULL : {device_under}->{packet_under}_hlc.data);
    {device_under}->{packet_under}_handler({device_under}, {high_level_arguments}user_data);

    {device_under}->{packet_under}_hlc.stream_in_progress = false;
    {device_under}->{packet_under}_hlc.length = 0;
}}

int tf_{device_under}_register_{packet_under}_callback(TF_{device_camel} *{device_under}, TF_{device_camel}_{packet_camel}Handler handler, {stream_data_type} *{stream_name_under}_buffer, void *user_data) {{
    if ({device_under} == NULL) {{
        return TF_E_NULL;
    }}

    {device_under}->{packet_under}_handler = handler;

    {device_under}->{packet_under}_hlc.data = {stream_name_under}_buffer;
    {device_under}->{packet_under}_hlc.length = 0;
    {device_under}->{packet_under}_hlc.stream_in_progress = false;

    return tf_{device_under}_register_{packet_under}_low_level_callback({device_under}, handler == NULL ? NULL : tf_{device_under}_{packet_under}_wrapper, user_data);
}}
"""

        other_handler_check_template = """{device_under}->tfp->needs_callback_tick |= {device_under}->{packet_under}_handler != NULL;"""

        for packet in self.get_packets('callback'):
            other_handler_checks = '\n        '.join([
                format(other_handler_check_template, self, other_packet)
                for other_packet in self.get_packets('callback')
                if other_packet != packet
            ])

            other_handler_checks = common.wrap_non_empty("\n        ", other_handler_checks, "")

            result.append(format(template, self, packet, other_handler_checks=other_handler_checks))

            if packet.has_high_level():
                stream_out = packet.get_high_level('stream_out')

                maybe_chunk = ""
                chunk_offset_or_zero = "0"
                if not stream_out.has_single_chunk():
                    maybe_chunk = "_chunk"
                    chunk_offset_or_zero = stream_out.get_name().under + "_chunk_offset"

                fixed_length_declaration = ""
                if stream_out.get_fixed_length() is not None:
                    chunk_offset_element = stream_out.get_chunk_offset_element()
                    stream_length_type = chunk_offset_element.get_c_type('default')
                    fixed_length_declaration = "{} {}_length = {};\n    ".format(stream_length_type, stream_out.get_name().under, stream_out.get_fixed_length())


                result.append(format(template_high_level, self, packet, -2,
                                     low_level_params=common.wrap_non_empty('', packet.get_c_parameters(), ', '),
                                     stream_name_under=stream_out.get_name().under,
                                     chunk_cardinality=stream_out.get_chunk_data_element().get_cardinality(),
                                     chunk_data_type=stream_out.get_chunk_data_element().get_c_type('default'),
                                     stream_data_type=stream_out.get_data_element().get_c_type('default'),
                                     high_level_arguments=common.wrap_non_empty('', packet.get_c_arguments('default', high_level=True), ', '),
                                     maybe_chunk=maybe_chunk,
                                     chunk_offset_or_zero=chunk_offset_or_zero,
                                     fixed_length_declaration=fixed_length_declaration))

        return format('#if TF_IMPLEMENT_CALLBACKS != 0{funcs}#endif', funcs='\n'.join(result))

    def get_c_callback_handler(self):
        no_callbacks_template = """
static bool tf_{device_under}_callback_handler(void *dev, uint8_t fid, TF_PacketBuffer *payload) {{
    (void)dev;
    (void)fid;
    (void)payload;

    return false;
}}"""
        template = """
#if TF_IMPLEMENT_CALLBACKS != 0
static bool tf_{device_under}_callback_handler(void *dev, uint8_t fid, TF_PacketBuffer *payload) {{
    TF_{device_camel} *{device_under} = (TF_{device_camel} *)dev;
    (void)payload;

    switch (fid) {{
{cases}
        default:
            return false;
    }}

    return true;
}}
#else
static bool tf_{device_under}_callback_handler(void *dev, uint8_t fid, TF_PacketBuffer *payload) {{
    return false;
}}
#endif"""

        case_template = """        case TF_{device_upper}_CALLBACK_{packet_upper}: {{
            TF_{device_camel}_{packet_camel}Handler fn = {device_under}->{packet_under}_handler;
            void *user_data = {device_under}->{packet_under}_user_data;
            if (fn == NULL) {{
                return false;
            }}
{i_decl}
{extract_payload}
            TF_HALCommon *hal_common = tf_hal_get_common((TF_HAL *){device_under}->tfp->hal);
            hal_common->locked = true;
            fn({device_under}, {params}user_data);
            hal_common->locked = false;
            break;
        }}
"""

        cases = []
        for packet in self.get_packets('callback'):
            extract_payload, needs_i = packet.get_c_return_list('payload', context='callback_handler')

            cases.append(format(case_template, self, packet,
                                extract_payload=common.wrap_non_empty('            ', '\n            '.join(extract_payload), ''),
                                params=common.wrap_non_empty('', packet.get_c_arguments(context='callback_wrapper'), ', '),
                                i_decl = '' if not needs_i else '            size_t i;'))

        return format(template if len(cases) > 0 else no_callbacks_template, self, cases='\n'.join(cases))

    def get_c_include_h(self):
        template = """{header_comment}
#ifndef TF_{device_upper}_H
#define TF_{device_upper}_H

#include "config.h"
#include "tfp.h"
#include "hal_common.h"
#include "macros.h"
#include "streaming.h"

#ifdef __cplusplus
extern "C" {{
#endif

/**
 * \\defgroup TF_{device_camel} {device_display}
 */

struct TF_{device_camel};
#if TF_IMPLEMENT_CALLBACKS != 0
{callback_typedefs}
#endif
/**
 * \\ingroup TF_{device_camel}
 *
 * {description}
 */
typedef struct TF_{device_camel} {{
    TF_TFP *tfp;
#if TF_IMPLEMENT_CALLBACKS != 0
{callback_handlers}
#endif
    uint8_t response_expected[{mapped_bytes}];
}} TF_{device_camel};
"""
        mapped_id_count = len([p for p in self.get_packets('function') if p.get_response_expected() != 'always_true'])

        cb_handler_template = """    TF_{device_camel}_{packet_camel}Handler {packet_under}_handler;
    void *{packet_under}_user_data;
"""
        cb_high_level_handler_template = """    TF_{device_camel}_{packet_camel}Handler {packet_under}_handler;
    TF_HighLevelCallback {packet_under}_hlc;
"""
        cb_handlers = [format(cb_handler_template, self, packet) for packet in self.get_packets('callback')]
        cb_handlers += [format(cb_high_level_handler_template, self, packet, -2) for packet in self.get_packets('callback') if packet.has_high_level()]

        return format(template, self, header_comment=self.get_generator().get_header_comment('asterisk'),
                                      callback_typedefs=self.get_c_typedefs(),
                                      callback_handlers='\n'.join(cb_handlers),
                                      description=common.select_lang(self.get_description()),
                                      mapped_bytes=math.ceil(mapped_id_count / 8.0))

    def get_c_end_h(self):
        return "\n#ifdef __cplusplus\n}\n#endif\n\n#endif\n"

    def get_c_end_c(self):
        return "\n#ifdef __cplusplus\n}\n#endif\n"

    def get_c_typedefs(self):
        typedefs = '\n'
        template = """typedef void (*TF_{device_camel}_{packet_camel}Handler)(struct TF_{device_camel} *device, {params}void *user_data);
"""

        # normal and low-level
        for packet in self.get_packets('callback'):
            typedefs += format(template, self, packet, params=common.wrap_non_empty('', packet.get_c_parameters(), ', '))
            if packet.has_high_level():
                typedefs += format(template, self, packet, -2, params=common.wrap_non_empty('', packet.get_c_parameters(high_level=True), ', '))

        return typedefs

    def get_c_create_declaration(self):
        template = """
/**
 * \\ingroup TF_{device_camel}
 *
 * Creates the device object \\c {device_under} with the unique device ID \\c uid and adds
 * it to the HAL \\c hal.
 */
int tf_{device_under}_create(TF_{device_camel} *{device_under}, const char *uid, TF_HAL *hal);
"""

        unknown_template = """
/**
 * \\ingroup TF_{device_camel}
 *
 * Creates the device object \\c {device_under} with the unique device ID \\c uid and adds
 * it to the HAL \\c hal.
 */
int tf_{device_under}_create(TF_{device_camel} *{device_under}, const char *uid, TF_HAL *hal, uint8_t port_id, uint8_t inventory_index);
"""
        if self.get_name().under == 'unknown':
            template = unknown_template

        return format(template, self)

    def get_c_destroy_declaration(self):
        template = """
/**
 * \\ingroup TF_{device_camel}
 *
 * Removes the device object \\c {device_under} from its HAL and destroys it.
 * The device object cannot be used anymore afterwards.
 */
int tf_{device_under}_destroy(TF_{device_camel} *{device_under});
"""
        return format(template, self)

    def get_c_callback_tick_declaration(self):
        template = """
#if TF_IMPLEMENT_CALLBACKS != 0
/**
 * \\ingroup TF_{device_camel}
 *
 * Polls for callbacks. Will block for the given timeout in microseconds.
 *
 * This function can be used in a non-blocking fashion by calling it with a timeout of 0.
 */
int tf_{device_under}_callback_tick(TF_{device_camel} *{device_under}, uint32_t timeout_us);
#endif
"""
        unknown_template = """
/**
 * \\ingroup TF_{device_camel}
 *
 * Polls for callbacks. Will block for the given timeout in microseconds.
 *
 * This function can be used in a non-blocking fashion by calling it with a timeout of 0.
 */
int tf_{device_under}_callback_tick(TF_{device_camel} *{device_under}, uint32_t timeout_us);
"""
        if self.get_name().under == 'unknown':
            template = unknown_template

        return format(template, self)

    def get_c_response_expected_declarations(self):
        template = """
/**
 * \\ingroup TF_{device_camel}
 *
 * Returns the response expected flag for the function specified by the
 * \\c function_id parameter. It is *true* if the function is expected to
 * send a response, *false* otherwise.
 *
 * For getter functions this is enabled by default and cannot be disabled,
 * because those functions will always send a response. For callback
 * configuration functions it is enabled by default too, but can be disabled
 * via the tf_{device_under}_set_response_expected function. For setter
 * functions it is disabled by default and can be enabled.
 *
 * Enabling the response expected flag for a setter function allows to
 * detect timeouts and other error conditions calls of this setter as well.
 * The device will then send a response for this purpose. If this flag is
 * disabled for a setter function then no response is sent and errors are
 * silently ignored, because they cannot be detected.
 */
int tf_{device_under}_get_response_expected(TF_{device_camel} *{device_under}, uint8_t function_id, bool *ret_response_expected);

/**
 * \\ingroup TF_{device_camel}
 *
 * Changes the response expected flag of the function specified by the
 * \\c function_id parameter. This flag can only be changed for setter
 * (default value: *false*) and callback configuration functions
 * (default value: *true*). For getter functions it is always enabled.
 *
 * Enabling the response expected flag for a setter function allows to detect
 * timeouts and other error conditions calls of this setter as well. The device
 * will then send a response for this purpose. If this flag is disabled for a
 * setter function then no response is sent and errors are silently ignored,
 * because they cannot be detected.
 */
int tf_{device_under}_set_response_expected(TF_{device_camel} *{device_under}, uint8_t function_id, bool response_expected);

/**
 * \\ingroup TF_{device_camel}
 *
 * Changes the response expected flag for all setter and callback configuration
 * functions of this device at once.
 */
int tf_{device_under}_set_response_expected_all(TF_{device_camel} *{device_under}, bool response_expected);
"""
        return format(template, self)

    def get_c_function_declaration(self):
        functions = ''

        # normal and low-level
        template = """
/**
 * \\ingroup TF_{device_camel}
 *
 * {doc}
 */
int tf_{device_under}_{packet_under}(TF_{device_camel} *{device_under}{parameters});
"""
        for packet in self.get_packets('function'):
            functions += format(template, self, packet,
                                doc=packet.get_c_formatted_doc(),
                                parameters=common.wrap_non_empty(', ', packet.get_c_parameters(), ''))

        # high-level
        for packet in self.get_packets('function'):
            if packet.has_high_level():
                functions += format(template, self, packet, -2,
                                    doc=packet.get_c_formatted_doc(),
                                    parameters=common.wrap_non_empty(', ', packet.get_c_parameters(high_level=True), ''))

        return functions

    def get_c_register_callback_declarations(self):
        if self.get_callback_count() == 0:
            return '\n'

        result = []

        template = """
/**
 * \\ingroup TF_{device_camel}
 *
 * Registers the given \\c handler to the {packet_space} callback. The
 * \\c user_data will be passed as the last parameter to the \\c handler.
 *
 * {doc}
 */
int tf_{device_under}_register_{packet_under}_callback(TF_{device_camel} *{device_under}, TF_{device_camel}_{packet_camel}Handler handler, {buffer_param}void *user_data);
"""

        for packet in self.get_packets('callback'):
            result.append(format(template, self, packet, doc=packet.get_c_formatted_doc(), buffer_param=""))

            if packet.has_high_level():
                stream_out = packet.get_high_level('stream_out')
                chunk_data_type = stream_out.get_chunk_data_element().get_c_type('default')
                stream_name_under = stream_out.get_name().under
                buffer_param = "{chunk_data_type} *{stream_name_under}, ".format(chunk_data_type=chunk_data_type, stream_name_under=stream_name_under)
                result.append(format(template, self, packet, -2, doc=packet.get_c_formatted_doc(), buffer_param=buffer_param))

        return '#if TF_IMPLEMENT_CALLBACKS != 0{}#endif'.format('\n'.join(result))

    def get_c_source(self):
        source  = self.get_c_include_c()
        source += self.get_c_callback_handler()
        source += self.get_c_create_function()
        source += self.get_c_destroy_function()
        source += self.get_c_response_expected_functions()
        source += self.get_c_functions()
        source += self.get_c_register_callback_functions()
        source += self.get_c_callback_tick_function()
        source += self.get_c_end_c()

        return source

    def get_c_header(self):
        header  = self.get_c_include_h()
        header += self.get_c_function_id_defines()
        header += self.get_c_callback_defines()
        header += self.get_c_constants()
        header += self.get_c_device_identifier_define()
        header += self.get_c_device_display_name_define()
        header += self.get_c_create_declaration()
        header += self.get_c_destroy_declaration()
        header += self.get_c_response_expected_declarations()
        header += self.get_c_register_callback_declarations()
        header += self.get_c_callback_tick_declaration()
        header += self.get_c_function_declaration()
        header += self.get_c_end_h()

        return header

class UCBindingsPacket(uc_common.UCPacket):
    def get_c_formatted_doc(self, high_level=False):
        text = common.select_lang(self.get_doc_text())

        # handle tables
        lines = text.split('\n')
        replaced_lines = []
        in_table_head = False
        in_table_body = False

        for line in lines:
            if line.strip() == '.. csv-table::':
                in_table_head = True
                replaced_lines.append('\\verbatim')
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

                replaced_lines.append('\\endverbatim')
                replaced_lines.append('')
            else:
                replaced_lines.append(line)

        text = '\n'.join(replaced_lines)
        text = self.get_device().specialize_c_doc_function_links(text)

        if self.get_type() == 'callback':
            parameters = self.get_c_parameters(high_level=high_level)

            if len(parameters) > 0:
                parameters += ', '

            text = 'Signature: \\code void callback({0}void *user_data) \\endcode\n'.format(parameters) + text

        text = text.replace('.. note::', '\\note')
        text = text.replace('.. warning::', '\\warning')

        def format_parameter(name):
            return '\\c {0}'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return '\n * '.join(text.strip().split('\n'))

    def get_c_struct_body(self, direction=None):
        struct_body = []

        for element in self.get_elements(direction=direction):
            c_type = element.get_c_type('struct')
            name = element.get_name().under

            if element.get_cardinality() > 1:
                struct_body.append('    {0} {1}[{2}];\n'.format(c_type, name, element.get_c_array_length()))
            else:
                struct_body.append('    {0} {1};\n'.format(c_type, name))

        return ''.join(struct_body)

    def get_c_struct_list(self):
        struct_list = ''
        needs_i = False

        offset = 0
        for element in self.get_elements(direction='in'):

            if element.get_type() == 'string':
                temp = '\n    strncpy((char *)(buf + {offset}), {src}, {count});\n'
                struct_list += temp.format(src=element.get_name().under, offset=offset, count=element.get_cardinality())
                offset += element.get_cardinality()
            elif element.get_type() == 'bool':
                if element.get_cardinality() > 1:
                    needs_i = True
                    byte_count = math.ceil(element.get_cardinality() / 8.0)
                    struct_list += '\n    memset(buf + {offset}, 0, {byte_count}); for (i = 0; i < {count}; ++i) buf[{offset} + (i / 8)] |= ({src}[i] ? 1 : 0) << (i % 8);' \
                                   .format(src=element.get_name().under, offset=offset, count=element.get_cardinality(), byte_count=math.ceil(element.get_cardinality() / 8.0))
                    offset += byte_count
                else:
                    struct_list += '\n    buf[{offset}] = {src} ? 1 : 0;'.format(offset=offset, src=element.get_name().under)
                    offset += 1
            elif element.get_cardinality() > 1:
                if element.get_item_size() > 1:
                    needs_i = True
                    struct_list += '\n    for (i = 0; i < {count}; i++) {{ {c_type} tmp_{src} = tf_leconvert_{type_}_to({src}[i]); memcpy(buf + {offset} + (i * sizeof({c_type})), &tmp_{src}, sizeof({c_type})); }}' \
                                   .format(src=element.get_name().under,
                                           c_type=element.get_c_type('default'),
                                           type_=element.get_type(),
                                           count=element.get_cardinality(),
                                           offset=offset)
                else:
                    temp = '\n    memcpy(buf + {offset}, {src}, {count});'
                    struct_list += temp.format(offset=offset,
                                               src=element.get_name().under,
                                               count=element.get_cardinality())
                offset += element.get_cardinality() * element.get_item_size()
            elif element.get_item_size() > 1:
                struct_list += '\n    {src} = tf_leconvert_{type_}_to({src}); memcpy(buf + {offset}, &{src}, {count});'.format(src=element.get_name().under, type_=element.get_type(), offset=offset, count=element.get_item_size())
                offset += element.get_item_size()
            else:
                # Cast fixes clang -Weverything complaining about sign conversion in case of char or int8_t
                struct_list += '\n    buf[{offset}] = (uint8_t){src};'.format(src=element.get_name().under, offset=offset)
                offset += 1

        return struct_list, needs_i

    def get_c_return_list(self, packet_buffer_name, context):
        assert context in ['callback_handler', 'getter']
        return_list = []
        needs_i = False

        for element in self.get_elements(direction='out'):
            if element.get_cardinality() > 1:
                if context == 'callback_handler':
                    t = '{type_} {dest}[{count}]; '
                else:
                    t = 'if ({dest} != NULL) {{ '

                if element.get_type() == 'string':
                    t += 'tf_packet_buffer_pop_n({packet_buffer}, (uint8_t*){dest}, {count});'
                elif element.get_type() == 'bool':
                    t += "tf_packet_buffer_read_bool_array({packet_buffer}, {dest}, {count});"
                else:
                    t += 'for (i = 0; i < {count}; ++i) {dest}[i] = tf_packet_buffer_read_{type_}({packet_buffer});'
                    needs_i = True

                if context == 'getter':
                    t += '}} else {{ tf_packet_buffer_remove({packet_buffer}, {size}); }}'

            else:
                if context == 'callback_handler':
                    t = '{type_} {dest} = tf_packet_buffer_read_{type_}({packet_buffer});'
                else:
                    t = 'if ({dest} != NULL) {{ *{dest} = tf_packet_buffer_read_{type_}({packet_buffer}); }} else {{ tf_packet_buffer_remove({packet_buffer}, {size}); }}'

            dest = ('ret_' if context == 'getter' else '') + element.get_name().under
            if self.get_function_id() == 255 and element.get_name().under == 'connected_uid':
                dest = 'tmp_connected_uid'
                # Overriding the template fixes clang's "comparison of array 'tmp_connected_uid' not equal to a null pointer is always true" warning
                t = 'tf_packet_buffer_pop_n({packet_buffer}, (uint8_t*){dest}, {count});'

            return_list.append(t.format(packet_buffer=packet_buffer_name,
                                        dest=dest,
                                        count=element.get_cardinality(),
                                        size=element.get_size(),
                                        type_=element.get_c_type('default')))

        if self.get_function_id() == 255:
            return_list.insert(0, 'char tmp_connected_uid[8] = {0};')
            return_list.append(
                format("""if (tmp_connected_uid[0] == 0 && ret_position != NULL) {{
            *ret_position = tf_hal_get_port_name((TF_HAL *){device_under}->tfp->hal, {device_under}->tfp->spitfp->port_id);
        }}
        if (ret_connected_uid != NULL) {{
            memcpy(ret_connected_uid, tmp_connected_uid, 8);
        }}""", self.get_device()))

        return return_list, needs_i

class UCBindingsGenerator(uc_common.UCGeneratorTrait, common.BindingsGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.device_name_cases = []

    def get_device_class(self):
        return UCBindingsDevice

    def get_packet_class(self):
        return UCBindingsPacket

    def get_element_class(self):
        return uc_common.UCElement

    def generate(self, device):
        if not device.has_comcu():
            return
        filename = format('{category_under}_{device_under}', device)

        with open(os.path.join(self.get_bindings_dir(), filename + '.c'), 'w') as f:
            f.write(device.get_c_source())

        with open(os.path.join(self.get_bindings_dir(), filename + '.h'), 'w') as f:
            f.write(device.get_c_header())

        if device.is_released():
            self.released_files.append(filename + '.c')
            self.released_files.append(filename + '.h')
            self.device_name_cases.append(format("""        case {device_id:4d}: return "{device_display}";""", device))

    def finish(self, *args, **kwargs):
        with open(os.path.join(self.get_bindings_dir(), 'display_names.c'), 'w') as f:
            f.write("""{header_comment}
#include "display_names.h"

#if TF_IMPLEMENT_STRERROR != 0
const char *tf_get_device_display_name(uint16_t device_id) {{
    switch (device_id) {{
{cases}
          default: return "unknown device";
    }}
}}
#endif
""".format(header_comment=self.get_header_comment('asterisk'), cases='\n'.join(self.device_name_cases)))

        self.released_files.append('display_names.c')

        super().finish(*args, **kwargs)

def generate(root_dir, language, internal):
    common.generate(root_dir, language, internal, UCBindingsGenerator)

if __name__ == '__main__':
    args = common.dockerize('uc', __file__, add_internal_argument=True)

    generate(os.getcwd(), 'en', args.internal)
