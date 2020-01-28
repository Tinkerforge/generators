#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PHP Bindings Generator
Copyright (C) 2012-2015, 2017-2018, 2020 Matthias Bolte <matthias@tinkerforge.com>
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

import math
import sys
import os

sys.path.append(os.path.split(os.getcwd())[0])
import common
import php_common

class PHPBindingsDevice(php_common.PHPDevice):
    def specialize_php_doc_function_links(self, text):
        def specializer(packet, high_level):
            if packet.get_type() == 'callback':
                return '{0}::CALLBACK_{1}'.format(packet.get_device().get_php_class_name(),
                                                  packet.get_name(skip=-2 if high_level else 0).upper)
            else:
                return '{0}::{1}()'.format(packet.get_device().get_php_class_name(),
                                           packet.get_name(skip=-2 if high_level else 0).headless)

        return self.specialize_doc_rst_links(text, specializer)

    def get_php_import(self):
        template = """{0}
namespace Tinkerforge;

require_once(__DIR__ . '/IPConnection.php');
"""

        return template.format(self.get_generator().get_header_comment('asterisk'))

    def get_php_class(self):
        template = """
/**
 * {1}
 */
class {0} extends Device
{{
"""

        return template.format(self.get_php_class_name(), common.select_lang(self.get_description()))

    def get_php_callback_wrapper_definitions(self):
        callbacks = ''
        template = """
        $this->callback_wrappers[self::CALLBACK_{0}] = 'callbackWrapper{1}';"""

        for packet in self.get_packets('callback'):
            callbacks += template.format(packet.get_name().upper,
                                         packet.get_name().camel)

        return callbacks

    def get_php_high_level_callbacks(self):
        callbacks = ''
        template = """
        $this->high_level_callbacks[self::CALLBACK_{0}] = array('data' => NULL);"""

        for packet in self.get_packets('callback'):
            if not packet.has_high_level():
                continue

            callbacks += template.format(packet.get_name(skip=-2).upper)

        return common.wrap_non_empty('\n', callbacks, '') + '\n\n        $ipcon->addDevice($this);\n    }\n'

    def get_php_callback_id_definitions(self):
        callbacks = ''
        template = """
    /**
     * {2}
     */
    const CALLBACK_{0} = {1};
"""

        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                doc = 'See CALLBACK_{}'.format(packet.get_name(skip=-2).upper)
            else:
                doc = packet.get_php_formatted_doc([])
            callbacks += template.format(packet.get_name().upper, packet.get_function_id(), doc)

        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                doc = packet.get_php_formatted_doc([])
                callbacks += template.format(packet.get_name(skip=-2).upper, -packet.get_function_id(), doc)

        if self.get_long_display_name() == 'RS232 Bricklet':
            callbacks += """
    /**
     * This callback is called if new data is available. The message has
     * a maximum size of 60 characters. The actual length of the message
     * is given in addition.
     *
     * To enable this callback, use BrickletRS232::enableReadCallback().
     */
    const CALLBACK_READ_CALLBACK = self::CALLBACK_READ; // for backward compatibility

    /**
     * This callback is called if an error occurs.
     * Possible errors are overrun, parity or framing error.
     *
     * .. versionadded:: 2.0.1$nbsp;(Plugin)
     */
    const CALLBACK_ERROR_CALLBACK = self::CALLBACK_ERROR; // for backward compatibility
"""

        return callbacks + '\n'

    def get_php_function_id_definitions(self):
        function_ids = ''
        template = """
    /**
     * @internal
     */
    const FUNCTION_{0} = {1};
"""

        for packet in self.get_packets('function'):
            function_ids += template.format(packet.get_name().upper, packet.get_function_id())

        return function_ids

    def get_php_constants(self):
        constant_format = '    const {constant_group_name_upper}_{constant_name_upper} = {constant_value};\n'

        return '\n' + self.get_formatted_constants(constant_format, bool_format_func=lambda value: str(value).lower())

    def get_php_device_identifier(self):
        template = """
    const DEVICE_IDENTIFIER = {0};
"""

        return template.format(self.get_device_identifier())

    def get_php_device_display_name(self):
        template = """
    const DEVICE_DISPLAY_NAME = '{0}';
"""

        return template.format(self.get_long_display_name())

    def get_php_constructor(self):
        template = """
    /**
     * Creates an object with the unique device ID $uid. This object can
     * then be added to the IP connection.
     *
     * @param string $uid
     */
    public function __construct($uid, $ipcon)
    {{
        parent::__construct($uid, $ipcon, self::DEVICE_IDENTIFIER, self::DEVICE_DISPLAY_NAME);

        $this->api_version = array({0}, {1}, {2});
"""
        response_expected = ''

        for packet in self.get_packets('function'):
            response_expected += '        $this->response_expected[self::FUNCTION_{0}] = self::RESPONSE_EXPECTED_{1};\n' \
                                 .format(packet.get_name().upper, packet.get_response_expected().upper())

        return template.format(*self.get_api_version()) + common.wrap_non_empty('\n', response_expected, '')

    def get_php_methods(self):
        methods = ''

        # normal and low-level
        method_multi = """
    /**
     * {6}
     */
    public function {0}({1})
    {{
        {7}$ret = array();

        $payload = '';
{2}

{3}

{4}

{5}

        return $ret;
    }}
"""
        method_single = """
    /**
     * {6}
     */
    public function {0}({1})
    {{
        {7}$payload = '';
{2}

{3}

{4}

{5}
    }}
"""

        for packet in self.get_packets('function'):
            name_headless = packet.get_name().headless
            parameter = packet.get_php_parameters()
            pack = []

            for element in packet.get_elements(direction='in'):
                name_under = element.get_name().under
                cardinality = element.get_cardinality()
                pack_format = element.get_php_pack_format()

                if element.get_type() == 'bool':
                    if cardinality > 1:
                        pack.append('        ${0} = array_fill(0, {1}, 0);'.format(name_under + '_bits', str(int(math.ceil(cardinality/8.0)))))
                        pack.append('        for ($i = 0; $i < {0}; $i++) {{'.format(cardinality))
                        pack.append('            if((bool)${1}[$i]) {{'.format(pack_format, name_under))
                        pack.append('              ${0}[$i / 8] |= 1 << ($i % 8);'.format(name_under + '_bits'))
                        pack.append('            }')
                        pack.append('        }')
                        pack.append('        for ($i = 0; $i < {0}; $i++) {{'.format(str(int(math.ceil(cardinality/8.0)))))
                        pack.append('          $payload .= pack(\'C\', intval(${0}[$i]));'.format(name_under + '_bits'))
                        pack.append('        }')
                    else:
                        pack.append('        $payload .= pack(\'{0}\', intval((bool)${1}));'.format(pack_format, name_under))
                elif element.get_type() == 'string':
                    if cardinality > 1:
                        pack.append('        for ($i = 0; $i < strlen(${0}) && $i < {1}; $i++) {{'.format(name_under, cardinality))
                        pack.append('            $payload .= pack(\'{0}\', ord(${1}[$i]));\n        }}'.format(pack_format, name_under))
                        pack.append('        for ($i = strlen(${0}); $i < {1}; $i++) {{'.format(name_under, cardinality))
                        pack.append('            $payload .= pack(\'{0}\', 0);\n        }}'.format(pack_format))
                    else:
                        pack.append('        $payload .= pack(\'{0}\', ord(${1}));'.format(pack_format, name_under))
                elif element.get_type() == 'char':
                    if cardinality > 1:
                        pack.append('        for ($i = 0; $i < count(${0}) && $i < {1}; $i++) {{'.format(name_under, cardinality))
                        pack.append('            $payload .= pack(\'{0}\', ord(${1}[$i]));\n        }}'.format(pack_format, name_under))
                        pack.append('        for ($i = count(${0}); $i < {1}; $i++) {{'.format(name_under, cardinality))
                        pack.append('            $payload .= pack(\'{0}\', 0);\n        }}'.format(pack_format))
                    else:
                        pack.append('        $payload .= pack(\'{0}\', ord(${1}));'.format(pack_format, name_under))
                elif element.get_type() == 'int64':
                    if cardinality > 1:
                        pack.append('        for ($i = 0; $i < {0}; $i++) {{'.format(cardinality))
                        pack.append('            $payload .= Base256::encodeAndPackInt64(${0}[$i], 8);\n        }}'.format(name_under))
                    else:
                        pack.append('        $payload .= Base256::encodeAndPackInt64(${0}, 8);'.format(name_under))
                elif element.get_type() == 'uint64':
                    if cardinality > 1:
                        pack.append('        for ($i = 0; $i < {0}; $i++) {{'.format(cardinality))
                        pack.append('            $payload .= Base256::encodeAndPackUInt64(${0}[$i], 8);\n        }}'.format(name_under))
                    else:
                        pack.append('        $payload .= Base256::encodeAndPackUInt64(${0}, 8);'.format(name_under))
                else:
                    if cardinality > 1:
                        pack.append('        for ($i = 0; $i < {0}; $i++) {{'.format(cardinality))
                        pack.append('            $payload .= pack(\'{0}\', ${1}[$i]);\n        }}'.format(pack_format, name_under))
                    else:
                        pack.append('        $payload .= pack(\'{0}\', ${1});'.format(pack_format, name_under))

            has_multi_return_value = len(packet.get_elements(direction='out')) > 1
            unpack_formats = []
            collect = []

            for element in packet.get_elements(direction='out'):
                name_under = element.get_name().under
                cardinality = element.get_cardinality()
                unpack_fix = element.get_php_unpack_fix()

                if unpack_fix == None:
                    unpack_fix = ('', '', '[', ']')

                unpack_formats.append(element.get_php_unpack_format())

                if has_multi_return_value:
                    if cardinality > 1:
                        collect.append('        $ret[\'{0}\'] = {2}$payload{4}\'{0}\'{5}, {1}{3};'.format(name_under, cardinality, *unpack_fix))
                    else:
                        collect.append('        $ret[\'{0}\'] = {1}$payload{3}\'{0}\'{4}{2};'.format(name_under, *unpack_fix))
                else:
                    if cardinality > 1:
                        collect.append('        return {2}$payload{4}\'{0}\'{5}, {1}{3};'.format(name_under, cardinality, *unpack_fix))
                    else:
                        collect.append('        return {1}$payload{3}\'{0}\'{4}{2};'.format(name_under, *unpack_fix))

            if len(unpack_formats) > 0:
                send = '        $data = $this->sendRequest(self::FUNCTION_{0}, $payload);\n'.format(packet.get_name().upper)
            else:
                send = '        $this->sendRequest(self::FUNCTION_{0}, $payload);\n'.format(packet.get_name().upper)

            final_unpack = ''

            if len(unpack_formats) > 0:
                final_unpack = '        $payload = unpack(\'{0}\', $data);'.format('/'.join(unpack_formats))

            doc = packet.get_php_formatted_doc([''] + packet.get_php_parameter_doc().split('\n'))

            if packet.get_function_id() == 255: # <device>->get_identity
                check = ''
            else:
                check = '$this->checkDeviceIdentifier();\n\n        '

            if has_multi_return_value:
                method = method_multi.format(name_headless,
                                             parameter,
                                             '\n'.join(pack),
                                             send,
                                             final_unpack,
                                             '\n'.join(collect),
                                             doc,
                                             check)
            else:
                method = method_single.format(name_headless,
                                              parameter,
                                              '\n'.join(pack),
                                              send,
                                              final_unpack,
                                              '\n'.join(collect),
                                              doc,
                                              check)

            prev = method
            method = method.replace('\n\n\n', '\n\n').replace('\n\n    }', '\n    }')

            while prev != method:
                prev = method
                method = method.replace('\n\n\n', '\n\n').replace('\n\n    }', '\n    }')

            methods += method

        # high-level
        template_stream_in = """
    /**
     * {doc}
     */
    public function {name}({high_level_parameters})
    {{
        if (count(${stream_name_under}) > {stream_max_length}) {{
            throw new \\InvalidArgumentException('{stream_name_space} can be at most {stream_max_length} items long');
        }}

        ${stream_name_under}_length = count(${stream_name_under});
        ${stream_name_under}_chunk_offset = 0;

        if (${stream_name_under}_length === 0) {{
            ${stream_name_under}_chunk_data = array_fill(0, {chunk_cardinality}, {chunk_padding});
            $ret = $this->{name}LowLevel({parameters});
        }} else {{
            while (${stream_name_under}_chunk_offset < ${stream_name_under}_length) {{
                ${stream_name_under}_chunk_data = $this->createChunkData(${stream_name_under}, ${stream_name_under}_chunk_offset, {chunk_cardinality}, {chunk_padding});
                $ret = $this->{name}LowLevel({parameters});
                ${stream_name_under}_chunk_offset += {chunk_cardinality};
            }}
        }}
{result}
    }}
"""
        template_stream_in_fixed_length = """
    /**
     * {doc}
     */
    public function {name}({high_level_parameters})
    {{
        ${stream_name_under}_length = {fixed_length};
        ${stream_name_under}_chunk_offset = 0;

        if (count(${stream_name_under}) !== ${stream_name_under}_length) {{
            throw new \\InvalidArgumentException("{stream_name_space} has to be exactly ${stream_name_under}_length items long");
        }}

        while (${stream_name_under}_chunk_offset < ${stream_name_under}_length) {{
            ${stream_name_under}_chunk_data = $this->createChunkData(${stream_name_under}, ${stream_name_under}_chunk_offset, {chunk_cardinality}, {chunk_padding});
            $ret = $this->{name}LowLevel({parameters});
            ${stream_name_under}_chunk_offset += {chunk_cardinality};
        }}
{result}
    }}
"""
        template_stream_in_result = """
        return $ret;"""
        template_stream_in_short_write = """
    /**
     * {doc}
     */
    public function {name}({high_level_parameters})
    {{
        if (count(${stream_name_under}) > {stream_max_length}) {{
            throw new \\InvalidArgumentException('{stream_name_space} can be at most {stream_max_length} items long');
        }}

        ${stream_name_under}_length = count(${stream_name_under});
        ${stream_name_under}_chunk_offset = 0;

        if (${stream_name_under}_length === 0) {{
            ${stream_name_under}_chunk_data = array_fill(0, {chunk_cardinality}, {chunk_padding});
            $ret = $this->{name}LowLevel({parameters});
            {chunk_written_0}
        }} else {{
            ${stream_name_under}_written = 0;

            while (${stream_name_under}_chunk_offset < ${stream_name_under}_length) {{
                ${stream_name_under}_chunk_data = $this->createChunkData(${stream_name_under}, ${stream_name_under}_chunk_offset, {chunk_cardinality}, {chunk_padding});
                $ret = $this->{name}LowLevel({parameters});
                {chunk_written_n}

                if ({chunk_written_test} < {chunk_cardinality}) {{
                    break; # either last chunk or short write
                }}

                ${stream_name_under}_chunk_offset += {chunk_cardinality};
            }}
        }}
{result}
    }}
"""
        template_stream_in_short_write_chunk_written = ['${stream_name_under}_written = $ret;',
                                                        '${stream_name_under}_written += $ret;',
                                                        '$ret']
        template_stream_in_short_write_namedtuple_chunk_written = ["${stream_name_under}_written = $ret['{stream_name_under}_chunk_written'];",
                                                                   "${stream_name_under}_written += $ret['{stream_name_under}_chunk_written'];",
                                                                   '$ret["{stream_name_under}_chunk_written"]']
        template_stream_in_short_write_result = """
        return ${stream_name_under}_written;"""
        template_stream_in_short_write_namedtuple_result = """
        return array({result_fields});"""
        template_stream_in_single_chunk = """
    /**
     * {doc}
     */
    public function {name}({high_level_parameters})
    {{
        ${stream_name_under}_length = count(${stream_name_under});
        ${stream_name_under}_data = ${stream_name_under};

        if (${stream_name_under}_length > {chunk_cardinality}) {{
            throw new \\InvalidArgumentException('{stream_name_space} can be at most {chunk_cardinality} items long');
        }}

        if (${stream_name_under}_length < {chunk_cardinality}) {{
            ${stream_name_under}_data = array_pad(${stream_name_under}_data, {chunk_cardinality}, {chunk_padding});
        }}
{result}
    }}
"""
        template_stream_in_single_chunk_result = """
        return $this->{name}LowLevel({parameters});"""
        template_stream_out = """
    /**
     * {doc}
     */
    public function {name}({high_level_parameters})
    {{{fixed_length}
        $ret = $this->{name}LowLevel({parameters});{dynamic_length_2}
        {chunk_offset_check}${stream_name_under}_out_of_sync = $ret['{stream_name_under}_chunk_offset'] != 0;
        {chunk_offset_check_indent}${stream_name_under}_data = $ret['{stream_name_under}_chunk_data'];{chunk_offset_check_end}

        while (!${stream_name_under}_out_of_sync && count(${stream_name_under}_data) < ${stream_name_under}_length) {{
            $ret = $this->{name}LowLevel({parameters});{dynamic_length_3}
            ${stream_name_under}_out_of_sync = $ret['{stream_name_under}_chunk_offset'] != count(${stream_name_under}_data);
            ${stream_name_under}_data = array_merge(${stream_name_under}_data, $ret['{stream_name_under}_chunk_data']);
        }}

        if (${stream_name_under}_out_of_sync) {{ // discard remaining stream to bring it back in-sync
            while ($ret['{stream_name_under}_chunk_offset'] + {chunk_cardinality} < ${stream_name_under}_length) {{
                $ret = $this->{name}LowLevel({parameters});{dynamic_length_4}
            }}

            throw new StreamOutOfSyncException('{stream_name_space} stream is out-of-sync');
        }}
{result}
    }}
"""
        template_stream_out_fixed_length = """
        ${stream_name_under}_length = {fixed_length};"""
        template_stream_out_dynamic_length = """
{{indent}}${stream_name_under}_length = $ret['{stream_name_under}_length'];"""
        template_stream_out_chunk_offset_check = """
        if ($ret['{stream_name_under}_chunk_offset'] === (1 << {shift_size}) - 1) {{ // maximum chunk offset -> stream has no data
            ${stream_name_under}_length = 0;
            ${stream_name_under}_out_of_sync = false;
            ${stream_name_under}_data = array();
        }} else {{
            """
        template_stream_out_single_chunk = """
    /**
     * {doc}
     */
    public function {name}({high_level_parameters})
    {{
        $ret = $this->{name}LowLevel({parameters});
{result}
    }}
"""
        template_stream_out_result = """
        return array_slice(${stream_name_under}_data, 0, ${stream_name_under}_length);"""
        template_stream_out_single_chunk_result = """
        return array_slice($ret["{stream_name_under}_data"], 0, $ret["{stream_name_under}_length"]);"""
        template_stream_out_namedtuple_result = """
        return array({result_fields});"""

        for packet in self.get_packets('function'):
            stream_in = packet.get_high_level('stream_in')
            stream_out = packet.get_high_level('stream_out')

            if stream_in != None:
                if stream_in.get_fixed_length() != None:
                    template = template_stream_in_fixed_length
                elif stream_in.has_short_write() and stream_in.has_single_chunk():
                    # the single chunk template also covers short writes
                    template = template_stream_in_single_chunk
                elif stream_in.has_short_write():
                    template = template_stream_in_short_write
                elif stream_in.has_single_chunk():
                    template = template_stream_in_single_chunk
                else:
                    template = template_stream_in

                if stream_in.has_short_write():
                    if len(packet.get_elements(direction='out')) < 2:
                        chunk_written_0 = template_stream_in_short_write_chunk_written[0].format(stream_name_under=stream_in.get_name().under)
                        chunk_written_n = template_stream_in_short_write_chunk_written[1].format(stream_name_under=stream_in.get_name().under)
                        chunk_written_test = template_stream_in_short_write_chunk_written[2].format(stream_name_under=stream_in.get_name().under)
                    else:
                        chunk_written_0 = template_stream_in_short_write_namedtuple_chunk_written[0].format(stream_name_under=stream_in.get_name().under)
                        chunk_written_n = template_stream_in_short_write_namedtuple_chunk_written[1].format(stream_name_under=stream_in.get_name().under)
                        chunk_written_test = template_stream_in_short_write_namedtuple_chunk_written[2].format(stream_name_under=stream_in.get_name().under)

                    if stream_in.has_single_chunk():
                        result = template_stream_in_single_chunk_result.format(name=packet.get_name(skip=-2).headless,
                                                                               parameters=packet.get_php_parameters())
                    elif len(packet.get_elements(direction='out', high_level=True)) < 2:
                        result = template_stream_in_short_write_result.format(stream_name_under=stream_in.get_name().under)
                    else:
                        fields = []

                        for element in packet.get_elements(direction='out', high_level=True):
                            if element.get_role() == 'stream_written':
                                fields.append("'{0}_written' => ${0}_written".format(stream_in.get_name().under))
                            else:
                                fields.append("'{0}' => $ret['{0}']".format(element.get_name().under))

                        result = template_stream_in_short_write_namedtuple_result.format(result_fields=', '.join(fields))
                else:
                    chunk_written_0 = ''
                    chunk_written_n = ''
                    chunk_written_test = ''

                    if stream_in.has_single_chunk():
                        result = template_stream_in_single_chunk_result.format(name=packet.get_name(skip=-2).headless,
                                                                               parameters=packet.get_php_parameters())
                    else:
                        result = template_stream_in_result

                methods += template.format(doc=packet.get_php_formatted_doc([''] + packet.get_php_parameter_doc(high_level=True).split('\n')),
                                           name=packet.get_name(skip=-2).headless,
                                           parameters=packet.get_php_parameters(),
                                           high_level_parameters=packet.get_php_parameters(high_level=True),
                                           stream_name_space=stream_in.get_name().space,
                                           stream_name_under=stream_in.get_name().under,
                                           stream_max_length=abs(stream_in.get_data_element().get_cardinality()),
                                           fixed_length=stream_in.get_fixed_length(),
                                           chunk_cardinality=stream_in.get_chunk_data_element().get_cardinality(),
                                           chunk_padding=stream_in.get_chunk_data_element().get_php_default_item_value(),
                                           chunk_written_0=chunk_written_0,
                                           chunk_written_n=chunk_written_n,
                                           chunk_written_test=chunk_written_test,
                                           result=result)
            elif stream_out != None:
                if stream_out.get_fixed_length() != None:
                    fixed_length = template_stream_out_fixed_length.format(stream_name_under=stream_out.get_name().under,
                                                                           fixed_length=stream_out.get_fixed_length())
                    dynamic_length = ''
                    shift_size = int(stream_out.get_chunk_offset_element().get_type().replace('uint', ''))
                    chunk_offset_check = template_stream_out_chunk_offset_check.format(stream_name_under=stream_out.get_name().under,
                                                                                       shift_size=shift_size)
                    chunk_offset_check_indent = '    '
                    chunk_offset_check_end = '\n        }'
                else:
                    fixed_length = ''
                    dynamic_length = template_stream_out_dynamic_length.format(stream_name_under=stream_out.get_name().under)
                    chunk_offset_check = ''
                    chunk_offset_check_indent = ''
                    chunk_offset_check_end = ''

                if len(packet.get_elements(direction='out', high_level=True)) < 2:
                    if stream_out.has_single_chunk():
                        result = template_stream_out_single_chunk_result.format(stream_name_under=stream_out.get_name().under)
                    else:
                        result = template_stream_out_result.format(stream_name_under=stream_out.get_name().under)
                else:
                    fields = []

                    for element in packet.get_elements(direction='out', high_level=True):
                        if element.get_role() == 'stream_data':
                            if stream_out.has_single_chunk():
                                fields.append("'{0}' => array_slice($ret['{0}_data'], 0, $ret['{0}_length'])".format(stream_out.get_name().under))
                            else:
                                fields.append("'{0}' => array_slice(${0}_data, 0, ${0}_length)".format(stream_out.get_name().under))
                        else:
                            fields.append("'{0}' => $ret['{0}']".format(element.get_name().under))

                    result = template_stream_out_namedtuple_result.format(result_fields=', '.join(fields))

                if stream_out.has_single_chunk():
                    template = template_stream_out_single_chunk
                else:
                    template = template_stream_out

                methods += template.format(doc=packet.get_php_formatted_doc([''] + packet.get_php_parameter_doc(high_level=True).split('\n')),
                                           name=packet.get_name(skip=-2).headless,
                                           parameters=packet.get_php_parameters(),
                                           high_level_parameters=packet.get_php_parameters(high_level=True),
                                           stream_name_space=stream_out.get_name().space,
                                           stream_name_under=stream_out.get_name().under,
                                           fixed_length=fixed_length,
                                           dynamic_length_2=dynamic_length.format(indent='    ' * 2),
                                           dynamic_length_3=dynamic_length.format(indent='    ' * 3),
                                           dynamic_length_4=dynamic_length.format(indent='    ' * 4),
                                           chunk_offset_check=chunk_offset_check,
                                           chunk_offset_check_indent=chunk_offset_check_indent,
                                           chunk_offset_check_end=chunk_offset_check_end,
                                           chunk_cardinality=stream_out.get_chunk_data_element().get_cardinality(),
                                           result=result)

        return """
    /**
     * @internal
     * @param string $header
     * @param string $data
     */
    public function handleCallback($header, $data)
    {
        call_user_func(array($this, $this->callback_wrappers[$header['function_id']]), $data);
    }
""" + methods

    def get_php_callback_wrappers(self):
        if self.get_callback_count() == 0:
            return ''

        wrappers = """
    /**
     * Registers the given $function with the given $callback_id. The optional
     * $user_data will be passed as the last parameter to the $function.
     *
     * @param int $callback_id
     * @param callable $function
     * @param mixed $user_data
     *
     * @return void
     */
    public function registerCallback($callback_id, $function, $user_data = NULL)
    {
        if (!is_callable($function)) {
            throw new \\Exception('Function is not callable');
        }

        $this->registered_callbacks[$callback_id] = $function;
        $this->registered_callback_user_data[$callback_id] = $user_data;
    }
"""
        wrapper = """
    /**
     * @internal
     * @param string $data
     */
    public function callbackWrapper{0}($data)
    {{
{1}{4}{5}
        if (array_key_exists(self::CALLBACK_{3}, $this->registered_callbacks)) {{
            $function = $this->registered_callbacks[self::CALLBACK_{3}];
            $user_data = $this->registered_callback_user_data[self::CALLBACK_{3}];

            call_user_func($function, {2}$user_data);
        }}
    }}
"""

        template_stream_out = """
        $high_level_callback = &$this->high_level_callbacks[self::CALLBACK_{name_upper}];
        ${stream_name_under}_chunk_length = min({stream_length} - $payload['{stream_name_under}_chunk_offset'], {chunk_cardinality});

        if ($high_level_callback['data'] === NULL) {{ // no stream in-progress
            if ($payload['{stream_name_under}_chunk_offset'] === 0) {{ // stream starts
                $high_level_callback['data'] = array_slice($payload['{stream_name_under}_chunk_data'], 0, ${stream_name_under}_chunk_length);

                if (count($high_level_callback['data']) >= {stream_length}) {{ // stream complete
                    if (array_key_exists(self::CALLBACK_{name_upper}, $this->registered_callbacks)) {{
                        $function = $this->registered_callbacks[self::CALLBACK_{name_upper}];
                        $user_data = $this->registered_callback_user_data[self::CALLBACK_{name_upper}];
                        $payload['{stream_name_under}'] = $high_level_callback['data'];

                        call_user_func($function, {high_level_parameters}$user_data);
                    }}

                    $high_level_callback['data'] = NULL;
                }}
            }} else {{ // ignore tail of current stream, wait for next stream start
            }}
        }} else {{ // stream in-progress
            if ($payload['{stream_name_under}_chunk_offset'] !== count($high_level_callback['data'])) {{ // stream out-of-sync
                $high_level_callback['data'] = NULL;

                if (array_key_exists(self::CALLBACK_{name_upper}, $this->registered_callbacks)) {{
                    $function = $this->registered_callbacks[self::CALLBACK_{name_upper}];
                    $user_data = $this->registered_callback_user_data[self::CALLBACK_{name_upper}];
                    $payload['{stream_name_under}'] = $high_level_callback['data'];

                    call_user_func($function, {high_level_parameters}$user_data);
                }}
            }} else {{ // stream in-sync
                $high_level_callback['data'] = array_merge($high_level_callback['data'], array_slice($payload['{stream_name_under}_chunk_data'], 0, ${stream_name_under}_chunk_length));

                if (count($high_level_callback['data']) >= {stream_length}) {{ // stream complete
                    if (array_key_exists(self::CALLBACK_{name_upper}, $this->registered_callbacks)) {{
                        $function = $this->registered_callbacks[self::CALLBACK_{name_upper}];
                        $user_data = $this->registered_callback_user_data[self::CALLBACK_{name_upper}];
                        $payload['{stream_name_under}'] = $high_level_callback['data'];

                        call_user_func($function, {high_level_parameters}$user_data);
                    }}

                    $high_level_callback['data'] = NULL;
                }}
            }}
        }}
"""
        template_stream_out_single_chunk = """
        if (array_key_exists(self::CALLBACK_{name_upper}, $this->registered_callbacks)) {{
            $payload['${stream_name_under}'] = array_slice($payload['{stream_name_under}_data'], 0, $payload['{stream_name_under}_length']);
            $function = $this->registered_callbacks[self::CALLBACK_{name_upper}];
            $user_data = $this->registered_callback_user_data[self::CALLBACK_{name_upper}];

            call_user_func($function, {high_level_parameters}$user_data);
        }}
"""

        for packet in self.get_packets('callback'):
            name = packet.get_name().camel
            unpack_formats = []
            unpack_fixes = []
            result = []

            for element in packet.get_elements(direction='out'):
                name_under = element.get_name().under
                cardinality = element.get_cardinality()

                unpack_formats.append(element.get_php_unpack_format())

                unpack_fix = element.get_php_unpack_fix()

                if unpack_fix != None:
                    if cardinality > 1:
                        unpack_fixes.append("        $payload['{0}'] = {2}$payload{4}'{0}'{5}, {1}{3};".format(name_under, cardinality, *unpack_fix))
                    else:
                        unpack_fixes.append("        $payload['{0}'] = {1}$payload{3}'{0}'{4}{2};".format(name_under, *unpack_fix))

                result.append("$payload['{0}']".format(name_under))

            final_unpack = ''

            if len(unpack_formats) > 0:
                final_unpack = "        $payload = unpack('{0}', $data);\n".format('/'.join(unpack_formats))

            stream_out = packet.get_high_level('stream_out')

            if stream_out != None:
                if stream_out.has_single_chunk():
                    template = template_stream_out_single_chunk
                else:
                    template = template_stream_out

                high_level_handling = template.format(name_camel=packet.get_name(skip=-2).camel,
                                                      name_upper=packet.get_name(skip=-2).upper,
                                                      high_level_parameters=common.wrap_non_empty('', packet.get_php_parameters(context='callback_wrapper', high_level=True), ', '),
                                                      stream_name_under=stream_out.get_name().under,
                                                      stream_length=stream_out.get_fixed_length(default="$payload['{0}_length']".format(stream_out.get_name().under)),
                                                      chunk_cardinality=stream_out.get_chunk_data_element().get_cardinality())
            else:
                high_level_handling = ''

            wrappers += wrapper.format(name,
                                       final_unpack,
                                       common.wrap_non_empty('', packet.get_php_parameters(context='callback_wrapper'), ', '),
                                       packet.get_name().upper,
                                       common.wrap_non_empty('', '\n'.join(unpack_fixes), '\n'),
                                       high_level_handling)

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
        source += self.get_php_high_level_callbacks()
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

    def get_php_parameter_doc(self, high_level=False):
        param = []

        for element in self.get_elements(high_level=high_level):
            if element.get_direction() == 'out' or self.get_type() != 'function':
                continue

            php_type = element.get_php_type()

            if element.get_cardinality() != 1 and element.get_type() != 'string':
                param.append('@param {0}[] ${1}'.format(php_type, element.get_name().under))
            else:
                param.append('@param {0} ${1}'.format(php_type, element.get_name().under))

        param.append('\n@return ' + self.get_php_return_type())

        return '\n'.join(param)

class PHPBindingsGenerator(php_common.PHPGeneratorTrait, common.BindingsGenerator):
    def get_device_class(self):
        return PHPBindingsDevice

    def get_packet_class(self):
        return PHPBindingsPacket

    def get_element_class(self):
        return php_common.PHPElement

    def prepare(self):
        common.BindingsGenerator.prepare(self)

        self.device_display_names = []

    def generate(self, device):
        filename = '{0}.php'.format(device.get_php_class_name())

        with open(os.path.join(self.get_bindings_dir(), filename), 'w') as f:
            f.write(device.get_php_source())

        if device.is_released():
            self.device_display_names.append((device.get_device_identifier(), device.get_long_display_name()))
            self.released_files.append(filename)

    def finish(self):
        template = """<?php

{header}
namespace Tinkerforge;

/**
 * @internal
 */
function getDeviceDisplayName($device_identifier)
{{
	switch ($device_identifier) {{
	{cases}
	default: return "Unknown Device [$device_identifier]";
	}}
}}

?>
"""

        cases = []

        for device_identifier, device_display_name in sorted(self.device_display_names):
            cases.append("case {0}: return '{1}';".format(device_identifier, device_display_name))

        with open(os.path.join(self.get_bindings_dir(), 'DeviceDisplayNames.php'), 'w') as f:
            f.write(template.format(header=self.get_header_comment('asterisk'),
                                    cases='\n\t'.join(cases)))

        self.released_files.append('DeviceDisplayNames.php')

        common.BindingsGenerator.finish(self)

def generate(root_dir):
    common.generate(root_dir, 'en', PHPBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
