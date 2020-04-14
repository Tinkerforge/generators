#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JavaScript Examples Generator
Copyright (C) 2015-2020 Matthias Bolte <matthias@tinkerforge.com>

generate_javascript_examples.py: Generator for JavaScript examples

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

sys.path.append(os.path.split(os.getcwd())[0])
import common
import javascript_common

global_line_prefix = ''
global_output_prefix = None
global_output_suffix = None
global_callback_output_suffix = None
global_last_sleep_function = None
global_sleep_duration_offset = 0
global_inside_for_loop = False
global_total_sleep_duration = 0

def end_previous_sleep_function(default):
    global global_line_prefix
    global global_last_sleep_function
    global global_sleep_duration_offset
    global global_total_sleep_duration

    result = default

    if global_last_sleep_function != None:
        global_line_prefix = ' '*(len(global_line_prefix) - 4)

        if global_inside_for_loop:
            template = '\r{global_line_prefix}        }}, <<<total_sleep_duration>>> * i + {duration});{comment2}\n'
        else:
            template = '\r{global_line_prefix}        }}, {duration});{comment2}\n'

        result = template.format(global_line_prefix=global_line_prefix,
                                 duration=global_sleep_duration_offset + global_last_sleep_function.get_sleep_duration(),
                                 comment2=global_last_sleep_function.get_formatted_sleep_comment2(' // {0}', ''))
        global_sleep_duration_offset += global_last_sleep_function.get_sleep_duration()
        global_total_sleep_duration = max(global_total_sleep_duration, global_sleep_duration_offset)
        global_last_sleep_function = None

    return result

class JavaScriptConstant(common.Constant):
    def get_javascript_source(self):
        template = 'Tinkerforge.{device_category}{device_name}.{constant_group_name}_{constant_name}'

        return template.format(device_category=self.get_device().get_category().camel,
                               device_name=self.get_device().get_name().camel,
                               constant_group_name=self.get_constant_group().get_name().upper,
                               constant_name=self.get_name().upper)

class JavaScriptExample(common.Example):
    def get_nodejs_source(self):
        global global_line_prefix
        global global_output_prefix
        global global_output_suffix
        global global_callback_output_suffix
        global global_last_sleep_function
        global global_sleep_duration_offset
        global global_inside_for_loop
        global global_total_sleep_duration

        global_line_prefix = ''
        global_output_prefix = 'console.log('
        global_output_suffix = ')'
        global_callback_output_suffix = ''
        global_last_sleep_function = None
        global_sleep_duration_offset = 0
        global_inside_for_loop = False
        global_total_sleep_duration = 0

        template = r"""var Tinkerforge = require('tinkerforge');{incomplete}{description}

var HOST = 'localhost';
var PORT = 4223;
var UID = '{dummy_uid}'; // Change {dummy_uid} to the UID of your {device_name_long_display}

var ipcon = new Tinkerforge.IPConnection(); // Create IP connection
var {device_name_initial} = new Tinkerforge.{device_category}{device_name_camel}(UID, ipcon); // Create device object

ipcon.connect(HOST, PORT,
    function (error) {{
        console.log('Error: ' + error);
    }}
); // Connect to brickd
// Don't use device before ipcon is connected
{functions}
console.log('Press key to exit');
process.stdin.on('data',
    function (data) {{
{cleanups}
    }}
);
"""
        template_connected = r"""ipcon.on(Tinkerforge.IPConnection.CALLBACK_CONNECTED,
    function (connectReason) {{
{sources}    }}
);
"""

        if self.is_incomplete():
            incomplete = '\n\n// FIXME: This example is incomplete'
        else:
            incomplete = ''

        if self.get_description() != None:
            description = '\n\n// {0}'.format(self.get_description().replace('\n', '\n// '))
        else:
            description = ''

        functions = []
        sources = []
        cleanups = []

        for function in self.get_functions():
            functions.append(function.get_javascript_function())
            sources.append(function.get_javascript_source())

        if len(sources) == 0:
            sources = ['        // TODO: Add example code here\n']
        else:
            sources.append(end_previous_sleep_function(None))

        for cleanup in self.get_cleanups():
            functions.append(cleanup.get_javascript_function())
            cleanups.append(cleanup.get_javascript_source())

        cleanups.append('{global_line_prefix}        ipcon.disconnect();\n\r'.format(global_line_prefix=global_line_prefix))
        cleanups.append('{global_line_prefix}        process.exit(0);\n'.format(global_line_prefix=global_line_prefix))
        cleanups.append(end_previous_sleep_function(None))

        while None in functions:
            functions.remove(None)

        while None in sources:
            sources.remove(None)

        if len(sources) > 0:
            connected = template_connected.format(sources='\n'.join(sources).replace('\n\r', '').replace('\xFF\n', '').replace('\xFF', '').lstrip('\r'))
            functions = [connected] + functions

        while None in cleanups:
            cleanups.remove(None)

        return template.format(incomplete=incomplete,
                               description=description,
                               device_category=self.get_device().get_category().camel,
                               device_name_camel=self.get_device().get_name().camel,
                               device_name_initial=self.get_device().get_initial_name(),
                               device_name_long_display=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               functions=common.wrap_non_empty('\n', '\n'.join(functions), ''),
                               cleanups='\n'.join(cleanups).replace('\n\r', '').replace('\xFF\n', '').replace('\xFF', '').lstrip('\r').rstrip('\n')).replace('<<<total_sleep_duration>>>', str(global_total_sleep_duration)).replace("console.log('');", "console.log();")

    def get_html_source(self):
        global global_line_prefix
        global global_output_prefix
        global global_output_suffix
        global global_callback_output_suffix
        global global_last_sleep_function
        global global_sleep_duration_offset
        global global_inside_for_loop
        global global_total_sleep_duration

        global_line_prefix = ''
        global_output_prefix = 'textArea.value += '
        global_output_suffix = " + '\\n'"
        global_callback_output_suffix = '\n        textArea.scrollTop = textArea.scrollHeight;'
        global_last_sleep_function = None
        global_sleep_duration_offset = 0
        global_inside_for_loop = False
        global_total_sleep_duration = 0

        template = r"""<!DOCTYPE html>{incomplete}{description}
<html>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <head>
        <title>Tinkerforge | JavaScript Example</title>
    </head>
    <body>
        <div style="text-align:center;">
            <h1>{device_name_long_display} {example_name} Example</h1>
            <p>
                <input value="localhost" id="host" type="text" size="20">:
                <input value="4280" id="port" type="text" size="5">,
                <input value="uid" id="uid" type="text" size="5">
                <input value="Start Example" id="start" type="button" onclick="startExample();">
            </p>
            <p>
                <textarea readonly id="text" cols="80" rows="24" style="resize:none;"
                          >Press "Start Example" to begin ...</textarea>
            </p>
        </div>
        <script src="./Tinkerforge.js" type='text/javascript'></script>
        <script type='text/javascript'>
            var ipcon;
            var textArea = document.getElementById("text");
            function startExample() {{
                textArea.value = "";
                var HOST = document.getElementById("host").value;
                var PORT = parseInt(document.getElementById("port").value);
                var UID = document.getElementById("uid").value;
                if(ipcon !== undefined) {{
                    ipcon.disconnect();
                }}
                ipcon = new Tinkerforge.IPConnection(); // Create IP connection
                var {device_name_initial} = new Tinkerforge.{device_category}{device_name_camel}(UID, ipcon); // Create device object
                ipcon.connect(HOST, PORT,
                    function(error) {{
                        textArea.value += 'Error: ' + error + '\n';
                    }}
                ); // Connect to brickd
                // Don't use device before ipcon is connected
{functions}
            }}
        </script>
    </body>
</html>
"""
        template_connected = r"""ipcon.on(Tinkerforge.IPConnection.CALLBACK_CONNECTED,
    function (connectReason) {{
{sources}    }}
);
"""

        if self.is_incomplete():
            incomplete = '\n\n<!-- FIXME: This example is incomplete -->\n'
        else:
            incomplete = ''

        if self.get_description() != None:
            description = '\n\n<!-- {0} -->\n'.format(self.get_description().replace('\n', '\n     '))
        else:
            description = ''

        functions = []
        sources = []

        for function in self.get_functions():
            functions.append(function.get_javascript_function())
            sources.append(function.get_javascript_source())

        if len(sources) == 0:
            sources = ['        // TODO: Add example code here\n']
        else:
            sources.append(end_previous_sleep_function(None))

        while None in functions:
            functions.remove(None)

        while None in sources:
            sources.remove(None)

        if len(sources) > 0:
            connected = template_connected.format(sources='\n'.join(sources).replace('\n\r', '').replace('\xFF\n', '').replace('\xFF', '').lstrip('\r'))
            functions = [connected] + functions

        return template.format(incomplete=incomplete,
                               description=description,
                               example_name=self.get_name().space,
                               device_name_long_display=self.get_device().get_long_display_name(),
                               device_category=self.get_device().get_category().camel,
                               device_name_camel=self.get_device().get_name().camel,
                               device_name_initial=self.get_device().get_initial_name(),
                               functions=common.wrap_non_empty('\n                ', '\n                '.join('\n'.join(functions).split('\n')), '').rstrip().replace('\n                \n', '\n\n')).replace('<<<total_sleep_duration>>>', str(global_total_sleep_duration))

class JavaScriptExampleArgument(common.ExampleArgument):
    def get_javascript_source(self):
        type_ = self.get_type()

        def helper(value):
            if type_ == 'float':
                return common.format_float(value)
            elif type_ == 'bool':
                return str(bool(value)).lower()
            elif type_ in ['char', 'string']:
                return "'{0}'".format(value.replace("'", "\\'"))
            elif ':bitmask:' in type_:
                return common.make_c_like_bitmask(value)
            elif type_.endswith(':constant'):
                return self.get_value_constant(value).get_javascript_source()
            else:
                return str(value)

        value = self.get_value()

        if isinstance(value, list):
            return '[{0}]'.format(', '.join([helper(item) for item in value]))

        return helper(value)

class JavaScriptExampleArgumentsMixin(object):
    def get_javascript_arguments(self):
        return [argument.get_javascript_source() for argument in self.get_arguments()]

class JavaScriptExampleParameter(common.ExampleParameter):
    def get_javascript_source(self):
        return self.get_name().headless

    def get_javascript_outputs(self):
        if self.get_type().split(':')[-1] == 'constant':
            if self.get_label_name() == None:
                return []

            # FIXME: need to handle multiple labels
            assert self.get_label_count() == 1

            template = "        {else_}if({name} === {constant_name}) {{\n            {global_output_prefix}'{label}: {constant_title}\xFE'{global_output_suffix};{comment}\n        }}"
            constant_group = self.get_constant_group()
            result = []

            for constant in constant_group.get_constants():
                result.append(template.format(else_='else ' if len(result) > 0 else '',
                                              global_output_prefix=global_output_prefix,
                                              global_output_suffix=global_output_suffix,
                                              name=self.get_name().headless,
                                              label=self.get_label_name(),
                                              constant_name=constant.get_javascript_source(),
                                              constant_title=constant.get_name().space,
                                              comment=self.get_formatted_comment(' // {0}')))

            result = ['\r' + '\n'.join(result).replace("\xFE' + '", '').replace('\xFE', '') + '\r']
        else:
            template = "        {global_output_prefix}'{label}: ' + {to_binary_prefix}{name}{index}{divisor}{to_binary_suffix}{unit}{global_output_suffix};{comment}"

            if self.get_label_name() == None:
                return []

            if self.get_cardinality() < 0:
                return [] # FIXME: streaming

            divisor = self.get_formatted_divisor('/{0}')

            # FIXME: toString(2) doesn't support leading zeros. therefore,
            #        the result is not padded to the requested number of digits
            if ':bitmask:' in self.get_type():
                if len(divisor) > 0:
                    to_binary_prefix = '('
                    to_binary_suffix = ').toString(2)'
                else:
                    to_binary_prefix = ''
                    to_binary_suffix = '.toString(2)'
            else:
                to_binary_prefix = ''
                to_binary_suffix = ''

            result = []

            for index in range(self.get_label_count()):
                result.append(template.format(global_output_prefix=global_output_prefix,
                                              global_output_suffix=global_output_suffix,
                                              name=self.get_name().headless,
                                              label=self.get_label_name(index=index),
                                              index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                              divisor=divisor,
                                              unit=self.get_formatted_unit_name(" + ' {0}\xFE'"),
                                              to_binary_prefix=to_binary_prefix,
                                              to_binary_suffix=to_binary_suffix,
                                              comment=self.get_formatted_comment(' // {0}')).replace("\xFE' + '", '').replace("\xFE", ''))

        return result

class JavaScriptExampleResult(common.ExampleResult):
    def get_javascript_source(self):
        return self.get_name().headless

    def get_javascript_outputs(self):
        if self.get_type().split(':')[-1] == 'constant':
            # FIXME: need to handle multiple labels
            assert self.get_label_count() == 1

            template = "                {else_}if({name} === {constant_name}) {{\n                    {global_output_prefix}'{label}: {constant_title}\xFE'{global_output_suffix};{comment}\n                }}"
            constant_group = self.get_constant_group()
            result = []

            for constant in constant_group.get_constants():
                result.append(template.format(else_='else ' if len(result) > 0 else '',
                                              global_output_prefix=global_output_prefix,
                                              global_output_suffix=global_output_suffix,
                                              name=self.get_name().headless,
                                              label=self.get_label_name(),
                                              constant_name=constant.get_javascript_source(),
                                              constant_title=constant.get_name().space,
                                              comment=self.get_formatted_comment(' // {0}')).replace("\xFE' + '", '').replace("\xFE", ''))

            result = ['\r' + '\n'.join(result) + '\r']
        else:
            template = "{global_line_prefix}                {global_output_prefix}'{label}: ' + {to_binary_prefix}{name}{index}{divisor}{to_binary_suffix}{unit}{global_output_suffix};{comment}"

            if self.get_label_name() == None:
                return []

            if self.get_cardinality() < 0:
                return [] # FIXME: streaming

            divisor = self.get_formatted_divisor('/{0}')

            # FIXME: toString(2) doesn't support leading zeros. therefore,
            #        the result is not padded to the requested number of digits
            if ':bitmask:' in self.get_type():
                if len(divisor) > 0:
                    to_binary_prefix = '('
                    to_binary_suffix = ').toString(2)'
                else:
                    to_binary_prefix = ''
                    to_binary_suffix = '.toString(2)'
            else:
                to_binary_prefix = ''
                to_binary_suffix = ''

            result = []

            for index in range(self.get_label_count()):
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              global_output_prefix=global_output_prefix,
                                              global_output_suffix=global_output_suffix,
                                              name=self.get_name().headless,
                                              label=self.get_label_name(index=index),
                                              index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                              divisor=divisor,
                                              unit=self.get_formatted_unit_name(" + ' {0}\xFE'"),
                                              to_binary_prefix=to_binary_prefix,
                                              to_binary_suffix=to_binary_suffix,
                                              comment=self.get_formatted_comment(' // {0}')).replace("\xFE' + '", '').replace("\xFE", ''))

        return result

class JavaScriptExampleGetterFunction(common.ExampleGetterFunction, JavaScriptExampleArgumentsMixin):
    def get_javascript_function(self):
        return None

    def get_javascript_source(self):
        template = r"""{global_line_prefix}        // Get current {function_name_comment}
{global_line_prefix}        {device_name}.{function_name_headless}({arguments}
{global_line_prefix}            function ({variables}) {{
{outputs}
{global_line_prefix}            }},
{global_line_prefix}            function (error) {{
{global_line_prefix}                {global_output_prefix}'Error: ' + error{global_output_suffix};
{global_line_prefix}            }}
{global_line_prefix}        );
"""
        variables = []
        outputs = []

        for result in self.get_results():
            variables.append(result.get_javascript_source())
            outputs += result.get_javascript_outputs()

        while None in outputs:
            outputs.remove(None)

        return template.format(global_line_prefix=global_line_prefix,
                               global_output_prefix=global_output_prefix,
                               global_output_suffix=global_output_suffix,
                               device_name=self.get_device().get_initial_name(),
                               function_name_headless=self.get_name().headless,
                               function_name_comment=self.get_comment_name(),
                               variables=', '.join(variables),
                               outputs='\n'.join(outputs).replace('\r\n\r', '\n\n').strip('\r').replace('\r', '\n'),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_javascript_arguments()), ','))

class JavaScriptExampleSetterFunction(common.ExampleSetterFunction, JavaScriptExampleArgumentsMixin):
    def get_javascript_function(self):
        return None

    def get_javascript_source(self):
        template = '{comment1}{global_line_prefix}        {device_name}.{function_name}({arguments});{comment2}\n'

        result = template.format(global_line_prefix=global_line_prefix,
                                 device_name=self.get_device().get_initial_name(),
                                 function_name=self.get_name().headless,
                                 arguments=',<BP>'.join(self.get_javascript_arguments()),
                                 comment1=self.get_formatted_comment1(global_line_prefix + '        // {0}\n', '\r', '\n' + global_line_prefix + '        // '),
                                 comment2=self.get_formatted_comment2(' // {0}', ''))

        return common.break_string(result, '.{}('.format(self.get_name().headless))

class JavaScriptExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_javascript_function(self):
        template1 = r"""// Register {function_name_comment} callback
{device_name_initial}.on(Tinkerforge.{device_category}{device_name_camel}.CALLBACK_{function_name_upper},
"""
        template2A = r"""    // Callback function for {function_name_comment} callback
"""
        template2B = r"""{override_comment}
"""
        template3 = r"""    function ({parameters}) {{
{outputs}{extra_message}{global_callback_output_suffix}
    }}
);
"""
        override_comment = self.get_formatted_override_comment('    // {0}', None, '\n    // ')

        if override_comment == None:
            template2 = template2A
        else:
            template2 = template2B

        parameters = []
        outputs = []

        for parameter in self.get_parameters():
            parameters.append(parameter.get_javascript_source())
            outputs += parameter.get_javascript_outputs()

        while None in outputs:
            outputs.remove(None)

        if len(outputs) > 1:
            outputs.append("        {global_output_prefix}'\xFE'{global_output_suffix};".format(global_output_prefix=global_output_prefix,
                                                                                                global_output_suffix=global_output_suffix))

        extra_message = self.get_formatted_extra_message("        {global_output_prefix}'{{0}}\xFE'{global_output_suffix};".format(global_output_prefix=global_output_prefix,
                                                                                                                                   global_output_suffix=global_output_suffix))

        if len(extra_message) > 0 and len(outputs) > 0:
            extra_message = '\n' + extra_message

        result = template1.format(device_category=self.get_device().get_category().camel,
                                  device_name_camel=self.get_device().get_name().camel,
                                  device_name_initial=self.get_device().get_initial_name(),
                                  function_name_upper=self.get_name().upper,
                                  function_name_comment=self.get_comment_name()) + \
                 template2.format(function_name_comment=self.get_comment_name(),
                                  override_comment=override_comment) + \
                 template3.format(global_callback_output_suffix=global_callback_output_suffix,
                                  parameters=',<BP>'.join(parameters),
                                  outputs='\n'.join(outputs).replace('\r\n\r', '\n\n').strip('\r').replace('\r', '\n'),
                                  extra_message=extra_message).replace("\xFE' + '", '').replace("\xFE", '')

        return common.break_string(result, 'function (')

    def get_javascript_source(self):
        return None

class JavaScriptExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction, JavaScriptExampleArgumentsMixin):
    def get_javascript_function(self):
        return None

    def get_javascript_source(self):
        templateA = r"""{global_line_prefix}        // Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
{global_line_prefix}        {device_name}.set{function_name_camel}Period({arguments}{period_msec});
"""
        templateB = r"""{global_line_prefix}        // Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
{global_line_prefix}        // Note: The {function_name_comment} callback is only called every {period_sec_long}
{global_line_prefix}        //       if the {function_name_comment} has changed since the last call!
{global_line_prefix}        {device_name}.set{function_name_camel}CallbackPeriod({arguments}{period_msec});
"""

        if self.get_device().get_name().space.startswith('IMU'):
            template = templateA # FIXME: special hack for IMU Brick (2.0) callback behavior and name mismatch
        else:
            template = templateB

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(global_line_prefix=global_line_prefix,
                               device_name=self.get_device().get_initial_name(),
                               function_name_camel=self.get_name().camel,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_javascript_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class JavaScriptExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_javascript_source(self):
        template = '{minimum}, {maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class JavaScriptExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction, JavaScriptExampleArgumentsMixin):
    def get_javascript_function(self):
        return None

    def get_javascript_source(self):
        template = r"""{global_line_prefix}        // Configure threshold for {function_name_comment} "{option_comment}"
{global_line_prefix}        {device_name}.set{function_name_camel}CallbackThreshold({arguments}'{option_char}', {minimum_maximums});
"""
        minimum_maximums = []

        for minimum_maximum in self.get_minimum_maximums():
            minimum_maximums.append(minimum_maximum.get_javascript_source())

        return template.format(global_line_prefix=global_line_prefix,
                               device_name=self.get_device().get_initial_name(),
                               function_name_camel=self.get_name().camel,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_javascript_arguments()), ', '),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               minimum_maximums=', '.join(minimum_maximums))

class JavaScriptExampleCallbackConfigurationFunction(common.ExampleCallbackConfigurationFunction, JavaScriptExampleArgumentsMixin):
    def get_javascript_function(self):
        return None

    def get_javascript_source(self):
        templateA = r"""{global_line_prefix}        // Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
{global_line_prefix}        {device_name}.set{function_name_camel}CallbackConfiguration({arguments}{period_msec}{value_has_to_change});
"""
        templateB = r"""{global_line_prefix}        // Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms) without a threshold
{global_line_prefix}        {device_name}.set{function_name_camel}CallbackConfiguration({arguments}{period_msec}{value_has_to_change}, '{option_char}', {minimum_maximums});
"""
        templateC = r"""{global_line_prefix}        // Configure threshold for {function_name_comment} "{option_comment}"
{global_line_prefix}        // with a debounce period of {period_sec_short} ({period_msec}ms)
{global_line_prefix}        {device_name}.set{function_name_camel}CallbackConfiguration({arguments}{period_msec}{value_has_to_change}, '{option_char}', {minimum_maximums});
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
            minimum_maximums.append(minimum_maximum.get_javascript_source())

        return template.format(global_line_prefix=global_line_prefix,
                               device_name=self.get_device().get_initial_name(),
                               function_name_camel=self.get_name().camel,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_javascript_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long,
                               value_has_to_change=common.wrap_non_empty(', ', self.get_value_has_to_change('true', 'false', ''), ''),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               minimum_maximums=', '.join(minimum_maximums))

class JavaScriptExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_javascript_function(self):
        return None

    def get_javascript_source(self):
        global global_line_prefix
        global global_last_sleep_function
        global global_inside_for_loop

        type_ = self.get_type()

        if type_ == 'empty':
            return ''
        elif type_ == 'debounce_period':
            template = r"""{global_line_prefix}        // Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms)
{global_line_prefix}        {device_name_initial}.setDebouncePeriod({period_msec});
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(global_line_prefix=global_line_prefix,
                                   device_name_initial=self.get_device().get_initial_name(),
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type_ == 'sleep':
            result = end_previous_sleep_function('')
            template = '{comment1}{global_line_prefix}        setTimeout(function () {{\n\xFF'
            result += template.format(global_line_prefix=global_line_prefix,
                                      duration=self.get_sleep_duration(),
                                      comment1=self.get_formatted_sleep_comment1(global_line_prefix + '        // {0}\n', '', '\n' + global_line_prefix + '        // '))
            global_line_prefix = ' '*(len(global_line_prefix) + 4)
            global_last_sleep_function = self

            return result
        elif type_ == 'wait':
            return None
        elif type_ == 'loop_header':
            template = '{comment}        for(var i = 0; i < {limit}; ++i) {{\n\xFF'
            global_line_prefix = '    '
            global_inside_for_loop = True

            return template.format(limit=self.get_loop_header_limit(),
                                   comment=self.get_formatted_loop_header_comment('        // {0}\n', '', '\n        // '))
        elif type_ == 'loop_footer':
            result = common.wrap_non_empty('', end_previous_sleep_function(''), '\n')
            global_line_prefix = ''
            global_inside_for_loop = False

            return result + '\r        }\n'

class JavaScriptExamplesGenerator(javascript_common.JavascriptGeneratorTrait, common.ExamplesGenerator):
    def get_bindings_name(self):
        return 'javascript'

    def get_constant_class(self):
        return JavaScriptConstant

    def get_example_class(self):
        return JavaScriptExample

    def get_example_argument_class(self):
        return JavaScriptExampleArgument

    def get_example_parameter_class(self):
        return JavaScriptExampleParameter

    def get_example_result_class(self):
        return JavaScriptExampleResult

    def get_example_getter_function_class(self):
        return JavaScriptExampleGetterFunction

    def get_example_setter_function_class(self):
        return JavaScriptExampleSetterFunction

    def get_example_callback_function_class(self):
        return JavaScriptExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return JavaScriptExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return JavaScriptExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return JavaScriptExampleCallbackThresholdFunction

    def get_example_callback_configuration_function_class(self):
        return JavaScriptExampleCallbackConfigurationFunction

    def get_example_special_function_class(self):
        return JavaScriptExampleSpecialFunction

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
            'lcd-20x4-bricklet/unicode'
        ]

        # nodejs
        for example in examples:
            filename = 'Example{0}.js'.format(example.get_name().camel)
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
                f.write(example.get_nodejs_source())

        # html
        for example in examples:
            filename = 'Example{0}.html'.format(example.get_name().camel)
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
                f.write(example.get_html_source())

def generate(root_dir):
    common.generate(root_dir, 'en', JavaScriptExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
