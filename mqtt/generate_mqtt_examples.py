#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MQTT Examples Generator
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>

generate_mqtt_examples.py: Generator for MQTT examples

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

import functools

global_line_prefix = ''

class MQTTExample(common.Example):
    def get_mqtt_source(self):
        template = r"""{incomplete}{description}# Change {dummy_uid} to the UID of your {device_long_display_name}
{sources}{cleanups}"""

        if self.is_incomplete():
            incomplete = '# FIXME: This example is incomplete\n'
        else:
            incomplete = ''

        if self.get_description() != None:
            description = '# {0}\n'.format(self.get_description().replace('\n', '\n# '))
        else:
            description = ''

        sources = []
        
        for function in self.get_functions():            
            sources.append(function.get_mqtt_source())

        while None in sources:
            sources.remove(None)

        if len(sources) == 0:
            sources = ['# TODO: Add example code here\n']
        
        cleanups = []

        for cleanup in self.get_cleanups():
            cleanups.append(cleanup.get_mqtt_source())

        while None in cleanups:
            cleanups.remove(None)

        sources = [s.lstrip('\r').rstrip('\n').split('\n') for s in sources]
        sources = reduce(lambda l, r: l + [''] + r, sources[1:], sources[0]) # Insert empty list between source blocks later generate a newline between blocks (so before comments). This also flattens the sublists
        
        cleanups = [s.lstrip('\r').rstrip('\n').split('\n') for s in cleanups]
        if len(cleanups) > 1:
            cleanups = reduce(lambda l, r: l + [''] + r, cleanups[1:], cleanups[0]) # Insert empty list between source blocks later generate a newline between blocks (so before comments). This also flattens the sublists
        else:
            cleanups = sum(cleanups, []) # Only flatten the list
        
        return template.format(incomplete=incomplete,
                               description=description,
                               device_long_display_name=self.get_device().get_long_display_name(),
                               dummy_uid=self.get_dummy_uid(),
                               sources='\nsetup:\n\t' + '\n\t'.join(sources),#.replace('\n\r', '').lstrip('\r'),
                               cleanups=common.wrap_non_empty('\n\ncleanup:\n\t# If you are done, run this to clean up\n\t', '\n\t'.join(cleanups), '').rstrip('\n') + '\n')

class MQTTExampleArgument(common.ExampleArgument):
    def get_mqtt_bitmask_comment(self):
        if ':bitmask:' in self.get_type():
            value = self.get_value()
            return '{0} = {1}'.format(common.make_c_like_bitmask(value), value)
        else:
            return None

    def get_mqtt_element(self, callback_fn=""):
        if callback_fn == "":
            return self.get_element()

        for packet in self.get_device().get_packets('function'):
            if callback_fn in packet.get_name().under:
                return packet.get_elements(direction='in')[self.get_index()]

    def get_mqtt_source(self, callback_fn=""):
        type_ = self.get_type()

        def helper(value):
            constant = self.get_value_constant(value)

            if constant != None:
                return '"{0}"'.format(constant.get_name().under)

            if type_ == 'bool':
                if value:
                    return 'true'
                else:
                    return 'false'
            elif type_ == 'char':
                return '"{0}"'.format(value)
            elif type_ == 'string':
                return '"{0}"'.format(value)
            elif ':bitmask:' in type_:
                return str(value)
            else:
                return str(value)

        value = self.get_value()
        name = '"' + self.get_mqtt_element(callback_fn).get_name().under + '"'
        if isinstance(value, list):
            return name + ": [" +','.join([helper(item) for item in value])+']'

        return name + ": " + helper(value)

class MQTTExampleArgumentsMixin(object):
    def __init__(self):
        print self.__class__

    def get_mqtt_arguments(self, callback_fn=""):
        arguments = []

        for argument in self.get_arguments():
            arguments.append(argument.get_mqtt_source(callback_fn))

        return arguments

class MQTTExampleParameter(common.ExampleParameter):
    def get_mqtt_source(self):
        template = '{label}: {{{{{name}}}}}{divisor}{unit}'

        if self.get_label_name() == None:
            return None

        return template.format(name=self.get_name().under,
                               label=self.get_label_name(),
                               divisor=self.get_formatted_divisor('/{0}', cast=int),
                               unit=self.get_formatted_unit_name(' {0}'))

class MQTTExampleResult(common.ExampleResult):
    pass

class MQTTExampleGetterFunction(common.ExampleGetterFunction, MQTTExampleArgumentsMixin):
    def get_mqtt_source(self):
        template = r"""{global_line_prefix}# Get current {function_name_comment}
subscribe to tinkerforge/response/{device_name}_{device_category}/{uid}/{function_name_under}
publish '{arguments}' to tinkerforge/request/{device_name}_{device_category}/{uid}/{function_name_under} 
"""

        return template.format(global_line_prefix=global_line_prefix,
                               device_name=self.get_device().get_name().under,
                               device_category=self.get_device().get_category().under,
                               uid=self.get_example().get_dummy_uid(), 
                               function_name_comment=self.get_comment_name(),
                               function_name_under=self.get_name().under,
                               arguments=common.wrap_non_empty('{', ', '.join(self.get_mqtt_arguments()), '}'))
 
class MQTTExampleSetterFunction(common.ExampleSetterFunction, MQTTExampleArgumentsMixin):
    def get_mqtt_source(self):
        template = "{comment1}{global_line_prefix}publish '{arguments}' to tinkerforge/request/{device_name}_{device_category}/{uid}/{function_name} {comment2}\n"
        bitmask_comments = []

        for argument in self.get_arguments():
            bitmask_comments.append(argument.get_mqtt_bitmask_comment())

        while None in bitmask_comments:
            bitmask_comments.remove(None)

        comment1 = self.get_formatted_comment1(global_line_prefix + '# {0}\n', '\r', '\n' + global_line_prefix + '# ')
        comment2 = self.get_formatted_comment2(' # {0}', '')

        if len(bitmask_comments) > 0:
            if comment1 == '\r':
                if len(comment2) == 0:
                    comment2 = ' # ' + ', '.join(bitmask_comments)
                else:
                    comment2 += ': ' + ', '.join(bitmask_comments)
            else:
                comment1 = comment1.rstrip('\n') + ': ' + ', '.join(bitmask_comments) + '\n'

        return template.format(global_line_prefix=global_line_prefix,
                               device_name=self.get_device().get_name().under,
                               device_category=self.get_device().get_category().under,
                               uid=self.get_example().get_dummy_uid(),
                               function_name=self.get_name().under,
                               arguments=common.wrap_non_empty('{', ', '.join(self.get_mqtt_arguments()), '}'),
                               comment1=comment1,
                               comment2=comment2)

class MQTTExampleCallbackFunction(common.ExampleCallbackFunction):
    def get_mqtt_source(self):
        template1A = r"""# Handle incoming {function_name_comment} callbacks
"""
        template1B = r"""{override_comment}
"""
        template2 = r"""subscribe to tinkerforge/callback/{device_name}_{device_category}/{uid}/{function_name_under}
publish '{{"register": true}}' to tinkerforge/register/{device_name}_{device_category}/{uid}/{function_name_under} # Register {function_name_under} callback
"""
        override_comment = self.get_formatted_override_comment('# {0}', None, '\n# ')

        if override_comment == None:
            template1 = template1A
        else:
            template1 = template1B

        parameters = []

        for parameter in self.get_parameters():
            parameters.append(parameter.get_mqtt_source())

        while None in parameters:
            parameters.remove(None)

        
        return template1.format(function_name_comment=self.get_comment_name(),
                                override_comment=override_comment) + \
               template2.format(device_name=self.get_device().get_name().under,
                                device_category=self.get_device().get_category().under,
                                uid=self.get_example().get_dummy_uid(), 
                                function_name_under=self.get_name().under)

class MQTTExampleCallbackPeriodFunction(common.ExampleCallbackPeriodFunction, MQTTExampleArgumentsMixin):
    def get_mqtt_source(self):

        callback_fn = "set_{function_name_under}_period" if self.get_device().get_name().space.startswith('IMU') else "set_{function_name_under}_callback_period"
        callback_fn = callback_fn.format(function_name_under=self.get_name().under)

        templateA = r"""# Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
publish '{arguments}' to tinkerforge/request/{device_name}_{device_category}/{uid}/{callback_fn}
"""
        templateB = r"""# Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
# Note: The {function_name_comment} callback is only called every {period_sec_long}
#       if the {function_name_comment} has changed since the last call!
publish '{arguments}' to tinkerforge/request/{device_name}_{device_category}/{uid}/{callback_fn}
"""

        if self.get_device().get_name().space.startswith('IMU'):
            template = templateA # FIXME: special hack for IMU Brick (2.0) callback behavior and name mismatch
        else:
            template = templateB

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        args = self.get_mqtt_arguments(callback_fn) + ['"period": ' + str(period_msec)]

        return template.format(device_name=self.get_device().get_name().under,
                               uid=self.get_example().get_dummy_uid(), 
                               device_category=self.get_device().get_category().under,
                               callback_fn=callback_fn,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('{', ', '.join(args), '}'),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long)

class MQTTExampleCallbackThresholdMinimumMaximum(common.ExampleCallbackThresholdMinimumMaximum):
    def get_mqtt_source(self):
        template = '"min{{mm_name}}": {minimum}, "max{{mm_name}}": {maximum}'

        return template.format(minimum=self.get_formatted_minimum(template='{result}'),
                               maximum=self.get_formatted_maximum(template='{result}'))

class MQTTExampleCallbackThresholdFunction(common.ExampleCallbackThresholdFunction, MQTTExampleArgumentsMixin):
    def get_mqtt_source(self):

        callback_fn = "set_{function_name_under}_callback_threshold".format(function_name_under=self.get_name().under)

        template = r"""# Configure threshold for {function_name_comment} "{option_comment}"
publish '{arguments}' to tinkerforge/request/{device_name}_{device_category}/{uid}/{callback_fn}
"""
        packet = None
        for p in self.get_device().get_packets('function'):
            if callback_fn in p.get_name().under:
                packet = p

        packet_min_max_names = [elem.get_name().under[3:] for elem in packet.get_elements(direction='in') if elem.get_name().under.startswith('min') ]
        minimum_maximums = []
        
        for mm_name, minimum_maximum in zip(packet_min_max_names, self.get_minimum_maximums()):
            minimum_maximums.append(minimum_maximum.get_mqtt_source().format(mm_name=mm_name))

        option_name_unders = {'o' : 'outside', '<': 'smaller', '>': 'greater'}

        args = self.get_mqtt_arguments(callback_fn) + ['"option": "' + option_name_unders[self.get_option_char()]+'"'] + minimum_maximums

        return template.format(device_name=self.get_device().get_name().under,
                               device_category=self.get_device().get_category().under,
                               callback_fn=callback_fn,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('{', ', '.join(args), '}'),                               
                               option_comment=self.get_option_comment(),
                               uid=self.get_example().get_dummy_uid())

class MQTTExampleCallbackConfigurationFunction(common.ExampleCallbackConfigurationFunction, MQTTExampleArgumentsMixin):
    def get_mqtt_source(self):
        callback_fn = "set_{function_name_under}_callback_configuration".format(function_name_under=self.get_name().under)

        templateA = r"""# Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms)
publish '{arguments}' to tinkerforge/request/{device_name}_{device_category}/{uid}/{callback_fn} 
"""
        templateB = r"""# Set period for {function_name_comment} callback to {period_sec_short} ({period_msec}ms) without a threshold
publish '{arguments}' to tinkerforge/request/{device_name}_{device_category}/{uid}/{callback_fn}  
"""
        templateC = r"""# Configure threshold for {function_name_comment} "{option_comment}"
# with a debounce period of {period_sec_short} ({period_msec}ms)
publish '{arguments}' to tinkerforge/request/{device_name}_{device_category}/{uid}/{callback_fn}  
"""

        if self.get_option_char() == None:
            template = templateA
            add_option = False
        elif self.get_option_char() == 'x':
            template = templateB
            add_option = True
        else:
            template = templateC
            add_option = True

        period_msec, period_sec_short, period_sec_long = self.get_formatted_period()

        packet = None
        for p in self.get_device().get_packets('function'):
            if callback_fn in p.get_name().under:
                packet = p

        packet_min_max_names = [elem.get_name().under[3:] for elem in packet.get_elements(direction='in') if elem.get_name().under.startswith('min') ]
        minimum_maximums = []
        
        for mm_name, minimum_maximum in zip(packet_min_max_names, self.get_minimum_maximums()):
            minimum_maximums.append(minimum_maximum.get_mqtt_source().format(mm_name=mm_name))

        option_name_unders = {None: '', 'x' : 'off', 'o' : 'outside', '<': 'smaller', '>': 'greater'}

        args = self.get_mqtt_arguments(callback_fn) + ['"period": ' + str(period_msec), '"value_has_to_change": ' + self.get_value_has_to_change('true', 'false', '')]
        if add_option:
            args += ['"option": "' + option_name_unders[self.get_option_char()]+'"']
        args += minimum_maximums

        return template.format(device_name=self.get_device().get_name().under,
                               uid=self.get_example().get_dummy_uid(), 
                               device_category=self.get_device().get_category().under,
                               callback_fn=callback_fn,
                               function_name_comment=self.get_comment_name(),
                               arguments=common.wrap_non_empty('{', ', '.join(args), '}'),
                               period_msec=period_msec,
                               period_sec_short=period_sec_short,
                               period_sec_long=period_sec_long,
                               option_comment=self.get_option_comment())

    
class MQTTExampleSpecialFunction(common.ExampleSpecialFunction):
    def get_mqtt_defines(self):
        return []

    def get_mqtt_function(self):
        return None

    def get_mqtt_source(self):
        global global_line_prefix

        type_ = self.get_type()

        if type_ == 'empty':
            return ''
        elif type_ == 'debounce_period':
            template = r"""# Get threshold callbacks with a debounce time of {period_sec} ({period_msec}ms)
publish '{{"debounce": {period_msec}}}' to tinkerforge/request/{device_name}_{device_category}/{uid}/set_debounce_period
"""
            period_msec, period_sec = self.get_formatted_debounce_period()

            return template.format(device_name=self.get_device().get_name().dash,
                                   uid=self.get_example().get_dummy_uid(), 
                                   device_category=self.get_device().get_category().dash,
                                   period_msec=period_msec,
                                   period_sec=period_sec)
        elif type_ == 'sleep':
            template = '{comment1}{global_line_prefix}wait for {duration}s {comment2}\n'
            duration = self.get_sleep_duration()

            if duration % 1000 == 0:
                duration //= 1000
            else:
                duration /= 1000.0

            return template.format(global_line_prefix=global_line_prefix,
                                   duration=duration,
                                   comment1=self.get_formatted_sleep_comment1(global_line_prefix + '# {0}\n', '\r', '\n' + global_line_prefix + '# '),
                                   comment2=self.get_formatted_sleep_comment2(' # {0}', ''))
        elif type_ == 'wait':
            return None
        elif type_ == 'loop_header':
            template = '{comment}for i in {limit}; do\n'
            global_line_prefix = '\t'

            return template.format(limit=' '.join(map(str, range(self.get_loop_header_limit()))),
                                   comment=self.get_formatted_loop_header_comment('# {0}\n', '', '\n# '))
        elif type_ == 'loop_footer':
            global_line_prefix = ''

            return '\rdone\n'

class MQTTExamplesGenerator(common.ExamplesGenerator):
    def get_bindings_name(self):
        return 'mqtt'

    def get_example_class(self):
        return MQTTExample

    def get_example_argument_class(self):
        return MQTTExampleArgument

    def get_example_parameter_class(self):
        return MQTTExampleParameter

    def get_example_result_class(self):
        return MQTTExampleResult

    def get_example_getter_function_class(self):
        return MQTTExampleGetterFunction

    def get_example_setter_function_class(self):
        return MQTTExampleSetterFunction

    def get_example_callback_function_class(self):
        return MQTTExampleCallbackFunction

    def get_example_callback_period_function_class(self):
        return MQTTExampleCallbackPeriodFunction

    def get_example_callback_threshold_minimum_maximum_class(self):
        return MQTTExampleCallbackThresholdMinimumMaximum

    def get_example_callback_threshold_function_class(self):
        return MQTTExampleCallbackThresholdFunction

    def get_example_callback_configuration_function_class(self):
        return MQTTExampleCallbackConfigurationFunction

    def get_example_special_function_class(self):
        return MQTTExampleSpecialFunction

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
            'led-strip-bricklet/callback',
            'nfc-bricklet/emulate-ndef',
            'nfc-bricklet/write-read-type2',
            'nfc-rfid-bricklet/write-read-type2'
        ]

        for example in examples:
            filename = 'example-{0}.txt'.format(example.get_name().dash)
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
                f.write(example.get_mqtt_source())

def generate(root_dir):
    common.generate(root_dir, 'en', MQTTExamplesGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
