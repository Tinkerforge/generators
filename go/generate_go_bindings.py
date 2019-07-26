#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Go Bindings Generator
Copyright (C) 2018 Erik Fleckstein <erik@tinkerforge.com>

generate_go_bindings.py: Generator for Go bindings

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
import go_common

packet_param_types = set()
packet_return_types = set()

class GoBindingsDevice(go_common.GoDevice):

    def get_go_imports(self):
        tf_doc_link = {'en': '// See also the documentation here: https://www.tinkerforge.com/en/doc/Software/{device_category_camel}s/{device_name_camel}_{device_category_camel}_Go.html.',
                       'de': '// Siehe auch die Dokumentation hier: https://www.tinkerforge.com/de/doc/Software/{device_category_camel}s/{device_name_camel}_{device_category_camel}_Go.html.'
        }

        desc = common.select_lang(self.get_description())

        plenk = "‍REPLACE_WITH_ZWJ" if len(desc) > 0 and desc[-1].isupper() else ""
        description = desc + plenk + "."
        description += '\n// \n// \n'
        description += common.select_lang(tf_doc_link).format(device_category_camel = self.get_category().camel,
                                                              device_name_camel = self.get_name().camel)

        return """{header}

//{description}
package {device}

import (
	"encoding/binary"
	"bytes"
    . "github.com/Tinkerforge/go-api-bindings/internal"
    "github.com/Tinkerforge/go-api-bindings/ipconnection"
)
""".format(header=self.get_generator().get_header_comment(kind='asterisk'), description=description, device=self.get_go_package())

    def get_go_constants(self):
        constants = []

        # Create function and callback constants for get/set response expected
        for packet in self.get_packets('function'):
            constants.append((packet.get_name().camel, packet.get_function_id()))
        for packet in self.get_packets('callback'):
            constants.append(("Callback"+packet.get_name().camel, packet.get_function_id()))

        const_prefix = "Function"

        template = """type {name} = {type}

const (
    {values}
)
"""
        result = template.format(name=const_prefix,
                                 type="uint8",
                                 values="\n\t".join("{const_prefix}{name} {const_prefix} = {value}".format(const_prefix=const_prefix, name=name, value=value) for (name, value) in constants))

        # Create constants used in function parameters
        for constant_group in self.get_constant_groups():
            constant_type = constant_group.get_go_type()
            constant_group_name = constant_group.get_name().camel
            enum_values = []
            for constant in constant_group.get_constants():
                name = constant.get_name().camel
                value = str(constant.get_value()) if not "rune" in constant_type else "'" + constant.get_value() + "'"
                if constant_type == "bool":
                    value = value.lower()
                enum_values.append("{const_prefix}{name} {const_prefix} = {value}".format(const_prefix = constant_group_name, name=name, value=value))
            result += "\n" + template.format(name=constant_group_name, type=constant_type, values="\n\t".join(enum_values))

        return result

    def get_go_response_expected(self, response_expected_str):
        if "always_true" in response_expected_str:
            return "ResponseExpectedFlagAlwaysTrue"
        elif "true" in response_expected_str:
            return "ResponseExpectedFlagTrue"
        else:
            return "ResponseExpectedFlagFalse"

    def get_go_device_definition(self):
        return "type {name} struct{{\n\tdevice Device\n}}".format(name=self.get_go_name())


    def go_fill_payload(self, elements, bufferName):
        fill_payload = []
        for elem in elements:
            if elem.get_level() == 'low' and elem.get_role() == 'stream_chunk_data':
                fill_payload.append("{buf}.Write({type}SliceToByteSlice({name}[:]))".format(buf=bufferName, type= elem.get_go_type(ignore_cardinality=True).title(), name=elem.get_go_name()))
                continue

            if "string" in elem.get_go_type():
                fill_payload.append("{elem_name}_byte_slice, err := StringToByteSlice({elem_name}, {max_len})".format( elem_name=elem.get_go_name(), max_len=elem.get_cardinality()))
                fill_payload.append("if err != nil { return }")
                fill_payload.append("{buf}.Write({elem_name}_byte_slice)".format(buf=bufferName, elem_name=elem.get_go_name()))
            else:
                fill_payload.append("binary.Write(&{buf}, binary.LittleEndian, {elem_name});".format(buf=bufferName, elem_name=elem.get_go_name()))
        return fill_payload

    def go_read_results(self, elements, bufferName, low_level_in_bits=True):
        read_results = []
        for elem in elements:
            size = elem.get_size()

            if elem.get_level() == 'low' and elem.get_role() == 'stream_chunk_data':
                read_results.append("copy({name}[:], ByteSliceTo{type}Slice({buf}.Next({mult} * {chunk_size}/8)))".format(buf=bufferName, name=elem.get_go_name(), type=elem.get_go_type(ignore_cardinality=True).title(), chunk_size= elem.get_cardinality(), mult =  go_common.get_go_type_size(elem.get_go_type(ignore_cardinality=True))))
                continue

            if "rune" in elem.get_go_type() and elem.get_cardinality() == 1:
                read_results.append("{ret_name} = rune({buf}.Next(1)[0])".format(buf=bufferName, ret_name=elem.get_go_name()))
            elif "rune" in elem.get_go_type():
                read_results.append("copy({ret_name}[:], ByteSliceTo{type}Slice({buf}.Next({len})))".format(buf=bufferName, ret_name=elem.get_go_name(), type=elem.get_go_type(ignore_cardinality=True).title(), len=elem.get_cardinality()))
            elif elem.get_go_type() == "string":
                read_results.append("{ret_name} = ByteSliceTo{type}({buf}.Next({len}))".format(buf=bufferName, ret_name=elem.get_go_name(), type=elem.get_go_type(ignore_cardinality=True).title(), len=elem.get_cardinality()))
            else:
                read_results.append("binary.Read({buf}, binary.LittleEndian, &{ret_name})".format(buf=bufferName, ret_name=elem.get_go_name()))
        return read_results

    def get_go_device_implementation(self):
        template = """const DeviceIdentifier = {device_identifier}
const DeviceDisplayName = "{device_display_name}"

// Creates an object with the unique device ID `uid`. This object can then be used after the IP Connection `ipcon` is connected.
func New(uid string, ipcon *ipconnection.IPConnection) ({name}, error) {{
    internalIPCon := ipcon.GetInternalHandle().(IPConnection)
    dev, err := NewDevice([3]uint8{{ {apiVersion} }}, uid, &internalIPCon, {high_level_function_count})
    if err != nil {{
        return {name}{{}}, err
    }}
    {response_expected_config}
    return {name}{{dev}}, nil
}}

// Returns the response expected flag for the function specified by the function ID parameter.
// It is true if the function is expected to send a response, false otherwise.
//
// For getter functions this is enabled by default and cannot be disabled, because those
// functions will always send a response. For callback configuration functions it is enabled
// by default too, but can be disabled by SetResponseExpected.
// For setter functions it is disabled by default and can be enabled.
//
// Enabling the response expected flag for a setter function allows to detect timeouts
// and other error conditions calls of this setter as well. The device will then send a response
// for this purpose. If this flag is disabled for a setter function then no response is send
// and errors are silently ignored, because they cannot be detected.
//
// See SetResponseExpected for the list of function ID constants available for this function.
func (device *{name}) GetResponseExpected(functionID {function}) (bool, error) {{
    return device.device.GetResponseExpected(uint8(functionID))
}}

// Changes the response expected flag of the function specified by the function ID parameter.
// This flag can only be changed for setter (default value: false) and callback configuration
// functions (default value: true). For getter functions it is always enabled.
//
// Enabling the response expected flag for a setter function allows to detect timeouts and
// other error conditions calls of this setter as well. The device will then send a response
// for this purpose. If this flag is disabled for a setter function then no response is send
// and errors are silently ignored, because they cannot be detected.
func (device *{name}) SetResponseExpected(functionID {function}, responseExpected bool) error {{
    return device.device.SetResponseExpected(uint8(functionID), responseExpected)
}}

// Changes the response expected flag for all setter and callback configuration functions of this device at once.
func (device *{name}) SetResponseExpectedAll(responseExpected bool) {{
	device.device.SetResponseExpectedAll(responseExpected)
}}

// Returns the version of the API definition (major, minor, revision) implemented by this API bindings. This is neither the release version of this API bindings nor does it tell you anything about the represented Brick or Bricklet.
func (device *{name}) GetAPIVersion() [3]uint8 {{
    return device.device.GetAPIVersion()
}}

{functions}
"""
        resp_expct_template = "dev.ResponseExpected[{function}{name}] = {value};"
        resp_expct_config = [resp_expct_template.format(function="Function", name=packet.get_name().camel, value=self.get_go_response_expected(packet.get_response_expected())) for packet in self.get_packets('function')]

        functions = []

        callback_template = """{description}\nfunc (device *{device_name}) Register{name}Callback(fn func({type})) uint64 {{
            wrapper := func(byteSlice []byte) {{
                {buf_decl}
                {param_decls}
                {param_reads}
                fn({params})
            }}
    return device.device.RegisterCallback(uint8({fun_enum}Callback{fn_id}), wrapper)
}}

//Remove a registered {name_desc} callback.
func (device *{device_name}) Deregister{name}Callback(registrationID uint64) {{
    device.device.DeregisterCallback(uint8({fun_enum}Callback{fn_id}), registrationID)
}}
"""

        high_level_callback_template = """{description}
func (device *{device_name}) Register{name}Callback(fn func({type})) uint64 {{
    buf := make([]{buf_type}, 0)
    wrapper := func({params})  {{
        if int({message_chunk_offset}) != len(buf) {{
            buf = make([]{buf_type}, 0)
            if {message_chunk_offset} != 0 {{
                return
            }}
        }}
        toRead := MinU(uint64({message_length}-{message_chunk_offset}), uint64(len({message_chunk_data}[:])))
        buf = append(buf, {message_chunk_data}[:toRead]...)
        if len(buf) >= int({message_length}) {{
            fn({high_level_params})
            buf = make([]{buf_type}, 0)
        }}
    }}
    return device.Register{low_level_name}Callback(wrapper)
}}

//Remove a registered {name_desc} callback.
func (device *{device_name}) Deregister{name}Callback(registrationID uint64) {{
    device.Deregister{low_level_name}Callback(registrationID)
}}
"""

        for packet in self.get_packets('callback'):
            params = packet.get_elements(direction='out')

            param_decls = ["var {} {}".format(param.get_go_name(), param.get_go_type()) for param in params]
            param_reads = self.go_read_results(params, "buf", low_level_in_bits=False)

            functions.append(callback_template.format(name = packet.get_name().camel,
                                                      name_desc = packet.get_name().space,
                                                      device_name=self.get_go_name(),
                                                      param_decls = "\n".join(param_decls),
                                                      param_reads = "\n".join(param_reads),
                                                      buf_decl = "buf := bytes.NewBuffer(byteSlice[8:])" if len(params) > 0 else "",
                                                      params = ", ".join(param.get_go_name() for param in params),
                                                      description= packet.get_go_formatted_doc(),
                                                      type = ", ".join(ret.get_go_type() for ret in params),
                                                      fun_enum = "Function",
                                                      fn_id = packet.get_name().camel))
            if packet.has_high_level():
                high_level_params = list(p for p in params if p.get_level() != 'low')
                stream = packet.get_high_level('stream_out')
                data = stream.get_chunk_data_element()
                data_type = data.get_go_type(ignore_cardinality=True)
                length = stream.get_length_element().get_go_name() if stream.get_fixed_length() is None else stream.get_fixed_length()
                chunk_offset = stream.get_chunk_offset_element().get_go_name() if not stream.has_single_chunk() else 0


                functions.append(high_level_callback_template.format(name = packet.get_name(skip=-2).camel,
                                                      name_desc = packet.get_name().space,
                                                      description= packet.get_go_formatted_doc(),
                                                      device_name=self.get_go_name(),
                                                      type=", ".join([p.get_go_type() for p in high_level_params] + ["[]"+data_type]),
                                                      buf_type = data_type,
                                                      params = ", ".join(p.get_go_name() + " " + p.get_go_type() for p in params),
                                                      message_length = length,
                                                      message_chunk_offset = chunk_offset,
                                                      message_chunk_data = data.get_go_name(),
                                                      high_level_params = ", ".join([p.get_go_name() for p in high_level_params] + ["buf"]),
                                                      low_level_name=packet.get_name().camel))

        function_template = """{description}\nfunc (device *{device_name}) {name}({params}) ({returnType}) {{
        var buf bytes.Buffer
    {fill_payload}
    resultBytes, err := device.device.{fn}(uint8({fun_enum}{fn_id}), buf.Bytes())
    if err != nil {{
        return {return_results}err
    }}
    if len(resultBytes) > 0 {{
        var header PacketHeader

        header.FillFromBytes(resultBytes)
        if header.ErrorCode != 0 {{
            return {return_results}DeviceError(header.ErrorCode)
        }}

        {resultBufAssignment}bytes.NewBuffer(resultBytes[8:])
        {read_results}
    }}

    return {return_results}nil
}}"""

        stream_in_setter_template = """{description}\n\tfunc (device *{device_name}) {name}({params}) ({returnType}) {{
        {lowLevelResult}, err {colon}= device.device.SetHighLevel(func({length} uint64, {chunkOffset} uint64, {payload} []byte) (LowLevelWriteResult, error) {{
            arr := [{chunk_size}]{chunk_data_type}{{}}
            copy(arr[:], ByteSliceTo{chunk_data_type_title}Slice({payload}))

            {low_level_results}err := device.{name}LowLevel({low_level_params})

            var lowLevelResults bytes.Buffer
            {fill_low_level_results}

            return LowLevelWriteResult{{
                uint64({written}),
                lowLevelResults.Bytes()}}, err
        }}, {high_level_function_idx}, {element_size_in_bit}, {chunk_len_in_bit}, {chunk_data_type_title}SliceToByteSlice({data_var}))

         if err != nil {{
            return
        }}

        {resultBuf}
        {expand_low_level_results}
        {copy_written}
        return
    }}"""

        stream_out_getter_template = """{description}\n\tfunc (device *{device_name}) {name}({params}) ({return_type}) {{
        buf, {result}, err := device.device.GetHighLevel(func() (LowLevelResult, error) {{
            {low_level_vars}, err := device.{name}LowLevel({params_without_type})

            if err != nil {{
                return LowLevelResult{{}}, err
            }}

            var lowLevelResults bytes.Buffer
            {fill_low_level_results}

            return LowLevelResult{{
                uint64({length_var}),
                uint64({chunk_offset_var}),
                {type_title}SliceToByteSlice({chunk_data_var}[:]),
                lowLevelResults.Bytes()}}, nil
        }},
            {high_level_function_idx},
            {element_size_in_bit})
        if err != nil {{
            return {return_results}, err
        }}
        {resultBuf}
        {expand_low_level_results}
        return {return_results}, nil
    }}"""

        high_level_function_count = len([packet for packet in self.get_packets() if packet.get_high_level('stream_in') != None or packet.get_high_level('stream_out') != None])
        high_level_function_counter = -1
        for packet in self.get_packets('function'):
            returns = packet.get_elements(direction='out')
            packet_params = packet.get_elements(direction='in')
            for p in packet_params:
                packet_param_types.add(p.get_go_type())
            params = ["{name} {t}".format(name=param.get_go_name(), t=param.get_go_type()) for param in packet_params]

            if len(packet.get_elements(direction='out')) > 0:
                fn = "Get"
            else:
                fn = "Set"

            byte_count = sum([param.get_size() for param in packet_params])

            fill_payload = self.go_fill_payload(packet_params, "buf")

            read_results = self.go_read_results(returns, "resultBuf")
            return_results = []

            if len(packet.get_constant_groups()) > 0:
                constant_doc = "\n//\n// Associated constants:\n//\n//\t{constants}".format(constants = "\n//\t".join(["* " + const_group.get_name().camel + const.get_name().camel for const_group in packet.get_constant_groups() for const in const_group.get_constants()]))
            else:
                constant_doc = ""

            return_results = ", ".join(ret.get_go_name() for ret in returns) + (", " if len(returns) > 0 else "")

            functions.append(function_template.format(name= packet.get_name().camel,
                                     description= packet.get_go_formatted_doc() + constant_doc,
                                     params= ", ".join(params),
                                     returnType = packet.get_go_return_type(),
                                     byte_count = byte_count,
                                     device_name = self.get_go_name(),
                                     resultBufAssignment = "resultBuf := " if len(return_results) > 0 else "",
                                     fill_payload = "\n\t".join(fill_payload) + ("\n" if len(fill_payload) > 0 else ""),
                                     read_results = "\n\t".join(read_results) + ("\n" if len(read_results) > 0 else ""),
                                     return_results = return_results,
                                     fn = fn,
                                     fun_enum = "Function",
                                     fn_id=packet.get_name().camel))

            if packet.get_high_level('stream_in') != None:
                high_level_function_counter += 1
                stream = packet.get_high_level('stream_in')
                name = packet.get_name(skip=-2).camel
                params = ", ".join(["{name} {type}".format(name=param.get_go_name(), type=param.get_go_type()) for param in packet_params if param.get_level() != 'low'] + [stream.get_data_element().get_go_name() +" []"+stream.get_data_element().get_go_type(ignore_cardinality=True)])
                params_without_type = ", ".join([param.get_go_name() for param in packet_params if param.get_level() != 'low'])

                chunk_type = stream.get_chunk_data_element().get_go_type(ignore_cardinality=True)
                chunk_size = stream.get_chunk_data_element().get_cardinality()

                written_elements = [elem for elem in packet.get_elements(direction='out') if elem.get_level() == 'low' and elem.get_role() == 'stream_chunk_written']

                return_type = packet.get_go_return_type(high_level=True)
                length = stream.get_length_element().get_go_name() if stream.get_fixed_length() is None else "length"
                chunkOffset = stream.get_chunk_offset_element().get_go_name() if not stream.has_single_chunk() else "chunkOffset"
                payload = stream.get_chunk_data_element().get_go_name()

                low_level_params = []
                for param in packet_params:
                    if param.get_level() != 'low':
                        low_level_params.append(param.get_go_name())
                        continue
                    if param.get_role() == 'stream_chunk_data':
                        low_level_params.append("arr")
                        continue
                    low_level_params.append(param.get_go_type() + "(" + param.get_go_name() + ")")

                functions.append(stream_in_setter_template.format(description= packet.get_go_formatted_doc(),
                                                                   device_name=self.get_go_name(),
                                                                   name=name,
                                                                   params=params,
                                                                   returnType=return_type,
                                                                   length = length,
                                                                   chunkOffset = chunkOffset,
                                                                   payload = payload,
                                                                   chunk_size = chunk_size,
                                                                   chunk_data_type = chunk_type,
                                                                   chunk_data_type_title = chunk_type.title(),
                                                                   low_level_params = ", ".join(low_level_params),
                                                                   low_level_results = ", ".join(ret.get_go_name() for ret in returns)+(", " if len(returns) > 0 else ""),
                                                                   fill_low_level_results = "\n\t".join(self.go_fill_payload((ret for ret in returns if ret.get_level() != "low"), "lowLevelResults")),
                                                                   written = written_elements[0].get_go_name() if stream.has_short_write() else chunk_size,
                                                                   high_level_function_idx = high_level_function_counter,
                                                                   element_size_in_bit = go_common.get_go_type_size(stream.get_data_element().get_go_type(ignore_cardinality=True)),
                                                                   chunk_len_in_bit = chunk_size * go_common.get_go_type_size(stream.get_data_element().get_go_type(ignore_cardinality=True)),
                                                                   data_var= stream.get_data_element().get_go_name(),
                                                                   lowLevelResult = "lowLevelResult" if return_type != "err error" else "_",
                                                                   colon = ":" if return_type != "err error"  else "",
                                                                   resultBuf = "resultBuf := bytes.NewBuffer(lowLevelResult.Result)\n" if any(ret for ret in returns if ret.get_level() != "low") else "",
                                                                   expand_low_level_results = "\n\t".join(self.go_read_results((ret for ret in returns if ret.get_level() != "low"), "resultBuf")),
                                                                   copy_written=written_elements[0].get_go_name() + " = lowLevelResult.Written" if stream.has_short_write() else ""))



            if packet.get_high_level('stream_out') != None:
                assert(fn == 'Get')
                high_level_function_counter += 1
                stream = packet.get_high_level('stream_out')
                name = packet.get_name(skip=-2).camel
                params = ", ".join(["{name} {type}".format(name=param.get_go_name(), type=param.get_go_type()) for param in packet_params if param.get_level() != 'low'])
                params_without_type = ", ".join([param.get_go_name() for param in packet_params if param.get_level() != 'low'])
                return_results = ", ".join(["ByteSliceTo{type}Slice(buf)".format(type=stream.get_data_element().get_go_type(ignore_cardinality=True).title())]+[ret.get_go_name() for ret in returns if ret.get_level() != 'low'])

                low_level_params = []
                for param in packet_params:
                    if param.get_level() != 'low':
                        low_level_params.append(param.get_go_name())
                    else:
                       print("Unexpected low level parameter in stream_out-getter!")


                if stream.get_fixed_length() is not None:
                    length = stream.get_fixed_length()
                else:
                    length = stream.get_length_element().get_go_name()

                if not stream.has_single_chunk():
                    chunk_offset = stream.get_chunk_offset_element().get_go_name()
                else:
                    chunk_offset = stream.get_length_element().get_go_name()

                functions.append(stream_out_getter_template.format(description= packet.get_go_formatted_doc(),
                                                                   device_name=self.get_go_name(),
                                                                   name=name,
                                                                   params=params,
                                                                   result = "result" if any(ret for ret in returns if ret.get_level() != "low") else "_",
                                                                   resultBuf = "resultBuf := bytes.NewBuffer(result)" if any(ret for ret in returns if ret.get_level() != "low") else "",
                                                                   params_without_type = params_without_type,
                                                                   return_type = packet.get_go_return_type(high_level=True),
                                                                   low_level_vars = ", ".join(ret.get_go_name() for ret in returns),
                                                                   fill_low_level_results = "\n\t".join(self.go_fill_payload((ret for ret in returns if ret.get_level() != "low"), "lowLevelResults")),
                                                                   length_var = length,
                                                                   chunk_offset_var = chunk_offset,
                                                                   type_lower = stream.get_chunk_data_element().get_go_type(ignore_cardinality=True).lower(),
                                                                   type_title = stream.get_chunk_data_element().get_go_type(ignore_cardinality=True).title(),
                                                                   chunk_data_var = stream.get_chunk_data_element().get_go_name(),
                                                                   high_level_function_idx = high_level_function_counter,
                                                                   element_size_in_bit = go_common.get_go_type_size(stream.get_data_element().get_go_type(ignore_cardinality=True)),
                                                                   return_results = return_results,
                                                                   expand_low_level_results = "\n\t".join(self.go_read_results((ret for ret in returns if ret.get_level() != "low"), "resultBuf"))
                                                                   ))

        return template.format(name=self.get_go_name(),
                               device_identifier = self.get_device_identifier(),
                               device_display_name = self.get_long_display_name(),
                               name_under = self.get_name().under + "_" + self.get_category().under,
                                name_camel = self.get_go_name(),
                               apiVersion = "{},{},{}".format(*self.get_api_version()),
                               high_level_function_count = high_level_function_count,
                               response_expected_config="\n\t".join(resp_expct_config),
                               function= "Function",
                               functions="\n\n".join(functions))

    def get_go_source(self):
        return "\n".join([
            self.get_go_imports(),
            self.get_go_constants(),
            self.get_go_device_definition(),
            self.get_go_device_implementation()
        ])

class GoBindingsGenerator(common.BindingsGenerator):
    def get_bindings_name(self):
        return 'go'

    def get_bindings_display_name(self):
        return 'Go'

    def get_device_class(self):
        return GoBindingsDevice

    def get_packet_class(self):
        return go_common.GoPacket

    def get_element_class(self):
        return go_common.GoElement

    def get_constant_group_class(self):
        return go_common.GoConstantGroup

    def generate(self, device):
        filename = '{0}_{1}'.format(device.get_name().under, device.get_category().under)
        os.mkdir(os.path.join(self.get_bindings_dir(), filename))
        if sys.version_info.major >= 3:
            content = device.get_go_source().replace("‍REPLACE_WITH_ZWJ", "\u200d")
        else:
            content = device.get_go_source().replace("‍REPLACE_WITH_ZWJ", (u"\u200d").encode('utf-8'))
        with open(os.path.join(self.get_bindings_dir(), filename + '.go'), 'w') as f:
            f.write(content)

        if device.is_released():
            self.released_files.append(filename + '.go')

def generate(root_dir):
    common.generate(root_dir, 'en', GoBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
