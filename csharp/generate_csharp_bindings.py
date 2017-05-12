#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C# Bindings Generator
Copyright (C) 2012-2015, 2017 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2012 Olaf Lüke <olaf@tinkerforge.com>

generate_csharp_bindings.py: Generator for C# bindings

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
import csharp_common

# this is a list of all the Bricks and Bricklets support by C# bindings version
# 2.1.12 released on 2017-01-25. this list is fixed and must never be changed.
# the RS232 Bricklet is excluded, because it already used the new callback naming
# format by accident. all other devices in this list also need to support the
# old callback naming format for backward compatibility with existing programs
LEGACY_CALLBACK_DEVICES = {
'BrickDC',
'BrickIMU',
'BrickIMUV2',
'BrickMaster',
'BrickRED',
'BrickServo',
'BrickStepper',
'BrickletAccelerometer',
'BrickletAmbientLight',
'BrickletAmbientLightV2',
'BrickletAnalogIn',
'BrickletAnalogInV2',
'BrickletAnalogOut',
'BrickletAnalogOutV2',
'BrickletBarometer',
'BrickletCAN',
'BrickletCO2',
'BrickletColor',
'BrickletCurrent12',
'BrickletCurrent25',
'BrickletDistanceIR',
'BrickletDistanceUS',
'BrickletDualButton',
'BrickletDualRelay',
'BrickletDustDetector',
'BrickletGPS',
'BrickletHallEffect',
'BrickletHumidity',
'BrickletIndustrialAnalogOut',
'BrickletIndustrialDigitalIn4',
'BrickletIndustrialDigitalOut4',
'BrickletIndustrialDual020mA',
'BrickletIndustrialDualAnalogIn',
'BrickletIndustrialQuadRelay',
'BrickletIO16',
'BrickletIO4',
'BrickletJoystick',
'BrickletLaserRangeFinder',
'BrickletLCD16x2',
'BrickletLCD20x4',
'BrickletLEDStrip',
'BrickletLine',
'BrickletLinearPoti',
'BrickletLoadCell',
'BrickletMoisture',
'BrickletMotionDetector',
'BrickletMultiTouch',
'BrickletNFCRFID',
'BrickletOLED128x64',
'BrickletOLED64x48',
'BrickletPiezoBuzzer',
'BrickletPiezoSpeaker',
'BrickletPTC',
'BrickletRealTimeClock',
'BrickletRemoteSwitch',
'BrickletRGBLED',
'BrickletRotaryEncoder',
'BrickletRotaryPoti',
#'BrickletRS232',
'BrickletSegmentDisplay4x7',
'BrickletSolidStateRelay',
'BrickletSoundIntensity',
'BrickletTemperature',
'BrickletTemperatureIR',
'BrickletThermocouple',
'BrickletTilt',
'BrickletUVLight',
'BrickletVoltage',
'BrickletVoltageCurrent'
}

class CSharpBindingsDevice(csharp_common.CSharpDevice):
    def specialize_csharp_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return '<see cref="Tinkerforge.{0}.{1}Callback"/>'.format(packet.get_device().get_csharp_class_name(),
                                                                          packet.get_camel_case_name(skip=-2 if high_level else 0))
            else:
                return '<see cref="Tinkerforge.{0}.{1}"/>'.format(packet.get_device().get_csharp_class_name(),
                                                                  packet.get_camel_case_name(skip=-2 if high_level else 0))

        return self.specialize_doc_rst_links(text, specializer)

    def get_csharp_import(self):
        template = """{0}
using System;

namespace Tinkerforge
{{"""

        return template.format(self.get_generator().get_header_comment('asterisk'))

    def get_csharp_class(self):
        template = """
	/// <summary>
	///  {1}
	/// </summary>
	public class {0} : Device
	{{
		/// <summary>
		///  Used to identify this device type in
		///  <see cref="Tinkerforge.IPConnection.EnumerateCallback"/>.
		/// </summary>
		public static int DEVICE_IDENTIFIER = {2};

		/// <summary>
		///  The display name of this device.
		/// </summary>
		public static string DEVICE_DISPLAY_NAME = "{3}";
"""

        return template.format(self.get_csharp_class_name(),
                               common.select_lang(self.get_description()),
                               self.get_device_identifier(),
                               self.get_long_display_name())

    def get_csharp_delegates(self):
        delegates = '\n'
        template = """
		/// <summary>
		///  {2}
		/// </summary>
		public event {0}EventHandler {0}Callback;
		/// <summary>
		/// </summary>
		public delegate void {0}EventHandler({3} sender{1});
"""
        template_legacy = """
		/// <summary>
		/// </summary>
		public event {0}EventHandler {0} // for backward compatibility
		{{
			add {{ {0}Callback += value; }}
			remove {{ {0}Callback -= value; }}
		}}
"""

        for packet in self.get_packets('callback'):
            name = packet.get_camel_case_name()
            parameter = packet.get_csharp_parameter_list()
            doc = packet.get_csharp_formatted_doc()

            if parameter != '':
                parameter = ', ' + parameter

            delegates += template.format(name, parameter, doc, self.get_csharp_class_name())

            if self.get_csharp_class_name() in LEGACY_CALLBACK_DEVICES:
                delegates += template_legacy.format(name)

        return delegates

    def get_csharp_function_id_definitions(self):
        function_ids = ''
        template = """
		/// <summary>
		///  Function ID to be used with
		///  <see cref="Tinkerforge.Device.GetResponseExpected"/>,
		///  <see cref="Tinkerforge.Device.SetResponseExpected"/> and
		///  <see cref="Tinkerforge.Device.SetResponseExpectedAll"/>.
		/// </summary>
		public const byte {2}_{0} = {1};
"""

        for packet in self.get_packets():
            function_ids += template.format(packet.get_upper_case_name(),
                                            packet.get_function_id(),
                                            packet.get_type().upper())
        return function_ids

    def get_csharp_constants(self):
        template = """
		/// <summary>
		/// </summary>
		public const {0} {1}_{2} = {3};
"""
        constants = []

        for constant_group in self.get_constant_groups():
            for constant in constant_group.get_constants():
                if constant_group.get_type() == 'char':
                    value = "'{0}'".format(constant.get_value())
                else:
                    value = str(constant.get_value())

                constants.append(template.format(csharp_common.get_csharp_type(constant_group.get_type(), 1),
                                                 constant_group.get_upper_case_name(),
                                                 constant.get_upper_case_name(),
                                                 value))
        return '\n' + ''.join(constants)

    def get_csharp_constructor(self):
        callbacks = []
        template = '\t\t\tcallbackWrappers[CALLBACK_{0}] = new CallbackWrapper(On{1}Callback);'
        constructor = """
		/// <summary>
		///  Creates an object with the unique device ID <c>uid</c> and adds  it to
		///  the IPConnection <c>ipcon</c>.
		/// </summary>
		public {0}(string uid, IPConnection ipcon) : base(uid, ipcon)
		{{
			apiVersion[0] = {2};
			apiVersion[1] = {3};
			apiVersion[2] = {4};

{1}
"""

        for packet in self.get_packets('callback'):
            name_upper = packet.get_upper_case_name()
            name_pascal = packet.get_camel_case_name()
            callbacks.append(template.format(name_upper, name_pascal))

        return constructor.format(self.get_csharp_class_name(), '\n'.join(callbacks),
                                  *self.get_api_version())

    def get_csharp_response_expected(self):
        response_expected = '\n'
        template = "\t\t\tresponseExpected[{0}] = {1}\n"

        for packet in self.get_packets('function'):
            name_upper = 'FUNCTION_' + packet.get_upper_case_name()
            setto = 'ResponseExpectedFlag.FALSE;'

            if len(packet.get_elements('out')) > 0:
                setto = 'ResponseExpectedFlag.ALWAYS_TRUE;'
            elif packet.get_doc_type() in ['ccf', 'llf']:
                setto = 'ResponseExpectedFlag.TRUE;'

            response_expected += template.format(name_upper, setto)

        for packet in self.get_packets('callback'):
            name_upper = 'CALLBACK_' + packet.get_upper_case_name()
            setto = 'ResponseExpectedFlag.ALWAYS_FALSE;'
            response_expected += template.format(name_upper, setto)

        return response_expected + '\t\t}\n'

    def get_csharp_callbacks(self):
        callbacks = ''
        template = """
		/// <summary>
		/// </summary>
		protected void On{0}Callback(byte[] response)
		{{
{1}			var handler = {0}Callback;
			if(handler != null)
			{{
				handler(this{3});
			}}
		}}
"""

        for packet in self.get_packets('callback'):
            name = packet.get_camel_case_name()
            name_upper = packet.get_upper_case_name()
            eles = []

            for element in packet.get_elements('out'):
                eles.append(element.get_headless_camel_case_name())

            callParams = ", ".join(eles)
            signatureParams = packet.get_csharp_parameter_list()
            size = str(packet.get_request_size())

            convs = ''
            conv = '\t\t\t{0} {1} = LEConverter.{2}({3}, response{4});\n'
            conv_bool_array ="""			bool[] {0} = new bool[{1}];
			byte[] {2} = new byte[{3}];
			{2} = LEConverter.ByteArrayFrom({4}, response, {3});
			for(int i = 0; i < {1}; i++) {{
				{0}[i] = ({2}[i / 8] & (1 << (i % 8))) != 0;
			}}
"""

            pos = 8

            for element in packet.get_elements('out'):
                csharp_type = element.get_csharp_type()
                cname = element.get_headless_camel_case_name()
                from_method = element.get_csharp_le_converter_from_method()
                length = ''

                if element.get_cardinality() > 1 and element.get_type() != 'bool':
                    length = ', ' + str(element.get_cardinality())
                else:
                    pass

                if element.get_cardinality() > 1 and element.get_type() == 'bool':
                    convs += conv_bool_array.format(cname,
                                                    element.get_cardinality(),
                                                    cname + 'Bits',
                                                    str(int(math.ceil(element.get_cardinality() / 8.0))),
                                                    pos)
                else:
                    convs += conv.format(csharp_type,
                                         cname,
                                         from_method,
                                         pos,
                                         length)

                pos += element.get_size()

            if convs != '':
                convs += '\n'

            if callParams != '':
                callParams = ', ' + callParams

            callbacks += template.format(name, convs, name_upper, callParams, pos, signatureParams)

        return callbacks + "\t}\n}\n"

    def get_csharp_methods(self):
        methods = ''
        template = """
		/// <summary>
		///  {5}
		/// </summary>
		{0}
		{{
			byte[] request = CreateRequestPacket({1}, FUNCTION_{2});
{3}
{4}
		}}
"""

        template_noresponse = """			SendRequest(request);
"""

        template_response = """			byte[] response = SendRequest(request);
{0}"""

        for packet in self.get_packets('function'):
            ret_count = len(packet.get_elements('out'))
            size = str(packet.get_request_size())
            name_upper = packet.get_upper_case_name()
            doc = packet.get_csharp_formatted_doc()

            write_convs = ''
            write_conv = '\t\t\tLEConverter.To(({2}){0}, {1}, request);\n'
            write_conv_length = '\t\t\tLEConverter.To(({3}){0}, {1}, {2}, request);\n'
            _write_conv_length = """			{0}[] {1} = new {0}[{2}];
			for (int i = 0; i < {2}; ++i) {{
				{1}[i] = ({0}){3}[i];
			}}
			LEConverter.To({1}, {4}, {2}, request);\n"""
            write_conv_bool_array = """			byte[] {0} = new byte[{1}];
			for(int i = 0; i < {2}; i++) {{
				if ({3}[i]) {{
					{0}[i / 8] |= (byte)(1 << (i % 8));
				}}
			}}
			LEConverter.To((byte[]){0}, {4}, {1}, request);
"""

            pos = 8

            for element in packet.get_elements('in'):
                wname = element.get_headless_camel_case_name()
                csharp_type = element.get_csharp_le_converter_type()

                if element.get_cardinality() > 1:
                    if element.get_type() == 'bool':
                        write_convs += write_conv_bool_array.format(wname + 'Bits',
                                                                    str(int(math.ceil(element.get_cardinality() / 8.0))),
                                                                    element.get_cardinality(),
                                                                    wname,
                                                                    pos)
                    else:
                        if element.get_csharp_le_converter_type() != element.get_csharp_type():
                            cs_le_type = element.get_csharp_le_converter_type().replace('[', '')
                            cs_le_type = cs_le_type.replace(']', '')
                            write_convs += _write_conv_length.format(cs_le_type,
                                                                     '_' + wname,
                                                                     element.get_cardinality(),
                                                                     wname,
                                                                     pos)
                        else:
                            write_convs += write_conv_length.format(wname,
                                                                    pos,
                                                                    element.get_cardinality(),
                                                                    csharp_type)
                else:
                    write_convs += write_conv.format(wname, pos, csharp_type)

                pos += element.get_size()

            method_tail = ''
            read_convs = ''
            read_conv = '\n\t\t\t{0} = LEConverter.{1}({2}, response{3});'
            read_conv_bool_array = """\n			byte[] {0} = new byte[{1}];
			{4} = new bool[{3}];
			{0} = LEConverter.ByteArrayFrom({2}, response, {1});
			for(int i = 0; i < {3}; i++) {{
				{4}[i] = ({0}[i / 8] & (1 << (i % 8))) != 0;
			}}"""

            pos = 8

            for element in packet.get_elements('out'):
                aname = element.get_headless_camel_case_name()
                from_method = element.get_csharp_le_converter_from_method()
                length = ''

                if element.get_cardinality() > 1:
                    if element.get_type() == 'bool':
                        pass
                    else:
                        length = ', ' + str(element.get_cardinality())

                if ret_count == 1:
                    read_convs = '\n\t\t\treturn LEConverter.{0}({1}, response{2});'.format(from_method, pos, length)
                else:
                    if element.get_cardinality() > 1 and element.get_type() == 'bool':
                        read_convs += read_conv_bool_array.format(aname + 'Bits',
                                                                  str(int(math.ceil(element.get_cardinality() / 8.0))),
                                                                  pos,
                                                                  element.get_cardinality(),
                                                                  aname)
                    else:
                        read_convs += read_conv.format(aname, from_method, pos, length)

                pos += element.get_size()

            if ret_count > 0:
                method_tail = template_response.format(read_convs)
            else:
                method_tail = template_noresponse

            signature = packet.get_csharp_method_signature()
            methods += template.format(signature,
                                       size,
                                       name_upper,
                                       write_convs,
                                       method_tail,
                                       doc)

        return methods

    def get_csharp_source(self):
        function_names = self.get_packet_names('function')
        callback_names = self.get_packet_names('callback')

        for callback_name in callback_names:
            if callback_name + ' Callback' in function_names:
                raise common.GeneratorError("Generated callback name '{0}[ Callback]' collides with function name '{0} Callback'".format(callback_name))

        source  = self.get_csharp_import()
        source += self.get_csharp_class()
        source += self.get_csharp_function_id_definitions()
        source += self.get_csharp_constants()
        source += self.get_csharp_delegates()
        source += self.get_csharp_constructor()
        source += self.get_csharp_response_expected()
        source += self.get_csharp_methods()
        source += self.get_csharp_callbacks()

        return source

class CSharpBindingsPacket(csharp_common.CSharpPacket):
    def get_csharp_formatted_doc(self):
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
        text = self.get_device().specialize_csharp_doc_function_links(text)

        def format_parameter(name):
            return name # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return '\n\t\t///  '.join(text.strip().split('\n'))

class CSharpBindingsGenerator(common.BindingsGenerator):
    def get_bindings_name(self):
        return 'csharp'

    def get_bindings_display_name(self):
        return 'C#'

    def get_device_class(self):
        return CSharpBindingsDevice

    def get_packet_class(self):
        return CSharpBindingsPacket

    def get_element_class(self):
        return csharp_common.CSharpElement

    def generate(self, device):
        filename = '{0}.cs'.format(device.get_csharp_class_name())

        with open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename), 'w') as f:
            f.write(device.get_csharp_source())

        if device.is_released():
            self.released_files.append(filename)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', CSharpBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
