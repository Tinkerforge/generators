#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Delphi/Lazarus Examples Generator
Copyright (C) 2015-2018 Matthias Bolte <matthias@tinkerforge.com>

generate_delphi_examples.py: Generator for Delphi/Lazarus examples

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
import delphi_common

global_line_prefix = ''

class DelphiPrintfFormatMixin(object):
    def get_delphi_printf_format(self):
        type_ = self.get_type()

        if type_ in ['char', 'string']:
            return '%s'
        elif type_.split(':')[0] != 'float' and self.get_divisor() == None:
            return '%d'
        else:
            return '%f' # FIXME: use %.<decimals>f instead, because %f defaults to %.2f

class DelphiConstant(common.Constant):
    def get_delphi_source(self):
        template = '{device_upper_case_category}_{device_upper_case_name}_{constant_group_upper_case_name}_{constant_upper_case_name}'

        return template.format(device_upper_case_category=self.get_device().get_upper_case_category(),
                               device_upper_case_name=self.get_device().get_upper_case_name(),
                               constant_group_upper_case_name=self.get_constant_group().get_upper_case_name(),
                               constant_upper_case_name=self.get_upper_case_name())

class DelphiExample(common.Example):
    def get_delphi_source(self):
        template = r"""program Example{example_camel_case_name};{incomplete}{description}

{{$ifdef MSWINDOWS}}{{$apptype CONSOLE}}{{$endif}}
{{$ifdef FPC}}{{$mode OBJFPC}}{{$H+}}{{$endif}}

uses
  SysUtils, IPConnection, {device_camel_case_category}{device_camel_case_name};

type
  TExample = class
  private
    ipcon: TIPConnection;
    {device_initial_name}: T{device_camel_case_category}{device_camel_case_name};
  public{prototypes}
    procedure Execute;
  end;

const
  HOST = 'localhost';
  PORT = 4223;
  UID = '{dummy_uid}'; {{ Change {dummy_uid} to the UID of your {device_long_display_name} }}

var
  e: TExample;
{procedures}
procedure TExample.Execute;{variable_declarations}
begin
  {{ Create IP connection }}
  ipcon := TIPConnection.Create;

  {{ Create device object }}
  {device_initial_name} := T{device_camel_case_category}{device_camel_case_name}.Create(UID, ipcon);

  {{ Connect to brickd }}
  ipcon.Connect(HOST, PORT);
  {{ Don't use device before ipcon is connected }}
{sources}
  WriteLn('Press key to exit');
  ReadLn;{cleanups}
  ipcon.Destroy; {{ Calls ipcon.Disconnect internally }}
end;

begin
  e := TExample.Create;
  e.Execute;
  e.Destroy;
end.
"""

        if self.is_incomplete():
            incomplete = '\n\n{ FIXME: This example is incomplete }'
        else:
            incomplete = ''

        if self.get_description() != None:
            description = '\n\n{{ {0} }}'.format(self.get_description().replace('\n', '\n  '))
        else:
            description = ''

        prototypes = []
        procedures = []
        variable_declarations = []
        sources = []
        cleanups = []

        for function in self.get_functions():
            prototypes.append(function.get_delphi_prototype())
            procedures.append(function.get_delphi_procedure())
            variable_declarations += function.get_delphi_variable_declarations()
            sources.append(function.get_delphi_source())

        for cleanup in self.get_cleanups():
            prototypes.append(cleanup.get_delphi_prototype())
            procedures.append(cleanup.get_delphi_procedure())
            variable_declarations += cleanup.get_delphi_variable_declarations()
            cleanups.append(cleanup.get_delphi_source())

        while None in prototypes:
            prototypes.remove(None)

        while None in procedures:
            procedures.remove(None)

        while None in sources:
            sources.remove(None)

        if len(sources) == 0:
            sources = ['  { TODO: Add example code here }\n']

        while None in cleanups:
            cleanups.remove(None)

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
            variable_declarations.append('{0}: {1}'.format(',<BP>'.join(merged_variable_declaration[1]),
                                                           merged_variable_declaration[0]))

        if len(variable_declarations) > 0:
            variable_declarations = common.break_string('var ' + ';<BP>'.join(variable_declarations), 'var ')
        else:
            variable_declarations = ''

        return template.format(incomplete=incomplete,
                               description=description,
                               example_camel_case_name=self.get_camel_case_name(),
                               device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               device_initial_name=self.get_device().get_initial_name(),
                               device_long_display_name=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               prototypes=common.wrap_non_empty('\n', '\n'.join(prototypes), ''),
                               procedures=common.wrap_non_empty('\n', '\n'.join(procedures), ''),
                               variable_declarations=common.wrap_non_empty('\n', variable_declarations, ';'),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), ''))

class DelphiExampleArgument(common.ExampleArgument):
    def get_delphi_source(self):
        type_ = self.get_type()
        value = self.get_value()

        if type_ == 'bool':
            if value:
                return 'true'
            else:
                return 'false'
        elif type_ in ['char', 'string']:
            return "'{0}'".format(value)
        elif ':bitmask:' in type_:
            return common.make_c_like_bitmask(value, shift='{0} shl {1}', combine='({0}) or ({1})')
        elif type_.endswith(':constant'):
            return self.get_value_constant().get_delphi_source()
        else:
            return str(value)

class DelphiExampleArgumentsMixin(object):
    def get_delphi_arguments(self):
        return [argument.get_delphi_source() for argument in self.get_arguments()]

class DelphiExampleParameter(common.ExampleParameter, DelphiPrintfFormatMixin):
    def get_delphi_source(self):
        templateA = 'const {headless_camel_case_name}: {type0}'
        templateB = 'const {headless_camel_case_name}: TArray0To{array_end}Of{type1}'
        templateC = 'const {headless_camel_case_name}: array of {type0}'

        if self.get_cardinality() == 1:
            template = templateA
        elif self.get_cardinality() > 1:
            template = templateB
        else: # cardinality < 0
            template = templateC

        headless_camel_case_name = self.get_headless_camel_case_name()

        if headless_camel_case_name == self.get_device().get_initial_name():
            headless_camel_case_name += '_'

        return template.format(type0=delphi_common.get_delphi_type(self.get_type().split(':')[0])[0],
                               type1=delphi_common.get_delphi_type(self.get_type().split(':')[0])[1],
                               array_end=self.get_cardinality() - 1,
                               headless_camel_case_name=headless_camel_case_name)

    def get_delphi_write_lns(self):
        # FIXME: the parameter type can indicate a bitmask, but there is no easy way in Delphi
        #        to format an integer in base-2, that doesn't require open-coding it with several
        #        lines of code. so just print the integer in base-10 the normal way
        template = "  WriteLn(Format('{label_name}: {printf_format}{unit_name}', [{headless_camel_case_name}{index}{divisor}]));{comment}"

        if self.get_label_name() == None:
            return []

        if self.get_cardinality() < 0:
            return [] # FIXME: streaming

        headless_camel_case_name = self.get_headless_camel_case_name()

        if headless_camel_case_name == self.get_device().get_initial_name():
            headless_camel_case_name += '_'

        result = []

        for index in range(self.get_label_count()):
            result.append(template.format(headless_camel_case_name=headless_camel_case_name,
                                          label_name=self.get_label_name(index=index).replace('%', '%%'),
                                          index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                          divisor=self.get_formatted_divisor('/{0}'),
                                          printf_format=self.get_delphi_printf_format(),
                                          unit_name=self.get_formatted_unit_name(' {0}').replace('%', '%%'),
                                          comment=self.get_formatted_comment(' {{ {0} }}')))

        return result

class DelphiExampleResult(common.ExampleResult, DelphiPrintfFormatMixin):
    def get_delphi_variable_declaration(self):
        templateA = '{type0}'
        templateB = 'TArray0To{array_end}Of{type1}'
        templateC = 'array of {type0}'

        if self.get_cardinality() == 1:
            template = templateA
        elif self.get_cardinality() > 1:
            template = templateB
        else: # cardinality < 0
            template = templateC

        headless_camel_case_name = self.get_headless_camel_case_name()

        if headless_camel_case_name == self.get_device().get_initial_name():
            headless_camel_case_name += '_'

        return template.format(type0=delphi_common.get_delphi_type(self.get_type().split(':')[0])[0],
                               type1=delphi_common.get_delphi_type(self.get_type().split(':')[0])[1],
                               array_end=self.get_cardinality() - 1), headless_camel_case_name

    def get_delphi_variable_name(self):
        headless_camel_case_name = self.get_headless_camel_case_name()

        if headless_camel_case_name == self.get_device().get_initial_name():
            headless_camel_case_name += '_'

        return headless_camel_case_name

    def get_delphi_write_lns(self):
        # FIXME: the result type can indicate a bitmask, but there is no easy way in Delphi
        #        to format an integer in base-2, that doesn't require open-coding it with several
        #        lines of code. so just print the integer in base-10 the normal way
        template = "  WriteLn(Format('{label_name}: {printf_format}{unit_name}', [{headless_camel_case_name}{index}{divisor}]));{comment}"

        if self.get_label_name() == None:
            return []

        if self.get_cardinality() < 0:
            return [] # FIXME: streaming

        headless_camel_case_name = self.get_headless_camel_case_name()

        if headless_camel_case_name == self.get_device().get_initial_name():
            headless_camel_case_name += '_'

        result = []

        for index in range(self.get_label_count()):
            result.append(template.format(headless_camel_case_name=headless_camel_case_name,
                                          label_name=self.get_label_name(index=index).replace('%', '%%'),
                                          index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                          divisor=self.get_formatted_divisor('/{0}'),
                                          printf_format=self.get_delphi_printf_format(),
                                          unit_name=self.get_formatted_unit_name(' {0}').replace('%', '%%'),
                                          comment=self.get_formatted_comment(' {{ {0} }}')))

        return result

class DelphiExampleGetterFunction(common.ExampleGetterFunction, DelphiPrintfFormatMixin, DelphiExampleArgumentsMixin):
    def get_delphi_prototype(self):
        return None

    def get_delphi_procedure(self):
        return None

    def get_delphi_variable_declarations(self):
        variable_declarations = []

        for result in self.get_results():
            variable_declarations.append(result.get_delphi_variable_declaration())

        return variable_declarations

    def get_delphi_source(self):
        templateA = r"""  {{ Get current {function_comment_name} }}
  {variable_names} := {device_initial_name}.{function_camel_case_name}{arguments};
{write_lns}
"""
        templateB = r"""  {{ Get current {function_comment_name} }}
  {device_initial_name}.{function_camel_case_name}{arguments};
{write_lns}
"""
        variable_names = []
        write_lns = []

        for result in self.get_results():
            variable_names.append(result.get_delphi_variable_name())
            write_lns += result.get_delphi_write_lns()

        if len(variable_names) == 1:
            template = templateA
        else:
            template = templateB

        while None in write_lns:
            write_lns.remove(None)

        if len(write_lns) > 1:
            write_lns.insert(0, '')

        arguments = self.get_delphi_arguments()

        if len(variable_names) > 1:
            arguments += variable_names
            variable_names = []

        result = template.format(device_initial_name=self.get_device().get_initial_name(),
                                 function_camel_case_name=self.get_camel_case_name(),
                                 function_comment_name=self.get_comment_name(),
                                 variable_names=''.join(variable_names),
                                 write_lns='\n'.join(write_lns),
                                 arguments=common.wrap_non_empty('(', ',<BP>'.join(arguments), ')'))

        return common.break_string(result, '.{0}('.format(self.get_camel_case_name()))

class DelphiExampleSetterFunction(common.ExampleSetterFunction, DelphiExampleArgumentsMixin):
    def get_delphi_prototype(self):
        return None

    def get_delphi_procedure(self):
        return None

    def get_delphi_variable_declarations(self):
        return []

    def get_delphi_source(self):
        template = '{comment1}{global_line_prefix}  {device_initial_name}.{function_camel_case_name}{arguments};{comment2}\n'

        result = template.format(global_line_prefix=global_line_prefix,
                                 device_initial_name=self.get_device().get_initial_name(),
                                 function_camel_case_name=self.get_camel_case_name(),
                                 arguments=common.wrap_non_empty('(', ',<BP>'.join(self.get_delphi_arguments()), ')'),
                                 comment1=self.get_formatted_comment1(global_line_prefix + '  {{ {0} }}\n', '\r', '\n' + global_line_prefix + '    '),
                                 comment2=self.get_formatted_comment2(' {{ {0} }}', ''))

        return common.break_string(result, '{}('.format(self.get_camel_case_name()))

class DelphiExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_delphi_prototype(self):
        template = '    procedure {function_camel_case_name}CB(sender: T{device_camel_case_category}{device_camel_case_name}{parameters});'
        parameters = []

        for parameter in self.get_parameters():
            parameters.append(parameter.get_delphi_source())

        result = template.format(device_camel_case_category=self.get_device().get_camel_case_category(),
                                 device_camel_case_name=self.get_device().get_camel_case_name(),
                                 function_camel_case_name=self.get_camel_case_name(),
                                 parameters=common.wrap_non_empty(';<BP>', ';<BP>'.join(parameters), ''))

        return common.break_string(result, '{}CB('.format(self.get_camel_case_name()))

    def get_delphi_procedure(self):
        template1A = r"""{{ Callback procedure for {function_comment_name} callback }}
"""
        template1B = r"""{override_comment}
"""
        template2 = r"""procedure TExample.{function_camel_case_name}CB(sender: T{device_camel_case_category}{device_camel_case_name}{parameters});
begin
{write_lns}{extra_message}
end;
"""
        override_comment = self.get_formatted_override_comment('{{ {0} }}', None, '\n  ')

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B

        parameters = []
        write_lns = []

        for parameter in self.get_parameters():
            parameters.append(parameter.get_delphi_source())
            write_lns += parameter.get_delphi_write_lns()

        while None in write_lns:
            write_lns.remove(None)

        if len(write_lns) > 1:
            write_lns.append("  WriteLn('');")

        extra_message = self.get_formatted_extra_message("  WriteLn('{0}');")

        if len(extra_message) > 0 and len(write_lns) > 0:
            extra_message = '\n' + extra_message

        result = template1.format(function_comment_name=self.get_comment_name(),
                                  override_comment=override_comment) + \
                 template2.format(device_camel_case_category=self.get_device().get_camel_case_category(),
                                  device_camel_case_name=self.get_device().get_camel_case_name(),
                                  function_camel_case_name=self.get_camel_case_name(),
                                  parameters=common.wrap_non_empty(';<BP>', ';<BP>'.join(parameters), ''),
                                  write_lns='\n'.join(write_lns),
                                  extra_message=extra_message)

        return common.break_string(result, '{}CB('.format(self.get_camel_case_name()))

    def get_delphi_variable_declarations(self):
        return []

    def get_delphi_source(self):
        template = r"""  {{ Register {function_comment_name}<BP>callback<BP>to<BP>procedure<BP>{function_camel_case_name}CB }}
  {device_initial_name}.On{function_camel_case_name} := {{$ifdef FPC}}@{{$endif}}{function_camel_case_name}CB;
"""

        result = template.format(device_initial_name=self.get_device().get_initial_name(),
                                 function_camel_case_name=self.get_camel_case_name(),
                                 function_comment_name=self.get_comment_name())

        return common.break_string(result, '{ ')

class DelphiExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction, DelphiExampleArgumentsMixin):
    def get_delphi_prototype(self):
        return None

    def get_delphi_procedure(self):
        return None

    def get_delphi_variable_declarations(self):
        return []

    def get_delphi_source(self):
        templateA = r"""  {{ Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms) }}
  {device_initial_name}.Set{function_camel_case_name}Period({arguments}{period_msec});
"""
        templateB = r"""  {{ Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
    Note: The {function_comment_name} callback is only called every {period_sec_long}
          if the {function_comment_name} has changed since the last call! }}
  {device_initial_name}.Set{function_camel_case_name}CallbackPeriod({arguments}{period_msec});
"""

        if self.get_device().get_underscore_name().startswith('imu'):
            template = templateA # FIXME: special hack for IMU Brick (2.0) callback behavior and name mismatch
        else:
            template = templateB

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_camel_case_name=self.get_camel_case_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_delphi_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class DelphiExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_delphi_source(self):
        template = '{minimum}, {maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class DelphiExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction, DelphiPrintfFormatMixin, DelphiExampleArgumentsMixin):
    def get_delphi_prototype(self):
        return None

    def get_delphi_procedure(self):
        return None

    def get_delphi_variable_declarations(self):
        return []

    def get_delphi_source(self):
        template = r"""  {{ Configure threshold for {function_comment_name} "{option_comment}" }}
  {device_initial_name}.Set{function_camel_case_name}CallbackThreshold({arguments}'{option_char}', {mininum_maximums});
"""
        mininum_maximums = []

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_delphi_source())

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_camel_case_name=self.get_camel_case_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_delphi_arguments()), ', '),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               mininum_maximums=', '.join(mininum_maximums))

class DelphiExampleCallbackConfigurationFunction(common.ExampleCallbackConfigurationFunction, DelphiPrintfFormatMixin, DelphiExampleArgumentsMixin):
    def get_delphi_prototype(self):
        return None

    def get_delphi_procedure(self):
        return None

    def get_delphi_variable_declarations(self):
        return []

    def get_delphi_source(self):
        templateA = r"""  {{ Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms) }}
  {device_initial_name}.Set{function_camel_case_name}CallbackConfiguration({arguments}{period_msec}, false);
"""
        templateB = r"""  {{ Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms) without a threshold }}
  {device_initial_name}.Set{function_camel_case_name}CallbackConfiguration({arguments}{period_msec}, false, '{option_char}', {mininum_maximums});
"""
        templateC = r"""  {{ Configure threshold for {function_comment_name} "{option_comment}"
    with a debounce period of {period_sec_short} ({period_msec}ms) }}
  {device_initial_name}.Set{function_camel_case_name}CallbackConfiguration({arguments}{period_msec}, false, '{option_char}', {mininum_maximums});
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
            mininum_maximums.append(mininum_maximum.get_delphi_source())

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_camel_case_name=self.get_camel_case_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_delphi_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long,
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               mininum_maximums=', '.join(mininum_maximums))

class DelphiExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_delphi_prototype(self):
        return None

    def get_delphi_procedure(self):
        return None

    def get_delphi_variable_declarations(self):
        if self.get_type() == 'loop_header':
            return [('integer', 'i')]
        else:
            return []

    def get_delphi_source(self):
        global global_line_prefix

        type_ = self.get_type()

        if type_ == 'empty':
            return ''
        elif type_ == 'debounce_period':
            template = r"""  {{ Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms) }}
  {device_initial_name}.SetDebouncePeriod({period_msec});
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_initial_name=self.get_device().get_initial_name(),
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type_ == 'sleep':
            template = '{comment1}{global_line_prefix}  Sleep({duration});{comment2}\n'

            return template.format(global_line_prefix=global_line_prefix,
                                   duration=self.get_sleep_duration(),
                                   comment1=self.get_formatted_sleep_comment1(global_line_prefix + '  {{ {0} }}\n', '\r', '\n' + global_line_prefix + '    '),
                                   comment2=self.get_formatted_sleep_comment2(' {{ {0} }}', ''))
        elif type_ == 'wait':
            return None
        elif type_ == 'loop_header':
            template = '{comment}  for i := 0 to {limit} do begin\n'
            global_line_prefix = '  '

            return template.format(limit=self.get_loop_header_limit() - 1,
                                   comment=self.get_formatted_loop_header_comment('  {{ {0} }}\n', '', '\n    '))
        elif type_ == 'loop_footer':
            global_line_prefix = ''

            return '\r  end;\n'

class DelphiExamplesGenerator(common.ExamplesGenerator):
    def get_bindings_name(self):
        return 'delphi'

    def get_constant_class(self):
        return DelphiConstant

    def get_example_class(self):
        return DelphiExample

    def get_example_argument_class(self):
        return DelphiExampleArgument

    def get_example_parameter_class(self):
        return DelphiExampleParameter

    def get_example_result_class(self):
        return DelphiExampleResult

    def get_example_getter_function_class(self):
        return DelphiExampleGetterFunction

    def get_example_setter_function_class(self):
        return DelphiExampleSetterFunction

    def get_example_callback_function_class(self):
        return DelphiExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return DelphiExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return DelphiExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return DelphiExampleCallbackThresholdFunction

    def get_example_callback_configuration_function_class(self):
        return DelphiExampleCallbackConfigurationFunction

    def get_example_special_function_class(self):
        return DelphiExampleSpecialFunction

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
            filename = 'Example{0}.pas'.format(example.get_camel_case_name())
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
                f.write(example.get_delphi_source())

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', DelphiExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
