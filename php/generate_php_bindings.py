#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PHP Bindings Generator
Copyright (C) 2012-2015 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generate_php_bindings.py: Generator for PHP bindings

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

import sys
import os

sys.path.append(os.path.split(os.getcwd())[0])
import common
import php_common

class PHPBindingsDevice(php_common.PHPDevice):
    def specialize_php_doc_function_links(self, text):
        def specializer(packet):
            if packet.get_type() == 'callback':
                return '{0}::CALLBACK_{1}'.format(packet.get_device().get_php_class_name(),
                                                  packet.get_upper_case_name())
            else:
                return '{0}::{1}()'.format(packet.get_device().get_php_class_name(),
                                           packet.get_headless_camel_case_name())

        return self.specialize_doc_function_links(text, specializer)

    def get_php_import(self):
        include = """{0}
namespace Tinkerforge;

require_once(__DIR__ . '/IPConnection.php');
"""

        return include.format(self.get_generator().get_header_comment('asterisk'))

    def get_php_class(self):
        class_str = """
/**
 * {1}
 */
class {0} extends Device
{{
"""

        return class_str.format(self.get_php_class_name(), self.get_description())

    def get_php_callback_wrapper_definitions(self):
        cbs = ''
        cb = """
        $this->callbackWrappers[self::CALLBACK_{0}] = 'callbackWrapper{1}';"""
        cbs_end = '\n    }\n'
        for packet in self.get_packets('callback'):
            typ = packet.get_upper_case_name()
            name = packet.get_camel_case_name()

            cbs += cb.format(typ, name)
        return cbs + cbs_end

    def get_php_callback_id_definitions(self):
        cbs = ''
        cb = """
    /**
     * {2}
     */
    const CALLBACK_{0} = {1};
"""
        for packet in self.get_packets('callback'):
            doc = packet.get_php_formatted_doc([])
            cbs += cb.format(packet.get_upper_case_name(), packet.get_function_id(), doc)
        return cbs + '\n'

    def get_php_function_id_definitions(self):
        function_ids = ''
        function_id = """
    /**
     * @internal
     */
    const FUNCTION_{0} = {1};
"""
        for packet in self.get_packets('function'):
            function_ids += function_id.format(packet.get_upper_case_name(), packet.get_function_id())
        return function_ids


    def get_php_constants(self):
        constant_format = '    const {constant_group_upper_case_name}_{constant_upper_case_name} = {constant_value};\n'

        return '\n' + self.get_formatted_constants(constant_format)

    def get_php_device_identifier(self):
        return """
    const DEVICE_IDENTIFIER = {0};
""".format(self.get_device_identifier())

    def get_php_device_display_name(self):
        return """
    const DEVICE_DISPLAY_NAME = "{0}";
""".format(self.get_long_display_name())

    def get_php_constructor(self):
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

        $this->apiVersion = array({0}, {1}, {2});
"""
        response_expected = ''

        for packet in self.get_packets():
            if packet.get_type() == 'callback':
                prefix = 'CALLBACK'
                flag = 'self::RESPONSE_EXPECTED_ALWAYS_FALSE'
            elif len(packet.get_elements('out')) > 0:
                prefix = 'FUNCTION'
                flag = 'self::RESPONSE_EXPECTED_ALWAYS_TRUE'
            elif packet.get_doc_type() == 'ccf':
                prefix = 'FUNCTION'
                flag = 'self::RESPONSE_EXPECTED_TRUE'
            else:
                prefix = 'FUNCTION'
                flag = 'self::RESPONSE_EXPECTED_FALSE'

            response_expected += '        $this->responseExpected[self::{1}_{2}] = {3};\n' \
                .format(self.get_upper_case_name(), prefix, packet.get_upper_case_name(), flag)

        if len(response_expected) > 0:
            response_expected = '\n' + response_expected

        return con.format(*self.get_api_version()) + response_expected

    def get_php_methods(self):
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

        for packet in self.get_packets('function'):
            name_lower = packet.get_headless_camel_case_name()
            parameter = packet.get_php_parameter_list()
            pack = []

            for element in packet.get_elements('in'):
                underscore_name = element.get_underscore_name()
                cardinality = element.get_cardinality()
                pack_format = element.get_php_pack_format()

                if element.get_type() == 'bool':
                    if cardinality > 1:
                        pack.append('        for ($i = 0; $i < {0}; $i++) {{'.format(element[2]))
                        pack.append('            $payload .= pack(\'{0}\', intval((bool)${1}[$i]));\n        }}'.format(pack_format, underscore_name))
                    else:
                        pack.append('        $payload .= pack(\'{0}\', intval((bool)${1}));'.format(pack_format, underscore_name))
                elif element.get_type() == 'string':
                    if cardinality > 1:
                        pack.append('        for ($i = 0; $i < strlen(${0}) && $i < {1}; $i++) {{'.format(underscore_name, cardinality))
                        pack.append('            $payload .= pack(\'{0}\', ord(${1}[$i]));\n        }}'.format(pack_format, underscore_name))
                        pack.append('        for ($i = strlen(${0}); $i < {1}; $i++) {{'.format(underscore_name, cardinality))
                        pack.append('            $payload .= pack(\'{0}\', 0);\n        }}'.format(pack_format))
                    else:
                        pack.append('        $payload .= pack(\'{0}\', ord(${1}));'.format(pack_format, underscore_name))
                elif element.get_type() == 'char':
                    if cardinality > 1:
                        pack.append('        for ($i = 0; $i < count(${0}) && $i < {1}; $i++) {{'.format(underscore_name, cardinality))
                        pack.append('            $payload .= pack(\'{0}\', ord(${1}[$i]));\n        }}'.format(pack_format, underscore_name))
                        pack.append('        for ($i = count(${0}); $i < {1}; $i++) {{'.format(underscore_name, cardinality))
                        pack.append('            $payload .= pack(\'{0}\', 0);\n        }}'.format(pack_format))
                    else:
                        pack.append('        $payload .= pack(\'{0}\', ord(${1}));'.format(pack_format, underscore_name))
                elif element.get_type() == 'int64':
                    if cardinality > 1:
                        pack.append('        for ($i = 0; $i < {0}; $i++) {{'.format(cardinality))
                        pack.append('            $payload .= Base256::encodeAndPackInt64(${0}[$i], 8);\n        }}'.format(underscore_name))
                    else:
                        pack.append('        $payload .= Base256::encodeAndPackInt64(${0}, 8);'.format(underscore_name))
                elif element.get_type() == 'uint64':
                    if cardinality > 1:
                        pack.append('        for ($i = 0; $i < {0}; $i++) {{'.format(cardinality))
                        pack.append('            $payload .= Base256::encodeAndPackUInt64(${0}[$i], 8);\n        }}'.format(underscore_name))
                    else:
                        pack.append('        $payload .= Base256::encodeAndPackUInt64(${0}, 8);'.format(underscore_name))
                else:
                    if cardinality > 1:
                        pack.append('        for ($i = 0; $i < {0}; $i++) {{'.format(cardinality))
                        pack.append('            $payload .= pack(\'{0}\', ${1}[$i]);\n        }}'.format(pack_format, underscore_name))
                    else:
                        pack.append('        $payload .= pack(\'{0}\', ${1});'.format(pack_format, underscore_name))

            has_multi_return_value = len(packet.get_elements('out')) > 1
            unpack_formats = []
            collect = []

            for element in packet.get_elements('out'):
                underscore_name = element.get_underscore_name()
                cardinality = element.get_cardinality()
                unpack_fix = element.get_php_unpack_fix()

                unpack_formats.append(element.get_php_unpack_format())

                if has_multi_return_value:
                    if cardinality > 1:
                        collect.append('        $result[\'{0}\'] = {2}$payload{4}\'{0}\'{5}, {1}{3};'.format(underscore_name, cardinality, *unpack_fix))
                    else:
                        collect.append('        $result[\'{0}\'] = {1}$payload{3}\'{0}\'{4}{2};'.format(underscore_name, *unpack_fix))
                else:
                    if cardinality > 1:
                        collect.append('        return {2}$payload{4}\'{0}\'{5}, {1}{3};'.format(underscore_name, cardinality, *unpack_fix))
                    else:
                        collect.append('        return {1}$payload{3}\'{0}\'{4}{2};'.format(underscore_name, *unpack_fix))

            if len(unpack_formats) > 0:
                send = '        $data = $this->sendRequest(self::FUNCTION_{0}, $payload);\n'.format(packet.get_upper_case_name())
            else:
                send = '        $this->sendRequest(self::FUNCTION_{0}, $payload);\n'.format(packet.get_upper_case_name())

            final_unpack = ''

            if len(unpack_formats) > 0:
                final_unpack = '        $payload = unpack(\'{0}\', $data);'.format('/'.join(unpack_formats))

            doc = packet.get_php_formatted_doc([''] + packet.get_php_parameter_doc().split('\n'))

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

    def get_php_callback_wrappers(self):
        if self.get_callback_count() == 0:
            return ''

        wrappers = """
    /**
     * Registers a callback with ID $id to the callable $callback.
     *
     * @param int $id
     * @param callable $callback
     * @param mixed $user_data
     *
     * @return void
     */
    public function registerCallback($id, $callback, $user_data = NULL)
    {
        if (!is_callable($callback)) {
            throw new \Exception('Callback function is not callable');
        }

        $this->registeredCallbacks[$id] = $callback;
        $this->registeredCallbackUserData[$id] = $user_data;
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
        array_push($result, $this->registeredCallbackUserData[self::CALLBACK_{3}]);

        call_user_func_array($this->registeredCallbacks[self::CALLBACK_{3}], $result);
    }}
"""

        for packet in self.get_packets('callback'):
            name = packet.get_camel_case_name()
            unpack_formats = []
            collect = []
            result = []

            for element in packet.get_elements('out'):
                underscore_name = element.get_underscore_name()
                cardinality = element.get_cardinality()

                unpack_formats.append(element.get_php_unpack_format())

                unpack_fix = element.get_php_unpack_fix()

                if cardinality > 1:
                    collect.append('        array_push($result, {2}$payload{4}\'{0}\'{5}, {1}{3});'.format(underscore_name, cardinality, *unpack_fix))
                else:
                    collect.append('        array_push($result, {1}$payload{3}\'{0}\'{4}{2});'.format(underscore_name, *unpack_fix))

                result.append('$payload[\'{0}\']'.format(underscore_name))

            final_unpack = ''

            if len(unpack_formats) > 0:
                final_unpack = '        $payload = unpack(\'{0}\', $data);'.format('/'.join(unpack_formats))

            wrappers += wrapper.format(name,
                                       final_unpack,
                                       '\n'.join(collect),
                                       packet.get_upper_case_name())

        return wrappers

    def get_php_source(self):
        source  = '<?php\n\n'
        source += self.get_php_import()
        source += self.get_php_class()
        source += self.get_php_callback_id_definitions()
        source += self.get_php_function_id_definitions()
        source += self.get_php_constants()
        source += self.get_php_device_identifier()
        source += self.get_php_device_display_name()
        source += self.get_php_constructor()
        source += self.get_php_callback_wrapper_definitions()
        source += self.get_php_methods()
        source += self.get_php_callback_wrappers()
        source += '}\n\n?>\n'

        return source

class PHPBindingsPacket(php_common.PHPPacket):
    def get_php_formatted_doc(self, suffix):
        text = common.select_lang(self.get_doc_text())

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
        text = self.get_device().specialize_php_doc_function_links(text)

        text = text.replace('.. note::', '\\note')
        text = text.replace('.. warning::', '\\warning')

        def format_parameter(name):
            return name # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return '\n     * '.join(text.strip().split('\n') + suffix)

    def get_php_parameter_doc(self):
        param = []

        for element in self.get_elements():
            if element.get_direction() == 'out' or self.get_type() != 'function':
                continue

            php_type = element.get_php_type()
            if element.get_cardinality() > 1 and element.get_type() != 'string':
                param.append('@param {0}[] ${1}'.format(php_type, element.get_underscore_name()))
            else:
                param.append('@param {0} ${1}'.format(php_type, element.get_underscore_name()))

        param.append('\n@return ' + self.get_php_return_type())

        return '\n'.join(param)

class PHPBindingsGenerator(common.BindingsGenerator):
    def get_bindings_name(self):
        return 'php'

    def get_bindings_display_name(self):
        return 'PHP'

    def get_device_class(self):
        return PHPBindingsDevice

    def get_packet_class(self):
        return PHPBindingsPacket

    def get_element_class(self):
        return php_common.PHPElement

    def generate(self, device):
        filename = '{0}.php'.format(device.get_php_class_name())

        php = open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename), 'wb')
        php.write(device.get_php_source())
        php.close()

        if device.is_released():
            self.released_files.append(filename)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', PHPBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
