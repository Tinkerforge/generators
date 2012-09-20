#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PHP Bindings Generator
Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_php_bindings.py: Generator for PHP bindings

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
import php_common

sys.path.append(os.path.split(os.getcwd())[0])
import common

device = None

def fix_links(text):
    link = '{0}{1}::{2}()'
    link_c = '{0}{1}::CALLBACK_{2}'

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
            replaced_lines.append('<warning>')
        elif len(line.strip()) == 0 and in_note:
            in_note = False
            replaced_lines.append('</note>')
            replaced_lines.append('')
        elif len(line.strip()) == 0 and in_warning:
            in_warning = False
            replaced_lines.append('</warning>')
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
        name_false = ':func:`{0}`'.format(packet.get_camel_case_name())
        if packet.get_type() == 'callback':
            name = packet.get_upper_case_name()
            name_right = link_c.format(device.get_category(), cls, name)
        else:
            name = packet.get_headless_camel_case_name()
            name_right = link.format(device.get_category(), cls, name)

        text = text.replace(name_false, name_right)

    text = text.replace(":word:`parameter`", "parameter")
    text = text.replace(":word:`parameters`", "parameters")
    text = text.replace('.. note::', '\\note')
    text = text.replace('.. warning::', '\\warning')

    return text

def make_parameter_doc(packet):
    param = []
    for element in packet.get_elements():
        if element[3] == 'out' or packet.get_type() != 'function':
            continue

        php_type = php_common.get_php_type(element[1])
        if element[2] > 1 and element[1] != 'string':
            param.append('@param {0}[] ${1}'.format(php_type, element[0]))
        else:
            param.append('@param {0} ${1}'.format(php_type, element[0]))

    param.append('\n@return ' + php_common.get_return_type(packet))
    return '\n'.join(param)

def make_import():
    include = """{0}
namespace Tinkerforge;

require_once(__DIR__ . '/IPConnection.php');
"""
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    return include.format(common.gen_text_star.format(date))

def make_class():
    class_str = """
/**
 * {2}
 */
class {0}{1} extends Device
{{
"""

    return class_str.format(device.get_category(), device.get_camel_case_name(), device.get_description())

def make_callback_wrapper_definitions():
    cbs = ''
    cb = """
        $this->callbackWrappers[self::CALLBACK_{0}] = 'callbackWrapper{1}';"""
    cbs_end = '\n    }\n'
    for packet in device.get_packets('callback'):
        typ = packet.get_upper_case_name()
        name = packet.get_camel_case_name()

        cbs += cb.format(typ, name)
    return cbs + cbs_end

def make_callback_id_definitions():
    cbs = ''
    cb = """
    /**
     * {2}
     */
    const CALLBACK_{0} = {1};
"""
    for packet in device.get_packets('callback'):
        doc = '\n     * '.join(fix_links(common.select_lang(packet.get_doc()[1])).strip().split('\n'))
        cbs += cb.format(packet.get_upper_case_name(), packet.get_function_id(), doc)
    return cbs + '\n'

def make_function_id_definitions():
    function_ids = ''
    function_id = """
    /**
     * @internal
     */
    const FUNCTION_{0} = {1};
"""
    for packet in device.get_packets('function'):
        function_ids += function_id.format(packet.get_upper_case_name(), packet.get_function_id())
    return function_ids

def make_parameter_list(packet):
    param = []
    for element in packet.get_elements():
        if element[3] == 'out' and packet.get_type() == 'function':
            continue
        name = element[0]
        param.append('$' + name)
    return ', '.join(param)

def make_constructor():
    con = """
    /**
     * Creates an object with the unique device ID $uid. This object can
     * then be added to the IP connection.
     *
     * @param string $uid
     */
    public function __construct($uid)
    {{
        parent::__construct($uid);

        $this->expectedName = '{5} {6}';

        $this->bindingVersion = array({2}, {3}, {4});
"""

    v = device.get_version()
    return con.format(device.get_category(),
                      device.get_camel_case_name(),
                      v[0],
                      v[1],
                      v[2],
                      device.get_display_name(),
                      device.get_category())

def get_pack_type(element):
    forms = {
        'int8' : 'c',
        'uint8' : 'C',
        'int16' : 'v',
        'uint16' : 'v',
        'int32' : 'V',
        'uint32' : 'V',
        #'int64' : # NOTE: unsupported
        #'uint64' : # NOTE: unsupported
        'float' : 'f',
        'bool' : 'C',
        'string' : 'c',
        'char' : 'c'
    }

    return forms[element[1]];

get_unpack_type = get_pack_type

def get_unpack_fix(element):
    if element[2] > 1:
        if element[1] == 'int16':
            return ('IPConnection::collectUnpackedInt16Array(', ')')
        elif element[1] == 'int32':
            return ('IPConnection::collectUnpackedInt32Array(', ')')
        elif element[1] == 'uint32':
            return ('IPConnection::collectUnpackedUInt32Array(', ')')
        elif element[1] == 'bool':
            return ('IPConnection::collectUnpackedBoolArray(', ')')
        elif element[1] == 'string':
            return ('IPConnection::implodeUnpackedString(', ')')
        elif element[1] == 'char':
            return ('IPConnection::collectUnpackedCharArray(', ')')
        else:
            return ('IPConnection::collectUnpackedArray(', ')')
    else:
        if element[1] == 'int16':
            return ('IPConnection::fixUnpackedInt16(', ')')
        elif element[1] == 'int32':
            return ('IPConnection::fixUnpackedInt32(', ')')
        elif element[1] == 'uint32':
            return ('IPConnection::fixUnpackedUInt32(', ')')
        elif element[1] == 'bool':
            return ('(bool)', '')
        elif element[1] == 'string':
            return ('chr(', ')')
        elif element[1] == 'char':
            return ('chr(', ')')
        else:
            return ('', '')

def make_methods():
    methods = ''
    method_multi = """
    /**
     * {6}
     */
    public function {0}({1})
    {{
        $result = array();

        $payload = '';
{2}

{3}

{4}

{5}

        return $result;
    }}
"""
    method_single = """
    /**
     * {6}
     */
    public function {0}({1})
    {{
        $payload = '';
{2}

{3}

{4}

{5}
    }}
"""

    for packet in device.get_packets('function'):
        name_lower = packet.get_headless_camel_case_name()
        parameter = make_parameter_list(packet)
        pack = []
        for element in packet.get_elements('in'):
            if element[1] == 'bool':
                if element[2] > 1:
                    pack.append('        for ($i = 0; $i < {0}; $i++) {{'.format(element[2]))
                    pack.append('            $payload .= pack(\'{0}\', intval((bool)${1}[$i]));\n        }}'.format(get_pack_type(element), element[0]))
                else:
                    pack.append('        $payload .= pack(\'{0}\', intval((bool)${1}));'.format(get_pack_type(element), element[0]))
            elif element[1] == 'string':
                if element[2] > 1:
                    pack.append('        for ($i = 0; $i < strlen(${0}) && $i < {1}; $i++) {{'.format(element[0], element[2]))
                    pack.append('            $payload .= pack(\'{0}\', ord(${1}[$i]));\n        }}'.format(get_pack_type(element), element[0]))
                    pack.append('        for ($i = strlen(${0}); $i < {1}; $i++) {{'.format(element[0], element[2]))
                    pack.append('            $payload .= pack(\'{0}\', 0);\n        }}'.format(get_pack_type(element)))
                else:
                    pack.append('        $payload .= pack(\'{0}\', ord(${1}));'.format(get_pack_type(element), element[0]))
            elif element[1] == 'char':
                if element[2] > 1:
                    pack.append('        for ($i = 0; $i < count(${0}) && $i < {1}; $i++) {{'.format(element[0], element[2]))
                    pack.append('            $payload .= pack(\'{0}\', ord(${1}[$i]));\n        }}'.format(get_pack_type(element), element[0]))
                    pack.append('        for ($i = count(${0}); $i < {1}; $i++) {{'.format(element[0], element[2]))
                    pack.append('            $payload .= pack(\'{0}\', 0);\n        }}'.format(get_pack_type(element)))
                else:
                    pack.append('        $payload .= pack(\'{0}\', ord(${1}));'.format(get_pack_type(element), element[0]))
            else:
                if element[2] > 1:
                    pack.append('        for ($i = 0; $i < {0}; $i++) {{'.format(element[2]))
                    pack.append('            $payload .= pack(\'{0}\', ${1}[$i]);\n        }}'.format(get_pack_type(element), element[0]))
                else:
                    pack.append('        $payload .= pack(\'{0}\', ${1});'.format(get_pack_type(element), element[0]))

        response_payload_elements = 0;
        response_payload_size = 0;
        unpack = []
        collect = []

        for element in packet.get_elements('out'):
            response_payload_elements += 1;
            response_payload_size += common.get_element_size(element)

        for element in packet.get_elements('out'):
            unpack.append('{0}{1}{2}'.format(get_unpack_type(element), element[2], element[0]))

            unpack_fix = get_unpack_fix(element)

            if response_payload_elements > 1:
                if element[2] > 1:
                    collect.append('        $result[\'{0}\'] = {2}$payload, \'{0}\', {1}{3};'.format(element[0], element[2], unpack_fix[0], unpack_fix[1]))
                else:
                    collect.append('        $result[\'{0}\'] = {1}$payload[\'{0}\']{2};'.format(element[0], unpack_fix[0], unpack_fix[1]))
            else:
                if element[2] > 1:
                    collect.append('        return {2}$payload, \'{0}\', {1}{3};'.format(element[0], element[2], unpack_fix[0], unpack_fix[1]))
                else:
                    collect.append('        return {1}$payload[\'{0}\']{2};'.format(element[0], unpack_fix[0], unpack_fix[1]))

        if response_payload_size > 0:
            send = '        $data = $this->sendRequestExpectResponse(self::FUNCTION_{0}, $payload, {1});\n'.format(packet.get_upper_case_name(), response_payload_size)
        else:
            send = '        $this->sendRequestNoResponse(self::FUNCTION_{0}, $payload);\n'.format(packet.get_upper_case_name())

        final_unpack = ''

        if response_payload_size > 0:
            final_unpack = '        $payload = unpack(\'{0}\', $data);'.format('/'.join(unpack))

        doc = '\n     * '.join(fix_links(common.select_lang(packet.get_doc()[1])).strip().split('\n') + [''] + make_parameter_doc(packet).split('\n'))

        if response_payload_elements > 1:
            method = method_multi.format(name_lower,
                                         parameter,
                                         '\n'.join(pack),
                                         send,
                                         final_unpack,
                                         '\n'.join(collect),
                                         doc)
        else:
            method = method_single.format(name_lower,
                                          parameter,
                                          '\n'.join(pack),
                                          send,
                                          final_unpack,
                                          '\n'.join(collect),
                                          doc)

        prev = method
        method = method.replace('\n\n\n', '\n\n').replace('\n\n    }', '\n    }')
        while prev != method:
            prev = method
            method = method.replace('\n\n\n', '\n\n').replace('\n\n    }', '\n    }')

        methods += method

    return """
    /**
     * @internal
     * @param string $header
     * @param string $data
     */
    public function handleCallback($header, $data)
    {
        call_user_func(array($this, $this->callbackWrappers[$header['functionID']]), $data);
    }
""" + methods

def make_callback_wrappers():
    if device.get_callback_count() == 0:
        return ''

    wrappers = """
    /**
     * Registers a callback with ID $id to the callable $callback.
     *
     * @param int $id
     * @param callable $callback
     *
     * @return void
     */
    public function registerCallback($id, $callback)
    {
        $this->registeredCallbacks[$id] = $callback;
    }
"""
    wrapper = """
    /**
     * @internal
     * @param string $data
     */
    public function callbackWrapper{0}($data)
    {{
        $result = array();
{1}

{2}

        call_user_func_array($this->registeredCallbacks[self::CALLBACK_{3}], $result);
    }}
"""

    for packet in device.get_packets('callback'):
        name = packet.get_camel_case_name()
        response_payload_elements = 0;
        response_payload_size = 0;
        unpack = []
        collect = []
        result = []

        for element in packet.get_elements('out'):
            response_payload_elements += 1;
            response_payload_size += common.get_element_size(element)

        for element in packet.get_elements('out'):
            unpack.append('{0}{1}{2}'.format(get_unpack_type(element), element[2], element[0]))

            unpack_fix = get_unpack_fix(element)

            if element[2] > 1:
                collect.append('        array_push($result, {2}$payload, \'{0}\', {1}{3});'.format(element[0], element[2], unpack_fix[0], unpack_fix[1]))
            else:
                collect.append('        array_push($result, {1}$payload[\'{0}\']{2});'.format(element[0], unpack_fix[0], unpack_fix[1]))

            result.append('$payload[\'{0}\']'.format(element[0]))

        foobar = ''

        if response_payload_size > 0:
            foobar = '        $payload = unpack(\'{0}\', $data);'.format('/'.join(unpack))

        wrappers += wrapper.format(name,
                                   foobar,
                                   '\n'.join(collect),
                                   packet.get_upper_case_name())

    return wrappers

def make_files(com_new, directory):
    global device
    device = common.Device(com_new)

    file_name = '{0}{1}'.format(device.get_category(), device.get_camel_case_name())

    directory += '/bindings'
    if not os.path.exists(directory):
        os.makedirs(directory)

    php = file('{0}/{1}.php'.format(directory, file_name), "w")
    php.write("<?php\n\n")
    php.write(make_import())
    php.write(make_class())
    php.write(make_callback_id_definitions())
    php.write(make_function_id_definitions())
    php.write(make_constructor())
    php.write(make_callback_wrapper_definitions())
    php.write(make_methods())
    php.write(make_callback_wrappers())
    php.write("}\n\n?>\n")

if __name__ == "__main__":
    common.generate(os.getcwd(), 'en', make_files)
