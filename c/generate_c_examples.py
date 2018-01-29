#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Examples Generator
Copyright (C) 2015-2018 Matthias Bolte <matthias@tinkerforge.com>

generate_c_examples.py: Generator for C/C++ examples

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

global_line_prefix = ''

class CTypeMixin(object):
    def get_c_type(self):
        type = self.get_type().split(':')[0]

        if 'int' in type:
            type += '_t'

        return type

class CPrintfFormatMixin(object):
    def get_c_printf_defines(self):
        if self.get_type().split(':')[0].endswith('int64'):
            return ['#define __STDC_FORMAT_MACROS // for PRId64/PRIu64 in C++']
        else:
            return []

    def get_c_printf_includes(self):
        if self.get_type().split(':')[0].endswith('int64'):
            return ['#include <inttypes.h>']
        else:
            return []

    def get_c_printf_format(self):
        type_ = self.get_type().split(':')[0]

        if type_ == 'char':
            return '%c'
        elif type_ == 'string':
            return '%s'
        elif type_ != 'float' and self.get_divisor() == None:
            if type_ == 'int64':
                return '%" PRId64 "'
            elif type_ == 'uint64':
                return '%" PRIu64 "'
            elif type_.startswith('uint'):
                return '%u'
            else:
                return '%d'
        else:
            return '%f'

    def get_c_printf_cast_suffix(self):
        if self.get_type().split(':')[0] == 'int64' and self.get_divisor() != None:
            return ')'
        else:
            return ''

class CConstant(common.Constant):
    def get_c_source(self):
        template = '{device_upper_case_name}_{constant_group_upper_case_name}_{constant_upper_case_name}'

        return template.format(device_upper_case_name=self.get_device().get_upper_case_name(),
                               constant_group_upper_case_name=self.get_constant_group().get_upper_case_name(),
                               constant_upper_case_name=self.get_upper_case_name())

class CExample(common.Example):
    def get_c_source(self):
        template = r"""{defines}#include <stdio.h>{includes}{incomplete}{description}

#include "ip_connection.h"
#include "{device_underscore_category}_{device_underscore_name}.h"

#define HOST "localhost"
#define PORT 4223
#define UID "{dummy_uid}" // Change {dummy_uid} to the UID of your {device_long_display_name}
{functions}
int main(void) {{
	// Create IP connection
	IPConnection ipcon;
	ipcon_create(&ipcon);

	// Create device object
	{device_camel_case_name} {device_initial_name};
	{device_underscore_name}_create(&{device_initial_name}, UID, &ipcon);

	// Connect to brickd
	if(ipcon_connect(&ipcon, HOST, PORT) < 0) {{
		fprintf(stderr, "Could not connect\n");
		return 1;
	}}
	// Don't use device before ipcon is connected
{sources}
	printf("Press key to exit\n");
	getchar();{cleanups}
	{device_underscore_name}_destroy(&{device_initial_name});
	ipcon_destroy(&ipcon); // Calls ipcon_disconnect internally
	return 0;
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

        defines = []
        includes = []
        functions = []
        sources = []
        cleanups = []

        for function in self.get_functions():
            defines += function.get_c_defines()
            includes += function.get_c_includes()
            functions.append(function.get_c_function())
            sources.append(function.get_c_source())

        for cleanup in self.get_cleanups():
            defines += cleanup.get_c_defines()
            includes += cleanup.get_c_includes()
            functions.append(cleanup.get_c_function())
            cleanups.append(cleanup.get_c_source())

        unique_includes = []

        for include in includes:
            if include not in unique_includes:
                unique_includes.append(include)

        unique_defines = []

        for define in defines:
            if define not in unique_defines:
                unique_defines.append(define)

        while None in functions:
            functions.remove(None)

        while None in sources:
            sources.remove(None)

        if len(sources) == 0:
            sources = ['\t// TODO: Add example code here\n']

        while None in cleanups:
            cleanups.remove(None)

        return template.format(defines=common.wrap_non_empty('', '\n'.join(unique_defines), '\n\n'),
                               includes=common.wrap_non_empty('\n', '\n'.join(unique_includes), ''),
                               incomplete=incomplete,
                               description=description,
                               device_underscore_category=self.get_device().get_underscore_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               device_underscore_name=self.get_device().get_underscore_name(),
                               device_initial_name=self.get_device().get_initial_name(),
                               device_long_display_name=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               functions=common.wrap_non_empty('\n', '\n'.join(functions), ''),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), ''))

class CExampleArgument(common.ExampleArgument):
    def get_c_source(self):
        type_ = self.get_type()
        value = self.get_value()

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
            return self.get_value_constant().get_c_source()
        else:
            return str(value)

class CExampleArgumentsMixin(object):
    def get_c_arguments(self):
        return [argument.get_c_source() for argument in self.get_arguments()]

class CExampleParameter(common.ExampleParameter, CTypeMixin, CPrintfFormatMixin):
    def get_c_source(self):
        templateA = '{type_} {underscore_name}'
        templateB = '{type_} {underscore_name}[{cardinality}]'
        templateC = '{type_} *{underscore_name}, uint16_t {underscore_name}_length' # FIXME: don't hardcode length as uint16_t

        if self.get_cardinality() == 1:
            template = templateA
        elif self.get_cardinality() > 1:
            template = templateB
        else: # cardinality < 0
            template = templateC

        return template.format(type_=self.get_c_type(),
                               underscore_name=self.get_underscore_name(),
                               cardinality=self.get_cardinality())

    def get_c_unused(self):
        if self.get_label_name() == None:
            if self.get_cardinality() < 0:
                return '\t(void){0}; // avoid unused parameter warning\n\t(void){0}_length; // avoid unused parameter warning'.format(self.get_underscore_name())
            else:
                return '\t(void){0}; // avoid unused parameter warning'.format(self.get_underscore_name())
        else:
            return None

    def get_c_printfs(self):
        # FIXME: the result type can indicate a bitmask, but there is no easy way in C to format an
        #        integer in base-2, that doesn't require open-coding it with several lines of code.
        #        there is "char *itoa(int value, int base)" (see http://www.strudel.org.uk/itoa/)
        #        but it's not in the standard C library and it's not reentrant. so just print the
        #        integer in base-10 the normal way
        template = '\tprintf("{label_name}: {printf_format}{unit_final_name}\\n", {underscore_name}{index}{divisor});'

        if self.get_label_name() == None:
            return []

        if self.get_cardinality() < 0:
            return [] # FIXME: streaming

        result = []

        for index in range(self.get_label_count()):
            result.append(template.format(underscore_name=self.get_underscore_name(),
                                          label_name=self.get_label_name(index=index).replace('%', '%%'),
                                          index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                          divisor=self.get_formatted_divisor('/{0}'),
                                          printf_format=self.get_c_printf_format(),
                                          unit_final_name=self.get_unit_formatted_final_name(' {0}').replace('%', '%%')))

        return result

class CExampleResult(common.ExampleResult, CTypeMixin, CPrintfFormatMixin):
    def get_c_variable_declaration(self):
        underscore_name = self.get_underscore_name()

        if underscore_name == self.get_device().get_initial_name():
            underscore_name += '_'

        if self.get_cardinality() > 1:
            underscore_name += '[{0}]'.format(self.get_cardinality())

        return self.get_c_type(), underscore_name

    def get_c_variable_reference(self):
        templateA = '{underscore_name}'
        templateB = '&{underscore_name}'

        if self.get_cardinality() > 1:
            template = templateA
        else:
            template = templateB

        underscore_name = self.get_underscore_name()

        if underscore_name == self.get_device().get_initial_name():
            underscore_name += '_'

        return template.format(underscore_name=underscore_name)

    def get_c_unused(self):
        if self.get_label_name() == None:
            return '\t(void){0}; // avoid unused parameter warning'.format(self.get_underscore_name())
        else:
            return None

    def get_c_printfs(self):
        # FIXME: the result type can indicate a bitmask, but there is no easy way in C to format an
        #        integer in base-2, that doesn't require open-coding it with several lines of code.
        #        there is "char *itoa(int value, int base)" (see http://www.strudel.org.uk/itoa/)
        #        but it's not in the standard C library and it's not reentrant. so just print the
        #        integer in base-10 the normal way
        template = '\tprintf("{label_name}: {printf_format}{unit_final_name}\\n", {underscore_name}{index}{divisor});'

        if self.get_label_name() == None:
            return []

        if self.get_cardinality() < 0:
            return [] # FIXME: streaming

        result = []

        underscore_name = self.get_underscore_name()

        if underscore_name == self.get_device().get_initial_name():
            underscore_name += '_'

        for index in range(self.get_label_count()):
            result.append(template.format(underscore_name=underscore_name,
                                          label_name=self.get_label_name(index=index).replace('%', '%%'),
                                          index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                          divisor=self.get_formatted_divisor('/{0}'),
                                          printf_format=self.get_c_printf_format(),
                                          unit_final_name=self.get_unit_formatted_final_name(' {0}').replace('%', '%%')))

        return result

class CExampleGetterFunction(common.ExampleGetterFunction, CExampleArgumentsMixin):
    def get_c_defines(self):
        defines = []

        for result in self.get_results():
            defines += result.get_c_printf_defines()

        return defines

    def get_c_includes(self):
        includes = []

        for result in self.get_results():
            includes += result.get_c_printf_includes()

        return includes

    def get_c_function(self):
        return None

    def get_c_source(self):
        template = r"""	// Get current {function_comment_name}{comments}
	{variable_declarations};
	if({device_underscore_name}_{function_underscore_name}(&{device_initial_name}{arguments}{variable_references}) < 0) {{
		fprintf(stderr, "Could not get {function_comment_name}, probably timeout\n");
		return 1;
	}}

{printfs}
"""
        comments = []
        variable_declarations = []
        variable_references = []
        printfs = []

        for result in self.get_results():
            comments.append(result.get_formatted_comment())
            variable_declarations.append(result.get_c_variable_declaration())
            variable_references.append(result.get_c_variable_reference())
            printfs += result.get_c_printfs()

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = comments[:1]

        merged_variable_declarations = [' '.join(variable_declarations[0])]

        for i in range(len(variable_declarations) - 1):
            type0 = variable_declarations[i][0]
            type1 = variable_declarations[i + 1][0]

            if type0 != type1:
                merged_variable_declarations.append('; ' + ' '.join(variable_declarations[i + 1]))
            else:
                merged_variable_declarations.append(', ' + variable_declarations[i + 1][1])

        while None in printfs:
            printfs.remove(None)

        result = template.format(device_underscore_name=self.get_device().get_underscore_name(),
                                 device_initial_name=self.get_device().get_initial_name(),
                                 function_comment_name=self.get_comment_name(),
                                 function_underscore_name=self.get_underscore_name(),
                                 comments=''.join(comments),
                                 variable_declarations=''.join(merged_variable_declarations),
                                 variable_references=',<BP>' + ',<BP>'.join(variable_references),
                                 printfs='\n'.join(printfs),
                                 arguments=common.wrap_non_empty(',<BP>', ',<BP>'.join(self.get_c_arguments()), ''))

        return common.break_string(result, '_{}('.format(self.get_underscore_name()))

class CExampleSetterFunction(common.ExampleSetterFunction, CExampleArgumentsMixin):
    def get_c_defines(self):
        return []

    def get_c_includes(self):
        return []

    def get_c_function(self):
        return None

    def get_c_source(self):
        template = '{comment1}{global_line_prefix}\t{device_underscore_name}_{function_underscore_name}(&{device_initial_name}{arguments});{comment2}\n'

        result = template.format(global_line_prefix=global_line_prefix,
                                 device_underscore_name=self.get_device().get_underscore_name(),
                                 device_initial_name=self.get_device().get_initial_name(),
                                 function_underscore_name=self.get_underscore_name(),
                                 arguments=common.wrap_non_empty(',<BP>', ',<BP>'.join(self.get_c_arguments()), ''),
                                 comment1=self.get_formatted_comment1(global_line_prefix + '\t// {0}\n', '\r', '\n' + global_line_prefix + '\t// '),
                                 comment2=self.get_formatted_comment2(' // {0}', ''))

        return common.break_string(result, '_{}('.format(self.get_underscore_name()))

class CExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_c_defines(self):
        defines = []

        for parameter in self.get_parameters():
            defines += parameter.get_c_printf_defines()

        return defines

    def get_c_includes(self):
        includes = []

        for parameter in self.get_parameters():
            includes += parameter.get_c_printf_includes()

        return includes

    def get_c_function(self):
        template1A = r"""// Callback function for {function_comment_name} callback{comments}
"""
        template1B = r"""{override_comment}
"""
        template2 = r"""void cb_{function_underscore_name}({parameters}void *user_data) {{{unuseds}
	(void)user_data; // avoid unused parameter warning

{printfs}{extra_message}
}}
"""
        override_comment = self.get_formatted_override_comment('// {0}', None, '\n// ')

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B

        comments = []
        parameters = []
        unuseds = []
        printfs = []

        for parameter in self.get_parameters():
            comments.append(parameter.get_formatted_comment())
            parameters.append(parameter.get_c_source())
            unuseds.append(parameter.get_c_unused())
            printfs += parameter.get_c_printfs()

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = [comments[0].replace('parameter has', 'parameters have')]

        while None in unuseds:
            unuseds.remove(None)

        while None in printfs:
            printfs.remove(None)

        if len(printfs) > 1:
            printfs.append('\tprintf("\\n");')

        extra_message = self.get_formatted_extra_message('\tprintf("{0}\\n");').replace('%', '%%')

        if len(extra_message) > 0 and len(printfs) > 0:
            extra_message = '\n' + extra_message

        result = template1.format(function_comment_name=self.get_comment_name(),
                                  comments=''.join(comments),
                                  override_comment=override_comment) + \
                 template2.format(function_underscore_name=self.get_underscore_name(),
                                  parameters=common.wrap_non_empty('', ',<BP>'.join(parameters), ',<BP>'),
                                  unuseds=common.wrap_non_empty('\n', '\n'.join(unuseds), ''),
                                  printfs='\n'.join(printfs),
                                  extra_message=extra_message)

        return common.break_string(result, 'cb_{}('.format(self.get_underscore_name()))

    def get_c_source(self):
        template = r"""	// Register {function_comment_name}<BP>callback<BP>to<BP>function<BP>cb_{function_underscore_name}
	{device_underscore_name}_register_callback(&{device_initial_name},
	{spaces}                   {device_upper_case_name}_CALLBACK_{function_upper_case_name},
	{spaces}                   (void *)cb_{function_underscore_name},
	{spaces}                   NULL);
"""

        result = template.format(device_underscore_name=self.get_device().get_underscore_name(),
                                 device_upper_case_name=self.get_device().get_upper_case_name(),
                                 device_initial_name=self.get_device().get_initial_name(),
                                 function_underscore_name=self.get_underscore_name(),
                                 function_upper_case_name=self.get_upper_case_name(),
                                 function_comment_name=self.get_comment_name(),
                                 spaces=' ' * len(self.get_device().get_underscore_name()))

        return common.break_string(result, '// ', indent_tail='// ')

class CExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction, CExampleArgumentsMixin):
    def get_c_defines(self):
        return []

    def get_c_includes(self):
        return []

    def get_c_function(self):
        return None

    def get_c_source(self):
        templateA = r"""	// Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
	{device_underscore_name}_set_{function_underscore_name}_period(&{device_initial_name}{arguments}, {period_msec});
"""
        templateB = r"""	// Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
	// Note: The {function_comment_name} callback is only called every {period_sec_long}
	//       if the {function_comment_name} has changed since the last call!
	{device_underscore_name}_set_{function_underscore_name}_callback_period(&{device_initial_name}{arguments}, {period_msec});
"""

        if self.get_device().get_underscore_name().startswith('imu'):
            template = templateA # FIXME: special hack for IMU Brick (2.0) callback behavior and name mismatch
        else:
            template = templateB

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_underscore_name=self.get_device().get_underscore_name(),
                               device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty(', ', ', '.join(self.get_c_arguments()), ''),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class CExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_c_source(self):
        template = '{minimum}, {maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class CExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction, CExampleArgumentsMixin):
    def get_c_defines(self):
        return []

    def get_c_includes(self):
        return []

    def get_c_function(self):
        return None

    def get_c_source(self):
        template = r"""	// Configure threshold for {function_comment_name} "{option_comment}"{mininum_maximum_unit_comments}
	{device_underscore_name}_set_{function_underscore_name}_callback_threshold(&{device_initial_name}{arguments}, '{option_char}', {mininum_maximums});
"""
        mininum_maximums = []
        mininum_maximum_unit_comments = []

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_c_source())
            mininum_maximum_unit_comments.append(mininum_maximum.get_unit_comment())

        if len(mininum_maximum_unit_comments) > 1 and len(set(mininum_maximum_unit_comments)) == 1:
            mininum_maximum_unit_comments = mininum_maximum_unit_comments[:1]

        return template.format(device_underscore_name=self.get_device().get_underscore_name(),
                               device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty(', ', ', '.join(self.get_c_arguments()), ''),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               mininum_maximums=', '.join(mininum_maximums),
                               mininum_maximum_unit_comments=''.join(mininum_maximum_unit_comments))

class CExampleCallbackConfigurationFunction(common.ExampleCallbackConfigurationFunction, CExampleArgumentsMixin):
    def get_c_defines(self):
        return []

    def get_c_includes(self):
        return []

    def get_c_function(self):
        return None

    def get_c_source(self):
        templateA = r"""	// Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
	{device_underscore_name}_set_{function_underscore_name}_callback_configuration(&{device_initial_name}{arguments}, {period_msec}, false);
"""
        templateB = r"""	// Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms) without a threshold
	{device_underscore_name}_set_{function_underscore_name}_callback_configuration(&{device_initial_name}{arguments}, {period_msec}, false, '{option_char}', {mininum_maximums});
"""
        templateC = r"""	// Configure threshold for {function_comment_name} "{option_comment}"{mininum_maximum_unit_comments}
	// with a debounce period of {period_sec_short} ({period_msec}ms)
	{device_underscore_name}_set_{function_underscore_name}_callback_configuration(&{device_initial_name}{arguments}, {period_msec}, false, '{option_char}', {mininum_maximums});
"""

        if self.get_option_char() == None:
            template = templateA
        elif self.get_option_char() == 'x':
            template = templateB
        else:
            template = templateC

        mininum_maximums = []
        mininum_maximum_unit_comments = []

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_c_source())
            mininum_maximum_unit_comments.append(mininum_maximum.get_unit_comment())

        if len(mininum_maximum_unit_comments) > 1 and len(set(mininum_maximum_unit_comments)) == 1:
            mininum_maximum_unit_comments = mininum_maximum_unit_comments[:1]

        return template.format(device_underscore_name=self.get_device().get_underscore_name(),
                               device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty(', ', ', '.join(self.get_c_arguments()), ''),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               mininum_maximums=', '.join(mininum_maximums),
                               mininum_maximum_unit_comments=''.join(mininum_maximum_unit_comments))

class CExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_c_defines(self):
        if self.get_type() == 'sleep':
            return ['#define IPCON_EXPOSE_MILLISLEEP']
        else:
            return []

    def get_c_includes(self):
        return []

    def get_c_function(self):
        return None

    def get_c_source(self):
        global global_line_prefix

        type_ = self.get_type()

        if type_ == 'empty':
            return ''
        elif type_ == 'debounce_period':
            template = r"""	// Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms)
	{device_underscore_name}_set_debounce_period(&{device_initial_name}, {period_msec});
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_underscore_name=self.get_device().get_underscore_name(),
                                   device_initial_name=self.get_device().get_initial_name(),
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type_ == 'sleep':
            template = '{comment1}{global_line_prefix}\tmillisleep({duration});{comment2}\n'

            return template.format(global_line_prefix=global_line_prefix,
                                   duration=self.get_sleep_duration(),
                                   comment1=self.get_formatted_sleep_comment1(global_line_prefix + '\t// {0}\n', '\r', '\n' + global_line_prefix + '\t// '),
                                   comment2=self.get_formatted_sleep_comment2(' // {0}', ''))
        elif type_ == 'wait':
            return None
        elif type_ == 'loop_header':
            template = '{comment}\tint i;\n\tfor(i = 0; i < {limit}; ++i) {{\n'
            global_line_prefix = '\t'

            return template.format(limit=self.get_loop_header_limit(),
                                   comment=self.get_formatted_loop_header_comment('\t// {0}\n', '', '\n\t// '))
        elif type_ == 'loop_footer':
            global_line_prefix = ''

            return '\r\t}\n'

class CExamplesGenerator(common.ExamplesGenerator):
    def get_bindings_name(self):
        return 'c'

    def get_constant_class(self):
        return CConstant

    def get_example_class(self):
        return CExample

    def get_example_argument_class(self):
        return CExampleArgument

    def get_example_parameter_class(self):
        return CExampleParameter

    def get_example_result_class(self):
        return CExampleResult

    def get_example_getter_function_class(self):
        return CExampleGetterFunction

    def get_example_setter_function_class(self):
        return CExampleSetterFunction

    def get_example_callback_function_class(self):
        return CExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return CExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return CExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return CExampleCallbackThresholdFunction

    def get_example_callback_configuration_function_class(self):
        return CExampleCallbackConfigurationFunction

    def get_example_special_function_class(self):
        return CExampleSpecialFunction

    def generate(self, device):
        if os.getenv('TINKERFORGE_GENERATE_EXAMPLES_FOR_DEVICE', device.get_camel_case_name()) != device.get_camel_case_name():
            print('  \033[01;31m- skipped\033[0m')
            return

        examples_directory = self.get_examples_directory(device)
        examples = device.get_examples()

        if len(examples) == 0:
            print('  \033[01;31m- no examples\033[0m')
            return

        if not os.path.exists(examples_directory):
            os.makedirs(examples_directory)

        for example in examples:
            filename = 'example_{0}.c'.format(example.get_underscore_name())
            filepath = os.path.join(examples_directory, filename)

            if example.is_incomplete():
                if os.path.exists(filepath) and self.skip_existing_incomplete_example:
                    print('  - ' + filename + ' \033[01;35m(incomplete, skipped)\033[0m')
                    continue
                else:
                    print('  - ' + filename + ' \033[01;31m(incomplete)\033[0m')
            else:
                print('  - ' + filename)

            with open(filepath, 'w') as f:
                f.write(example.get_c_source())

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', CExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
