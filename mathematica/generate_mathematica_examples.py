#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mathematica Examples Generator
Copyright (C) 2015-2018 Matthias Bolte <matthias@tinkerforge.com>

generate_mathematica_examples.py: Generator for Mathematica examples

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
import re

sys.path.append(os.path.split(os.getcwd())[0])
import common
from txt2nb import txt2nb

global_line_prefix = ''
global_line_suffix = ''

class MathematicaConstant(common.Constant):
    def get_mathematica_source(self):
        template = 'Tinkerforge`{device_category}{device_name}`{constant_group_name}U{constant_name}'

        return template.format(device_category=self.get_device().get_category().camel,
                               device_name=self.get_device().get_name().camel,
                               constant_group_name=self.get_constant_group().get_name().upper.replace('_', 'U'),
                               constant_name=self.get_name().upper.replace('_', 'U'))

class MathematicaExample(common.Example):
    def get_mathematica_source(self):
        template = r"""Needs["NETLink`"]
LoadNETAssembly["Tinkerforge",NotebookDirectory[]<>"../../.."]{incomplete}{description}

host="localhost"
port=4223
uid="{dummy_uid}"(*Change {dummy_uid} to the UID of your {device_name_long_display}*)

(*Create IPConnection and device object*)
ipcon=NETNew["Tinkerforge.IPConnection"]
{device_name_initial}=NETNew["Tinkerforge.{device_category}{device_name_camel}",uid,ipcon]
ipcon@Connect[host,port]
{sources}
(*Clean up*){cleanups}
ipcon@Disconnect[]
ReleaseNETObject[{device_name_initial}]
ReleaseNETObject[ipcon]
"""

        if self.is_incomplete():
            incomplete = '\n\n(*FIXME: This example is incomplete*)'
        else:
            incomplete = ''

        if self.get_description() != None:
            description = '\n\n(*{0}*)'.format(self.get_description().replace('\n', '*)\n(*'))
        else:
            description = ''

        sources = []
        add_input_call = False

        for function in self.get_functions():
            if isinstance(function, MathematicaExampleCallbackFunction):
                add_input_call = True
            elif isinstance(function, MathematicaExampleSpecialFunction) and function.get_type() == 'wait':
                add_input_call = True

            sources.append(function.get_mathematica_source())

        while None in sources:
            sources.remove(None)

        if len(sources) == 0:
            sources = ['(*TODO: Add example code here*)\n']
        elif add_input_call:
            sources.append('Input["Click OK to exit"]\n')

        cleanups = []

        for cleanup in self.get_cleanups():
            cleanups.append(cleanup.get_mathematica_source())

        while None in cleanups:
            cleanups.remove(None)

        return template.format(incomplete=incomplete,
                               description=description,
                               device_category=self.get_device().get_category().camel,
                               device_name_camel=self.get_device().get_name().camel,
                               device_name_initial=self.get_device().get_initial_name(),
                               device_name_long_display=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               # FIXME: '*)\n\n\b' -> '*)\n\n' misses to remove the final semicolon before a comment inside of a loop
                               sources='\n' + '\n'.join(sources).replace('*)\n\n\b', '*)\n\n').replace(';\n\n\b', '\n\n').replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), ''))

class MathematicaExampleArgument(common.ExampleArgument):
    def get_mathematica_source(self):
        type_ = self.get_type()

        def helper(value):
            if type_ == 'bool':
                if value:
                    return 'True'
                else:
                    return 'False'
            elif type_ == 'char':
                return 'ToCharacterCode["{0}"][[1]]'.format(value)
            elif type_ == 'string':
                return '"{0}"'.format(value)
            elif ':bitmask:' in type_:
                bits = []

                for i in range(64):
                    if (value & (1 << i)) != 0:
                        bits = ['1'] + bits
                    else:
                        bits = ['0'] + bits

                length = int(type_.split(':')[2])

                return 'FromDigits[{{{0}}},2]'.format(','.join(bits[-length:]))
            elif type_.endswith(':constant'):
                return self.get_value_constant(value).get_mathematica_source()
            else:
                return str(value)

        value = self.get_value()

        if isinstance(value, list):
            return '{{{0}}}'.format(','.join([helper(item) for item in value]))

        return helper(value)

class MathematicaExampleArgumentsMixin(object):
    def get_mathematica_arguments(self):
        return [argument.get_mathematica_source() for argument in self.get_arguments()]

class MathematicaExampleParameter(common.ExampleParameter):
    def get_mathematica_source(self):
        if self.get_cardinality() == 1:
            template = '{name}_'

            return template.format(name=self.get_name().headless)
        elif self.get_cardinality() > 0:
            result = []

            for i in range(self.get_cardinality()):
                result.append('{}{}_'.format(self.get_name().headless, i + 1))

            return '{{{}}}'.format(','.join(result))
        else:
            return 'FIXME_'

    def get_mathematica_prints(self):
        if self.get_type().split(':')[-1] == 'constant':
            if self.get_label_name() == None:
                return []
                
            # FIXME: need to handle multiple labels
            assert self.get_label_count() == 1

            template = '{global_line_prefix} {else_}If[{name}=={constant_name},Print["{label}: {constant_title}"]]{comment}'
            constant_group = self.get_constant_group()
            result = []

            for constant in constant_group.get_constants():
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              else_=' ' if len(result) > 0 else '',
                                              name=self.get_name().headless,
                                              label=self.get_label_name(),
                                              constant_name=constant.get_mathematica_source(),
                                              constant_title=constant.get_name().space,
                                              comment=self.get_formatted_comment('(*{0}*)')))

            result = ['\n'.join(result)]
        else:
            templateA = '{global_line_prefix} Print["{label}: "<>{name}{index}]{comment}'
            templateB = '{global_line_prefix} Print["{label}: "<>ToString[N[Quantity[{name}{index},"{quantity}"]]]]{comment}'
            templateC = '{global_line_prefix} Print["{label}: "<>ToString[N[{name}{index}/{divisor}]]]{comment}'
            templateD = '{global_line_prefix} Print["{label}: "<>FromCharacterCode[{name}{index}]]{comment}'
            templateE = '{global_line_prefix} Print["{label}: "<>StringJoin[Map[ToString,IntegerDigits[{name}{index},2,{bitmask_length}]]]]{comment}'
            templateF = '{global_line_prefix} Print["{label}: "<>ToString[{name}{index}]]{comment}'

            if self.get_label_name() == None:
                return []

            if self.get_cardinality() < 0:
                return [] # FIXME: streaming

            type_ = self.get_type()
            quantity = self.get_formatted_unit_name('{0}' + self.get_formatted_divisor('/{0}', cast=int)) # FIXME: move divisor out of quantity name
            divisor = self.get_formatted_divisor('{0}')
            bitmask_length = 0

            if type_ == 'string':
                template = templateA
            elif len(quantity) > 0:
                template = templateB
            elif len(divisor) > 0:
                template = templateC
            elif type_ == 'char':
                template = templateD
            elif ':bitmask:' in type_:
                template = templateE
                bitmask_length = int(type_.split(':')[2])
            else:
                template = templateF

            result = []

            for index in range(self.get_label_count()):
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              name=self.get_name().headless,
                                              label=self.get_label_name(index=index),
                                              quantity=quantity,
                                              index='{0}'.format(index + 1) if self.get_label_count() > 1 else '',
                                              divisor=divisor,
                                              bitmask_length=bitmask_length,
                                              comment=self.get_formatted_comment('(*{0}*)')))

        return result

class MathematicaExampleResult(common.ExampleResult):
    def get_mathematica_variable_name(self):
        name = self.get_name().headless

        if name == self.get_device().get_initial_name():
            name += 'U'

        return name

    def get_mathematica_prints(self, getter_call=None):
        if self.get_type().split(':')[-1] == 'constant':
            assert getter_call == None

            # FIXME: need to handle multiple labels
            assert self.get_label_count() == 1

            template = '{global_line_prefix}If[{name}=={constant_name},Print["{label}: {constant_title}"]]{global_line_suffix}{comment}'
            constant_group = self.get_constant_group()
            result = []

            for constant in constant_group.get_constants():
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              global_line_suffix=global_line_suffix,
                                              name=self.get_name().headless,
                                              label=self.get_label_name(),
                                              constant_name=constant.get_mathematica_source(),
                                              constant_title=constant.get_name().space,
                                              comment=self.get_formatted_comment('(*{0}*)')))

            result = ['\n'.join(result)]
        else:
            templateA = '{global_line_prefix}Print["{label}: "<>{value}{index}]{global_line_suffix}{comment}'
            templateB = '{global_line_prefix}Print["{label}: "<>ToString[N[Quantity[{value}{index},"{quantity}"]]]]{global_line_suffix}{comment}'
            templateC = '{global_line_prefix}Print["{label}: "<>ToString[N[{value}{index}/{divisor}]]]{global_line_suffix}{comment}'
            templateD = '{global_line_prefix}Print["{label}: "<>FromCharacterCode[{value}{index}]]{global_line_suffix}{comment}'
            templateE = '{global_line_prefix}Print["{label}: "<>StringJoin[Map[ToString,IntegerDigits[{value}{index},2,{bitmask_length}]]]]{global_line_suffix}{comment}'
            templateF = '{global_line_prefix}Print["{label}: "<>ToString[{value}{index}]]{global_line_suffix}{comment}'

            if self.get_label_name() == None:
                return []

            if self.get_cardinality() < 0:
                return [] # FIXME: streaming

            if getter_call != None:
                value = getter_call
            else:
                name = self.get_name().headless

                if name == self.get_device().get_initial_name():
                    name += 'U'

                value = name

            type_ = self.get_type()
            quantity = self.get_formatted_unit_name('{0}' + self.get_formatted_divisor('/{0}', cast=int)) # FIXME: move divisor out of quantity name
            divisor = self.get_formatted_divisor('{0}')
            bitmask_length = 0

            if type_ == 'string':
                template = templateA
            elif len(quantity) > 0:
                template = templateB
            elif len(divisor) > 0:
                template = templateC
            elif type_ == 'char':
                template = templateD
            elif ':bitmask:' in type_:
                template = templateE
                bitmask_length = int(type_.split(':')[2])
            else:
                template = templateF

            result = []

            for index in range(self.get_label_count()):
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              global_line_suffix=global_line_suffix,
                                              value=value,
                                              label=self.get_label_name(index=index),
                                              quantity=quantity,
                                              index='{0}'.format(index + 1) if self.get_label_count() > 1 else '',
                                              divisor=divisor,
                                              bitmask_length=bitmask_length,
                                              comment=self.get_formatted_comment('(*{0}*)')))

        return result

class MathematicaExampleGetterFunction(common.ExampleGetterFunction, MathematicaExampleArgumentsMixin):
    def get_mathematica_source(self):
        template1 = '{device_name}@{function_name}[{arguments}]'
        template2A = r"""{global_line_prefix}(*Get current {function_name_comment}*)
{global_line_prefix}{variable_declarations}={device_name}@{function_name_camel}[{arguments}]{global_line_suffix}

{prints}
"""
        template2B = r"""{global_line_prefix}(*Get current {function_name_comment}*)
{prints}
"""
        template2C = r"""{global_line_prefix}(*Get current {function_name_comment}*)
{global_line_prefix}{variable_declarations}{global_line_suffix}
{global_line_prefix}{device_name}@{function_name_camel}[{arguments}]{global_line_suffix}
{prints}
"""
        arguments = self.get_mathematica_arguments()
        results = self.get_results()

        if len(results) == 1 and results[0].get_type().split(':')[-1] != 'constant':
            getter_call = template1.format(global_line_prefix=global_line_prefix,
                                           device_name=self.get_device().get_initial_name(),
                                           function_name=self.get_name().camel,
                                           arguments=','.join(arguments))
        else:
            getter_call = None

        comments = []
        variable_names = []
        prints = []

        for result in results:
            variable_names.append(result.get_mathematica_variable_name())
            prints += result.get_mathematica_prints(getter_call)

        if getter_call == None and len(results) == 1:
            template2 = template2A
            variable_declarations = list(variable_names)
        elif len(variable_names) == 1:
            template2 = template2B
            variable_declarations = []
        else:
            template2 = template2C
            variable_declarations = ['{0}=0'.format(variable_name) for variable_name in variable_names]

        while None in prints:
            prints.remove(None)

        if len(prints) > 1:
            prints.insert(0, '')

        if len(variable_names) > 1:
            arguments += variable_names

        return template2.format(global_line_prefix=global_line_prefix,
                                global_line_suffix=global_line_suffix,
                                device_name=self.get_device().get_initial_name(),
                                function_name_camel=self.get_name().camel,
                                function_name_headless=self.get_name().headless,
                                function_name_comment=self.get_comment_name(),
                                variable_names=''.join(variable_names),
                                variable_declarations=';'.join(variable_declarations),
                                prints='\n'.join(prints),
                                arguments=','.join(arguments))

class MathematicaExampleSetterFunction(common.ExampleSetterFunction, MathematicaExampleArgumentsMixin):
    def get_mathematica_source(self):
        template = '{comment1}{global_line_prefix}{device_name}@{function_name}[{arguments}]{global_line_suffix}{comment2}\n'

        result = template.format(global_line_prefix=global_line_prefix,
                                 global_line_suffix=global_line_suffix,
                                 device_name=self.get_device().get_initial_name(),
                                 function_name=self.get_name().camel,
                                 arguments=',<BP>'.join(self.get_mathematica_arguments()),
                                 comment1=re.sub('\\(\\*[ ]*\\*\\)\n', '', self.get_formatted_comment1(global_line_prefix + '(*{0}*)\n', '\r', '*)\n' + global_line_prefix + '(*')),
                                 comment2=self.get_formatted_comment2('(*{0}*)', ''))

        return common.break_string(result, '@{}['.format(self.get_name().camel), space='')

class MathematicaExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_mathematica_source(self):
        template1A = r"""(*Callback function for {function_name_comment} callback*)
"""
        template1B = r"""{override_comment}
"""
        template2A = r"""{function_name_camel}CB[sender_{parameters}]:=
 Module[{{}},
{prints}{extra_message}
 ]

AddEventHandler[{device_name}@{function_name_camel}Callback,{function_name_camel}CB]
"""
        template2B = r"""{function_name_camel}CB[sender_{parameters}]:=
{prints}{extra_message}
AddEventHandler[{device_name}@{function_name_camel}Callback,{function_name_camel}CB]
"""
        override_comment = self.get_formatted_override_comment('(*{0}*)', None, '*)\n(*')

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B
            override_comment = re.sub('\\(\\*[ ]+\\*\\)\n', '', override_comment)

        parameters = []
        prints = []

        for parameter in self.get_parameters():
            parameters.append(parameter.get_mathematica_source())
            prints += parameter.get_mathematica_prints()

        while None in prints:
            prints.remove(None)

        extra_message = self.get_formatted_extra_message(' Print["{0}"]')

        if len(prints) > 1 or (len(prints) == 1 and len(extra_message) > 0) or sum([1 for p in prints if '\n' in p]) > 0:
            template2 = template2A
            prints = [' ' + prints for prints in prints]

            if len(extra_message) > 0:
                extra_message = ' ' + extra_message
        else:
            template2 = template2B

        if len(extra_message) > 0 and len(prints) > 0:
            extra_message = ';\n' + extra_message

        result = template1.format(function_name_comment=self.get_comment_name(),
                                  override_comment=override_comment) + \
                 template2.format(device_name=self.get_device().get_initial_name(),
                                  function_name_camel=self.get_name().camel,
                                  parameters=common.wrap_non_empty(',<BP>', ',<BP>'.join(parameters), ''),
                                  prints='\n'.join(prints).replace('\n', ';\n'),
                                  extra_message=extra_message)

        return common.break_string(result, '{}CB['.format(self.get_name().camel), space='')

class MathematicaExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction, MathematicaExampleArgumentsMixin):
    def get_mathematica_source(self):
        templateA = r"""(*Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)*)
{device_name}@Set{function_name_camel}Period[{arguments}{period_msec}]
"""
        templateB = r"""(*Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)*)
(*Note: The {function_name_comment} callback is only called every {period_sec_long}*)
(*if the {function_name_comment} has changed since the last call!*)
{device_name}@Set{function_name_camel}CallbackPeriod[{arguments}{period_msec}]
"""

        if self.get_device().get_name().space.startswith('IMU'):
            template = templateA # FIXME: special hack for IMU Brick (2.0) callback behavior and name mismatch
        else:
            template = templateB

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_name=self.get_device().get_initial_name(),
                               function_name_camel=self.get_name().camel,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ','.join(self.get_mathematica_arguments()), ','),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class MathematicaExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_mathematica_source(self):
        template = '{minimum},{maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class MathematicaExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction, MathematicaExampleArgumentsMixin):
    def get_mathematica_source(self):
        template = r"""(*Configure threshold for {function_name_comment} "{option_comment}"*)
option=Tinkerforge`{device_category}{device_name_camel}`THRESHOLDUOPTIONU{option_name_upper}
{device_name_initial}@Set{function_name_camel}CallbackThreshold[{arguments}option,{mininum_maximums}]
"""
        mininum_maximums = []

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_mathematica_source())

        option_name_uppers = {'o' : 'OUTSIDE', '<': 'SMALLER', '>': 'GREATER'}

        return template.format(device_category=self.get_device().get_category().camel,
                               device_name_camel=self.get_device().get_name().camel,
                               device_name_initial=self.get_device().get_initial_name(),
                               function_name_camel=self.get_name().camel,
                               function_name_under=self.get_name().under,
                               function_name_comment=self.get_comment_name(),
                               option_name_upper=option_name_uppers[self.get_option_char()],
                               option_comment=self.get_option_comment(),
                               arguments=common.wrap_non_empty('', ','.join(self.get_mathematica_arguments()), ','),
                               mininum_maximums=','.join(mininum_maximums))

class MathematicaExampleCallbackConfigurationFunction(common.ExampleCallbackConfigurationFunction, MathematicaExampleArgumentsMixin):
    def get_mathematica_source(self):
        templateA = r"""(*Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)*)
{device_name_initial}@Set{function_name_camel}CallbackConfiguration[{arguments}{period_msec}{value_has_to_change}]
"""
        templateB = r"""(*Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms) without a threshold*)
option=Tinkerforge`{device_category}{device_name_camel}`THRESHOLDUOPTIONU{option_name}
{device_name_initial}@Set{function_name_camel}CallbackConfiguration[{arguments}{period_msec}{value_has_to_change},option,{mininum_maximums}]
"""
        templateC = r"""(*Configure threshold for {function_name_comment} "{option_comment}"*)
(*with a debounce period of {period_sec_short} ({period_msec}ms)*)
option=Tinkerforge`{device_category}{device_name_camel}`THRESHOLDUOPTIONU{option_name}
{device_name_initial}@Set{function_name_camel}CallbackConfiguration[{arguments}{period_msec}{value_has_to_change},option,{mininum_maximums}]
"""

        if self.get_option_char() == None:
            template = templateA
        elif self.get_option_char() == 'x':
            template = templateB
        else:
            template = templateC

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        mininum_maximums = []

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_mathematica_source())

        option_names = {None: '', 'x': 'OFF', 'o' : 'OUTSIDE', '<': 'SMALLER', '>': 'GREATER'}

        return template.format(device_category=self.get_device().get_category().camel,
                               device_name_camel=self.get_device().get_name().camel,
                               device_name_initial=self.get_device().get_initial_name(),
                               function_name_camel=self.get_name().camel,
                               function_name_under=self.get_name().under,
                               function_name_comment=self.get_comment_name(),
                               option_name=option_names[self.get_option_char()],
                               option_comment=self.get_option_comment(),
                               arguments=common.wrap_non_empty('', ','.join(self.get_mathematica_arguments()), ','),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long,
                               value_has_to_change=common.wrap_non_empty(',', self.get_value_has_to_change('True', 'False', ''), ''),
                               mininum_maximums=','.join(mininum_maximums))

class MathematicaExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_mathematica_source(self):
        global global_line_prefix
        global global_line_suffix

        type_ = self.get_type()

        if type_ == 'empty':
            return ''
        elif type_ == 'debounce_period':
            template = r"""(*Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms)*)
{device_name}@SetDebouncePeriod[{period_msec}]
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_name=self.get_device().get_initial_name(),
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type_ == 'sleep':
            template = '{comment1}{global_line_prefix}Pause[{duration}]{global_line_suffix}{comment2}\n'
            duration = self.get_sleep_duration()

            if duration % 1000 == 0:
                duration //= 1000
            else:
                duration /= 1000.0

            return template.format(global_line_prefix=global_line_prefix,
                                   global_line_suffix=global_line_suffix,
                                   duration=duration,
                                   comment1=re.sub('\\(\\*[ ]*\\*\\)\n', '', self.get_formatted_sleep_comment1('(*{0}*)\n', '\r', '*)\n' + global_line_prefix + '(*')),
                                   comment2=self.get_formatted_sleep_comment2('(*{0}*)', ''))
        elif type_ == 'wait':
            return None
        elif type_ == 'loop_header':
            template = '{comment}For[i=0,i<{limit},i++,\n'
            global_line_prefix = ' '
            global_line_suffix = ';'

            return template.format(limit=self.get_loop_header_limit(),
                                   comment=re.sub('\\(\\*[ ]*\\*\\)\n', '', self.get_formatted_loop_header_comment('(*{0}*)\n', '', '*)\n' + global_line_prefix + '(*')))
        elif type_ == 'loop_footer':
            global_line_prefix = ''
            global_line_suffix = ''

            return '\b\r]\n'

class MathematicaExamplesGenerator(common.ExamplesGenerator):
    def get_bindings_name(self):
        return 'mathematica'

    def get_constant_class(self):
        return MathematicaConstant

    def get_example_class(self):
        return MathematicaExample

    def get_example_argument_class(self):
        return MathematicaExampleArgument

    def get_example_parameter_class(self):
        return MathematicaExampleParameter

    def get_example_result_class(self):
        return MathematicaExampleResult

    def get_example_getter_function_class(self):
        return MathematicaExampleGetterFunction

    def get_example_setter_function_class(self):
        return MathematicaExampleSetterFunction

    def get_example_callback_function_class(self):
        return MathematicaExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return MathematicaExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return MathematicaExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return MathematicaExampleCallbackThresholdFunction

    def get_example_callback_configuration_function_class(self):
        return MathematicaExampleCallbackConfigurationFunction

    def get_example_special_function_class(self):
        return MathematicaExampleSpecialFunction

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

        blacklist = [
            'lcd-16x2-bricklet/unicode',
            'lcd-20x4-bricklet/unicode',
            'nfc-bricklet/enumlate-ndef'
        ]

        for example in examples:
            filename = 'Example{0}.nb.txt'.format(example.get_name().camel)
            filepath = os.path.join(examples_dir, filename)

            if device.get_git_name() + '/' + example.get_name().dash in blacklist:
                print('  - ' + filename + ' \033[01;35m(blacklisted, skipped)\033[0m')
                continue

            if example.is_incomplete():
                if os.path.exists(filepath) and self.skip_existing_incomplete_example:
                    print('  - ' + filename + ' \033[01;35m(incomplete, skipped)\033[0m')
                    continue
                else:
                    print('  - ' + filename + ' \033[01;31m(incomplete)\033[0m')
            else:
                print('  - ' + filename)

            with open(filepath, 'w') as f:
                f.write(example.get_mathematica_source())

            txt2nb(filepath)

def generate(root_dir):
    common.generate(root_dir, 'en', MathematicaExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
