#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Bindings Generator
Copyright (C) 2012-2018 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

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
import os
import math

sys.path.append(os.path.split(os.getcwd())[0])
import common
import c_common

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

#define IPCON_EXPOSE_INTERNALS

#include "{1}_{2}.h"

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
#define {0}_FUNCTION_{1} {2}
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
#define {0}_CALLBACK_{1} {2}
"""

        for packet in self.get_packets('callback'):
            defines += template.format(self.get_name().upper,
                                       packet.get_name().upper,
                                       packet.get_function_id(),
                                       packet.get_c_formatted_doc(),
                                       self.get_name().camel,
                                       self.get_category().camel)

        template = """
/**
 * \\ingroup {5}{4}
 *
 * {3}
 */
#define {0}_CALLBACK_{1} (-{2})
"""

        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                defines += template.format(self.get_name().upper,
                                           packet.get_name(skip=-2).upper,
                                           packet.get_function_id(),
                                           packet.get_c_formatted_doc(high_level=True),
                                           self.get_name().camel,
                                           self.get_category().camel)

        if self.get_long_display_name() == 'RS232 Bricklet':
            defines += """
/**
 * \\ingroup BrickletRS232
 *
 * Signature: \\code void callback(char ret_message[60], uint8_t length, void *user_data) \\endcode
 *
 * This callback is called if new data is available. The message has
 * a maximum size of 60 characters. The actual length of the message
 * is given in addition.
 *
 * To enable this callback, use {@link rs232_enable_read_callback}.
 */
#define RS232_CALLBACK_READ_CALLBACK RS232_CALLBACK_READ // for backward compatibility

/**
 * \\ingroup BrickletRS232
 *
 * Signature: \\code void callback(uint8_t error, void *user_data) \\endcode
 *
 * This callback is called if an error occurs.
 * Possible errors are overrun, parity or framing error.
 *
 * .. versionadded:: 2.0.1$nbsp;(Plugin)
 */
#define RS232_CALLBACK_ERROR_CALLBACK RS232_CALLBACK_ERROR // for backward compatibility
"""

        return defines

    def get_c_constants(self):
        constant_format = """
/**
 * \\ingroup {doxygen}
 */
#define {device_name}_{constant_group_name_upper}_{constant_name_upper} {constant_value}
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
#define {0}_DEVICE_IDENTIFIER {1}
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
#define {0}_DEVICE_DISPLAY_NAME "{1}"
"""

        return template.format(self.get_name().upper,
                               self.get_long_display_name(),
                               self.get_name().camel,
                               self.get_category().camel)

    def get_c_structs(self):
        structs = """
#if defined _MSC_VER || defined __BORLANDC__
	#pragma pack(push)
	#pragma pack(1)
	#define ATTRIBUTE_PACKED
#elif defined __GNUC__
	#ifdef _WIN32
		// workaround struct packing bug in GCC 4.7 on Windows
		// https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52991
		#define ATTRIBUTE_PACKED __attribute__((gcc_struct, packed))
	#else
		#define ATTRIBUTE_PACKED __attribute__((packed))
	#endif
#else
	#error unknown compiler, do not know how to enable struct packing
#endif
"""

        struct_template = """
typedef struct {{
	PacketHeader header;
{0}}} ATTRIBUTE_PACKED {1}_{2};
"""

        for packet in self.get_packets():
            if packet.get_type() == 'callback':
                structs += struct_template.format(packet.get_c_struct_body(), packet.get_name().camel, 'Callback')
                continue

            structs += struct_template.format(packet.get_c_struct_body(direction='in'), packet.get_name().camel, 'Request')

            if len(packet.get_elements(direction='out')) == 0:
                continue

            structs += struct_template.format(packet.get_c_struct_body(direction='out'), packet.get_name().camel, 'Response')

        structs += """
#if defined _MSC_VER || defined __BORLANDC__
	#pragma pack(pop)
#endif
#undef ATTRIBUTE_PACKED
"""
        return structs

    def get_c_create_function(self):
        template = """
void {0}_create({1} *{0}, const char *uid, IPConnection *ipcon) {{
	DevicePrivate *device_p;

	device_create({0}, uid, ipcon->p, {3}, {4}, {5});

	device_p = {0}->p;
{2}
}}
"""
        cb_temp = """
	device_p->callback_wrappers[{3}_CALLBACK_{1}] = {0}_callback_wrapper_{2};"""
        hlcb_temp = """
	device_p->high_level_callbacks[-{2}_CALLBACK_{1}].exists = true;"""
        callbacks = ''

        for packet in self.get_packets('callback'):
            callbacks += cb_temp.format(self.get_name().under, packet.get_name().upper, packet.get_name().under, self.get_name().upper)

        if len(callbacks) > 0:
            callbacks += '\n'

        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                callbacks += hlcb_temp.format(self.get_name().under, packet.get_name(skip=-2).upper, self.get_name().upper)

        response_expected = ''

        for packet in self.get_packets('function'):
            response_expected += '\tdevice_p->response_expected[{0}_FUNCTION_{1}] = DEVICE_RESPONSE_EXPECTED_{2};\n' \
                                 .format(self.get_name().upper,
                                         packet.get_name().upper,
                                         packet.get_response_expected().upper())

        if len(response_expected) > 0:
            response_expected = '\n' + response_expected

        return template.format(self.get_name().under,
                               self.get_name().camel,
                               response_expected + callbacks,
                               *self.get_api_version())

    def get_c_destroy_function(self):
        template = """
void {0}_destroy({1} *{0}) {{
	device_release({0}->p);
}}
"""
        return template.format(self.get_name().under,
                               self.get_name().camel)

    def get_c_response_expected_functions(self):
        template = """
int {0}_get_response_expected({1} *{0}, uint8_t function_id, bool *ret_response_expected) {{
	return device_get_response_expected({0}->p, function_id, ret_response_expected);
}}

int {0}_set_response_expected({1} *{0}, uint8_t function_id, bool response_expected) {{
	return device_set_response_expected({0}->p, function_id, response_expected);
}}

int {0}_set_response_expected_all({1} *{0}, bool response_expected) {{
	return device_set_response_expected_all({0}->p, response_expected);
}}
"""
        return template.format(self.get_name().under,
                               self.get_name().camel)

    def get_c_functions(self):
        functions = ''

        # normal and low-level
        template_version = """
int {0}_get_api_version({1} *{0}, uint8_t ret_api_version[3]) {{
	return device_get_api_version({0}->p, ret_api_version);
}}
"""
        template = """
int {0}_{1}({2} *{0}{3}) {{
	DevicePrivate *device_p = {0}->p;
	{5}_Request request;{6}
	int ret;{9}

	ret = packet_header_create(&request.header, sizeof(request), {4}, device_p->ipcon_p, device_p);

	if (ret < 0) {{
		return ret;
	}}
{7}
	ret = device_send_request(device_p, (Packet *)&request, {10});
{8}
	return ret;
}}
"""
        template_ret = """
	if (ret < 0) {{
		return ret;
	}}

{2}"""

        device_name = self.get_name().under
        c = self.get_name().camel
        functions += template_version.format(device_name, c)

        for packet in self.get_packets('function'):
            packet_name = packet.get_name().under
            params = common.wrap_non_empty(', ', packet.get_c_parameters(), '')
            fid = '{0}_FUNCTION_{1}'.format(self.get_name().upper,
                                            packet.get_name().upper)
            f = packet.get_name().camel
            h, needs_i = packet.get_c_struct_list()

            if len(h) > 0:
                h += '\n'

            if len(packet.get_elements(direction='out')) > 0:
                g = '\n\t' + f + '_Response response;'
                rl, needs_i2 = packet.get_c_return_list()
                i = template_ret.format(f, device_name, rl)
                r = '(Packet *)&response'
            else:
                g = ''
                i = ''
                needs_i2 = False
                r = 'NULL'

            if needs_i or needs_i2:
                k = '\n\tint i;'
            else:
                k = ''

            functions += template.format(device_name, packet_name, c, params, fid, f, g, h, i, k, r)

        # high-level
        template_stream_in = """
int {device_name_under}_{name_under}({device_name_camel} *{device_name_under}{high_level_parameters}) {{
	DevicePrivate *device_p = {device_name_under}->p;
	int ret;
	{stream_length_type} {stream_name_under}_chunk_offset = 0;
	{chunk_data_type} {stream_name_under}_chunk_data[{chunk_cardinality}];
	{stream_length_type} {stream_name_under}_chunk_length;

	if ({stream_name_under}_length == 0) {{
		memset(&{stream_name_under}_chunk_data, 0, sizeof({chunk_data_type}) * {chunk_cardinality});

		ret = {device_name_under}_{name_under}_low_level({device_name_under}{parameters});
	}} else {{
		mutex_lock(&device_p->stream_mutex);

		while ({stream_name_under}_chunk_offset < {stream_name_under}_length) {{
			{stream_name_under}_chunk_length = {stream_name_under}_length - {stream_name_under}_chunk_offset;

			if ({stream_name_under}_chunk_length > {chunk_cardinality}) {{
				{stream_name_under}_chunk_length = {chunk_cardinality};
			}}

			memcpy({stream_name_under}_chunk_data, &{stream_name_under}[{stream_name_under}_chunk_offset], sizeof({chunk_data_type}) * {stream_name_under}_chunk_length);
			memset(&{stream_name_under}_chunk_data[{stream_name_under}_chunk_length], 0, sizeof({chunk_data_type}) * ({chunk_cardinality} - {stream_name_under}_chunk_length));

			ret = {device_name_under}_{name_under}_low_level({device_name_under}{parameters});

			if (ret < 0) {{
				break;
			}}

			{stream_name_under}_chunk_offset += {chunk_cardinality};
		}}

		mutex_unlock(&device_p->stream_mutex);
	}}

	return ret;
}}
"""
        template_stream_in_fixed_length = """
int {device_name_under}_{name_under}({device_name_camel} *{device_name_under}{high_level_parameters}) {{
	DevicePrivate *device_p = {device_name_under}->p;
	int ret;
	{stream_length_type} {stream_name_under}_length = {fixed_length};
	{stream_length_type} {stream_name_under}_chunk_offset = 0;
	{chunk_data_type} {stream_name_under}_chunk_data[{chunk_cardinality}];
	{stream_length_type} {stream_name_under}_chunk_length;

	mutex_lock(&device_p->stream_mutex);

	while ({stream_name_under}_chunk_offset < {stream_name_under}_length) {{
		{stream_name_under}_chunk_length = {stream_name_under}_length - {stream_name_under}_chunk_offset;

		if ({stream_name_under}_chunk_length > {chunk_cardinality}) {{
			{stream_name_under}_chunk_length = {chunk_cardinality};
		}}

		memcpy({stream_name_under}_chunk_data, &{stream_name_under}[{stream_name_under}_chunk_offset], sizeof({chunk_data_type}) * {stream_name_under}_chunk_length);
		memset(&{stream_name_under}_chunk_data[{stream_name_under}_chunk_length], 0, sizeof({chunk_data_type}) * ({chunk_cardinality} - {stream_name_under}_chunk_length));

		ret = {device_name_under}_{name_under}_low_level({device_name_under}{parameters});

		if (ret < 0) {{
			break;
		}}

		{stream_name_under}_chunk_offset += {chunk_cardinality};
	}}

	mutex_unlock(&device_p->stream_mutex);

	return ret;
}}
"""
        template_stream_in_short_write = """
int {device_name_under}_{name_under}({device_name_camel} *{device_name_under}{high_level_parameters}) {{
	DevicePrivate *device_p = {device_name_under}->p;
	int ret;
	{stream_length_type} {stream_name_under}_chunk_offset = 0;
	{chunk_data_type} {stream_name_under}_chunk_data[{chunk_cardinality}];
	{stream_length_type} {stream_name_under}_chunk_length;
	uint8_t {stream_name_under}_chunk_written;

	*ret_{stream_name_under}_written = 0;

	if ({stream_name_under}_length == 0) {{
		memset(&{stream_name_under}_chunk_data, 0, sizeof({chunk_data_type}) * {chunk_cardinality});

		ret = {device_name_under}_{name_under}_low_level({device_name_under}{parameters});

		if (ret < 0) {{
			return ret;
		}}

		*ret_{stream_name_under}_written = {stream_name_under}_chunk_written;
	}} else {{
		mutex_lock(&device_p->stream_mutex);

		while ({stream_name_under}_chunk_offset < {stream_name_under}_length) {{
			{stream_name_under}_chunk_length = {stream_name_under}_length - {stream_name_under}_chunk_offset;

			if ({stream_name_under}_chunk_length > {chunk_cardinality}) {{
				{stream_name_under}_chunk_length = {chunk_cardinality};
			}}

			memcpy({stream_name_under}_chunk_data, &{stream_name_under}[{stream_name_under}_chunk_offset], sizeof({chunk_data_type}) * {stream_name_under}_chunk_length);
			memset(&{stream_name_under}_chunk_data[{stream_name_under}_chunk_length], 0, sizeof({chunk_data_type}) * ({chunk_cardinality} - {stream_name_under}_chunk_length));

			ret = {device_name_under}_{name_under}_low_level({device_name_under}{parameters});

			if (ret < 0) {{
				*ret_{stream_name_under}_written = 0;

				break;
			}}

			*ret_{stream_name_under}_written += {stream_name_under}_chunk_written;

			if ({stream_name_under}_chunk_written < {chunk_cardinality}) {{
				break; // either last chunk or short write
			}}

			{stream_name_under}_chunk_offset += {chunk_cardinality};
		}}

		mutex_unlock(&device_p->stream_mutex);
	}}

	return ret;
}}
"""
        template_stream_in_single_chunk = """
int {device_name_under}_{name_under}({device_name_camel} *{device_name_under}{high_level_parameters}) {{
	{chunk_data_type} {stream_name_under}_data[{chunk_cardinality}];

	if ({stream_name_under}_length > {chunk_cardinality}) {{
		return E_INVALID_PARAMETER;
	}}

	memcpy({stream_name_under}_data, {stream_name_under}, sizeof({chunk_data_type}) * {stream_name_under}_length);
	memset(&{stream_name_under}_data[{stream_name_under}_length], 0, sizeof({chunk_data_type}) * ({chunk_cardinality} - {stream_name_under}_length));

	return {device_name_under}_{name_under}_low_level({device_name_under}{parameters});
}}
"""
        template_stream_in_short_write_single_chunk = """
int {device_name_under}_{name_under}({device_name_camel} *{device_name_under}{high_level_parameters}) {{
	int ret;
	{chunk_data_type} {stream_name_under}_data[{chunk_cardinality}];
	uint8_t {stream_name_under}_written = 0;

	if ({stream_name_under}_length > {chunk_cardinality}) {{
		return E_INVALID_PARAMETER;
	}}

	memcpy({stream_name_under}_data, {stream_name_under}, sizeof({chunk_data_type}) * {stream_name_under}_length);
	memset(&{stream_name_under}_data[{stream_name_under}_length], 0, sizeof({chunk_data_type}) * ({chunk_cardinality} - {stream_name_under}_length));

	ret = {device_name_under}_{name_under}_low_level({device_name_under}{parameters});

	if (ret < 0) {{
		return ret;
	}}

	*ret_{stream_name_under}_written = {stream_name_under}_written;

	return ret;
}}
"""
        template_stream_out = """
int {device_name_under}_{name_under}({device_name_camel} *{device_name_under}{high_level_parameters}) {{
	DevicePrivate *device_p = {device_name_under}->p;
	int ret;
	{stream_length_type} {stream_name_under}_length = {fixed_length};
	{stream_length_type} {stream_name_under}_chunk_offset;
	{chunk_data_type} {stream_name_under}_chunk_data[{chunk_cardinality}];
	bool {stream_name_under}_out_of_sync;
	{stream_length_type} {stream_name_under}_chunk_length;

	*ret_{stream_name_under}_length = 0;

	mutex_lock(&device_p->stream_mutex);

	ret = {device_name_under}_{name_under}_low_level({device_name_under}{parameters});

	if (ret < 0) {{
		goto unlock;
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
			ret = {device_name_under}_{name_under}_low_level({device_name_under}{parameters});

			if (ret < 0) {{
				goto unlock;
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
			ret = {device_name_under}_{name_under}_low_level({device_name_under}{parameters});

			if (ret < 0) {{
				goto unlock;
			}}
		}}

		ret = E_STREAM_OUT_OF_SYNC;
	}}

unlock:
	mutex_unlock(&device_p->stream_mutex);

	return ret;
}}
"""
        template_stream_out_chunk_offset_check = """

	if ({stream_name_under}_chunk_offset == (1 << {shift_size}) - 1) {{ // maximum chunk offset -> stream has no data
		goto unlock;
	}}"""
        template_stream_out_single_chunk = """
int {device_name_under}_{name_under}({device_name_camel} *{device_name_under}{high_level_parameters}) {{
	int ret;
	{stream_length_type} {stream_name_under}_length;
	{chunk_data_type} {stream_name_under}_data[{chunk_cardinality}];

	*ret_{stream_name_under}_length = 0;

	ret = {device_name_under}_{name_under}_low_level({device_name_under}{parameters});

	if (ret < 0) {{
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

    def get_c_register_callback_function(self):
        if self.get_callback_count() == 0:
            return '\n'

        template = """
void {0}_register_callback({1} *{0}, int16_t callback_id, void *function, void *user_data) {{
	device_register_callback({0}->p, callback_id, function, user_data);
}}
"""
        return template.format(self.get_name().under, self.get_name().camel)

    def get_c_callback_wrapper_functions(self):
        functions = ''

        # high-level
        template_stream_out = """
static void {device_name_under}_callback_wrapper_{name_under}(DevicePrivate *device_p{parameters}) {{
	{name_camel}_CallbackFunction callback_function;
	void *user_data = device_p->registered_callback_user_data[DEVICE_NUM_FUNCTION_IDS + {device_name_upper}_CALLBACK_{name_upper}];
	HighLevelCallback *high_level_callback = &device_p->high_level_callbacks[-{device_name_upper}_CALLBACK_{name_upper}];
	{stream_length_type} {stream_name_under}_chunk_length = {stream_length} - {stream_name_under}_chunk_offset;

	*(void **)(&callback_function) = device_p->registered_callbacks[DEVICE_NUM_FUNCTION_IDS + {device_name_upper}_CALLBACK_{name_upper}];

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

	*(void **)(&callback_function) = device_p->registered_callbacks[DEVICE_NUM_FUNCTION_IDS + {device_name_upper}_CALLBACK_{name_upper}];

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
	void *user_data = device_p->registered_callback_user_data[DEVICE_NUM_FUNCTION_IDS + {fid}];{loop_index_decl}{bool_unpack_decls}{alignment_copies}{callback_packet_decl}

	*(void **)(&callback_function) = device_p->registered_callbacks[DEVICE_NUM_FUNCTION_IDS + {fid}];

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
	void *user_data = device_p->registered_callback_user_data[DEVICE_NUM_FUNCTION_IDS + {fid}];{loop_index_decl}{bool_unpack_decls}{alignment_copies}{callback_packet_decl}

	*(void **)(&callback_function) = device_p->registered_callbacks[DEVICE_NUM_FUNCTION_IDS + {fid}];
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
                        endian_list.append('\tfor (i = 0; i < {2}; i++) aligned_{0}[i] = leconvert_{1}_from(callback->{0}[i]);' \
                                           .format(element.get_name().under, element.get_type(), element.get_cardinality()))
                    else:
                        endian_list.append('\tcallback->{0} = leconvert_{1}_from(callback->{0});'.format(element.get_name().under, element.get_type()))

            if len(callback_arg_list) > 0:
                callback_packet_decl = '\n\t{0}_Callback *callback = ({0}_Callback *)packet;'.format(packet.get_name().camel)
            else:
                callback_packet_decl = '\n\t(void)packet;'

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
                                         callback_packet_decl=callback_packet_decl,
                                         loop_index_decl=loop_index_decl,
                                         bool_unpack_decls=bool_unpack_decls,
                                         bool_unpacks=bool_unpacks,
                                         ll_packet_name_under=ll_packet_name_under,
                                         alignment_copies=common.wrap_non_empty('\n', '\n'.join(alignment_copy_list), '\n'))

        return functions

    def get_c_include_h(self):
        template = """{0}
#ifndef {1}_{2}_H
#define {1}_{2}_H

#include "ip_connection.h"

#ifdef __cplusplus
extern "C" {{
#endif

/**
 * \\defgroup {4}{3} {6}
 */

/**
 * \\ingroup {4}{3}
 *
 * {5}
 */
typedef Device {3};
"""

        return template.format(self.get_generator().get_header_comment('asterisk'),
                               self.get_category().upper,
                               self.get_name().upper,
                               self.get_name().camel,
                               self.get_category().camel,
                               common.select_lang(self.get_description()),
                               self.get_long_display_name())

    def get_c_end_h(self):
        return "\n#ifdef __cplusplus\n}\n#endif\n\n#endif\n"

    def get_c_end_c(self):
        return "\n#ifdef __cplusplus\n}\n#endif\n"

    def get_c_typedefs(self):
        typedefs = '\n'
        template = """
typedef void (*{0}_CallbackFunction)({1});
"""

        # normal and low-level
        for packet in self.get_packets('callback'):
            name = packet.get_name().camel
            parameters = packet.get_c_parameters()

            typedefs += template.format(name, common.wrap_non_empty('', parameters, ', ') + 'void *user_data')

        # high-level
        for packet in self.get_packets('callback'):
            if not packet.has_high_level():
                continue

            name = packet.get_name(skip=-2).camel
            parameters = packet.get_c_parameters(high_level=True)

            typedefs += template.format(name, common.wrap_non_empty('', parameters, ', ') + 'void *user_data')

        return typedefs

    def get_c_create_declaration(self):
        template = """
/**
 * \\ingroup {2}{1}
 *
 * Creates the device object \\c {0} with the unique device ID \\c uid and adds
 * it to the IPConnection \\c ipcon.
 */
void {0}_create({1} *{0}, const char *uid, IPConnection *ipcon);
"""
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
void {0}_destroy({1} *{0});
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
 * disabled for a setter function then no response is send and errors are
 * silently ignored, because they cannot be detected.
 */
int {0}_get_response_expected({1} *{0}, uint8_t function_id, bool *ret_response_expected);

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
 * setter function then no response is send and errors are silently ignored,
 * because they cannot be detected.
 */
int {0}_set_response_expected({1} *{0}, uint8_t function_id, bool response_expected);

/**
 * \\ingroup {2}{1}
 *
 * Changes the response expected flag for all setter and callback configuration
 * functions of this device at once.
 */
int {0}_set_response_expected_all({1} *{0}, bool response_expected);
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
int {device_name_under}_{function_name}({device_name_camel} *{device_name_under}{parameters});
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

    def get_c_register_callback_declaration(self):
        if self.get_callback_count() == 0:
            return '\n'

        template = """
/**
 * \\ingroup {2}{1}
 *
 * Registers the given \\c function with the given \\c callback_id. The
 * \\c user_data will be passed as the last parameter to the \\c function.
 */
void {0}_register_callback({1} *{0}, int16_t callback_id, void *function, void *user_data);
"""
        return template.format(self.get_name().under, self.get_name().camel, self.get_category().camel)

    def get_c_source(self):
        source  = self.get_c_include_c()
        source += self.get_c_typedefs()
        source += self.get_c_structs()
        source += self.get_c_callback_wrapper_functions()
        source += self.get_c_create_function()
        source += self.get_c_destroy_function()
        source += self.get_c_response_expected_functions()
        source += self.get_c_register_callback_function()
        source += self.get_c_functions()
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
        header += self.get_c_register_callback_declaration()
        header += self.get_c_function_declaration()
        header += self.get_c_end_h()

        return header

    def get_c_symbols(self):
        symbols = []
        name = self.get_name().under

        symbols.append('{0}_create'.format(name))
        symbols.append('{0}_destroy'.format(name))
        symbols.append('{0}_get_response_expected'.format(name))
        symbols.append('{0}_set_response_expected'.format(name))
        symbols.append('{0}_set_response_expected_all'.format(name))

        if self.get_callback_count() > 0:
            symbols.append('{0}_register_callback'.format(name))

        symbols.append('{0}_get_api_version'.format(name))

        # normal and low-level
        for packet in self.get_packets('function'):
            symbols.append('{0}_{1}'.format(name, packet.get_name().under))

        # high-level
        for packet in self.get_packets('function'):
            if packet.has_high_level():
                symbols.append('{0}_{1}'.format(name, packet.get_name(skip=-2).under))

        return '\n'.join(symbols) + '\n'

class CBindingsPacket(c_common.CPacket):
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

        for element in self.get_elements(direction='in'):
            sf = 'request'

            if element.get_type() == 'string':
                # use memcpy for string instead of strncpy. strncpy would work
                # just fine for our strings that might no be null-terminated if
                # they have full length. but MSVC complains about strncpy being
                # unsafe, because it might not copy the null-terminator
                # resulting in an unterminated string. MSVC wants us to use
                # strncpy_s instead, but we cannot do that. just use memcpy to
                # copy the string. our strings are short, so there is no point
                # in trying to do an optimized copy operation here. also memcpy
                # will copy the null-terminator if there is one and MSVC has
                # nothing to complain anymore
                temp = '\n\tmemcpy({0}.{1}, {1}, {2});\n'
                struct_list += temp.format(sf, element.get_name().under, element.get_cardinality())
            elif element.get_type() == 'bool':
                if element.get_cardinality() > 1:
                    needs_i = True
                    struct_list += '\n\tmemset({0}.{1}, 0, {3}); for (i = 0; i < {2}; i++) {0}.{1}[i / 8] |= ({1}[i] ? 1 : 0) << (i % 8);' \
                                   .format(sf, element.get_name().under, element.get_cardinality(),
                                           element.get_c_array_length())
                else:
                    struct_list += '\n\t{0}.{1} = {1} ? 1 : 0;'.format(sf, element.get_name().under)
            elif element.get_cardinality() > 1:
                if element.get_item_size() > 1:
                    needs_i = True
                    struct_list += '\n\tfor (i = 0; i < {3}; i++) {0}.{1}[i] = leconvert_{2}_to({1}[i]);' \
                                   .format(sf, element.get_name().under, element.get_type(), element.get_cardinality())
                else:
                    temp = '\n\tmemcpy({0}.{1}, {1}, {2} * sizeof({3}));'
                    struct_list += temp.format(sf,
                                               element.get_name().under,
                                               element.get_cardinality(),
                                               element.get_c_type('default'))
            elif element.get_item_size() > 1:
                struct_list += '\n\t{0}.{1} = leconvert_{2}_to({1});'.format(sf, element.get_name().under, element.get_type())
            else:
                struct_list += '\n\t{0}.{1} = {1};'.format(sf, element.get_name().under)

        return struct_list, needs_i

    def get_c_return_list(self):
        return_list = ''
        needs_i = False

        for element in self.get_elements(direction='out'):
            sf = 'response'

            if element.get_type() == 'string':
                # use memcpy for string instead of strncpy. strncpy would work
                # just fine for our strings that might no be null-terminated if
                # they have full length. but MSVC complains about strncpy being
                # unsafe, because it might not copy the null-terminator
                # resulting in an unterminated string. MSVC wants us to use
                # strncpy_s instead, but we cannot do that. just use memcpy to
                # copy the string. our strings are short, so there is no point
                # in trying to do an optimized copy operation here. also memcpy
                # will copy the null-terminator if there is one and MSVC has
                # nothing to complain anymore
                temp = '\tmemcpy(ret_{0}, {1}.{0}, {2});\n'
                return_list += temp.format(element.get_name().under, sf, element.get_cardinality())
            elif element.get_type() == 'bool':
                if element.get_cardinality() > 1:
                    needs_i = True
                    return_list += '\tfor (i = 0; i < {2}; i++) ret_{0}[i] = ({1}.{0}[i / 8] & (1 << (i % 8))) != 0;\n' \
                                   .format(element.get_name().under, sf, element.get_cardinality())
                else:
                    return_list += '\t*ret_{0} = {1}.{0} != 0;\n'.format(element.get_name().under, sf)
            elif element.get_cardinality() > 1:
                if element.get_item_size() > 1:
                    needs_i = True
                    return_list += '\tfor (i = 0; i < {3}; i++) ret_{0}[i] = leconvert_{2}_from({1}.{0}[i]);\n' \
                                   .format(element.get_name().under, sf, element.get_type(), element.get_cardinality())
                else:
                    temp = '\tmemcpy(ret_{0}, {1}.{0}, {2} * sizeof({3}));\n'
                    return_list += temp.format(element.get_name().under,
                                               sf,
                                               element.get_cardinality(),
                                               element.get_c_type('default'))
            elif element.get_item_size() > 1:
                return_list += '\t*ret_{0} = leconvert_{2}_from({1}.{0});\n'.format(element.get_name().under, sf, element.get_type())
            else:
                return_list += '\t*ret_{0} = {1}.{0};\n'.format(element.get_name().under, sf)

        return return_list, needs_i

class CBindingsGenerator(common.BindingsGenerator):
    def get_bindings_name(self):
        return 'c'

    def get_bindings_display_name(self):
        return 'C/C++'

    def get_device_class(self):
        return CBindingsDevice

    def get_packet_class(self):
        return CBindingsPacket

    def get_element_class(self):
        return c_common.CElement

    def generate(self, device):
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
