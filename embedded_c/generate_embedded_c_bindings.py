#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Bindings Generator
Copyright (C) 2012-2018, 2020 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>

generate_c_bindings.py: Generator for C/C++ bindings

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
from generators.embedded_c import embedded_c_common

def format(s, device=None, packet=None, packet_skip=0, **kwargs):
    if device is not None:
        kwargs['device_space'] = device.get_name().space
        kwargs['device_lower'] = device.get_name().lower
        kwargs['device_camel'] = device.get_name().camel
        kwargs['device_headless'] = device.get_name().headless
        kwargs['device_under'] = device.get_name().under
        kwargs['device_upper'] = device.get_name().upper
        kwargs['device_dash'] = device.get_name().dash
        kwargs['device_camel_abbrv'] = device.get_name().camel_abbrv
        kwargs['device_lower_no_space'] = device.get_name().lower_no_space
        kwargs['device_camel_constant_safe'] = device.get_name().camel_constant_safe

        kwargs['category_space'] = device.get_category().space
        kwargs['category_lower'] = device.get_category().lower
        kwargs['category_camel'] = device.get_category().camel
        kwargs['category_headless'] = device.get_category().headless
        kwargs['category_under'] = device.get_category().under
        kwargs['category_upper'] = device.get_category().upper
        kwargs['category_dash'] = device.get_category().dash
        kwargs['category_camel_abbrv'] = device.get_category().camel_abbrv
        kwargs['category_lower_no_space'] = device.get_category().lower_no_space
        kwargs['category_camel_constant_safe'] = device.get_category().camel_constant_safe

    if packet is not None:
        kwargs['packet_space'] = packet.get_name(packet_skip).space
        kwargs['packet_lower'] = packet.get_name(packet_skip).lower
        kwargs['packet_camel'] = packet.get_name(packet_skip).camel
        kwargs['packet_headless'] = packet.get_name(packet_skip).headless
        kwargs['packet_under'] = packet.get_name(packet_skip).under
        kwargs['packet_upper'] = packet.get_name(packet_skip).upper
        kwargs['packet_dash'] = packet.get_name(packet_skip).dash
        kwargs['packet_camel_abbrv'] = packet.get_name(packet_skip).camel_abbrv
        kwargs['packet_lower_no_space'] = packet.get_name(packet_skip).lower_no_space
        kwargs['packet_camel_constant_safe'] = packet.get_name(packet_skip).camel_constant_safe

    return s.format(**kwargs)

class CBindingsDevice(common.Device):
    def specialize_c_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return '{{@link {0}_CALLBACK_{1}}}'.format(packet.get_device().get_name().upper,
                                                           packet.get_name(skip=-2 if high_level else 0).upper)
            else:
                return '{{@link {0}_{1}}}'.format(packet.get_device().get_name().under,
                                                  packet.get_name(skip=-2 if high_level else 0).under)

        return self.specialize_doc_rst_links(text, specializer)

    def get_c_include_c(self):
        template = """{0}

//#define IPCON_EXPOSE_INTERNALS

#include "{1}_{2}.h"
#include "base58.h"
#include "endian_convert.h"
#include "errors.h"

#include <string.h>

#ifdef __cplusplus
extern "C" {{
#endif

"""

        return template.format(self.get_generator().get_header_comment('asterisk'),
                               self.get_category().under,
                               self.get_name().under)

    def get_c_function_id_defines(self):
        defines = ''
        template = """
/**
 * \\ingroup {4}{3}
 */
#define TF_{0}_FUNCTION_{1} {2}
"""

        for packet in self.get_packets('function'):
            defines += template.format(self.get_name().upper,
                                       packet.get_name().upper,
                                       packet.get_function_id(),
                                       self.get_name().camel,
                                       self.get_category().camel)

        return defines

    def get_c_callback_defines(self):
        defines = ''
        template = """
/**
 * \\ingroup {5}{4}
 *
 * {3}
 */
#define TF_{0}_CALLBACK_{1} {2}
"""

        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                doc = 'See {0}_CALLBACK_{1}'.format(self.get_name().upper, packet.get_name(skip=-2).upper)
            else:
                doc = packet.get_c_formatted_doc()
            defines += template.format(self.get_name().upper,
                                       packet.get_name().upper,
                                       packet.get_function_id(),
                                       doc,
                                       self.get_name().camel,
                                       self.get_category().camel)

        template = """
/**
 * \\ingroup {5}{4}
 *
 * {3}
 */
#define TF_{0}_CALLBACK_{1} (-{2})
"""

        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                defines += template.format(self.get_name().upper,
                                           packet.get_name(skip=-2).upper,
                                           packet.get_function_id(),
                                           packet.get_c_formatted_doc(high_level=True),
                                           self.get_name().camel,
                                           self.get_category().camel)

        return defines

    def get_c_constants(self):
        constant_format = """
/**
 * \\ingroup {doxygen}
 */
#define TF_{device_name}_{constant_group_name_upper}_{constant_name_upper} {constant_value}
"""

        return '\n' + self.get_formatted_constants(constant_format,
                                                   bool_format_func=lambda value: str(value).lower(),
                                                   doxygen=self.get_category().camel + self.get_name().camel,
                                                   device_name=self.get_name().upper)

    def get_c_device_identifier_define(self):
        template = """
/**
 * \\ingroup {3}{2}
 *
 * This constant is used to identify a {5}.
 *
 * The {{@link {4}_get_identity}} function and the
 * {{@link IPCON_CALLBACK_ENUMERATE}} callback of the IP Connection have a
 * \\c device_identifier parameter to specify the Brick's or Bricklet's type.
 */
#define TF_{0}_DEVICE_IDENTIFIER {1}
"""

        return template.format(self.get_name().upper,
                               self.get_device_identifier(),
                               self.get_name().camel,
                               self.get_category().camel,
                               self.get_name().under,
                               self.get_long_display_name())

    def get_c_device_display_name_define(self):
        template = """
/**
 * \\ingroup {3}{2}
 *
 * This constant represents the display name of a {1}.
 */
#define TF_{0}_DEVICE_DISPLAY_NAME "{1}"
"""

        return template.format(self.get_name().upper,
                               self.get_long_display_name(),
                               self.get_name().camel,
                               self.get_category().camel)

    def get_c_create_function(self):
        template = """
int tf_{device_under}_create(TF_{device_camel} *{device_under}, const char *uid, TF_HalContext *hal) {{
	uint32_t numeric_uid;
    int rc = tf_base58_decode(uid, &numeric_uid);
    if (rc != TF_E_OK) {{
        return rc;
    }}

    int port_id, inventory_index;
    rc = tf_hal_get_port_id(hal, numeric_uid, &port_id, &inventory_index);
    if (rc < 0) {{
        return rc;
    }}

    rc = tf_tfp_init(&{device_under}->tfp, numeric_uid, hal, port_id, inventory_index, tf_{device_under}_callback_handler);
    if (rc != TF_E_OK) {{
        return rc;
    }}{response_expected_init}
    return TF_E_OK;
}}
"""

        unknown_template = """
int tf_{device_under}_create(TF_{device_camel} *{device_under}, const char *uid, TF_HalContext *hal, int port_id, int inventory_index) {{
    uint32_t numeric_uid;
    int rc = tf_base58_decode(uid, &numeric_uid);
    if (rc != TF_E_OK) {{
        return rc;
    }}

    rc = tf_tfp_init(&{device_under}->tfp, numeric_uid, hal, port_id, inventory_index, tf_{device_under}_callback_handler);
    if (rc != TF_E_OK) {{
        return rc;
    }}{response_expected_init}
    return TF_E_OK;
}}
"""

        callbacks = ''

    #     cb_temp = """
	# device_p->callback_wrappers[{3}_CALLBACK_{1}] = {0}_callback_wrapper_{2};"""
    #     hlcb_temp = """
	# device_p->high_level_callbacks[-{2}_CALLBACK_{1}].exists = true;"""


    #     for packet in self.get_packets('callback'):
    #         callbacks += cb_temp.format(self.get_name().under, packet.get_name().upper, packet.get_name().under, self.get_name().upper)

    #     if len(callbacks) > 0:
    #         callbacks += '\n'

    #     for packet in self.get_packets('callback'):
    #         if packet.has_high_level():
    #             callbacks += hlcb_temp.format(self.get_name().under, packet.get_name(skip=-2).upper, self.get_name().upper)

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
            response_expected_assigns.append("{}->response_expected[{}] = 0x{:02X};".format(self.get_name().under, i, b))

        response_expected_init = common.wrap_non_empty('\n\t', '\n\t'.join(response_expected_assigns), '')

        if self.get_name().under == 'unknown':
            template = unknown_template

        return template.format(device_under=self.get_name().under,
                               device_camel=self.get_name().camel,
                               response_expected_init=response_expected_init)

    def get_c_destroy_function(self):
        return ''

        template = """
void {0}_destroy({1} *{0}) {{
	device_release({0}->p);
}}
"""
        return template.format(self.get_name().under,
                               self.get_name().camel)

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
    switch(function_id) {{
{getter_cases}
        default:
            return TF_E_INVALID_PARAMETER;
    }}
    return TF_E_OK;
}}

int tf_{device_under}_set_response_expected(TF_{device_camel} *{device_under}, uint8_t function_id, bool response_expected) {{
    switch(function_id) {{
{setter_cases}
        default:
            return TF_E_INVALID_PARAMETER;
    }}
    return TF_E_OK;
}}

void tf_{device_under}_set_response_expected_all(TF_{device_camel} *{device_under}, bool response_expected) {{
    memset({device_under}->response_expected, response_expected ? 0xFF : 0, {mapped_bytes});
}}
"""

        getter_template = """        case TF_{device_upper}_FUNCTION_{packet_upper}:
            *ret_response_expected = ({device_under}->response_expected[{byte}] & (1 << {bit})) != 0;
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

        device_under = self.get_name().under
        device_camel = self.get_name().camel

        mapped_bytes, response_map = self.get_c_response_expected_info()

        for packet in self.get_packets('function'):
            if packet.get_function_id() not in response_map:
                continue

            mapped_id = response_map[packet.get_function_id()]
            byte = mapped_id // 8
            bit = mapped_id % 8

            g = getter_template.format(device_upper=self.get_name().upper,
                                       packet_upper=packet.get_name().upper,
                                       device_under=device_under,
                                       device_camel=device_camel,
                                       byte=byte,
                                       bit=bit)

            s = setter_template.format(device_upper=self.get_name().upper,
                                       packet_upper=packet.get_name().upper,
                                       device_under=device_under,
                                       device_camel=device_camel,
                                       byte=byte,
                                       bit=bit)
            getters.append(g)
            setters.append(s)

        return template.format(device_under=device_under,
                               device_camel=device_camel,
                               setter_cases='\n'.join(setters),
                               getter_cases='\n'.join(getters),
                               mapped_bytes=mapped_bytes)


    def get_c_functions(self):
        functions = ''

        # normal and low-level
        template_version = """
TF_ATTRIBUTE_NONNULL int tf_{device_under}_get_api_version(TF_{device_camel} *{device_under}, uint8_t ret_api_version[3]) {{
	ret_api_version[0] = {api_major};
    ret_api_version[1] = {api_minor};
    ret_api_version[2] = {api_patch};
    return TF_E_OK;
}}
"""
        template = """
int tf_{device_under}_{packet_under}(TF_{device_camel} *{device_under}{params}) {{
    bool response_expected = true;{response_expected}
    tf_tfp_prepare_send(&{device_under}->tfp, TF_{fid}, {request_size}, {response_size}, response_expected);
    {unknown_bricklet_seq_num_hack}
	{loop_counter_def}{request_assignments}
    uint32_t deadline = tf_hal_current_time_ms({device_under}->tfp.spitfp.hal) + tf_hal_get_common({device_under}->tfp.spitfp.hal)->timeout;

    uint8_t error_code = 0;
	int result = tf_tfp_transmit_packet(&{device_under}->tfp, response_expected, deadline, &error_code);

    if (result & TF_TICK_TIMEOUT) {{
        //return -result;
        return TF_E_TIMEOUT;
    }}
{extract_response}
    tf_tfp_finish_send(&{device_under}->tfp, result, deadline);

    return tf_tfp_get_error(error_code);
}}
"""
        template_response_expected = """
    tf_{device_under}_get_response_expected({device_under}, TF_{fid}, &response_expected);"""

        template_extract_response = """
    if (result & TF_TICK_PACKET_RECEIVED && error_code == 0) {{
        {response_assignments}
        tf_tfp_packet_processed(&{device_under}->tfp);
    }}
"""

        device_under = self.get_name().under
        device_camel = self.get_name().camel
        functions += template_version.format(device_under=device_under,
                                             device_camel=device_camel,
                                             api_major=self.get_api_version()[0],
                                             api_minor=self.get_api_version()[1],
                                             api_patch=self.get_api_version()[2])

        for packet in self.get_packets('function'):
            seq_num_hack = ''
            if self.get_name().under == 'unknown' and packet.get_name().under == 'comcu_enumerate':
                seq_num_hack = 'unknown->tfp.waiting_for_sequence_number = 0;\n\tunknown->tfp.waiting_for_fid = 253;'
                packet.elements = next(p for p in self.get_packets('callback') if p.get_name().under == 'comcu_enumerate').elements



            packet_under = packet.get_name().under
            params = common.wrap_non_empty(', ', packet.get_c_parameters(), '')
            fid = '{0}_FUNCTION_{1}'.format(self.get_name().upper,
                                            packet.get_name().upper)
            packet_camel = packet.get_name().camel
            request_assignments, needs_i = packet.get_c_struct_list()

            request_size = sum(e.get_size() for e in packet.get_elements(direction='in'))
            response_size = sum(e.get_size() for e in packet.get_elements(direction='out'))

            if len(request_assignments) > 0:
                request_assignments = '\n\tuint8_t *buf = tf_tfp_get_payload_buffer(&{}->tfp);\n{}\n'.format(device_under, request_assignments)

            if len(packet.get_elements(direction='out')) > 0:
                response_struct_def = '\n\t' + packet_camel + '_Response response;'
                return_list, needs_i2 = packet.get_c_return_list('&{}->tfp.spitfp.recv_buf'.format(device_under), context='getter')
                response_assignments = template_extract_response.format(response_assignments='\n        '.join(return_list),
                                                                        device_under=device_under)
                reponse_ptr = '(Packet *)&response'
            else:
                response_struct_def = ''
                response_assignments = ''
                needs_i2 = False
                reponse_ptr = 'NULL'

            if needs_i or needs_i2:
                loop_counter_def = '\n\tint i;'
            else:
                loop_counter_def = ''

            if packet.get_response_expected() != 'always_true':
                response_expected = template_response_expected.format(device_under=device_under, fid=fid)
            else:
                response_expected = ''

            functions += template.format(device_under=device_under,
                                         packet_under=packet_under,
                                         device_camel=device_camel,
                                         params=params,
                                         fid=fid,
                                         packet_camel=packet_camel,
                                         response_struct_def=response_struct_def,#6
                                         request_assignments=request_assignments,
                                         response_expected=response_expected,
                                         extract_response=response_assignments,
                                         loop_counter_def=loop_counter_def,
                                         reponse_ptr=reponse_ptr,
                                         request_size=request_size,
                                         response_size=response_size,
                                         unknown_bricklet_seq_num_hack=seq_num_hack)

        # high-level
        template_stream_in = """
int tf_{device_name_under}_{name_under}(TF_{device_name_camel} *{device_name_under}{high_level_parameters}) {{
	int ret = TF_E_OK;
	{stream_length_type} {stream_name_under}_chunk_offset = 0;
	{chunk_data_type} {stream_name_under}_chunk_data[{chunk_cardinality}];
	{stream_length_type} {stream_name_under}_chunk_length;

	if ({stream_name_under}_length == 0) {{
		memset(&{stream_name_under}_chunk_data, 0, sizeof({chunk_data_type}) * {chunk_cardinality});

		ret = tf_{device_name_under}_{name_under}_low_level({device_name_under}{parameters});
	}} else {{

		while ({stream_name_under}_chunk_offset < {stream_name_under}_length) {{
			{stream_name_under}_chunk_length = {stream_name_under}_length - {stream_name_under}_chunk_offset;

			if ({stream_name_under}_chunk_length > {chunk_cardinality}) {{
				{stream_name_under}_chunk_length = {chunk_cardinality};
			}}

			memcpy({stream_name_under}_chunk_data, &{stream_name_under}[{stream_name_under}_chunk_offset], sizeof({chunk_data_type}) * {stream_name_under}_chunk_length);
			memset(&{stream_name_under}_chunk_data[{stream_name_under}_chunk_length], 0, sizeof({chunk_data_type}) * ({chunk_cardinality} - {stream_name_under}_chunk_length));

			ret = tf_{device_name_under}_{name_under}_low_level({device_name_under}{parameters});

			if (ret != TF_E_OK) {{
				break;
			}}

			{stream_name_under}_chunk_offset += {chunk_cardinality};
		}}

	}}

	return ret;
}}
"""
        template_stream_in_fixed_length = """
int tf_{device_name_under}_{name_under}(TF_{device_name_camel} *{device_name_under}{high_level_parameters}) {{
	int ret = TF_E_OK;
	{stream_length_type} {stream_name_under}_length = {fixed_length};
	{stream_length_type} {stream_name_under}_chunk_offset = 0;
	{chunk_data_type} {stream_name_under}_chunk_data[{chunk_cardinality}];
	{stream_length_type} {stream_name_under}_chunk_length;

	while ({stream_name_under}_chunk_offset < {stream_name_under}_length) {{
		{stream_name_under}_chunk_length = {stream_name_under}_length - {stream_name_under}_chunk_offset;

		if ({stream_name_under}_chunk_length > {chunk_cardinality}) {{
			{stream_name_under}_chunk_length = {chunk_cardinality};
		}}

		memcpy({stream_name_under}_chunk_data, &{stream_name_under}[{stream_name_under}_chunk_offset], sizeof({chunk_data_type}) * {stream_name_under}_chunk_length);
		memset(&{stream_name_under}_chunk_data[{stream_name_under}_chunk_length], 0, sizeof({chunk_data_type}) * ({chunk_cardinality} - {stream_name_under}_chunk_length));

		ret = tf_{device_name_under}_{name_under}_low_level({device_name_under}{parameters});

		if (ret < TF_E_OK) {{
			break;
		}}

		{stream_name_under}_chunk_offset += {chunk_cardinality};
	}}

	return ret;
}}
"""
        template_stream_in_short_write = """
int tf_{device_name_under}_{name_under}(TF_{device_name_camel} *{device_name_under}{high_level_parameters}) {{
	int ret = TF_E_OK;
	{stream_length_type} {stream_name_under}_chunk_offset = 0;
	{chunk_data_type} {stream_name_under}_chunk_data[{chunk_cardinality}];
	{stream_length_type} {stream_name_under}_chunk_length;
	uint8_t {stream_name_under}_chunk_written;

	*ret_{stream_name_under}_written = 0;

	if ({stream_name_under}_length == 0) {{
		memset(&{stream_name_under}_chunk_data, 0, sizeof({chunk_data_type}) * {chunk_cardinality});

		ret = tf_{device_name_under}_{name_under}_low_level({device_name_under}{parameters});

		if (ret != TF_E_OK) {{
			return ret;
		}}

		*ret_{stream_name_under}_written = {stream_name_under}_chunk_written;
	}} else {{

		while ({stream_name_under}_chunk_offset < {stream_name_under}_length) {{
			{stream_name_under}_chunk_length = {stream_name_under}_length - {stream_name_under}_chunk_offset;

			if ({stream_name_under}_chunk_length > {chunk_cardinality}) {{
				{stream_name_under}_chunk_length = {chunk_cardinality};
			}}

			memcpy({stream_name_under}_chunk_data, &{stream_name_under}[{stream_name_under}_chunk_offset], sizeof({chunk_data_type}) * {stream_name_under}_chunk_length);
			memset(&{stream_name_under}_chunk_data[{stream_name_under}_chunk_length], 0, sizeof({chunk_data_type}) * ({chunk_cardinality} - {stream_name_under}_chunk_length));

			ret = tf_{device_name_under}_{name_under}_low_level({device_name_under}{parameters});

			if (ret != TF_E_OK) {{
				*ret_{stream_name_under}_written = 0;

				break;
			}}

			*ret_{stream_name_under}_written += {stream_name_under}_chunk_written;

			if ({stream_name_under}_chunk_written < {chunk_cardinality}) {{
				break; // either last chunk or short write
			}}

			{stream_name_under}_chunk_offset += {chunk_cardinality};
		}}

	}}

	return ret;
}}
"""
        template_stream_in_single_chunk = """
int tf_{device_name_under}_{name_under}(TF_{device_name_camel} *{device_name_under}{high_level_parameters}) {{
	{chunk_data_type} {stream_name_under}_data[{chunk_cardinality}];

	if ({stream_name_under}_length > {chunk_cardinality}) {{
		return TF_E_INVALID_PARAMETER;
	}}

	memcpy({stream_name_under}_data, {stream_name_under}, sizeof({chunk_data_type}) * {stream_name_under}_length);
	memset(&{stream_name_under}_data[{stream_name_under}_length], 0, sizeof({chunk_data_type}) * ({chunk_cardinality} - {stream_name_under}_length));

	return tf_{device_name_under}_{name_under}_low_level({device_name_under}{parameters});
}}
"""
        template_stream_in_short_write_single_chunk = """
int tf_{device_name_under}_{name_under}(TF_{device_name_camel} *{device_name_under}{high_level_parameters}) {{
	int ret = TF_E_OK;
	{chunk_data_type} {stream_name_under}_data[{chunk_cardinality}];
	uint8_t {stream_name_under}_written = 0;

	if ({stream_name_under}_length > {chunk_cardinality}) {{
		return TF_E_INVALID_PARAMETER;
	}}

	memcpy({stream_name_under}_data, {stream_name_under}, sizeof({chunk_data_type}) * {stream_name_under}_length);
	memset(&{stream_name_under}_data[{stream_name_under}_length], 0, sizeof({chunk_data_type}) * ({chunk_cardinality} - {stream_name_under}_length));

	ret = tf_{device_name_under}_{name_under}_low_level({device_name_under}{parameters});

	if (ret != TF_E_OK) {{
		return ret;
	}}

	*ret_{stream_name_under}_written = {stream_name_under}_written;

	return ret;
}}
"""
        template_stream_out = """
int tf_{device_name_under}_{name_under}(TF_{device_name_camel} *{device_name_under}{high_level_parameters}) {{
	int ret = TF_E_OK;
	{stream_length_type} {stream_name_under}_length = {fixed_length};
	{stream_length_type} {stream_name_under}_chunk_offset;
	{chunk_data_type} {stream_name_under}_chunk_data[{chunk_cardinality}];
	bool {stream_name_under}_out_of_sync;
	{stream_length_type} {stream_name_under}_chunk_length;

	*ret_{stream_name_under}_length = 0;

	ret = tf_{device_name_under}_{name_under}_low_level({device_name_under}{parameters});

	if (ret != TF_E_OK) {{
		return ret;
	}}{chunk_offset_check}

	{stream_name_under}_out_of_sync = {stream_name_under}_chunk_offset != 0;

	if (!{stream_name_under}_out_of_sync) {{
		{stream_name_under}_chunk_length = {stream_name_under}_length - {stream_name_under}_chunk_offset;

		if ({stream_name_under}_chunk_length > {chunk_cardinality}) {{
			{stream_name_under}_chunk_length = {chunk_cardinality};
		}}

		memcpy(ret_{stream_name_under}, {stream_name_under}_chunk_data, sizeof({chunk_data_type}) * {stream_name_under}_chunk_length);
		*ret_{stream_name_under}_length = {stream_name_under}_chunk_length;

		while (*ret_{stream_name_under}_length < {stream_name_under}_length) {{
			ret = tf_{device_name_under}_{name_under}_low_level({device_name_under}{parameters});

			if (ret != TF_E_OK) {{
				return ret;
			}}

			{stream_name_under}_out_of_sync = {stream_name_under}_chunk_offset != *ret_{stream_name_under}_length;

			if ({stream_name_under}_out_of_sync) {{
				break;
			}}

			{stream_name_under}_chunk_length = {stream_name_under}_length - {stream_name_under}_chunk_offset;

			if ({stream_name_under}_chunk_length > {chunk_cardinality}) {{
				{stream_name_under}_chunk_length = {chunk_cardinality};
			}}

			memcpy(&ret_{stream_name_under}[*ret_{stream_name_under}_length], {stream_name_under}_chunk_data, sizeof({chunk_data_type}) * {stream_name_under}_chunk_length);
			*ret_{stream_name_under}_length += {stream_name_under}_chunk_length;
		}}
	}}

	if ({stream_name_under}_out_of_sync) {{
		*ret_{stream_name_under}_length = 0; // return empty array

		// discard remaining stream to bring it back in-sync
		while ({stream_name_under}_chunk_offset + {chunk_cardinality} < {stream_name_under}_length) {{
			ret = tf_{device_name_under}_{name_under}_low_level({device_name_under}{parameters});

			if (ret != TF_E_OK) {{
				return ret;
			}}
		}}

		ret = TF_E_STREAM_OUT_OF_SYNC;
	}}

	return ret;
}}
"""
        template_stream_out_chunk_offset_check = """

	if ({stream_name_under}_chunk_offset == (1 << {shift_size}) - 1) {{ // maximum chunk offset -> stream has no data
		return ret;
	}}"""
        template_stream_out_single_chunk = """
int tf_{device_name_under}_{name_under}(TF_{device_name_camel} *{device_name_under}{high_level_parameters}) {{
	int ret = TF_E_OK;
	{stream_length_type} {stream_name_under}_length;
	{chunk_data_type} {stream_name_under}_data[{chunk_cardinality}];

	*ret_{stream_name_under}_length = 0;

	ret = tf_{device_name_under}_{name_under}_low_level({device_name_under}{parameters});

	if (ret != TF_E_OK) {{
		return ret;
	}}

	memcpy(ret_{stream_name_under}, {stream_name_under}_data, sizeof({chunk_data_type}) * {stream_name_under}_length);
	memset(&{stream_name_under}_data[{stream_name_under}_length], 0, sizeof({chunk_data_type}) * ({chunk_cardinality} - {stream_name_under}_length));

	*ret_{stream_name_under}_length = {stream_name_under}_length;

	return ret;
}}
"""

        for packet in self.get_packets('function'):
            stream_in = packet.get_high_level('stream_in')
            stream_out = packet.get_high_level('stream_out')

            if stream_in != None:
                length_element = stream_in.get_length_element()
                chunk_offset_element = stream_in.get_chunk_offset_element()

                if length_element != None:
                    stream_length_type = length_element.get_c_type('default')
                elif chunk_offset_element != None:
                    stream_length_type = chunk_offset_element.get_c_type('default')

                if stream_in.get_fixed_length() != None:
                    template = template_stream_in_fixed_length
                elif stream_in.has_short_write() and stream_in.has_single_chunk():
                    template = template_stream_in_short_write_single_chunk
                elif stream_in.has_short_write():
                    template = template_stream_in_short_write
                elif stream_in.has_single_chunk():
                    template = template_stream_in_single_chunk
                else:
                    template = template_stream_in

                functions += template.format(device_name_camel=self.get_name().camel,
                                             device_name_under=self.get_name().under,
                                             name_under=packet.get_name(skip=-2).under,
                                             parameters=common.wrap_non_empty(', ', packet.get_c_arguments('default'), ''),
                                             high_level_parameters=common.wrap_non_empty(', ', packet.get_c_parameters(high_level=True), ''),
                                             stream_name_under=stream_in.get_name().under,
                                             stream_length_type=stream_length_type,
                                             fixed_length=stream_in.get_fixed_length(),
                                             chunk_data_type=stream_in.get_chunk_data_element().get_c_type('default'),
                                             chunk_cardinality=stream_in.get_chunk_data_element().get_cardinality())
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
                    chunk_offset_check = template_stream_out_chunk_offset_check.format(stream_name_under=stream_out.get_name().under,
                                                                                       shift_size=int(stream_out.get_chunk_offset_element().get_type().replace('uint', '')))
                else:
                    chunk_offset_check = ''

                functions += template.format(device_name_camel=self.get_name().camel,
                                             device_name_under=self.get_name().under,
                                             name_under=packet.get_name(skip=-2).under,
                                             parameters=common.wrap_non_empty(', ', packet.get_c_arguments('default'), ''),
                                             high_level_parameters=common.wrap_non_empty(', ', packet.get_c_parameters(high_level=True), ''),
                                             stream_name_under=stream_out.get_name().under,
                                             stream_length_type=stream_length_type,
                                             fixed_length=stream_out.get_fixed_length(default='0'),
                                             chunk_offset_check=chunk_offset_check,
                                             chunk_data_type=stream_out.get_chunk_data_element().get_c_type('default'),
                                             chunk_cardinality=stream_out.get_chunk_data_element().get_cardinality())

        return functions

    def get_c_register_callback_functions(self):
        if self.get_callback_count() == 0:
            return '\n'

        result = []

        template = """
void tf_{device_under}_register_{packet_under}_callback(TF_{device_camel} *{device_under}, TF_{device_camel}{packet_camel}Handler handler, void *user_data) {{
    {device_under}->{packet_under}_handler = handler;
    {device_under}->{packet_under}_user_data = user_data;
}}
"""
        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                continue
            result.append(format(template, self, packet))

        return '\n'.join(result)

    def get_c_callback_handler(self):
        template = """
static bool tf_{device_under}_callback_handler(void *dev, uint8_t fid, TF_Packetbuffer *payload) {{
    TF_{device_camel} *{device_under} = (TF_{device_camel} *) dev;

    switch(fid) {{
{cases}
        default:
            return false;
    }}

    return true;
}}"""

        case_template = """
        case TF_{device_upper}_CALLBACK_{packet_upper}: {{
            TF_{device_camel}{packet_camel}Handler fn = {device_under}->{packet_under}_handler;
            void *user_data = {device_under}->{packet_under}_user_data;
            if (fn == NULL)
                return false;
{i_decl}
{extract_payload}
            tf_tfp_packet_processed(&{device_under}->tfp);

            fn({device_under}, {params}user_data);
            break;
        }}"""

        cases = []
        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                continue
            extract_payload, needs_i = packet.get_c_return_list('payload', context='callback_handler')

            cases.append(format(case_template, self, packet,
                                extract_payload=common.wrap_non_empty('            ', '\n            '.join(extract_payload), ''),
                                params=common.wrap_non_empty('', packet.get_c_arguments(context='callback_wrapper'), ', '),
                                i_decl = '' if not needs_i else '            int i;'))
        return format(template, self, cases='\n'.join(cases))

    def get_c_callback_wrapper_functions(self):
        return ''

        functions = ''

        # high-level
        template_stream_out = """
static void {device_name_under}_callback_wrapper_{name_under}(DevicePrivate *device_p{parameters}) {{
	{name_camel}_CallbackFunction callback_function;
	void *user_data = device_p->registered_callback_user_data[DEVICE_NUM_FUNCTION_IDS + {device_name_upper}_CALLBACK_{name_upper}];
	HighLevelCallback *high_level_callback = &device_p->high_level_callbacks[-{device_name_upper}_CALLBACK_{name_upper}];
	{stream_length_type} {stream_name_under}_chunk_length = {stream_length} - {stream_name_under}_chunk_offset;

	callback_function = ({name_camel}_CallbackFunction)device_p->registered_callbacks[DEVICE_NUM_FUNCTION_IDS + {device_name_upper}_CALLBACK_{name_upper}];

	if ({stream_name_under}_chunk_length > {chunk_cardinality}) {{
		{stream_name_under}_chunk_length = {chunk_cardinality};
	}}

	if (high_level_callback->data == NULL) {{ // no stream in-progress
		if ({stream_name_under}_chunk_offset == 0) {{ // stream starts
			high_level_callback->data = malloc(sizeof({chunk_data_type}) * {stream_length});
			high_level_callback->length = {stream_name_under}_chunk_length;

			memcpy(high_level_callback->data, {stream_name_under}_chunk_data, sizeof({chunk_data_type}) * {stream_name_under}_chunk_length);

			if (high_level_callback->length >= {stream_length}) {{ // stream complete
				if (callback_function != NULL) {{
					callback_function({high_level_parameters}user_data);
				}}

				free(high_level_callback->data);
				high_level_callback->data = NULL;
				high_level_callback->length = 0;
			}}
		}} else {{ // ignore tail of current stream, wait for next stream start
		}}
	}} else {{ // stream in-progress
		if ({stream_name_under}_chunk_offset != high_level_callback->length) {{ // stream out-of-sync
			free(high_level_callback->data);
			high_level_callback->data = NULL;
			high_level_callback->length = 0;

			if (callback_function != NULL) {{
				callback_function({high_level_parameters}user_data);
			}}
		}} else {{ // stream in-sync
			memcpy(&(({chunk_data_type} *)high_level_callback->data)[high_level_callback->length], {stream_name_under}_chunk_data, sizeof({chunk_data_type}) * {stream_name_under}_chunk_length);
			high_level_callback->length += {stream_name_under}_chunk_length;

			if (high_level_callback->length >= {stream_length}) {{ // stream complete
				if (callback_function != NULL) {{
					callback_function({high_level_parameters}user_data);
				}}

				free(high_level_callback->data);
				high_level_callback->data = NULL;
				high_level_callback->length = 0;
			}}
		}}
	}}
}}
"""
        template_stream_out_single_chunk = """
static void {device_name_under}_callback_wrapper_{name_under}(DevicePrivate *device_p{parameters}) {{
	{name_camel}_CallbackFunction callback_function;
	void *user_data = device_p->registered_callback_user_data[DEVICE_NUM_FUNCTION_IDS + {device_name_upper}_CALLBACK_{name_upper}];

	callback_function = ({name_camel}_CallbackFunction)device_p->registered_callbacks[DEVICE_NUM_FUNCTION_IDS + {device_name_upper}_CALLBACK_{name_upper}];

	if (callback_function != NULL) {{
		callback_function({high_level_parameters}user_data);
	}}
}}
"""

        for packet in self.get_packets('callback'):
            stream_out = packet.get_high_level('stream_out')

            if stream_out != None:
                if stream_out.has_single_chunk():
                    template = template_stream_out_single_chunk
                else:
                    template = template_stream_out

                stream_length = 'stream_length'
                length_element = stream_out.get_length_element()
                chunk_offset_element = stream_out.get_chunk_offset_element()

                if length_element != None:
                    stream_length = length_element.get_name().under
                    stream_length_type = length_element.get_c_type('default')
                elif chunk_offset_element != None:
                    stream_length_type = chunk_offset_element.get_c_type('default')

                functions += template.format(device_name_under=packet.get_device().get_name().under,
                                             device_name_upper=packet.get_device().get_name().upper,
                                             name_under=packet.get_name(skip=-2).under,
                                             name_upper=packet.get_name(skip=-2).upper,
                                             name_camel=packet.get_name(skip=-2).camel,
                                             parameters=common.wrap_non_empty(', ', packet.get_c_parameters(), ''),
                                             high_level_parameters=common.wrap_non_empty('', packet.get_c_arguments('callback_wrapper', high_level=True, single_chunk=stream_out.has_single_chunk()), ', '),
                                             stream_name_under=stream_out.get_name().under,
                                             stream_length_type=stream_length_type,
                                             stream_length=stream_out.get_fixed_length(default=stream_length),
                                             chunk_data_type=stream_out.get_chunk_data_element().get_c_type('default'),
                                             chunk_cardinality=stream_out.get_chunk_data_element().get_cardinality())

        # normal and low-level
        template_normal = """
static void {device_name_under}_callback_wrapper_{packet_name_under}(DevicePrivate *device_p, Packet *packet) {{
	{packet_name_camel}_CallbackFunction callback_function;
	void *user_data;
	{packet_name_camel}_Callback *callback;{loop_index_decl}{bool_unpack_decls}{alignment_copies}

	if (packet->header.length != sizeof({packet_name_camel}_Callback)) {{
		return; // silently ignoring callback with wrong length
	}}

	callback_function = ({packet_name_camel}_CallbackFunction)device_p->registered_callbacks[DEVICE_NUM_FUNCTION_IDS + {fid}];
	user_data = device_p->registered_callback_user_data[DEVICE_NUM_FUNCTION_IDS + {fid}];
	callback = ({packet_name_camel}_Callback *)packet;
	(void)callback; // avoid unused variable warning

	if (callback_function == NULL) {{
		return;
	}}
{endian_conversions}{bool_unpacks}
	callback_function({callback_args}{callback_args_comma}user_data);
}}
"""
        template_low_level = """
static void {device_name_under}_callback_wrapper_{packet_name_under}(DevicePrivate *device_p, Packet *packet) {{
	{packet_name_camel}_CallbackFunction callback_function;
	void *user_data;
	{packet_name_camel}_Callback *callback;{loop_index_decl}{bool_unpack_decls}{alignment_copies}

	if (packet->header.length != sizeof({packet_name_camel}_Callback)) {{
		return; // silently ignoring callback with wrong length
	}}

	callback_function = ({packet_name_camel}_CallbackFunction)device_p->registered_callbacks[DEVICE_NUM_FUNCTION_IDS + {fid}];
	user_data = device_p->registered_callback_user_data[DEVICE_NUM_FUNCTION_IDS + {fid}];
	callback = ({packet_name_camel}_Callback *)packet;
	(void)callback; // avoid unused variable warning

{endian_conversions}{bool_unpacks}
	{device_name_under}_callback_wrapper_{ll_packet_name_under}(device_p, {callback_args});

	if (callback_function != NULL) {{
		callback_function({callback_args}{callback_args_comma}user_data);
	}}
}}
"""
        for packet in self.get_packets('callback'):
            callback_arg_list = []

            for element in packet.get_elements():
                if element.get_type() == 'bool':
                    callback_arg_list.append('unpacked_{0}'.format(element.get_name().under))
                else:
                    callback_arg_list.append('callback->{0}'.format(element.get_name().under))

            endian_list = []
            loop_index_decl = ''
            bool_unpack_decls = ''
            bool_unpacks = ''

            # GCC 9.1 upwards warns (correctly) if a pointer to a member of a packed struct is accessed.
            # Such code is only generated for arrays of types > 1 byte in callback wrappers.
            # Fortunately all those arrays are accessed anyway by the little endian conversion.
            # Assigning the converted values into an aligned array fixes the issue.
            alignment_copy_list = []

            for element in packet.get_elements():
                if element.get_type() == 'bool':
                    if element.get_cardinality() > 1:
                        loop_index_decl = '\n\tint i;'
                        bool_unpack_decls += '\n\tbool unpacked_{0}[{1}];'.format(element.get_name().under, element.get_cardinality())
                        bool_unpacks += '\tfor (i = 0; i < {1}; i++) unpacked_{0}[i] = (callback->{0}[i / 8] & (1 << (i % 8))) != 0;\n' \
                                    .format(element.get_name().under, element.get_cardinality())
                    else:
                        bool_unpack_decls += '\n\tbool unpacked_{0};'.format(element.get_name().under)
                        bool_unpacks += '\tunpacked_{0} = callback->{0} != 0;\n'.format(element.get_name().under)
                elif element.get_item_size() > 1:
                    if element.get_cardinality() > 1:
                        template = "\t{type} aligned_{name}[{size}];"
                        alignment_copy_list.append(template.format(type=element.get_c_type('default'), name=element.get_name().under, size=element.get_cardinality()))
                        callback_arg_list = [elem if elem != "callback->" + element.get_name().under else "aligned_" + element.get_name().under for elem in callback_arg_list]
                        loop_index_decl = '\n\tint i;'
                        endian_list.append('\tfor (i = 0; i < {2}; i++) aligned_{0}[i] = tf_leconvert_{1}_from(callback->{0}[i]);' \
                                           .format(element.get_name().under, element.get_type(), element.get_cardinality()))
                    else:
                        endian_list.append('\tcallback->{0} = tf_leconvert_{1}_from(callback->{0});'.format(element.get_name().under, element.get_type()))

            if packet.get_high_level('stream_out') != None:
                template = template_low_level
                ll_packet_name_under = packet.get_name(skip=-2).under
            else:
                template = template_normal
                ll_packet_name_under = ''

            fid = '{0}_CALLBACK_{1}'.format(self.get_name().upper, packet.get_name().upper)

            functions += template.format(device_name_under=self.get_name().under,
                                         packet_name_under=packet.get_name().under,
                                         device_name_camel=self.get_name().camel,
                                         packet_name_camel=packet.get_name().camel,
                                         callback_args=', '.join(callback_arg_list),
                                         callback_args_comma=', ' if len(callback_arg_list) > 0 else '',
                                         endian_conversions=common.wrap_non_empty('\n', '\n'.join(endian_list), '\n'),
                                         fid=fid,
                                         loop_index_decl=loop_index_decl,
                                         bool_unpack_decls=bool_unpack_decls,
                                         bool_unpacks=bool_unpacks,
                                         ll_packet_name_under=ll_packet_name_under,
                                         alignment_copies=common.wrap_non_empty('\n', '\n'.join(alignment_copy_list), '\n'))

        return functions

    def get_c_include_h(self):
        template = """{header_comment}
#ifndef TF_{category_upper}_{device_upper}_H
#define TF_{category_upper}_{device_upper}_H

#include "tfp.h"
#include "hal_common.h"
#include "macros.h"

#ifdef __cplusplus
extern "C" {{
#endif

/**
 * \\defgroup {category_camel}{device_camel} {display_name}
 */

struct TF_{device_camel};

{callback_typedefs}

/**
 * \\ingroup {category_camel}{device_camel}
 *
 * {description}
 */
typedef struct TF_{device_camel} {{
    TF_TfpContext tfp;
{callback_handlers}
    uint8_t response_expected[{mapped_bytes}];
}} TF_{device_camel};
"""
        mapped_id_count = len([p for p in self.get_packets('function') if p.get_response_expected() != 'always_true'])

        cb_handler_template = """    TF_{device_camel}{cb_camel}Handler {cb_under}_handler;
    void *{cb_under}_user_data;
"""
        cb_handlers = [cb_handler_template.format(device_camel=self.get_name().camel,
                                                  cb_camel=cb.get_name().camel,
                                                  cb_under=cb.get_name().under)
                        for cb in self.get_packets('callback') if not cb.has_high_level()]

        return template.format(header_comment=self.get_generator().get_header_comment('asterisk'),
                               category_upper=self.get_category().upper,
                               device_upper=self.get_name().upper,
                               device_camel=self.get_name().camel,
                               category_camel=self.get_category().camel,
                               callback_typedefs=self.get_c_typedefs(),
                               callback_handlers='\n'.join(cb_handlers),
                               description=common.select_lang(self.get_description()),
                               display_name=self.get_long_display_name(),
                               mapped_bytes=math.ceil(mapped_id_count / 8.0))

    def get_c_end_h(self):
        return "\n#ifdef __cplusplus\n}\n#endif\n\n#endif\n"

    def get_c_end_c(self):
        return "\n#ifdef __cplusplus\n}\n#endif\n"

    def get_c_typedefs(self):
        typedefs = '\n'
        template = """typedef void (*TF_{device_camel}{cb_camel}Handler)(struct TF_{device_camel} *device, {params}void *user_data);
"""

        # normal and low-level
        for packet in self.get_packets('callback'):

            typedefs += template.format(device_camel=self.get_name().camel,
                                        device_under=self.get_name().under,
                                        cb_camel=packet.get_name().camel,
                                        params=common.wrap_non_empty('', packet.get_c_parameters(), ', '))

        # high-level
        for packet in self.get_packets('callback'):
            if not packet.has_high_level():
                continue

            typedefs += template.format(device_camel=self.get_name().camel,
                                        device_under=self.get_name().under,
                                        cb_camel=packet.get_name(skip=-2).camel,
                                        params=common.wrap_non_empty('', packet.get_c_parameters(high_level=True), ', '))

        return typedefs

    def get_c_create_declaration(self):
        template = """
/**
 * \\ingroup {2}{1}
 *
 * Creates the device object \\c {0} with the unique device ID \\c uid and adds
 * it to the IPConnection \\c ipcon.
 */
int tf_{0}_create(TF_{1} *{0}, const char *uid, TF_HalContext *hal);
"""

        unknown_template = """
/**
 * \\ingroup {2}{1}
 *
 * Creates the device object \\c {0} with the unique device ID \\c uid and adds
 * it to the IPConnection \\c ipcon.
 */
int tf_{0}_create(TF_{1} *{0}, const char *uid, TF_HalContext *hal, int port_id, int inventory_index);
"""
        if self.get_name().under == 'unknown':
            template = unknown_template

        return template.format(self.get_name().under,
                               self.get_name().camel,
                               self.get_category().camel)

    def get_c_destroy_declaration(self):
        template = """
/**
 * \\ingroup {2}{1}
 *
 * Removes the device object \\c {0} from its IPConnection and destroys it.
 * The device object cannot be used anymore afterwards.
 */
void tf_{0}_destroy(TF_{1} *{0});
"""
        return template.format(self.get_name().under,
                               self.get_name().camel,
                               self.get_category().camel)

    def get_c_response_expected_declarations(self):
        template = """
/**
 * \\ingroup {2}{1}
 *
 * Returns the response expected flag for the function specified by the
 * \\c function_id parameter. It is *true* if the function is expected to
 * send a response, *false* otherwise.
 *
 * For getter functions this is enabled by default and cannot be disabled,
 * because those functions will always send a response. For callback
 * configuration functions it is enabled by default too, but can be disabled
 * via the {0}_set_response_expected function. For setter functions it is
 * disabled by default and can be enabled.
 *
 * Enabling the response expected flag for a setter function allows to
 * detect timeouts and other error conditions calls of this setter as well.
 * The device will then send a response for this purpose. If this flag is
 * disabled for a setter function then no response is sent and errors are
 * silently ignored, because they cannot be detected.
 */
int tf_{0}_get_response_expected(TF_{1} *{0}, uint8_t function_id, bool *ret_response_expected);

/**
 * \\ingroup {2}{1}
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
int tf_{0}_set_response_expected(TF_{1} *{0}, uint8_t function_id, bool response_expected);

/**
 * \\ingroup {2}{1}
 *
 * Changes the response expected flag for all setter and callback configuration
 * functions of this device at once.
 */
void tf_{0}_set_response_expected_all(TF_{1} *{0}, bool response_expected);
"""
        return template.format(self.get_name().under,
                               self.get_name().camel,
                               self.get_category().camel)

    def get_c_function_declaration(self):
        functions = ''

        # normal and low-level
        template = """
/**
 * \\ingroup {category}{device_name_camel}
 *
 * {doc}
 */
TF_ATTRIBUTE_NONNULL int tf_{device_name_under}_{function_name}(TF_{device_name_camel} *{device_name_under}{parameters});
"""
        functions += template.format(category=self.get_category().camel,
                                     device_name_camel=self.get_name().camel,
                                     device_name_under=self.get_name().under,
                                     doc='Returns the API version (major, minor, release) of the bindings for this\n * device.',
                                     function_name='get_api_version',
                                     parameters=', uint8_t ret_api_version[3]')

        for packet in self.get_packets('function'):
            functions += template.format(category=self.get_category().camel,
                                         device_name_camel=self.get_name().camel,
                                         device_name_under=self.get_name().under,
                                         doc=packet.get_c_formatted_doc(),
                                         function_name=packet.get_name().under,
                                         parameters=common.wrap_non_empty(', ', packet.get_c_parameters(), ''))

        # high-level
        for packet in self.get_packets('function'):
            if packet.has_high_level():
                functions += template.format(category=self.get_category().camel,
                                             device_name_camel=self.get_name().camel,
                                             device_name_under=self.get_name().under,
                                             doc=packet.get_c_formatted_doc(),
                                             function_name=packet.get_name(skip=-2).under,
                                             parameters=common.wrap_non_empty(', ', packet.get_c_parameters(high_level=True), ''))

        return functions

    def get_c_register_callback_declarations(self):
        if self.get_callback_count() == 0:
            return '\n'

        result = []

        template = """
/**
 * \\ingroup {category_camel}{device_camel}
 *
 * Registers the given \\c function with the given \\c callback_id. The
 * \\c user_data will be passed as the last parameter to the \\c function.
 */
void tf_{device_under}_register_{packet_under}_callback(TF_{device_camel} *{device_under}, TF_{device_camel}{packet_camel}Handler handler, void *user_data);
"""

        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                continue
            result.append(format(template, self, packet))

        return '\n'.join(result)

    def get_c_source(self):
        source  = self.get_c_include_c()
        source += self.get_c_callback_wrapper_functions()
        source += self.get_c_callback_handler()
        source += self.get_c_create_function()
        source += self.get_c_destroy_function()
        source += self.get_c_response_expected_functions()

        source += self.get_c_functions()
        source += self.get_c_register_callback_functions()

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
        header += self.get_c_function_declaration()
        header += self.get_c_end_h()

        return header

    def get_c_symbols(self):
        symbols = []
        name = self.get_name().under

        symbols.append('tf_{0}_create'.format(name))
        symbols.append('tf_{0}_destroy'.format(name))
        symbols.append('tf_{0}_get_response_expected'.format(name))
        symbols.append('tf_{0}_set_response_expected'.format(name))
        symbols.append('tf_{0}_set_response_expected_all'.format(name))

        if self.get_callback_count() > 0:
            symbols.append('tf_{0}_register_callback'.format(name))

        symbols.append('tf_{0}_get_api_version'.format(name))

        # normal and low-level
        for packet in self.get_packets('function'):
            symbols.append('tf_{0}_{1}'.format(name, packet.get_name().under))

        # high-level
        for packet in self.get_packets('function'):
            if packet.has_high_level():
                symbols.append('tf_{0}_{1}'.format(name, packet.get_name(skip=-2).under))

        return '\n'.join(symbols) + '\n'

class CBindingsPacket(embedded_c_common.CPacket):
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
                struct_body.append('\t{0} {1}[{2}];\n'.format(c_type, name, element.get_c_array_length()))
            else:
                struct_body.append('\t{0} {1};\n'.format(c_type, name))

        return ''.join(struct_body)

    def get_c_struct_list(self):
        struct_list = ''
        needs_i = False

        offset = 0
        for element in self.get_elements(direction='in'):

            if element.get_type() == 'string':
                temp = '\n\tmemcpy(buf + {offset}, {src}, {count});\n'
                struct_list += temp.format(src=element.get_name().under, offset=offset, count=element.get_cardinality())
                offset += element.get_cardinality()
            elif element.get_type() == 'bool':
                if element.get_cardinality() > 1:
                    needs_i = True
                    byte_count = math.ceil(element.get_cardinality() / 8.0)
                    struct_list += '\n\tmemset(buf + {offset}, 0, {byte_count}); for (i = 0; i < {count}; ++i) buf[{offset} + (i / 8)] |= ({src}[i] ? 1 : 0) << (i % 8);' \
                                   .format(src=element.get_name().under, offset=offset, count=element.get_cardinality(), byte_count=math.ceil(element.get_cardinality() / 8.0))
                    offset += byte_count
                else:
                    struct_list += '\n\tbuf[{offset}] = {src} ? 1 : 0;'.format(offset=offset, src=element.get_name().under)
                    offset += 1
            elif element.get_cardinality() > 1:
                if element.get_item_size() > 1:
                    needs_i = True
                    struct_list += '\n\tfor (i = 0; i < {count}; i++) buf[{offset} + i] = tf_leconvert_{type_}_to({src}[i]);' \
                                   .format(src=element.get_name().under, type_=element.get_type(), count=element.get_cardinality(), offset=offset)
                else:
                    temp = '\n\tmemcpy(buf + {offset}, {src}, {count});'
                    struct_list += temp.format(offset=offset,
                                               src=element.get_name().under,
                                               count=element.get_cardinality())
                offset += element.get_cardinality() * element.get_item_size()
            elif element.get_item_size() > 1:
                struct_list += '\n\t{src} = tf_leconvert_{type_}_to({src}); memcpy(buf + {offset}, &{src}, {count});'.format(src=element.get_name().under, type_=element.get_type(), offset=offset, count=element.get_item_size())
                offset += element.get_item_size()
            elif element.get_type() == 'char':
                # Fixes clang -Weverything complaining about sign conversion
                struct_list += '\n\tbuf[{offset}] = (uint8_t){src};'.format(src=element.get_name().under, offset=offset)
                offset += 1
            else:
                struct_list += '\n\tbuf[{offset}] = {src};'.format(src=element.get_name().under, offset=offset)
                offset += 1

        return struct_list, needs_i

    def get_c_return_list(self, packetbuffer_name, context):
        assert context in ['callback_handler', 'getter']
        return_list = []
        needs_i = False

        for element in self.get_elements(direction='out'):
            if element.get_cardinality() > 1:
                if context == 'callback_handler':
                    t = '{type_} {dest}[{count}]; '
                else:
                    t = ''

                if element.get_type() == 'string':
                    t += 'tf_packetbuffer_pop_n({packetbuffer}, (uint8_t*){dest}, {count});'
                elif element.get_type() == 'bool':
                    t += "tf_packetbuffer_read_bool_array({packetbuffer}, {dest}, {count});"
                else:
                    t += 'for (i = 0; i < {count}; ++i) {dest}[i] = tf_packetbuffer_read_{type_}({packetbuffer});'
                    needs_i = True

            else:
                if context == 'callback_handler':
                    t = '{type_} {dest} = tf_packetbuffer_read_{type_}({packetbuffer});'
                else:
                    t = '*{dest} = tf_packetbuffer_read_{type_}({packetbuffer});'

            return_list.append(t.format(packetbuffer=packetbuffer_name,
                                        dest=('ret_' if context == 'getter' else '') + element.get_name().under,
                                        count=element.get_cardinality(),
                                        item_size=element.get_item_size(),
                                        type_=element.get_c_type('default')))

        return return_list, needs_i

class CBindingsGenerator(embedded_c_common.CGeneratorTrait, common.BindingsGenerator):
    def get_device_class(self):
        return CBindingsDevice

    def get_packet_class(self):
        return CBindingsPacket

    def get_element_class(self):
        return embedded_c_common.CElement

    def generate(self, device):
        if not device.has_comcu():
            return
        filename = '{0}_{1}'.format(device.get_category().under, device.get_name().under)

        with open(os.path.join(self.get_bindings_dir(), filename + '.c'), 'w') as f:
            f.write(device.get_c_source())

        with open(os.path.join(self.get_bindings_dir(), filename + '.h'), 'w') as f:
            f.write(device.get_c_header())

        with open(os.path.join(self.get_bindings_dir(), filename + '.symbols'), 'w') as f:
            f.write(device.get_c_symbols())

        if device.is_released():
            self.released_files.append(filename + '.c')
            self.released_files.append(filename + '.h')
            self.released_files.append(filename + '.symbols')

def generate(root_dir):
    common.generate(root_dir, 'en', CBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
