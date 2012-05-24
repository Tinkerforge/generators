#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C# Bindings Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_csharp_bindings.py: Generator for C# bindings

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
import csharp_common
from xml.sax.saxutils import escape

sys.path.append(os.path.split(os.getcwd())[0])
import common

device = None
lang = 'en'

def fix_links(text):
    link = '<see cref="Tinkerforge.{0}{1}.{2}"/>'

    # escape XML special chars
    text = escape(text)

    # handle notes and warnings
    lines = text.split('\n')
    replaced_lines = []
    in_note = False
    in_warning = False
    in_table_head = False
    in_table_body = False

    for line in lines:
        if line.strip() == '.. note::':
            in_note = True
            replaced_lines.append('<note>')
        elif line.strip() == '.. warning::':
            in_warning = True
            replaced_lines.append('<note type="caution">')
        elif len(line.strip()) == 0 and (in_note or in_warning):
            if in_note:
                in_note = False
            if in_warning:
                in_warning = False

            replaced_lines.append('</note>')
            replaced_lines.append('')
        elif line.strip() == '.. csv-table::':
            in_table_head = True
            replaced_lines.append('<code>')
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

            replaced_lines.append('</code>')
            replaced_lines.append('')
        else:
            replaced_lines.append(line)

    text = '\n'.join(replaced_lines)

    cls = device.get_camel_case_name()
    for packet in device.get_packets():
        name_false = ':func:`{0}`'.format(packet['name'][0])
        name = packet['name'][0]
        name_right = link.format(device.get_category(), cls, name)

        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", "parameter")
    text = text.replace(":word:`parameters`", "parameters")

    return text

def make_import():
    include = """{0}
using System;

namespace Tinkerforge
{{"""
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    return include.format(common.gen_text_star.format(date))

def make_class():
    class_str = """
\t/// <summary>
\t///  {2}
\t/// </summary>
\tpublic class {0}{1} : Device 
\t{{
"""
        
    return class_str.format(device.get_category(),
                            device.get_camel_case_name(),
                            device.get_description())

def make_delegates():
    cbs = '\n'
    cb = """
\t\t/// <summary>
\t\t///  {2}
\t\t/// </summary>
\t\tpublic delegate void {0}({1});
"""
    for packet in device.get_packets():
        if packet['type'] != 'callback':
            continue

        name = packet['name'][0]
        parameter = csharp_common.make_parameter_list(packet)
        doc = '\n\t\t///  '.join(fix_links(packet['doc'][1][lang]).strip().split('\n'))
        cbs += cb.format(name, parameter, doc)
    return cbs

def make_function_id_definitions():
    function_ids = ''
    function_id = '\t\tprivate static byte {2}_{0} = {1};\n'
    for i, packet in zip(range(len(device.get_packets())), device.get_packets()):
        if packet['type'] == 'callback':
            function_ids += function_id.format(packet['name'][1].upper(), i+1, 'CALLBACK')
        else:
            function_ids += function_id.format(packet['name'][1].upper(), i+1, 'FUNCTION')
    return function_ids

def make_constructor():
    cbs = []
    cb = '\t\t\tmessageCallbacks[CALLBACK_{0}] = new MessageCallback(Callback{1});'
    con = """
\t\t/// <summary>
\t\t///  Creates an object with the unique device ID <c>uid</c>. This object can
\t\t///  then be added to the IP connection.
\t\t/// </summary>
\t\tpublic {0}{1}(string uid) : base(uid) 
\t\t{{
\t\t\tthis.expectedName = "{6} {7}";
\t\t\tthis.bindingVersion[0] = {3};
\t\t\tthis.bindingVersion[1] = {4};
\t\t\tthis.bindingVersion[2] = {5};
{2}
\t\t}}
"""

    for packet in device.get_packets():
        if packet['type'] != 'callback':
            continue

        name_upper = packet['name'][1].upper()
        name_pascal = packet['name'][0]
        cbs.append(cb.format(name_upper, name_pascal))

    v = device.get_version()
    return con.format(device.get_category(),
                      device.get_camel_case_name(),
                      '\n'.join(cbs),
                      v[0],
                      v[1],
                      v[2],
                      device.get_display_name(),
                      device.get_category())

def get_from_type(element):
    forms = {
        'int8' : 'SByteFrom',
        'uint8' : 'ByteFrom',
        'int16' : 'ShortFrom',
        'uint16' : 'UShortFrom',
        'int32' : 'IntFrom',
        'uint32' : 'UIntFrom',
        'int64' : 'LongFrom',
        'uint64' : 'ULongFrom',
        'float' : 'FloatFrom',
        'bool' : 'BoolFrom',
        'string' : 'StringFrom',
        'char' : 'CharFrom'
    }

    if element[1] in forms:
        from_type = forms[element[1]]
        if from_type != 'StringFrom' and element[2] > 1:
            from_type = from_type.replace('From', 'ArrayFrom')

        return from_type

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

def make_register_callback():
    if device.get_callback_count() == 0:
        return '\t}\n}\n'

    typeofs = ''
    typeof = """\t\t\t{0}if(d.GetType() == typeof({1}))
\t\t\t{{
\t\t\t\tcallbacks[CALLBACK_{2}] = d;
\t\t\t}}
"""

    cb = """
\t\t/// <summary>
\t\t///  Registers a callback function.
\t\t/// </summary>
\t\tpublic void RegisterCallback(System.Delegate d)
\t\t{{
{0}\t\t}}
\t}}
}}
"""

    i = 0
    for packet in device.get_packets():
        if packet['type'] != 'callback':
            continue

        els = ''
        if i > 0:
            els = 'else '

        name = packet['name'][0]
        name_upper = packet['name'][1].upper()

        typeofs += typeof.format(els, name, name_upper)
        
        i += 1

    return cb.format(typeofs)

def make_callbacks():
    cbs = ''
    cb = """
\t\tinternal int Callback{0}(byte[] data_)
\t\t{{
{1}\t\t\t(({0})callbacks[CALLBACK_{2}])({3});
\t\t\treturn {4};
\t\t}}
"""
    cls = device.get_camel_case_name()
    for packet in device.get_packets():
        if packet['type'] != 'callback':
            continue

        name = packet['name'][0]
        name_upper = packet['name'][1].upper()
        eles = []
        for element in packet['elements']:
            if element[3] == 'out':
                eles.append(csharp_common.to_camel_case(element[0]))
        params = ", ".join(eles)
        size = str(get_data_size(packet['elements']))

        convs = ''
        conv = '\t\t\t{0} {1} = LEConverter.{2}({3}, data_{4});\n'

        pos = 4
        for element in packet['elements']:
            if element[3] != 'out':
                continue

            csharp_type = csharp_common.get_csharp_type(element)
            cname = csharp_common.to_camel_case(element[0])
            from_type = get_from_type(element)
            length = ''
            if element[2] > 1:
                length = ', ' + str(element[2])
            convs += conv.format(csharp_type, 
                                 cname, 
                                 from_type,
                                 pos,
                                 length)

            pos += get_type_size(element)

        if convs != '':
            convs += '\n'
        
        cbs += cb.format(name, convs, name_upper, params, pos)

    return cbs

def make_methods():
    methods = ''
    method = """
\t\t/// <summary>
\t\t///  {5}
\t\t/// </summary>
\t\t{0}
\t\t{{
\t\t\tbyte[] data_ = new byte[{1}];
\t\t\tLEConverter.To(stackID, 0, data_);
\t\t\tLEConverter.To(FUNCTION_{2}, 1, data_);
\t\t\tLEConverter.To((ushort){1}, 2, data_);
{3}
{4}
\t\t}}
"""
    method_oneway = "\t\t\tsendOneWayMessage(data_);"
    method_answer = """\t\t\tbyte[] answer;
\t\t\tsendReturningMessage(data_, FUNCTION_{0}, out answer);
{1}"""

    cls = device.get_camel_case_name()
    for packet in device.get_packets():
        if packet['type'] != 'function':
            continue

        ret_count = csharp_common.count_return_values(packet['elements'])
        size = str(get_data_size(packet['elements']))
        name_upper = packet['name'][1].upper()
        doc = '\n\t\t///  '.join(fix_links(packet['doc'][1][lang]).strip().split('\n'))

        write_convs = ''
        write_conv = '\t\t\tLEConverter.To({0}, {1}, data_);\n'
        write_conv_length = '\t\t\tLEConverter.To({0}, {1}, {2}, data_);\n'

        pos = 4
        for element in packet['elements']:
            if element[3] != 'in':
                continue
            wname = csharp_common.to_camel_case(element[0])
            if element[2] > 1:
                write_convs += write_conv_length.format(wname, pos, element[2])
            else:
                write_convs += write_conv.format(wname, pos)
            pos += get_type_size(element)
            
        method_tail = ''
        if ret_count > 0:
            read_convs = ''
            read_conv = '\n\t\t\t{0} = LEConverter.{1}({2}, answer{3});'

            pos = 4
            for element in packet['elements']:
                if element[3] != 'out':
                    continue

                aname = csharp_common.to_camel_case(element[0])
                from_type = get_from_type(element)
                length = ''
                if element[2] > 1:
                    length = ', ' + str(element[2])

                if ret_count == 1:
                    read_convs = '\n\t\t\treturn LEConverter.{0}({1}, answer{2});'.format(from_type, pos, length)
                else:
                    read_convs += read_conv.format(aname, from_type, pos, length)
                pos += get_type_size(element)

            method_tail = method_answer.format(name_upper, read_convs)
        else:
            method_tail = method_oneway

        signature = csharp_common.make_method_signature(packet)
        methods += method.format(signature,
                                 size,
                                 name_upper,
                                 write_convs,
                                 method_tail,
                                 doc)

    return methods

def make_obsolete_methods():
    methods = ''
    method = """
\t\t/// <summary>
\t\t///  Obsolete. Use overloaded version instead that returns the result.
\t\t/// </summary>
\t\t[Obsolete()]
\t\tpublic void {0}({1})
\t\t{{
\t\t\t{2} = {0}({3});
\t\t}}
"""

    cls = device.get_camel_case_name()
    for packet in device.get_packets():
        if packet['type'] != 'function':
            continue

        ret_count = csharp_common.count_return_values(packet['elements'])
        if ret_count != 1:
            continue

        name = packet['name'][0]
        sigParams = csharp_common.make_parameter_list(packet, True)
        outParam = csharp_common.to_camel_case(filter(lambda e: e[3] == 'out', packet['elements'])[0][0])
        callParams = ", ".join(map(lambda e: csharp_common.to_camel_case(e[0]), filter(lambda e: e[3] == 'in', packet['elements'])))
        doc = '\n\t\t///  '.join(fix_links(packet['doc'][1][lang]).strip().split('\n'))

        methods += method.format(name,
                                 sigParams,
                                 outParam,
                                 callParams,
                                 doc)

    return methods

def get_data_size(elements):
    size = 0
    for element in elements:
        if element[3] != 'in':
            continue
        size += get_type_size(element)
    return size + 4

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)

    file_name = '{0}{1}'.format(device.get_category(), device.get_camel_case_name())
    
    directory += '/bindings'
    if not os.path.exists(directory):
        os.makedirs(directory)

    csharp = file('{0}/{1}.cs'.format(directory, file_name), "w")
    csharp.write(make_import())
    csharp.write(make_class())
    csharp.write(make_function_id_definitions())
    csharp.write(make_delegates())
    csharp.write(make_constructor())
    csharp.write(make_methods())
    csharp.write(make_obsolete_methods())
    csharp.write(make_callbacks())
    csharp.write(make_register_callback())

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
