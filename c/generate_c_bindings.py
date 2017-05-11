#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Bindings Generator
Copyright (C) 2012-2017 Matthias Bolte <matthias@tinkerforge.com>
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
                return '{{@link {0}_CALLBACK_{1}}}'.format(packet.get_device().get_upper_case_name(),
                                                           packet.get_upper_case_name(skip=-2 if high_level else 0))
            else:
                return '{{@link {0}_{1}}}'.format(packet.get_device().get_underscore_name(),
                                                  packet.get_underscore_name(skip=-2 if high_level else 0))

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
                               self.get_underscore_category(),
                               self.get_underscore_name())

    def get_c_function_id_defines(self):
        defines = ''
        template =  """
/**
 * \ingroup {4}{3}
 */
#define {0}_FUNCTION_{1} {2}
"""

        for packet in self.get_packets('function'):
            defines += template.format(self.get_upper_case_name(),
                                       packet.get_upper_case_name(),
                                       packet.get_function_id(),
                                       self.get_camel_case_name(),
                                       self.get_camel_case_category())

        return defines

    def get_c_callback_defines(self):
        defines = ''
        template = """
/**
 * \ingroup {5}{4}
 *
 * {3}
 */
#define {0}_CALLBACK_{1} {2}
"""

        for packet in self.get_packets('callback'):
            defines += template.format(self.get_upper_case_name(),
                                       packet.get_upper_case_name(),
                                       packet.get_function_id(),
                                       packet.get_c_formatted_doc(),
                                       self.get_camel_case_name(),
                                       self.get_camel_case_category())

        template = """
/**
 * \ingroup {5}{4}
 *
 * {3}
 */
#define {0}_CALLBACK_{1} (-{2})
"""

        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                defines += template.format(self.get_upper_case_name(),
                                           packet.get_upper_case_name(skip=-2),
                                           packet.get_function_id(),
                                           packet.get_c_formatted_doc(high_level=True),
                                           self.get_camel_case_name(),
                                           self.get_camel_case_category())

        if self.get_long_display_name() == 'RS232 Bricklet':
            defines += """
/**
 * \ingroup BrickletRS232
 *
 * Signature: \code void callback(char ret_message[60], uint8_t length, void *user_data) \endcode
 *
 * This callback is called if new data is available. The message has
 * a maximum size of 60 characters. The actual length of the message
 * is given in addition.
 *
 * To enable this callback, use {@link rs232_enable_read_callback}.
 */
#define RS232_CALLBACK_READ_CALLBACK RS232_CALLBACK_READ // for backward compatibility

/**
 * \ingroup BrickletRS232
 *
 * Signature: \code void callback(uint8_t error, void *user_data) \endcode
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
 * \ingroup {doxygen}
 */
#define {prefix}_{constant_group_upper_case_name}_{constant_upper_case_name} {constant_value}
"""

        return '\n' + self.get_formatted_constants(constant_format,
                                                   doxygen=self.get_camel_case_category()+self.get_camel_case_name(),
                                                   prefix=self.get_upper_case_name())

    def get_c_device_identifier_define(self):
        template = """
/**
 * \ingroup {3}{2}
 *
 * This constant is used to identify a {5}.
 *
 * The {{@link {4}_get_identity}} function and the
 * {{@link IPCON_CALLBACK_ENUMERATE}} callback of the IP Connection have a
 * \c device_identifier parameter to specify the Brick's or Bricklet's type.
 */
#define {0}_DEVICE_IDENTIFIER {1}
"""

        return template.format(self.get_upper_case_name(),
                               self.get_device_identifier(),
                               self.get_camel_case_name(),
                               self.get_camel_case_category(),
                               self.get_underscore_name(),
                               self.get_long_display_name())

    def get_c_device_display_name_define(self):
        template = """
/**
 * \ingroup {3}{2}
 *
 * This constant represents the display name of a {1}.
 */
#define {0}_DEVICE_DISPLAY_NAME "{1}"
"""

        return template.format(self.get_upper_case_name(),
                               self.get_long_display_name(),
                               self.get_camel_case_name(),
                               self.get_camel_case_category())

    def get_c_structs(self):
        structs = """
#if defined _MSC_VER || defined __BORLANDC__
	#pragma pack(push)
	#pragma pack(1)
	#define ATTRIBUTE_PACKED
#elif defined __GNUC__
	#ifdef _WIN32
		// workaround struct packing bug in GCC 4.7 on Windows
		// http://gcc.gnu.org/bugzilla/show_bug.cgi?id=52991
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
                struct_body = ''

                for element in packet.get_elements():
                    c_type = element.get_c_type(False, struct=True)

                    if element.get_cardinality() > 1:
                        if element.get_type() == 'bool':
                            length = int(math.ceil(element.get_cardinality() / 8.0))
                        else:
                            length = element.get_cardinality()

                        struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                                  element.get_underscore_name(),
                                                                  length);
                    else:
                        struct_body += '\t{0} {1};\n'.format(c_type, element.get_underscore_name())

                structs += struct_template.format(struct_body, packet.get_camel_case_name(), 'Callback')
                continue

            struct_body = ''

            for element in packet.get_elements('in'):
                c_type = element.get_c_type(False, struct=True)

                if element.get_cardinality() > 1:
                    if element.get_type() == 'bool':
                        length = int(math.ceil(element.get_cardinality() / 8.0))
                    else:
                        length = element.get_cardinality()

                    struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                              element.get_underscore_name(),
                                                              length);
                else:
                    struct_body += '\t{0} {1};\n'.format(c_type, element.get_underscore_name())

            structs += struct_template.format(struct_body, packet.get_camel_case_name(), 'Request')

            if len(packet.get_elements('out')) == 0:
                continue

            struct_body = ''

            for element in packet.get_elements('out'):
                c_type = element.get_c_type(False, struct=True)

                if element.get_cardinality() > 1:
                    if element.get_type() == 'bool':
                        length = int(math.ceil(element.get_cardinality() / 8.0))
                    else:
                        length = element.get_cardinality()

                    struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                              element.get_underscore_name(),
                                                              length);
                else:
                    struct_body += '\t{0} {1};\n'.format(c_type, element.get_underscore_name())

            structs += struct_template.format(struct_body, packet.get_camel_case_name(), 'Response')

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
        llcb_temp = """
	device_p->low_level_callbacks[{2}_CALLBACK_{1}].exists = true;"""
        callbacks = ''

        for packet in self.get_packets('callback'):
            callbacks += cb_temp.format(self.get_underscore_name(), packet.get_upper_case_name(), packet.get_underscore_name(), self.get_upper_case_name())

        if len(callbacks) > 0:
            callbacks += '\n'

        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                callbacks += llcb_temp.format(self.get_underscore_name(), packet.get_upper_case_name(), self.get_upper_case_name())

        response_expected = ''

        for packet in self.get_packets():
            if packet.get_type() == 'callback':
                prefix = 'CALLBACK'
                flag = 'DEVICE_RESPONSE_EXPECTED_ALWAYS_FALSE'
            elif len(packet.get_elements('out')) > 0:
                prefix = 'FUNCTION'
                flag = 'DEVICE_RESPONSE_EXPECTED_ALWAYS_TRUE'
            elif packet.get_doc_type() in ['ccf', 'llf']:
                prefix = 'FUNCTION'
                flag = 'DEVICE_RESPONSE_EXPECTED_TRUE'
            else:
                prefix = 'FUNCTION'
                flag = 'DEVICE_RESPONSE_EXPECTED_FALSE'

            response_expected += '\tdevice_p->response_expected[{1}_{2}_{3}] = {4};\n' \
                                 .format(self.get_underscore_name(),
                                         self.get_upper_case_name(),
                                         prefix,
                                         packet.get_upper_case_name(),
                                         flag)

        if len(response_expected) > 0:
            response_expected = '\n' + response_expected

        return template.format(self.get_underscore_name(),
                               self.get_camel_case_name(),
                               response_expected + callbacks,
                               *self.get_api_version())

    def get_c_destroy_function(self):
        template = """
void {0}_destroy({1} *{0}) {{
	device_release({0}->p);
}}
"""
        return template.format(self.get_underscore_name(),
                               self.get_camel_case_name())

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
        return template.format(self.get_underscore_name(),
                               self.get_camel_case_name())

    def get_c_functions(self):
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
{2}
"""

        device_name = self.get_underscore_name()
        c = self.get_camel_case_name()
        functions = []

        for packet in self.get_packets('function'):
            packet_name = packet.get_underscore_name()
            params = common.wrap_non_empty(', ', packet.get_c_parameters(), '')
            fid = '{0}_FUNCTION_{1}'.format(self.get_upper_case_name(),
                                            packet.get_upper_case_name())
            f = packet.get_camel_case_name()
            h, needs_i = packet.get_c_struct_list()

            if len(packet.get_elements('out')) > 0:
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

            functions.append(template.format(device_name, packet_name, c, params, fid, f, g, h, i, k, r))

        return template_version.format(device_name, c) + ''.join(functions)

    def get_c_high_level_functions(self):
        functions = ''
        template_stream_in = """
int {device_underscore_name}_{underscore_name}({device_camel_case_name} *{device_underscore_name}{high_level_parameters}) {{
	DevicePrivate *device_p = {device_underscore_name}->p;
	int ret = 0;
	uint16_t stream_total_length = {data_underscore_name}_length; // FIXME: uint16_t is not always the correct type
	uint16_t stream_chunk_offset = 0; // FIXME: uint16_t is not always the correct type
	{chunk_c_type} stream_chunk_data[{chunk_cardinality}];
	uint16_t stream_chunk_length; // FIXME: uint16_t is not always the correct type

	mutex_lock(&device_p->stream_mutex);

	while (stream_chunk_offset < stream_total_length) {{
		stream_chunk_length = stream_total_length - stream_chunk_offset;

		if (stream_chunk_length > {chunk_cardinality}) {{
			stream_chunk_length = {chunk_cardinality};
		}}

		// FIXME: only do memcpy/memset for last short chunk
		memcpy(stream_chunk_data, &{data_underscore_name}[stream_chunk_offset], sizeof({chunk_c_type}) * stream_chunk_length);

		if (stream_chunk_length < {chunk_cardinality}) {{
			memset(&stream_chunk_data[stream_chunk_length], 0, sizeof({chunk_c_type}) * ({chunk_cardinality} - stream_chunk_length));
		}}

		// FIXME: validate that the extra out values for all low-level calls are identical
		ret = {device_underscore_name}_{underscore_name}_low_level({device_underscore_name}{parameters});

		if (ret < 0) {{
			break;
		}}

		stream_chunk_offset += {chunk_cardinality};
	}}

	mutex_unlock(&device_p->stream_mutex);

	return ret;
}}
"""
        template_stream_in_short_write = """
int {device_underscore_name}_{underscore_name}({device_camel_case_name} *{device_underscore_name}{high_level_parameters}) {{
	DevicePrivate *device_p = {device_underscore_name}->p;
	int ret = 0;
	uint16_t stream_total_written = 0; // FIXME: uint16_t is not always the correct type
	uint16_t stream_total_length = {data_underscore_name}_length; // FIXME: uint16_t is not always the correct type
	uint16_t stream_chunk_offset = 0; // FIXME: uint16_t is not always the correct type
	uint8_t stream_chunk_written;
	{chunk_c_type} stream_chunk_data[{chunk_cardinality}];
	uint16_t stream_chunk_length; // FIXME: uint16_t is not always the correct type

	mutex_lock(&device_p->stream_mutex);

	while (stream_chunk_offset < stream_total_length) {{
		stream_chunk_length = stream_total_length - stream_chunk_offset;

		if (stream_chunk_length > {chunk_cardinality}) {{
			stream_chunk_length = {chunk_cardinality};
		}}

		// FIXME: only do memcpy/memset for last short chunk
		memcpy(stream_chunk_data, &{data_underscore_name}[stream_chunk_offset], sizeof({chunk_c_type}) * stream_chunk_length);

		if (stream_chunk_length < {chunk_cardinality}) {{
			memset(&stream_chunk_data[stream_chunk_length], 0, sizeof({chunk_c_type}) * ({chunk_cardinality} - stream_chunk_length));
		}}

		// FIXME: validate that the extra out values for all low-level calls are identical
		ret = {device_underscore_name}_{underscore_name}_low_level({device_underscore_name}{parameters});

		if (ret < 0) {{
			stream_total_written = 0;
			break;
		}}

		stream_total_written += stream_chunk_written;

		if (stream_chunk_written < {chunk_cardinality}) {{
			break; // either last chunk or short write
		}}

		stream_chunk_offset += {chunk_cardinality};
	}}

	mutex_unlock(&device_p->stream_mutex);

	*ret_written = stream_total_written;

	return ret;
}}
"""
        template_stream_out = """
int {device_underscore_name}_{underscore_name}({device_camel_case_name} *{device_underscore_name}{high_level_parameters}) {{
	DevicePrivate *device_p = {device_underscore_name}->p;
	int ret = 0;
	uint16_t stream_total_length = {fixed_total_length}; // FIXME: uint16_t is not always the correct type
	uint16_t stream_chunk_offset; // FIXME: uint16_t is not always the correct type
	{chunk_c_type} stream_chunk_data[{chunk_cardinality}];
	uint16_t stream_chunk_length; // FIXME: uint16_t is not always the correct type

	*ret_{data_underscore_name}_length = 0;

	mutex_lock(&device_p->stream_mutex);

	ret = {device_underscore_name}_{underscore_name}_low_level({device_underscore_name}{parameters});

	if (ret < 0) {{
		goto cleanup;
	}}

	if (stream_chunk_offset != 0) {{ // stream out-of-sync
		goto discard;
	}}

	stream_chunk_length = stream_total_length - stream_chunk_offset;

	if (stream_chunk_length > {chunk_cardinality}) {{
		stream_chunk_length = {chunk_cardinality};
	}}

	memcpy(ret_{data_underscore_name}, stream_chunk_data, sizeof({chunk_c_type}) * stream_chunk_length);
	*ret_{data_underscore_name}_length = stream_chunk_length;

	while (*ret_{data_underscore_name}_length < stream_total_length) {{
		// FIXME: validate chunk offset < total length
		// FIXME: validate that total length is identical for all low-level getters of a stream
		// FIXME: validate that the extra out values for all low-level calls are identical
		ret = {device_underscore_name}_{underscore_name}_low_level({device_underscore_name}{parameters});

		if (ret < 0) {{
			goto cleanup;
		}}

		if (stream_chunk_offset != *ret_{data_underscore_name}_length) {{ // stream out-of-sync
			goto discard;
		}}

		stream_chunk_length = stream_total_length - stream_chunk_offset;

		if (stream_chunk_length > {chunk_cardinality}) {{
			stream_chunk_length = {chunk_cardinality};
		}}

		memcpy(&ret_{data_underscore_name}[*ret_{data_underscore_name}_length], stream_chunk_data, sizeof({chunk_c_type}) * stream_chunk_length);
		*ret_{data_underscore_name}_length += stream_chunk_length;
	}}

	goto cleanup;

discard:
	*ret_{data_underscore_name}_length = 0; // return empty array

	// discard remaining stream to bring it back in-sync
	while (stream_chunk_offset + {chunk_cardinality} < stream_total_length) {{
		// FIXME: validate that total length is identical for all low-level getters of a stream
		// FIXME: validate that stream_chunk_offset grows
		ret = {device_underscore_name}_{underscore_name}_low_level({device_underscore_name}{parameters});

		if (ret < 0) {{
			goto cleanup;
		}}
	}}

	ret = E_STREAM_OUT_OF_SYNC;

cleanup:
	mutex_unlock(&device_p->stream_mutex);

	return ret;
}}
"""

        for packet in self.get_packets('function'):
            stream_in = packet.get_high_level('stream_in')
            stream_out = packet.get_high_level('stream_out')

            if stream_in != None:
                if stream_in.has_short_write():
                    template = template_stream_in_short_write
                else:
                    template = template_stream_in

                functions += template.format(device_camel_case_name=packet.get_device().get_camel_case_name(),
                                             device_underscore_name=packet.get_device().get_underscore_name(),
                                             underscore_name=packet.get_underscore_name(skip=-2),
                                             parameters=common.wrap_non_empty(', ', packet.get_c_parameters(signature=False), ''),
                                             high_level_parameters=common.wrap_non_empty(', ', packet.get_c_parameters(high_level=True), ''),
                                             data_underscore_name=stream_in.get_data_underscore_name(),
                                             chunk_c_type=stream_in.get_chunk_data_element().get_c_type(False),
                                             chunk_cardinality=stream_in.get_chunk_data_element().get_cardinality())
            elif stream_out != None:
                functions += template_stream_out.format(device_camel_case_name=packet.get_device().get_camel_case_name(),
                                                        device_underscore_name=packet.get_device().get_underscore_name(),
                                                        underscore_name=packet.get_underscore_name(skip=-2),
                                                        parameters=common.wrap_non_empty(', ', packet.get_c_parameters(signature=False), ''),
                                                        high_level_parameters=common.wrap_non_empty(', ', packet.get_c_parameters(high_level=True), ''),
                                                        data_underscore_name=stream_out.get_data_underscore_name(),
                                                        fixed_total_length=stream_out.get_fixed_total_length(default='0'),
                                                        chunk_c_type=stream_out.get_chunk_data_element().get_c_type(False),
                                                        chunk_cardinality=stream_out.get_chunk_data_element().get_cardinality())

        return functions

    def get_c_register_callback_function(self):
        if self.get_callback_count() == 0:
            return '\n'

        template = """
void {0}_register_callback({1} *{0}, int16_t id, void *callback, void *user_data) {{
	device_register_callback({0}->p, id, callback, user_data);
}}
"""
        return template.format(self.get_underscore_name(), self.get_camel_case_name())

    def get_c_high_level_callback_wrapper_functions(self):
        functions = ''
        template = """
static void {device_underscore_name}_callback_wrapper_{underscore_name}(DevicePrivate *device_p{parameters}) {{
	{camel_case_name}_CallbackFunction callback_function;
	void *user_data = device_p->registered_callback_user_data[DEVICE_NUM_FUNCTION_IDS + {device_upper_case_name}_CALLBACK_{upper_case_name}];
	LowLevelCallback *low_level_callback = &device_p->low_level_callbacks[-{device_upper_case_name}_CALLBACK_{upper_case_name}];
	uint16_t stream_chunk_length = {stream_total_length} - stream_chunk_offset; // FIXME: uint16_t is not always the correct type

	*(void **)(&callback_function) = device_p->registered_callbacks[DEVICE_NUM_FUNCTION_IDS + {device_upper_case_name}_CALLBACK_{upper_case_name}];

	if (stream_chunk_length > {chunk_cardinality}) {{
		stream_chunk_length = {chunk_cardinality};
	}}

	// FIXME: validate that extra parameters are identical for all low-level callbacks of a stream
	// FIXME: validate that total length is identical for all low-level callbacks of a stream
	// FIXME: validate chunk offset < total length

	if (low_level_callback->data == NULL) {{ // no stream in-progress
		if (stream_chunk_offset == 0) {{ // stream starts
			low_level_callback->data = malloc(sizeof({chunk_c_type}) * {stream_total_length});
			low_level_callback->data_length = stream_chunk_length;

			memcpy(low_level_callback->data, stream_chunk_data, sizeof({chunk_c_type}) * stream_chunk_length);

			if (low_level_callback->data_length >= {stream_total_length}) {{ // stream complete
				if (callback_function != NULL) {{
					callback_function({high_level_parameters}user_data);
				}}

				free(low_level_callback->data);
				low_level_callback->data = NULL;
				low_level_callback->data_length = 0;
			}}
		}} else {{ // ignore tail of current stream, wait for next stream start
		}}
	}} else {{ // stream in-progress
		if (stream_chunk_offset != low_level_callback->data_length) {{ // stream out-of-sync
			free(low_level_callback->data);
			low_level_callback->data = NULL;
			low_level_callback->data_length = 0;

			if (callback_function != NULL) {{
				callback_function({high_level_parameters}user_data);
			}}
		}} else {{ // stream in-sync
			memcpy(&(({chunk_c_type} *)low_level_callback->data)[low_level_callback->data_length], stream_chunk_data, sizeof({chunk_c_type}) * stream_chunk_length);
			low_level_callback->data_length += stream_chunk_length;

			if (low_level_callback->data_length >= {stream_total_length}) {{ // stream complete
				if (callback_function != NULL) {{
					callback_function({high_level_parameters}user_data);
				}}

				free(low_level_callback->data);
				low_level_callback->data = NULL;
				low_level_callback->data_length = 0;
			}}
		}}
	}}
}}
"""

        for packet in self.get_packets('callback'):
            stream_out = packet.get_high_level('stream_out')

            if stream_out != None:
                functions += template.format(device_underscore_name=packet.get_device().get_underscore_name(),
                                             device_upper_case_name=packet.get_device().get_upper_case_name(),
                                             underscore_name=packet.get_underscore_name(skip=-2),
                                             upper_case_name=packet.get_upper_case_name(skip=-2),
                                             camel_case_name=packet.get_camel_case_name(skip=-2),
                                             parameters=common.wrap_non_empty(', ', packet.get_c_parameters(), ''),
                                             high_level_parameters=common.wrap_non_empty('', packet.get_c_parameters(signature=False, high_level=True, callback_wrapper=True), ', '),
                                             data_underscore_name=stream_out.get_data_underscore_name(),
                                             stream_total_length=stream_out.get_fixed_total_length(default='stream_total_length'),
                                             chunk_c_type=stream_out.get_chunk_data_element().get_c_type(False),
                                             chunk_cardinality=stream_out.get_chunk_data_element().get_cardinality())

        return functions

    def get_c_callback_wrapper_functions(self):
        functions = []
        template = """
static void {0}_callback_wrapper_{1}(DevicePrivate *device_p, Packet *packet) {{
	{3}_CallbackFunction callback_function;
	void *user_data = device_p->registered_callback_user_data[{7}];{9}{10}{8}

	*(void **)(&callback_function) = device_p->registered_callbacks[DEVICE_NUM_FUNCTION_IDS + {7}];

	if (callback_function == NULL) {{
		return;
	}}
{6}{11}
	callback_function({5}{4}user_data);
}}
"""
        template_low_level = """
static void {0}_callback_wrapper_{1}(DevicePrivate *device_p, Packet *packet) {{
	{3}_CallbackFunction callback_function;
	void *user_data = device_p->registered_callback_user_data[{7}];{9}{10}{8}

	*(void **)(&callback_function) = device_p->registered_callbacks[DEVICE_NUM_FUNCTION_IDS + {7}];
{6}{11}
	{0}_callback_wrapper_{12}(device_p, {5});

	if (callback_function != NULL) {{
		callback_function({5}{4}user_data);
	}}
}}
"""

        for packet in self.get_packets('callback'):
            a = self.get_underscore_name()
            b = packet.get_underscore_name()
            c = self.get_camel_case_name()
            d = packet.get_camel_case_name()
            e = ''
            f_list = []

            for element in packet.get_elements():
                if element.get_type() == 'bool':
                    f_list.append('unpacked_{0}'.format(element.get_underscore_name()))
                else:
                    f_list.append('callback->{0}'.format(element.get_underscore_name()))

            f = ', '.join(f_list)

            if len(f_list) > 0:
                e = ', '

            endian_list = []
            i = ''
            variables = ''
            unpacks = ''

            for element in packet.get_elements():
                if element.get_type() == 'bool':
                    if element.get_cardinality() > 1:
                        i = '\n\tint i;'
                        variables += '\n\tbool unpacked_{0}[{1}];'.format(element.get_underscore_name(), element.get_cardinality())
                        unpacks += '\tfor (i = 0; i < {1}; i++) unpacked_{0}[i] = (callback->{0}[i / 8] & (1 << (i % 8))) != 0;\n' \
                                    .format(element.get_underscore_name(), element.get_cardinality())
                    else:
                        variables += '\n\tbool unpacked_{0};'.format(element.get_underscore_name())
                        unpacks += '\tunpacked_{0} = callback->{0} != 0;\n'.format(element.get_underscore_name())
                elif element.get_item_size() > 1:
                    if element.get_cardinality() > 1:
                        i = '\n\tint i;'
                        endian_list.append('\tfor (i = 0; i < {2}; i++) callback->{0}[i] = leconvert_{1}_from(callback->{0}[i]);' \
                                           .format(element.get_underscore_name(), element.get_type(), element.get_cardinality()))
                    else:
                        endian_list.append('\tcallback->{0} = leconvert_{1}_from(callback->{0});'.format(element.get_underscore_name(), element.get_type()))

            endian = '\n'.join(endian_list)

            if len(endian) > 0:
                endian = '\n' + endian + '\n'

            fid = '{0}_CALLBACK_{1}'.format(self.get_upper_case_name(),
                                            packet.get_upper_case_name())
            if len(f_list) > 0:
                cb = '\n\t{0}_Callback *callback = ({0}_Callback *)packet;'.format(d)
            else:
                cb = '\n\t(void)packet;'

            if packet.get_high_level('stream_out') != None:
                temp = template_low_level
            else:
                temp = template

            functions.append(temp.format(a, b, c, d, e, f, endian, fid, cb, i, variables, unpacks, packet.get_underscore_name(skip=-2)))

        return ''.join(functions)

    def get_c_include_h(self):
        template = """{0}
#ifndef {1}_{2}_H
#define {1}_{2}_H

#include "ip_connection.h"

#ifdef __cplusplus
extern "C" {{
#endif

/**
 * \defgroup {4}{3} {6}
 */

/**
 * \ingroup {4}{3}
 *
 * {5}
 */
typedef Device {3};
"""

        return template.format(self.get_generator().get_header_comment('asterisk'),
                               self.get_upper_case_category(),
                               self.get_upper_case_name(),
                               self.get_camel_case_name(),
                               self.get_camel_case_category(),
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


        for packet in self.get_packets('callback'):
            name = packet.get_camel_case_name()
            c_type_list = []

            for element in packet.get_elements():
                if element.get_cardinality() > 1:
                    c_type_list.append('{0}[{1}]'.format(element.get_c_type(True), element.get_cardinality()))
                else:
                    c_type_list.append(element.get_c_type(True))

            typedefs += template.format(name, ', '.join(c_type_list + ['void *']))

        return typedefs

    def get_c_high_level_typedefs(self):
        typedefs = ''
        template = """
typedef void (*{0}_CallbackFunction)({1});
"""

        for packet in self.get_packets('callback'):
            if not packet.has_high_level():
                continue

            name = packet.get_camel_case_name(skip=-2)
            c_type_list = []

            for element in packet.get_elements(high_level=True):
                if element.get_cardinality() > 1:
                    c_type_list.append('{0}[{1}]'.format(element.get_c_type(True), element.get_cardinality()))
                elif element.get_cardinality() < 1:
                    c_type_list.append('{0} *'.format(element.get_c_type(True)))
                    c_type_list.append('uint16_t') # FIXME: uint16_t is not always the correct type
                else:
                    c_type_list.append(element.get_c_type(True))

            typedefs += template.format(name, ', '.join(c_type_list + ['void *']))

        return typedefs

    def get_c_create_declaration(self):
        template = """
/**
 * \ingroup {2}{1}
 *
 * Creates the device object \c {0} with the unique device ID \c uid and adds
 * it to the IPConnection \c ipcon.
 */
void {0}_create({1} *{0}, const char *uid, IPConnection *ipcon);
"""
        return template.format(self.get_underscore_name(),
                               self.get_camel_case_name(),
                               self.get_camel_case_category())

    def get_c_destroy_declaration(self):
        template = """
/**
 * \ingroup {2}{1}
 *
 * Removes the device object \c {0} from its IPConnection and destroys it.
 * The device object cannot be used anymore afterwards.
 */
void {0}_destroy({1} *{0});
"""
        return template.format(self.get_underscore_name(),
                               self.get_camel_case_name(),
                               self.get_camel_case_category())

    def get_c_response_expected_declarations(self):
        template = """
/**
 * \ingroup {2}{1}
 *
 * Returns the response expected flag for the function specified by the
 * \c function_id parameter. It is *true* if the function is expected to
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
 * \ingroup {2}{1}
 *
 * Changes the response expected flag of the function specified by the
 * \c function_id parameter. This flag can only be changed for setter
 * (default value: *false*) and callback configuration functions
 * (default value: *true*). For getter functions it is always enabled and
 * callbacks it is always disabled.
 *
 * Enabling the response expected flag for a setter function allows to detect
 * timeouts and other error conditions calls of this setter as well. The device
 * will then send a response for this purpose. If this flag is disabled for a
 * setter function then no response is send and errors are silently ignored,
 * because they cannot be detected.
 */
int {0}_set_response_expected({1} *{0}, uint8_t function_id, bool response_expected);

/**
 * \ingroup {2}{1}
 *
 * Changes the response expected flag for all setter and callback configuration
 * functions of this device at once.
 */
int {0}_set_response_expected_all({1} *{0}, bool response_expected);
"""
        return template.format(self.get_underscore_name(),
                               self.get_camel_case_name(),
                               self.get_camel_case_category())

    def get_c_function_declaration(self):
        func_version = """
/**
 * \ingroup {2}{1}
 *
 * Returns the API version (major, minor, release) of the bindings for this
 * device.
 */
int {0}_get_api_version({1} *{0}, uint8_t ret_api_version[3]);
"""
        func = """
/**
 * \ingroup {5}{2}
 *
 * {4}
 */
int {0}_{1}({2} *{0}{3});
"""

        a = self.get_underscore_name()
        c = self.get_camel_case_name()
        functions = ''

        for packet in self.get_packets('function'):
            b = packet.get_underscore_name()
            d = common.wrap_non_empty(', ', packet.get_c_parameters(), '')
            doc = packet.get_c_formatted_doc()

            functions += func.format(a, b, c, d, doc, self.get_camel_case_category())

        return func_version.format(a, c, self.get_camel_case_category()) + functions

    def get_c_high_level_function_declaration(self):
        functions = ''
        template = """
/**
 * \ingroup {category}{device_camel_case_name}
 *
 * {doc}
 */
int {device_underscore_name}_{underscore_name}({device_camel_case_name} *{device_underscore_name}{high_level_parameters});
"""

        for packet in self.get_packets('function'):
            if packet.get_high_level('stream_*') != None:
                functions += template.format(category=packet.get_device().get_category(),
                                             device_camel_case_name=packet.get_device().get_camel_case_name(),
                                             doc=packet.get_c_formatted_doc(),
                                             device_underscore_name=packet.get_device().get_underscore_name(),
                                             underscore_name=packet.get_underscore_name(skip=-2),
                                             high_level_parameters=common.wrap_non_empty(', ', packet.get_c_parameters(high_level=True), ''))

        return functions

    def get_c_register_callback_declaration(self):
        if self.get_callback_count() == 0:
            return '\n'

        template = """
/**
 * \ingroup {2}{1}
 *
 * Registers a callback with ID \c id to the function \c callback. The
 * \c user_data will be given as a parameter of the callback.
 */
void {0}_register_callback({1} *{0}, int16_t id, void *callback, void *user_data);
"""
        return template.format(self.get_underscore_name(), self.get_camel_case_name(), self.get_camel_case_category())

    def get_c_source(self):
        source  = self.get_c_include_c()
        source += self.get_c_typedefs()
        source += self.get_c_high_level_typedefs()
        source += self.get_c_structs()
        source += self.get_c_high_level_callback_wrapper_functions()
        source += self.get_c_callback_wrapper_functions()
        source += self.get_c_create_function()
        source += self.get_c_destroy_function()
        source += self.get_c_response_expected_functions()
        source += self.get_c_register_callback_function()
        source += self.get_c_functions()
        source += self.get_c_high_level_functions()
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
        header += self.get_c_high_level_function_declaration()
        header += self.get_c_end_h()

        return header

    def get_c_symbols(self):
        symbols = []
        underscore_name = self.get_underscore_name()

        symbols.append('{0}_create'.format(underscore_name))
        symbols.append('{0}_destroy'.format(underscore_name))
        symbols.append('{0}_get_response_expected'.format(underscore_name))
        symbols.append('{0}_set_response_expected'.format(underscore_name))
        symbols.append('{0}_set_response_expected_all'.format(underscore_name))

        if self.get_callback_count() > 0:
            symbols.append('{0}_register_callback'.format(underscore_name))

        symbols.append('{0}_get_api_version'.format(underscore_name))

        for packet in self.get_packets('function'):
            symbols.append('{0}_{1}'.format(underscore_name, packet.get_underscore_name()))

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
            parameters = self.get_c_parameters(signature=True, high_level=high_level)

            if len(parameters) > 0:
                parameters += ', '

            text = 'Signature: \code void callback({0}void *user_data) \endcode\n'.format(parameters) + text

        text = text.replace('.. note::', '\\note')
        text = text.replace('.. warning::', '\\warning')

        def format_parameter(name):
            return '\c {0}'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return '\n * '.join(text.strip().split('\n'))

    def get_c_struct_list(self):
        struct_list = ''
        needs_i = False

        for element in self.get_elements('in'):
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
                struct_list += temp.format(sf, element.get_underscore_name(), element.get_cardinality())
            elif element.get_type() == 'bool':
                if element.get_cardinality() > 1:
                    needs_i = True
                    struct_list += '\n\tmemset({0}.{1}, 0, {3}); for (i = 0; i < {2}; i++) {0}.{1}[i / 8] = ({1}[i] ? 1 : 0) << (i % 8);' \
                                   .format(sf, element.get_underscore_name(), element.get_cardinality(),
                                           int(math.ceil(element.get_cardinality() / 8.0)))
                else:
                    struct_list += '\n\t{0}.{1} = {1} ? 1 : 0;'.format(sf, element.get_underscore_name())
            elif element.get_cardinality() > 1:
                if element.get_item_size() > 1:
                    needs_i = True
                    struct_list += '\n\tfor (i = 0; i < {3}; i++) {0}.{1}[i] = leconvert_{2}_to({1}[i]);' \
                                   .format(sf, element.get_underscore_name(), element.get_type(), element.get_cardinality())
                else:
                    temp = '\n\tmemcpy({0}.{1}, {1}, {2} * sizeof({3}));'
                    struct_list += temp.format(sf,
                                               element.get_underscore_name(),
                                               element.get_cardinality(),
                                               element.get_c_type(False))
            elif element.get_item_size() > 1:
                struct_list += '\n\t{0}.{1} = leconvert_{2}_to({1});'.format(sf, element.get_underscore_name(), element.get_type())
            else:
                struct_list += '\n\t{0}.{1} = {1};'.format(sf, element.get_underscore_name())

        return struct_list, needs_i

    def get_c_return_list(self):
        return_list = ''
        needs_i = False

        for element in self.get_elements('out'):
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
                return_list += temp.format(element.get_underscore_name(), sf, element.get_cardinality())
            elif element.get_type() == 'bool':
                if element.get_cardinality() > 1:
                    needs_i = True
                    return_list += '\tfor (i = 0; i < {2}; i++) ret_{0}[i] = ({1}.{0}[i / 8] & (1 << (i % 8))) != 0;\n' \
                                   .format(element.get_underscore_name(), sf, element.get_cardinality())
                else:
                    return_list += '\t*ret_{0} = {1}.{0} != 0;\n'.format(element.get_underscore_name(), sf)
            elif element.get_cardinality() > 1:
                if element.get_item_size() > 1:
                    needs_i = True
                    return_list += '\tfor (i = 0; i < {3}; i++) ret_{0}[i] = leconvert_{2}_from({1}.{0}[i]);\n' \
                                   .format(element.get_underscore_name(), sf, element.get_type(), element.get_cardinality())
                else:
                    temp = '\tmemcpy(ret_{0}, {1}.{0}, {2} * sizeof({3}));\n'
                    return_list += temp.format(element.get_underscore_name(),
                                               sf,
                                               element.get_cardinality(),
                                               element.get_c_type(False))
            elif element.get_item_size() > 1:
                return_list += '\t*ret_{0} = leconvert_{2}_from({1}.{0});\n'.format(element.get_underscore_name(), sf, element.get_type())
            else:
                return_list += '\t*ret_{0} = {1}.{0};\n'.format(element.get_underscore_name(), sf)

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
        filename = '{0}_{1}'.format(device.get_underscore_category(), device.get_underscore_name())

        with open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename + '.c'), 'wb') as f:
            f.write(device.get_c_source())

        with open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename + '.h'), 'wb') as f:
            f.write(device.get_c_header())

        with open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename + '.symbols'), 'wb') as f:
            f.write(device.get_c_symbols())

        if device.is_released():
            self.released_files.append(filename + '.c')
            self.released_files.append(filename + '.h')
            self.released_files.append(filename + '.symbols')

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', CBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
