#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Examples Generator
Copyright (C) 2015-2019 Matthias Bolte <matthias@tinkerforge.com>

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

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import re
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
from generators.embedded_c import embedded_c_common

global_line_prefix = ''

class CTypeMixin(object):
    def get_c_type(self):
        type_ = self.get_type().split(':')[0]

        if type_ == 'string':
            type_ = 'char'
        elif 'int' in type_:
            type_ += '_t'

        return type_

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
        elif type_ == 'bool':
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

    def get_c_printf_prefix(self):
        return ''

    def get_c_printf_suffix(self):
        type_ = self.get_type().split(':')[0]

        if type_ == 'bool':
            return ' ? "true" : "false"'
        else:
            return ''

class CConstant(common.Constant):
    def get_c_source(self):
        template = '{device_name}_{constant_group_name}_{constant_name}'

        return template.format(device_name=self.get_device().get_name().upper,
                               constant_group_name=self.get_constant_group().get_name().upper,
                               constant_name=self.get_name().upper)

class CExample(common.Example):
    def __init__(self, raw_data, device):
        common.Example.__init__(self, raw_data, device)
        self.used_argument_decl_names = {}

    def get_c_source(self):
        template = r"""{defines}#include <stdio.h>{includes}{incomplete}{description}

#include "ip_connection.h"
#include "{device_category}_{device_name_under}.h"

#define HOST "localhost"
#define PORT 4223
#define UID "{dummy_uid}" // Change {dummy_uid} to the UID of your {device_long_display_name}
{functions}
int main(void) {{
	// Create IP connection
	IPConnection ipcon;
	ipcon_create(&ipcon);

	// Create device object
	{device_name_camel} {device_name_initial};
	{device_name_under}_create(&{device_name_initial}, UID, &ipcon);

	// Connect to brickd
	if(ipcon_connect(&ipcon, HOST, PORT) < 0) {{
		fprintf(stderr, "Could not connect\n");
		return 1;
	}}
	// Don't use device before ipcon is connected
{sources}
	printf("Press key to exit\n");
	getchar();{cleanups}
	{device_name_under}_destroy(&{device_name_initial});
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
                               device_category=self.get_device().get_category().under,
                               device_name_camel=self.get_device().get_name().camel,
                               device_name_under=self.get_device().get_name().under,
                               device_name_initial=self.get_device().get_initial_name(),
                               device_long_display_name=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               functions=common.wrap_non_empty('\n', '\n'.join(functions), ''),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), '\n'))

class CExampleArgument(common.ExampleArgument, CTypeMixin):
    def get_c_source(self):
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
                return common.make_c_like_bitmask(value)
            elif type_.endswith(':constant'):
                return self.get_value_constant(value).get_c_source()
            else:
                return str(value)

        value = self.get_value()

        if isinstance(value, list):
            name = self.get_element().get_name().under
            if name in self.get_example().used_argument_decl_names:
                suffix = self.get_example().used_argument_decl_names[name]
                suffix += 1
                self.get_example().used_argument_decl_names[name] = suffix
                name += '_' + str(suffix)
            else:
                self.get_example().used_argument_decl_names[name] = 0

            declaration = '{type} {name}[{size}] = {{{data}}};'.format(type=self.get_c_type(),
                                                                       name=name,
                                                                       size=len(value),
                                                                       data=', '.join([helper(item) for item in value]))
            if self.get_element().get_cardinality() < 0:
                return (declaration, '{name}, {size}'.format(name=name,
                                                             size=len(value)))
            return (declaration, '{name}'.format(name=name))

        return (None, helper(value))

class CExampleArgumentsMixin(object):
    def get_c_arguments(self):
        args = self.get_arguments()
        if len(args) == 0:
            return ([], [])
        definitions, arguments = zip(*(argument.get_c_source() for argument in self.get_arguments()))
        definitions = [d for d in definitions if d is not None]
        return (definitions, arguments)

class CExampleParameter(common.ExampleParameter, CTypeMixin, CPrintfFormatMixin):
    def get_c_source(self):
        templateA = '{type_} {name}'
        templateB = '{type_} {name}[{cardinality}]'
        templateC = '{type_} *{name}, uint16_t {name}_length' # FIXME: don't hardcode length as uint16_t

        if self.get_cardinality() == 1:
            template = templateA
        elif self.get_cardinality() > 1:
            template = templateB
        else: # cardinality < 0
            template = templateC

        return template.format(type_=self.get_c_type(),
                               name=self.get_name().under,
                               cardinality=self.get_cardinality())

    def get_c_unuseds(self):
        templateA = '(void){name};'
        templateB = '(void){name}_length;'
        result = []

        if self.get_label_name() == None:
            result = [templateA.format(name=self.get_name().under)]

            if self.get_cardinality() < 0:
                result.append(templateB.format(name=self.get_name().under))

        return result

    def get_c_printfs(self):
        if self.get_type().split(':')[-1] == 'constant':
            if self.get_label_name() == None:
                return []

            # FIXME: need to handle multiple labels
            assert self.get_label_count() == 1

            template = '{else_}if({name} == {constant_name}) {{\n{global_line_prefix}\t\tprintf("{label}: {constant_title}\\n");{comment}\n\t}}'
            constant_group = self.get_constant_group()
            result = []

            for constant in constant_group.get_constants():
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              else_='\belse ' if len(result) > 0 else global_line_prefix + '\t',
                                              name=self.get_name().under,
                                              label=self.get_label_name().replace('%', '%%'),
                                              constant_name=constant.get_c_source(),
                                              constant_title=constant.get_name().space,
                                              comment=self.get_formatted_comment(' // {0}')))

            result = ['\r' + '\n'.join(result).replace('\n\b', ' ') + '\r']
        else:
            # FIXME: the result type can indicate a bitmask, but there is no easy way in C to format an
            #        integer in base-2, that doesn't require open-coding it with several lines of code.
            #        there is "char *itoa(int value, int base)" (see https://www.strudel.org.uk/itoa/)
            #        but it's not in the standard C library and it's not reentrant. so just print the
            #        integer in base-10 the normal way
            template = '{global_line_prefix}\tprintf("{label}: {printf_format}{unit}\\n", {printf_prefix}{name}{index}{divisor}{printf_suffix});{comment}'

            if self.get_label_name() == None:
                return []

            if self.get_cardinality() < 0:
                return [] # FIXME: streaming

            result = []

            for index in range(self.get_label_count()):
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              name=self.get_name().under,
                                              label=self.get_label_name(index=index).replace('%', '%%'),
                                              index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                              divisor=self.get_formatted_divisor('/{0}'),
                                              printf_format=self.get_c_printf_format(),
                                              printf_prefix=self.get_c_printf_prefix(),
                                              printf_suffix=self.get_c_printf_suffix(),
                                              unit=self.get_formatted_unit_name(' {0}').replace('%', '%%'),
                                              comment=self.get_formatted_comment(' // {0}')))

        return result

class CExampleResult(common.ExampleResult, CTypeMixin, CPrintfFormatMixin):
    def get_c_variable_declaration(self):
        name = self.get_name().under

        if name == self.get_device().get_initial_name():
            name += '_'

        if self.get_cardinality() > 1:
            name += '[{0}]'.format(self.get_cardinality())

        return self.get_c_type(), name

    def get_c_variable_reference(self):
        templateA = '{name}'
        templateB = '&{name}'

        if self.get_cardinality() > 1:
            template = templateA
        else:
            template = templateB

        name = self.get_name().under

        if name == self.get_device().get_initial_name():
            name += '_'

        return template.format(name=name)

    def get_c_printfs(self):
        if self.get_type().split(':')[-1] == 'constant':
            # FIXME: need to handle multiple labels
            assert self.get_label_count() == 1

            template = '{else_}if({name} == {constant_name}) {{\n{global_line_prefix}\t\tprintf("{label}: {constant_title}\\n");{comment}\n\t}}'
            constant_group = self.get_constant_group()
            result = []

            for constant in constant_group.get_constants():
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              else_='\belse ' if len(result) > 0 else global_line_prefix + '\t',
                                              name=self.get_name().under,
                                              label=self.get_label_name().replace('%', '%%'),
                                              constant_name=constant.get_c_source(),
                                              constant_title=constant.get_name().space,
                                              comment=self.get_formatted_comment(' // {0}')))

            result = ['\r' + '\n'.join(result).replace('\n\b', ' ') + '\r']
        else:
            # FIXME: the result type can indicate a bitmask, but there is no easy way in C to format an
            #        integer in base-2, that doesn't require open-coding it with several lines of code.
            #        there is "char *itoa(int value, int base)" (see https://www.strudel.org.uk/itoa/)
            #        but it's not in the standard C library and it's not reentrant. so just print the
            #        integer in base-10 the normal way
            template = '{global_line_prefix}\tprintf("{label}: {printf_format}{unit}\\n", {printf_prefix}{name}{index}{divisor}{printf_suffix});{comment}'

            if self.get_label_name() == None:
                return []

            if self.get_cardinality() < 0:
                return [] # FIXME: streaming

            name = self.get_name().under

            if name == self.get_device().get_initial_name():
                name += '_'

            result = []

            for index in range(self.get_label_count()):
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              name=name,
                                              label=self.get_label_name(index=index).replace('%', '%%'),
                                              index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                              divisor=self.get_formatted_divisor('/{0}'),
                                              printf_format=self.get_c_printf_format(),
                                              printf_prefix=self.get_c_printf_prefix(),
                                              printf_suffix=self.get_c_printf_suffix(),
                                              unit=self.get_formatted_unit_name(' {0}').replace('%', '%%'),
                                              comment=self.get_formatted_comment(' // {0}')))

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
        template = r"""{global_line_prefix}	// Get current {function_name_comment}
{global_line_prefix}{variable_declarations};
{global_line_prefix}	if({device_name_under}_{function_name_under}(&{device_name_initial}{arguments}{variable_references}) < 0) {{
{global_line_prefix}		fprintf(stderr, "Could not get {function_name_comment}, probably timeout\n");
{global_line_prefix}		return 1;
{global_line_prefix}	}}

{printfs}
"""
        variable_declarations = []
        variable_references = []
        printfs = []

        for result in self.get_results():
            variable_declarations.append(result.get_c_variable_declaration())
            variable_references.append(result.get_c_variable_reference())
            printfs += result.get_c_printfs()

        arg_declarations, arguments = self.get_c_arguments()
        variable_declarations += arg_declarations

        merged_variable_declarations = []

        for variable_declaration in variable_declarations:
            merged = False

            for merged_variable_declaration in merged_variable_declarations:
                if merged_variable_declaration[0] == variable_declaration[0]:
                    merged_variable_declaration[1].append(variable_declaration[1])
                    merged = True
                    break

            if not merged:
                merged_variable_declarations.append([variable_declaration[0], [variable_declaration[1]]])

        variable_declarations = []

        for merged_variable_declaration in merged_variable_declarations:
            variable_declarations.append('{0} {1}'.format(merged_variable_declaration[0],
                                                          ',<BP>'.join(merged_variable_declaration[1])))

        variable_declarations = common.break_string('\t' + ';<BP>'.join(variable_declarations),
                                                    merged_variable_declarations[0][0] + ' ')
        variable_declarations = re.sub(';\n\t([ ]+)', ';\n\t', variable_declarations, flags=re.MULTILINE)

        while None in printfs:
            printfs.remove(None)



        result = template.format(global_line_prefix=global_line_prefix,
                                 device_name_under=self.get_device().get_name().under,
                                 device_name_initial=self.get_device().get_initial_name(),
                                 function_name_comment=self.get_comment_name(),
                                 function_name_under=self.get_name().under,
                                 variable_declarations=variable_declarations,
                                 variable_references=',<BP>' + ',<BP>'.join(variable_references),
                                 printfs='\n'.join(printfs).replace('\r\n\r', '\n\n').strip('\r').replace('\r', '\n'),
                                 arguments=common.wrap_non_empty(',<BP>', ',<BP>'.join(arguments), ''))

        return common.break_string(result, '_{}('.format(self.get_name().under))

class CExampleSetterFunction(common.ExampleSetterFunction, CExampleArgumentsMixin):
    def get_c_defines(self):
        return []

    def get_c_includes(self):
        return []

    def get_c_function(self):
        return None

    def get_c_source(self):
        template = '{comment1}{declarations}{global_line_prefix}\t{device_name_under}_{function_name}(&{device_name_initial}{arguments});{comment2}\n'

        arg_declarations, arguments = self.get_c_arguments()
        declarations = common.wrap_non_empty('', '\n'.join(['{global_line_prefix}\t{decl}'.format(global_line_prefix=global_line_prefix, decl=decl) for decl in arg_declarations]), '\n')

        result = template.format(global_line_prefix=global_line_prefix,
                                 device_name_under=self.get_device().get_name().under,
                                 device_name_initial=self.get_device().get_initial_name(),
                                 function_name=self.get_name().under,
                                 declarations=declarations,
                                 arguments=common.wrap_non_empty(',<BP>', ',<BP>'.join(arguments), ''),
                                 comment1=self.get_formatted_comment1(global_line_prefix + '\t// {0}\n', '\r', '\n' + global_line_prefix + '\t// '),
                                 comment2=self.get_formatted_comment2(' // {0}', ''))

        return common.break_string(result, '_{}('.format(self.get_name().under))

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
        template1A = r"""// Callback function for {function_name_comment} callback
"""
        template1B = r"""{override_comment}
"""
        template2 = r"""void cb_{function_name_under}({parameters}void *user_data) {{
	{unuseds}

{printfs}{extra_message}
}}
"""
        override_comment = self.get_formatted_override_comment('// {0}', None, '\n// ')

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B

        parameters = []
        unuseds = []
        printfs = []

        for parameter in self.get_parameters():
            parameters.append(parameter.get_c_source())
            unuseds += parameter.get_c_unuseds()
            printfs += parameter.get_c_printfs()

        while None in unuseds:
            unuseds.remove(None)

        unuseds.append('(void)user_data;')

        unuseds = common.wrap_non_empty('', '<BP>'.join(unuseds), ' // avoid unused parameter warning')
        unuseds = common.break_string(unuseds, '').replace('\n', '\n\t')

        while None in printfs:
            printfs.remove(None)

        if len(printfs) > 1:
            printfs.append('\tprintf("\\n");')

        extra_message = self.get_formatted_extra_message('\tprintf("{0}\\n");').replace('%', '%%')

        if len(extra_message) > 0 and len(printfs) > 0:
            extra_message = '\n' + extra_message

        result = template1.format(function_name_comment=self.get_comment_name(),
                                  override_comment=override_comment) + \
                 template2.format(function_name_under=self.get_name().under,
                                  parameters=common.wrap_non_empty('', ',<BP>'.join(parameters), ',<BP>'),
                                  unuseds=unuseds,
                                  printfs='\n'.join(printfs).replace('\r\n\r', '\n\n').strip('\r').replace('\r', '\n'),
                                  extra_message=extra_message)

        return common.break_string(result, 'cb_{}('.format(self.get_name().under))

    def get_c_source(self):
        template = r"""	// Register {function_name_comment}<BP>callback<BP>to<BP>function<BP>cb_{function_name_under}
	{device_name_under}_register_callback(&{device_name_initial},
	{spaces}                   {device_name_upper}_CALLBACK_{function_name_upper},
	{spaces}                   (void (*)(void))cb_{function_name_under},
	{spaces}                   NULL);
"""

        result = template.format(device_name_under=self.get_device().get_name().under,
                                 device_name_upper=self.get_device().get_name().upper,
                                 device_name_initial=self.get_device().get_initial_name(),
                                 function_name_under=self.get_name().under,
                                 function_name_upper=self.get_name().upper,
                                 function_name_comment=self.get_comment_name(),
                                 spaces=' ' * len(self.get_device().get_name().under))

        return common.break_string(result, '// ', indent_tail='// ')

class CExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction, CExampleArgumentsMixin):
    def get_c_defines(self):
        return []

    def get_c_includes(self):
        return []

    def get_c_function(self):
        return None

    def get_c_source(self):
        templateA = r"""	// Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms){declarations}
	{device_name_under}_set_{function_name_under}_period(&{device_name_initial}{arguments}, {period_msec});
"""
        templateB = r"""	// Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
	// Note: The {function_name_comment} callback is only called every {period_sec_long}
	//       if the {function_name_comment} has changed since the last call!{declarations}
	{device_name_under}_set_{function_name_under}_callback_period(&{device_name_initial}{arguments}, {period_msec});
"""

        if self.get_device().get_name().space.startswith('IMU'):
            template = templateA # FIXME: special hack for IMU Brick (2.0) callback behavior and name mismatch
        else:
            template = templateB

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        arg_declarations, arguments = self.get_c_arguments()
        declarations = common.wrap_non_empty('\n', '\n'.join(['{global_line_prefix}\t{decl}'.format(global_line_prefix=global_line_prefix, decl=decl) for decl in arg_declarations]), '')

        return template.format(device_name_under=self.get_device().get_name().under,
                               device_name_initial=self.get_device().get_initial_name(),
                               function_name_under=self.get_name().under,
                               function_name_comment=self.get_comment_name(),
                               declarations=declarations,
                               arguments=common.wrap_non_empty(', ', ', '.join(arguments), ''),
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
        template = r"""	// Configure threshold for {function_name_comment} "{option_comment}"{declarations}
	{device_name_under}_set_{function_name_under}_callback_threshold(&{device_name_initial}{arguments}, '{option_char}', {minimum_maximums});
"""
        minimum_maximums = []

        for minimum_maximum in self.get_minimum_maximums():
            minimum_maximums.append(minimum_maximum.get_c_source())

        arg_declarations, arguments = self.get_c_arguments()
        declarations = common.wrap_non_empty('\n', '\n'.join(['{global_line_prefix}\t{decl}'.format(global_line_prefix=global_line_prefix, decl=decl) for decl in arg_declarations]), '')

        return template.format(device_name_under=self.get_device().get_name().under,
                               device_name_initial=self.get_device().get_initial_name(),
                               function_name_under=self.get_name().under,
                               function_name_comment=self.get_comment_name(),
                               declarations=declarations,
                               arguments=common.wrap_non_empty(', ', ', '.join(arguments), ''),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               minimum_maximums=', '.join(minimum_maximums))

class CExampleCallbackConfigurationFunction(common.ExampleCallbackConfigurationFunction, CExampleArgumentsMixin):
    def get_c_defines(self):
        return []

    def get_c_includes(self):
        return []

    def get_c_function(self):
        return None

    def get_c_source(self):
        templateA = r"""	// Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms){declarations}
	{device_name_under}_set_{function_name_under}_callback_configuration(&{device_name_initial}{arguments}, {period_msec}{value_has_to_change});
"""
        templateB = r"""	// Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms) without a threshold{declarations}
	{device_name_under}_set_{function_name_under}_callback_configuration(&{device_name_initial}{arguments}, {period_msec}{value_has_to_change}, '{option_char}', {minimum_maximums});
"""
        templateC = r"""	// Configure threshold for {function_name_comment} "{option_comment}"
	// with a debounce period of {period_sec_short} ({period_msec}ms){declarations}
	{device_name_under}_set_{function_name_under}_callback_configuration(&{device_name_initial}{arguments}, {period_msec}{value_has_to_change}, '{option_char}', {minimum_maximums});
"""

        if self.get_option_char() == None:
            template = templateA
        elif self.get_option_char() == 'x':
            template = templateB
        else:
            template = templateC

        minimum_maximums = []

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        for minimum_maximum in self.get_minimum_maximums():
            minimum_maximums.append(minimum_maximum.get_c_source())

        arg_declarations, arguments = self.get_c_arguments()
        declarations = common.wrap_non_empty('\n', '\n'.join(['{global_line_prefix}\t{decl}'.format(global_line_prefix=global_line_prefix, decl=decl) for decl in arg_declarations]), '')

        return template.format(device_name_under=self.get_device().get_name().under,
                               device_name_initial=self.get_device().get_initial_name(),
                               function_name_under=self.get_name().under,
                               function_name_comment=self.get_comment_name(),
                               declarations=declarations,
                               arguments=common.wrap_non_empty(', ', ', '.join(arguments), ''),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               value_has_to_change=common.wrap_non_empty(', ', self.get_value_has_to_change('true', 'false', ''), ''),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               minimum_maximums=', '.join(minimum_maximums))

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
	{device_name_under}_set_debounce_period(&{device_name_initial}, {period_msec});
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_name_under=self.get_device().get_name().under,
                                   device_name_initial=self.get_device().get_initial_name(),
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

class CExamplesGenerator(embedded_c_common.CGeneratorTrait, common.ExamplesGenerator):
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
            filename = 'example_{0}.c'.format(example.get_name().under)
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
                f.write(example.get_c_source())

def generate(root_dir):
    return
    common.generate(root_dir, 'en', CExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
