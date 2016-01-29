#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JavaScript Examples Generator
Copyright (C) 2015-2016 Matthias Bolte <matthias@tinkerforge.com>

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
import os

sys.path.append(os.path.split(os.getcwd())[0])
import common

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
        template = 'Tinkerforge.{device_camel_case_category}{device_camel_case_name}.{constant_group_upper_case_name}_{constant_upper_case_name}'

        return template.format(device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               constant_group_upper_case_name=self.get_constant_group().get_upper_case_name(),
                               constant_upper_case_name=self.get_upper_case_name())

class JavaScriptExample(common.Example):
    def get_nodejs_source(self):
        global global_output_prefix
        global global_output_suffix
        global global_callback_output_suffix
        global global_last_sleep_function
        global global_sleep_duration_offset
        global global_total_sleep_duration

        global_output_prefix = 'console.log('
        global_output_suffix = ')'
        global_callback_output_suffix = ''
        global_last_sleep_function = None
        global_sleep_duration_offset = 0
        global_total_sleep_duration = 0

        template = r"""var Tinkerforge = require('tinkerforge');{incomplete}

var HOST = 'localhost';
var PORT = 4223;
var UID = '{dummy_uid}'; // Change to your UID

var ipcon = new Tinkerforge.IPConnection(); // Create IP connection
var {device_initial_name} = new Tinkerforge.{device_camel_case_category}{device_camel_case_name}(UID, ipcon); // Create device object

ipcon.connect(HOST, PORT,
    function (error) {{
        console.log('Error: ' + error);
    }}
); // Connect to brickd
// Don't use device before ipcon is connected
{functions}
console.log('Press key to exit');
process.stdin.on('data',
    function (data) {{{cleanups}
        ipcon.disconnect();
        process.exit(0);
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
                               device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               device_initial_name=self.get_device().get_initial_name(),
                               dummy_uid=self.get_dummy_uid(),
                               functions=common.wrap_non_empty('\n', '\n'.join(functions), ''),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), '')).replace('<<<total_sleep_duration>>>', str(global_total_sleep_duration)).replace("console.log('');", "console.log();")

    def get_html_source(self):
        global global_output_prefix
        global global_output_suffix
        global global_callback_output_suffix
        global global_last_sleep_function
        global global_sleep_duration_offset
        global global_total_sleep_duration

        global_output_prefix = 'textArea.value += '
        global_output_suffix = " + '\\n'"
        global_callback_output_suffix = '\n        textArea.scrollTop = textArea.scrollHeight;'
        global_last_sleep_function = None
        global_sleep_duration_offset = 0
        global_total_sleep_duration = 0

        template = r"""<!DOCTYPE html>{incomplete}
<html>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <head>
        <title>Tinkerforge | JavaScript Example</title>
    </head>
    <body>
        <div style="text-align:center;">
            <h1>{device_long_display_name} {example_name} Example</h1>
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
        <div>
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
                var {device_initial_name} = new Tinkerforge.{device_camel_case_category}{device_camel_case_name}(UID, ipcon); // Create device object
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
                               example_name=self.get_name(),
                               device_long_display_name=self.get_device().get_long_display_name(),
                               device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               device_initial_name=self.get_device().get_initial_name(),
                               functions=common.wrap_non_empty('\n                ', '\n                '.join('\n'.join(functions).split('\n')), '').rstrip().replace('\n                \n', '\n\n'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), '')).replace('<<<total_sleep_duration>>>', str(global_total_sleep_duration)).replace("' + '\\n';", "\\n';")

class JavaScriptExampleArgument(common.ExampleArgument):
    def get_javascript_source(self):
        type = self.get_type()
        value = self.get_value()

        if type == 'bool':
            if value:
                return 'true'
            else:
                return 'false'
        elif type in ['char', 'string']:
            return "'{0}'".format(value)
        elif ':bitmask:' in type:
            return common.make_c_like_bitmask(value)
        elif type.endswith(':constant'):
            return self.get_value_constant().get_javascript_source()
        else:
            return str(value)

class JavaScriptExampleParameter(common.ExampleParameter):
    def get_javascript_source(self):
        return self.get_headless_camel_case_name()

    def get_javascript_output(self):
        template = "        {global_output_prefix}'{label_name}: ' + {to_binary_prefix}{headless_camel_case_name}{divisor}{to_binary_suffix}{unit_final_name}{global_output_suffix};"

        if self.get_label_name() == None:
            return None

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

        return template.format(global_output_prefix=global_output_prefix,
                               global_output_suffix=global_output_suffix,
                               headless_camel_case_name=self.get_headless_camel_case_name(),
                               label_name=self.get_label_name(),
                               divisor=divisor,
                               unit_final_name=self.get_unit_formatted_final_name(" + ' {0}'"),
                               to_binary_prefix=to_binary_prefix,
                               to_binary_suffix=to_binary_suffix)

class JavaScriptExampleResult(common.ExampleResult):
    def get_javascript_source(self):
        return self.get_headless_camel_case_name()

    def get_javascript_output(self):
        template = "{global_line_prefix}                {global_output_prefix}'{label_name}: ' + {to_binary_prefix}{headless_camel_case_name}{divisor}{to_binary_suffix}{unit_final_name}{global_output_suffix};"

        if self.get_label_name() == None:
            return None

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

        return template.format(global_line_prefix=global_line_prefix,
                               global_output_prefix=global_output_prefix,
                               global_output_suffix=global_output_suffix,
                               headless_camel_case_name=self.get_headless_camel_case_name(),
                               label_name=self.get_label_name(),
                               divisor=divisor,
                               unit_final_name=self.get_unit_formatted_final_name(" + ' {0}'"),
                               to_binary_prefix=to_binary_prefix,
                               to_binary_suffix=to_binary_suffix)

class JavaScriptExampleGetterFunction(common.ExampleGetterFunction):
    def get_javascript_function(self):
        return None

    def get_javascript_source(self):
        template = r"""{global_line_prefix}        // Get current {function_comment_name}{comments}
{global_line_prefix}        {device_initial_name}.{function_headless_camel_case_name}({arguments}
{global_line_prefix}            function ({variables}) {{
{outputs}
{global_line_prefix}            }},
{global_line_prefix}            function (error) {{
{global_line_prefix}                {global_output_prefix}'Error: ' + error{global_output_suffix};
{global_line_prefix}            }}
{global_line_prefix}        );
"""
        comments = []
        variables = []
        outputs = []

        for result in self.get_results():
            comments.append(result.get_formatted_comment())
            variables.append(result.get_javascript_source())
            outputs.append(result.get_javascript_output())

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = comments[:1]

        while None in outputs:
            outputs.remove(None)

        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_javascript_source())

        return template.format(global_line_prefix=global_line_prefix,
                               global_output_prefix=global_output_prefix,
                               global_output_suffix=global_output_suffix,
                               device_initial_name=self.get_device().get_initial_name(),
                               function_headless_camel_case_name=self.get_headless_camel_case_name(),
                               function_comment_name=self.get_comment_name(),
                               comments=''.join(comments),
                               variables=', '.join(variables),
                               outputs='\n'.join(outputs),
                               arguments=common.wrap_non_empty('', ', '.join(arguments), ','))

class JavaScriptExampleSetterFunction(common.ExampleSetterFunction):
    def get_javascript_function(self):
        return None

    def get_javascript_source(self):
        template = '{comment1}{global_line_prefix}        {device_initial_name}.{function_headless_camel_case_name}({arguments});{comment2}\n'
        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_javascript_source())

        return template.format(global_line_prefix=global_line_prefix,
                               device_initial_name=self.get_device().get_initial_name(),
                               function_headless_camel_case_name=self.get_headless_camel_case_name(),
                               arguments=', '.join(arguments),
                               comment1=self.get_formatted_comment1(global_line_prefix + '        // {0}\n', '\r', '\n' + global_line_prefix + '        // '),
                               comment2=self.get_formatted_comment2(' // {0}', ''))

class JavaScriptExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_javascript_function(self):
        template1 = r"""// Register {function_comment_name} callback
{device_initial_name}.on(Tinkerforge.{device_camel_case_category}{device_camel_case_name}.CALLBACK_{function_upper_case_name},
"""
        template2A = r"""    // Callback function for {function_comment_name} callback{comments}
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

        comments = []
        parameters = []
        outputs = []

        for parameter in self.get_parameters():
            comments.append(parameter.get_formatted_comment())
            parameters.append(parameter.get_javascript_source())
            outputs.append(parameter.get_javascript_output())

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = [comments[0].replace('parameter has', 'parameters have')]

        while None in outputs:
            outputs.remove(None)

        if len(outputs) > 1:
            outputs.append("        {global_output_prefix}''{global_output_suffix};".format(global_output_prefix=global_output_prefix,
                                                                                            global_output_suffix=global_output_suffix))

        extra_message = self.get_formatted_extra_message("        {global_output_prefix}'{{0}}'{global_output_suffix};".format(global_output_prefix=global_output_prefix,
                                                                                                                               global_output_suffix=global_output_suffix))

        if len(extra_message) > 0 and len(outputs) > 0:
            extra_message = '\n' + extra_message

        return template1.format(device_camel_case_category=self.get_device().get_camel_case_category(),
                                device_camel_case_name=self.get_device().get_camel_case_name(),
                                device_initial_name=self.get_device().get_initial_name(),
                                function_upper_case_name=self.get_upper_case_name(),
                                function_comment_name=self.get_comment_name()) + \
               template2.format(function_comment_name=self.get_comment_name(),
                                comments=''.join(comments),
                                override_comment=override_comment) + \
               template3.format(global_callback_output_suffix=global_callback_output_suffix,
                                parameters=', '.join(parameters),
                                outputs='\n'.join(outputs),
                                extra_message=extra_message)

    def get_javascript_source(self):
        return None

class JavaScriptExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction):
    def get_javascript_function(self):
        return None

    def get_javascript_source(self):
        template = r"""{global_line_prefix}        // Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
{global_line_prefix}        // Note: The {function_comment_name} callback is only called every {period_sec_long}
{global_line_prefix}        //       if the {function_comment_name} has changed since the last call!
{global_line_prefix}        {device_initial_name}.set{function_camel_case_name}{suffix}Period({arguments}{period_msec});
"""

        if self.get_device().get_underscore_name().startswith('imu'):
            suffix = '' # FIXME: special hack for IMU Brick name mismatch
        else:
            suffix = 'Callback'

        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_javascript_source())

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(global_line_prefix=global_line_prefix,
                               device_initial_name=self.get_device().get_initial_name(),
                               function_camel_case_name=self.get_camel_case_name(),
                               function_comment_name=self.get_comment_name(),
                               suffix=suffix,
                               arguments=common.wrap_non_empty('', ', '.join(arguments), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class JavaScriptExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_javascript_source(self):
        template = '{minimum}, {maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class JavaScriptExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction):
    def get_javascript_function(self):
        return None

    def get_javascript_source(self):
        template = r"""{global_line_prefix}        // Configure threshold for {function_comment_name} "{option_comment}"{mininum_maximum_unit_comments}
{global_line_prefix}        {device_initial_name}.set{function_camel_case_name}CallbackThreshold({arguments}'{option_char}', {mininum_maximums});
"""
        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_javascript_source())

        mininum_maximums = []
        mininum_maximum_unit_comments = []

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_javascript_source())
            mininum_maximum_unit_comments.append(mininum_maximum.get_unit_comment())

        if len(mininum_maximum_unit_comments) > 1 and len(set(mininum_maximum_unit_comments)) == 1:
            mininum_maximum_unit_comments = mininum_maximum_unit_comments[:1]

        return template.format(global_line_prefix=global_line_prefix,
                               device_initial_name=self.get_device().get_initial_name(),
                               function_camel_case_name=self.get_camel_case_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(arguments), ', '),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               mininum_maximums=', '.join(mininum_maximums),
                               mininum_maximum_unit_comments=''.join(mininum_maximum_unit_comments))

class JavaScriptExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_javascript_function(self):
        return None

    def get_javascript_source(self):
        global global_line_prefix
        global global_last_sleep_function
        global global_inside_for_loop

        type = self.get_type()

        if type == 'empty':
            return ''
        elif type == 'debounce_period':
            template = r"""{global_line_prefix}        // Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms)
{global_line_prefix}        {device_initial_name}.setDebouncePeriod({period_msec});
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(global_line_prefix=global_line_prefix,
                                   device_initial_name=self.get_device().get_initial_name(),
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type == 'sleep':
            result = end_previous_sleep_function('')
            template = '{comment1}{global_line_prefix}        setTimeout(function () {{\n\xFF'
            result += template.format(global_line_prefix=global_line_prefix,
                                      duration=self.get_sleep_duration(),
                                      comment1=self.get_formatted_sleep_comment1(global_line_prefix + '        // {0}\n', '', '\n' + global_line_prefix + '        // '))
            global_line_prefix = ' '*(len(global_line_prefix) + 4)
            global_last_sleep_function = self

            return result
        elif type == 'wait':
            return None
        elif type == 'loop_header':
            template = '{comment}        for(var i = 0; i < {limit}; ++i) {{\n\xFF'
            global_line_prefix = '    '
            global_inside_for_loop = True

            return template.format(limit=self.get_loop_header_limit(),
                                   comment=self.get_formatted_loop_header_comment('        // {0}\n', '', '\n        // '))
        elif type == 'loop_footer':
            result = common.wrap_non_empty('', end_previous_sleep_function(''), '\n')
            global_line_prefix = ''
            global_inside_for_loop = False

            return result + '\r        }\n'

class JavaScriptExamplesGenerator(common.ExamplesGenerator):
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

    def get_example_special_function_class(self):
        return JavaScriptExampleSpecialFunction

    def generate(self, device):
        if os.getenv('TINKERFORGE_GENERATE_EXAMPLES_FOR_DEVICE', device.get_camel_case_name()) != device.get_camel_case_name():
            return

        examples_directory = self.get_examples_directory(device)
        examples = device.get_examples()

        if len(examples) == 0:
            print('  \033[01;31m- no examples\033[0m')
            return

        if not os.path.exists(examples_directory):
            os.makedirs(examples_directory)

        # nodejs
        for example in examples:
            filename = 'Example{0}.js'.format(example.get_camel_case_name())
            filepath = os.path.join(examples_directory, filename)

            if example.is_incomplete():
                if os.path.exists(filepath) and self.skip_existing_incomplete_example:
                    print('  - ' + filename + ' \033[01;35m(incomplete, skipped)\033[0m')
                    continue
                else:
                    print('  - ' + filename + ' \033[01;31m(incomplete)\033[0m')
            else:
                print('  - ' + filename)

            js = open(filepath, 'wb')
            js.write(example.get_nodejs_source())
            js.close()

        # html
        for example in examples:
            filename = 'Example{0}.html'.format(example.get_camel_case_name())
            filepath = os.path.join(examples_directory, filename)

            if example.is_incomplete():
                if os.path.exists(filepath) and self.skip_existing_incomplete_example:
                    print('  - ' + filename + ' \033[01;35m(incomplete, skipped)\033[0m')
                    continue
                else:
                    print('  - ' + filename + ' \033[01;31m(incomplete)\033[0m')
            else:
                print('  - ' + filename)

            html = open(filepath, 'wb')
            html.write(example.get_html_source())
            html.close()

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', JavaScriptExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
