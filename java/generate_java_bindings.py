#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bindings Generator
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_python.py: Generator for Python bindings

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

gen_text = """/*************************************************************
 * This file was automatically generated on {0}.      *
 *                                                           *
 * If you have a bugfix for this file and want to commit it, *
 * please fix the bug in the generator. You can find a link  *
 * to the generator git on tinkerforge.com                   *
 *************************************************************/
"""

def make_import():
    include = """{0}
package com.tinkerforge;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.concurrent.TimeUnit;

"""
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    return include.format(gen_text.format(date))

def make_class():
    class_str = '\npublic class {0}{1} extends Device {{\n'
        
    return class_str.format(com['type'], com['name'][0])

def make_return_objects():
    objs = ''
    obj = """
\tpublic class {0} {{
{1}

\t\tpublic String toString() {{
\t\t\t return "[" + {2} "]";
\t\t}}
\t}}
"""
    param = '\t\tpublic {0}{1} {2}{3};'
    for i, packet in zip(range(len(com['packets'])), com['packets']):
        if packet['type'] == 'signal':
            continue

        if get_num_return(packet['elements']) < 2:
            continue

        name = get_object_name(packet)

        params = []
        tostr = []
        for element in packet['elements']:
            typ = get_java_type(element[1])
            ele_name = to_camel_case(element[0])
            arr = ''
            new = ''
            if element[2] > 1:
                arr = '[]'
                new = ' = new {0}[{1}]'.format(typ, element[2])

            to = '"{0} = " + {0} +'.format(ele_name)

            tostr.append(to)
            params.append(param.format(typ, arr, ele_name, new))
            
        objs += obj.format(name, 
                           '\n'.join(params),
                           ' ", " + '.join(tostr))
        
    return objs

def make_listener_definitions():
    cbs = ''
    cb = """
\tpublic interface {0}Listener {{
\t\tpublic void {1}({2});
\t}}
"""
    for i, packet in zip(range(len(com['packets'])), com['packets']):
        if packet['type'] != 'signal':
            continue

        name = packet['name'][0]
        name_lower = name[0].lower() + name[1:]
        parameter = make_parameter_list(packet)
        cbs += cb.format(name, name_lower, parameter)
    return cbs

def make_callback_listener_definitions():
    cbs = ''
    cb = """
\t\tcallbacks[TYPE_{0}] = new CallbackListener() {{
\t\t\tpublic void callback(byte[] data) {{{1}
\t\t\t\t(({2}Listener)listenerObjects[TYPE_{0}]).{3}({4});
\t\t\t}}
\t\t}};
"""

    data = """
\t\t\t\tByteBuffer bb = ByteBuffer.wrap(data, 4, data.length - 4);
\t\t\t\tbb.order(ByteOrder.LITTLE_ENDIAN);

{1}"""
    cbs_end = '\t}\n'
    for i, packet in zip(range(len(com['packets'])), com['packets']):
        if packet['type'] != 'signal':
            continue

        typ = packet['name'][1].upper()
        name = packet['name'][0]
        name_lower = name[0].lower() + name[1:]
        parameter = ''
        parameter_list = []
        for element in packet['elements']:
            parameter_list.append(to_camel_case(element[0]))
        parameter = ', '.join(parameter_list)

        has_ret = has_return_value(packet['elements'])

        cbdata = ''
        if has_ret == 'true':
            bbgets, bbret = make_bbgets(packet)
            bbgets = bbgets.replace('\t\t', '\t\t\t\t')
            cbdata = data.format(name_lower,
                                 bbgets,
                                 bbret)

        cbs += cb.format(typ, cbdata, name, name_lower, parameter)
    return cbs + cbs_end

def make_add_listener():
    listeners = """
\tpublic void addListener(Object o) {{
\t\t{0}
\t}}
}}"""
    listener = """if(o instanceof {0}Listener) {{
\t\t\tlistenerObjects[TYPE_{1}] = o;
\t\t}}"""

    l = []
    for i, packet in zip(range(len(com['packets'])), com['packets']):
        if packet['type'] != 'signal':
            continue

        name = packet['name'][0]
        name_upper = packet['name'][1].upper()
        l.append(listener.format(name, name_upper))
    return listeners.format(' else '.join(l))

def make_type_definitions():
    types = ''
    type = '\tprivate final static byte TYPE_{0} = (byte){1};\n'
    for i, packet in zip(range(len(com['packets'])), com['packets']):
        types += type.format(packet['name'][1].upper(), i+1)
    return types


def make_parameter_list(packet):
    param = []
    for element in packet['elements']:
        if element[3] == 'out' and packet['type'] == 'method':
            continue
        java_type = get_java_type(element[1])
        name = to_camel_case(element[0])
        arr = ''
        if element[2] > 1:
            arr = '[]'
       
        param.append('{0}{1} {2}'.format(java_type, arr, name))
    return ', '.join(param)

def make_init_method():
    return """
    def __init__(self, uid):
        Device.__init__(self, uid)

"""

def make_callbacks_format():
    cbs = ''
    cb = "        self.callbacks_format[{0}.CALLBACK_{1}] = '{2}'\n"
    for i, packet in zip(range(len(com['packets'])), com['packets']):
        if packet['type'] != 'signal':
            continue
        form = make_format_list(packet, 'out')
        cbs += cb.format(com['name'][0], packet['name'][1].upper(), form)
    return cbs

def make_constructor():
    con = """
\tpublic {0}{1}(String uid) {{
\t\tsuper(uid);
"""
    return con.format(com['type'], com['name'][0])

def get_put_type(typ):
    forms = {
        'int8' : '',
        'uint8' : '',
        'int16' : 'Short',
        'uint16' : 'Short',
        'int32' : 'Int',
        'uint32' : 'Int',
        'int64' : 'Long',
        'uint64' : 'Long',
        'float' : 'Float',
        'bool' : '',
        'string' : '',
        'char' : ''
    }

    if typ in forms:
        return forms[typ]

    return ''

def get_put_java_type(typ):
    forms = {
        'int8' : 'byte',
        'uint8' : 'byte',
        'int16' : 'short',
        'uint16' : 'short',
        'int32' : 'int',
        'uint32' : 'int',
        'int64' : 'long',
        'uint64' : 'long',
        'float' : 'float',
        'bool' : 'byte',
        'string' : 'byte',
        'char' : 'byte'
    }

    if typ in forms:
        return forms[typ]

    return ''


def get_java_type(typ):
    forms = {
        'int8' : 'byte',
        'uint8' : 'short',
        'int16' : 'short',
        'uint16' : 'int',
        'int32' : 'int',
        'uint32' : 'long',
        'int64' : 'long',
        'uint64' : 'long',
        'float' : 'float',
        'bool' : 'boolean',
        'string' : 'String',
        'char' : 'char'
    }

    if typ in forms:
        return forms[typ]

    return ''


def get_type_size(element):
    forms = {
        'int8' : 1,
        'uint8' : 1,
        'int16' : 2,
        'uint16' : 2,
        'int32' : 4,
        'uint32' : 4,
        'int64' : 8,
        'uint64' : 8,
        'float' : 4,
        'bool' : 1,
        'string' : 1,
        'char' : 1
    }

    if element[1] in forms:
        return forms[element[1]]*element[2]

    return 0

def make_format_list(packet, io):
    forms = []
    for element in packet['elements']:
        if element[3] != io:
            continue
        num = ''
        if element[2] > 1:
            num = element[2]
        form = make_format_from_element(element)
        forms.append('{0}{1}'.format(num, form))
    return " ".join(forms)

def make_methods():
    methods = ''
    method = """
\tpublic {0} {1}({2}) {3} {{
\t\tByteBuffer bb = ByteBuffer.allocate({4});
\t\tbb.order(ByteOrder.LITTLE_ENDIAN);
\t\tbb.put((byte)stackID);
\t\tbb.put((byte)TYPE_{5});
\t\tbb.putShort((short){4});
{6}
\t\tipcon.write(this, bb, TYPE_{5}, {7});{8}
\t}}
"""
    method_answer = """

\t\tbyte[] answer = null;
\t\ttry {{
\t\t\tanswer = answerQueue.poll(IPConnection.TIMEOUT_ANSWER, TimeUnit.MILLISECONDS);
\t\t\tif(answer == null) {{
\t\t\t\tthrow new IPConnection.TimeoutException("Did not receive answer for {0} in time");
\t\t\t}}
\t\t}} catch (InterruptedException e) {{
\t\t\te.printStackTrace();
\t\t}}

\t\tbb = ByteBuffer.wrap(answer, 4, answer.length - 4);
\t\tbb.order(ByteOrder.LITTLE_ENDIAN);

{1}
\t\treturn {2};"""

    loop = """\t\tfor(int i = 0; i < {0}; i++) {{
{1}
\t\t}}
"""
    cls = com['name'][0]
    for packet in com['packets']:
        if packet['type'] != 'method':
            continue

        ret = get_return_value(packet)
        name_lower = packet['name'][0][0].lower() + packet['name'][0][1:]
        parameter = make_parameter_list(packet)
        size = str(get_bb_size(packet['elements']))
        name_upper = packet['name'][1].upper()

# TODO: string
        bbputs = ''
        bbput = '\t\tbb.put{0}(({1}){2});'
        for element in packet['elements']:
            if element[3] != 'in':
                continue

            bbput_format = bbput.format(get_put_type(element[1]),
                                        get_put_java_type(element[1]), 
                                        to_camel_case(element[0]))

            if element[2] > 1:
                bbput_format = bbput_format.replace(');', '[i]);')
                bbput_format = loop.format(element[2], '\t' + bbput_format)

            bbputs += bbput_format + '\n'

        has_ret = has_return_value(packet['elements'])

        throw = '' 
        answer = ''
        if has_ret == 'true':
            throw = 'throws IPConnection.TimeoutException'
            bbgets, bbret = make_bbgets(packet, False)
            if get_num_return(packet['elements']) > 1:
                bbgets, bbret = make_bbgets(packet, True)
                obj_name = get_object_name(packet)
                obj = '\t\t{0} obj = new {0}();\n'.format(obj_name)
                bbgets = obj + bbgets
                bbret = 'obj'

            answer = method_answer.format(name_lower,
                                          bbgets,
                                          bbret)
        methods += method.format(ret,
                                 name_lower,
                                 parameter,
                                 throw,
                                 size,
                                 name_upper,
                                 bbputs,
                                 has_ret,
                                 answer)

    return methods

def make_bbgets(packet, with_obj = False):
    bbgets = ''
    bbget = '\t\t{0}{1}{2} = {3}(bb.get{4}()){5};'
    loop = """\t\tfor(int i = 0; i < {0}; i++) {{
{1}
\t\t}}
"""
    for element in packet['elements']:
        if element[3] == 'out':
            typ = ''
            if not with_obj:
                typ = get_java_type(element[1]) + ' '
            
            bbret = to_camel_case(element[0])
            obj = ''
            if with_obj:
                obj = 'obj.'
            cast = ''
            boolean = ''
            if element[1] == 'uint8':
                cast = 'IPConnection.unsignedByte'
            elif element[1] == 'uint16':
                cast = 'IPConnection.unsignedShort'
            elif element[1] == 'uint32':
                cast = 'IPConnection.unsignedInt'
            elif element[1] == 'bool':
                boolean = ' != 0'
            elif element[1] == 'char':
                cast = '(char)'

            bbget_format = bbget.format(typ,
                                        obj,
                                        bbret, 
                                        cast,
                                        get_put_type(element[1]),
                                        boolean)

            if element[2] > 1:
                bbget_format = bbget_format.replace(' =', '[i] =')
                bbget_format = loop.format(element[2], '\t' + bbget_format)

            bbgets += bbget_format + '\n'
    return bbgets, bbret

def get_object_name(packet):
    name = packet['name'][0]
    if name.startswith('Get'):
        name = name[3:]

    return name

def get_num_return(elements): 
    num = 0
    for element in elements:
        if element[3] == 'out':
            num += 1

    return num

def get_return_value(packet):
    num = 0
    ret = 'void'
    for element in packet['elements']:
        if element[3] == 'out':
            ret = get_java_type(element[1])
            num += 1

    if num > 1:
        return get_object_name(packet)

    return ret

def get_bb_size(elements):
    size = 0
    for element in elements:
        if element[3] != 'in':
            continue
        size += get_type_size(element)
    return size + 4

def has_return_value(elements):
    for element in elements:
        if element[3] == 'out':
            return 'true'
    return 'false'

def to_camel_case(name):
    names = name.split('_')
    ret = names[0]
    for n in names[1:]:
        ret += n[0].upper() + n[1:]
    return ret

def make_files(com_new, directory):
    global com
    com = com_new

    file_name = '{0}{1}'.format(com['type'], com['name'][0])
    
    directory += '/bindings'
    if not os.path.exists(directory):
        os.makedirs(directory)

    java = file('{0}/{1}.java'.format(directory, file_name), "w")
    java.write(make_import())
    java.write(make_class())
    java.write(make_type_definitions())
    java.write(make_return_objects())
    java.write(make_listener_definitions())
    java.write(make_constructor())
    java.write(make_callback_listener_definitions())
    java.write(make_methods())
    java.write(make_add_listener())

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
