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

device = None
call_devices = []
dispatch_devices = []
devices_identifiers = []
completion_devices = []

def get_argparse_type_converter(element):
    types = {
        'int8':   'int',
        'uint8':  'int',
        'int16':  'int',
        'uint16': 'int',
        'int32':  'int',
        'uint32': 'int',
        'int64':  'int',
        'uint64': 'int',
        'bool':   'convert_bool',
        'char':   'convert_char',
        'string': 'str',
        'float':  'float'
    }

    t = types[element[1]]

    if element[2] == 1 or t == 'str':
        return t, 1
    else:
        return t, element[2]

def get_element_help(element):
    types = {
        'int8': 'int',
        'uint8': 'int',
        'int16': 'int',
        'uint16': 'int',
        'int32': 'int',
        'uint32': 'int',
        'int64': 'int',
        'uint64': 'int',
        'bool': 'bool',
        'char': 'char',
        'string': 'string',
        'float': 'float'
    }

    t = types[element[1]]

    if element[2] == 1 or t == 'string':
        return t
    else:
        return ','.join([t] * element[2])

def get_format(element):
    formats = {
        'int8':   'b',
        'uint8':  'B',
        'int16':  'h',
        'uint16': 'H',
        'int32':  'i',
        'uint32': 'I',
        'int64':  'q',
        'uint64': 'Q',
        'float':  'f',
        'bool':   '?',
        'string': 's',
        'char':   'c'
    }

    return formats[element[1]]

def make_format_list(packet, direction):
    formats = []

    for element in packet.get_elements(direction):
        number = ''

        if element[2] > 1:
            number = element[2]

        formats.append('{0}{1}'.format(number, get_format(element)))

    return ' '.join(formats)

def make_class():
    klass = """
class {0}{1}(Device):"""

    return klass.format(device.get_camel_case_name(),
                        device.get_category())

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
def call_{0}_{2}(argv):
\tprog_prefix = 'tinkerforge call {1}-{2} <uid>'

"""

    return header.format(device.get_underscore_name(),
                         device.get_underscore_name().replace('_', '-'),
                         device.get_category().lower())

def make_call_functions():
    setter = """\tdef {0}(argv):
\t\tparser = Parser(prog_prefix + ' {1}')
{2}
\t\targs = parser.parse_args(argv)

\t\tdevice_send_request({7}{8}, {3}, ({4}), '{5}', '{6}', None, False, [])
"""
    getter = """\tdef {0}(argv):
\t\tparser = ParserWithExecute(prog_prefix + ' {1}')
{2}
\t\targs = parser.parse_args(argv)

\t\tdevice_send_request({7}{8}, {3}, ({4}), '{5}', '{6}', args.execute, args.replace, [{9}])
"""
    get_identity = """\tdef get_identity(argv):
\t\tcommon_get_identity(prog_prefix, {0}{1}, argv)
"""

    functions = []
    entries = []

    for packet in device.get_packets('function'):
        if packet.get_function_id() == 255:
            function = get_identity.format(device.get_camel_case_name(),
                                           device.get_category())
        else:
            params = []
            request_data = []

            for element in packet.get_elements('in'):
                name = element[0]
                type, length = get_argparse_type_converter(element)
                help = get_element_help(element)
                metavar = "'<{0}>'".format(name.replace('_', '-'))

                if length > 1:
                    params.append("\t\tparser.add_argument('{0}', type=create_array_converter({1}, {2}), help='{3}', metavar={4})".format(name, type, length, help, metavar))
                else:
                    params.append("\t\tparser.add_argument('{0}', type={1}, help='{2}', metavar={3})".format(name, type, help, metavar))

                request_data.append('args.{0}'.format(element[0]))

            comma = ''
            if len(request_data) == 1:
                comma = ','

            if len(params) > 0:
                params = [''] + params + ['']

            output = []

            for element in packet.get_elements('out'):
                output.append("'{0}'".format(element[0].replace('_', '-')))

            if len(output) > 0:
                function = getter.format(packet.get_underscore_name(),
                                         packet.get_underscore_name().replace('_', '-'),
                                         '\n'.join(params),
                                         packet.get_function_id(),
                                         ', '.join(request_data) + comma,
                                         make_format_list(packet, 'in'),
                                         make_format_list(packet, 'out'),
                                         device.get_camel_case_name(),
                                         device.get_category(),
                                         ', '.join(output))
            else:
                function = setter.format(packet.get_underscore_name(),
                                         packet.get_underscore_name().replace('_', '-'),
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

\tcall_generic('{0}-{1}', functions, argv)
"""

    return footer.format(device.get_underscore_name().replace('_', '-'),
                         device.get_category().lower())

def make_dispatch_header():
    header = """
def dispatch_{0}_{2}(argv):
\tprog_prefix = 'tinkerforge dispatch {1}-{2} <uid>'

"""

    return header.format(device.get_underscore_name(),
                         device.get_underscore_name().replace('_', '-'),
                         device.get_category().lower())

def make_dispatch_functions():
    func = """\tdef {0}(argv):
\t\tparser = ParserWithExecute(prog_prefix + ' {1}')

\t\targs = parser.parse_args(argv)

\t\tdevice_callback({2}{3}, {4}, args.execute, args.replace, [{5}])
"""

    functions = []
    entries = []

    for packet in device.get_packets('callback'):
        output = []

        for element in packet.get_elements('out'):
            output.append("'{0}'".format(element[0].replace('_', '-')))

        function = func.format(packet.get_underscore_name(),
                               packet.get_underscore_name().replace('_', '-'),
                               device.get_camel_case_name(),
                               device.get_category(),
                               packet.get_function_id(),
                               ', '.join(output))

        entries.append("'{0}': {1}".format(packet.get_underscore_name().replace('_', '-'),
                                           packet.get_underscore_name()))

        functions.append(function)

    return '\n'.join(functions) + '\n\tcallbacks = {\n\t' + ',\n\t'.join(entries) + '\n\t}'

def make_dispatch_footer():
    footer = """

\tdispatch_generic('{0}-{1}', callbacks, argv)
"""

    return footer.format(device.get_underscore_name().replace('_', '-'),
                         device.get_category().lower())

def make_files(device_, directory):
    global device
    device = device_
    file_name = '{0}-{1}'.format(device.get_underscore_name().replace('_', '-'),
                                 device.get_category().lower())
    directory += '/bindings'

    global call_devices
    call_devices.append("'{0}-{1}': call_{2}_{1}".format(device.get_underscore_name().replace('_', '-'),
                                                         device.get_category().lower(),
                                                         device.get_underscore_name()))

    global dispatch_devices
    dispatch_devices.append("'{0}-{1}': dispatch_{2}_{1}".format(device.get_underscore_name().replace('_', '-'),
                                                                 device.get_category().lower(),
                                                                 device.get_underscore_name()))

    global devices_identifiers
    devices_identifiers.append("{0}: '{1}-{2}'".format(device.get_device_identifier(),
                                                       device.get_underscore_name().replace('_', '-'),
                                                       device.get_category().lower()))

    global completion_devices
    completion_devices.append('{0}-{1}'.format(device.get_underscore_name().replace('_', '-'),
                                               device.get_category().lower()))

    shell = file('{0}/{1}.part'.format(directory, file_name), 'wb')
    shell.write(make_class())
    shell.write(make_init_method())
    shell.write(make_callback_formats())
    shell.write(make_call_header())
    shell.write(make_call_functions())
    shell.write(make_call_footer())
    shell.write(make_dispatch_header())
    shell.write(make_dispatch_functions())
    shell.write(make_dispatch_footer())

def finish(directory):
    version = common.get_changelog_version(directory)
    shell = file('{0}/tinkerforge'.format(directory), 'wb')
    header = file('{0}/tinkerforge.header'.format(directory), 'rb').read()
    footer = file('{0}/tinkerforge.footer'.format(directory), 'rb').read().replace('<<VERSION>>', '.'.join(version))
    directory += '/bindings'

    shell.write(header)

    ipcon = file(os.path.join(directory, '..', '..', 'python', 'ip_connection.py'), 'rb').read()
    shell.write('\n\n\n' + ipcon + '\n\n\n')

    for part in os.listdir(directory):
        shell.write(file(os.path.join(directory, part), 'rb').read())

    shell.write('\ncall_devices = {\n' + ',\n'.join(call_devices) + '\n}\n')
    shell.write('\ndispatch_devices = {\n' + ',\n'.join(dispatch_devices) + '\n}\n')
    shell.write('\ndevices_identifiers = {\n' + ',\n'.join(devices_identifiers) + '\n}\n')
    shell.write(footer)
    shell.close()
    os.system('chmod +x tinkerforge')

    template = file('{0}/../tinkerforge-bash-completion.template'.format(directory), 'rb').read()
    template = template.replace('<<DEVICES>>', '|'.join(sorted(completion_devices)))
    file('{0}/../tinkerforge-bash-completion.sh'.format(directory), 'wb').write(template)

def generate(path):
    common.generate(path, 'en', make_files, common.prepare_bindings, finish, False)

if __name__ == "__main__":
    generate(os.getcwd())
