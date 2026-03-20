#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MicroPython Examples Generator
Created by René Rohner
Copyright (C) 2026 Tinkerforge GmbH

generate_micropython_examples.py: Generator for MicroPython examples

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
from generators.micropython import micropython_common

global_line_prefix = ''

class MicroPythonConstant(common.Constant):
    def get_micropython_source(self, callback=False):
        templateA = '{device_class}.{constant_group_name}_{constant_name}'
        templateB = '{device_name}.{constant_group_name}_{constant_name}'

        if callback:
            template = templateA
        else:
            template = templateB

        return template.format(device_class=self.get_device().get_micropython_class_name(),
                               device_name=self.get_device().get_initial_name(),
                               constant_group_name=self.get_constant_group().get_name().upper,
                               constant_name=self.get_name().upper)

class MicroPythonExample(common.Example):
    def get_micropython_source(self):
        template = r"""#!/usr/bin/env micropython
# -*- coding: utf-8 -*-{incomplete}{description}

HOST = "localhost"
PORT = 4223
UID = "{dummy_uid}" # Change {dummy_uid} to the UID of your {device_name_long_display}
{imports}
from ip_connection import IPConnection
from {device_category_under}_{device_name_under} import {device_category_camel}{device_name_camel}
{functions}
if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    {device_name_initial} = {device_category_camel}{device_name_camel}(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected
{sources}
    {wait_or_sleep}{cleanups}
    ipcon.disconnect()
"""

        if self.is_incomplete():
            incomplete = '\n\n# FIXME: This example is incomplete'
        else:
            incomplete = ''

        if self.get_description() != None:
            description = '\n\n# {0}'.format(self.get_description().replace('\n', '\n# '))
        else:
            description = ''

        imports = []
        functions = []
        sources = []
        cleanups = []

        for function in self.get_functions():
            imports += function.get_micropython_imports()
            functions.append(function.get_micropython_function())
            sources.append(function.get_micropython_source())

        for cleanup in self.get_cleanups():
            imports += cleanup.get_micropython_imports()
            functions.append(cleanup.get_micropython_function())
            cleanups.append(cleanup.get_micropython_source())

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

        # Use dispatch_callbacks for callback examples, sleep for others
        has_callbacks = any(isinstance(f, MicroPythonExampleCallbackFunction) for f in self.get_functions())

        if has_callbacks:
            wait_or_sleep = 'ipcon.dispatch_callbacks(-1) # Dispatch callbacks forever'
        else:
            wait_or_sleep = 'time.sleep(1)'

            if 'import time\n' not in unique_imports:
                unique_imports.append('import time\n')

        return template.format(incomplete=incomplete,
                               description=description,
                               device_category_camel=self.get_device().get_category().camel,
                               device_category_under=self.get_device().get_category().under,
                               device_name_camel=self.get_device().get_name().camel,
                               device_name_under=self.get_device().get_name().under,
                               device_name_initial=self.get_device().get_initial_name(),
                               device_name_long_display=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               imports=common.wrap_non_empty('\n', ''.join(unique_imports), ''),
                               functions=common.wrap_non_empty('\n', '\n'.join(functions), ''),
                               sources='\n' + '\n'.join(sources).replace('\n\r', '').lstrip('\r'),
                               wait_or_sleep=wait_or_sleep,
                               cleanups=common.wrap_non_empty('\n\n', '\n'.join(cleanups).replace('\n\r', '').lstrip('\r').rstrip('\n'), '\n'))

class MicroPythonExampleArgument(common.ExampleArgument):
    def get_micropython_source(self):
        type_ = self.get_type()

        def helper(value):
            if type_ == 'float':
                return common.format_float(value)
            elif type_ == 'bool':
                return str(bool(value))
            elif type_ in  ['char', 'string']:
                return '"{0}"'.format(value.replace('"', '\\"'))
            elif ':bitmask:' in type_:
                return common.make_c_like_bitmask(value)
            elif type_.endswith(':constant'):
                return self.get_value_constant(value).get_micropython_source()
            else:
                return str(value)

        value = self.get_value()

        if isinstance(value, list):
            return '[{0}]'.format(', '.join([helper(item) for item in value]))

        return helper(value)

class MicroPythonExampleArgumentsMixin(object):
    def get_micropython_arguments(self):
        return [argument.get_micropython_source() for argument in self.get_arguments()]

class MicroPythonExampleParameter(common.ExampleParameter):
    def get_micropython_source(self):
        return self.get_name().under

    def get_micropython_prints(self):
        if self.get_type().split(':')[-1] == 'constant':
            if self.get_label_name() == None:
                return []

            # FIXME: need to handle multiple labels
            assert self.get_label_count() == 1

            template = '{global_line_prefix}    {else_}if {name} == {constant_name}:\n{global_line_prefix}        print("{label}: {constant_title}"){comment}'
            constant_group = self.get_constant_group()
            result = []

            for constant in constant_group.get_constants():
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              else_='el' if len(result) > 0 else '',
                                              name=self.get_name().under,
                                              label=self.get_label_name(),
                                              constant_name=constant.get_micropython_source(callback=True),
                                              constant_title=constant.get_name().space,
                                              comment=self.get_formatted_comment(' # {0}')))

            result = ['\r' + '\n'.join(result) + '\r']
        else:
            template = '{global_line_prefix}    print("{label}: " + {format_prefix}{name}{index}{divisor}{format_suffix}{unit}){comment}'

            if self.get_label_name() == None:
                return []

            if self.get_cardinality() < 0:
                return [] # FIXME: streaming

            type_ = self.get_type()

            if ':bitmask:' in type_:
                format_prefix = 'format('
                format_suffix = ', "0{0}b")'.format(int(type_.split(':')[2]))
            elif type_ in ['char', 'string']:
                format_prefix = ''
                format_suffix = ''
            else:
                format_prefix = 'str('
                format_suffix = ')'

            result = []

            for index in range(self.get_label_count()):
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              name=self.get_name().under,
                                              label=self.get_label_name(index=index),
                                              index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                              divisor=self.get_formatted_divisor('/{0}'),
                                              unit=self.get_formatted_unit_name(' + " {0}"'),
                                              format_prefix=format_prefix,
                                              format_suffix=format_suffix,
                                              comment=self.get_formatted_comment(' # {0}')))

        return result

class MicroPythonExampleResult(common.ExampleResult):
    def get_micropython_variable(self):
        name = self.get_name().under

        if name == self.get_device().get_initial_name():
            name += '_'

        return name

    def get_micropython_prints(self):
        if self.get_type().split(':')[-1] == 'constant':
            # FIXME: need to handle multiple labels
            assert self.get_label_count() == 1

            template = '{global_line_prefix}    {else_}if {name} == {constant_name}:\n{global_line_prefix}        print("{label}: {constant_title}"){comment}'
            constant_group = self.get_constant_group()
            result = []

            for constant in constant_group.get_constants():
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              else_='el' if len(result) > 0 else '',
                                              name=self.get_name().under,
                                              label=self.get_label_name(),
                                              constant_name=constant.get_micropython_source(),
                                              constant_title=constant.get_name().space,
                                              comment=self.get_formatted_comment(' # {0}')))

            result = ['\r' + '\n'.join(result) + '\r']
        else:
            template = '{global_line_prefix}    print("{label}: " + {format_prefix}{name}{index}{divisor}{format_suffix}{unit}){comment}'

            if self.get_label_name() == None:
                return []

            if self.get_cardinality() < 0:
                return [] # FIXME: streaming

            name = self.get_name().under

            if name == self.get_device().get_initial_name():
                name += '_'

            type_ = self.get_type()

            if ':bitmask:' in type_:
                format_prefix = 'format('
                format_suffix = ', "0{0}b")'.format(int(type_.split(':')[2]))
            elif type_ in ['char', 'string']:
                format_prefix = ''
                format_suffix = ''
            else:
                format_prefix = 'str('
                format_suffix = ')'

            result = []

            for index in range(self.get_label_count()):
                result.append(template.format(global_line_prefix=global_line_prefix,
                                              name=name,
                                              label=self.get_label_name(index=index),
                                              index='[{0}]'.format(index) if self.get_label_count() > 1 else '',
                                              divisor=self.get_formatted_divisor('/{0}'),
                                              unit=self.get_formatted_unit_name(' + " {0}"'),
                                              format_prefix=format_prefix,
                                              format_suffix=format_suffix,
                                              comment=self.get_formatted_comment(' # {0}')))

        return result

class MicroPythonExampleGetterFunction(common.ExampleGetterFunction, MicroPythonExampleArgumentsMixin):
    def get_micropython_imports(self):
        return []

    def get_micropython_function(self):
        return None

    def get_micropython_source(self):
        template = r"""{global_line_prefix}    # Get current {function_name_comment}
{global_line_prefix}    {variables} = {device_name}.{function_name_under}({arguments})
{prints}
"""
        variables = []
        prints = []

        for result in self.get_results():
            variables.append(result.get_micropython_variable())
            prints += result.get_micropython_prints()

        while None in prints:
            prints.remove(None)

        if len(prints) > 1:
            prints.insert(0, '\b')

        result = template.format(global_line_prefix=global_line_prefix,
                                 device_name=self.get_device().get_initial_name(),
                                 function_name_under=self.get_name().under,
                                 function_name_comment=self.get_comment_name(),
                                 variables=',<BP>'.join(variables),
                                 prints='\n'.join(prints).replace('\b\n\r', '\n').replace('\b', '').replace('\r\n\r', '\n\n').rstrip('\r').replace('\r', '\n'),
                                 arguments=', '.join(self.get_micropython_arguments()))

        return common.break_string(result, '    ', continuation=' \\', indent_suffix='  ')

class MicroPythonExampleSetterFunction(common.ExampleSetterFunction, MicroPythonExampleArgumentsMixin):
    def get_micropython_imports(self):
        return []

    def get_micropython_function(self):
        return None

    def get_micropython_source(self):
        template = '{comment1}{global_line_prefix}    {device_name}.{function_name}({arguments}){comment2}\n'

        result = template.format(global_line_prefix=global_line_prefix,
                                 device_name=self.get_device().get_initial_name(),
                                 function_name=self.get_name().under,
                                 arguments=',<BP>'.join(self.get_micropython_arguments()),
                                 comment1=self.get_formatted_comment1(global_line_prefix + '    # {0}\n', '\r', '\n' + global_line_prefix + '    # '),
                                 comment2=self.get_formatted_comment2(' # {0}', ''))

        return common.break_string(result, '.{0}('.format(self.get_name().under))

class MicroPythonExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_micropython_imports(self):
        return []

    def get_micropython_function(self):
        template1A = r"""# Callback function for {function_name_comment} callback
"""
        template1B = r"""{override_comment}
"""
        template2 = r"""def cb_{function_name_under}({parameters}):
{prints}{extra_message}
"""
        override_comment = self.get_formatted_override_comment('# {0}', None, '\n# ')

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B

        parameters = []
        prints = []

        for parameter in self.get_parameters():
            parameters.append(parameter.get_micropython_source())
            prints += parameter.get_micropython_prints()

        while None in prints:
            prints.remove(None)

        if len(prints) > 1:
            prints.append('    print("")')

        extra_message = self.get_formatted_extra_message('    print("{0}")')

        if len(extra_message) > 0 and len(prints) > 0:
            extra_message = '\n' + extra_message

        if len(prints) == 0 and len(extra_message) == 0:
            prints_str = '    pass'
        else:
            prints_str = '\n'.join(prints).replace('\r\n\r', '\n\n').strip('\r').replace('\r', '\n')

        result = template1.format(function_name_comment=self.get_comment_name(),
                                  override_comment=override_comment) + \
                 template2.format(function_name_under=self.get_name().under,
                                  parameters=',<BP>'.join(parameters),
                                  prints=prints_str,
                                  extra_message=extra_message)

        return common.break_string(result, 'cb_{}('.format(self.get_name().under))

    def get_micropython_source(self):
        template1 = r"""    # Register {function_name_comment}<BP>callback<BP>to<BP>function<BP>cb_{function_name_under}
"""
        template2 = r"""    {device_name}.register_callback({device_name}.CALLBACK_{function_name_upper},<BP>cb_{function_name_under})
"""

        result1 = template1.format(function_name_under=self.get_name().under,
                                   function_name_comment=self.get_comment_name())
        result2 = template2.format(device_name=self.get_device().get_initial_name(),
                                   function_name_under=self.get_name().under,
                                   function_name_upper=self.get_name().upper)

        return common.break_string(result1, '# ', indent_tail='# ') + \
               common.break_string(result2, 'register_callback(')

class MicroPythonExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction, MicroPythonExampleArgumentsMixin):
    def get_micropython_imports(self):
        return []

    def get_micropython_function(self):
        return None

    def get_micropython_source(self):
        templateA = r"""    # Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
    {device_name}.set_{function_name_under}_period({arguments}{period_msec})
"""
        templateB = r"""    # Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
    # Note: The {function_name_comment} callback is only called every {period_sec_long}
    #       if the {function_name_comment} has changed since the last call!
    {device_name}.set_{function_name_under}_callback_period({arguments}{period_msec})
"""

        if self.get_device().get_name().space.startswith('IMU'):
            template = templateA # FIXME: special hack for IMU Brick (2.0) callback behavior and name mismatch
        else:
            template = templateB

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        return template.format(device_name=self.get_device().get_initial_name(),
                               function_name_under=self.get_name().under,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_micropython_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class MicroPythonExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_micropython_source(self):
        template = '{minimum}, {maximum}'

        return template.format(minimum=self.get_formatted_minimum(),
                               maximum=self.get_formatted_maximum())

class MicroPythonExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction, MicroPythonExampleArgumentsMixin):
    def get_micropython_imports(self):
        return []

    def get_micropython_function(self):
        return None

    def get_micropython_source(self):
        template = r"""    # Configure threshold for {function_name_comment} "{option_comment}"
    {device_name}.set_{function_name_under}_callback_threshold({arguments}"{option_char}", {minimum_maximums})
"""
        minimum_maximums = []

        for minimum_maximum in self.get_minimum_maximums():
            minimum_maximums.append(minimum_maximum.get_micropython_source())

        return template.format(device_name=self.get_device().get_initial_name(),
                               function_name_under=self.get_name().under,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_micropython_arguments()), ', '),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               minimum_maximums=', '.join(minimum_maximums))

class MicroPythonExampleCallbackConfigurationFunction(common.ExampleCallbackConfigurationFunction, MicroPythonExampleArgumentsMixin):
    def get_micropython_imports(self):
        return []

    def get_micropython_function(self):
        return None

    def get_micropython_source(self):
        templateA = r"""    # Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
    {device_name}.set_{function_name_under}_callback_configuration({arguments}{period_msec}{value_has_to_change})
"""
        templateB = r"""    # Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms) without a threshold
    {device_name}.set_{function_name_under}_callback_configuration({arguments}{period_msec}{value_has_to_change}, "{option_char}", {minimum_maximums})
"""
        templateC = r"""    # Configure threshold for {function_name_comment} "{option_comment}"
    # with a debounce period of {period_sec_short} ({period_msec}ms)
    {device_name}.set_{function_name_under}_callback_configuration({arguments}{period_msec}{value_has_to_change}, "{option_char}", {minimum_maximums})
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
            minimum_maximums.append(minimum_maximum.get_micropython_source())

        return template.format(device_name=self.get_device().get_initial_name(),
                               function_name_under=self.get_name().under,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('', ', '.join(self.get_micropython_arguments()), ', '),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long,
                               value_has_to_change=common.wrap_non_empty(', ', self.get_value_has_to_change('True', 'False', ''), ''),
                               option_char=self.get_option_char(),
                               option_comment=self.get_option_comment(),
                               minimum_maximums=', '.join(minimum_maximums))

class MicroPythonExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_micropython_imports(self):
        if self.get_type() == 'sleep':
            return ['import time\n']
        else:
            return []

    def get_micropython_function(self):
        return None

    def get_micropython_source(self):
        global global_line_prefix

        type_ = self.get_type()

        if type_ == 'empty':
            return ''
        elif type_ == 'debounce_period':
            template = r"""    # Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms)
    {device_name_initial}.set_debounce_period({period_msec})
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_name_initial=self.get_device().get_initial_name(),
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type_ == 'sleep':
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
        elif type_ == 'wait':
            return None
        elif type_ == 'loop_header':
            template = '{comment}    for i in range({limit}):\n'
            global_line_prefix = '    '

            return template.format(limit=self.get_loop_header_limit(),
                                   comment=self.get_formatted_loop_header_comment('    # {0}\n', '', '\n    # '))
        elif type_ == 'loop_footer':
            global_line_prefix = ''

            return '\r'

class MicroPythonExamplesGenerator(micropython_common.MicroPythonGeneratorTrait, common.ExamplesGenerator):
    def get_constant_class(self):
        return MicroPythonConstant

    def get_device_class(self):
        return micropython_common.MicroPythonDevice

    def get_example_class(self):
        return MicroPythonExample

    def get_example_argument_class(self):
        return MicroPythonExampleArgument

    def get_example_parameter_class(self):
        return MicroPythonExampleParameter

    def get_example_result_class(self):
        return MicroPythonExampleResult

    def get_example_getter_function_class(self):
        return MicroPythonExampleGetterFunction

    def get_example_setter_function_class(self):
        return MicroPythonExampleSetterFunction

    def get_example_callback_function_class(self):
        return MicroPythonExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return MicroPythonExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return MicroPythonExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return MicroPythonExampleCallbackThresholdFunction

    def get_example_callback_configuration_function_class(self):
        return MicroPythonExampleCallbackConfigurationFunction

    def get_example_special_function_class(self):
        return MicroPythonExampleSpecialFunction

    def generate(self, device):
        if os.getenv('TINKERFORGE_GENERATE_EXAMPLES_FOR_DEVICE', device.get_name().camel) != device.get_name().camel:
            common.print_verbose('    \033[01;31m- skipped\033[0m')
            return

        examples_dir = self.get_examples_dir(device)
        examples = device.get_examples()

        if len(examples) == 0:
            common.print_verbose('    \033[01;31m- no examples\033[0m')
            return

        if not os.path.exists(examples_dir):
            os.makedirs(examples_dir)

        for example in examples:
            filename = 'example_{0}.py'.format(example.get_name().under)
            filepath = os.path.join(examples_dir, filename)

            if example.is_incomplete():
                if os.path.exists(filepath) and self.skip_existing_incomplete_example:
                    common.print_verbose('    - ' + filename + ' \033[01;35m(incomplete, skipped)\033[0m')
                    continue
                else:
                    common.print_verbose('    - ' + filename + ' \033[01;31m(incomplete)\033[0m')
            else:
                common.print_verbose('    - ' + filename)

            with open(filepath, 'w') as f:
                f.write(example.get_micropython_source())

def generate(root_dir, language, internal):
    common.generate(root_dir, language, internal, MicroPythonExamplesGenerator)

if __name__ == '__main__':
    args = common.dockerize('micropython', __file__, add_internal_argument=True)

    generate(os.getcwd(), 'en', args.internal)
