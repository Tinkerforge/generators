#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Shell Bindings Generator
Copyright (C) 2013 Matthias Bolte <matthias@tinkerforge.com>

generator_shell_bindings.py: Generator for shell bindings

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

import datetime
import sys
import os

sys.path.append(os.path.split(os.getcwd())[0])
import common
import shell_common

device = None
call_devices = []
dispatch_devices = []
device_identifier_symbols = []
completion_devices = []
getter_patterns = []
setter_patterns = []
callback_patterns = []

def make_format_list(packet, direction):
    formats = []

    for element in packet.get_elements(direction):
        formats.append(element.get_shell_struct_format())

    return ' '.join(formats)

def make_class():
    klass = """
class {0}(Device):"""

    return klass.format(device.get_shell_class_name())

def make_init_method():
    init = """
\tdef __init__(self, uid, ipcon):
\t\tDevice.__init__(self, uid, ipcon)

{0}
"""
    response_expected = []

    for packet in device.get_packets('function'):
        if len(packet.get_elements('out')) > 0:
            flag = 1 #'Device.RESPONSE_EXPECTED_ALWAYS_TRUE'
        elif packet.get_doc()[0] == 'ccf':
            flag = 3 #'Device.RESPONSE_EXPECTED_TRUE'
        else:
            flag = 4 #'Device.RESPONSE_EXPECTED_FALSE'

        response_expected.append('re[{0}] = {1}'.format(packet.get_function_id(), flag))

    if len(response_expected) > 0:
        return init.format('\t\tre = self.response_expected\n\t\t' + '; '.join(response_expected))
    else:
        return init.format('')

def make_callback_formats():
    callbacks = []
    callback = "cf[{0}] = '{1}'"

    for packet in device.get_packets('callback'):
        callbacks.append(callback.format(packet.get_function_id(),
                                         make_format_list(packet, 'out')))

    if len(callbacks) > 0:
        return '\t\tcf = self.callback_formats\n\t\t' + '; '.join(callbacks) + '\n'
    else:
        return '\n'

def make_call_header():
    header = """
def call_{0}_{1}(ctx, argv):
\tprog_prefix = 'call {2} <uid>'

"""

    return header.format(device.get_underscore_name(),
                         device.get_category().lower(),
                         device.get_shell_device_name())

def make_call_functions():
    setter = """\tdef {0}(ctx, argv):
\t\tparser = ParserWithExpectResponse(ctx, prog_prefix + ' {1}')
{2}
\t\targs = parser.parse_args(argv)

\t\tdevice_send_request(ctx, {7}{8}, {3}, ({4}), '{5}', '{6}', None, args.expect_response, [], [])
"""
    getter = """\tdef {0}(ctx, argv):
\t\tparser = ParserWithExecute(ctx, prog_prefix + ' {1}')
{2}
\t\targs = parser.parse_args(argv)

\t\tdevice_send_request(ctx, {7}{8}, {3}, ({4}), '{5}', '{6}', args.execute, False, [{9}], [{10}])
"""
    get_identity = """\tdef get_identity(ctx, argv):
\t\tcommon_get_identity(ctx, prog_prefix, {0}, argv)
"""

    functions = []
    entries = []

    for packet in device.get_packets('function'):
        if packet.get_function_id() == 255:
            function = get_identity.format(device.get_shell_class_name())
        else:
            params = []
            request_data = []

            for element in packet.get_elements('in'):
                name = element.get_underscore_name()
                type_converter = element.get_shell_type_converter()
                help = element.get_shell_help()
                metavar = "'<{0}>'".format(element.get_dash_name())

                params.append("\t\tparser.add_argument('{0}', type={1}, help={2}, metavar={3})".format(name, type_converter, help, metavar))
                request_data.append('args.{0}'.format(name))

            comma = ''
            if len(request_data) == 1:
                comma = ','

            if len(params) > 0:
                params = [''] + params + ['']

            output_names = []
            output_symbols = []

            for element in packet.get_elements('out'):
                output_names.append("'{0}'".format(element.get_dash_name()))

                if element.has_constants():
                    symbols = {}

                    for symbol in element.get_constants()[2]:
                        symbols[symbol[2]] = symbol[1].replace('_', '-')

                    output_symbols.append(str(symbols))
                else:
                    output_symbols.append('None')

            underscore_name = packet.get_underscore_name()

            if len(output_names) > 0:
                if not underscore_name.startswith('get_') and \
                   not underscore_name.startswith('is_') and \
                   not underscore_name.startswith('are_'):
                    getter_patterns.append(underscore_name.replace('_', '-'))

                function = getter.format(underscore_name,
                                         underscore_name.replace('_', '-'),
                                         '\n'.join(params),
                                         packet.get_function_id(),
                                         ', '.join(request_data) + comma,
                                         make_format_list(packet, 'in'),
                                         make_format_list(packet, 'out'),
                                         device.get_camel_case_name(),
                                         device.get_category(),
                                         ', '.join(output_names),
                                         ', '.join(output_symbols))
            else:
                if not underscore_name.startswith('set_'):
                    setter_patterns.append(underscore_name.replace('_', '-'))

                function = setter.format(underscore_name,
                                         underscore_name.replace('_', '-'),
                                         '\n'.join(params),
                                         packet.get_function_id(),
                                         ', '.join(request_data) + comma,
                                         make_format_list(packet, 'in'),
                                         make_format_list(packet, 'out'),
                                         device.get_camel_case_name(),
                                         device.get_category())

        functions.append(function)

        entries.append("'{0}': {1}".format(packet.get_underscore_name().replace('_', '-'),
                                           packet.get_underscore_name()))

    return '\n'.join(functions) + '\n\tfunctions = {\n\t' + ',\n\t'.join(entries) + '\n\t}'

def make_call_footer():
    footer = """

\tcall_generic(ctx, '{0}', functions, argv)
"""

    return footer.format(device.get_shell_device_name())

def make_dispatch_header():
    header = """
def dispatch_{0}_{1}(ctx, argv):
\tprog_prefix = 'dispatch {2} <uid>'

"""

    return header.format(device.get_underscore_name(),
                         device.get_category().lower(),
                         device.get_shell_device_name())

def make_dispatch_functions():
    func = """\tdef {0}(ctx, argv):
\t\tparser = ParserWithExecute(ctx, prog_prefix + ' {1}')

\t\targs = parser.parse_args(argv)

\t\tdevice_callback(ctx, {2}{3}, {4}, args.execute, [{5}])
"""

    functions = []
    entries = []

    for packet in device.get_packets('callback'):
        output = []

        for element in packet.get_elements('out'):
            output.append("'{0}'".format(element.get_dash_name()))

        underscore_name = packet.get_underscore_name()

        function = func.format(underscore_name,
                               underscore_name.replace('_', '-'),
                               device.get_camel_case_name(),
                               device.get_category(),
                               packet.get_function_id(),
                               ', '.join(output))

        entries.append("'{0}': {1}".format(underscore_name.replace('_', '-'),
                                           underscore_name))

        callback_patterns.append(underscore_name.replace('_', '-'))

        functions.append(function)

    return '\n'.join(functions) + '\n\tcallbacks = {\n\t' + ',\n\t'.join(entries) + '\n\t}'

def make_dispatch_footer():
    footer = """

\tdispatch_generic(ctx, '{0}', callbacks, argv)
"""

    return footer.format(device.get_shell_device_name())

def finish(directory):
    version = common.get_changelog_version(directory)
    shell = file('{0}/tinkerforge'.format(directory), 'wb')
    header = file('{0}/tinkerforge.header'.format(directory), 'rb').read().replace('<<VERSION>>', '.'.join(version))
    footer = file('{0}/tinkerforge.footer'.format(directory), 'rb').read().replace('<<VERSION>>', '.'.join(version))
    directory += '/bindings'

    shell.write(header)

    ipcon = file(os.path.join(directory, '..', '..', 'python', 'ip_connection.py'), 'rb').read()
    shell.write('\n\n\n' + ipcon + '\n\n\n')

    for part in os.listdir(directory):
        shell.write(file(os.path.join(directory, part), 'rb').read())

    shell.write('\ncall_devices = {\n' + ',\n'.join(call_devices) + '\n}\n')
    shell.write('\ndispatch_devices = {\n' + ',\n'.join(dispatch_devices) + '\n}\n')
    shell.write('\ndevice_identifier_symbols = {\n' + ',\n'.join(device_identifier_symbols) + '\n}\n')
    shell.write(footer)
    shell.close()
    os.system('chmod +x {0}/../tinkerforge'.format(directory))

    template = file('{0}/../tinkerforge-bash-completion.template'.format(directory), 'rb').read()
    template = template.replace('<<DEVICES>>', '|'.join(sorted(completion_devices)))

    if len(getter_patterns) > 0:
        template = template.replace('<<GETTER>>', '|' + '|'.join(sorted(list(set(getter_patterns)))))
    else:
        template = template.replace('<<GETTER>>', '')

    if len(setter_patterns) > 0:
        template = template.replace('<<SETTER>>', '|' + '|'.join(sorted(list(set(setter_patterns)))))
    else:
        template = template.replace('<<SETTER>>', '')

    if len(callback_patterns) > 0:
        template = template.replace('<<CALLBACK>>', '|' + '|'.join(sorted(list(set(callback_patterns)))))
    else:
        template = template.replace('<<CALLBACK>>', '')

    file('{0}/../tinkerforge-bash-completion.sh'.format(directory), 'wb').write(template)

class ShellBindingsGenerator(common.BindingsGenerator):
    def __init__(self, *args, **kwargs):
        common.BindingsGenerator.__init__(self, *args, **kwargs)

        self.released_files_name_prefix = 'shell'

    def get_device_class(self):
        return shell_common.ShellDevice

    def get_element_class(self):
        return shell_common.ShellElement

    def generate(self, device_):
        if not device_.is_released():
            return

        global device
        device = device_

        global call_devices
        call_devices.append("'{0}': call_{1}_{2}".format(device.get_shell_device_name(),
                                                         device.get_underscore_name(),
                                                         device.get_category().lower()))

        global dispatch_devices
        dispatch_devices.append("'{0}': dispatch_{1}_{2}".format(device.get_shell_device_name(),
                                                                 device.get_underscore_name(),
                                                                 device.get_category().lower()))

        global device_identifier_symbols
        device_identifier_symbols.append("{0}: '{1}'".format(device.get_device_identifier(),
                                                             device.get_shell_device_name()))

        global completion_devices
        completion_devices.append(device.get_shell_device_name())

        file_name = '{0}.part'.format(device.get_shell_device_name())

        shell = open(os.path.join(self.get_bindings_root_directory(), 'bindings', file_name), 'wb')
        shell.write(make_class())
        shell.write(make_init_method())
        shell.write(make_callback_formats())
        shell.write(make_call_header())
        shell.write(make_call_functions())
        shell.write(make_call_footer())
        shell.write(make_dispatch_header())
        shell.write(make_dispatch_functions())
        shell.write(make_dispatch_footer())
        shell.close()

        self.released_files.append(file_name)

    def finish(self):
        common.BindingsGenerator.finish(self)

        finish(self.get_bindings_root_directory())

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', ShellBindingsGenerator, False)

if __name__ == "__main__":
    generate(os.getcwd())
