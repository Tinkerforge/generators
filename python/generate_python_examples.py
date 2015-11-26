#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Examples Generator
Copyright (C) 2015 Matthias Bolte <matthias@tinkerforge.com>

generate_python_examples.py: Generator for Python examples

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

class PythonConstant(common.Constant):
    def get_python_source(self):
        template = '{device_initial_name}.{constant_group_upper_case_name}_{constant_upper_case_name}'

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               constant_group_upper_case_name=self.get_constant_group().get_upper_case_name(),
                               constant_upper_case_name=self.get_upper_case_name())

class PythonExample(common.Example):
    def get_python_source(self):
        template = r"""#!/usr/bin/env python
# -*- coding: utf-8 -*-{incomplete}

HOST = "localhost"
PORT = 4223
UID = "{dummy_uid}" # Change to your UID
{imports}
from tinkerforge.ip_connection import IPConnection
from tinkerforge.{device_underscore_category}_{device_underscore_name} import {device_camel_case_category}{device_camel_case_name}
{functions}
if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    {device_initial_name} = {device_camel_case_category}{device_camel_case_name}(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected
{sources}
    raw_input("Press key to exit\n") # Use input() in Python 3{cleanups}
    ipcon.disconnect()
"""

        if self.is_incomplete():
            incomplete = '\n\n# FIXME: This example is incomplete'
        else:
            incomplete = ''

        imports = []
        functions = []
        sources = []
        cleanups = []

        for function in self.get_functions():
            imports += function.get_python_imports()
            functions.append(function.get_python_function())
            sources.append(function.get_python_source())

        for cleanup in self.get_cleanups():
            imports += cleanup.get_python_imports()
            functions.append(cleanup.get_python_function())
            cleanups.append(cleanup.get_python_source())

        unique_imports = []

        for import_ in imports:
            if import_ not in unique_imports:
                unique_imports.append(import_)

        while None in functions:
            functions.remove(None)

        while None in sources:
            sources.remove(None)

        if len(sources) == 0:
            sources = ['    # TODO: Add example code here\n']

        while None in cleanups:
            cleanups.remove(None)

        return template.format(incomplete=incomplete,
                               device_camel_case_category=self.get_device().get_camel_case_category(),
                               device_underscore_category=self.get_device().get_underscore_category(),
                               device_camel_case_name=self.get_device().get_camel_case_name(),
                               device_underscore_name=self.get_device().get_underscore_name(),
                               device_initial_name=self.get_device().get_initial_name(),
                               dummy_uid=self.get_dummy_uid(),
                               imports=common.wrap_non_empty('\n', ''.join(unique_imports), ''),
                               functions=common.wrap_non_empty('\n', '\n'.join(functions), ''),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), ''))

class PythonExampleArgument(common.ExampleArgument):
    def get_python_source(self):
        type = self.get_type()
        value = self.get_value()

        if type == 'bool':
            if value:
                return 'True'
            else:
                return 'False'
        elif type in  ['char', 'string']:
            return '"{0}"'.format(value)
        elif ':bitmask:' in type:
            return common.make_c_like_bitmask(value)
        elif type.endswith(':constant'):
            return self.get_value_constant().get_python_source()
        else:
            return str(value)

class PythonExampleParameter(common.ExampleParameter):
    def get_python_source(self):
        return self.get_underscore_name()

    def get_python_print(self):
        template = '    print("{label_name}: " + {format_prefix}{underscore_name}{divisor}{format_suffix}{unit_final_name})'

        if self.get_label_name() == None:
            return None

        type = self.get_type()

        if ':bitmask:' in type:
            format_prefix = 'format('
            format_suffix = ', "0{0}b")'.format(int(type.split(':')[2]))
        elif type in ['char', 'string']:
            format_prefix = ''
            format_suffix = ''
        else:
            format_prefix = 'str('
            format_suffix = ')'

        return template.format(underscore_name=self.get_underscore_name(),
                               label_name=self.get_label_name(),
                               divisor=self.get_formatted_divisor('/{0}'),
                               unit_final_name=self.get_unit_formatted_final_name(' + " {0}"'),
                               format_prefix=format_prefix,
                               format_suffix=format_suffix)

class PythonExampleResult(common.ExampleResult):
    def get_python_variable(self):
        underscore_name = self.get_underscore_name()

        if underscore_name == self.get_device().get_initial_name():
            underscore_name += '_'

        return underscore_name

    def get_python_print(self):
        template = '    print("{label_name}: " + {format_prefix}{underscore_name}{divisor}{format_suffix}{unit_final_name})'

        if self.get_label_name() == None:
            return None

        underscore_name = self.get_underscore_name()

        if underscore_name == self.get_device().get_initial_name():
            underscore_name += '_'

        type = self.get_type()

        if ':bitmask:' in type:
            format_prefix = 'format('
            format_suffix = ', "0{0}b")'.format(int(type.split(':')[2]))
        elif type in ['char', 'string']:
            format_prefix = ''
            format_suffix = ''
        else:
            format_prefix = 'str('
            format_suffix = ')'

        return template.format(underscore_name=underscore_name,
                               label_name=self.get_label_name(),
                               divisor=self.get_formatted_divisor('/{0}'),
                               unit_final_name=self.get_unit_formatted_final_name(' + " {0}"'),
                               format_prefix=format_prefix,
                               format_suffix=format_suffix)

class PythonExampleGetterFunction(common.ExampleGetterFunction):
    def get_python_imports(self):
        return []

    def get_python_function(self):
        return None

    def get_python_source(self):
        template = r"""    # Get current {function_comment_name}{comments}
    {variables} = {device_initial_name}.{function_underscore_name}({arguments})
{prints}
"""
        comments = []
        variables = []
        prints = []

        for result in self.get_results():
            comments.append(result.get_formatted_comment())
            variables.append(result.get_python_variable())
            prints.append(result.get_python_print())

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = comments[:1]

        while None in prints:
            prints.remove(None)

        if len(prints) > 1:
            prints.insert(0, '')

        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_python_source())

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               function_comment_name=self.get_comment_name(),
                               comments=''.join(comments),
                               variables=', '.join(variables),
                               prints='\n'.join(prints),
                               arguments=', '.join(arguments))

class PythonExampleSetterFunction(common.ExampleSetterFunction):
    def get_python_imports(self):
        return []

    def get_python_function(self):
        return None

    def get_python_source(self):
        template = '{comment1}{global_line_prefix}    {device_initial_name}.{function_underscore_name}({arguments}){comment2}\n'
        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_python_source())

        return template.format(global_line_prefix=global_line_prefix,
                               device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               arguments=', '.join(arguments),
                               comment1=self.get_formatted_comment1(global_line_prefix + '    # {0}\n', '\r', '\n' + global_line_prefix + '    # '),
                               comment2=self.get_formatted_comment2(' # {0}', ''))

class PythonExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_python_imports(self):
        return []

    def get_python_function(self):
        template1A = r"""# Callback function for {function_comment_name} callback{comments}
"""
        template1B = r"""{override_comment}
"""
        template2 = r"""def cb_{function_underscore_name}({parameters}):
{prints}{extra_message}
"""
        override_comment = self.get_formatted_override_comment('# {0}', None, '\n# ')

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B

        comments = []
        parameters = []
        prints = []

        for parameter in self.get_parameters():
            comments.append(parameter.get_formatted_comment())
            parameters.append(parameter.get_python_source())
            prints.append(parameter.get_python_print())

        if len(comments) > 1 and len(set(comments)) == 1:
            comments = [comments[0].replace('parameter has', 'parameters have')]

        while None in prints:
            prints.remove(None)

        if len(prints) > 1:
            prints.append('    print("")')

        extra_message = self.get_formatted_extra_message('    print("{0}")')

        if len(extra_message) > 0 and len(prints) > 0:
            extra_message = '\n' + extra_message

        return template1.format(function_comment_name=self.get_comment_name(),
                                comments=''.join(comments),
                                override_comment=override_comment) + \
               template2.format(function_underscore_name=self.get_underscore_name(),
                                parameters=', '.join(parameters),
                                prints='\n'.join(prints),
                                extra_message=extra_message)

    def get_python_source(self):
        template = r"""    # Register {function_comment_name} callback to function cb_{function_underscore_name}
    {device_initial_name}.register_callback({device_initial_name}.CALLBACK_{function_upper_case_name}, cb_{function_underscore_name})
"""

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               function_upper_case_name=self.get_upper_case_name(),
                               function_comment_name=self.get_comment_name())

class PythonExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction):
    def get_python_imports(self):
        return []

    def get_python_function(self):
        return None

    def get_python_source(self):
        template = r"""    # Set period for {function_comment_name} callback to {period_sec_short} ({period_msec}ms)
    # Note: The {function_comment_name} callback is only called every {period_sec_long}
    #       if the {function_comment_name} has changed since the last call!
    {device_initial_name}.set_{function_underscore_name}{suffix}_period({arguments}{period_msec})
"""

        if self.get_device().get_underscore_name().startswith('imu'):
            suffix = '' # FIXME: special hack for IMU Brick name mismatch
        else:
            suffix = '_callback'

        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_python_source())

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               function_comment_name=self.get_comment_name(),
                               suffix=suffix,
                               arguments=common.wrap_non_empty('', ', '.join(arguments), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class PythonExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_python_source(self):
        template = '{minimum}, {maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class PythonExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction):
    def get_python_imports(self):
        return []

    def get_python_function(self):
        return None

    def get_python_source(self):
        template = r"""    # Configure threshold for {function_comment_name} "{option_comment}"{mininum_maximum_unit_comments}
    {device_initial_name}.set_{function_underscore_name}_callback_threshold({arguments}"{option_char}", {mininum_maximums})
"""
        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_python_source())

        mininum_maximums = []
        mininum_maximum_unit_comments = []

        for mininum_maximum in self.get_minimum_maximums():
            mininum_maximums.append(mininum_maximum.get_python_source())
            mininum_maximum_unit_comments.append(mininum_maximum.get_unit_comment())

        if len(mininum_maximum_unit_comments) > 1 and len(set(mininum_maximum_unit_comments)) == 1:
            mininum_maximum_unit_comments = mininum_maximum_unit_comments[:1]

        return template.format(device_initial_name=self.get_device().get_initial_name(),
                               function_underscore_name=self.get_underscore_name(),
                               function_comment_name=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(arguments), ', '),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               mininum_maximums=', '.join(mininum_maximums),
                               mininum_maximum_unit_comments=''.join(mininum_maximum_unit_comments))

class PythonExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_python_imports(self):
        if self.get_type() == 'sleep':
            return ['import time\n']
        else:
            return []

    def get_python_function(self):
        return None

    def get_python_source(self):
        global global_line_prefix

        type = self.get_type()

        if type == 'empty':
            return ''
        elif type == 'debounce_period':
            template = r"""    # Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms)
    {device_initial_name}.set_debounce_period({period_msec})
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_initial_name=self.get_device().get_initial_name(),
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type == 'sleep':
            template = '{comment1}{global_line_prefix}    time.sleep({duration}){comment2}\n'
            duration = self.get_sleep_duration()

            if duration % 1000 == 0:
                duration //= 1000
            else:
                duration /= 1000.0

            return template.format(global_line_prefix=global_line_prefix,
                                   duration=duration,
                                   comment1=self.get_formatted_sleep_comment1(global_line_prefix + '    # {0}\n', '\r', '\n' + global_line_prefix + '    # '),
                                   comment2=self.get_formatted_sleep_comment2(' # {0}', ''))
        elif type == 'wait':
            return None
        elif type == 'loop_header':
            template = '{comment}    for i in range({limit}):\n'
            global_line_prefix = '    '

            return template.format(limit=self.get_loop_header_limit(),
                                   comment=self.get_formatted_loop_header_comment('    # {0}\n', '', '\n    # '))
        elif type == 'loop_footer':
            global_line_prefix = ''

            return '\r'

class PythonExamplesGenerator(common.ExamplesGenerator):
    def get_bindings_name(self):
        return 'python'

    def get_constant_class(self):
        return PythonConstant

    def get_example_class(self):
        return PythonExample

    def get_example_argument_class(self):
        return PythonExampleArgument

    def get_example_parameter_class(self):
        return PythonExampleParameter

    def get_example_result_class(self):
        return PythonExampleResult

    def get_example_getter_function_class(self):
        return PythonExampleGetterFunction

    def get_example_setter_function_class(self):
        return PythonExampleSetterFunction

    def get_example_callback_function_class(self):
        return PythonExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return PythonExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return PythonExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return PythonExampleCallbackThresholdFunction

    def get_example_special_function_class(self):
        return PythonExampleSpecialFunction

    def generate(self, device):
        examples_directory = self.get_examples_directory(device)
        examples = device.get_examples()

        if len(examples) == 0:
            print('  \033[01;31m- no examples\033[0m')
            return

        if not os.path.exists(examples_directory):
            os.makedirs(examples_directory)

        for example in examples:
            filename = 'example_{0}.py'.format(example.get_underscore_name())
            filepath = os.path.join(examples_directory, filename)

            if example.is_incomplete():
                if os.path.exists(filepath) and self.skip_existing_incomplete_example:
                    print('  - ' + filename + ' \033[01;35m(incomplete, skipped)\033[0m')
                    continue
                else:
                    print('  - ' + filename + ' \033[01;31m(incomplete)\033[0m')
            else:
                print('  - ' + filename)

            py = open(filepath, 'wb')
            py.write(example.get_python_source())
            py.close()

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', PythonExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
