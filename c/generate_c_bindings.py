#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bindings Generator
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_c_bindings.py: Generator for C bindings

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

com = None

gen_text = """\
/*************************************************************
 * This file was automatically generated on {0}.      *
 *                                                           *
 * If you have a bugfix for this file and want to commit it, *
 * please fix the bug in the generator. You can find a link  *
 * to the generator git on tinkerforge.com                   *
 *************************************************************/
"""

def make_parameter_list(packet):
    param = ''
    for element in packet['elements']:
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


def make_short_form(name):
    short = ''
    for x in name.split('_'):
        short += x[0].lower()

    return short

def has_outgoing(packet):
    return any(element[3] == 'out' for element in packet['elements'])

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
    lower_type = com['type'].lower()

    return include.format(gen_text.format(date), lower_type, com['name'][1])

def make_type_defines():
    define_temp = '#define TYPE_{0} {1}\n'

    defines = ''
    for i, packet in zip(range(len(com['packets'])), com['packets']):
        defines += define_temp.format(packet['name'][1].upper(), i+1)

    return defines

def make_callback_defines():
    define_temp = '#define {0}_CALLBACK_{1} {2}\n'

    defines = ''
    for i, packet in zip(range(len(com['packets'])), com['packets']):
        if packet['type'] != 'signal':
            continue
        defines += define_temp.format(com['name'][1].upper(), 
                                      packet['name'][1].upper(), 
                                      i+1)

    return defines


def make_structs():
    structs = """
#ifdef _MSC_VER
\t#pragma pack(push)
\t#pragma pack(1)

\t#define PACKED
#else
\t#define PACKED __attribute__((packed))
#endif
"""

    struct_temp = """
typedef struct {{
\tuint8_t stack_id;
\tuint8_t type;
\tuint16_t length;
{0}}} PACKED {1}{2}_;
"""

    for packet in com['packets']:
        if packet['type'] == 'signal':
            cb = "Callback"
            struct_body = ''
            for element in packet['elements']:
                c_type = get_c_type(element[1])
                if element[2] > 1:
                    struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                              element[0],
                                                              element[2]);
                else:
                    struct_body += '\t{0} {1};\n'.format(c_type, element[0])

            structs += struct_temp.format(struct_body, packet['name'][0], cb)
            continue

        struct_body = ''
        for element in packet['elements']:
            if element[3] == 'in':
                c_type = get_c_type(element[1])
                if element[2] > 1:
                    struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                              element[0],
                                                              element[2]);
                else:
                    struct_body += '\t{0} {1};\n'.format(c_type, element[0])

        structs += struct_temp.format(struct_body, packet['name'][0], '')

        if not has_outgoing(packet):
            continue

        struct_body = ''
        for element in packet['elements']:
            if element[3] == 'out':
                c_type = get_c_type(element[1])
                if element[2] > 1:
                    struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                              element[0],
                                                              element[2]);
                else:
                    struct_body += '\t{0} {1};\n'.format(c_type, element[0])

        structs += struct_temp.format(struct_body, packet['name'][0], 'Return')

    structs += """
#ifdef _MSC_VER
\t#pragma pack(pop)
#endif
"""    
    return structs

def make_create_func():
    func = """
void {0}_create({1} *{0}, const char *uid) {{
\tipcon_device_create({0}, uid);

\t{0}->binding_version[0] = {3};
\t{0}->binding_version[1] = {4};
\t{0}->binding_version[2] = {5};
{2}\n}}
"""

    cb_temp = """
\t{0}->device_callbacks[TYPE_{1}] = {0}_callback_{2};"""

    cbs = ''
    dev_name = com['name'][1]
    for packet in com['packets']:
        if packet['type'] != 'signal':
            continue
        type_name = packet['name'][1]
        cbs += cb_temp.format(dev_name, type_name.upper(), type_name)
    
    v = com['version']
    return func.format(dev_name, com['name'][0], cbs, v[0], v[1], v[2])

def make_method_funcs():
    def make_struct_list(packet):
        struct_list = ''
        for element in packet['elements']:
            if element[3] != 'in':
                continue
            
            sf = make_short_form(packet['name'][1])
            if element[1] == 'string':
                temp = '\n\tstrcpy({0}.{1}, {1});\n'
                struct_list += temp.format(sf, element[0])
            elif element[2] > 1:
                temp = '\n\tmemcpy({0}.{1}, {1}, {2}*sizeof({3}));'
                struct_list += temp.format(sf, 
                                           element[0], 
                                           element[2], 
                                           get_c_type(element[1]))
            else:
                struct_list += '\n\t{0}.{1} = {1};'.format(sf, element[0])
        return struct_list

    def make_return_list(packet):
        return_list = ''
        for element in packet['elements']:
            if element[3] != 'out':
                continue

            sf = make_short_form(packet['name'][1])
            if element[1] == 'string':
                temp = '\tstrcpy(ret_{0}, {1}r->{0});\n'
                return_list += temp.format(element[0], sf)
            elif element[2] > 1:
                temp = '\tmemcpy(ret_{0}, {1}r->{0}, {2}*sizeof({3}));\n'
                return_list += temp.format(element[0],
                                           sf, 
                                           element[2], 
                                           get_c_type(element[1]))
            else:
                temp = '\t*ret_{0} = {1}r->{0};\n'
                return_list += temp.format(element[0], sf)
        return return_list

    func_version = """
int {0}_get_version({1} *{0}, char ret_name[40], uint8_t ret_firmware_version[3], uint8_t ret_binding_version[3]) {{
	strncpy(ret_name, {0}->name, 40);

	ret_firmware_version[0] = {0}->firmware_version[0];
	ret_firmware_version[1] = {0}->firmware_version[1];
	ret_firmware_version[2] = {0}->firmware_version[2];

	ret_binding_version[0] = {0}->binding_version[0];
	ret_binding_version[1] = {0}->binding_version[1];
	ret_binding_version[2] = {0}->binding_version[2];

	return E_OK;
}}
"""

    func = """
int {0}_{1}({2} *{0}{3}) {{
\tif({0}->ipcon == NULL) {{
\t\treturn E_NOT_ADDED;
\t}}

\tipcon_sem_wait_write({0});

{9}\t{5}_ {6};
\t{6}.stack_id = {0}->stack_id;
\t{6}.type = {4};
\t{6}.length = sizeof({5}_);{7}

\tipcon_device_write({0}, (char *)&{6}, sizeof({5}_));

{10}{8}\tipcon_sem_post_write({0});

\treturn E_OK;
}}
"""

    func_ret = """\t{0}Return_ *{1}r = ({0}Return_ *){2}->answer.buffer;
{3}
"""

    sizeof_ret = """\t{0}->answer.type = {1};
\t{0}->answer.length = sizeof({2}Return_);
"""

    answer_sem = """\tif(ipcon_answer_sem_wait_timeout({0}) != 0) {{
\t\tipcon_sem_post_write({0});
\t\treturn E_TIMEOUT;
\t}}

"""

    a = com['name'][1]
    c = com['name'][0]

    funcs = ''
    for packet in com['packets']:
        if packet['type'] != 'method':
            continue

        b = packet['name'][1]
        d = make_parameter_list(packet)
        e = 'TYPE_{0}'.format(packet['name'][1].upper())
        f = packet['name'][0]
        g = make_short_form(b)
        h = make_struct_list(packet)
        if has_outgoing(packet):
            i = func_ret.format(f, g, a, make_return_list(packet))
            j = sizeof_ret.format(a, e, f)
            k = answer_sem.format(a)
        else:
            i = ''
            j = ''
            k = ''

        funcs += func.format(a, b, c, d, e, f, g, h, i, j, k)

    return funcs + func_version.format(a, c)

def make_set_callback_funcs():
    func = """
void {0}_set_callback_{1}({2} *{0}, {1}_func_t func) {{
\t{0}->callbacks[{3}] = (void*)func;
}}
"""
    
    funcs = ''       
    for packet in com['packets']:
        if packet['type'] != 'signal':
            continue


        funcs += func.format(com['name'][1], 
                             packet['name'][1], 
                             com['name'][0],
                             'TYPE_{0}'.format(packet['name'][1].upper()))
    return funcs

def make_register_callback_func():
    func = """
void {0}_register_callback({1} *{0}, uint8_t cb, void *func) {{
    {0}->callbacks[cb] = func;
}}
"""
    return func.format(com['name'][1], com['name'][0])

def make_callback_funcs():
    func = """
int {0}_callback_{1}({2} *{0}, const unsigned char *buffer) {{
\t{3}Callback_ *{4}c = ({3}Callback_ *)buffer;
\t(({1}_func_t){0}->callbacks[{4}c->type])({5});
\treturn sizeof({3}Callback_);
}}
"""

    funcs = ''
    for packet in com['packets']:
        if packet['type'] != 'signal':
            continue
        a = com['name'][1]
        b = packet['name'][1]
        c = com['name'][0]
        d = packet['name'][0]
        e = make_short_form(b)
        f_list = []
        for element in packet['elements']:
            f_list.append("{0}c->{1}".format(e, element[0]))
        f = ', '.join(f_list)

        funcs += func.format(a, b, c, d, e, f)

    return funcs

def make_include_h():
    include = """{0}
#ifndef {1}_{2}_H
#define {1}_{2}_H

#include "ip_connection.h"

typedef Device {3};

"""

    date = datetime.datetime.now().strftime("%d.%m.%Y")
    upper_type = com['type'].upper()
    upper_name = com['name'][1].upper()

    return include.format(gen_text.format(date), 
                          upper_type, 
                          upper_name, 
                          com['name'][0])

def make_end_h():
    return "\n#endif"

def make_typedefs():
    typedef = 'typedef void (*{0}_func_t)({1});\n'

    typedefs = '\n'
    for packet in com['packets']:
        if packet['type'] != 'signal':
            continue

        name = packet['name'][1]
        c_type_list = []
        for element in packet['elements']:
            c_type_list.append(get_c_type(element[1]))

        typedefs += typedef.format(name, ', '.join(c_type_list))

    return typedefs

def make_create_declaration():
    create = '\nvoid {0}_create({1} *{0}, const char *uid);\n\n'
    return create.format(com['name'][1], com['name'][0])

def make_method_declarations():
    func_version = """int {0}_get_version({1} *{0}, char ret_name[40], uint8_t ret_firmware_version[3], uint8_t ret_binding_version[3]);"""
    func = 'int {0}_{1}({2} *{0}{3});\n'
    a = com['name'][1]
    c = com['name'][0]

    funcs = ''
    for packet in com['packets']:
        b = packet['name'][1]
        d = make_parameter_list(packet)

        funcs += func.format(a, b, c, d)

    return funcs + func_version.format(a, c)

def make_set_callback_declarations():
    func = 'void {0}_set_callback_{1}({2} *{0}, {1}_func_t func);\n'

    funcs = '\n'       
    for packet in com['packets']:
        if packet['type'] != 'signal':
            continue

        funcs += func.format(com['name'][1], 
                             packet['name'][1],  
                             com['name'][0])
    return funcs

def make_register_callback_declaration():
    func = """
void {0}_register_callback({1} *{0}, uint8_t cb, void *func);
"""
    return func.format(com['name'][1], com['name'][0])

def make_callback_declarations():
    func = 'int {0}_callback_{1}({2} *{0}, const unsigned char *buffer);\n'

    funcs = '\n'
    for packet in com['packets']:
        if packet['type'] != 'signal':
            continue

        funcs += func.format(com['name'][1], 
                             packet['name'][1],
                             com['name'][0])

    return funcs

def make_files(com_new, directory):
    global com
    com = com_new

    file_name = '{0}_{1}'.format(com['type'].lower(), com['name'][1])
    
    directory += '/bindings'
    if not os.path.exists(directory):
        os.makedirs(directory)

    c = file('{0}/{1}.c'.format(directory, file_name), "w")
    c.write(make_include_c())
    c.write(make_type_defines())
    c.write(make_typedefs())
    c.write(make_structs())
    c.write(make_method_funcs())
    c.write(make_callback_funcs())
    c.write(make_register_callback_func())
    c.write(make_create_func())

    h = file('{0}/{1}.h'.format(directory, file_name), "w")
    h.write(make_include_h())
    h.write(make_callback_defines())
    h.write(make_create_declaration())
    h.write(make_method_declarations())
    h.write(make_register_callback_declaration())
    h.write(make_end_h())

def generate(path):
    path_list = path.split('/')
    path_list[-1] = 'configs'
    path_config = '/'.join(path_list)
    sys.path.append(path_config)
    configs = os.listdir(path_config)

    for config in configs:
        if config.endswith('_config.py'):
            module = __import__(config[:-3])
            print(" * {0}".format(config[:-10]))
            make_files(module.com, path)

if __name__ == "__main__":
    generate(os.getcwd())
