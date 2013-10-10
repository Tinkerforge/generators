#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PHP Bindings Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
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

sys.path.append(os.path.split(os.getcwd())[0])
import common
import php_common

device = None
released_files = []

def format_doc(packet, suffix):
    text = common.select_lang(packet.get_doc()[1])
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
    for other_packet in device.get_packets():
        name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
        if other_packet.get_type() == 'callback':
            name = other_packet.get_upper_case_name()
            name_right = link_c.format(device.get_category(), cls, name)
        else:
            name = other_packet.get_headless_camel_case_name()
            name_right = link.format(device.get_category(), cls, name)

        text = text.replace(name_false, name_right)

    text = text.replace('.. note::', '\\note')
    text = text.replace('.. warning::', '\\warning')

    text = common.handle_rst_word(text)
    text = common.handle_rst_if(text, device)
    text += common.format_since_firmware(device, packet)

    return '\n     * '.join(text.strip().split('\n') + suffix)

def make_parameter_doc(packet):
    param = []
    for element in packet.get_elements():
        if element.get_direction() == 'out' or packet.get_type() != 'function':
            continue

        php_type = php_common.get_php_type(element.get_type())
        if element.get_cardinality() > 1 and element.get_type() != 'string':
            param.append('@param {0}[] ${1}'.format(php_type, element.get_underscore_name()))
        else:
            param.append('@param {0} ${1}'.format(php_type, element.get_underscore_name()))

    param.append('\n@return ' + php_common.get_return_type(packet))
    return '\n'.join(param)

def make_import(version):
    include = """{0}
namespace Tinkerforge;

require_once(__DIR__ . '/IPConnection.php');
"""
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    return include.format(common.gen_text_star.format(date, *version))

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
        doc = format_doc(packet, [])
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


def make_constants():
    str_constants = '\n'
    str_constant = '    const {0}_{1} = {2};\n'
    constants = device.get_constants()
    for constant in constants:
        for definition in constant.definitions:
            if constant.type == 'char':
                value = "'{0}'".format(definition.value)
            else:
                value = str(definition.value)

            str_constants += str_constant.format(constant.name_uppercase,
                                                 definition.name_uppercase,
                                                 value)
    return str_constants

def make_device_identifier():
    return """
    const DEVICE_IDENTIFIER = {0};
""".format(device.get_device_identifier())

def make_constructor():
    con = """
    /**
     * Creates an object with the unique device ID $uid. This object can
     * then be added to the IP connection.
     *
     * @param string $uid
     */
    public function __construct($uid, $ipcon)
    {{
        parent::__construct($uid, $ipcon);

        $this->apiVersion = array({2}, {3}, {4});
"""
    response_expected = ''

    for packet in device.get_packets():
        if packet.get_type() == 'callback':
            prefix = 'CALLBACK'
            flag = 'self::RESPONSE_EXPECTED_ALWAYS_FALSE'
        elif len(packet.get_elements('out')) > 0:
            prefix = 'FUNCTION'
            flag = 'self::RESPONSE_EXPECTED_ALWAYS_TRUE'
        elif packet.get_doc()[0] == 'ccf':
            prefix = 'FUNCTION'
            flag = 'self::RESPONSE_EXPECTED_TRUE'
        else:
            prefix = 'FUNCTION'
            flag = 'self::RESPONSE_EXPECTED_FALSE'

        response_expected += '        $this->responseExpected[self::{1}_{2}] = {3};\n' \
            .format(device.get_upper_case_name(), prefix, packet.get_upper_case_name(), flag)

    if len(response_expected) > 0:
        response_expected = '\n' + response_expected

    return con.format(device.get_category(),
                      device.get_camel_case_name(),
                      *device.get_api_version()) + response_expected

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

    return forms[element.get_type()];

get_unpack_type = get_pack_type

def get_unpack_fix(element):
    if element.get_cardinality() > 1:
        if element.get_type() == 'int16':
            return ('IPConnection::collectUnpackedInt16Array(', ')')
        elif element.get_type() == 'int32':
            return ('IPConnection::collectUnpackedInt32Array(', ')')
        elif element.get_type() == 'uint32':
            return ('IPConnection::collectUnpackedUInt32Array(', ')')
        elif element.get_type() == 'bool':
            return ('IPConnection::collectUnpackedBoolArray(', ')')
        elif element.get_type() == 'string':
            return ('IPConnection::implodeUnpackedString(', ')')
        elif element.get_type() == 'char':
            return ('IPConnection::collectUnpackedCharArray(', ')')
        else:
            return ('IPConnection::collectUnpackedArray(', ')')
    else:
        if element.get_type() == 'int16':
            return ('IPConnection::fixUnpackedInt16(', ')')
        elif element.get_type() == 'int32':
            return ('IPConnection::fixUnpackedInt32(', ')')
        elif element.get_type() == 'uint32':
            return ('IPConnection::fixUnpackedUInt32(', ')')
        elif element.get_type() == 'bool':
            return ('(bool)', '')
        elif element.get_type() == 'string':
            return ('chr(', ')')
        elif element.get_type() == 'char':
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
        parameter = php_common.make_parameter_list(packet)
        pack = []
        for element in packet.get_elements('in'):
            if element.get_type() == 'bool':
                if element.get_cardinality() > 1:
                    pack.append('        for ($i = 0; $i < {0}; $i++) {{'.format(element[2]))
                    pack.append('            $payload .= pack(\'{0}\', intval((bool)${1}[$i]));\n        }}'.format(get_pack_type(element), element.get_underscore_name()))
                else:
                    pack.append('        $payload .= pack(\'{0}\', intval((bool)${1}));'.format(get_pack_type(element), element.get_underscore_name()))
            elif element.get_type() == 'string':
                if element.get_cardinality() > 1:
                    pack.append('        for ($i = 0; $i < strlen(${0}) && $i < {1}; $i++) {{'.format(element.get_underscore_name(), element.get_cardinality()))
                    pack.append('            $payload .= pack(\'{0}\', ord(${1}[$i]));\n        }}'.format(get_pack_type(element), element.get_underscore_name()))
                    pack.append('        for ($i = strlen(${0}); $i < {1}; $i++) {{'.format(element.get_underscore_name(), element.get_cardinality()))
                    pack.append('            $payload .= pack(\'{0}\', 0);\n        }}'.format(get_pack_type(element)))
                else:
                    pack.append('        $payload .= pack(\'{0}\', ord(${1}));'.format(get_pack_type(element), element.get_underscore_name()))
            elif element.get_type() == 'char':
                if element.get_cardinality() > 1:
                    pack.append('        for ($i = 0; $i < count(${0}) && $i < {1}; $i++) {{'.format(element.get_underscore_name(), element.get_cardinality()))
                    pack.append('            $payload .= pack(\'{0}\', ord(${1}[$i]));\n        }}'.format(get_pack_type(element), element.get_underscore_name()))
                    pack.append('        for ($i = count(${0}); $i < {1}; $i++) {{'.format(element.get_underscore_name(), element.get_cardinality()))
                    pack.append('            $payload .= pack(\'{0}\', 0);\n        }}'.format(get_pack_type(element)))
                else:
                    pack.append('        $payload .= pack(\'{0}\', ord(${1}));'.format(get_pack_type(element), element.get_underscore_name()))
            else:
                if element.get_cardinality() > 1:
                    pack.append('        for ($i = 0; $i < {0}; $i++) {{'.format(element.get_cardinality()))
                    pack.append('            $payload .= pack(\'{0}\', ${1}[$i]);\n        }}'.format(get_pack_type(element), element.get_underscore_name()))
                else:
                    pack.append('        $payload .= pack(\'{0}\', ${1});'.format(get_pack_type(element), element.get_underscore_name()))

        has_multi_return_value = len(packet.get_elements('out')) > 1
        unpack_format = []
        collect = []

        for element in packet.get_elements('out'):
            unpack_format.append('{0}{1}{2}'.format(get_unpack_type(element), element.get_cardinality(), element.get_underscore_name()))

            unpack_fix = get_unpack_fix(element)

            if has_multi_return_value:
                if element.get_cardinality() > 1:
                    collect.append('        $result[\'{0}\'] = {2}$payload, \'{0}\', {1}{3};'.format(element.get_underscore_name(), element.get_cardinality(), unpack_fix[0], unpack_fix[1]))
                else:
                    collect.append('        $result[\'{0}\'] = {1}$payload[\'{0}\']{2};'.format(element.get_underscore_name(), unpack_fix[0], unpack_fix[1]))
            else:
                if element.get_cardinality() > 1:
                    collect.append('        return {2}$payload, \'{0}\', {1}{3};'.format(element.get_underscore_name(), element.get_cardinality(), unpack_fix[0], unpack_fix[1]))
                else:
                    collect.append('        return {1}$payload[\'{0}\']{2};'.format(element.get_underscore_name(), unpack_fix[0], unpack_fix[1]))

        if len(unpack_format) > 0:
            send = '        $data = $this->sendRequest(self::FUNCTION_{0}, $payload);\n'.format(packet.get_upper_case_name())
        else:
            send = '        $this->sendRequest(self::FUNCTION_{0}, $payload);\n'.format(packet.get_upper_case_name())

        final_unpack = ''

        if len(unpack_format) > 0:
            final_unpack = '        $payload = unpack(\'{0}\', $data);'.format('/'.join(unpack_format))

        doc = format_doc(packet, [''] + make_parameter_doc(packet).split('\n'))

        if has_multi_return_value:
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
     * @param mixed $userData
     *
     * @return void
     */
    public function registerCallback($id, $callback, $userData = NULL)
    {
        $this->registeredCallbacks[$id] = $callback;
        $this->registeredCallbackUserData[$id] = $userData;
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
        unpack_format = []
        collect = []
        result = []

        for element in packet.get_elements('out'):
            unpack_format.append('{0}{1}{2}'.format(get_unpack_type(element), element.get_cardinality(), element.get_underscore_name()))

            unpack_fix = get_unpack_fix(element)

            if element.get_cardinality() > 1:
                collect.append('        array_push($result, {2}$payload, \'{0}\', {1}{3});'.format(element.get_underscore_name(), element.get_cardinality(), unpack_fix[0], unpack_fix[1]))
            else:
                collect.append('        array_push($result, {1}$payload[\'{0}\']{2});'.format(element.get_underscore_name(), unpack_fix[0], unpack_fix[1]))

            result.append('$payload[\'{0}\']'.format(element.get_underscore_name()))

        final_unpack = ''

        if len(unpack_format) > 0:
            final_unpack = '        $payload = unpack(\'{0}\', $data);'.format('/'.join(unpack_format))

        wrappers += wrapper.format(name,
                                   final_unpack,
                                   '\n'.join(collect),
                                   packet.get_upper_case_name())

    return wrappers

def make_files(device_, directory):
    global device
    device = device_
    file_name = '{0}{1}.php'.format(device.get_category(), device.get_camel_case_name())
    version = common.get_changelog_version(directory)
    directory += '/bindings'

    php = file('{0}/{1}'.format(directory , file_name), "w")
    php.write("<?php\n\n")
    php.write(make_import(version))
    php.write(make_class())
    php.write(make_callback_id_definitions())
    php.write(make_function_id_definitions())
    php.write(make_constants())
    php.write(make_device_identifier())
    php.write(make_constructor())
    php.write(make_callback_wrapper_definitions())
    php.write(make_methods())
    php.write(make_callback_wrappers())
    php.write("}\n\n?>\n")

    if device.is_released():
        global released_files
        released_files.append(file_name)

class PHPBindingsGenerator(common.Generator):
    def prepare(self):
        common.recreate_directory(os.path.join(self.get_bindings_root_directory(), 'bindings'))

    def generate(self, device):
        make_files(device, self.get_bindings_root_directory())

    def finish(self):
        r = open(os.path.join(self.get_bindings_root_directory(), 'php_released_files.py'), 'wb')
        r.write('released_files = ' + repr(released_files))
        r.close()

def generate(path):
    common.generate(path, 'en', PHPBindingsGenerator, False)

if __name__ == "__main__":
    generate(os.getcwd())
