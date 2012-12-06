#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Bindings Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_c_bindings.py: Generator for C/C++ bindings

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

def format_doc(packet):
    text = common.select_lang(packet.get_doc()[1])
    link = '{{@link {0}_{1}}}'
    link_c = '{{@link {0}_CALLBACK_{1}}}'

    # handle tables
    lines = text.split('\n')
    replaced_lines = []
    in_table_head = False
    in_table_body = False

    for line in lines:
        if line.strip() == '.. csv-table::':
            in_table_head = True
            replaced_lines.append('\\verbatim')
        elif line.strip().startswith(':header: ') and in_table_head:
            replaced_lines.append(line[len(':header: '):])
        elif line.strip().startswith(':widths:') and in_table_head:
            pass
        elif len(line.strip()) == 0 and in_table_head:
            in_table_head = False
            in_table_body = True

            replaced_lines.append('')
        elif len(line.strip()) == 0 and in_table_body:
            in_table_body = False

            replaced_lines.append('\\endverbatim')
            replaced_lines.append('')
        else:
            replaced_lines.append(line)

    text = '\n'.join(replaced_lines)

    for other_packet in device.get_packets():
        name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
        if other_packet.get_type() == 'callback':
            name = other_packet.get_upper_case_name()
            name_right = link_c.format(device.get_upper_case_name(), name)
        else:
            name = other_packet.get_underscore_name()
            name_right = link.format(device.get_underscore_name(), name)

        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", "parameter")
    text = text.replace(":word:`parameters`", "parameters")
    text = text.replace('.. note::', '\\note')
    text = text.replace('.. warning::', '\\warning')

    text = common.handle_rst_if(text, device)
    text = common.handle_since_firmware(text, device, packet)

    return '\n * '.join(text.strip().split('\n'))

def make_parameter_list(packet):
    param = ''
    for element in packet.get_elements():
        c_type = get_c_type(element[1])
        name = element[0]
        pointer = ''
        arr = ''
        if element[3] == 'out':
            pointer = '*'
            name = "ret_{0}".format(name)
        if element[2] > 1:
            arr = '[{0}]'.format(element[2])
            pointer = ''
       
        param += ', {0} {1}{2}{3}'.format(c_type, pointer, name, arr)
    return param

def get_c_type(py_type):
    if py_type == 'string':
        return 'char'
    if py_type in ( 'int8',  'int16',  'int32' , 'int64', \
                   'uint8', 'uint16', 'uint32', 'uint64'):
        return "{0}_t".format(py_type)
    return py_type

def make_include_c():
    include = """{0}
#include "{1}_{2}.h"

#include <string.h>

"""
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    return include.format(common.gen_text_star.format(date),
                          device.get_category().lower(),
                          device.get_underscore_name())

def make_function_id_defines():
    define_temp =  """
/**
 * \ingroup {4}{3}
 */
#define {0}_FUNCTION_{1} {2}
"""

    defines = ''
    for packet in device.get_packets('function'):
        defines += define_temp.format(device.get_upper_case_name(),
                                      packet.get_upper_case_name(),
                                      packet.get_function_id(),
                                      device.get_camel_case_name(),
                                      device.get_category())

    return defines

def make_callback_defines():
    define_temp = """
/**
 * \ingroup {5}{4}
 *
 * {3}
 */
#define {0}_CALLBACK_{1} {2}
"""

    defines = ''
    for packet in device.get_packets('callback'):
        doc = format_doc(packet)
        defines += define_temp.format(device.get_upper_case_name(),
                                      packet.get_upper_case_name(),
                                      packet.get_function_id(),
                                      doc,
                                      device.get_camel_case_name(),
                                      device.get_category())

    return defines

def make_structs():
    structs = """
#if defined _MSC_VER || defined __BORLANDC__
\t#pragma pack(push)
\t#pragma pack(1)
\t#define ATTRIBUTE_PACKED
#elif defined __GNUC__
\t#define ATTRIBUTE_PACKED __attribute__((packed))
#else
\t#error unknown compiler, do not know how to enable struct packing
#endif
"""

    struct_temp = """
typedef struct {{
\tPacketHeader header;
{0}}} ATTRIBUTE_PACKED {1}{2}_;
"""

    for packet in device.get_packets():
        if packet.get_type() == 'callback':
            cb = "Callback"
            struct_body = ''
            for element in packet.get_elements():
                c_type = get_c_type(element[1])
                if element[2] > 1:
                    struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                              element[0],
                                                              element[2]);
                else:
                    struct_body += '\t{0} {1};\n'.format(c_type, element[0])

            structs += struct_temp.format(struct_body, packet.get_camel_case_name(), cb)
            continue

        struct_body = ''
        for element in packet.get_elements('in'):
            c_type = get_c_type(element[1])
            if element[2] > 1:
                struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                          element[0],
                                                          element[2]);
            else:
                struct_body += '\t{0} {1};\n'.format(c_type, element[0])

        structs += struct_temp.format(struct_body, packet.get_camel_case_name(), '')

        if len(packet.get_elements('out')) == 0:
            continue

        struct_body = ''
        for element in packet.get_elements('out'):
            c_type = get_c_type(element[1])
            if element[2] > 1:
                struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                          element[0],
                                                          element[2]);
            else:
                struct_body += '\t{0} {1};\n'.format(c_type, element[0])

        structs += struct_temp.format(struct_body, packet.get_camel_case_name(), 'Response')

    structs += """
#if defined _MSC_VER || defined __BORLANDC__
\t#pragma pack(pop)
#endif
#undef ATTRIBUTE_PACKED
"""    
    return structs

def make_create_func():
    func = """
void {0}_create({1} *{0}, const char *uid, IPConnection *ipcon) {{
\tdevice_create({0}, uid, ipcon);

\t{0}->api_version[0] = {3};
\t{0}->api_version[1] = {4};
\t{0}->api_version[2] = {5};
{2}
}}
"""
    func2 = """
void {0}_destroy({1} *{0}) {{
\tdevice_destroy({0});
}}
"""

    cb_temp = """
\t{0}->callback_wrappers[{3}_CALLBACK_{1}] = {0}_callback_wrapper_{2};"""

    cbs = ''
    dev_name = device.get_underscore_name()
    for packet in device.get_packets('callback'):
        type_name = packet.get_underscore_name()
        cbs += cb_temp.format(dev_name, type_name.upper(), type_name, dev_name.upper())

    response_expected = ''

    for packet in device.get_packets():
        if packet.get_type() == 'callback':
            prefix = 'CALLBACK'
            flag = 'DEVICE_RESPONSE_EXPECTED_ALWAYS_FALSE'
        elif len(packet.get_elements('out')) > 0:
            prefix = 'FUNCTION'
            flag = 'DEVICE_RESPONSE_EXPECTED_ALWAYS_TRUE'
        else:
            prefix = 'FUNCTION'
            flag = 'DEVICE_RESPONSE_EXPECTED_FALSE'

        response_expected += '\t{0}->response_expected[{1}_{2}_{3}] = {4};\n' \
            .format(dev_name, device.get_upper_case_name(), prefix, packet.get_upper_case_name(), flag)

    if len(response_expected) > 0:
        response_expected = '\n' + response_expected

    return func.format(dev_name, device.get_camel_case_name(), response_expected + cbs,
                       *device.get_api_version()) + \
           func2.format(dev_name, device.get_camel_case_name())

def make_method_funcs():
    def make_struct_list(packet):
        struct_list = ''
        needs_i = False
        for element in packet.get_elements('in'):
            sf = 'request'
            if element[1] == 'string':
                temp = '\n\tstrncpy({0}.{1}, {1}, {2});\n'
                struct_list += temp.format(sf, element[0], element[2])
            elif element[2] > 1:
                if common.get_type_size(element[1]) > 1:
                    needs_i = True
                    struct_list += '\n\tfor (i = 0; i < {3}; i++) {0}.{1}[i] = leconvert_{2}_to({1}[i]);' \
                                   .format(sf, element[0], element[1], element[2])
                else:
                    temp = '\n\tmemcpy({0}.{1}, {1}, {2}*sizeof({3}));'
                    struct_list += temp.format(sf,
                                               element[0],
                                               element[2],
                                               get_c_type(element[1]))
            elif common.get_type_size(element[1]) > 1:
                struct_list += '\n\t{0}.{1} = leconvert_{2}_to({1});'.format(sf, element[0], element[1])
            else:
                struct_list += '\n\t{0}.{1} = {1};'.format(sf, element[0])
        return struct_list, needs_i

    def make_return_list(packet):
        return_list = ''
        needs_i = False
        for element in packet.get_elements('out'):
            sf = 'response'
            if element[1] == 'string':
                temp = '\tstrncpy(ret_{0}, {1}->{0}, {2});\n'
                return_list += temp.format(element[0], sf, element[2])
            elif element[2] > 1:
                if common.get_type_size(element[1]) > 1:
                    needs_i = True
                    return_list += '\tfor (i = 0; i < {3}; i++) ret_{0}[i] = leconvert_{2}_from({1}->{0}[i]);\n' \
                                   .format(element[0], sf, element[1], element[2])
                else:
                    temp = '\tmemcpy(ret_{0}, {1}->{0}, {2} * sizeof({3}));\n'
                    return_list += temp.format(element[0],
                                               sf,
                                               element[2],
                                               get_c_type(element[1]))
            elif common.get_type_size(element[1]) > 1:
                return_list += '\t*ret_{0} = leconvert_{2}_from({1}->{0});\n'.format(element[0], sf, element[1])
            else:
                return_list += '\t*ret_{0} = {1}->{0};\n'.format(element[0], sf)
        return return_list, needs_i

    func_version = """
int {0}_get_api_version({1} *{0}, uint8_t ret_api_version[3]) {{
\tret_api_version[0] = {0}->api_version[0];
\tret_api_version[1] = {0}->api_version[1];
\tret_api_version[2] = {0}->api_version[2];

\treturn E_OK;
}}
"""

    func = """
int {0}_{1}({2} *{0}{3}) {{
\t{5}_ request;{6}
\tint ret;{9}

\tmutex_lock(&{0}->request_mutex);

\tpacket_header_create(&request.header, sizeof(request), {4}, {0}->ipcon, {0});
{7}

\tret = device_send_request({0}, (Packet *)&request);
{8}
\tmutex_unlock(&{0}->request_mutex);

\treturn ret;
}}
"""

    func_ret = """
\tif (ret < 0) {{
\t\tmutex_unlock(&{1}->request_mutex);

\t\treturn ret;
\t}}

\tresponse = ({0}Response_ *)&{1}->response_packet;
{2}
"""

    sizeof_ret = """\t{0}->response.function_id = {1};
\t{0}->response.length = sizeof({2}Response_);
"""

    device_name = device.get_underscore_name()
    c = device.get_camel_case_name()

    funcs = ''
    for packet in device.get_packets('function'):
        packet_name = packet.get_underscore_name()
        d = make_parameter_list(packet)
        fid = '{0}_FUNCTION_{1}'.format(device.get_upper_case_name(),
                                        packet.get_upper_case_name())
        f = packet.get_camel_case_name()
        h, needs_i = make_struct_list(packet)
        if len(packet.get_elements('out')) > 0:
            g = '\n\t' + f + 'Response_ *response;'
            rl, needs_i2 = make_return_list(packet)
            i = func_ret.format(f, device_name, rl)
            j = sizeof_ret.format(device_name, fid, f)
        else:
            g = ''
            i = ''
            needs_i2 = False
            j = ''
        if needs_i or needs_i2:
            k = '\n\tint i;'
        else:
            k = ''

        funcs += func.format(device_name, packet_name, c, d, fid, f, g, h, i, k)

    return funcs + func_version.format(device_name, c)

def make_register_callback_func():
    func = """
void {0}_register_callback({1} *{0}, uint8_t id, void *callback, void *user_data) {{
\t{0}->registered_callbacks[id] = callback;
\t{0}->registered_callback_user_data[id] = user_data;
}}
"""
    return func.format(device.get_underscore_name(), device.get_camel_case_name())

def make_callback_wrapper_funcs():
    func = """
static void {0}_callback_wrapper_{1}({2} *{0}, Packet *packet) {{
\t{3}CallbackFunction callback_function = ({3}CallbackFunction){0}->registered_callbacks[{7}];
\tvoid *user_data = {0}->registered_callback_user_data[{7}];{9}{8}
{6}
\tif (callback_function != NULL) {{
\t\tcallback_function({5}{4}user_data);
\t}}
}}
"""

    funcs = ''
    for packet in device.get_packets('callback'):
        a = device.get_underscore_name()
        b = packet.get_underscore_name()
        c = device.get_camel_case_name()
        d = packet.get_camel_case_name()
        e = ''
        f_list = []
        for element in packet.get_elements():
            f_list.append("callback->{0}".format(element[0]))
        f = ', '.join(f_list)
        if len(f_list) > 0:
            e = ', '
        endian_list = []
        i = ''
        for element in packet.get_elements():
            if common.get_type_size(element[1]) > 1:
                if element[2] > 1:
                    i = '\n\tint i;'
                    endian_list.append('\tfor (i = 0; i < {2}; i++) callback->{0}[i] = leconvert_{1}_from(callback->{0}[i]);' \
                                       .format(element[0], element[1], element[2]))
                else:
                    endian_list.append('\tcallback->{0} = leconvert_{1}_from(callback->{0});'.format(element[0], element[1]))
        endian = '\n'.join(endian_list)
        if len(endian) > 0:
            endian = '\n' + endian + '\n'
        fid = '{0}_CALLBACK_{1}'.format(device.get_upper_case_name(),
                                        packet.get_upper_case_name())
        if len(f_list) > 0:
            cb = '\n\t{0}Callback_ *callback = ({0}Callback_ *)packet;'.format(d)
        else:
            cb = '\n\t(void)packet;'

        funcs += func.format(a, b, c, d, e, f, endian, fid, cb, i)

    return funcs

def make_include_h():
    include = """{0}
#ifndef {1}_{2}_H
#define {1}_{2}_H

#include "ip_connection.h"

/**
 * \defgroup {4}{3} {3} {4}
 */

/**
 * \ingroup {4}{3}
 *
 * {5}
 */
typedef Device {3};
"""

    date = datetime.datetime.now().strftime("%Y-%m-%d")
    upper_type = device.get_category().upper()
    upper_name = device.get_upper_case_name()

    return include.format(common.gen_text_star.format(date),
                          upper_type, 
                          upper_name, 
                          device.get_camel_case_name(),
                          device.get_category(),
                          device.get_description())

def make_end_h():
    return "\n#endif\n"

def make_typedefs():
    typedef = """
typedef void (*{0}CallbackFunction)({1});
"""

    typedefs = '\n'
    for packet in device.get_packets('callback'):
        name = packet.get_camel_case_name()
        c_type_list = []
        for element in packet.get_elements():
            if element[2] > 1:
                c_type_list.append('{0}[{1}]'.format(get_c_type(element[1]), element[2]))
            else:
                c_type_list.append(get_c_type(element[1]))

        typedefs += typedef.format(name, ', '.join(c_type_list + ['void *']))

    return typedefs

def make_create_declaration():
    create = """
/**
 * \ingroup {2}{1}
 *
 * Creates an object with the unique device ID \c uid. This object can then be
 * added to the IP connection.
 */
void {0}_create({1} *{0}, const char *uid, IPConnection *ipcon);
"""
    destroy = """
/**
 * \ingroup {2}{1}
 *
 * Creates an object with the unique device ID \c uid. This object can then be
 * added to the IP connection.
 */
void {0}_destroy({1} *{0});
"""
    return create.format(device.get_underscore_name(),
                         device.get_camel_case_name(),
                         device.get_category()) + \
           destroy.format(device.get_underscore_name(),
                          device.get_camel_case_name(),
                          device.get_category())

def make_method_declarations():
    func_version = """
/**
 * \ingroup {2}{1}
 *
 * Returns the name (including the hardware version), the firmware version
 * and the binding version of the device. The firmware and binding versions are
 * given in arrays of size 3 with the syntax [major, minor, revision].
 */
int {0}_get_api_version({1} *{0}, uint8_t ret_api_version[3]);
"""
    func = """
/**
 * \ingroup {5}{2}
 *
 * {4}
 */
int {0}_{1}({2} *{0}{3});
"""

    a = device.get_underscore_name()
    c = device.get_camel_case_name()

    funcs = ''
    for packet in device.get_packets('function'):
        b = packet.get_underscore_name()
        d = make_parameter_list(packet)
        doc = format_doc(packet)

        funcs += func.format(a, b, c, d, doc, device.get_category())

    return func_version.format(a, c, device.get_category()) + funcs

def make_register_callback_declaration():
    if device.get_callback_count() == 0:
        return '\n'

    func = """
/**
 * \ingroup {2}{1}
 *
 * Registers a callback with ID \c id to the function \c callback.
 */
void {0}_register_callback({1} *{0}, uint8_t id, void *callback, void *user_data);
"""
    return func.format(device.get_underscore_name(), device.get_camel_case_name(), device.get_category())

def make_callback_wrapper_declarations():
    func = 'int {0}_callback_wrapper_{1}({2} *{0}, const unsigned char *buffer);\n'

    funcs = '\n'
    for packet in device.get_packets('callback'):
        funcs += func.format(device.get_underscore_name(),
                             packet.get_underscore_name(),
                             device.get_camel_case_name())

    return funcs

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)
    file_name = '{0}_{1}'.format(device.get_category().lower(), device.get_underscore_name())
    directory += '/bindings'

    c = file('{0}/{1}.c'.format(directory, file_name), "w")
    c.write(make_include_c())
    c.write(make_typedefs())
    c.write(make_structs())
    c.write(make_callback_wrapper_funcs())
    c.write(make_create_func())
    c.write(make_method_funcs())
    c.write(make_register_callback_func())

    h = file('{0}/{1}.h'.format(directory, file_name), "w")
    h.write(make_include_h())
    h.write(make_function_id_defines())
    h.write(make_callback_defines())
    h.write(make_create_declaration())
    h.write(make_register_callback_declaration())
    h.write(make_method_declarations())
    h.write(make_end_h())

if __name__ == "__main__":
    common.generate(os.getcwd(), 'en', make_files, common.prepare_bindings, False)
