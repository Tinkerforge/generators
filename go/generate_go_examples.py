#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Go Examples Generator
Copyright (C) 2018 Erik Fleckstein <erik@tinkerforge.com>

generate_go_examples.py: Generator for Go examples

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
import go_common
import subprocess

global_line_prefix = ''

class GoConstant(common.Constant):
    def get_go_source(self):
        template = '{device_name}_{device_category}.{constant_group_name}{constant_name}'

        return template.format(device_category=self.get_device().get_category().under,
                               device_name=self.get_device().get_name().under,
                               constant_group_name=self.get_constant_group().get_name().camel,
                               constant_name=self.get_name().camel)

class GoExample(common.Example):
    def get_go_source(self):
        template = r"""package main

import (
    "fmt"
    "github.com/tinkerforge/go-api-bindings/ipconnection"
    "github.com/tinkerforge/go-api-bindings/{dev_package}"
    {imports}
)
{incomplete}{description}

const ADDR string = "localhost:4223"
const UID string = "{dummy_uid}"  // Change {dummy_uid} to the UID of your {device_name_long_display}.
{functions}
func main() {{
    ipcon := ipconnection.New()
    defer ipcon.Close()
    {device_name_initials}, _ := {dev_package}.New(UID, &ipcon) // Create device object.

    ipcon.Connect(ADDR) // Connect to brickd.
    defer ipcon.Disconnect()
    // Don't use device before ipcon is connected.
{sources}
    fmt.Print("Press enter to exit.")
    fmt.Scanln()
    {cleanups}
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
            imports += function.get_go_imports()
            functions.append(function.get_go_function())
            sources.append(function.get_go_source())

        for cleanup in self.get_cleanups():
            imports += function.get_go_imports()
            functions.append(cleanup.get_go_function())
            cleanups.append(cleanup.get_go_source())

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

        if len(self.get_device().get_name().camel) > 14:
            constructor_break = '\n\t\t  '
        else:
            constructor_break = ' '

        return template.format(incomplete=incomplete,
                               description=description,
                               dev_package = self.get_device().get_go_package(),
                               device_category_camel=self.get_device().get_category().camel,
                               device_name_camel=self.get_device().get_name().camel,
                               device_name_initials=self.get_device().get_initial_name(),
                               device_name_long_display=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               imports='\n\t'.join(unique_imports),
                               functions=common.wrap_non_empty('\n', '\n'.join(functions), ''),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), ''),
                               constructor_break=constructor_break)

class GoExampleArgument(common.ExampleArgument):

    def get_go_source(self):
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
                return '"{0}"'.format(value)
            elif ':bitmask:' in type_:
                return common.make_c_like_bitmask(value)
            elif type_.endswith(':constant'):
                return self.get_value_constant(value).get_go_source()
            else:
                return str(value)

        value = self.get_value()
        array = self.get_element().get_cardinality() > 1 if self.get_element() is not None else False # < 0 as slice, > 1 as array
        if isinstance(value, list):            
            return '{type}{{{values}}}'.format(type=go_common.get_go_type(type_, len(value), array=array), values=', '.join([helper(item) for item in value]))
            
        return helper(value)

class GoExampleArgumentsMixin(object):
    def get_go_arguments(self):
        return [argument.get_go_source() for argument in self.get_arguments()]

class GoExampleParameter(common.ExampleParameter):
    def get_go_source(self):
        templateA = '{name} {type_}'
        templateB = '{name} []{type_}'
        templateC = '{name} [{size}]{type_}'

        if self.get_cardinality() == 1:
            template = templateA
        elif self.get_cardinality() < 0:   
            template = templateB
        else:
            template = templateC

        splt = self.get_type().split(':')
        if len(splt) > 1 and splt[1] == 'constant':
            type_ = self.get_device().get_name().under + "_" + self.get_device().get_category().under + "." + self.get_constant_group().get_name().camel
        else:
            type_ = go_common.get_go_type(self.get_type().split(':')[0], 1)

        return template.format(type_=type_,
                               name=self.get_name().headless,
                               size=self.get_cardinality())

    def get_go_write_lines(self, parameter_struct_name='', override_parameter_name=''):
        name = self.get_name().headless
        if parameter_struct_name is not '':
            name = parameter_struct_name + "." + name
        if override_parameter_name is not '':
            name = override_parameter_name
        if self.get_type().split(':')[-1] == 'constant':
            if self.get_label_name() == None:
                return []
            # FIXME: need to handle multiple labels
            assert self.get_label_count() <= 1

            template = '{global_line_prefix}{else_}if {name} == {constant_name} {{ \n{global_line_prefix}\t\t\tfmt.Println("{label}: {constant_title}");{comment}\n{global_line_prefix}\t\t}}'
            constant_group = self.get_constant_group()
            result = ""

            for constant in constant_group.get_constants():
                result += template.format(global_line_prefix=global_line_prefix,
                                              else_='else ' if len(result) > 0 else '\n',
                                              name=name,
                                              label=self.get_label_name(),
                                              constant_name=constant.get_go_source(),
                                              constant_title=constant.get_name().space,
                                              comment=self.get_formatted_comment(' // {0}'))

            result = ['\r' + result + '\r']
        else:
            non_array_template = '{global_line_prefix}\t\tfmt.Printf("{label}: {fmt}{unit_param}\\n", {float_cast}{name}{index}{float_cast_end}{divisor});{comment}'
            array_template = '{global_line_prefix}\t\tfor _, item := range {name} {{fmt.Printf("{label}: {fmt}{unit_param}\n", {float_cast}item{index}{float_cast_end}{divisor});}}{comment}'

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
                fmt = '%b'
            elif 'float' in self.get_type() or self.get_divisor() is not None:
                fmt =  '%f'
            elif 'int' in self.get_type():
                fmt = '%d'
            elif 'char' in self.get_type():
                fmt = '%c'
            else:
                fmt = '%s'


            result = []

            unit_param = self.get_formatted_unit_name(' {0}')

            for index in range(self.get_label_count()):
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              name=name,
                                              label=self.get_label_name(index=index),
                                              colon=colon,
                                              fmt=fmt,
                                              index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                              float_cast = "float64(" if self.get_divisor() is not None else "",
                                              float_cast_end = ")" if self.get_divisor() is not None else "",
                                              divisor=self.get_formatted_divisor(' /{0}'),
                                              unit_param=unit_param,
                                              comment=self.get_formatted_comment(' // {0}')))

        return result

class GoExampleResult(common.ExampleResult):
    def get_go_name(self):
        name = self.get_name().headless
        if name == self.get_device().get_initial_name():
            name += '_'
        return name


    def get_go_write_lines(self):
        name = self.get_go_name()
        
        if self.get_type().split(':')[-1] == 'constant':
            # FIXME: need to handle multiple labels
            assert self.get_label_count() == 1

            template = '{global_line_prefix}{else_}if {name} == {constant_name} {{\n\t\t\tfmt.Println("{label}: {constant_title}");{comment}\n{global_line_prefix}\t\t}}'
            constant_group = self.get_constant_group()
            result = ""

            for constant in constant_group.get_constants():
                result += template.format(global_line_prefix=global_line_prefix,
                                              else_='else ' if len(result) > 0 else '\n',
                                              name=name,
                                              label=self.get_label_name(),
                                              constant_name=constant.get_go_source(),
                                              constant_title=constant.get_name().space,
                                              comment=self.get_formatted_comment(' // {0}'))

            result = ['\r' + result + '\r']
        else:
            template = '{global_line_prefix}\t\tfmt.Printf("{label}: {format_verb}{unit_param}\\n", {float_cast}{name}{index}{float_cast_end}{divisor});{comment}'

            if self.get_label_name() == None:
                return []

            if self.get_cardinality() < 0:
                return [] # FIXME: streaming

            if ':bitmask:' in self.get_type():
                format_verb = '%b'
            else:
                format_verb =  ''

            if 'float' in self.get_type() or self.get_divisor() is not None:
                format_verb = '%f'

            result = []

            unit_param = self.get_formatted_unit_name(' {0}')

            for index in range(self.get_label_count()):
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              name=name,
                                              label=self.get_label_name(index=index),
                                              format_verb=format_verb,
                                              unit_param=unit_param,
                                              index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                              float_cast = "float64(" if self.get_divisor() is not None else "",
                                              float_cast_end = ")" if self.get_divisor() is not None else "",
                                              divisor=self.get_formatted_divisor(' /{0}'),                                              
                                              comment=self.get_formatted_comment(' // {0}')))

        return result

class GoExampleGetterFunction(common.ExampleGetterFunction, GoExampleArgumentsMixin):
    def get_go_imports(self):
        return []

    def get_go_function(self):
        return None

    def get_go_result_prefix(self):
        return ", ".join(r.get_go_name() if r.get_label_count() > 0 else "_" for r in self.get_results() )

    def get_go_source(self):        
        template = r"""{global_line_prefix}		// Get current {function_name_comment}.
{global_line_prefix}{result_name}, _ := {device_name_initials}.{function_name_camel}({arguments})
{write_lines}
"""
        result_name = self.get_go_result_prefix()
        
        write_lines = []
        for result in self.get_results():
            write_lines += result.get_go_write_lines()

        while None in write_lines:
            write_lines.remove(None)

        if len(write_lines) > 1:
            write_lines.insert(0, '\b')

        arguments = self.get_go_arguments()

        result = template.format(device_name_under=self.get_device().get_name().camel,
                                 device_name_initials=self.get_device().get_initial_name(),
                                 device_category_under = self.get_device().get_category().camel,
                                 result_name = result_name,                                 
                                 function_name_camel=self.get_name().camel,
                                 function_name_comment=self.get_comment_name(),                                 
                                 write_lines='\n'.join(write_lines).replace('\b\n\r', '\n').replace('\b', '').replace('\r\n\r', '\n\n').rstrip('\r').replace('\r', '\n'),
                                 arguments=',<BP>'.join(arguments),
                                 global_line_prefix=global_line_prefix)

        return common.break_string(result, '{}('.format(self.get_name().camel))

class GoExampleSetterFunction(common.ExampleSetterFunction, GoExampleArgumentsMixin):
    def get_go_imports(self):
        return []

    def get_go_function(self):
        return None

    def get_go_source(self):
        template = '{comment1}{global_line_prefix}\t\t{device_name_initials}.{function_name}({arguments}){comment2}\n'

        result = template.format(global_line_prefix=global_line_prefix,
                                 device_name_under=self.get_device().get_name().camel,
                                 device_name_initials=self.get_device().get_initial_name(),
                                 device_category_under = self.get_device().get_category().camel,
                                 function_name=self.get_name().camel,
                                 arguments=',<BP>'.join(self.get_go_arguments()),
                                 comment1=self.get_formatted_comment1(global_line_prefix + '\t\t// {0}\n', '\r', '\n' + global_line_prefix + '\t\t// '),
                                 comment2=self.get_formatted_comment2(' // {0}', ''))

        return common.break_string(result, '{}('.format(self.get_name().camel))

class GoExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_go_imports(self):
        return []

    def get_go_function(self):
        return ""

    def get_go_source(self):        
        template = r"""{device_name_initials}.Register{function_name_camel}Callback(func({params}) {{
        {write_lines}{extra_message}
    }})
"""
        write_lines = []
        params = []
        packet = [packet for packet in self.get_device().get_packets(type_='callback') if (packet.get_name().under == self.get_name().under) or (len(packet.get_name().under.split("_")) > 2 and packet.get_name(skip=-2).under == self.get_name().under)][0]
        
        for parameter in self.get_parameters():
            params.append(parameter.get_go_source())
            write_lines += parameter.get_go_write_lines()

        while None in write_lines:
            write_lines.remove(None)

        if len(write_lines) > 1:
            write_lines.append('\t\tfmt.Println();')

        extra_message = self.get_formatted_extra_message('\t\tfmt.Println("{0}");')

        if len(extra_message) > 0 and len(write_lines) > 0:
            extra_message = '\n' + extra_message

        result = template.format(device_name_initials=self.get_device().get_initial_name(),                                 
                                 params=", ".join(params),
                                 function_name_camel=self.get_name().camel,
                                 function_name_comment=self.get_comment_name(),
                                 write_lines='\n'.join(write_lines).replace('\r\n\r', '\n\n').strip('\r').replace('\r', '\n'),
                                 extra_message=extra_message)

        return common.break_string(result, '// ', indent_tail='// ')

class GoExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction, GoExampleArgumentsMixin):
    def get_go_imports(self):
        return []

    def get_go_function(self):
        return None

    def get_go_source(self):
        templateA = r"""		// Set period for {function_name_comment} receiver to {period_sec_short} ({period_msec}ms).
		{device_name_initials}.Set{function_name_camel}Period({arguments}{period_msec});
"""
        templateB = r"""		// Set period for {function_name_comment} receiver to {period_sec_short} ({period_msec}ms).
		// Note: The {function_name_comment} callback is only called every {period_sec_long}
		//       if the {function_name_comment} has changed since the last call!
		{device_name_initials}.Set{function_name_camel}CallbackPeriod({arguments}{period_msec});
"""

        if self.get_device().get_name().space.startswith('IMU'):
            template = templateA # FIXME: special hack for IMU Brick (2.0) callback behavior and name mismatch
        else:
            template = templateB

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_name_under=self.get_device().get_name().under,
                               device_name_initials=self.get_device().get_initial_name(),
                               device_category_under=self.get_device().get_category().under,
                               function_name_camel=self.get_name().camel,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_go_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class GoExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_go_imports(self):
        return []

    def get_go_source(self):
        template = '{minimum}, {maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class GoExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction, GoExampleArgumentsMixin):
    def get_go_imports(self):
        return []

    def get_go_function(self):
        return None

    def get_go_source(self):
        template = r"""		// Configure threshold for {function_name_comment} "{option_comment}".
		{device_name_initials}.Set{function_name_camel}CallbackThreshold({arguments}'{option_char}', {minimum_maximums});
"""
        minimum_maximums = []

        for minimum_maximum in self.get_minimum_maximums():
            minimum_maximums.append(minimum_maximum.get_go_source())

        return template.format(device_name_under=self.get_device().get_name().under,
                               device_name_initials=self.get_device().get_initial_name(),
                               device_category_under=self.get_device().get_category().under,
                               function_name_camel=self.get_name().camel,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_go_arguments()), ', '),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               minimum_maximums=', '.join(minimum_maximums))

class GoExampleCallbackConfigurationFunction(common.ExampleCallbackConfigurationFunction, GoExampleArgumentsMixin):
    def get_go_imports(self):
        return []

    def get_go_function(self):
        return None

    def get_go_source(self):
        templateA = r"""		// Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms).
		{device_name_initials}.Set{function_name_camel}CallbackConfiguration({arguments}{period_msec}{value_has_to_change});
"""
        templateB = r"""		// Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms) without a threshold.
		{device_name_initials}.Set{function_name_camel}CallbackConfiguration({arguments}{period_msec}{value_has_to_change}, '{option_char}', {minimum_maximums});
"""
        templateC = r"""		// Configure threshold for {function_name_comment} "{option_comment}"
		// with a debounce period of {period_sec_short} ({period_msec}ms).
		{device_name_initials}.Set{function_name_camel}CallbackConfiguration({arguments}{period_msec}{value_has_to_change}, '{option_char}', {minimum_maximums});
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
            minimum_maximums.append(minimum_maximum.get_go_source())

        return template.format(device_name_under=self.get_device().get_name().under,
                               device_name_initials=self.get_device().get_initial_name(),
                               device_category_under=self.get_device().get_category().under,
                               function_name_camel=self.get_name().camel,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_go_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               value_has_to_change=common.wrap_non_empty(', ', self.get_value_has_to_change('true', 'false', ''), ''),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               minimum_maximums=', '.join(minimum_maximums))

class GoExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_go_imports(self):
        if self.get_type() == 'sleep':
            return ['"time"']
        else:
            return []

    def get_go_function(self):
        return None

    def get_go_source(self):
        global global_line_prefix

        type_ = self.get_type()

        if type_ == 'empty':
            return ''
        elif type_ == 'debounce_period':
            template = r"""		// Get threshold receivers with a debounce time of {period_sec} ({period_msec}ms).
		{device_name_initials}.SetDebouncePeriod({period_msec});
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_name_initials=self.get_device().get_initial_name(),
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type_ == 'sleep':
            template = '{comment1}{global_line_prefix}\t\ttime.Sleep({duration} * time.Millisecond);{comment2}\n'

            return template.format(global_line_prefix=global_line_prefix,
                                   duration=self.get_sleep_duration(),
                                   comment1=self.get_formatted_sleep_comment1(global_line_prefix + '\t\t// {0}\n', '\r', '\n' + global_line_prefix + '\t\t// '),
                                   comment2=self.get_formatted_sleep_comment2(' // {0}', ''))
        elif type_ == 'wait':
            return None
        elif type_ == 'loop_header':
            template = '{comment}\t\tfor i := 0; i < {limit}; i++ {{\n'
            global_line_prefix = '\t'

            return template.format(limit=self.get_loop_header_limit(),
                                   comment=self.get_formatted_loop_header_comment('\t\t// {0}\n', '', '\n\t\t// '))
        elif type_ == 'loop_footer':
            global_line_prefix = ''

            return '\r\t\t}\n'

class GoExamplesGenerator(common.ExamplesGenerator):
    def get_bindings_name(self):
        return 'go'

    def get_constant_class(self):
        return GoConstant

    def get_device_class(self):
        return go_common.GoDevice

    def get_example_class(self):
        return GoExample

    def get_example_argument_class(self):
        return GoExampleArgument

    def get_example_parameter_class(self):
        return GoExampleParameter

    def get_example_result_class(self):
        return GoExampleResult

    def get_example_getter_function_class(self):
        return GoExampleGetterFunction

    def get_example_setter_function_class(self):
        return GoExampleSetterFunction

    def get_example_callback_function_class(self):
        return GoExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return GoExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return GoExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return GoExampleCallbackThresholdFunction

    def get_example_callback_configuration_function_class(self):
        return GoExampleCallbackConfigurationFunction

    def get_example_special_function_class(self):
        return GoExampleSpecialFunction

    def generate(self, device):
        if os.getenv('TINKERFORGE_GENERATE_EXAMPLES_FOR_DEVICE', device.get_name().camel) != device.get_name().camel:
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
            filename = 'example_{0}.go'.format(example.get_name().under)
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
                f.write(example.get_go_source())
            if not example.is_incomplete():
                p = subprocess.Popen(["go", "fmt", filename], cwd=examples_dir, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                out, err = p.communicate() #block unti l gofmt has finished
                if p.returncode != 0:
                    print("Got the following output from go fmt:")
                    print(out)
                    print(err)

def generate(root_dir):
    common.generate(root_dir, 'en', GoExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
