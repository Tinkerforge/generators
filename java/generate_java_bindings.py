#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java Bindings Generator
Copyright (C) 2012-2015, 2017-2018 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2013 Olaf Lüke <olaf@tinkerforge.com>

generate_java_bindings.py: Generator for Java bindings

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

import math
import sys
import os
from xml.sax.saxutils import escape

sys.path.append(os.path.split(os.getcwd())[0])
import common
import java_common

class JavaBindingsDevice(java_common.JavaDevice):
    def specialize_java_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return '{{@link {0}.{1}Listener}}'.format(packet.get_device().get_java_class_name(),
                                                          packet.get_name(skip=-2 if high_level else 0).camel)
            else:
                return '{{@link {0}#{1}({2})}}'.format(packet.get_device().get_java_class_name(),
                                                       packet.get_name(skip=-2 if high_level else 0).headless,
                                                       packet.get_java_parameters(context='link', high_level=high_level))

        return self.specialize_doc_rst_links(text, specializer)

    def get_java_import(self):
        if self.get_generator().is_octave():
            template = """{0}
package com.tinkerforge;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.Arrays;
import java.util.List;
import org.octave.OctaveReference;
"""
        else:
            template = """{0}
package com.tinkerforge;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.Arrays;
import java.util.List;
"""

        if self.get_long_display_name() == 'RS232 Bricklet' and not self.get_generator().is_octave():
            template += 'import java.util.ArrayList;\n'

        return template.format(self.get_generator().get_header_comment('asterisk'))

    def get_java_class(self):
        template = """
/**
 * {1}
 */
public class {0} extends Device {{
	public final static int DEVICE_IDENTIFIER = {2};
	public final static String DEVICE_DISPLAY_NAME = "{3}";

"""

        return template.format(self.get_java_class_name(),
                               common.select_lang(self.get_description()),
                               self.get_device_identifier(),
                               self.get_long_display_name())

    def get_matlab_callback_data_objects(self):
        objects = ''
        template = """
	public class {0}CallbackData extends java.util.EventObject {{
		private static final long serialVersionUID = 1L;

{1}

		public {0}CallbackData(Object device{3}) {{
			super(device);

{4}
		}}

		public String toString() {{
			return "[" + {2} "]";
		}}
	}}
"""

        # normal and low-level
        for packet in self.get_packets('callback'):
            if packet.has_prototype_in_device():
                continue

            params = []
            tostr = []
            assignments = []

            for element in packet.get_elements():
                type_ = element.get_java_type()
                name = element.get_name().headless

                if element.get_cardinality() != 1 and element.get_type() != 'string':
                    to = '"{0} = " + Arrays.toString({0}) +'.format(name)
                else:
                    to = '"{0} = " + {0} +'.format(name)

                tostr.append(to)
                params.append('\t\tpublic {0} {1};'.format(type_, name))
                assignments.append('\t\t\tthis.{0} = {0};'.format(name))

            objects += template.format(packet.get_java_object_name(),
                                       '\n'.join(params),
                                       ' ", " + '.join(tostr),
                                       common.wrap_non_empty(', ', packet.get_java_parameters(), ''),
                                       '\n'.join(assignments))

        # high-level
        for packet in self.get_packets('callback'):
            if packet.has_prototype_in_device() or not packet.has_high_level():
                continue

            params = []
            tostr = []
            assignments = []

            for element in packet.get_elements(high_level=True):
                type_ = element.get_java_type()
                name = element.get_name().headless

                if element.get_cardinality() != 1 and element.get_type() != 'string':
                    to = '"{0} = " + Arrays.toString({0}) +'.format(name)
                else:
                    to = '"{0} = " + {0} +'.format(name)

                tostr.append(to)
                params.append('\t\tpublic {0} {1};'.format(type_, name))
                assignments.append('\t\t\tthis.{0} = {0};'.format(name))

            objects += template.format(packet.get_java_object_name(high_level=True),
                                       '\n'.join(params),
                                       ' ", " + '.join(tostr),
                                       common.wrap_non_empty(', ', packet.get_java_parameters(high_level=True), ''),
                                       '\n'.join(assignments))

        return objects

    def get_java_return_objects(self):
        objects = ''
        template = """
	public class {0} {{
{1}

		public String toString() {{
			return "[" + {2} "]";
		}}
	}}
"""
        template_high_level = """
	public class {0} {{
{1}

		public {0}({3}) {{
{4}
		}}

		public String toString() {{
			return "[" + {2} "]";
		}}
	}}
"""

        def make_return_object(packet, high_level):
            params = []
            tostr = []
            ctors = []
            assignments = []

            for element in packet.get_elements(direction='out', high_level=high_level):
                type_ = element.get_java_type()
                name = element.get_name().headless

                if element.get_cardinality() != 1 and element.get_type() != 'string':
                    if not high_level:
                        new = ' = {0}'.format(element.get_java_new())
                    else:
                        new = ''

                    to = '"{0} = " + Arrays.toString({0}) +'.format(name)
                else:
                    new = ''
                    to = '"{0} = " + {0} +'.format(name)

                params.append('\t\tpublic {0} {1}{2};'.format(type_, name, new))
                ctors.append('{0} {1}'.format(type_, name))
                assignments.append('\t\t\tthis.{0} = {0};'.format(name))
                tostr.append(to)

            if high_level:
                template2 = template_high_level
            else:
                template2 = template

            return template2.format(packet.get_java_object_name(high_level),
                                    '\n'.join(params),
                                    ' ", " + '.join(tostr),
                                    ', '.join(ctors),
                                    '\n'.join(assignments))

        # normal and low-level
        for packet in self.get_packets('function'):
            if packet.has_prototype_in_device():
                continue

            if len(packet.get_elements(direction='out')) < 2:
                continue

            objects += make_return_object(packet, False)

        for packet in self.get_packets('function'):
            if packet.has_prototype_in_device() or not packet.has_high_level():
                continue

            if len(packet.get_elements(direction='out', high_level=True)) < 2:
                continue

            objects += make_return_object(packet, True)

        return objects

    def get_java_listener_definitions(self):
        listeners = ''
        template = """
	/**
	 * {3}
	 */
	public interface {0}Listener extends DeviceListener {{
		public void {1}({2});
	}}
"""

        # normal and low-level
        for packet in self.get_packets('callback'):
            name_camel = packet.get_name().camel
            name_headless = packet.get_name().headless

            if self.get_generator().is_matlab() or self.get_generator().is_octave():
                parameter = name_camel + 'CallbackData data'
            else:
                parameter = packet.get_java_parameters()

            if packet.has_high_level():
                doc = '@see {}Listener'.format(packet.get_name(skip=-2).camel)
            else:
                doc = packet.get_java_formatted_doc()

            listeners += template.format(name_camel, name_headless, parameter, doc)

        # high-level
        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                name_camel = packet.get_name(skip=-2).camel
                name_headless = packet.get_name(skip=-2).headless

                if self.get_generator().is_matlab() or self.get_generator().is_octave():
                    parameter = name_camel + 'CallbackData data'
                else:
                    parameter = packet.get_java_parameters(high_level=True)

                doc = packet.get_java_formatted_doc()
                listeners += template.format(name_camel, name_headless, parameter, doc)

        if self.get_long_display_name() == 'RS232 Bricklet':
            if self.get_generator().is_matlab() or self.get_generator().is_octave():
                read_parameter = 'ReadCallbackData data'
                error_parameter = 'ErrorCallbackData data'
            else:
                read_parameter = 'char[] message, short length'
                error_parameter = 'short error'

            listeners += """
	/**
	 * This listener is called if new data is available. The message has
	 * a maximum size of 60 characters. The actual length of the message
	 * is given in addition.
	 *
	 * To enable this listener, use {{@link BrickletRS232#enableReadCallback()}}.
	 */
	public interface ReadCallbackListener extends DeviceListener {{ // for backward compatibility
		public void readCallback({0});
	}}

	/**
	 * This listener is called if an error occurs.
	 * Possible errors are overrun, parity or framing error.
	 *
	 * .. versionadded:: 2.0.1$nbsp;(Plugin)
	 */
	public interface ErrorCallbackListener extends DeviceListener {{ // for backward compatibility
		public void errorCallback({1});
	}}
""".format(read_parameter, error_parameter)

        return listeners

    def get_java_response_expected(self):
        result = []
        template = '\t\tresponseExpected[IPConnection.unsignedByte(FUNCTION_{name})] = RESPONSE_EXPECTED_FLAG_{flag};\n'

        for packet in self.get_packets('function'):
            result.append(template.format(name=packet.get_name().upper,
                                          flag=packet.get_response_expected().upper()))

        return ''.join(result)

    def get_java_callback_listener_definitions(self):
        listeners = ''
        template = """{6}
		callbacks[CALLBACK_{0}] = new IPConnection.DeviceCallbackListener() {{
			public void callback({3}byte[] packet) {{{1}{7}
				for ({4} listener: listener{2}) {{
					{5}
				}}
			}}
		}};
"""
        data = """
				ByteBuffer bb = ByteBuffer.wrap(packet, 8, packet.length - 8);
				bb.order(ByteOrder.LITTLE_ENDIAN);

{1}"""
        template_stream_out = """
				IPConnection.DeviceHighLevelCallback highLevelCallback = highLevelCallbacks[-CALLBACK_{name_upper}];
				{stream_length_type} {stream_name_headless}ChunkLength = Math.min({stream_length} - {stream_name_headless}ChunkOffset, {chunk_cardinality});

				if (highLevelCallback.data == null) {{ // no stream in-progress
					if ({stream_name_headless}ChunkOffset == 0) {{ // stream starts
						highLevelCallback.data = {stream_data_new};
						highLevelCallback.length = {stream_name_headless}ChunkLength;

						System.arraycopy({stream_name_headless}ChunkData, 0, ({chunk_data_type})highLevelCallback.data, 0, {stream_name_headless}ChunkLength);

						if (highLevelCallback.length >= {stream_length}) {{ // stream complete
							for ({high_level_listener_type} listener: listener{name_camel}) {{
								{high_level_listener_call}
							}}

							highLevelCallback.data = null;
							highLevelCallback.length = 0;
						}}
					}} else {{ // ignore tail of current stream, wait for next stream start
					}}
				}} else {{ // stream in-progress
					if ({stream_name_headless}ChunkOffset != highLevelCallback.length) {{ // stream out-of-sync
						highLevelCallback.data = null;
						highLevelCallback.length = 0;

						for ({high_level_listener_type} listener: listener{name_camel}) {{
							{high_level_listener_call}
						}}
					}} else {{ // stream in-sync
						System.arraycopy({stream_name_headless}ChunkData, 0, ({chunk_data_type})highLevelCallback.data, highLevelCallback.length, {stream_name_headless}ChunkLength);
						highLevelCallback.length += {stream_name_headless}ChunkLength;

						if (highLevelCallback.length >= {stream_length}) {{ // stream complete
							for ({high_level_listener_type} listener: listener{name_camel}) {{
								{high_level_listener_call}
							}}

							highLevelCallback.data = null;
							highLevelCallback.length = 0;
						}}
					}}
				}}
"""
        template_stream_out_single_chunk = """
				{chunk_data_type} {stream_name_headless} = {stream_data_new};

				System.arraycopy({stream_name_headless}Data, 0, {stream_name_headless}, 0, {stream_name_headless}Length);

				for ({high_level_listener_type} listener: listener{name_camel}) {{
					{high_level_listener_call}
				}}
"""

        for packet in self.get_packets('callback'):
            type_ = packet.get_name().upper
            name_camel = packet.get_name().camel
            name_headless = packet.get_name().headless
            parameters = packet.get_java_parameters(context='call')
            cbdata = ''

            if len(packet.get_elements(direction='out')) > 0:
                bbgets, bbret = packet.get_java_bbgets()
                bbgets = bbgets.replace('\t\t', '\t\t\t\t')
                cbdata = data.format(name_headless,
                                     bbgets,
                                     bbret)

            if self.get_generator().is_matlab():
                device_param = 'Device device, '
                listener_type = name_camel + 'Listener'
                listener_call = 'listener.{0}(new {1}CallbackData(device{2}));'.format(name_headless, name_camel, common.wrap_non_empty(', ', parameters, ''))
            elif self.get_generator().is_octave():
                device_param = 'Device device, '
                listener_type = 'OctaveReference'
                listener_call = 'IPConnection.doOctaveInvoke(listener, new Object[]{{new {0}CallbackData(device{1})}});'.format(name_camel, common.wrap_non_empty(', ', parameters, ''))
            else:
                device_param = ''
                listener_type = name_camel + 'Listener'
                listener_call = 'listener.{0}({2});'.format(name_headless, name_camel, parameters)

            stream_out = packet.get_high_level('stream_out')

            if stream_out != None:
                if stream_out.has_single_chunk():
                    template2 = template_stream_out_single_chunk
                    context = 'call'
                else:
                    template2 = template_stream_out
                    context = 'listener'

                length_element = stream_out.get_length_element()
                chunk_offset_element = stream_out.get_chunk_offset_element()

                if length_element != None:
                    stream_length_type = length_element.get_java_type()
                elif chunk_offset_element != None:
                    stream_length_type = chunk_offset_element.get_java_type()

                high_level_parameters = packet.get_java_parameters(context=context, high_level=True)

                if self.get_generator().is_matlab():
                    high_level_listener_type = packet.get_name(skip=-2).camel + 'Listener'
                    high_level_listener_call = 'listener.{0}(new {1}CallbackData(device{2}));'.format(packet.get_name(skip=-2).headless,
                                                                                                      packet.get_name(skip=-2).camel,
                                                                                                      common.wrap_non_empty(', ', high_level_parameters, ''))
                elif self.get_generator().is_octave():
                    high_level_listener_type = 'OctaveReference'
                    high_level_listener_call = 'IPConnection.doOctaveInvoke(listener, new Object[]{{new {0}CallbackData(device{1})}});'.format(packet.get_name(skip=-2).camel,
                                                                                                                                               common.wrap_non_empty(', ', high_level_parameters, ''))
                else:
                    high_level_listener_type = packet.get_name(skip=-2).camel + 'Listener'
                    high_level_listener_call = 'listener.{0}({1});'.format(packet.get_name(skip=-2).headless, high_level_parameters)

                high_level_callback = '\n\t\thighLevelCallbacks[-CALLBACK_{0}] = new IPConnection.DeviceHighLevelCallback();'.format(packet.get_name(skip=-2).upper)
                high_level_handling = template2.format(name_camel=packet.get_name(skip=-2).camel,
                                                       name_upper=packet.get_name(skip=-2).upper,
                                                       high_level_listener_type=high_level_listener_type,
                                                       high_level_listener_call=high_level_listener_call,
                                                       stream_name_headless=stream_out.get_name().headless,
                                                       stream_length=stream_out.get_fixed_length(default='{0}Length'.format(stream_out.get_name().headless)),
                                                       stream_length_type=stream_length_type,
                                                       stream_data_new=stream_out.get_chunk_data_element().get_java_new(cardinality=stream_out.get_fixed_length(default='{0}Length'.format(stream_out.get_name().headless))),
                                                       chunk_data_type=stream_out.get_chunk_data_element().get_java_type(),
                                                       chunk_cardinality=stream_out.get_chunk_data_element().get_cardinality())
            else:
                high_level_callback = ''
                high_level_handling = ''

            listeners += template.format(type_, cbdata, name_camel, device_param, listener_type, listener_call, high_level_callback, high_level_handling)

        return listeners + '\t}\n'

    def get_java_add_listener(self):
        listeners = ''
        template = """
	/**
	 * Adds a {0} listener.
	 */
	public void add{0}{2}({1} listener) {{
		listener{0}.add(listener);
	}}

	/**
	 * Removes a {0} listener.
	 */
	public void remove{0}{2}({1} listener) {{
		listener{0}.remove(listener);
	}}
"""

        # normal and low-level
        for packet in self.get_packets('callback'):
            name = packet.get_name().camel

            if self.get_generator().is_octave():
                listener_type = 'OctaveReference'
                suffix = 'Callback'
            else:
                listener_type = name + 'Listener'
                suffix = 'Listener'

            listeners += template.format(name, listener_type, suffix)

        # high-level
        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                name = packet.get_name(skip=-2).camel

                if self.get_generator().is_octave():
                    listener_type = 'OctaveReference'
                    suffix = 'Callback'
                else:
                    listener_type = name + 'Listener'
                    suffix = 'Listener'

                listeners += template.format(name, listener_type, suffix)

        if self.get_long_display_name() == 'RS232 Bricklet':
            if self.get_generator().is_octave():
                listeners += """
	/**
	 * Adds a ReadCallback listener.
	 */
	public void addReadCallbackCallback(OctaveReference listener) { // for backward compatibility
		listenerRead.add(listener);
	}

	/**
	 * Removes a ReadCallback listener.
	 */
	public void removeReadCallbackCallback(OctaveReference listener) { // for backward compatibility
		listenerRead.remove(listener);
	}

	/**
	 * Adds a ErrorCallback listener.
	 */
	public void addErrorCallbackCallback(OctaveReference listener) { // for backward compatibility
		listenerError.add(listener);
	}

	/**
	 * Removes a ErrorCallback listener.
	 */
	public void removeErrorCallbackCallback(OctaveReference listener) { // for backward compatibility
		listenerError.remove(listener);
	}
"""
            else:
                if self.get_generator().is_matlab():
                    read_parameters = 'ReadCallbackData data'
                    read_forward = 'listener.readCallback(data);'
                    error_parameters = 'ErrorCallbackData data'
                    error_forward = 'listener.errorCallback(data);'
                else:
                    read_parameters = 'char[] message, short length'
                    read_forward = 'listener.readCallback(message, length);'
                    error_parameters = 'short error'
                    error_forward = 'listener.errorCallback(error);'

                listeners += """
	private class ReadListenerForwarder implements ReadListener {{
		public ReadCallbackListener listener;

		public ReadListenerForwarder(ReadCallbackListener listener) {{
			this.listener = listener;
		}}

		public void read({0}) {{
			{1}
		}}
	}}

	private List<ReadListenerForwarder> readListenerForwarders = new ArrayList<ReadListenerForwarder>();

	/**
	 * Adds a ReadCallback listener.
	 */
	public void addReadCallbackListener(ReadCallbackListener listener) {{ // for backward compatibility
		synchronized (readListenerForwarders) {{
			ReadListenerForwarder forwarder = new ReadListenerForwarder(listener);

			readListenerForwarders.add(forwarder);
			listenerRead.add(forwarder);
		}}
	}}

	/**
	 * Removes a ReadCallback listener.
	 */
	public void removeReadCallbackListener(ReadCallbackListener listener) {{ // for backward compatibility
		synchronized (readListenerForwarders) {{
			for (ReadListenerForwarder forwarder: readListenerForwarders) {{
				if (forwarder.listener.equals(listener)) {{
					readListenerForwarders.remove(forwarder);
					listenerRead.remove(forwarder);

					break;
				}}
			}}
		}}
	}}

	private class ErrorListenerForwarder implements ErrorListener {{
		public ErrorCallbackListener listener;

		public ErrorListenerForwarder(ErrorCallbackListener listener) {{
			this.listener = listener;
		}}

		public void error({2}) {{
			{3}
		}}
	}}

	private List<ErrorListenerForwarder> errorListenerForwarders = new ArrayList<ErrorListenerForwarder>();

	/**
	 * Adds a ErrorCallback listener.
	 */
	public void addErrorCallbackListener(ErrorCallbackListener listener) {{ // for backward compatibility
		synchronized (errorListenerForwarders) {{
			ErrorListenerForwarder forwarder = new ErrorListenerForwarder(listener);

			errorListenerForwarders.add(forwarder);
			listenerError.add(forwarder);
		}}
	}}

	/**
	 * Removes a ErrorCallback listener.
	 */
	public void removeErrorCallbackListener(ErrorCallbackListener listener) {{ // for backward compatibility
		synchronized (errorListenerForwarders) {{
			for (ErrorListenerForwarder forwarder: errorListenerForwarders) {{
				if (forwarder.listener.equals(listener)) {{
					errorListenerForwarders.remove(forwarder);
					listenerError.remove(forwarder);

					break;
				}}
			}}
		}}
	}}
""".format(read_parameters, read_forward, error_parameters, error_forward)

        return listeners

    def get_java_function_id_definitions(self):
        function_ids = ''
        template_function = '\tpublic final static byte FUNCTION_{0} = (byte){1};\n'
        template_callback = '\tprivate final static int CALLBACK_{0} = {1};\n'

        for packet in self.get_packets('function'):
            function_ids += template_function.format(packet.get_name().upper,
                                                     packet.get_function_id())

        for packet in self.get_packets('callback'):
            function_ids += template_callback.format(packet.get_name().upper,
                                                     packet.get_function_id())

        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                function_ids += template_callback.format(packet.get_name(skip=-2).upper,
                                                         -packet.get_function_id())

        return function_ids

    def get_java_constants(self):
        template = '\tpublic final static {0} {1}_{2} = {3}{4};\n'
        constants = []

        for constant_group in self.get_constant_groups():
            if constant_group.is_virtual():
                continue

            type_ = java_common.get_java_type(constant_group.get_type(), 1, legacy=self.has_java_legacy_types(), octave=self.get_generator().is_octave())

            for constant in constant_group.get_constants():
                if constant_group.get_type() == 'char':
                    cast = ''

                    if self.get_generator().is_octave():
                        value = "new String(new char[]{{'{0}'}})".format(constant.get_value())
                        type_ = 'String'
                    else:
                        value = "'{0}'".format(constant.get_value())
                elif constant_group.get_type() == 'bool':
                    value = str(constant.get_value()).lower()
                else:
                    if type_ == 'int':
                        cast = '' # no need to cast int, its the default type for number literals
                    else:
                        cast = '({0})'.format(type_)

                    value = str(constant.get_value())

                    if type_ == 'long':
                        cast = ''
                        value += 'L' # mark longs as such, because int is the default type for number literals

                constants.append(template.format(type_,
                                                 constant_group.get_name().upper,
                                                 constant.get_name().upper,
                                                 cast,
                                                 value))

        return '\n' + ''.join(constants)

    def get_java_listener_lists(self):
        listeners = '\n'
        template = '\tprivate List<{0}Listener> listener{0} = new CopyOnWriteArrayList<{0}Listener>();\n'

        # normal and low-level
        for packet in self.get_packets('callback'):
            listeners += template.format(packet.get_name().camel)

        # high-level
        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                listeners += template.format(packet.get_name(skip=-2).camel)

        return listeners

    def get_octave_listener_lists(self):
        listeners = '\n'
        template = '\tprivate List<OctaveReference> listener{0} = new CopyOnWriteArrayList<OctaveReference>();\n'

        # normal and low-level
        for packet in self.get_packets('callback'):
            listeners += template.format(packet.get_name().camel)

        # high-level
        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                listeners += template.format(packet.get_name(skip=-2).camel)

        return listeners

    def get_java_constructor(self):
        template = """
	/**
	 * Creates an object with the unique device ID \\c uid. and adds it to
	 * the IP Connection \\c ipcon.
	 */
	public {0}(String uid, IPConnection ipcon) {{
		super(uid, ipcon);

		apiVersion[0] = {1};
		apiVersion[1] = {2};
		apiVersion[2] = {3};
"""

        return template.format(self.get_java_class_name(), *self.get_api_version())

    def get_java_methods(self):
        methods = ''

        # normal and low-level
        template = """
	/**
	 * {8}
	 */
	public {0} {1}({2}) {3} {{
		ByteBuffer bb = ipcon.createRequestPacket((byte){4}, FUNCTION_{5}, this);

{6}
{7}
	}}
"""
        template_response = """		byte[] response = sendRequest(bb.array());

		bb = ByteBuffer.wrap(response, 8, response.length - 8);
		bb.order(ByteOrder.LITTLE_ENDIAN);

{1}
		return {2};"""
        template_noresponse = '\t\tsendRequest(bb.array());'
        plain_loop = """		for (int i = 0; i < {0}; i++) {{
	{1}
		}}"""
        string_loop = """		for (int i = 0; i < {0}; i++) {{
			try {{
		{1}
			}} catch(Exception e) {{
				bb.put((byte)0);
			}}
		}}"""

        bool_loop_sub1 = """		for (int i = 0; i < {0}; i++) {{
			if ({1}[i]) {{
				{2}[i / 8] |= 1 << (i % 8);
			}}
		}}"""

        bool_loop_sub2 = """		for (int i = 0; i < {0}; i++) {{
			bb.put({1}[i]);
		}}"""

        bool_loop = """\n		byte[] {0} = new byte[{1}];
		Arrays.fill({0}, (byte)0);

{2}
{3}"""

        for packet in self.get_packets('function'):
            ret = packet.get_java_return_type()
            name_headless = packet.get_name().headless
            name_upper = packet.get_name().upper
            parameter = packet.get_java_parameters()
            size = str(packet.get_request_size())
            doc = packet.get_java_formatted_doc()
            bbputs = ''
            bbput = '\t\tbb.put{0}({1}{2});'
            bbput_bool_array = ''

            for element in packet.get_elements(direction='in'):
                name = element.get_name().headless
                storage_type = element.get_java_byte_buffer_storage_type()
                put_suffix = element.get_java_byte_buffer_method_suffix()

                if storage_type != element.get_java_type():
                    cast = '({0})'.format(storage_type.replace('[]', ''))
                else:
                    cast = ''

                if element.get_cardinality() > 1:
                    if element.get_type() == 'string':
                        bbput_format = string_loop.format(element.get_cardinality(),
                                                          bbput.format(put_suffix, cast, name + '.charAt(i)'))

                    elif self.get_generator().is_octave() and element.get_type() == 'char':
                        bbput_format = plain_loop.format(element.get_cardinality(),
                                                         bbput.format(put_suffix, cast, name + '[i].charAt(0)'))
                    elif element.get_type() == 'bool':
                        bbput_format = bool_loop.format(name + 'Bits',
                                                        int(math.ceil(element.get_cardinality() / 8.0)),
                                                        bool_loop_sub1.format(element.get_cardinality(),
                                                                              name,
                                                                              name + 'Bits'),
                                                        bool_loop_sub2.format(int(math.ceil(element.get_cardinality() / 8.0)),
                                                                              name + 'Bits'))
                    else:
                        bbput_format = plain_loop.format(element.get_cardinality(),
                                                         bbput.format(put_suffix, cast, name + '[i]'))
                elif self.get_generator().is_octave() and element.get_type() == 'char':
                    bbput_format = bbput.format(put_suffix, cast, name + '.charAt(0)')
                elif element.get_type() == 'bool':
                    bbput_format = bbput.format(put_suffix, cast, '({0} ? 1 : 0)'.format(name))
                else:
                    bbput_format = bbput.format(put_suffix, cast, name)

                bbputs += bbput_format + '\n'

            throws = 'throws TinkerforgeException'

            if len(packet.get_elements(direction='out')) == 0:
                bbgets = ''
                bbret = ''
            elif len(packet.get_elements(direction='out')) > 1:
                bbgets, bbret = packet.get_java_bbgets(True)
                obj_name = packet.get_java_object_name()
                obj = '\t\t{0} obj = new {0}();\n'.format(obj_name)
                bbgets = obj + bbgets
                bbret = 'obj'
            else:
                bbgets, bbret = packet.get_java_bbgets(False)

            if len(packet.get_elements(direction='out')) == 0:
                response = template_noresponse.format(name_upper)
            else:
                response = template_response.format(name_upper,
                                                    bbgets,
                                                    bbret)

            methods += template.format(ret,
                                       name_headless,
                                       parameter,
                                       throws,
                                       size,
                                       name_upper,
                                       bbputs,
                                       response,
                                       doc)

        # high-level
        template_stream_in = """
	/**
	 * {doc}
	 */
	public {return_type} {name_headless}({high_level_parameters}) throws TinkerforgeException {{
		if ({stream_name_headless}.length > {stream_max_length}) {{
			throw new IllegalArgumentException("{stream_name_space} can be at most {stream_max_length} items long");
		}}
{result_variable}
		{stream_length_type} {stream_name_headless}Length = {stream_name_headless}.length;
		{stream_length_type} {stream_name_headless}ChunkOffset = 0;
		{chunk_data_type} {stream_name_headless}ChunkData = {chunk_data_new};
		{stream_length_type} {stream_name_headless}ChunkLength;

		if ({stream_name_headless}Length == 0) {{
			Arrays.fill({stream_name_headless}ChunkData, {chunk_padding});

			{result_assignment}{name_headless}LowLevel({parameters});
		}} else {{
			synchronized (streamMutex) {{
				while ({stream_name_headless}ChunkOffset < {stream_name_headless}Length) {{
					{stream_name_headless}ChunkLength = Math.min({stream_name_headless}Length - {stream_name_headless}ChunkOffset, {chunk_cardinality});

					System.arraycopy({stream_name_headless}, {stream_name_headless}ChunkOffset, {stream_name_headless}ChunkData, 0, {stream_name_headless}ChunkLength);
					Arrays.fill({stream_name_headless}ChunkData, {stream_name_headless}ChunkLength, {chunk_cardinality}, {chunk_padding});

					{result_assignment}{name_headless}LowLevel({parameters});
					{stream_name_headless}ChunkOffset += {chunk_cardinality};
				}}
			}}
		}}{result_return}
	}}
"""
        template_stream_in_fixed_length = """
	/**
	 * {doc}
	 */
	public {return_type} {name_headless}({high_level_parameters}) throws TinkerforgeException {{{result_variable}
		{stream_length_type} {stream_name_headless}Length = {fixed_length};
		{stream_length_type} {stream_name_headless}ChunkOffset = 0;
		{chunk_data_type} {stream_name_headless}ChunkData = {chunk_data_new};
		{stream_length_type} {stream_name_headless}ChunkLength;

		if ({stream_name_headless}.length != {stream_name_headless}Length) {{
			throw new IllegalArgumentException("{stream_name_space} has to be exactly " + {stream_name_headless}Length + " items long");
		}}

		synchronized (streamMutex) {{
			while ({stream_name_headless}ChunkOffset < {stream_name_headless}Length) {{
				{stream_name_headless}ChunkLength = Math.min({stream_name_headless}Length - {stream_name_headless}ChunkOffset, {chunk_cardinality});

				System.arraycopy({stream_name_headless}, {stream_name_headless}ChunkOffset, {stream_name_headless}ChunkData, 0, {stream_name_headless}ChunkLength);
				Arrays.fill({stream_name_headless}ChunkData, {stream_name_headless}ChunkLength, {chunk_cardinality}, {chunk_padding});

				{result_assignment}{name_headless}LowLevel({parameters});
				{stream_name_headless}ChunkOffset += {chunk_cardinality};
			}}
		}}{result_return}
	}}
"""
        template_stream_in_namedtuple_result = """

		return new {result_name_camel}({result_fields});"""
        template_stream_in_short_write = """
	/**
	 * {doc}
	 */
	public {return_type} {name_headless}({high_level_parameters}) throws TinkerforgeException {{
		if ({stream_name_headless}.length > {stream_max_length}) {{
			throw new IllegalArgumentException("{stream_name_space} can be at most {stream_max_length} items long");
		}}
{result_variable}
		{stream_length_type} {stream_name_headless}Length = {stream_name_headless}.length;
		{stream_length_type} {stream_name_headless}ChunkOffset = 0;
		{chunk_data_type} {stream_name_headless}ChunkData = {chunk_data_new};
		{stream_length_type} {stream_name_headless}ChunkLength;
		{stream_length_type} {stream_name_headless}Written;

		if ({stream_name_headless}Length == 0) {{
			Arrays.fill({stream_name_headless}ChunkData, {chunk_padding});

			ret = {name_headless}LowLevel({parameters});
			{chunk_written_0}
		}} else {{
			{stream_name_headless}Written = 0;

			synchronized (streamMutex) {{
				while ({stream_name_headless}ChunkOffset < {stream_name_headless}Length) {{
					{stream_name_headless}ChunkLength = Math.min({stream_name_headless}Length - {stream_name_headless}ChunkOffset, {chunk_cardinality});

					System.arraycopy({stream_name_headless}, {stream_name_headless}ChunkOffset, {stream_name_headless}ChunkData, 0, {stream_name_headless}ChunkLength);
					Arrays.fill({stream_name_headless}ChunkData, {stream_name_headless}ChunkLength, {chunk_cardinality}, {chunk_padding});

					ret = {name_headless}LowLevel({parameters});
					{chunk_written_n}

					if ({chunk_written_test} < {chunk_cardinality}) {{
						break; // either last chunk or short write
					}}

					{stream_name_headless}ChunkOffset += {chunk_cardinality};
				}}
			}}
		}}{result_return}
	}}
"""
        template_stream_in_short_write_chunk_written = ['{stream_name_headless}Written = ret;',
                                                        '{stream_name_headless}Written += ret;',
                                                        'ret']
        template_stream_in_short_write_namedtuple_chunk_written = ['{stream_name_headless}Written = ret.{stream_name_headless}ChunkWritten;',
                                                                   '{stream_name_headless}Written += ret.{stream_name_headless}ChunkWritten;',
                                                                   'ret.{stream_name_headless}ChunkWritten']
        template_stream_in_single_chunk = """
	/**
	 * {doc}
	 */
	public {return_type} {name_headless}({high_level_parameters}) throws TinkerforgeException {{
		if ({stream_name_headless}.length > {chunk_cardinality}) {{
			throw new IllegalArgumentException("{stream_name_space} can be at most {chunk_cardinality} items long");
		}}

		{stream_length_type} {stream_name_headless}Length = {stream_name_headless}.length;
		{chunk_data_type} {stream_name_headless}Data = {chunk_data_new};{result_variable}

		System.arraycopy({stream_name_headless}, 0, {stream_name_headless}Data, 0, {stream_name_headless}Length);
		Arrays.fill({stream_name_headless}Data, {stream_name_headless}Length, {chunk_cardinality}, {chunk_padding});

		{result_assignment}{name_headless}LowLevel({parameters});{result_return}
	}}
"""
        template_stream_out = """
	/**
	 * {doc}
	 */
	public {return_type} {name_headless}({high_level_parameters}) throws TinkerforgeException {{
		{result_type} ret;
		{chunk_data_type} {stream_name_headless} = null; // stop the compiler from wrongly complaining that this variable is used unassigned
		{stream_length_type} {stream_name_headless}Length{fixed_length};
		{stream_length_type} {stream_name_headless}ChunkOffset;
		{stream_length_type} {stream_name_headless}ChunkLength;
		boolean {stream_name_headless}OutOfSync;
		{stream_length_type} {stream_name_headless}CurrentLength;

		synchronized (streamMutex) {{
			ret = {name_headless}LowLevel({parameters});{dynamic_length_3}{chunk_offset_check}
			{chunk_offset_check_indent}{stream_name_headless}ChunkOffset = ret.{stream_name_headless}ChunkOffset;
			{chunk_offset_check_indent}{stream_name_headless}OutOfSync = {stream_name_headless}ChunkOffset != 0;{chunk_offset_check_end}

			if (!{stream_name_headless}OutOfSync) {{
				{stream_name_headless} = {stream_data_new};
				{stream_name_headless}ChunkLength = Math.min({stream_name_headless}Length - {stream_name_headless}ChunkOffset, {chunk_cardinality});

				System.arraycopy(ret.{stream_name_headless}ChunkData, 0, {stream_name_headless}, 0, {stream_name_headless}ChunkLength);

				{stream_name_headless}CurrentLength = {stream_name_headless}ChunkLength;

				while ({stream_name_headless}CurrentLength < {stream_name_headless}Length) {{
					ret = {name_headless}LowLevel({parameters});{dynamic_length_5}
					{stream_name_headless}OutOfSync = ret.{stream_name_headless}ChunkOffset != {stream_name_headless}CurrentLength;

					if ({stream_name_headless}OutOfSync) {{
						break;
					}}

					{stream_name_headless}ChunkLength = Math.min({stream_name_headless}Length - ret.{stream_name_headless}ChunkOffset, {chunk_cardinality});

					System.arraycopy(ret.{stream_name_headless}ChunkData, 0, {stream_name_headless}, {stream_name_headless}CurrentLength, {stream_name_headless}ChunkLength);

					{stream_name_headless}CurrentLength += {stream_name_headless}ChunkLength;
				}}
			}}

			if ({stream_name_headless}OutOfSync) {{ // discard remaining stream to bring it back in-sync
				while (ret.{stream_name_headless}ChunkOffset + {chunk_cardinality} < {stream_name_headless}Length) {{
					ret = {name_headless}LowLevel({parameters});{dynamic_length_5}
				}}

				throw new StreamOutOfSyncException("{stream_name_space} stream is out-of-sync");
			}}
		}}
{result_return}
	}}
"""
        template_stream_out_dynamic_length = """
{{indent}}{stream_name_headless}Length = ret.{stream_name_headless}Length;"""
        template_stream_out_chunk_offset_check = """

			if (ret.{stream_name_headless}ChunkOffset == (1 << {shift_size}) - 1) {{ // maximum chunk offset -> stream has no data
				{stream_name_headless}Length = 0;
				{stream_name_headless}ChunkOffset = 0;
				{stream_name_headless}OutOfSync = false;
			}} else {{"""
        template_stream_out_single_chunk = """
	/**
	 * {doc}
	 */
	public {return_type} {name_headless}({high_level_parameters}) throws TinkerforgeException {{
		{result_type} ret = {name_headless}LowLevel({parameters});
		{chunk_data_type} {stream_name_headless} = {stream_data_new};

		System.arraycopy(ret.{stream_name_headless}Data, 0, {stream_name_headless}, 0, ret.{stream_name_headless}Length);
{result_return}
	}}
"""
        template_stream_out_result = """
		return {stream_name_headless};"""
        template_stream_out_namedtuple_result = """
		return new {result_name_camel}({result_fields});"""

        for packet in self.get_packets('function'):
            stream_in = packet.get_high_level('stream_in')
            stream_out = packet.get_high_level('stream_out')

            if stream_in != None:
                length_element = stream_in.get_length_element()
                chunk_offset_element = stream_in.get_chunk_offset_element()

                if length_element != None:
                    stream_length_type = length_element.get_java_type()
                elif chunk_offset_element != None:
                    stream_length_type = chunk_offset_element.get_java_type()

                if stream_in.get_fixed_length() != None:
                    template = template_stream_in_fixed_length
                elif stream_in.has_short_write() and stream_in.has_single_chunk():
                    # the single chunk template also covers short writes
                    template = template_stream_in_single_chunk
                elif stream_in.has_short_write():
                    template = template_stream_in_short_write
                elif stream_in.has_single_chunk():
                    template = template_stream_in_single_chunk
                else:
                    template = template_stream_in

                return_elements = packet.get_elements(direction='out', high_level=True)

                if len(return_elements) > 0:
                    if len(return_elements) > 1:
                        return_type = packet.get_java_object_name(high_level=True)
                        result_type = packet.get_java_object_name()
                        result_default = 'null'
                    else:
                        return_type = return_elements[0].get_java_type()
                        result_type = return_elements[0].get_java_type()
                        result_default = return_elements[0].get_java_default_value()

                    result_assignment = 'ret = '

                    if len(return_elements) > 1:
                        fields = []

                        for element in return_elements:
                            if element.get_role() == 'stream_written':
                                if stream_in.has_single_chunk():
                                    fields.append('ret.{0}Written'.format(stream_in.get_name().headless))
                                else:
                                    fields.append('{0}Written'.format(stream_in.get_name().headless))
                            else:
                                fields.append('ret.{0}'.format(element.get_name().headless))

                        if stream_in.has_single_chunk():
                            result_variable = '\n\t\t{0} ret;'.format(result_type)
                        else:
                            result_variable = '\n\t\t{0} ret = {1}; // stop the compiler from wrongly complaining that this variable is used unassigned YYY1'.format(result_type, result_default)

                        result_return = template_stream_in_namedtuple_result.format(result_name_camel=packet.get_java_object_name(high_level=True),
                                                                                    result_fields=', '.join(fields))
                    elif not stream_in.has_single_chunk() and return_elements[0].get_role() == 'stream_written':
                        result_variable = '\n\t\t{0} ret;'.format(result_type)
                        result_return = '\n\n\t\treturn {0}Written;'.format(stream_in.get_name().headless)
                    else:
                        if stream_in.has_single_chunk():
                            result_variable = '\n\t\t{0} ret;'.format(result_type)
                        else:
                            result_variable = '\n\t\t{0} ret = {1}; // stop the compiler from wrongly complaining that this variable is used unassigned YYY2'.format(result_type, result_default)

                        result_return = '\n\n\t\treturn ret;'
                else:
                    return_type = 'void'
                    result_variable = ''
                    result_assignment = ''
                    result_return = ''

                if stream_in.has_short_write():
                    if len(packet.get_elements(direction='out')) < 2:
                        chunk_written_0 = template_stream_in_short_write_chunk_written[0].format(stream_name_headless=stream_in.get_name().headless)
                        chunk_written_n = template_stream_in_short_write_chunk_written[1].format(stream_name_headless=stream_in.get_name().headless)
                        chunk_written_test = template_stream_in_short_write_chunk_written[2].format(stream_name_headless=stream_in.get_name().headless)
                    else:
                        chunk_written_0 = template_stream_in_short_write_namedtuple_chunk_written[0].format(stream_name_headless=stream_in.get_name().headless)
                        chunk_written_n = template_stream_in_short_write_namedtuple_chunk_written[1].format(stream_name_headless=stream_in.get_name().headless)
                        chunk_written_test = template_stream_in_short_write_namedtuple_chunk_written[2].format(stream_name_headless=stream_in.get_name().headless)
                else:
                    chunk_written_0 = ''
                    chunk_written_n = ''
                    chunk_written_test = ''

                methods += template.format(doc=packet.get_java_formatted_doc(),
                                           name_headless=packet.get_name(skip=-2).headless,
                                           parameters=packet.get_java_parameters(context='call'),
                                           high_level_parameters=packet.get_java_parameters(high_level=True),
                                           return_type=return_type,
                                           result_variable=result_variable,
                                           result_assignment=result_assignment,
                                           result_return=result_return,
                                           stream_name_space=stream_in.get_name().space,
                                           stream_name_headless=stream_in.get_name().headless,
                                           stream_length_type=stream_length_type,
                                           stream_max_length=abs(stream_in.get_data_element().get_cardinality()),
                                           fixed_length=stream_in.get_fixed_length(),
                                           chunk_data_type=stream_in.get_chunk_data_element().get_java_type(),
                                           chunk_data_new=stream_in.get_chunk_data_element().get_java_new(),
                                           chunk_cardinality=stream_in.get_chunk_data_element().get_cardinality(),
                                           chunk_padding=stream_in.get_chunk_data_element().get_java_default_item_value(),
                                           chunk_written_0=chunk_written_0,
                                           chunk_written_n=chunk_written_n,
                                           chunk_written_test=chunk_written_test)
            elif stream_out != None:
                length_element = stream_out.get_length_element()
                chunk_offset_element = stream_out.get_chunk_offset_element()

                if length_element != None:
                    stream_length_type = length_element.get_java_type()
                elif chunk_offset_element != None:
                    stream_length_type = chunk_offset_element.get_java_type()

                if stream_out.get_fixed_length() != None:
                    shift_size = int(stream_out.get_chunk_offset_element().get_type().replace('uint', ''))
                    chunk_offset_check = template_stream_out_chunk_offset_check.format(stream_name_headless=stream_out.get_name().headless,
                                                                                       shift_size=shift_size)
                    chunk_offset_check_indent = '\t'
                    chunk_offset_check_end = '\n\t\t\t}'
                else:
                    chunk_offset_check = ''
                    chunk_offset_check_indent = ''
                    chunk_offset_check_end = ''

                return_elements = packet.get_elements(direction='out', high_level=True)

                if len(return_elements) > 0:
                    if len(return_elements) > 1:
                        return_type = packet.get_java_object_name(high_level=True)
                        fields = []

                        for element in packet.get_elements(direction='out', high_level=True):
                            if element.get_role() == 'stream_data':
                                fields.append(stream_out.get_name().headless)
                            else:
                                fields.append('ret.{0}'.format(element.get_name().headless))

                        result_return = template_stream_out_namedtuple_result.format(result_name_camel=packet.get_java_object_name(high_level=True),
                                                                                     result_fields=', '.join(fields))
                    else:
                        return_type = return_elements[0].get_java_type()
                        result_return = template_stream_out_result.format(stream_name_headless=stream_out.get_name().headless)
                else:
                    return_type = 'void'
                    result_return = ''

                if stream_out.get_fixed_length() == None:
                    dynamic_length = template_stream_out_dynamic_length.format(stream_name_headless=stream_out.get_name().headless)
                else:
                    dynamic_length = ''

                if stream_out.has_single_chunk():
                    stream_data_new = stream_out.get_chunk_data_element().get_java_new(cardinality='ret.{0}Length'.format(stream_out.get_name().headless))
                else:
                    stream_data_new = stream_out.get_chunk_data_element().get_java_new(cardinality='{0}Length'.format(stream_out.get_name().headless))

                if stream_out.has_single_chunk():
                    template = template_stream_out_single_chunk
                else:
                    template = template_stream_out

                methods += template.format(doc=packet.get_java_formatted_doc(),
                                           name_headless=packet.get_name(skip=-2).headless,
                                           parameters=packet.get_java_parameters(context='call'),
                                           high_level_parameters=packet.get_java_parameters(high_level=True),
                                           return_type=return_type,
                                           result_type=packet.get_java_object_name(),
                                           stream_name_space=stream_out.get_name().space,
                                           stream_name_headless=stream_out.get_name().headless,
                                           stream_length_type=stream_length_type,
                                           stream_data_new=stream_data_new,
                                           fixed_length=common.wrap_non_empty(' = ', str(stream_out.get_fixed_length(default='')), ''),
                                           dynamic_length_3=dynamic_length.format(indent='\t' * 3),
                                           dynamic_length_5=dynamic_length.format(indent='\t' * 5),
                                           chunk_data_type=stream_out.get_chunk_data_element().get_java_type(),
                                           chunk_offset_check=chunk_offset_check,
                                           chunk_offset_check_indent=chunk_offset_check_indent,
                                           chunk_offset_check_end=chunk_offset_check_end,
                                           chunk_cardinality=stream_out.get_chunk_data_element().get_cardinality(),
                                           result_return=result_return)

        return methods

    def get_java_source(self, close_device_class=True):
        source  = self.get_java_import()
        source += self.get_java_class()
        source += self.get_java_function_id_definitions()
        source += self.get_java_constants()

        if self.get_generator().is_octave():
            source += self.get_octave_listener_lists()
        else:
            source += self.get_java_listener_lists()

        if self.get_generator().is_matlab() or self.get_generator().is_octave():
            source += self.get_matlab_callback_data_objects()

        source += self.get_java_return_objects()

        if not self.get_generator().is_octave():
            source += self.get_java_listener_definitions()

        source += self.get_java_constructor()
        source += self.get_java_response_expected()
        source += self.get_java_callback_listener_definitions()
        source += self.get_java_methods()
        source += self.get_java_add_listener()

        if close_device_class:
            source += '}\n'

        return source

    def get_java_provider(self):
        template = """{0}
package com.tinkerforge;

public class {1}Provider implements DeviceProvider {{
	public {1}Provider() {{}}
	public int getDeviceIdentifier() {{ return {1}.DEVICE_IDENTIFIER; }}
	public String getDeviceDisplayName() {{ return {1}.DEVICE_DISPLAY_NAME; }}
	public Class<? extends Device> getDeviceClass() {{ return {1}.class; }}
}}
"""

        return template.format(self.get_generator().get_header_comment('asterisk'),
                               self.get_java_class_name(),
                               self.get_device_identifier(),
                               self.get_long_display_name())

class JavaBindingsPacket(java_common.JavaPacket):
    def get_java_formatted_doc(self):
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
        text = self.get_device().specialize_java_doc_function_links(text)

        text = text.replace('Callback ', 'Listener ')
        text = text.replace(' Callback', ' Listener')
        text = text.replace('callback ', 'listener ')
        text = text.replace(' callback', ' listener')
        text = text.replace('.. note::', '\\note')
        text = text.replace('.. warning::', '\\warning')

        def format_parameter(name):
            return '\\c {0}'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        # escape HTML special chars
        text = escape(text)

        return '\n\t * '.join(text.strip().split('\n'))

    def get_java_bbgets(self, with_obj=False):
        bbgets = ''
        bbget_other = '\t\t{0}{1}{2} = {3}(bb.get{4}(){5}){6};'
        bool_array_unpack = '\t\t\t{0}{1}[i] = ({2}[i / 8] & (1 << (i % 8))) != 0;'
        bbget_bool_array = """		byte[] {0} = new byte[{1}];
		bb.get({0});
{2}
"""
        bbget_string = '\t\t{0}{1}{2} = {3}(bb{4}{5}){6};'
        new_arr ='{0} {1} = {2};'
        loop = """		{2}for (int i = 0; i < {0}; i++) {{
{1}
		}}"""

        for element in self.get_elements(direction='out'):
            bbget_format_bool_array = False
            type_ = ''

            if not with_obj:
                type_ = element.get_java_type()

            bbret = element.get_name().headless
            obj = ''

            if with_obj:
                obj = 'obj.'

            cast = ''
            cast_extra = ''
            suffix = ''

            if element.get_type() == 'uint8':
                cast = 'IPConnection.unsignedByte'
            elif element.get_type() == 'uint16':
                cast = 'IPConnection.unsignedShort'
            elif element.get_type() == 'uint32':
                cast = 'IPConnection.unsignedInt'
            elif element.get_type() == 'bool' and element.get_cardinality() <= 1:
                suffix = ' != 0'
            elif element.get_type() == 'bool' and element.get_cardinality() > 1:
                suffix = ''
            elif element.get_type() == 'char':
                if self.get_generator().is_octave():
                    cast = 'new String(new char[]{(char)'
                    suffix = '})'
                else:
                    cast = '(char)'
            elif element.get_type() == 'string':
                cast = 'IPConnection.string'
                cast_extra = ', {0}'.format(element.get_cardinality())

            format_type_ = ''

            if not element.get_cardinality() > 1 or (element.get_type() == 'string' and not with_obj):
                format_type_ = type_

            if element.get_type() == 'string':
                bbget = bbget_string
            elif element.get_type() == 'bool' and element.get_cardinality() > 1:
                bbget = bbget_bool_array
                bbget_format_bool_array = True
            else:
                bbget = bbget_other

            if not bbget_format_bool_array:
                bbget_format = bbget.format(format_type_,
                                            (' ' if len(format_type_) > 0 else '') + obj,
                                            bbret,
                                            cast,
                                            element.get_java_byte_buffer_method_suffix(),
                                            cast_extra,
                                            suffix)

            if element.get_cardinality() > 1 and element.get_type() != 'string':
                if with_obj:
                    if element.get_type() == 'bool':
                        bbget_format = bbget.format(bbret + 'Bits',
                                                    int(math.ceil(element.get_cardinality() / 8.0)),
                                                    loop.format(element.get_cardinality(),
                                                                bool_array_unpack.format(obj,
                                                                                         bbret,
                                                                                         bbret + 'Bits'),
                                                                ''))
                    else:
                        bbget_format = bbget_format.replace(' =', '[i] =')
                        bbget_format = loop.format(element.get_cardinality(), '\t' + bbget_format, '')
                else:
                    arr = new_arr.format(type_.replace(' ', ''), bbret, element.get_java_new())

                    if element.get_type() == 'bool':
                        bbget_format = bbget.format(bbret + 'Bits',
                                                    int(math.ceil(element.get_cardinality() / 8.0)),
                                                    loop.format(element.get_cardinality(),
                                                                bool_array_unpack.format(obj,
                                                                                         bbret,
                                                                                         bbret + 'Bits'),
                                                                arr + '\n\t\t'))
                    else:
                        bbget_format = bbget_format.replace(' =', '[i] =')
                        bbget_format = loop.format(element.get_cardinality(), '\t' + bbget_format, arr + '\n\t\t')

            bbgets += bbget_format + '\n'

        return bbgets, bbret

class JavaBindingsGenerator(java_common.JavaGeneratorTrait, common.BindingsGenerator):
    def get_bindings_name(self):
        return 'java'

    def get_bindings_display_name(self):
        return 'Java'

    def get_device_class(self):
        return JavaBindingsDevice

    def get_packet_class(self):
        return JavaBindingsPacket

    def get_element_class(self):
        return java_common.JavaElement

    def prepare(self):
        self.device_classes = []

        result = common.BindingsGenerator.prepare(self)

        if self.is_matlab():
            os.makedirs(os.path.join(self.get_bindings_dir(), 'matlab'))
        elif self.is_octave():
            os.makedirs(os.path.join(self.get_bindings_dir(), 'octave'))

        return result

    def generate(self, device):
        class_name = device.get_java_class_name()

        if self.is_matlab():
            flavor = 'matlab'
        elif self.is_octave():
            flavor = 'octave'
        else:
            flavor = ''

        with open(os.path.join(self.get_bindings_dir(), flavor, class_name + '.java'), 'w') as f:
            f.write(device.get_java_source())

        with open(os.path.join(self.get_bindings_dir(), flavor, class_name + 'Provider.java'), 'w') as f:
            f.write(device.get_java_provider())

        if device.is_released():
            self.device_classes.append(class_name)
            self.released_files.append(class_name + '.java')
            self.released_files.append(class_name + 'Provider.java')

    def finish(self):
        if self.is_matlab():
            flavor = 'matlab'
        elif self.is_octave():
            flavor = 'octave'
        else:
            flavor = ''

        with open(os.path.join(self.get_bindings_dir(), flavor, 'com.tinkerforge.DeviceProvider'), 'w') as f:
            for name in sorted(self.device_classes):
                f.write('com.tinkerforge.{0}Provider\n'.format(name))

        return common.BindingsGenerator.finish(self)

    def is_matlab(self):
        return False

    def is_octave(self):
        return False

def generate(root_dir):
    common.generate(root_dir, 'en', JavaBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
