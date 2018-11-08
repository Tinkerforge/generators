#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Rust Bindings Generator
Copyright (C) 2018 Erik Fleckstein <erik@tinkerforge.com>

generate_rust_bindings.py: Generator for Rust bindings

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
import rust_common

packet_param_types = set()
packet_return_types = set()

class RustBindingsDevice(rust_common.RustDevice):    

    def get_rust_imports(self):
        conv_receiver_imports = ["ConvertingReceiver"]

        # High level functions return a Result<(PayloadT, ResultT), BrickletRecvTimeoutError> directly, because they block.
        if any(packet.has_high_level() for packet in self.get_packets()):
            conv_receiver_imports.append("BrickletRecvTimeoutError")

        # Conversion from String to bytes can raise an error, which is sent directly into the created result channel.
        # Rust can't deduce the channel's type parameters, so we need to specify them. BrickletError is the Result's error type.
        if any("String" in elem.get_rust_type() for packet in self.get_packets() for elem in packet.get_elements(direction='in')):
            conv_receiver_imports.append("BrickletError")

        conv_receiver = conv_receiver_imports[0] if len(conv_receiver_imports) == 1 else ("{" + ", ".join(conv_receiver_imports) + "}")

        return """{header}
        
//! {description}
use crate::{{
    byte_converter::*,
    converting_receiver::{conv_receiver},{callback_recv}{high_level_callback_recv}
    device::*,
    ip_connection::IpConnection,{low_level}    
}};""".format(header=self.get_generator().get_header_comment(kind='asterisk'),
              description=common.select_lang(self.get_description()),
              callback_recv = "" if len(self.get_packets("callback")) == 0 else "\n\tconverting_callback_receiver::ConvertingCallbackReceiver,",
              high_level_callback_recv = "" if all(not packet.has_high_level() for packet in self.get_packets("callback")) else "\n\tconverting_high_level_callback_receiver::ConvertingHighLevelCallbackReceiver,",
              low_level = "" if all(not packet.has_high_level() for packet in self.get_packets()) else "\n\tlow_level_traits::*",
              conv_receiver = conv_receiver)

    def get_rust_constants(self):        
        constants = []

        # Create function and callback constants for get/set response expected
        for packet in self.get_packets('function'):
            constants.append((packet.get_name().camel_abbrv, packet.get_function_id()))
        for packet in self.get_packets('callback'):
            constants.append(("Callback"+packet.get_name().camel_abbrv, packet.get_function_id()))
        
        function_enum_name = self.get_rust_name() + "Function"

        result = """pub enum {name} {{
    {values}
}}""".format(name= function_enum_name, 
             values = ",\n\t".join(name for (name, value) in constants))

        # Create mapping from enum values to integer constants
        from_template = """
impl From<{function}> for u8 {{
    fn from(fun: {function}) -> Self {{
        match fun {{
            {patterns}
        }}
    }}
}}"""
        result += from_template.format(
            function=function_enum_name,
            patterns = ",\n\t\t\t".join("{function}::{name} => {value}".format(name=name, value=value, function=function_enum_name) for (name, value) in constants))
        
        # Create constants used in function parameters
        for constant_group in self.get_constant_groups():
            constant_type = constant_group.get_elements()[0].get_rust_type(ignore_cardinality=True)
            constant_name = self.get_name().upper + "_" + self.get_category().upper +'_'+ constant_group.get_name().upper + "_" 
            enum_values = []
            for constant in constant_group.get_constants():
                name = constant_name + constant.get_name().upper
                value = str(constant.get_value()) if not "char" in constant_type else "'" + constant.get_value() + "'"
                # clippy nags about number literals with a length > 5, so insert '_' after every three characters from the right:
                # 4294967295 becomes 4_294_967_295
                if len(value) > 5 and "32" in constant_type or "64" in constant_type:
                    value = value[::-1]                  
                    value = "_".join(value[i:i+3] for i in range(0, len(value), 3))
                    value = value[::-1]
                enum_values.append("pub const {name}: {type} = {value};".format(type=constant_type, name=name, value=value))
            result += "\n" + "\n".join(enum_values)

        return result
    

    def get_rust_structs_and_trait_impls(self):
        result = ""
        member_template = """pub {name}: {type},"""
        struct_template = """\n{derive_string}
pub struct {name} {{
    {members}
}}
"""
        from_bytes_template = """impl FromByteSlice for {name} {{
    fn bytes_expected() -> usize {{ {size_in_bytes} }}
    fn from_le_bytes({unused_bytes}bytes: &[u8]) -> {name} {{
        {name} {{ {init_string} }}
    }}
}}
"""

        low_level_read_template = """impl LowLevelRead<{data_type}, {result_type}> for {low_level_type} {{
    fn ll_message_length(&self) -> usize {{
		{length_var}
	}}

	fn ll_message_chunk_offset(&self) -> usize {{
		{chunk_offset_var}
	}}

	fn ll_message_chunk_data(&self) -> &[{data_type}] {{
		{chunk_data_var}
	}}

	fn get_result(&self) -> {result_type} {{
		{result_type} {{
			{result_member_assignments}
		}}
	}}
}}
"""
        low_level_write_template = """impl LowLevelWrite<{result_type}> for {low_level_type} {{
    fn ll_message_written(&self) -> usize {{
		{written_var}
	}}
	
	fn get_result(&self) -> {result_type} {{
		{result_type} {{
			{result_member_assignments}
		}}
	}}
}}
"""
        self.returnTypes = {}
        
        for packet in self.get_packets():
            returns = packet.get_elements(direction='out')            
            name = packet.get_rust_type_name() + ("Event" if packet.get_type() == 'callback' else "")
            
            if name in self.returnTypes.values():
                # Another function already created this struct.
                self.returnTypes[packet] = name
                continue

            # Don't create structs for functions returning nothing or one value, except if they are low level functions.
            if len(returns) == 0 and not packet.has_high_level():
                self.returnTypes[packet] = "()"
                packet_return_types.add("()")
                continue
            if len(returns) == 1 and not packet.has_high_level():
                self.returnTypes[packet] = returns[0].get_rust_type()
                packet_return_types.add(returns[0].get_rust_type())
                continue

            # Create struct for return type
            self.returnTypes[packet] = name
            for r in returns:
                packet_return_types.add(r.get_rust_type())

            byte_size = sum(ret.get_size() for ret in returns)

            members = "\n\t".join([member_template.format(name=ret.get_rust_name(), type=ret.get_rust_type()) for ret in returns])
            init_exprs = []
            byte_offset = 0
            for ret in returns:
                size = ret.get_size()
                init_exprs.append("{name}: <{type}>::from_le_bytes(&bytes[{first_byte}..{to}])".format(name=ret.get_rust_name(), type=ret.get_rust_type(), first_byte=byte_offset, to=byte_offset + size))
                byte_offset += size
            
            init_string = ",".join(init_exprs)
            
            result += struct_template.format(name=name,
                                             members = members,
                                             derive_string = packet.get_rust_derive_string())
            result += from_bytes_template.format(name=name,unused_bytes = "" if byte_size > 0 else "_", size_in_bytes=byte_size, init_string=init_string)

            if packet.get_high_level('stream_in') != None:
                ll_data = [elem for elem in packet.get_elements(direction='in') if elem.get_level() == 'low' and elem.get_role() == 'stream_chunk_data'][0]
                written_var = ll_data.get_cardinality()
                if packet.get_high_level('stream_in').has_short_write():                    
                    written_elem = [elem for elem in packet.get_elements(direction='out') if elem.get_level() == 'low' and elem.get_role() == 'stream_chunk_written'][0]
                    written_var = "self.{name} as usize".format(name=written_elem.get_rust_name())
                hl_returns = [elem for elem in packet.get_elements(direction='out') if elem.get_level() != 'low']
                member_assignment_template = "{name}: self.{name}"
                member_assignments = ",\n\t\t\t".join([member_assignment_template.format(name=ret.get_rust_name()) for ret in hl_returns])

                result += low_level_write_template.format(result_type = packet.get_rust_type_name(skip=-2) + "Result",
                                                          low_level_type = packet.get_rust_type_name() + ("Event" if packet.get_type() == 'callback' else ""),
                                                          written_var = written_var,
                                                          result_member_assignments=member_assignments)
            if packet.get_high_level('stream_out') != None:
                ll_data = [elem for elem in packet.get_elements(direction='out') if elem.get_level() == 'low' and elem.get_role() == 'stream_chunk_data'][0]
                
                length_var = ll_data.get_cardinality()
                if any(elem.get_level() == 'low' and elem.get_role() == 'stream_length' for elem in packet.get_elements(direction='out')):
                    length_var = "self.{name} as usize".format(name=[elem for elem in packet.get_elements(direction='out') if elem.get_level() == 'low' and elem.get_role() == 'stream_length'][0].get_rust_name())
                
                chunk_offset_var = "0"
                if any(elem.get_level() == 'low' and elem.get_role() == 'stream_chunk_offset' for elem in packet.get_elements(direction='out')):
                    chunk_offset_var = "self.{name} as usize".format(name=[elem for elem in packet.get_elements(direction='out') if elem.get_level() == 'low' and elem.get_role() == 'stream_chunk_offset'][0].get_rust_name())
                
                chunk_data_var = "&self.{name}".format(name=[elem for elem in packet.get_elements(direction='out') if elem.get_level() == 'low' and elem.get_role() == 'stream_chunk_data'][0].get_rust_name())
                
                hl_returns = [elem for elem in packet.get_elements(direction='out') if elem.get_level() != 'low']
                member_assignment_template = "{name}: self.{name}"
                member_assignments = ",\n\t\t\t".join([member_assignment_template.format(name=ret.get_rust_name()) for ret in hl_returns])
                
                result += low_level_read_template.format(data_type=ll_data.get_rust_type(ignore_cardinality=True),
                                                         result_type = packet.get_rust_type_name(skip=-2) + "Result",
                                                         low_level_type = packet.get_rust_type_name() + ("Event" if packet.get_type() == 'callback' else ""),
                                                         length_var = length_var,
                                                         chunk_offset_var = chunk_offset_var,
                                                         chunk_data_var = chunk_data_var,
                                                         result_member_assignments = member_assignments)

        #generate low level result structs (for results created by the low level function, which are not stream info, but should be given to the user)
        self.returnTypesResult = {}
        self.returnTypesResultCardinality = {}
        low_level_packets = [packet for packet in self.get_packets() if packet.has_high_level()]
        for packet in low_level_packets:            
            returns = [elem for elem in packet.get_elements(direction='out') if elem.get_level() != 'low']
                    
            name = packet.get_rust_type_name(skip=-2) + "Result"
            if name in self.returnTypesResult.values():
                self.returnTypesResult[packet] = name
                self.returnTypesResultCardinality[packet] = len(returns)
                continue            
            
            self.returnTypesResult[packet] = name
            self.returnTypesResultCardinality[packet] = len(returns)

            members = "\n\t".join([member_template.format(name=ret.get_rust_name(), type=ret.get_rust_type()) for ret in returns])
            result += struct_template.format(name=name,
                                             members = members,
                                             derive_string = packet.get_rust_derive_string(high_level_only=True))           
        return result

    def get_rust_response_expected(self, response_expected_str):
        if "always_true" in response_expected_str:
            return "ResponseExpectedFlag::AlwaysTrue"
        elif "true" in response_expected_str:
            return "ResponseExpectedFlag::True"
        else:
            return "ResponseExpectedFlag::False"

    def get_rust_device_definition(self):
        return "/// {description}\n#[derive(Clone)]\npub struct {name} {{\n\tdevice: Device,\n}}".format(name=self.get_rust_name(), description=common.select_lang(self.get_description()))

    def get_rust_device_implementation(self):
        template = """impl {name} {{
    pub const DEVICE_IDENTIFIER: u16 = {device_identifier};
    pub const DEVICE_DISPLAY_NAME: &'static str = "{device_display_name}";
    /// Creates an object with the unique device ID `uid`. This object can then be used after the IP Connection `ip_connection` is connected.
    pub fn new(uid: &str, ip_connection: &IpConnection) -> {name} {{
        let mut result = {name} {{ device: Device::new({apiVersion}, uid, ip_connection, {high_level_function_count}) }};
        {response_expected_config}
        result
    }}

    /// Returns the response expected flag for the function specified by the function ID parameter.
    /// It is true if the function is expected to send a response, false otherwise.
    /// 
    /// For getter functions this is enabled by default and cannot be disabled, because those 
    /// functions will always send a response. For callback configuration functions it is enabled 
    /// by default too, but can be disabled by [`set_response_expected`](crate::{name_under}::{name_camel}::set_response_expected). 
    /// For setter functions it is disabled by default and can be enabled.
    /// 
    /// Enabling the response expected flag for a setter function allows to detect timeouts 
    /// and other error conditions calls of this setter as well. The device will then send a response
    /// for this purpose. If this flag is disabled for a setter function then no response is send
    /// and errors are silently ignored, because they cannot be detected.
    /// 
    /// See [`set_response_expected`](crate::{name_under}::{name_camel}::set_response_expected) for the list of function ID constants available for this function.
    pub fn get_response_expected(&mut self, fun: {function}) -> Result<bool, GetResponseExpectedError> {{
        self.device.get_response_expected(u8::from(fun))
    }}

    /// Changes the response expected flag of the function specified by the function ID parameter.
    /// This flag can only be changed for setter (default value: false) and callback configuration
    /// functions (default value: true). For getter functions it is always enabled.
    /// 
    /// Enabling the response expected flag for a setter function allows to detect timeouts and
    /// other error conditions calls of this setter as well. The device will then send a response
    /// for this purpose. If this flag is disabled for a setter function then no response is send
    /// and errors are silently ignored, because they cannot be detected.
    pub fn set_response_expected(&mut self, fun: {function}, response_expected: bool) -> Result<(), SetResponseExpectedError> {{
        self.device.set_response_expected(u8::from(fun), response_expected)
    }}

    /// Changes the response expected flag for all setter and callback configuration functions of this device at once.
    pub fn set_response_expected_all(&mut self, response_expected: bool) {{
        self.device.set_response_expected_all(response_expected)
    }}

    {functions}
}}"""
        resp_expct_template = "result.device.response_expected[u8::from({function}::{name}) as usize] = {value};"
        resp_expct_config = [resp_expct_template.format(function=self.get_rust_name() + "Function", name=packet.get_name().camel_abbrv, value=self.get_rust_response_expected(packet.get_response_expected())) for packet in self.get_packets('function')]
     
        functions = []

        callback_template = """{description}\n\tpub fn get_{name}_callback_receiver(&self) -> ConvertingCallbackReceiver<{type}> {{
        self.device.get_callback_receiver(u8::from({fun_enum}::Callback{fn_id}))
    }}"""
        high_level_callback_template = """{description}\n\tpub fn get_{name}_callback_receiver(&self) -> ConvertingHighLevelCallbackReceiver<{payload_type}, {result_type}, {low_level_type}> {{
        ConvertingHighLevelCallbackReceiver::new(self.device.get_callback_receiver(u8::from({fun_enum}::Callback{fn_id})))
    }}"""

        for packet in self.get_packets('callback'):
            functions.append(callback_template.format(name = packet.get_name().under,
                                                      description= packet.get_rust_formatted_doc(),
                                                      type = self.returnTypes[packet],
                                                      fun_enum = self.get_rust_name() + "Function",
                                                      fn_id = packet.get_name().camel_abbrv))
            if packet.has_high_level():
                payload_type = [elem.get_rust_type(ignore_cardinality=True) for elem in packet.get_elements(direction='out') if elem.get_level() == 'low' and elem.get_role() == 'stream_chunk_data'][0]

                functions.append(high_level_callback_template.format(name = packet.get_name(skip=-2).under,
                                                      description= packet.get_rust_formatted_doc(),
                                                      payload_type=payload_type,
                                                      result_type=packet.get_name(skip=-2).camel_abbrv+"Result",
                                                      low_level_type = self.returnTypes[packet],
                                                      fun_enum = self.get_rust_name() + "Function",
                                                      fn_id = packet.get_name().camel_abbrv))

        function_template = """{description}\n\tpub fn {name}(&self{params}) -> {returnType} {{
        let {mut}payload = vec![0;{byte_count}];
        {fill_payload}
        self.device.{fn}(u8::from({fun_enum}::{fn_id}), payload)
    }}"""


        stream_in_setter_template = """{description}\n\tpub fn {name}(&self{params}) -> Result<(), BrickletRecvTimeoutError> {{
        let _ll_result = self.device.set_high_level({high_level_function_idx}, {stream_data}, {stream_size}, {chunk_size}, &mut |{unused_length}length: usize, {unused_chunk_offset}chunk_offset: usize, chunk: &[{chunk_type}]| {{
            let chunk_length = chunk.len() as u16;
            let mut chunk_array = [<{chunk_type}>::default(); {chunk_size}];
            chunk_array[0..chunk_length as usize].copy_from_slice(&chunk);

            let result = self.{low_level_function}({low_level_params}).recv();
            if let Err(BrickletRecvTimeoutError::SuccessButResponseExpectedIsDisabled) = result{{
                Ok(Default::default())                
            }}
            else {{
                result
            }}        
        }})?;
        Ok(())
    }}"""
        stream_in_getter_template = """{description}\n\tpub fn {name}(&self{params}) -> Result<{result_type}, BrickletRecvTimeoutError> {{
        let ll_result = self.device.set_high_level({high_level_function_idx}, {stream_data}, {stream_size}, {chunk_size}, &mut |{unused_length}length: usize, {unused_chunk_offset}chunk_offset: usize, chunk: &[{chunk_type}]| {{
            let chunk_length = chunk.len() as u16;
            let mut chunk_array = [<{chunk_type}>::default(); {chunk_size}];
            chunk_array[0..chunk_length as usize].copy_from_slice(&chunk);

            self.{low_level_function}({low_level_params}).recv()
        }})?;
        {short_write_result}
    }}"""

        stream_out_getter_template = """{description}\n\tpub fn {name}(&self{params}) -> Result<{open_parenthesis}Vec<{payload_type}>{result_type}{close_parenthesis}, BrickletRecvTimeoutError> {{
        let ll_result = self.device.get_high_level({high_level_function_idx}, &mut || {{
            self.{low_level_function}({low_level_params}).recv()
        }})?;
        Ok({open_parenthesis}ll_result.0{result}{close_parenthesis})
    }}"""

        high_level_function_count = len([packet for packet in self.get_packets() if packet.get_high_level('stream_in') != None or packet.get_high_level('stream_out') != None])
        high_level_function_counter = -1
        for packet in self.get_packets('function'):
            packet_params = packet.get_elements(direction='in')
            for p in packet_params:
                packet_param_types.add(p.get_rust_type())
            params = ["{name}: {type}".format(name=param.get_rust_name(), type=param.get_rust_type()) for param in packet_params]

            returnType = "ConvertingReceiver<{type}>".format(type=self.returnTypes[packet])

            if len(packet.get_elements(direction='out')) > 0:                
                fn = "get"
            else:                
                fn = "set"
            
            byte_count = sum([param.get_size() for param in packet_params])

            fill_payload = []
            byte_offset = 0

            string_param_template = """match <String>::try_to_le_bytes({param_name}, {max_len}) {{
            Err(e) => {{
                let (tx, rx) = std::sync::mpsc::channel::<Result<Vec<u8>, BrickletError>>();
                let _ = tx.send(Err(e));
                return ConvertingReceiver::new(rx, std::time::Duration::new(1,0));
            }}
            Ok(bytes) => payload[{first_byte}..{to}].copy_from_slice(&bytes)
        }}
            """

            for param in packet_params:
                size = param.get_size()
                if "String" in param.get_rust_type():
                    fill_payload.append(string_param_template.format(param_name=param.get_rust_name(), max_len=size, type=param.get_rust_type(), first_byte=byte_offset, to=byte_offset + size))
                else:
                    fill_payload.append("payload[{first_byte}..{to}].copy_from_slice(&<{type}>::to_le_bytes({param_name}));".format(param_name=param.get_rust_name(), type=param.get_rust_type(), first_byte=byte_offset, to=byte_offset + size))
                byte_offset += size
            
            if len(packet.get_constant_groups()) > 0:
                constant_doc = "\n\t///\n\t/// Associated constants:\n\t/// {constants}".format(constants = "\n\t///\t".join(["* " + self.get_name().upper + self.get_category().upper +'_'+ const_group.get_name().upper + "_" + const.get_name().upper for const_group in packet.get_constant_groups() for const in const_group.get_constants()]))
            else:
                constant_doc = ""

            functions.append(function_template.format(name= packet.get_name().under,
                                     description= packet.get_rust_formatted_doc() + constant_doc,
                                     params= (", " if len(params) > 0 else "") +  ", ".join(params),
                                     returnType = returnType,
                                     mut = "mut " if byte_count > 0 else "",
                                     byte_count = byte_count,
                                     fill_payload = "\n\t\t".join(fill_payload) + ("\n" if len(fill_payload) > 0 else ""),
                                     fn = fn,
                                     fun_enum = self.get_rust_name() + "Function",
                                     fn_id=packet.get_name().camel_abbrv))

            if packet.get_high_level('stream_in') != None:                
                high_level_function_counter += 1
                stream = packet.get_high_level('stream_in')
                name = packet.get_name(skip=-2).under
                params = ", ".join(["{name}: {type}".format(name=param.get_rust_name(), type=param.get_rust_type()) for param in packet_params if param.get_level() != 'low'] + [stream.get_name().under +": &["+stream.get_data_element().get_rust_type(ignore_cardinality=True)+"]"])               
                
                low_level_params = []
                have_length = False
                have_chunk_offset = False
                for param in packet_params:
                    if param.get_level() != 'low':
                        low_level_params.append(param.get_rust_name())
                    else:
                        role = param.get_role()
                        if role == 'stream_length':
                            low_level_params.append("length as " + param.get_rust_type())
                            have_length = True
                        elif role == 'stream_chunk_offset':
                            low_level_params.append("chunk_offset as " + param.get_rust_type())
                            have_chunk_offset = True
                        elif role == 'stream_chunk_data':
                            low_level_params.append("chunk_array")
                        else:
                            print("Unknown role {role} for stream_in-getter".format(role=role))

                if fn == 'get':
                    result_count = self.returnTypesResultCardinality[packet]
                    short_write = stream.has_short_write()                    

                    # Don't return structs without or with one member only. The decision tree is a bit more complicated than the one below because of short writes.
                    #  
                    # scenario                                     return                          result_type
                    # short write and no other results             Ok(ll_result.0)                 usize
                    # short write and one other result             Ok(ll_result.0, ll_result.1.0)  (usize, type of first item of ...result)
                    # short write and two or more results          Ok(ll_result)                   (usize, ...result)
                    # no short write and no other results          Ok(())                          ()
                    # no short write and one other results         Ok(ll_result.1.0)               type of first item of ...result
                    # no short write and two or more other results Ok(ll_result.1)                 ...result
                    if short_write:
                        if   result_count == 0:
                            fn_result = "Ok(ll_result.0)"
                            fn_result_type = "usize"
                        elif result_count == 1:
                            first_result = next(x for x in packet.get_elements(direction='out') if x.get_level() != 'low')
                            fn_result = "Ok((ll_result.0, ll_result.1." + first_result.get_rust_name() + "))"
                            fn_result_type = "(usize, " + first_result.get_rust_type() + ")"
                        else:
                            fn_result = "Ok(ll_result)"
                            fn_result_type = "(usize, " + packet.get_rust_type_name(skip=-2) + "Result)"
                    if not short_write:
                        if   result_count == 0:
                            fn_result = "Ok(())"
                            fn_result_type = "()"
                        elif result_count == 1:
                            first_result = next(x for x in packet.get_elements(direction='out') if x.get_level() != 'low')
                            fn_result = "Ok(ll_result.1." + first_result.get_rust_name() + ")"
                            fn_result_type = first_result.get_rust_type()
                        else:
                            fn_result = "Ok(ll_result.1)"
                            fn_result_type = packet.get_rust_type_name(skip=-2) + "Result"

                    functions.append(stream_in_getter_template.format(name=name,
                                                     description= packet.get_rust_formatted_doc(),
                                                     params=(", " + params) if len(params) > 0 else "",                                                     
                                                     result_type = fn_result_type,
                                                     high_level_function_idx = high_level_function_counter,
                                                     stream_data = stream.get_name().under,
                                                     stream_size = abs(stream.get_data_element().get_cardinality()),
                                                     chunk_size = stream.get_chunk_data_element().get_cardinality(),
                                                     chunk_type = stream.get_chunk_data_element().get_rust_type(ignore_cardinality=True),
                                                     unused_length = "" if have_length else "_",
                                                     unused_chunk_offset = "" if have_chunk_offset else "_",
                                                     low_level_function = packet.get_name().under,
                                                     low_level_params = ", ".join(low_level_params),
                                                     short_write_result = fn_result))
                else:
                    functions.append(stream_in_setter_template.format(name=name,
                                                     description= packet.get_rust_formatted_doc(),
                                                     params=(", " + params) if len(params) > 0 else "",
                                                     high_level_function_idx = high_level_function_counter,
                                                     stream_data = stream.get_name().under,
                                                     stream_size = abs(stream.get_data_element().get_cardinality()),
                                                     chunk_size = stream.get_chunk_data_element().get_cardinality(),
                                                     chunk_type = stream.get_chunk_data_element().get_rust_type(ignore_cardinality=True),
                                                     unused_length = "" if have_length else "_",
                                                     unused_chunk_offset = "" if have_chunk_offset else "_",
                                                     low_level_function = packet.get_name().under,
                                                     low_level_params = ", ".join(low_level_params)))

            if packet.get_high_level('stream_out') != None:
                assert(fn == 'get')
                high_level_function_counter += 1
                stream = packet.get_high_level('stream_out')
                name = packet.get_name(skip=-2).under
                params = ", ".join(["{name}: {type}".format(name=param.get_rust_name(), type=param.get_rust_type()) for param in packet_params if param.get_level() != 'low'])               
                
                payload_type = [elem.get_rust_type(ignore_cardinality=True) for elem in packet.get_elements(direction='out') if elem.get_level() == 'low' and elem.get_role() == 'stream_chunk_data'][0]
                result_count = self.returnTypesResultCardinality[packet]

                # Don't return structs without or with one member only.
                #  
                # scenario            return                          result_type
                #no results:          ""                              ""
                #one results:         , ll_result.1.0                 , type of first item of ...result
                #two or more results: , ll_result.1                   , ...result            
                if   result_count == 0:
                    fn_result = ""
                    fn_result_type = ""
                elif result_count == 1:
                    first_result = next(x for x in packet.get_elements(direction='out') if x.get_level() != 'low')
                    fn_result = ", ll_result.1." + first_result.get_rust_name()
                    fn_result_type = ", " + first_result.get_rust_type()
                else:
                    fn_result = ", ll_result.1"
                    fn_result_type = ", " + packet.get_rust_type_name(skip=-2) + "Result"

                low_level_params = []                
                for param in packet_params:
                    if param.get_level() != 'low':
                        low_level_params.append(param.get_rust_name())
                    else:
                       print("Unexpected low level parameter in stream_out-getter!")
                functions.append(stream_out_getter_template.format(name=name,
                                                                   description= packet.get_rust_formatted_doc(),
                                                                   params=(", " + params) if len(params) > 0 else "",
                                                                   payload_type=payload_type,
                                                                   #result_type = packet.get_rust_type_name(skip=-2) + "Result",
                                                                   result_type = fn_result_type,
                                                                   result = fn_result,
                                                                   open_parenthesis = "" if result_count == 0 else "(",
                                                                   close_parenthesis = "" if result_count == 0 else ")",
                                                                   high_level_function_idx = high_level_function_counter,
                                                                   low_level_function = packet.get_name().under,
                                                                   low_level_params = ", ".join(low_level_params)))
        
        return template.format(name=self.get_rust_name(),
                               device_identifier = self.get_device_identifier(),
                               device_display_name = self.get_long_display_name(),
                               name_under = self.get_name().under + "_" + self.get_category().under,
                                name_camel = self.get_rust_name(),
                               apiVersion = str(self.get_api_version()),
                               high_level_function_count = high_level_function_count,
                               response_expected_config="\n\t\t".join(resp_expct_config),
                               function= self.get_rust_name() + "Function",
                               functions="\n\n\t".join(functions))
    
    def get_rust_source(self):
        return "\n".join([
            self.get_rust_imports(),
            self.get_rust_constants(),
            self.get_rust_structs_and_trait_impls(),
            self.get_rust_device_definition(),
            self.get_rust_device_implementation()
        ])

class RustBindingsPacket(rust_common.RustPacket):
    def get_rust_derive_string(self, high_level_only=False):
        return "#[derive({traits})]".format(traits=", ".join(self.get_rust_derivable_traits(high_level_only)))

class RustBindingsGenerator(common.BindingsGenerator):
    def get_bindings_name(self):
        return 'rust'

    def get_bindings_display_name(self):
        return 'Rust'

    def get_device_class(self):
        return RustBindingsDevice

    def get_packet_class(self):
        return RustBindingsPacket

    def get_element_class(self):
        return rust_common.RustElement

    def generate(self, device):
        filename = '{0}_{1}'.format(device.get_name().under, device.get_category().under)

        with open(os.path.join(self.get_bindings_dir(), filename + '.rs'), 'w') as f:
            f.write(device.get_rust_source())

        if device.is_released():
            self.released_files.append(filename + '.rs')

    def write_byte_converter(self):
        with open(os.path.join(self.get_bindings_dir(), '..', 'byte_converter_template.rs'), 'r') as f: 
            primitive_type_impl = f.read()
        array_impl = []
        one_byte_template = """impl ToBytes for [u8; {count}] {{
    fn to_le_bytes(arr: [u8; {count}]) -> Vec<u8> {{
        arr.to_vec()
    }}
}}

impl FromByteSlice for [u8; {count}] {{
    fn from_le_bytes(bytes: &[u8]) -> [u8; {count}] {{
        let mut buf = [0u8; {count}];
        buf.copy_from_slice(bytes);
        buf
    }}
    fn bytes_expected() -> usize {{ {count} }}
}}"""
        i8_char_template = """impl ToBytes for [{type}; {count}] {{
    fn to_le_bytes(arr: [{type}; {count}]) -> Vec<u8> {{
        vec![{to_u8}]
    }}
}}

impl FromByteSlice for [{type}; {count}] {{
    fn from_le_bytes(bytes: &[u8]) -> [{type}; {count}] {{
        [{to_i8}]
    }}
    fn bytes_expected() -> usize {{ {count} }}
}}"""
        template = """impl ToBytes for [{type}; {count}] {{
    fn to_le_bytes(arr: [{type}; {count}]) -> Vec<u8> {{
        let mut buf = vec![0,{count_in_bytes}];
        LittleEndian::write_{type}_into(&arr, &mut buf);
        buf
    }}
}}

impl FromByteSlice for [{type}; {count}] {{
    fn from_le_bytes(bytes: &[u8]) -> [{type}; {count}] {{
        let mut buf = [0{type}; {count}];
        LittleEndian::read_{type}_into{unchecked}(&bytes, &mut buf);
        buf
    }}
    fn bytes_expected() -> usize {{ {count_in_bytes} }}
}}"""

        bool_template = """impl ToBytes for [bool; {count}] {{
    fn to_le_bytes(arr: [bool; {count}]) -> Vec<u8> {{
        let mut buf = vec![0u8; arr.len() / 8 + if arr.len() % 8 == 0 {{0}} else {{1}}];
        for (i, b) in arr.into_iter().enumerate() {{
            buf[i / 8] |= (*b as u8) << (i % 8);
        }}
        buf
    }}
}}

impl FromByteSlice for [bool; {count}] {{
    fn from_le_bytes(bytes: &[u8]) -> [bool; {count}] {{
        let mut result = [false; {count}];
        for (byte, elem) in bytes.into_iter().enumerate() {{            
            for i in 0..8 {{
                if byte * 8 + i >= result.len() {{
                    break;
                }}
                result[byte * 8 + i] = (*elem & 1 << i) > 0;
            }}
        }}
        result
    }}
    fn bytes_expected() -> usize {{ {size_in_bytes} }}
}}"""

        for i in range(0, 513):
            typestring = "[bool; " + str(i) + "]"
            if typestring in packet_param_types or typestring in packet_return_types:
                array_impl.append(bool_template.format(count=i, size_in_bytes=i//8 + (0 if i % 8 == 0 else 1)))

        for i in range(0,65):
            typestring = "[u8; " + str(i) + "]"
            if typestring in packet_param_types or typestring in packet_return_types:
                array_impl.append(one_byte_template.format(count=i))
        
        for i in range(0,65):
            typestring = "[i8; " + str(i) + "]"
            if typestring in packet_param_types or typestring in packet_return_types:
                array_impl.append(i8_char_template.format(type="i8", count=i, to_u8=", ".join(["arr["+str(j)+"] as u8" for j in range(0,i)]), to_i8=", ".join(["bytes["+str(j)+"] as i8" for j in range(0,i)])))
            typestring = "[char; " + str(i) + "]"
            if typestring in packet_param_types or typestring in packet_return_types:
                array_impl.append(i8_char_template.format(type="char", count=i, to_u8=", ".join(["arr["+str(j)+"] as u8" for j in range(0,i)]), to_i8=", ".join(["bytes["+str(j)+"] as char" for j in range(0,i)])))

        for (primitive_type, size_in_bytes) in [("u16", 2), ("i16", 2), ("u32", 4), ("i32", 4), ("u64", 8), ("i64", 8), ("f32", 4), ("f64", 8)]:
            for i in range(0, int(64 / size_in_bytes) + 1):
                typestring = "["+primitive_type+"; " + str(i) + "]"
                if typestring in packet_param_types or typestring in packet_return_types:
                    array_impl.append(template.format(type=primitive_type, count=i, count_in_bytes=size_in_bytes*i, unchecked=("" if "f" not in primitive_type else "_unchecked")))
        
        with open(os.path.join(self.get_bindings_dir(), '..', 'byte_converter.rs'), 'w') as f:
            f.write(primitive_type_impl)
            f.write("\n")
            f.write("\n\n".join(array_impl))

    def write_lib_rs(self):
        template = """#![forbid(unsafe_code)]
#![allow(clippy::too_many_arguments)]
#![allow(unstable_name_collisions)]
#![cfg_attr(feature = "fail-on-warnings", deny(warnings))]
#![cfg_attr(feature = "fail-on-warnings", deny(clippy::all))]
#![doc(html_root_url = "https://docs.rs/tinkerforge/0.1.0")]

//! Rust API bindings for [Tinkerforge](https://www.tinkerforge.com) bricks and bricklets.

mod bindings;
pub use crate::bindings::*;
pub mod base58;
pub mod byte_converter;
pub mod converting_callback_receiver;
pub mod converting_high_level_callback_receiver;
pub mod converting_receiver;
pub mod device;
pub mod ip_connection;
pub mod low_level_traits;
"""
        with open(os.path.join(self.get_bindings_dir(), "..", 'lib.rs'), 'w') as f:
            f.write(template)

        bindings_mod_template = """pub mod {module};"""
        decls = [bindings_mod_template.format(module=f.replace(".rs", "")) for f in self.released_files]
        with open(os.path.join(self.get_bindings_dir(), 'mod.rs'), 'w') as f:
            f.write("\n".join(decls))

    def finish(self):        
        self.write_lib_rs()
        self.write_byte_converter()
        common.BindingsGenerator.finish(self)


def generate(root_dir):
    common.generate(root_dir, 'en', RustBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
