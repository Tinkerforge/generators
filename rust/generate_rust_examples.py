#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Rust Examples Generator
Copyright (C) 2018 Erik Fleckstein <erik@tinkerforge.com>

generate_rust_examples.py: Generator for Rust examples

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
import rust_common
import subprocess

global_line_prefix = ''

class RustConstant(common.Constant):
    def get_rust_source(self):
        template = '{device_name}_{device_category}_{constant_group_name}_{constant_name}'

        return template.format(device_category=self.get_device().get_category().upper,
                               device_name=self.get_device().get_name().upper,
                               constant_group_name=self.get_constant_group().get_name().upper,
                               constant_name=self.get_name().upper)

class RustExample(common.Example):
    def get_rust_source(self):
        template = r"""use std::{{io, error::Error}};
{imports}
use tinkerforge::{{ip_connection::IpConnection, 
                  {device_name_under}_{device_category_under}::*}};
{incomplete}{description}

const HOST: &str = "localhost";
const PORT: u16 = 4223;
const UID: &str = "{dummy_uid}"; // Change {dummy_uid} to the UID of your {device_name_long_display}.
{functions}
fn main() -> Result<(), Box<dyn Error>> {{
    let ipcon = IpConnection::new(); // Create IP connection.
    let {device_name_initials} = {device_name_camel}{device_category_camel}::new(UID, &ipcon); // Create device object.

    ipcon.connect((HOST, PORT)).recv()??; // Connect to brickd.
    // Don't use device before ipcon is connected.
{sources}
    println!("Press enter to exit.");
    let mut _input = String::new();
    io::stdin().read_line(&mut _input)?;{cleanups}
    ipcon.disconnect();
    Ok(())
}}
"""
        if self.is_incomplete():
            incomplete = '\n\n// FIXME: This example is incomplete'
        else:
            incomplete = ''

        if self.get_description() != None:
            description = '\n\n// {0}'.format(self.get_description().replace('\n', '\n// '))
        else:
            description = ''

        imports = []
        functions = []
        sources = []
        cleanups = []

        for function in self.get_functions():
            imports += function.get_rust_imports()
            functions.append(function.get_rust_function())
            sources.append(function.get_rust_source())

        for cleanup in self.get_cleanups():
            imports += function.get_rust_imports()
            functions.append(cleanup.get_rust_function())
            cleanups.append(cleanup.get_rust_source())

        unique_imports = []

        for import_ in imports:
            if import_ not in unique_imports:
                unique_imports.append(import_)

        while None in functions:
            functions.remove(None)

        while None in sources:
            sources.remove(None)

        if len(sources) == 0:
            sources = ['\t// TODO: Add example code here.\n']

        while None in cleanups:
            cleanups.remove(None)

        if len(self.get_device().get_name().camel_abbrv) > 14:
            constructor_break = '\n\t\t  '
        else:
            constructor_break = ' '

        return template.format(incomplete=incomplete,
                               description=description,
                               device_category_under=self.get_device().get_category().under,
                               device_category_camel=self.get_device().get_category().camel_abbrv,
                               device_name_under=self.get_device().get_name().under,
                               device_name_camel=self.get_device().get_name().camel_abbrv,                               
                               device_name_initials=self.get_device().get_initial_name(),
                               device_name_long_display=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               imports='\n'.join(unique_imports),
                               functions=common.wrap_non_empty('\n', '\n'.join(functions), ''),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), ''),
                               constructor_break=constructor_break)

class RustExampleArgument(common.ExampleArgument):
    def get_rust_source(self):
        type_ = self.get_type()

        def helper(value):
            if type_ == 'bool':
                if value:
                    return 'true'
                else:
                    return 'false'
            elif type_ == 'char':
                return "'{0}'".format(value)
            elif type_ == 'string':
                return '"{0}".to_string()'.format(value)
            elif ':bitmask:' in type_:
                return common.make_c_like_bitmask(value)
            elif type_.endswith(':constant'):
                return self.get_value_constant(value).get_rust_source()
            else:
                return str(value)

        value = self.get_value()

        if isinstance(value, list):            
            fn = self.get_function()
            packets_of_function = [packet for packet in self.get_device().get_packets()  
                                            if (packet.get_name().under == fn.get_name().under) # compare name directly
                                            or (len(packet.get_name().under.split("_")) > 2 and packet.get_name(skip=-2).under == fn.get_name().under)] # or try without "low level"
            assert len(packets_of_function) == 1, "Found not exactly one packet in device %s for function %s. Maybe the example's configuration is wrong? (Found %d packets)" % (self.get_device().get_name().under, fn.get_name().under, len(packets_of_function))
            has_high_level = packets_of_function[0].has_high_level()
            if has_high_level:
                return '&[{}]'.format(', '.join([helper(item) for item in value]))
            else:
                return '[{}]'.format(', '.join([helper(item) for item in value]))

        return helper(value)

class RustExampleArgumentsMixin(object):
    def get_rust_arguments(self):
        return [argument.get_rust_source() for argument in self.get_arguments()]

class RustExampleParameter(common.ExampleParameter):
    def get_rust_source(self):
        templateA = '{name}: {type_}'
        templateB = '{name}: &[{type_}]'

        if self.get_cardinality() == 1:
            template = templateA
        else:
            template = templateB

        return template.format(type_=rust_common.get_rust_type(self.get_type().split(':')[0], 1),
                               name=self.get_name().under)

    def get_rust_write_lines(self, parameter_struct_name='', override_parameter_name=''):
        name = self.get_name().under
        if parameter_struct_name is not '':
            name = parameter_struct_name + "." + name
        if override_parameter_name is not '':
            name = override_parameter_name
        if self.get_type().split(':')[-1] == 'constant':
            if self.get_label_name() == None:
                return []
                
            # FIXME: need to handle multiple labels
            assert self.get_label_count() == 1

            template = '{global_line_prefix}\t\t{else_}if {name} == {constant_name} {{ \n{global_line_prefix}\t\t\tprintln!("{label}: {constant_title}");{comment}\n{global_line_prefix}\t\t}}'
            constant_group = self.get_constant_group()
            result = []

            for constant in constant_group.get_constants():
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              else_='else ' if len(result) > 0 else '',
                                              name=name,
                                              label=self.get_label_name(),
                                              constant_name=constant.get_rust_source(),
                                              constant_title=constant.get_name().space,
                                              comment=self.get_formatted_comment(' // {0}')))

            result = ['\r' + '\n'.join(result) + '\r']
        else:
            non_array_template = '{global_line_prefix}\t\tprintln!("{label}: {{{colon}{binary}}}{unit_param}", {name}{index}{divisor});{comment}'
            array_template = '{global_line_prefix}\t\tfor item in {name}.iter() {{println!("{label}: {{{colon}{binary}}}{unit_param}", item{index}{divisor});}}{comment}'

            if self.get_label_name() == None:
                return []

            if self.get_cardinality() < 0:
                return [] # FIXME: streaming

            if self.get_cardinality() > 1 and "string" not in self.get_type() and self.get_label_count() <= 1:
                template = array_template
            else:
                template = non_array_template

            colon = ''

            if ':bitmask:' in self.get_type():
                binary = 'b'
                colon = ':'
            else:
                binary =  ''

            result = []

            unit_param = self.get_formatted_unit_name(' {0}')

            for index in range(self.get_label_count()):
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              name=name,
                                              label=self.get_label_name(index=index),
                                              colon=colon,
                                              binary=binary,
                                              index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                              divisor=self.get_formatted_divisor(' as f32 /{0}'),
                                              unit_param=unit_param,
                                              comment=self.get_formatted_comment(' // {0}')))

        return result

class RustExampleResult(common.ExampleResult):
    def get_rust_variable_declaration(self):
        name = self.get_name().headless

        type_ = rust_common.get_rust_type(self.get_type().split(':')[0], 1)

        if self.get_cardinality() > 1:
            type_ += '[]'

        return type_, name

    def get_rust_variable_reference(self):
        template = 'out {name}'
        name = self.get_name().headless

        return template.format(name=name)

    def get_rust_write_lines(self):
        #name = self.get_name().under
        name = self.get_function().get_rust_result_prefix()
        if len(self.get_function().get_results()) > 1:
            #name = self.get_function().get_name().under + "_result." + name
            name += "." + self.get_name().under

        if self.get_type().split(':')[-1] == 'constant':
            # FIXME: need to handle multiple labels
            assert self.get_label_count() == 1

            template = '{global_line_prefix}\t\t{else_}if {name} == {constant_name} {{\n\t\t\tprintln!("{label}: {constant_title}");{comment}\n{global_line_prefix}\t\t}}'
            constant_group = self.get_constant_group()
            result = []

            for constant in constant_group.get_constants():
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              else_='else ' if len(result) > 0 else '',
                                              name=name,
                                              label=self.get_label_name(),
                                              constant_name=constant.get_rust_source(),
                                              constant_title=constant.get_name().space,
                                              comment=self.get_formatted_comment(' // {0}')))

            result = ['\r' + '\n'.join(result) + '\r']
        else:
            template = '{global_line_prefix}\t\tprintln!("{label}: {{{colon}{binary}}}{unit_param}", {name}{index}{divisor});{comment}'

            if self.get_label_name() == None:
                return []

            if self.get_cardinality() < 0:
                return [] # FIXME: streaming

            colon = ''

            if ':bitmask:' in self.get_type():
                binary = 'b'
                colon = ':'
            else:
                binary =  ''

            result = []

            unit_param = self.get_formatted_unit_name(' {0}')

            for index in range(self.get_label_count()):
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              name=name,
                                              label=self.get_label_name(index=index),
                                              colon=colon,
                                              binary=binary,
                                              unit_param=unit_param,
                                              index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                              divisor=self.get_formatted_divisor(' as f32 /{0}'),                                              
                                              comment=self.get_formatted_comment(' // {0}')))

        return result

class RustExampleGetterFunction(common.ExampleGetterFunction, RustExampleArgumentsMixin):
    def get_rust_imports(self):
        return []

    def get_rust_function(self):
        return None

    def get_rust_result_prefix(self):
        if len(self.get_results()) > 1:
            if self.get_name().under.startswith("is_") or self.get_name().under.startswith("get_"):
                return self.get_name(skip=1).under
            return self.get_name().under+"_result"
        else:
            return self.get_results()[0].get_name().under

    def get_rust_source(self):        
        template = r"""{global_line_prefix}		// Get current {function_name_comment}.
{global_line_prefix}let {result_name} = {device_name_initials}.{function_name_under}({arguments}).recv()?;
{write_lines}
"""
        result_name = self.get_rust_result_prefix()

        #returns_struct = len(self.get_results()) > 1
        #if returns_struct:
        #    result_name = self.get_name().under+"_result"
        #else:
        #    result_name = self.get_results()[0].get_name().under
        
        write_lines = []
        for result in self.get_results():
            write_lines += result.get_rust_write_lines()

        while None in write_lines:
            write_lines.remove(None)

        if len(write_lines) > 1:
            write_lines.insert(0, '\b')

        arguments = self.get_rust_arguments()

        result = template.format(device_name_under=self.get_device().get_name().under,
                                 device_name_initials=self.get_device().get_initial_name(),
                                 device_category_under = self.get_device().get_category().under,
                                 result_name = result_name,                                 
                                 function_name_under=self.get_name().under,
                                 function_name_comment=self.get_comment_name(),                                 
                                 write_lines='\n'.join(write_lines).replace('\b\n\r', '\n').replace('\b', '').replace('\r\n\r', '\n\n').rstrip('\r').replace('\r', '\n'),
                                 arguments=',<BP>'.join(arguments),
                                 global_line_prefix=global_line_prefix)

        return common.break_string(result, '{}('.format(self.get_name().camel_abbrv))

class RustExampleSetterFunction(common.ExampleSetterFunction, RustExampleArgumentsMixin):
    def get_rust_imports(self):
        return []

    def get_rust_function(self):
        return None

    def get_rust_source(self):
        template = '{comment1}{global_line_prefix}\t\t{device_name_initials}.{function_name}({arguments});{comment2}\n'

        result = template.format(global_line_prefix=global_line_prefix,
                                 device_name_under=self.get_device().get_name().under,
                                 device_name_initials=self.get_device().get_initial_name(),
                                 device_category_under = self.get_device().get_category().under,
                                 function_name=self.get_name().under,
                                 arguments=',<BP>'.join(self.get_rust_arguments()),
                                 comment1=self.get_formatted_comment1(global_line_prefix + '\t\t// {0}\n', '\r', '\n' + global_line_prefix + '\t\t// '),
                                 comment2=self.get_formatted_comment2(' // {0}', ''))

        return common.break_string(result, '{}('.format(self.get_name().camel_abbrv))

class RustExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_rust_imports(self):
        return ["use std::thread;"]

    def get_rust_function(self):
        return ""

    def get_rust_source(self):
        #TODO: high level callback receivers send Option<Result>, so we need to match them here. OTOH streaming examples are incomplete anyway, so this can be done manually.
        template = r"""     let {function_name_under}_receiver = {device_name_initials}.get_{function_name_under}_callback_receiver();

        // Spawn thread to handle received callback messages. 
        // This thread ends when the `{device_name_initials}` object
        // is dropped, so there is no need for manual cleanup.
        thread::spawn(move || {{
            for {function_name_under} in {function_name_under}_receiver {{{match_expr}           
                {write_lines}{extra_message}
            {match_expr_end}}}
        }});
"""
        write_lines = []
        has_high_level = [packet for packet in self.get_device().get_packets(type_='callback') if (packet.get_name().under == self.get_name().under) or (len(packet.get_name().under.split("_")) > 2 and packet.get_name(skip=-2).under == self.get_name().under)][0].has_high_level()

        if has_high_level:
            match_expr = "match {function_name_under} {{\nSome((payload, result)) => {{\n".format(function_name_under = self.get_name().under)
            match_expr_end = '}\nNone => println!("Stream was out of sync.")\n}'
        else:
            match_expr = ""
            match_expr_end = ""

        if len(self.get_parameters()) > 1:
            for parameter in self.get_parameters():
                write_lines += parameter.get_rust_write_lines(parameter_struct_name=self.get_name().under if not has_high_level else "result")
        else:
            for parameter in self.get_parameters():
                write_lines += parameter.get_rust_write_lines(override_parameter_name=self.get_name().under if not has_high_level else "result")

        while None in write_lines:
            write_lines.remove(None)

        if len(write_lines) > 1:
            write_lines.append('\t\tprintln!();')

        extra_message = self.get_formatted_extra_message('\t\tprintln!("{0}");')

        if len(extra_message) > 0 and len(write_lines) > 0:
            extra_message = '\n' + extra_message

        result = template.format(match_expr = match_expr, 
                                 match_expr_end = match_expr_end,
                                 device_name_under=self.get_device().get_name().under,
                                 device_name_initials=self.get_device().get_initial_name(),
                                 device_category_under=self.get_device().get_category().under,
                                 function_name_under=self.get_name().under,
                                 function_name_comment=self.get_comment_name(),
                                 write_lines='\n'.join(write_lines).replace('\r\n\r', '\n\n').strip('\r').replace('\r', '\n'),
                                 extra_message=extra_message)

        return common.break_string(result, '// ', indent_tail='// ')

class RustExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction, RustExampleArgumentsMixin):
    def get_rust_imports(self):
        return ["use std::thread;"]

    def get_rust_function(self):
        return None

    def get_rust_source(self):
        templateA = r"""		// Set period for {function_name_comment} receiver to {period_sec_short} ({period_msec}ms).
		{device_name_initials}.set_{function_name_under}_period({arguments}{period_msec});
"""
        templateB = r"""		// Set period for {function_name_comment} receiver to {period_sec_short} ({period_msec}ms).
		// Note: The {function_name_comment} callback is only called every {period_sec_long}
		//       if the {function_name_comment} has changed since the last call!
		{device_name_initials}.set_{function_name_under}_callback_period({arguments}{period_msec});
"""

        if self.get_device().get_name().space.startswith('IMU'):
            template = templateA # FIXME: special hack for IMU Brick (2.0) callback behavior and name mismatch
        else:
            template = templateB

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_name_under=self.get_device().get_name().under,
                               device_name_initials=self.get_device().get_initial_name(),
                               device_category_under=self.get_device().get_category().under,
                               function_name_under=self.get_name().under,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_rust_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class RustExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_rust_imports(self):
        return []

    def get_rust_source(self):
        template = '{minimum}, {maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class RustExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction, RustExampleArgumentsMixin):
    def get_rust_imports(self):
        return []

    def get_rust_function(self):
        return None

    def get_rust_source(self):
        template = r"""		// Configure threshold for {function_name_comment} "{option_comment}".
		{device_name_initials}.set_{function_name_under}_callback_threshold({arguments}'{option_char}', {minimum_maximums});
"""
        minimum_maximums = []

        for minimum_maximum in self.get_minimum_maximums():
            minimum_maximums.append(minimum_maximum.get_rust_source())

        return template.format(device_name_under=self.get_device().get_name().under,
                               device_name_initials=self.get_device().get_initial_name(),
                               device_category_under=self.get_device().get_category().under,
                               function_name_under=self.get_name().under,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_rust_arguments()), ', '),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               minimum_maximums=', '.join(minimum_maximums))

class RustExampleCallbackConfigurationFunction(common.ExampleCallbackConfigurationFunction, RustExampleArgumentsMixin):
    def get_rust_imports(self):
        return []

    def get_rust_function(self):
        return None

    def get_rust_source(self):
        templateA = r"""		// Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms).
		{device_name_initials}.set_{function_name_under}_callback_configuration({arguments}{period_msec}{value_has_to_change});
"""
        templateB = r"""		// Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms) without a threshold.
		{device_name_initials}.set_{function_name_under}_callback_configuration({arguments}{period_msec}{value_has_to_change}, '{option_char}', {minimum_maximums});
"""
        templateC = r"""		// Configure threshold for {function_name_comment} "{option_comment}"
		// with a debounce period of {period_sec_short} ({period_msec}ms).
		{device_name_initials}.set_{function_name_under}_callback_configuration({arguments}{period_msec}{value_has_to_change}, '{option_char}', {minimum_maximums});
"""

        if self.get_option_char() == None:
            template = templateA
        elif self.get_option_char() == 'x':
            template = templateB
        else:
            template = templateC

        period_msec, period_sec_short, _period_sec_long = self.get_formatted_period()

        minimum_maximums = []

        for minimum_maximum in self.get_minimum_maximums():
            minimum_maximums.append(minimum_maximum.get_rust_source())

        return template.format(device_name_under=self.get_device().get_name().under,
                               device_name_initials=self.get_device().get_initial_name(),
                               device_category_under=self.get_device().get_category().under,
                               function_name_under=self.get_name().under,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_rust_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               value_has_to_change=common.wrap_non_empty(', ', self.get_value_has_to_change('true', 'false', ''), ''),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               minimum_maximums=', '.join(minimum_maximums))

class RustExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_rust_imports(self):
        if self.get_type() == 'sleep':
            return ['use std::thread;', 'use std::time::Duration;']
        else:
            return []

    def get_rust_function(self):
        return None

    def get_rust_source(self):
        global global_line_prefix

        type_ = self.get_type()

        if type_ == 'empty':
            return ''
        elif type_ == 'debounce_period':
            template = r"""		// Get threshold receivers with a debounce time of {period_sec} ({period_msec}ms).
		{device_name_initials}.set_debounce_period({period_msec});
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_name_under=self.get_device().get_name().under,
                                   device_name_initials=self.get_device().get_initial_name(),
                                   device_category_under=self.get_device().get_category().under,
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type_ == 'sleep':
            template = '{comment1}{global_line_prefix}\t\tthread::sleep(Duration::from_millis({duration}));{comment2}\n'

            return template.format(global_line_prefix=global_line_prefix,
                                   duration=self.get_sleep_duration(),
                                   comment1=self.get_formatted_sleep_comment1(global_line_prefix + '\t\t// {0}\n', '\r', '\n' + global_line_prefix + '\t\t// '),
                                   comment2=self.get_formatted_sleep_comment2(' // {0}', ''))
        elif type_ == 'wait':
            return None
        elif type_ == 'loop_header':
            template = '{comment}\t\tfor i in 0..{limit}{{\n'
            global_line_prefix = '\t'

            return template.format(limit=self.get_loop_header_limit(),
                                   comment=self.get_formatted_loop_header_comment('\t\t// {0}\n', '', '\n\t\t// '))
        elif type_ == 'loop_footer':
            global_line_prefix = ''

            return '\r\t\t}\n'

class RustExamplesGenerator(common.ExamplesGenerator):
    def get_bindings_name(self):
        return 'rust'

    def get_constant_class(self):
        return RustConstant

    def get_example_class(self):
        return RustExample

    def get_example_argument_class(self):
        return RustExampleArgument

    def get_example_parameter_class(self):
        return RustExampleParameter

    def get_example_result_class(self):
        return RustExampleResult

    def get_example_getter_function_class(self):
        return RustExampleGetterFunction

    def get_example_setter_function_class(self):
        return RustExampleSetterFunction

    def get_example_callback_function_class(self):
        return RustExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return RustExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return RustExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return RustExampleCallbackThresholdFunction

    def get_example_callback_configuration_function_class(self):
        return RustExampleCallbackConfigurationFunction

    def get_example_special_function_class(self):
        return RustExampleSpecialFunction

    def generate(self, device):
        if os.getenv('TINKERFORGE_GENERATE_EXAMPLES_FOR_DEVICE', device.get_name().camel_abbrv) != device.get_name().camel_abbrv:
            print('  \033[01;31m- skipped\033[0m')
            return

        examples_dir = self.get_examples_dir(device)
        examples = device.get_examples()

        if len(examples) == 0:
            print('  \033[01;31m- no examples\033[0m')
            return

        if not os.path.exists(examples_dir):
            os.makedirs(examples_dir)

        for example in examples:
            filename = 'example_{0}.rs'.format(example.get_name().under)
            filepath = os.path.join(examples_dir, filename)

            if example.is_incomplete():
                if os.path.exists(filepath) and self.skip_existing_incomplete_example:
                    print('  - ' + filename + ' \033[01;35m(incomplete, skipped)\033[0m')
                    continue
                else:
                    print('  - ' + filename + ' \033[01;31m(incomplete)\033[0m')
            else:
                print('  - ' + filename)

            with open(filepath, 'w') as f:
                f.write(example.get_rust_source())
            if not example.is_incomplete():
                p = subprocess.Popen(["rustfmt", filename, "--config-path", os.getcwd()], cwd=examples_dir, stdout = subprocess.PIPE)
                out, err = p.communicate() #block until rustfmt has finished
                if out != "" or err is not None:
                    print("Got the following output from rustfmt:")
                    print(out)
                    print(err)

def generate(root_dir):
    common.generate(root_dir, 'en', RustExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
