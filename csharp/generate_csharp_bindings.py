#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C# Bindings Generator
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
namespace Tinkerforge
{{"""
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    return include.format(gen_text.format(date))

def make_class():
    class_str = """
\tpublic class {0}{1} : Device 
\t{{
"""
        
    return class_str.format(com['type'], com['name'][0])

def make_delegates():
    cbs = '\n'
    cb = """\t\tpublic delegate void {0}({1});
"""
    for packet in com['packets']:
        if packet['type'] != 'signal':
            continue

        name = packet['name'][0]
        parameter = make_parameter_list(packet)
        cbs += cb.format(name, parameter)
    return cbs

def make_type_definitions():
    types = ''
    type = '\t\tprivate static byte TYPE_{0} = {1};\n'
    for i, packet in zip(range(len(com['packets'])), com['packets']):
        types += type.format(packet['name'][1].upper(), i+1)
    return types

def make_parameter_list(packet, useOutParams = True):
    param = []
    for element in packet['elements']:
        if (not useOutParams) and element[3] == 'out':
            continue
        
        out = ''
        if element[3] == 'out' and packet['type'] == 'method':
            out = 'out '

        csharp_type = get_csharp_type(element[1])
        name = to_camel_case(element[0])
        arr = ''
        if element[2] > 1 and element[1] != 'string':
            arr = '[]'
       
        param.append('{0}{1}{2} {3}'.format(out, csharp_type, arr, name))
    return ', '.join(param)

def make_constructor():
    cbs = []
    cb = '\t\t\tmessageCallbacks[TYPE_{0}] = new MessageCallback(Callback{1});'
    con = """
\t\tpublic {0}{1}(string uid) : base(uid) 
\t\t{{
\t\t\tthis.bindingVersion[0] = {3};
\t\t\tthis.bindingVersion[1] = {4};
\t\t\tthis.bindingVersion[2] = {5};
{2}
\t\t}}
"""

    for packet in com['packets']:
        if packet['type'] != 'signal':
            continue

        name_upper = packet['name'][1].upper()
        name_pascal = packet['name'][0]
        cbs.append(cb.format(name_upper, name_pascal))

    v = com['version']
    return con.format(com['type'], com['name'][0], '\n'.join(cbs), v[0], v[1], v[2])

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


def get_csharp_type(typ):
    forms = {
        'int8' : 'sbyte',
        'uint8' : 'byte',
        'int16' : 'short',
        'uint16' : 'ushort',
        'int32' : 'int',
        'uint32' : 'uint',
        'int64' : 'long',
        'uint64' : 'ulong',
        'float' : 'float',
        'bool' : 'bool',
        'string' : 'string',
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

def make_register_callback():
    typeofs = ''
    typeof = """\t\t\t{0}if(d.GetType() == typeof({1}))
\t\t\t{{
\t\t\t\tcallbacks[TYPE_{2}] = d;
\t\t\t}}
"""

    cb = """
\t\tpublic void RegisterCallback(System.Delegate d)
\t\t{{
{0}\t\t}}
\t}}
}}
"""

    i = 0
    for packet in com['packets']:
        if packet['type'] != 'signal':
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
{1}\t\t\t(({0})callbacks[TYPE_{2}])({3});
\t\t\treturn {4};
\t\t}}
"""
    cls = com['name'][0]
    for packet in com['packets']:
        if packet['type'] != 'signal':
            continue

        name = packet['name'][0]
        name_upper = packet['name'][1].upper()
        eles = []
        for element in packet['elements']:
            if element[3] == 'out':
                eles.append(to_camel_case(element[0]))
        params = ", ".join(eles)
        size = str(get_data_size(packet['elements']))

        convs = ''
        conv = '\t\t\t{0} {1} = LEConverter.{2}({3}, data_{4});\n'

        pos = 4
        for element in packet['elements']:
            if element[3] != 'out':
                continue

            csharp_type = get_csharp_type(element[1])
            cname = to_camel_case(element[0])
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

def make_version_method():
    return """
\t\tpublic void GetVersion(out string name, out byte[] firmwareVersion, out byte[] bindingVersion)
\t\t{{
\t\t\tname = this.name;
\t\t\tfirmwareVersion = this.firmwareVersion;
\t\t\tbindingVersion = this.bindingVersion;
\t\t}}
"""

def make_methods():
    methods = ''
    sig_format = "public {0} {1}({2})"
    method = """
\t\t{0}
\t\t{{
\t\t\tbyte[] data_ = new byte[{1}];
\t\t\tLEConverter.To(stackID, 0, data_);
\t\t\tLEConverter.To(TYPE_{2}, 1, data_);
\t\t\tLEConverter.To((ushort){1}, 2, data_);
{3}
{4}\t\t}}
"""
    method_oneway = """
\t\t\tsendOneWayMessage(data_);
"""
    method_answer = """
\t\t\tbyte[] answer;
\t\t\tsendReturningMessage(data_, TYPE_{0}, out answer);

{1}
"""

    cls = com['name'][0]
    for packet in com['packets']:
        if packet['type'] != 'method':
            continue

        ret_count = count_return_values(packet['elements'])
        useOutParams = ret_count > 1
        name = packet['name'][0]
        params = make_parameter_list(packet, useOutParams)
        size = str(get_data_size(packet['elements']))
        name_upper = packet['name'][1].upper()

        write_convs = ''
        write_conv = '\t\t\tLEConverter.To({0}, {1}, data_);\n'

        pos = 4
        for element in packet['elements']:
            if element[3] != 'in':
                continue
            wname = to_camel_case(element[0])
            write_convs += write_conv.format(wname, pos)
            pos += get_type_size(element)
            
        signature = ''
        return_type = 'void'
        method_tail = ''
        if ret_count > 0:
            read_convs = ''
            read_conv = '\t\t\t{0} = LEConverter.{1}({2}, answer{3});\n'

            pos = 4
            for element in packet['elements']:
                if element[3] != 'out':
                    continue

                aname = to_camel_case(element[0])
                from_type = get_from_type(element)
                length = ''
                if element[2] > 1:
                    length = ', ' + str(element[2])

                if ret_count == 1:
                    read_convs = '\t\t\treturn LEConverter.{0}({1}, answer{2});\n'.format(from_type, pos, length)
                    return_type = get_csharp_type(element[1])
                    if element[2] > 1 and element[1] != 'string':
                        return_type += '[]'
                else:
                    read_convs += read_conv.format(aname, from_type, pos, length)
                pos += get_type_size(element)

            method_tail = method_answer.format(name_upper, read_convs)
        else:
            method_tail = method_oneway

        signature = sig_format.format(return_type, name, params)
        methods += method.format(signature,
                                 size,
                                 name_upper,
                                 write_convs,
                                 method_tail)

    return methods

def get_data_size(elements):
    size = 0
    for element in elements:
        if element[3] != 'in':
            continue
        size += get_type_size(element)
    return size + 4

def count_return_values(elements):
    count = 0
    for element in elements:
        if element[3] == 'out':
            count += 1
    return count

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

    csharp = file('{0}/{1}.cs'.format(directory, file_name), "w")
    csharp.write(make_import())
    csharp.write(make_class())
    csharp.write(make_type_definitions())
    csharp.write(make_delegates())
    csharp.write(make_constructor())
    csharp.write(make_methods())
    csharp.write(make_version_method())
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
