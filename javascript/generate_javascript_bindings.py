#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JavaScript Bindings Generator
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2014-2015, 2017-2018, 2020 Matthias Bolte <matthias@tinkerforge.com>

generate_javascript_bindings.py: Generator for JavaScript bindings

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
import javascript_common

class JavaScriptBindingsDevice(javascript_common.JavaScriptDevice):
    def get_javascript_require(self):
        template = """{0}
var Device = require('./Device');
var IPConnection = require('./IPConnection');

{1}.DEVICE_IDENTIFIER = {2};
{1}.DEVICE_DISPLAY_NAME = '{3}';
"""

        return template.format(self.get_generator().get_header_comment('asterisk'),
                               self.get_javascript_class_name(),
                               self.get_device_identifier(),
                               self.get_long_display_name())

    def get_javascript_constants(self):
        callback_constants = ''
        callback_constant_statement = self.get_javascript_class_name()+'.CALLBACK_{0} = {1};\n'

        for packet in self.get_packets('callback'):
            callback_constants += callback_constant_statement.format(packet.get_name().upper,
                                                                     packet.get_function_id())

        if self.get_long_display_name() == 'RS232 Bricklet':
            callback_constants += 'BrickletRS232.CALLBACK_READ_CALLBACK = 8; // for backward compatibility\n'
            callback_constants += 'BrickletRS232.CALLBACK_ERROR_CALLBACK = 9; // for backward compatibility\n'

        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                callback_constants += callback_constant_statement.format(packet.get_name(skip=-2).upper,
                                                                         -packet.get_function_id())

        function_constants = ''
        function_constant_statement = self.get_javascript_class_name() + '.FUNCTION_{0} = {1};\n'

        for packet in self.get_packets('function'):
            function_constants += function_constant_statement.format(packet.get_name().upper,
                                                                     packet.get_function_id())
        constant_statement = self.get_javascript_class_name() + \
                             '.{constant_group_name_upper}_{constant_name_upper} = {constant_value};\n'
        constants = self.get_formatted_constants(constant_statement, bool_format_func=lambda value: str(value).lower()) + '\n'

        return callback_constants+function_constants+constants

    def get_javascript_class_opening(self):
        template = """function {0}(uid, ipcon) {{
	//{1}

	/*
	Creates an object with the unique device ID *uid* and adds it to
	the IP Connection *ipcon*.
	*/
	Device.call(this, this, uid, ipcon, {2}.DEVICE_IDENTIFIER, {2}.DEVICE_DISPLAY_NAME);
	{2}.prototype = Object.create(Device);
	this.APIVersion = [{3}, {4}, {5}];\n"""

        return template.format(self.get_javascript_class_name(),
                               common.select_lang(self.get_description()),
                               self.get_javascript_class_name(),
                               *self.get_api_version())

    def get_javascript_response_expected(self):
        result = []
        template = '\tthis.responseExpected[{0}.FUNCTION_{1}] = Device.RESPONSE_EXPECTED_{2};\n'

        for packet in self.get_packets('function'):
            result.append(template.format(self.get_javascript_class_name(),
                                          packet.get_name().upper,
                                          packet.get_response_expected().upper()))

        return ''.join(result)

    def get_javascript_callback_formats(self):
        callbacks = ''
        template = "\tthis.callbackFormats[{0}.CALLBACK_{1}] = '{2}';\n"

        for packet in self.get_packets('callback'):
            callbacks += template.format(self.get_javascript_class_name(),
                                         packet.get_name().upper,
                                         packet.get_javascript_format_list('out'))

        return callbacks + '\n'

    def get_javascript_high_level_callbacks(self):
        high_level_callbacks = ''
        template = "\tthis.highLevelCallbacks[{0}.CALLBACK_{1}] = [{4}, {{'fixedLength': {2}, 'singleChunk': {3}}}, null];\n"

        for packet in self.get_packets('callback'):
            fixed_length = ''
            single_chunk = 'false'
            stream = packet.get_high_level('stream_*')

            if stream != None:
                roles = []

                for element in packet.get_elements(direction='out'):
                    if not element.get_role():
                        roles.append(element.get_role())
                        continue

                    role_split = element.get_role().split('_')

                    for i in range(1, len(role_split)):
                        role_split[i] = role_split[i].lower().capitalize()

                    roles.append(''.join(role_split))

                if stream.get_fixed_length() == None:
                    fixed_length = 'null'
                else:
                    fixed_length = stream.get_fixed_length()

                if stream.has_single_chunk():
                    single_chunk = 'true'

                high_level_callbacks += template.format(self.get_javascript_class_name(),
                                                        packet.get_name(skip=-2).upper,
                                                        fixed_length,
                                                        single_chunk,
                                                        repr(list(roles)).replace('None', 'null'))

        return high_level_callbacks + '\n'

    def get_javascript_stream_state_objects(self):
        stream_state_objects = ''
        template = """	this.streamStateObjects[{0}.FUNCTION_{1}] = {{
		'dataMapping': {5},
		'dataMappingStreamIn': {6},
		'streamProperties': {{
			'fixedLength': {2},
			'singleChunk': {3},
			'shortWrite': {4}
		}},
		'responseProperties': {{
			'running': false,
			'runningSubcall': false,
			'runningSubcallOOS': false,
			'waitingFirstChunk': true,
			'timeout': null,
			'data': [],
			'streamInChunkOffset': 0,
			'streamInChunkLength': 0,
			'streamInResponseEmpty': {7},
			'streamInWritten': 0,
			'streamInLLParams': null,
			'responseHandler': null,
			'packFormatString': '{8}',
			'unpackFormatString': '{9}',
			'returnCB': null,
			'errorCB': null,
			'callQueue': []
		}}
	}};
"""

        for packet in self.get_packets('function'):
            if not packet.get_high_level('stream_in') and not packet.get_high_level('stream_out'):
                continue

            fixed_length = ''
            short_write = 'false'
            single_chunk = 'false'
            stream_in_response_empty = 'true'
            stream_in = packet.get_high_level('stream_in')
            stream_out = packet.get_high_level('stream_out')

            if stream_in != None:
                roles = []
                roles_stream_in = []

                for element in packet.get_elements(direction='out'):
                    stream_in_response_empty = 'false'

                    if not element.get_role():
                        roles.append(element.get_role())
                        continue

                    role_split = element.get_role().split('_')

                    for i in range(1, len(role_split)):
                        role_split[i] = role_split[i].lower().capitalize()

                    roles.append(''.join(role_split))

                for element in packet.get_elements(direction='in'):
                    if not element.get_role():
                        roles_stream_in.append(element.get_role())
                        continue

                    role_split = element.get_role().split('_')

                    for i in range(1, len(role_split)):
                        role_split[i] = role_split[i].lower().capitalize()

                    roles_stream_in.append(''.join(role_split))

                if stream_in.get_fixed_length() == None:
                    fixed_length = 'null'
                else:
                    fixed_length = stream_in.get_fixed_length()

                if stream_in.has_single_chunk():
                    single_chunk = 'true'

                if stream_in.has_short_write():
                    short_write = 'true'

                stream_state_objects += template.format(self.get_javascript_class_name(),
                                                        packet.get_name().upper,
                                                        fixed_length,
                                                        single_chunk,
                                                        short_write,
                                                        repr(list(roles)).replace('None', 'null'),
                                                        repr(list(roles_stream_in)).replace('None', 'null'),
                                                        stream_in_response_empty,
                                                        packet.get_javascript_format_list('in'),
                                                        packet.get_javascript_format_list('out'))

            elif stream_out != None:
                roles = []

                for element in packet.get_elements(direction='out'):
                    if not element.get_role():
                        roles.append(element.get_role())
                        continue

                    role_split = element.get_role().split('_')

                    for i in range(1, len(role_split)):
                        role_split[i] = role_split[i].lower().capitalize()

                    roles.append(''.join(role_split))

                if stream_out.get_fixed_length() == None:
                    fixed_length = 'null'
                else:
                    fixed_length = stream_out.get_fixed_length()

                if stream_out.has_single_chunk():
                    single_chunk = 'true'

                stream_state_objects += template.format(self.get_javascript_class_name(),
                                                        packet.get_name().upper,
                                                        fixed_length,
                                                        single_chunk,
                                                        short_write,
                                                        repr(list(roles)).replace('None', 'null'),
                                                        '[]',
                                                        stream_in_response_empty,
                                                        packet.get_javascript_format_list('in'),
                                                        packet.get_javascript_format_list('out'))
        return stream_state_objects + '\n'

    def get_javascript_methods(self):
        methods = ''

        # Normal and low-level
        for packet in self.get_packets('function'):
            doc = packet.get_javascript_formatted_doc()
            name_headless = packet.get_name().headless
            name_upper = packet.get_name().upper
            param_list = packet.get_javascript_parameter_list()
            pack_format = packet.get_javascript_format_list('in')
            unpack_format = packet.get_javascript_format_list('out')
            no_param_method_code = """	this.{0} = function(returnCallback, errorCallback) {{
		/*
		{1}
		*/
		this.ipcon.sendRequest(this, {2}.FUNCTION_{3}, [{4}], '{5}', '{6}', returnCallback, errorCallback, false);
	}};
"""
            param_method_code = """	this.{0} = function({1}, returnCallback, errorCallback) {{
		/*
		{2}
		*/
		this.ipcon.sendRequest(this, {3}.FUNCTION_{4}, [{5}], '{6}', '{7}', returnCallback, errorCallback, false);
	}};
"""

            if len(param_list) == 0:
                methods += no_param_method_code.format(name_headless,
                                                       doc,
                                                       self.get_javascript_class_name(),
                                                       name_upper,
                                                       param_list,
                                                       pack_format,
                                                       unpack_format)
            else:
                methods += param_method_code.format(name_headless,
                                                    param_list,
                                                    doc,
                                                    self.get_javascript_class_name(),
                                                    name_upper,
                                                    param_list,
                                                    pack_format,
                                                    unpack_format)

        # High-level
        no_param_method_code = """
	this.{name} = function(returnCallback, errorCallback) {{
		/*
		{doc}
		*/
		var responseHandler = null;
		var functionToQueue = null;
		var streamStateObject = this.streamStateObjects[{fid}];
		if (streamStateObject['responseProperties']['responseHandler'] === null) {{
			responseHandler = {response_handler_function}
			streamStateObject['responseProperties']['responseHandler'] = responseHandler;
		}}
		if (!streamStateObject['responseProperties']['running']) {{
			streamStateObject['responseProperties']['running'] = true;
			streamStateObject['responseProperties']['returnCB'] = returnCallback;
			streamStateObject['responseProperties']['errorCB'] = errorCallback;
			this.ipcon.sendRequest(this,
			                       {device_class}.FUNCTION_{function_name},
			                       [{param_list}],
			                       '{pack_format}',
			                       '{unpack_format}',
			                       returnCallback,
			                       errorCallback,
			                       true);
		}}
		else {{
			functionToQueue = function (device) {{
				device.{name}.call(device, returnCallback, errorCallback);
			}}
			streamStateObject['responseProperties']['callQueue'].push(functionToQueue);
		}}
	}};
"""
        param_method_code = """
	this.{name} = function({param_list}, returnCallback, errorCallback) {{
		/*
		{doc}
		*/
		var responseHandler = null;
		var functionToQueue = null;
		var streamStateObject = this.streamStateObjects[{fid}];
		if (streamStateObject['responseProperties']['responseHandler'] === null) {{
			responseHandler = {response_handler_function}
			streamStateObject['responseProperties']['responseHandler'] = responseHandler;
		}}
		if (!streamStateObject['responseProperties']['running']) {{
			streamStateObject['responseProperties']['running'] = true;
			streamStateObject['responseProperties']['returnCB'] = returnCallback;
			streamStateObject['responseProperties']['errorCB'] = errorCallback;
			this.ipcon.sendRequest(this,
			                       {device_class}.FUNCTION_{function_name},
			                       [{param_list}],
			                       '{pack_format}',
			                       '{unpack_format}',
			                       returnCallback,
			                       errorCallback,
			                       true);
		}}
		else {{
			functionToQueue = function (device) {{
				device.{name}.call(device, {param_list}, returnCallback, errorCallback);
			}}
			streamStateObject['responseProperties']['callQueue'].push(functionToQueue);
		}}
	}};
"""

        template_response_handler_stream_out = """
				function (device, fid, packetResponse) {{
					var result = [];
					var llvalues = null;
					var packetErrorFlag = 0;
					var rolesMappedData = [];
					var {stream_name_headless}Length = null;
					var {stream_name_headless}ChunkData = null;
					var {stream_name_headless}OutOfSync = false;
					var streamStateObject = device.streamStateObjects[fid];
					var {stream_name_headless}ChunkOffset = null;
					var payload = device.ipcon.getPayloadFromPacket(packetResponse);

					packetErrorFlag = device.ipcon.getEFromPacket(packetResponse);

					if (packetErrorFlag !== 0) {{
						if (streamStateObject['responseProperties']['errorCB'] !== undefined) {{
							if (packetErrorFlag === 1) {{
								streamStateObject['responseProperties']['errorCB'].call(device, IPConnection.ERROR_INVALID_PARAMETER);
							}}
							else if (packetErrorFlag === 2) {{
								streamStateObject['responseProperties']['errorCB'].call(device, IPConnection.ERROR_FUNCTION_NOT_SUPPORTED);
							}}
							else {{
								streamStateObject['responseProperties']['errorCB'].call(device, IPConnection.ERROR_UNKNOWN_ERROR);
							}}
						}}

						device.resetStreamStateObject(streamStateObject);

						if (streamStateObject['responseProperties']['callQueue'].length > 0) {{
							streamStateObject['responseProperties']['callQueue'].shift()(device);
						}}

						return;
					}}

					if (payload.length === 0) {{
						device.resetStreamStateObject(streamStateObject);

						if (streamStateObject['responseProperties']['callQueue'].length > 0) {{
							streamStateObject['responseProperties']['callQueue'].shift()(device);
						}}

						return;
					}}

					llvalues = device.ipcon.unpack(payload,
					                               streamStateObject['responseProperties']['unpackFormatString']);

					for (var i = 0; i < streamStateObject['dataMapping'].length; i++) {{
						if (streamStateObject['dataMapping'][i] === 'streamChunkData') {{
							{stream_name_headless}ChunkData = llvalues[i];
						}}
						else if (streamStateObject['dataMapping'][i] === 'streamChunkOffset') {{
							{stream_name_headless}ChunkOffset = llvalues[i];
						}}
					}}

					{get_length}
					{body}
				}};
"""

        template_response_handler_stream_out_get_length_fixed = """{stream_name_headless}Length = streamStateObject['streamProperties']['fixedLength'];
"""

        template_response_handler_stream_out_get_length_variable = """for (var i = 0; i < streamStateObject['dataMapping'].length; i++) {{
						if (streamStateObject['dataMapping'][i] === 'streamLength') {{
							{stream_name_headless}Length = llvalues[i];
							break;
						}}
					}}
"""

        template_response_handler_stream_out_body_subcall = \
            """device.ipcon.sendRequest(device, \
{device_class}.FUNCTION_{function_name}, \
[{param_list}], \
'{pack_format}', \
'{unpack_format}', \
streamStateObject['responseProperties']['returnCB'], \
streamStateObject['responseProperties']['errorCB'], \
true);"""

        template_response_handler_stream_out_body_single_chunk = """{stream_name_headless}ChunkOffset = 0;

					if (streamStateObject['responseProperties']['returnCB']) {{
						for (var i = 0; i < streamStateObject['dataMapping'].length; i++) {{
							rolesMappedData.push({{'role': streamStateObject['dataMapping'][i], 'llvalue': llvalues[i]}});
						}}

						for (var i = 0; i < rolesMappedData.length; i++) {{
							if (rolesMappedData[i]['role'] === 'streamChunkData') {{
								result.push({stream_name_headless}ChunkData.splice(0, {stream_name_headless}Length));
							}}
							else if (rolesMappedData[i]['role'] === null) {{
								result.push(rolesMappedData[i]['llvalue']);
							}}
						}}

						streamStateObject['responseProperties']['returnCB'].apply(device, result);
					}}

					device.resetStreamStateObject(streamStateObject);

					if (streamStateObject['responseProperties']['callQueue'].length > 0) {{
						streamStateObject['responseProperties']['callQueue'].shift()(device);
					}}"""

        template_response_handler_stream_out_body_fixed_stream_length = """function handleOOS() {{
						if (({stream_name_headless}ChunkOffset + {chunk_cardinality}) < {stream_name_headless}Length) {{
							streamStateObject['responseProperties']['runningSubcallOOS'] = true;
							{subcall}

							return;
						}}

						if (streamStateObject['responseProperties']['errorCB']) {{
							streamStateObject['responseProperties']['errorCB'].call(device, IPConnection.ERROR_STREAM_OUT_OF_SYNC);
						}}

						device.resetStreamStateObject(streamStateObject);

						if (streamStateObject['responseProperties']['callQueue'].length > 0) {{
							streamStateObject['responseProperties']['callQueue'].shift()(device);
						}}
					}}

					if (streamStateObject['responseProperties']['waitingFirstChunk']) {{
						streamStateObject['responseProperties']['waitingFirstChunk'] = false;

						if ({stream_name_headless}ChunkOffset === ((1 << {shift_size}) - 1)) {{ // maximum chunk offset -> stream has no data
							{stream_name_headless}Length = 0;
							{stream_name_headless}OutOfSync = false;
							streamStateObject['responseProperties']['data'].length = 0;
						}}
						else {{
								{stream_name_headless}OutOfSync = ({stream_name_headless}ChunkOffset !== 0);
								streamStateObject['responseProperties']['data'] = {stream_name_headless}ChunkData;
						}}
					}}

					if (!streamStateObject['responseProperties']['runningSubcallOOS']) {{
						if (!streamStateObject['responseProperties']['runningSubcall']) {{
							if (!{stream_name_headless}OutOfSync &&
								(streamStateObject['responseProperties']['data'].length < {stream_name_headless}Length)) {{
									streamStateObject['responseProperties']['runningSubcall'] = true;
									{subcall}

									return;
							}}
						}}
						else {{
							{stream_name_headless}OutOfSync =
								({stream_name_headless}ChunkOffset !== streamStateObject['responseProperties']['data'].length);

							if (!{stream_name_headless}OutOfSync &&
								(streamStateObject['responseProperties']['data'].length < {stream_name_headless}Length)) {{
									streamStateObject['responseProperties']['data'] =
										streamStateObject['responseProperties']['data'].concat({stream_name_headless}ChunkData);
									if (streamStateObject['responseProperties']['data'].length >= {stream_name_headless}Length) {{
										streamStateObject['responseProperties']['data'] =
											streamStateObject['responseProperties']['data'].splice(0, {stream_name_headless}Length);
									}}
									else {{
										{subcall}

										return;
									}}
							}}
						}}
					}}
					else {{
						handleOOS();

						return;
					}}

					if ({stream_name_headless}OutOfSync) {{ // Discard remaining stream to bring it back in-sync
						handleOOS();

						return;
					}}

					if (streamStateObject['responseProperties']['returnCB']) {{
						for (var i = 0; i < streamStateObject['dataMapping'].length; i++) {{
							rolesMappedData.push({{'role': streamStateObject['dataMapping'][i], 'llvalue': llvalues[i]}});
						}}

						for (var i = 0; i < rolesMappedData.length; i++) {{
							if (rolesMappedData[i]['role'] === 'streamChunkData') {{
								result.push(streamStateObject['responseProperties']['data'].splice(0, {stream_name_headless}Length));
							}}
							else if (rolesMappedData[i]['role'] === null) {{
								result.push(rolesMappedData[i]['llvalue']);
							}}
						}}

						streamStateObject['responseProperties']['returnCB'].apply(device, result);
					}}

					device.resetStreamStateObject(streamStateObject);

					if (streamStateObject['responseProperties']['callQueue'].length > 0) {{
						streamStateObject['responseProperties']['callQueue'].shift()(device);
					}}"""

        template_response_handler_stream_out_body_variable_stream_length = """function handleOOS() {{
						if (({stream_name_headless}ChunkOffset + {chunk_cardinality}) < {stream_name_headless}Length) {{
							streamStateObject['responseProperties']['runningSubcallOOS'] = true;
							{subcall}

							return;
						}}

						if (streamStateObject['responseProperties']['errorCB']) {{
							streamStateObject['responseProperties']['errorCB'].call(device, IPConnection.ERROR_STREAM_OUT_OF_SYNC);
						}}

						device.resetStreamStateObject(streamStateObject);

						if (streamStateObject['responseProperties']['callQueue'].length > 0) {{
							streamStateObject['responseProperties']['callQueue'].shift()(device);
						}}
					}}

					if (streamStateObject['responseProperties']['waitingFirstChunk']) {{
						streamStateObject['responseProperties']['waitingFirstChunk'] = false;
						{stream_name_headless}OutOfSync = ({stream_name_headless}ChunkOffset !== 0);
						streamStateObject['responseProperties']['data'] = {stream_name_headless}ChunkData;
					}}

					if (!streamStateObject['responseProperties']['runningSubcallOOS']) {{
						if (!streamStateObject['responseProperties']['runningSubcall']) {{
							if (!{stream_name_headless}OutOfSync &&
							    (streamStateObject['responseProperties']['data'].length < {stream_name_headless}Length)) {{
							        streamStateObject['responseProperties']['runningSubcall'] = true;
							        {subcall}

							        return;
							}}
						}}
						else {{
							{stream_name_headless}OutOfSync =
								({stream_name_headless}ChunkOffset !== streamStateObject['responseProperties']['data'].length);

							if (!{stream_name_headless}OutOfSync &&
								(streamStateObject['responseProperties']['data'].length < {stream_name_headless}Length)) {{
									streamStateObject['responseProperties']['data'] =
										streamStateObject['responseProperties']['data'].concat({stream_name_headless}ChunkData);

									if (streamStateObject['responseProperties']['data'].length >= {stream_name_headless}Length) {{
										streamStateObject['responseProperties']['data'] =
											streamStateObject['responseProperties']['data'].splice(0, {stream_name_headless}Length);
									}}
									else {{
										{subcall}

										return;
									}}
							}}
						}}
					}}
					else{{
						handleOOS();

						return;
					}}

					if ({stream_name_headless}OutOfSync) {{ // Discard remaining stream to bring it back in-sync
						handleOOS();

						return;
					}}

					if (streamStateObject['responseProperties']['returnCB']) {{
						for (var i = 0; i < streamStateObject['dataMapping'].length; i++) {{
							rolesMappedData.push({{'role': streamStateObject['dataMapping'][i], 'llvalue': llvalues[i]}});
						}}

						for (var i = 0; i < rolesMappedData.length; i++) {{
							if (rolesMappedData[i]['role'] === 'streamChunkData') {{
								result.push(streamStateObject['responseProperties']['data'].splice(0, {stream_name_headless}Length));
							}}
							else if (rolesMappedData[i]['role'] === null) {{
								result.push(rolesMappedData[i]['llvalue']);
							}}
						}}

						streamStateObject['responseProperties']['returnCB'].apply(device, result);
					}}

					device.resetStreamStateObject(streamStateObject);

					if (streamStateObject['responseProperties']['callQueue'].length > 0) {{
						streamStateObject['responseProperties']['callQueue'].shift()(device);
					}}
					"""

        param_method_code_stream_in = """	this.{name} = function({param_list_hl}, returnCallback, errorCallback) {{
		/*
		{doc}
		*/

		var {stream_length_param_name_ll} = 0;
		var {stream_chunk_data_param_name_ll} = [];
		var {stream_chunk_offset_param_name_ll} = 0;
		var streamStateObject = this.streamStateObjects[{fid}];

		if ({data_param_name_hl}.length > {stream_max_length}) {{
			if (errorCallback !== null){{
				errorCallback(IPConnection.ERROR_INVALID_PARAMETER);
			}}

			this.resetStreamStateObject(streamStateObject);

			if (streamStateObject['responseProperties']['callQueue'].length > 0) {{
				streamStateObject['responseProperties']['callQueue'].shift()(device);
			}}

			return;
		}}

		if (!this.getResponseExpected({fid})) {{
			if (streamStateObject['streamProperties']['fixedLength']) {{
				{stream_length_param_name_ll} = streamStateObject['streamProperties']['fixedLength'];
			}}
			else {{
				{stream_length_param_name_ll} = {data_param_name_hl}.length;
			}}

			if (streamStateObject['streamProperties']['singleChunk']) {{
				{stream_chunk_data_param_name_ll} =
					this.ipcon.createChunkData({data_param_name_hl}, 0, {chunk_cardinality}, '\\0');

				this.ipcon.sendRequest(this,
				                       {device_class}.FUNCTION_{function_name},
				                       [{param_list_ll}],
				                       '{pack_format}',
				                       '{unpack_format}',
				                       returnCallback,
				                       errorCallback,
				                       false);
			}}
			else {{
				while ({stream_chunk_offset_param_name_ll} < {data_param_name_hl}.length) {{
					{stream_chunk_data_param_name_ll} =
						this.ipcon.createChunkData({data_param_name_hl}, {stream_chunk_offset_param_name_ll}, {chunk_cardinality}, '\\0');

					this.ipcon.sendRequest(this,
					                       {device_class}.FUNCTION_{function_name},
					                       [{param_list_ll}],
					                       '{pack_format}',
					                       '{unpack_format}',
					                       returnCallback,
					                       errorCallback,
					                       false);

					{stream_chunk_offset_param_name_ll} += {chunk_cardinality};
				}}
			}}

			if (returnCallback) {{
				returnCallback();
			}}
		}}
		else {{
			var responseHandler = null;
			var functionToQueue = null;

			if (streamStateObject['responseProperties']['responseHandler'] === null) {{
				responseHandler = {response_handler_function}
				streamStateObject['responseProperties']['responseHandler'] = responseHandler;
			}}

			if (!streamStateObject['responseProperties']['running']) {{
				streamStateObject['responseProperties']['running'] = true;
				streamStateObject['responseProperties']['returnCB'] = returnCallback;
				streamStateObject['responseProperties']['errorCB'] = errorCallback;
				streamStateObject['responseProperties']['data'].length = 0;
				streamStateObject['responseProperties']['data'].push.apply(streamStateObject['responseProperties']['data'],
				                                                           {data_param_name_hl});

				if (streamStateObject['streamProperties']['fixedLength']) {{
					{stream_length_param_name_ll} = streamStateObject['streamProperties']['fixedLength'];
				}}
				else {{
					{stream_length_param_name_ll} = {data_param_name_hl}.length;
				}}

				{stream_chunk_offset_param_name_ll} = 0;
				{stream_chunk_data_param_name_ll} =
					this.ipcon.createChunkData({data_param_name_hl}, 0, {chunk_cardinality}, '\\0');

				streamStateObject['responseProperties']['streamInChunkOffset'] = {chunk_cardinality};
				streamStateObject['responseProperties']['streamInChunkLength'] = {chunk_cardinality};
				streamStateObject['responseProperties']['streamInLLParams'] = [{param_list_ll}];

				this.ipcon.sendRequest(this,
				                       {device_class}.FUNCTION_{function_name},
				                       [{param_list_ll}],
				                       '{pack_format}',
				                       '{unpack_format}',
				                       returnCallback,
				                       errorCallback,
				                       true);
			}}
			else {{
				functionToQueue = function (device) {{
					device.{name}.call(device, {param_list_hl}, returnCallback, errorCallback);
				}}

				streamStateObject['responseProperties']['callQueue'].push(functionToQueue);
			}}
		}}
	}};
"""

        for packet in self.get_packets('function'):
            stream_in = packet.get_high_level('stream_in')
            stream_out = packet.get_high_level('stream_out')

            if stream_in != None:
                param_list_hl_arr = []
                param_stream_params_ll = {}
                fid = packet.get_function_id()
                doc = packet.get_javascript_formatted_doc()
                param_stream_params_ll['stream_length'] = None
                param_stream_params_ll['stream_chunk_data'] = None
                param_stream_params_ll['stream_chunk_offset'] = None

                template_response_handler_stream_in = """function (device, fid, packetResponse) {{
					var result = [];
					var payload = null;
					var llvalues = null;
					var packetErrorFlag = 0;
					var rolesMappedData = [];
					var shortWriteWritten = -1;
					var streamStateObject = device.streamStateObjects[fid];
					var responseEmpty = streamStateObject['responseProperties']['streamInResponseEmpty'];
					var {stream_length_param_name_ll} = 0;
					var {stream_chunk_data_param_name_ll} = [];
					var {stream_chunk_offset_param_name_ll} = 0;

					function doNextLLCall() {{
						{stream_length_param_name_ll} = streamStateObject['responseProperties']['data'].length;
						{stream_chunk_data_param_name_ll} =
							device.ipcon.createChunkData(streamStateObject['responseProperties']['data'],
							                             streamStateObject['responseProperties']['streamInChunkOffset'],
							                             streamStateObject['responseProperties']['streamInChunkLength'],
							                             '\\0');
						{stream_chunk_offset_param_name_ll} = streamStateObject['responseProperties']['streamInChunkOffset'];

						for (var i = 0; i < streamStateObject['dataMappingStreamIn'].length; i++) {{
							if (streamStateObject['dataMappingStreamIn'][i] === null) {{
								continue;
							}}

							if (streamStateObject['dataMappingStreamIn'][i].endsWith('Length')) {{
								streamStateObject['responseProperties']['streamInLLParams'][i] = {stream_length_param_name_ll};
							}}
							else if (streamStateObject['dataMappingStreamIn'][i].endsWith('Offset')) {{
								streamStateObject['responseProperties']['streamInLLParams'][i] = {stream_chunk_offset_param_name_ll};
							}}
							else if (streamStateObject['dataMappingStreamIn'][i].endsWith('Data')) {{
								streamStateObject['responseProperties']['streamInLLParams'][i] = {stream_chunk_data_param_name_ll};
							}}
						}}

						device.ipcon.sendRequest(device,
						                         {device_class}.FUNCTION_{function_name},
						                         streamStateObject['responseProperties']['streamInLLParams'],
						                         '{pack_format}',
						                         '{unpack_format}',
						                         returnCallback,
						                         errorCallback,
						                         true);

						streamStateObject['responseProperties']['streamInChunkOffset'] += {chunk_cardinality};
					}}

					function handleStreamInDone() {{
						if (streamStateObject['responseProperties']['returnCB']) {{
							if (streamStateObject['streamProperties']['shortWrite']) {{
								for (var i = 0; i < streamStateObject['dataMapping'].length; i++) {{
									if (streamStateObject['dataMapping'][i].endsWith('Written')) {{
										result[i] = streamStateObject['responseProperties']['streamInWritten'];
										break;
									}}
								}}
							}}

							if (!responseEmpty) {{
								streamStateObject['responseProperties']['returnCB'].apply(device, result);
							}}
							else {{
								streamStateObject['responseProperties']['returnCB'].apply(device);
							}}
						}}

						device.resetStreamStateObject(streamStateObject);

						if (streamStateObject['responseProperties']['callQueue'].length > 0) {{
							streamStateObject['responseProperties']['callQueue'].shift()(device);
						}}
					}}

					if (!streamStateObject) {{
						return;
					}}

					packetErrorFlag = device.ipcon.getEFromPacket(packetResponse);

					if (packetErrorFlag !== 0) {{
						if (streamStateObject['responseProperties']['errorCB'] !== undefined) {{
							if (packetErrorFlag === 1) {{
								streamStateObject['responseProperties']['errorCB'].call(device, IPConnection.ERROR_INVALID_PARAMETER);
							}}
							else if (packetErrorFlag === 2) {{
								streamStateObject['responseProperties']['errorCB'].call(device, IPConnection.ERROR_FUNCTION_NOT_SUPPORTED);
							}}
							else {{
								streamStateObject['responseProperties']['errorCB'].call(device, IPConnection.ERROR_UNKNOWN_ERROR);
							}}
						}}

						device.resetStreamStateObject(streamStateObject);

						if (streamStateObject['responseProperties']['callQueue'].length > 0) {{
							streamStateObject['responseProperties']['callQueue'].shift()(device);
						}}

						return;
					}}

					if (responseEmpty) {{
						if (streamStateObject['streamProperties']['singleChunk']) {{
							handleStreamInDone();

							return;
						}}

						if (streamStateObject['responseProperties']['streamInChunkOffset'] < streamStateObject['responseProperties']['data'].length) {{
							doNextLLCall();
						}}
						else {{
							handleStreamInDone();
						}}
					}}
					else {{
						payload = device.ipcon.getPayloadFromPacket(packetResponse);
						llvalues = device.ipcon.unpack(payload,
						                               streamStateObject['responseProperties']['unpackFormatString']);

						if (!payload || !llvalues) {{
							device.resetStreamStateObject(streamStateObject);

							if (streamStateObject['responseProperties']['callQueue'].length > 0) {{
								streamStateObject['responseProperties']['callQueue'].shift()(device);
							}}

							return;
						}}

						for (var i = 0; i < streamStateObject['dataMapping'].length; i++) {{
							result.push(llvalues[i]);
						}}

						if (streamStateObject['streamProperties']['singleChunk']) {{
							if (streamStateObject['responseProperties']['returnCB']) {{
								streamStateObject['responseProperties']['returnCB'].apply(device, result);
							}}

							device.resetStreamStateObject(streamStateObject);

							if (streamStateObject['responseProperties']['callQueue'].length > 0) {{
								streamStateObject['responseProperties']['callQueue'].shift()(device);
							}}

							return;
						}}

						if (streamStateObject['streamProperties']['shortWrite']) {{
							for (var i = 0; i < streamStateObject['dataMapping'].length; i++) {{
								if (streamStateObject['dataMapping'][i].endsWith('Written')) {{
									shortWriteWritten = llvalues[i];
									streamStateObject['responseProperties']['streamInWritten'] += shortWriteWritten;
									break;
								}}
							}}
							if ((shortWriteWritten !== -1) && (shortWriteWritten < {chunk_cardinality})) {{
								// Either last chunk or short write
								handleStreamInDone();
								return;
							}}
						}}

						if (streamStateObject['responseProperties']['streamInChunkOffset'] < streamStateObject['responseProperties']['data'].length) {{
							doNextLLCall();
						}}
						else {{
							handleStreamInDone();
						}}
					}}
				}};
"""

                name_upper = packet.get_name().upper
                name_headless = packet.get_name(skip=-2).headless
                param_list_ll = packet.get_javascript_parameter_list()
                pack_format = packet.get_javascript_format_list('in')
                unpack_format = packet.get_javascript_format_list('out')
                chunk_cardinality = stream_in.get_chunk_data_element().get_cardinality()
                stream_name_headless = stream_in.get_name().headless

                for element in packet.get_elements(direction='in'):
                    role = element.get_role()

                    if role:
                        if role == 'stream_length':
                            param_stream_params_ll['stream_length'] = element.get_name().headless
                        elif role == 'stream_chunk_offset':
                            param_stream_params_ll['stream_chunk_offset'] = element.get_name().headless
                        elif role == 'stream_chunk_data':
                            param_stream_params_ll['stream_chunk_data'] = element.get_name().headless
                            param_list_hl_arr.append(stream_in.get_name().headless)

                        continue

                    param_list_hl_arr.append(element.get_name().headless)

                data_param_name_hl = stream_in.get_name().headless

                param_list_hl = ', '.join(param_list_hl_arr)

                response_handler_function = template_response_handler_stream_in.format(stream_length_param_name_ll = param_stream_params_ll['stream_length'],
                                                                                       stream_chunk_data_param_name_ll = param_stream_params_ll['stream_chunk_data'],
                                                                                       stream_chunk_offset_param_name_ll = param_stream_params_ll['stream_chunk_offset'],device_class = self.get_javascript_class_name(),
                                                                                       function_name = name_upper,
                                                                                       param_list_ll = param_list_ll,
                                                                                       pack_format = pack_format,
                                                                                       unpack_format = unpack_format,
                                                                                       chunk_cardinality = chunk_cardinality)

                methods += param_method_code_stream_in.format(name = name_headless,
                                                              param_list_hl = param_list_hl,
                                                              doc = doc,
                                                              stream_length_param_name_ll = param_stream_params_ll['stream_length'],
                                                              stream_chunk_data_param_name_ll = param_stream_params_ll['stream_chunk_data'],
                                                              stream_chunk_offset_param_name_ll = param_stream_params_ll['stream_chunk_offset'],
                                                              fid = fid,
                                                              stream_max_length = abs(stream_in.get_data_element().get_cardinality()),
                                                              data_param_name_hl = data_param_name_hl,
                                                              chunk_cardinality = chunk_cardinality,
                                                              device_class = self.get_javascript_class_name(),
                                                              function_name = name_upper,
                                                              param_list_ll = param_list_ll,
                                                              pack_format = pack_format,
                                                              unpack_format = unpack_format,
                                                              response_handler_function = response_handler_function)

            elif stream_out != None:
                fid = packet.get_function_id()
                doc = packet.get_javascript_formatted_doc()
                name_upper = packet.get_name().upper
                name_headless = packet.get_name(skip=-2).headless
                param_list = packet.get_javascript_parameter_list()
                pack_format = packet.get_javascript_format_list('in')
                unpack_format = packet.get_javascript_format_list('out')
                stream_name_headless = stream_out.get_name().headless

                if stream_out.has_single_chunk():
                    # Single chunk stream
                    get_length = \
                        template_response_handler_stream_out_get_length_variable.format(stream_name_headless = stream_name_headless)
                    body = \
                        template_response_handler_stream_out_body_single_chunk.format(stream_name_headless = stream_name_headless)

                    response_handler_function = \
                        template_response_handler_stream_out.format(stream_name_headless = stream_name_headless,
                                                                    get_length = get_length,
                                                                    body = body)
                elif stream_out.get_fixed_length() != None:
                    # Fixed stream length
                    shift_size = int(stream_out.get_chunk_offset_element().get_type().replace('uint', ''))
                    subcall = template_response_handler_stream_out_body_subcall.format(device_class = self.get_javascript_class_name(),
                                                                                       function_name = name_upper,
                                                                                       param_list = param_list,
                                                                                       pack_format = pack_format,
                                                                                       unpack_format = unpack_format)
                    chunk_cardinality = stream_out.get_chunk_data_element().get_cardinality()

                    get_length = \
                        template_response_handler_stream_out_get_length_fixed.format(stream_name_headless = stream_name_headless)
                    body = \
                        template_response_handler_stream_out_body_fixed_stream_length.format(stream_name_headless = stream_name_headless,
                                                                                             shift_size = shift_size,
                                                                                             subcall = subcall,
                                                                                             chunk_cardinality = chunk_cardinality)

                    response_handler_function = \
                        template_response_handler_stream_out.format(stream_name_headless = stream_name_headless,
                                                                    get_length = get_length,
                                                                    body = body)
                else:
                    # Variable length stream
                    shift_size = int(stream_out.get_chunk_offset_element().get_type().replace('uint', ''))
                    subcall = template_response_handler_stream_out_body_subcall.format(device_class = self.get_javascript_class_name(),
                                                                                       function_name = name_upper,
                                                                                       param_list = param_list,
                                                                                       pack_format = pack_format,
                                                                                       unpack_format = unpack_format)
                    chunk_cardinality = stream_out.get_chunk_data_element().get_cardinality()

                    get_length = \
                        template_response_handler_stream_out_get_length_variable.format(stream_name_headless = stream_name_headless)
                    body = \
                        template_response_handler_stream_out_body_variable_stream_length.format(stream_name_headless = stream_name_headless,
                                                                                                shift_size = shift_size,
                                                                                                subcall = subcall,
                                                                                                chunk_cardinality = chunk_cardinality)

                    response_handler_function = \
                        template_response_handler_stream_out.format(stream_name_headless = stream_name_headless,
                                                                    get_length = get_length,
                                                                    body = body)

                if len(param_list) == 0:
                    methods += no_param_method_code.format(name = name_headless,
                                                           doc = doc,
                                                           fid = fid,
                                                           device_class = self.get_javascript_class_name(),
                                                           function_name = name_upper,
                                                           response_handler_function = response_handler_function,
                                                           param_list = param_list,
                                                           pack_format = pack_format,
                                                           unpack_format = unpack_format)
                else:
                    methods += param_method_code.format(name = name_headless,
                                                        param_list = param_list,
                                                        doc = doc,
                                                        fid = fid,
                                                        device_class = self.get_javascript_class_name(),
                                                        function_name = name_upper,
                                                        response_handler_function = response_handler_function,
                                                        pack_format = pack_format,
                                                        unpack_format = unpack_format)

        return methods

    def get_javascript_class_closing(self):
        template = """}}

module.exports = {0};
"""

        return template.format(self.get_javascript_class_name())

    def get_javascript_source(self):
        source  = self.get_javascript_require()
        source += self.get_javascript_constants()
        source += self.get_javascript_class_opening()
        source += self.get_javascript_response_expected()
        source += self.get_javascript_callback_formats()
        source += self.get_javascript_high_level_callbacks()
        source += self.get_javascript_stream_state_objects()
        source += self.get_javascript_methods()
        source += self.get_javascript_class_closing()

        return source

class JavaScriptBindingsPacket(javascript_common.JavaScriptPacket):
    def get_javascript_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return '\n\t\t'.join(text.strip().split('\n'))

    def get_javascript_format_list(self, io):
        forms = []

        for element in self.get_elements(direction=io):
            forms.append(element.get_javascript_struct_format())

        return ' '.join(forms)

class JavaScriptBindingsGenerator(javascript_common.JavascriptGeneratorTrait, common.BindingsGenerator):
    def get_bindings_name(self):
        return 'javascript'

    def get_bindings_display_name(self):
        return 'JavaScript'

    def get_device_class(self):
        return JavaScriptBindingsDevice

    def get_packet_class(self):
        return JavaScriptBindingsPacket

    def get_element_class(self):
        return javascript_common.JavaScriptElement

    def prepare(self):
        ret = common.BindingsGenerator.prepare(self)

        browser_api_filename = os.path.join(self.get_bindings_dir(), 'BrowserAPI.js')
        npm_main_filename = os.path.join(self.get_bindings_dir(), 'TinkerforgeNPM.js')
        source_main_filename = os.path.join(self.get_bindings_dir(), 'TinkerforgeSource.js')

        self.browser_api_file = open(browser_api_filename, 'w')
        self.npm_main_file = open(npm_main_filename, 'w')
        self.source_main_file = open(source_main_filename, 'w')

        self.released_files.append('BrowserAPI.js')
        self.released_files.append('TinkerforgeNPM.js')
        self.released_files.append('TinkerforgeSource.js')

        self.browser_api_file.write("""function Tinkerforge() {
	this.IPConnection = require('./IPConnection');
""")

        self.npm_main_file.write("""function Tinkerforge() {
	this.IPConnection = require('./lib/IPConnection');
""")

        self.source_main_file.write("""function Tinkerforge() {
	this.IPConnection = require('./Tinkerforge/IPConnection');
""")

        return ret

    def add_browser_api_function(self, device):
        if device.is_released():
            api = """	this.{0}{1} = require('./{0}{1}');
"""
            api_format = api.format(device.get_category().camel, device.get_name().camel)
            self.browser_api_file.write(api_format)

    def add_npm_main_function(self, device):
        if device.is_released():
            npm_main = """	this.{0}{1} = require('./lib/{0}{1}');
"""
            npm_main_format = npm_main.format(device.get_category().camel, device.get_name().camel)
            self.npm_main_file.write(npm_main_format)

    def add_source_main_function(self, device):
        if device.is_released():
            source_main = """	this.{0}{1} = require('./Tinkerforge/{0}{1}');
"""
            source_main_format = source_main.format(device.get_category().camel, device.get_name().camel)
            self.source_main_file.write(source_main_format)

    def generate(self, device):
        self.add_browser_api_function(device)
        self.add_npm_main_function(device)
        self.add_source_main_function(device)

        filename = '{0}{1}.js'.format(device.get_category().camel, device.get_name().camel)

        with open(os.path.join(self.get_bindings_dir(), filename), 'w') as f:
            f.write(device.get_javascript_source())

        if device.is_released():
            self.released_files.append(filename)

    def finish(self):
        self.browser_api_file.write("""}

global.Tinkerforge = new Tinkerforge();""")
        self.browser_api_file.close()

        self.npm_main_file.write("""}

module.exports = new Tinkerforge();""")
        self.npm_main_file.close()

        self.source_main_file.write("""}

module.exports = new Tinkerforge();""")
        self.source_main_file.close()

        return common.BindingsGenerator.finish(self)

def generate(root_dir):
    common.generate(root_dir, 'en', JavaScriptBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
