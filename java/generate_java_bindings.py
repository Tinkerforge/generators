#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java Bindings Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_java_bindings.py: Generator for Java bindings

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
lang = 'en'

def fix_links(text):
    link = '{{@link com.tinkerforge.{0}{1}.{2}}}'
    link_c = '{{@link com.tinkerforge.{0}{1}.{2}Listener}}'

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

    cls = device.get_camel_case_name()
    for packet in device.get_packets():
        name_false = ':func:`{0}`'.format(packet.get_camel_case_name())
        if packet.get_type() == 'callback':
            name = packet.get_camel_case_name()
            name_right = link_c.format(device.get_category(), cls, name)
        else:
            name = packet.get_headless_camel_case_name()
            name_right = link.format(device.get_category(), cls, name)

        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", "parameter")
    text = text.replace(":word:`parameters`", "parameters")
    text = text.replace('Callback ', 'Listener ')
    text = text.replace(' Callback', ' Listener')
    text = text.replace('callback ', 'listener ')
    text = text.replace(' callback', ' listener')
    text = text.replace('.. note::', '\\note')
    text = text.replace('.. warning::', '\\warning')

    return text

def make_import():
    include = """{0}
package com.tinkerforge;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.concurrent.TimeUnit;

"""
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    return include.format(common.gen_text_star.format(date))

def make_class():
    class_str = """
/**
 * {2}
 */
public class {0}{1} extends Device {{
"""

    return class_str.format(device.get_category(), device.get_camel_case_name(), device.get_description())

def make_return_objects():
    objs = ''
    obj = """
\tpublic class {0} {{
{1}

\t\tpublic String toString() {{
\t\t\treturn "[" + {2} "]";
\t\t}}
\t}}
"""
    param = '\t\tpublic {0}{1} {2}{3};'
    for packet in device.get_packets('function'):
        if len(packet.get_elements('out')) < 2:
            continue

        name = get_object_name(packet)

        params = []
        tostr = []
        for element in packet.get_elements():
            typ = get_java_type(element[1])
            ele_name = common.underscore_to_headless_camel_case(element[0])
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
\t/**
\t * {3}
\t */
\tpublic interface {0}Listener {{
\t\tpublic void {1}({2});
\t}}
"""
    for packet in device.get_packets('callback'):
        name = packet.get_camel_case_name()
        name_lower = packet.get_headless_camel_case_name()
        parameter = make_parameter_list(packet)
        doc = '\n\t * '.join(fix_links(packet.get_doc()[1][lang]).strip().split('\n'))
        cbs += cb.format(name, name_lower, parameter, doc)
    return cbs

def make_callback_listener_definitions():
    cbs = ''
    cb = """
\t\tcallbacks[CALLBACK_{0}] = new CallbackListener() {{
\t\t\tpublic void callback(byte[] data) {{{1}
\t\t\t\t(({2}Listener)listenerObjects[CALLBACK_{0}]).{3}({4});
\t\t\t}}
\t\t}};
"""

    data = """
\t\t\t\tByteBuffer bb = ByteBuffer.wrap(data, 4, data.length - 4);
\t\t\t\tbb.order(ByteOrder.LITTLE_ENDIAN);

{1}"""
    cbs_end = '\t}\n'
    for packet in device.get_packets('callback'):
        typ = packet.get_upper_case_name()
        name = packet.get_camel_case_name()
        name_lower = packet.get_headless_camel_case_name()
        parameter = ''
        parameter_list = []
        for element in packet.get_elements():
            parameter_list.append(common.underscore_to_headless_camel_case(element[0]))
        parameter = ', '.join(parameter_list)
        cbdata = ''
        if len(packet.get_elements('out')) > 0:
            bbgets, bbret = make_bbgets(packet)
            bbgets = bbgets.replace('\t\t', '\t\t\t\t')
            cbdata = data.format(name_lower,
                                 bbgets,
                                 bbret)

        cbs += cb.format(typ, cbdata, name, name_lower, parameter)
    return cbs + cbs_end

def make_add_listener():
    if device.get_callback_count() == 0:
        return '}'

    listeners = """
\t/**
\t * Registers a listener object.
\t */
\tpublic void addListener(Object o) {{
\t\t{0}
\t}}
}}"""
    listener = """if(o instanceof {0}Listener) {{
\t\t\tlistenerObjects[CALLBACK_{1}] = o;
\t\t}}"""

    l = []
    for packet in device.get_packets('callback'):
        name = packet.get_camel_case_name()
        name_upper = packet.get_upper_case_name()
        l.append(listener.format(name, name_upper))
    return listeners.format(' else '.join(l))

def make_function_id_definitions():
    function_ids = ''
    function_id = '\tprivate final static byte {2}_{0} = (byte){1};\n'
    for packet in device.get_packets():
        function_ids += function_id.format(packet.get_upper_case_name(),
                                           packet.get_function_id(),
                                           packet.get_type().upper())
    return function_ids

def make_parameter_list(packet):
    param = []
    for element in packet.get_elements():
        if element[3] == 'out' and packet.get_type() == 'function':
            continue
        java_type = get_java_type(element[1])
        name = common.underscore_to_headless_camel_case(element[0])
        arr = ''
        if element[2] > 1 and element[1] != 'string':
            arr = '[]'
       
        param.append('{0}{1} {2}'.format(java_type, arr, name))
    return ', '.join(param)

def make_constructor():
    con = """
\t/**
\t * Creates an object with the unique device ID \c uid. This object can
\t * then be added to the IP connection.
\t */
\tpublic {0}{1}(String uid) {{
\t\tsuper(uid);

\t\texpectedName = "{5} {6}";

\t\tbindingVersion[0] = {2};
\t\tbindingVersion[1] = {3};
\t\tbindingVersion[2] = {4};
"""

    v = device.get_version()
    return con.format(device.get_category(),
                      device.get_camel_case_name(),
                      v[0],
                      v[1],
                      v[2],
                      device.get_display_name(),
                      device.get_category())

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

def make_format_list(packet, io):
    forms = []
    for element in packet.get_elements(io):
        num = ''
        if element[2] > 1:
            num = element[2]
        form = make_format_from_element(element)
        forms.append('{0}{1}'.format(num, form))
    return " ".join(forms)

def make_methods():
    methods = ''
    method = """
\t/**
\t * {9}
\t */
\tpublic {0} {1}({2}) {3} {{
\t\tByteBuffer bb = IPConnection.createRequestBuffer((byte)stackID, FUNCTION_{5}, (short){4});
{6}
\t\tipcon.write(this, bb, FUNCTION_{5}, {7});{8}
\t}}
"""
    method_response = """

\t\tbyte[] response = null;
\t\ttry {{
\t\t\tresponse = responseQueue.poll(IPConnection.RESPONSE_TIMEOUT, TimeUnit.MILLISECONDS);
\t\t\tif(response == null) {{
\t\t\t\tthrow new IPConnection.TimeoutException("Did not receive response for {0} in time");
\t\t\t}}
\t\t}} catch (InterruptedException e) {{
\t\t\te.printStackTrace();
\t\t}}

\t\tbb = ByteBuffer.wrap(response, 4, response.length - 4);
\t\tbb.order(ByteOrder.LITTLE_ENDIAN);

{1}
\t\tsemaphoreWrite.release();
\t\treturn {2};"""

    loop = """\t\tfor(int i = 0; i < {0}; i++) {{
{1}
\t\t}}
"""
    string_loop = """\t\ttry {{
\t\t{0}
\t\t\t}} catch(Exception e) {{
\t\t\t\tbb.put((byte)0);
\t\t\t}}"""

    cls = device.get_camel_case_name()
    for packet in device.get_packets('function'):
        ret = get_return_value(packet)
        name_lower = packet.get_headless_camel_case_name()
        parameter = make_parameter_list(packet)
        size = str(packet.get_request_length())
        name_upper = packet.get_upper_case_name()
        doc = '\n\t * '.join(fix_links(packet.get_doc()[1][lang]).strip().split('\n'))
        bbputs = ''
        bbput = '\t\tbb.put{0}(({1}){2});'
        for element in packet.get_elements('in'):
            name = common.underscore_to_headless_camel_case(element[0])
            if element[1] == 'bool':
                name = '({0} ? 1 : 0)'.format(name)

            bbput_format = bbput.format(get_put_type(element[1]),
                                        get_put_java_type(element[1]), 
                                        name)

            if element[2] > 1:
                if element[1] == 'string':
                    bbput_format = bbput_format.replace(');', '.charAt(i));')
                    bbput_format = string_loop.format(bbput_format)
                else:
                    bbput_format = bbput_format.replace(');', '[i]);')
                bbput_format = loop.format(element[2], '\t' + bbput_format)

            bbputs += bbput_format + '\n'

        throw = '' 
        response = ''
        has_ret = 'false'
        if len(packet.get_elements('out')) > 0:
            has_ret = 'true'
            throw = 'throws IPConnection.TimeoutException'
            bbgets, bbret = make_bbgets(packet, False)
            if len(packet.get_elements('out')) > 1:
                bbgets, bbret = make_bbgets(packet, True)
                obj_name = get_object_name(packet)
                obj = '\t\t{0} obj = new {0}();\n'.format(obj_name)
                bbgets = obj + bbgets
                bbret = 'obj'

            response = method_response.format(name_lower,
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
                                 response,
                                 doc)

    return methods

def make_bbgets(packet, with_obj = False):
    bbgets = ''
    bbget = '\t\t{0}{1}{2} = {3}(bb.get{4}()){5};'
    new_arr ='{0}[] {1} = new {0}[{2}];'
    loop = """\t\t{2}
\t\tfor(int i = 0; i < {0}; i++) {{
{1}
\t\t}}
"""
    for element in packet.get_elements('out'):
        typ = ''
        if not with_obj:
            typ = get_java_type(element[1]) + ' '

        bbret = common.underscore_to_headless_camel_case(element[0])
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

        format_typ = ''
        if not element[2] > 1:
            format_typ = typ

        bbget_format = bbget.format(format_typ,
                                    obj,
                                    bbret,
                                    cast,
                                    get_put_type(element[1]),
                                    boolean)

        if element[2] > 1:
            arr = new_arr.format(typ.replace(' ', ''), bbret, element[2])
            bbget_format = bbget_format.replace(' =', '[i] =')
            bbget_format = loop.format(element[2], '\t' + bbget_format, arr)

        bbgets += bbget_format + '\n'
    return bbgets, bbret

def get_object_name(packet):
    name = packet.get_camel_case_name()
    if name.startswith('Get'):
        name = name[3:]

    return name

def get_return_value(packet):
    num = 0
    ret = 'void'
    for element in packet.get_elements('out'):
        ret = get_java_type(element[1])
        if element[2] > 1:
            ret += '[]'
        num += 1

    if num > 1:
        return get_object_name(packet)

    return ret

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)

    file_name = '{0}{1}'.format(device.get_category(), device.get_camel_case_name())
    
    directory += '/bindings'
    if not os.path.exists(directory):
        os.makedirs(directory)

    java = file('{0}/{1}.java'.format(directory, file_name), "w")
    java.write(make_import())
    java.write(make_class())
    java.write(make_function_id_definitions())
    java.write(make_return_objects())
    java.write(make_listener_definitions())
    java.write(make_constructor())
    java.write(make_callback_listener_definitions())
    java.write(make_methods())
    java.write(make_add_listener())

if __name__ == "__main__":
    common.generate(os.getcwd(), make_files)
