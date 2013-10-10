#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Java Bindings Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011-2013 Olaf Lüke <olaf@tinkerforge.com>

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
import java_common

device = None

def format_doc(packet):
    text = common.select_lang(packet.get_doc()[1])
    link = '{{@link {0}#{1}({2})}}'
    link_c = '{{@link {0}.{1}Listener}}'

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

    cls = device.get_java_class_name()
    for other_packet in device.get_packets():
        name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
        if other_packet.get_type() == 'callback':
            name = other_packet.get_camel_case_name()
            name_right = link_c.format(cls, name)
        else:
            name = other_packet.get_headless_camel_case_name()
            name_right = link.format(cls, name, java_common.make_parameter_list(other_packet, True))

        text = text.replace(name_false, name_right)

    text = text.replace('Callback ', 'Listener ')
    text = text.replace(' Callback', ' Listener')
    text = text.replace('callback ', 'listener ')
    text = text.replace(' callback', ' listener')
    text = text.replace('.. note::', '\\note')
    text = text.replace('.. warning::', '\\warning')

    text = common.handle_rst_word(text)
    text = common.handle_rst_if(text, device)
    text += common.format_since_firmware(device, packet)

    return '\n\t * '.join(text.strip().split('\n'))

def make_import(version):
    include = """{0}
package com.tinkerforge;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.Arrays;
import java.util.List;
"""
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    return include.format(common.gen_text_star.format(date, *version))

def make_class():
    class_str = """
/**
 * {1}
 */
public class {0} extends Device {{
\tpublic final static int DEVICE_IDENTIFIER = {2};

"""

    return class_str.format(device.get_java_class_name(),
                            device.get_description(),
                            device.get_device_identifier())

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
        if packet.has_prototype_in_device():
            continue
        if len(packet.get_elements('out')) < 2:
            continue

        name = java_common.get_object_name(packet)

        params = []
        tostr = []
        for element in packet.get_elements():
            typ = java_common.get_java_type(element.get_type())
            ele_name = element.get_headless_camel_case_name()
            if element.get_cardinality() > 1 and element.get_type() != 'string':
                arr = '[]'
                new = ' = new {0}[{1}]'.format(typ, element.get_cardinality())
                to = '"{0} = " + Arrays.toString({0}) +'.format(ele_name)
            else:
                arr = ''
                new = ''
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
        parameter = java_common.make_parameter_list(packet)
        doc = format_doc(packet)
        cbs += cb.format(name, name_lower, parameter, doc)
    return cbs


def make_response_expected():
    res = ''
    re = "\t\tresponseExpected[IPConnection.unsignedByte({0})] = {1}\n"

    for packet in device.get_packets('function'):
        name_upper = 'FUNCTION_' + packet.get_upper_case_name()
        setto = 'RESPONSE_EXPECTED_FLAG_FALSE;'
        if len(packet.get_elements('out')) > 0:
            setto = 'RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE;'
        elif packet.get_doc()[0] == 'ccf':
            setto = 'RESPONSE_EXPECTED_FLAG_TRUE;'

        res += re.format(name_upper, setto)

    for packet in device.get_packets('callback'):
        name_upper = 'CALLBACK_' + packet.get_upper_case_name()
        setto = 'RESPONSE_EXPECTED_FLAG_ALWAYS_FALSE;'
        res += re.format(name_upper, setto)

    return res

def make_callback_listener_definitions():
    cbs = ''
    cb = """
\t\tcallbacks[CALLBACK_{0}] = new CallbackListener() {{
\t\t\tpublic void callback(byte[] data) {{{1}
\t\t\t\tfor({2}Listener listener: listener{2}) {{
\t\t\t\t\tlistener.{3}({4});
\t\t\t\t}}
\t\t\t}}
\t\t}};
"""

    data = """
\t\t\t\tByteBuffer bb = ByteBuffer.wrap(data, 8, data.length - 8);
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
            parameter_list.append(element.get_headless_camel_case_name())
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

    listeners = ''
    listener = """
\t/**
\t * Adds a {0} listener.
\t */
\tpublic void add{0}Listener({0}Listener listener) {{
\t\tlistener{0}.add(listener);
\t}}

\t/**
\t * Removes a {0} listener.
\t */
\tpublic void remove{0}Listener({0}Listener listener) {{
\t\tlistener{0}.remove(listener);
\t}}
"""

    l = []
    for packet in device.get_packets('callback'):
        name = packet.get_camel_case_name()
        listeners += listener.format(name)
    return listeners + '}'

def make_function_id_definitions():
    function_ids = ''
    function_id = '\tpublic final static byte {2}_{0} = (byte){1};\n'
    for packet in device.get_packets():
        function_ids += function_id.format(packet.get_upper_case_name(),
                                           packet.get_function_id(),
                                           packet.get_type().upper())
    return function_ids

def make_constants():
    str_constants = '\n'
    str_constant = '\tpublic final static {0} {1}_{2} = {3}{4};\n'
    constants = device.get_constants()
    for constant in constants:
        for definition in constant.definitions:
            if constant.type == 'char':
                cast = ''
                value = "'{0}'".format(definition.value)
            else:
                cast = '({0})'.format(java_common.get_java_type(constant.type))
                value = str(definition.value)

            str_constants += str_constant.format(java_common.get_java_type(constant.type),
                                                 constant.name_uppercase,
                                                 definition.name_uppercase,
                                                 cast,
                                                 value)
    return str_constants

def make_listener_lists():
    llists = '\n'
    llist = '\tprivate List<{0}Listener> listener{0} = new CopyOnWriteArrayList<{0}Listener>();\n'
    for packet in device.get_packets('callback'):
        name = packet.get_camel_case_name()
        llists += llist.format(name)

    return llists

def make_constructor():
    con = """
\t/**
\t * Creates an object with the unique device ID \c uid. and adds it to
\t * the IP Connection \c ipcon.
\t */
\tpublic {0}(String uid, IPConnection ipcon) {{
\t\tsuper(uid, ipcon);

\t\tapiVersion[0] = {1};
\t\tapiVersion[1] = {2};
\t\tapiVersion[2] = {3};
"""

    return con.format(device.get_java_class_name(),
                      *device.get_api_version())

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

def make_methods():
    methods = ''
    method = """
\t/**
\t * {8}
\t */
\tpublic {0} {1}({2}) {3} {{
\t\tByteBuffer bb = ipcon.createRequestPacket((byte){4}, FUNCTION_{5}, this);
{6}
{7}
\t}}
"""
    method_response = """\t\tbyte[] response = sendRequest(bb.array());

\t\tbb = ByteBuffer.wrap(response, 8, response.length - 8);
\t\tbb.order(ByteOrder.LITTLE_ENDIAN);

{1}
\t\treturn {2};"""

    method_noresponse = """\t\tsendRequest(bb.array());"""

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
        options = 0
        ret = java_common.get_return_type(packet)
        name_lower = packet.get_headless_camel_case_name()
        parameter = java_common.make_parameter_list(packet)
        size = str(packet.get_request_size())
        name_upper = packet.get_upper_case_name()
        doc = format_doc(packet)
        bbputs = ''
        bbput = '\t\tbb.put{0}({1}{2});'
        for element in packet.get_elements('in'):
            name = element.get_headless_camel_case_name()
            if element.get_type() == 'bool':
                name = '({0} ? 1 : 0)'.format(name)

            cast = ''
            put_java_type = get_put_java_type(element.get_type())
            if put_java_type != java_common.get_java_type(element.get_type()):
                cast = '({0})'.format(put_java_type)

            bbput_format = bbput.format(get_put_type(element.get_type()),
                                        cast,
                                        name)

            if element.get_cardinality() > 1:
                if element.get_type() == 'string':
                    bbput_format = bbput_format.replace(');', '.charAt(i));')
                    bbput_format = string_loop.format(bbput_format)
                else:
                    bbput_format = bbput_format.replace(');', '[i]);')
                bbput_format = loop.format(element.get_cardinality(), '\t' + bbput_format)

            bbputs += bbput_format + '\n'

        throw = 'throws TimeoutException, NotConnectedException'
        if len(packet.get_elements('out')) == 0:
            bbgets = ''
            bbret = ''
        elif len(packet.get_elements('out')) > 1:
            bbgets, bbret = make_bbgets(packet, True)
            obj_name = java_common.get_object_name(packet)
            obj = '\t\t{0} obj = new {0}();\n'.format(obj_name)
            bbgets = obj + bbgets
            bbret = 'obj'
        else:
            bbgets, bbret = make_bbgets(packet, False)

        if len(packet.get_elements('out')) == 0:
            response = method_noresponse.format(name_upper)
        else:
            response = method_response.format(name_upper,
                                              bbgets,
                                              bbret)

        methods += method.format(ret,
                                 name_lower,
                                 parameter,
                                 throw,
                                 size,
                                 name_upper,
                                 bbputs,
                                 response,
                                 doc)

    return methods

def make_bbgets(packet, with_obj = False):
    bbgets = ''
    bbget_other = '\t\t{0}{1}{2} = {3}(bb.get{4}(){5}){6};'
    bbget_string = '\t\t{0}{1}{2} = {3}(bb{4}{5}){6};'
    new_arr ='{0}[] {1} = new {0}[{2}];'
    loop = """\t\t{2}for(int i = 0; i < {0}; i++) {{
{1}
\t\t}}
"""
    for element in packet.get_elements('out'):
        typ = ''
        if not with_obj:
            typ = java_common.get_java_type(element.get_type()) + ' '

        bbret = element.get_headless_camel_case_name()
        obj = ''
        if with_obj:
            obj = 'obj.'
        cast = ''
        cast_extra = ''
        boolean = ''
        if element.get_type() == 'uint8':
            cast = 'IPConnection.unsignedByte'
        elif element.get_type() == 'uint16':
            cast = 'IPConnection.unsignedShort'
        elif element.get_type() == 'uint32':
            cast = 'IPConnection.unsignedInt'
        elif element.get_type() == 'bool':
            boolean = ' != 0'
        elif element.get_type() == 'char':
            cast = '(char)'
        elif element.get_type() == 'string':
            cast = 'IPConnection.string'
            cast_extra = ', {0}'.format(element.get_cardinality())

        format_typ = ''
        if not element.get_cardinality() > 1 or (element.get_type() == 'string' and not with_obj):
            format_typ = typ

        if element.get_type() == 'string':
            bbget = bbget_string
        else:
            bbget = bbget_other

        bbget_format = bbget.format(format_typ,
                                    obj,
                                    bbret,
                                    cast,
                                    get_put_type(element.get_type()),
                                    cast_extra,
                                    boolean)

        if element.get_cardinality() > 1 and element.get_type() != 'string':
            if with_obj:
                bbget_format = bbget_format.replace(' =', '[i] =')
                bbget_format = loop.format(element.get_cardinality(), '\t' + bbget_format, '')
            else:
                arr = new_arr.format(typ.replace(' ', ''), bbret, element.get_cardinality())
                bbget_format = bbget_format.replace(' =', '[i] =')
                bbget_format = loop.format(element.get_cardinality(), '\t' + bbget_format, arr + '\n\t\t')

        bbgets += bbget_format + '\n'
    return bbgets, bbret

class JavaBindingsGenerator(common.BindingsGenerator):
    def __init__(self, *args, **kwargs):
        common.BindingsGenerator.__init__(self, *args, **kwargs)

        self.released_files_name_prefix = 'java'

    def get_device_class(self):
        return java_common.JavaDevice

    def generate(self, device_):
        global device
        device = device_

        version = common.get_changelog_version(self.get_bindings_root_directory())
        file_name = '{0}.java'.format(device.get_java_class_name())

        java = open(os.path.join(self.get_bindings_root_directory(), 'bindings', file_name), 'wb')
        java.write(make_import(version))
        java.write(make_class())
        java.write(make_function_id_definitions())
        java.write(make_constants())
        java.write(make_listener_lists())
        java.write(make_return_objects())
        java.write(make_listener_definitions())
        java.write(make_constructor())
        java.write(make_response_expected())
        java.write(make_callback_listener_definitions())
        java.write(make_methods())
        java.write(make_add_listener())
        java.close()

        if device.is_released():
            self.released_files.append(file_name)

def generate(path):
    common.generate(path, 'en', JavaBindingsGenerator, False)

if __name__ == "__main__":
    generate(os.getcwd())
