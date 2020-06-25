#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java Examples Generator
Copyright (C) 2015-2019 Matthias Bolte <matthias@tinkerforge.com>

generate_java_examples.py: Generator for Java examples

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
from generators.java import java_common

global_line_prefix = ''

class JavaConstant(common.Constant):
    def get_java_source(self):
        template = '{device_category}{device_name}.{constant_group_name}_{constant_name}'

        return template.format(device_category=self.get_device().get_category().camel,
                               device_name=self.get_device().get_name().camel,
                               constant_group_name=self.get_constant_group().get_name().upper,
                               constant_name=self.get_name().upper)

class JavaExample(common.Example):
    def get_java_source(self):
        template = r"""import com.tinkerforge.IPConnection;
import com.tinkerforge.{device_category}{device_name_camel};{imports}{incomplete}{description}

public class Example{example_name} {{
	private static final String HOST = "localhost";
	private static final int PORT = 4223;

	// Change {dummy_uid} to the UID of your {device_name_long_display}
	private static final String UID = "{dummy_uid}";

	// Note: To make the example code cleaner we do not handle exceptions. Exceptions
	//       you might normally want to catch are described in the documentation
	public static void main(String args[]) throws Exception {{
		IPConnection ipcon = new IPConnection(); // Create IP connection
		{device_category}{device_name_camel} {device_name_initial} ={constructor_break}new {device_category}{device_name_camel}(UID, ipcon); // Create device object

		ipcon.connect(HOST, PORT); // Connect to brickd
		// Don't use device before ipcon is connected
{sources}
		System.out.println("Press key to exit"); System.in.read();{cleanups}
		ipcon.disconnect();
	}}
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
        sources = []
        cleanups = []

        for function in self.get_functions():
            imports += function.get_java_imports()
            sources.append(function.get_java_source())

        for cleanup in self.get_cleanups():
            imports += cleanup.get_java_imports()
            cleanups.append(cleanup.get_java_source())

        unique_imports = []

        for import_ in imports:
            if import_ not in unique_imports:
                unique_imports.append(import_)

        while None in sources:
            sources.remove(None)

        if len(sources) == 0:
            sources = ['\t\t// TODO: Add example code here\n']

        while None in cleanups:
            cleanups.remove(None)

        if len(self.get_device().get_name().camel) > 14:
            constructor_break = '\n\t\t  '
        else:
            constructor_break = ' '

        return template.format(incomplete=incomplete,
                               description=description,
                               example_name=self.get_name().camel,
                               device_category=self.get_device().get_category().camel,
                               device_name_camel=self.get_device().get_name().camel,
                               device_name_initial=self.get_device().get_initial_name(),
                               device_name_long_display=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               imports=common.wrap_non_empty('\n', '\n'.join(unique_imports), ''),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), '\n'),
                               constructor_break=constructor_break)

class JavaExampleArgument(common.ExampleArgument):
    def get_java_source(self):
        type_ = self.get_type()

        def helper(value):
            if type_ == 'float':
                return common.format_float(value) + 'f'
            elif type_ == 'bool':
                return str(bool(value)).lower()
            elif type_ == 'char':
                return "'{0}'".format(value.replace("'", "\\'"))
            elif type_ == 'string':
                return '"{0}"'.format(value.replace('"', '\\"'))
            elif ':bitmask:' in type_:
                value = common.make_c_like_bitmask(value)
                cast = java_common.get_java_type(type_.split(':')[0], 1, legacy=self.get_device().has_java_legacy_types())

                if cast in ['byte', 'short']:
                    return '({0})({1})'.format(cast, value)
                else:
                    return value
            elif type_.endswith(':constant'):
                return self.get_value_constant(value).get_java_source()
            else:
                cast = java_common.get_java_type(type_, 1, legacy=self.get_device().has_java_legacy_types())

                if cast in ['byte', 'short']:
                    cast = '({0})'.format(cast)
                else:
                    cast = ''

                return cast + str(value)

        value = self.get_value()

        if isinstance(value, list):
            return 'new {0}[]{{{1}}}'.format(java_common.get_java_type(self.get_type().split(':')[0], 1, legacy=self.get_device().has_java_legacy_types()), ', '.join([helper(item) for item in value]))

        return helper(value)

class JavaExampleArgumentsMixin(object):
    def get_java_arguments(self):
        return [argument.get_java_source() for argument in self.get_arguments()]

class JavaExampleParameter(common.ExampleParameter):
    def get_java_source(self):
        templateA = '{type_} {name}'
        templateB = '{type_}[] {name}'

        if self.get_cardinality() == 1:
            template = templateA
        else:
            template = templateB

        return template.format(type_=java_common.get_java_type(self.get_type().split(':')[0], 1, legacy=self.get_device().has_java_legacy_types()),
                               name=self.get_name().headless)

    def get_java_printlns(self):
        if self.get_type().split(':')[-1] == 'constant':
            if self.get_label_name() == None:
                return []

            # FIXME: need to handle multiple labels
            assert self.get_label_count() == 1

            template = '{else_}if({name} == {constant_name}) {{\n{global_line_prefix}\t\t\t\t\tSystem.out.println("{label}: {constant_title}");{comment}\n{global_line_prefix}\t\t\t\t}}'
            constant_group = self.get_constant_group()
            result = []

            for constant in constant_group.get_constants():
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              else_='\belse ' if len(result) > 0 else global_line_prefix + '\t\t\t\t',
                                              name=self.get_name().headless,
                                              label=self.get_label_name(),
                                              constant_name=constant.get_java_source(),
                                              constant_title=constant.get_name().space,
                                              comment=self.get_formatted_comment(' // {0}')))

            result = ['\r' + '\n'.join(result).replace('\n\b', ' ') + '\r']
        else:
            template = '{global_line_prefix}\t\t\t\tSystem.out.println("{label}: " + {to_binary_prefix}{name}{index}{divisor}{to_binary_suffix}{unit});{comment}'

            if self.get_label_name() == None:
                return []

            if self.get_cardinality() < 0:
                return [] # FIXME: streaming

            # FIXME: Integer.toBinaryString() doesn't support leading zeros. therefore,
            #        the result is not padded to the requested number of digits
            if ':bitmask:' in self.get_type():
                to_binary_prefix = 'Integer.toBinaryString('
                to_binary_suffix = ')'
            else:
                to_binary_prefix = ''
                to_binary_suffix = ''

            result = []

            for index in range(self.get_label_count()):
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              name=self.get_name().headless,
                                              label=self.get_label_name(index=index),
                                              index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                              divisor=self.get_formatted_divisor('/{0}'),
                                              unit=self.get_formatted_unit_name(' + " {0}"'),
                                              to_binary_prefix=to_binary_prefix,
                                              to_binary_suffix=to_binary_suffix,
                                              comment=self.get_formatted_comment(' // {0}')))

        return result

class JavaExampleResult(common.ExampleResult):
    def get_java_variable(self):
        template = '{type_} {name}'
        name = self.get_name().headless

        if name == self.get_device().get_initial_name():
            name += '_'

        return template.format(type_=java_common.get_java_type(self.get_type().split(':')[0], self.get_cardinality(), legacy=self.get_device().has_java_legacy_types()),
                               name=name)

    def get_java_printlns(self):
        if self.get_type().split(':')[-1] == 'constant':
            # FIXME: need to handle multiple labels
            assert self.get_label_count() == 1

            template = '{else_}if({object_prefix}{name} == {constant_name}) {{\n{global_line_prefix}\t\t\tSystem.out.println("{label}: {constant_title}");{comment}\n{global_line_prefix}\t\t}}'
            constant_group = self.get_constant_group()
            name = self.get_name().headless

            if len(self.get_function().get_results()) > 1:
                object_prefix = self.get_function().get_name(skip=1).headless + '.'
            else:
                if name == self.get_device().get_initial_name():
                    name += '_'

                object_prefix = ''

            result = []

            for constant in constant_group.get_constants():
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              else_='\belse ' if len(result) > 0 else global_line_prefix + '\t\t',
                                              object_prefix=object_prefix,
                                              name=self.get_name().headless,
                                              label=self.get_label_name(),
                                              constant_name=constant.get_java_source(),
                                              constant_title=constant.get_name().space,
                                              comment=self.get_formatted_comment(' // {0}')))

            result = ['\r' + '\n'.join(result).replace('\n\b', ' ') + '\r']
        else:
            template = '{global_line_prefix}\t\tSystem.out.println("{label}: " + {to_binary_prefix}{object_prefix}{name}{index}{divisor}{to_binary_suffix}{unit});{comment}'

            if self.get_label_name() == None:
                return []

            if self.get_cardinality() < 0:
                return [] # FIXME: streaming

            name = self.get_name().headless

            if len(self.get_function().get_results()) > 1:
                object_prefix = self.get_function().get_name(skip=1).headless + '.'
            else:
                if name == self.get_device().get_initial_name():
                    name += '_'

                object_prefix = ''

            # FIXME: Integer.toBinaryString() doesn't support leading zeros. therefore,
            #        the result is not padded to the requested number of digits
            if ':bitmask:' in self.get_type():
                to_binary_prefix = 'Integer.toBinaryString('
                to_binary_suffix = ')'
            else:
                to_binary_prefix = ''
                to_binary_suffix = ''

            result = []

            for index in range(self.get_label_count()):
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              object_prefix=object_prefix,
                                              name=name,
                                              label=self.get_label_name(index=index),
                                              index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                              divisor=self.get_formatted_divisor('/{0}'),
                                              unit=self.get_formatted_unit_name(' + " {0}"'),
                                              to_binary_prefix=to_binary_prefix,
                                              to_binary_suffix=to_binary_suffix,
                                              comment=self.get_formatted_comment(' // {0}')))

        return result

class JavaExampleGetterFunction(common.ExampleGetterFunction, JavaExampleArgumentsMixin):
    def get_java_imports(self):
        template = 'import com.tinkerforge.{device_category}{device_name}.{object_name};'

        if len(self.get_results()) > 1:
            return [template.format(device_category=self.get_device().get_category().camel,
                                    device_name=self.get_device().get_name().camel,
                                    object_name=self.get_name(skip=1).camel)]
        else:
            return []

    def get_java_source(self):
        template = r"""{global_line_prefix}		// Get current {function_name_comment}
{global_line_prefix}		{variable} = {device_name}.{function_name_headless}({arguments}); // Can throw com.tinkerforge.TimeoutException
{printlns}
"""
        variables = []
        printlns = []

        for result in self.get_results():
            variables.append(result.get_java_variable())
            printlns += result.get_java_printlns()

        if len(variables) > 1:
            variable = '{0} {1}'.format(self.get_name(skip=1).camel, self.get_name(skip=1).headless)
        else:
            variable = variables[0]

        while None in printlns:
            printlns.remove(None)

        if len(printlns) > 1:
            printlns.insert(0, '\b')

        return template.format(global_line_prefix=global_line_prefix,
                               device_name=self.get_device().get_initial_name(),
                               function_name_headless=self.get_name().headless,
                               function_name_comment=self.get_comment_name(),
                               variable=variable,
                               printlns='\n'.join(printlns).replace('\b\n\r', '\n').replace('\b', '').replace('\r\n\r', '\n\n').rstrip('\r').replace('\r', '\n'),
                               arguments=', '.join(self.get_java_arguments()))

class JavaExampleSetterFunction(common.ExampleSetterFunction, JavaExampleArgumentsMixin):
    def get_java_imports(self):
        return []

    def get_java_source(self):
        template = '{comment1}{global_line_prefix}\t\t{device_name}.{function_name}({arguments});{comment2}\n'

        result = template.format(global_line_prefix=global_line_prefix,
                                 device_name=self.get_device().get_initial_name(),
                                 function_name=self.get_name().headless,
                                 arguments=',<BP>'.join(self.get_java_arguments()),
                                 comment1=self.get_formatted_comment1(global_line_prefix + '\t\t// {0}\n', '\r', '\n' + global_line_prefix + '\t\t// '),
                                 comment2=self.get_formatted_comment2(' // {0}', ''))

        return common.break_string(result, '{}('.format(self.get_name().headless))

class JavaExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_java_imports(self):
        return []

    def get_java_source(self):
        template1A = r"""		// Add {function_name_comment} listener
"""
        template1B = r"""{override_comment}
"""
        template2 = r"""		{device_name_initial}.add{function_name_camel}Listener(new {device_category}{device_name_camel}.{function_name_camel}Listener() {{
			public void {function_name_headless}({parameters}) {{
{printlns}{extra_message}
			}}
		}});
"""
        override_comment = self.get_formatted_override_comment('\t\t// {0}', None, '\n\t\t// ')

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B

        parameters = []
        printlns = []

        for parameter in self.get_parameters():
            parameters.append(parameter.get_java_source())
            printlns += parameter.get_java_printlns()

        while None in printlns:
            printlns.remove(None)

        if len(printlns) > 1:
            printlns.append('\t\t\t\tSystem.out.println("");')

        extra_message = self.get_formatted_extra_message('\t\t\t\tSystem.out.println("{0}");')

        if len(extra_message) > 0 and len(printlns) > 0:
            extra_message = '\n' + extra_message

        result = template1.format(function_name_comment=self.get_comment_name(),
                                  override_comment=override_comment) + \
                 template2.format(device_category=self.get_device().get_category().camel,
                                  device_name_camel=self.get_device().get_name().camel,
                                  device_name_initial=self.get_device().get_initial_name(),
                                  function_name_camel=self.get_name().camel,
                                  function_name_headless=self.get_name().headless,
                                  parameters=',<BP>'.join(parameters),
                                  printlns='\n'.join(printlns).replace('\r\n\r', '\n\n').strip('\r').replace('\r', '\n'),
                                  extra_message=extra_message)

        return common.break_string(result, '{}('.format(self.get_name().headless))

class JavaExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction, JavaExampleArgumentsMixin):
    def get_java_imports(self):
        return []

    def get_java_source(self):
        templateA = r"""		// Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
		{device_name}.set{function_name_camel}Period({arguments}{period_msec});
"""
        templateB = r"""		// Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
		// Note: The {function_name_comment} callback is only called every {period_sec_long}
		//       if the {function_name_comment} has changed since the last call!
		{device_name}.set{function_name_camel}CallbackPeriod({arguments}{period_msec});
"""

        if self.get_device().get_name().space.startswith('IMU'):
            template = templateA # FIXME: special hack for IMU Brick (2.0) callback behavior and name mismatch
        else:
            template = templateB

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_name=self.get_device().get_initial_name(),
                               function_name_camel=self.get_name().camel,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_java_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class JavaExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_java_source(self):
        template = '{minimum},<BP>{maximum}'
        minimum = self.get_formatted_minimum()
        maximum = self.get_formatted_maximum()
        cast = java_common.get_java_type(self.get_type(), 1, legacy=self.get_device().has_java_legacy_types())

        if cast in ['byte', 'short']:
            cast = '({0})'.format(cast)

            if minimum.isdigit():
                minimum = cast + minimum
            else:
                minimum = '{0}({1})'.format(cast, minimum)

            if maximum.isdigit():
                maximum = cast + maximum
            else:
                maximum = '{0}({1})'.format(cast, maximum)

        return template.format(minimum=minimum,
                               maximum=maximum)

class JavaExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction, JavaExampleArgumentsMixin):
    def get_java_imports(self):
        return []

    def get_java_source(self):
        template = r"""		// Configure threshold for {function_name_comment} "{option_comment}"
		{device_name}.set{function_name_camel}CallbackThreshold({arguments}'{option_char}',<BP>{minimum_maximums});
"""
        minimum_maximums = []

        for minimum_maximum in self.get_minimum_maximums():
            minimum_maximums.append(minimum_maximum.get_java_source())

        result = template.format(device_name=self.get_device().get_initial_name(),
                                 function_name_camel=self.get_name().camel,
                                 function_name_comment=self.get_comment_name(),
                                 arguments=common.wrap_non_empty('', ',<BP>'.join(self.get_java_arguments()), ',<BP>'),
                                 option_char=self.get_option_char(),
                                 option_comment=self.get_option_comment(),
                                 minimum_maximums=',<BP>'.join(minimum_maximums))

        return common.break_string(result, 'CallbackThreshold(')

class JavaExampleCallbackConfigurationFunction(common.ExampleCallbackConfigurationFunction, JavaExampleArgumentsMixin):
    def get_java_imports(self):
        return []

    def get_java_source(self):
        templateA = r"""		// Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
		{device_name}.set{function_name_camel}CallbackConfiguration({arguments}{period_msec}{value_has_to_change});
"""
        templateB = r"""		// Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms) without a threshold
		{device_name}.set{function_name_camel}CallbackConfiguration({arguments}{period_msec}{value_has_to_change},<BP>'{option_char}', {minimum_maximums});
"""
        templateC = r"""		// Configure threshold for {function_name_comment} "{option_comment}"
		// with a debounce period of {period_sec_short} ({period_msec}ms)
		{device_name}.set{function_name_camel}CallbackConfiguration({arguments}{period_msec}{value_has_to_change},<BP>'{option_char}', {minimum_maximums});
"""

        if self.get_option_char() == None:
            template = templateA
        elif self.get_option_char() == 'x':
            template = templateB
        else:
            template = templateC

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        minimum_maximums = []

        for minimum_maximum in self.get_minimum_maximums():
            minimum_maximums.append(minimum_maximum.get_java_source())

        result = template.format(device_name=self.get_device().get_initial_name(),
                                 function_name_camel=self.get_name().camel,
                                 function_name_comment=self.get_comment_name(),
                                 arguments=common.wrap_non_empty('', ',<BP>'.join(self.get_java_arguments()), ',<BP>'),
                                 period_msec=period_msec,
                                 period_sec_short=period_sec_short,
                                 period_sec_long=period_sec_long,
                                 value_has_to_change=common.wrap_non_empty(', ', self.get_value_has_to_change('true', 'false', ''), ''),
                                 option_char=self.get_option_char(),
                                 option_comment=self.get_option_comment(),
                                 minimum_maximums=',<BP>'.join(minimum_maximums))

        return common.break_string(result, 'CallbackConfiguration(')

class JavaExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_java_imports(self):
        return []

    def get_java_source(self):
        global global_line_prefix

        type_ = self.get_type()

        if type_ == 'empty':
            return ''
        elif type_ == 'debounce_period':
            template = r"""		// Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms)
		{device_name_initial}.setDebouncePeriod({period_msec});
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_name_initial=self.get_device().get_initial_name(),
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type_ == 'sleep':
            template = '{comment1}{global_line_prefix}\t\tThread.sleep({duration});{comment2}\n'

            return template.format(global_line_prefix=global_line_prefix,
                                   duration=self.get_sleep_duration(),
                                   comment1=self.get_formatted_sleep_comment1(global_line_prefix + '\t\t// {0}\n', '\r', '\n' + global_line_prefix + '\t\t// '),
                                   comment2=self.get_formatted_sleep_comment2(' // {0}', ''))
        elif type_ == 'wait':
            return None
        elif type_ == 'loop_header':
            template = '{comment}\t\tfor(int i = 0; i < {limit}; i++) {{\n'
            global_line_prefix = '\t'

            return template.format(limit=self.get_loop_header_limit(),
                                   comment=self.get_formatted_loop_header_comment('\t\t// {0}\n', '', '\n\t\t// '))
        elif type_ == 'loop_footer':
            global_line_prefix = ''

            return '\r\t\t}\n'

class JavaExamplesGenerator(java_common.JavaGeneratorTrait, common.ExamplesGenerator):
    def get_device_class(self):
        return java_common.JavaDevice

    def get_constant_class(self):
        return JavaConstant

    def get_example_class(self):
        return JavaExample

    def get_example_argument_class(self):
        return JavaExampleArgument

    def get_example_parameter_class(self):
        return JavaExampleParameter

    def get_example_result_class(self):
        return JavaExampleResult

    def get_example_getter_function_class(self):
        return JavaExampleGetterFunction

    def get_example_setter_function_class(self):
        return JavaExampleSetterFunction

    def get_example_callback_function_class(self):
        return JavaExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return JavaExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return JavaExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return JavaExampleCallbackThresholdFunction

    def get_example_callback_configuration_function_class(self):
        return JavaExampleCallbackConfigurationFunction

    def get_example_special_function_class(self):
        return JavaExampleSpecialFunction

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
            filename = 'Example{0}.java'.format(example.get_name().camel)
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
                f.write(example.get_java_source())

def generate(root_dir):
    common.generate(root_dir, 'en', JavaExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
