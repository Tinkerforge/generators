#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Bindings Generator
Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

generator_c_bindings.py: Generator for C/C++ bindings

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
import c_common

class CBindingsDevice(common.Device):
    def get_c_include_c(self):
        include = """{0}

#define IPCON_EXPOSE_INTERNALS

#include "{1}_{2}.h"

#include <string.h>

"""
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        version = common.get_changelog_version(self.get_generator().get_bindings_root_directory())

        return include.format(common.gen_text_star.format(date, *version),
                              self.get_category().lower(),
                              self.get_underscore_name())

    def get_c_function_id_defines(self):
        define_temp =  """
/**
 * \ingroup {4}{3}
 */
#define {0}_FUNCTION_{1} {2}
"""

        defines = ''
        for packet in self.get_packets('function'):
            defines += define_temp.format(self.get_upper_case_name(),
                                          packet.get_upper_case_name(),
                                          packet.get_function_id(),
                                          self.get_camel_case_name(),
                                          self.get_category())

        return defines

    def get_c_callback_defines(self):
        define_temp = """
/**
 * \ingroup {5}{4}
 *
 * {3}
 */
#define {0}_CALLBACK_{1} {2}
"""

        defines = ''
        for packet in self.get_packets('callback'):
            defines += define_temp.format(self.get_upper_case_name(),
                                          packet.get_upper_case_name(),
                                          packet.get_function_id(),
                                          packet.get_c_formatted_doc(),
                                          self.get_camel_case_name(),
                                          self.get_category())

        return defines

    def get_c_constants(self):
        str_constants = '\n'
        str_constant = """
/**
 * \ingroup {4}{3}
 */
#define {5}_{0}_{1} {2}
"""
        constants = self.get_constants()
        for constant in constants:
            for definition in constant.definitions:
                if constant.type == 'char':
                    value = "'{0}'".format(definition.value)
                else:
                    value = str(definition.value)

                str_constants += str_constant.format(constant.name_uppercase,
                                                     definition.name_uppercase,
                                                     value,
                                                     self.get_camel_case_name(),
                                                     self.get_category(),
                                                     self.get_upper_case_name())
        return str_constants

    def get_c_device_identifier_define(self):
        define_temp = """
/**
 * \ingroup {3}{2}
 *
 * This constant is used to identify a {2} {3}.
 *
 * The {{@link {4}_get_identity}} function and the
 * {{@link IPCON_CALLBACK_ENUMERATE}} callback of the IP Connection have a
 * \c device_identifier parameter to specify the Brick's or Bricklet's type.
 */
#define {0}_DEVICE_IDENTIFIER {1}
"""
        return define_temp.format(self.get_upper_case_name(),
                                  self.get_device_identifier(),
                                  self.get_camel_case_name(),
                                  self.get_category(),
                                  self.get_underscore_name())

    def get_c_structs(self):
        structs = """
#if defined _MSC_VER || defined __BORLANDC__
\t#pragma pack(push)
\t#pragma pack(1)
\t#define ATTRIBUTE_PACKED
#elif defined __GNUC__
\t#ifdef _WIN32
\t\t// workaround struct packing bug in GCC 4.7 on Windows
\t\t// http://gcc.gnu.org/bugzilla/show_bug.cgi?id=52991
\t\t#define ATTRIBUTE_PACKED __attribute__((gcc_struct, packed))
\t#else
\t\t#define ATTRIBUTE_PACKED __attribute__((packed))
\t#endif
#else
\t#error unknown compiler, do not know how to enable struct packing
#endif
"""

        struct_temp = """
typedef struct {{
\tPacketHeader header;
{0}}} ATTRIBUTE_PACKED {1}{2}_;
"""

        for packet in self.get_packets():
            if packet.get_type() == 'callback':
                cb = "Callback"
                struct_body = ''
                for element in packet.get_elements():
                    c_type = element.get_c_type(False)
                    if element.get_cardinality() > 1:
                        struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                                  element.get_underscore_name(),
                                                                  element.get_cardinality());
                    else:
                        struct_body += '\t{0} {1};\n'.format(c_type, element.get_underscore_name())

                structs += struct_temp.format(struct_body, packet.get_camel_case_name(), cb)
                continue

            struct_body = ''
            for element in packet.get_elements('in'):
                c_type = element.get_c_type(False)
                if element.get_cardinality() > 1:
                    struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                              element.get_underscore_name(),
                                                              element.get_cardinality());
                else:
                    struct_body += '\t{0} {1};\n'.format(c_type, element.get_underscore_name())

            structs += struct_temp.format(struct_body, packet.get_camel_case_name(), '')

            if len(packet.get_elements('out')) == 0:
                continue

            struct_body = ''
            for element in packet.get_elements('out'):
                c_type = element.get_c_type(False)
                if element.get_cardinality() > 1:
                    struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                              element.get_underscore_name(),
                                                              element.get_cardinality());
                else:
                    struct_body += '\t{0} {1};\n'.format(c_type, element.get_underscore_name())

            structs += struct_temp.format(struct_body, packet.get_camel_case_name(), 'Response')

        structs += """
#if defined _MSC_VER || defined __BORLANDC__
\t#pragma pack(pop)
#endif
#undef ATTRIBUTE_PACKED
"""
        return structs

    def get_c_create_function(self):
        func = """
void {0}_create({1} *{0}, const char *uid, IPConnection *ipcon) {{
\tDevicePrivate *device_p;

\tdevice_create({0}, uid, ipcon->p, {3}, {4}, {5});

\tdevice_p = {0}->p;
{2}
}}
"""

        cb_temp = """
\tdevice_p->callback_wrappers[{3}_CALLBACK_{1}] = {0}_callback_wrapper_{2};"""

        cbs = ''
        dev_name = self.get_underscore_name()
        for packet in self.get_packets('callback'):
            type_name = packet.get_underscore_name()
            cbs += cb_temp.format(dev_name, type_name.upper(), type_name, dev_name.upper())

        response_expected = ''

        for packet in self.get_packets():
            if packet.get_type() == 'callback':
                prefix = 'CALLBACK'
                flag = 'DEVICE_RESPONSE_EXPECTED_ALWAYS_FALSE'
            elif len(packet.get_elements('out')) > 0:
                prefix = 'FUNCTION'
                flag = 'DEVICE_RESPONSE_EXPECTED_ALWAYS_TRUE'
            elif packet.get_doc()[0] == 'ccf':
                prefix = 'FUNCTION'
                flag = 'DEVICE_RESPONSE_EXPECTED_TRUE'
            else:
                prefix = 'FUNCTION'
                flag = 'DEVICE_RESPONSE_EXPECTED_FALSE'

            response_expected += '\tdevice_p->response_expected[{1}_{2}_{3}] = {4};\n' \
                .format(dev_name, self.get_upper_case_name(), prefix, packet.get_upper_case_name(), flag)

        if len(response_expected) > 0:
            response_expected = '\n' + response_expected

        return func.format(dev_name,
                           self.get_camel_case_name(),
                           response_expected + cbs,
                           *self.get_api_version())

    def get_c_destroy_function(self):
        function = """
void {0}_destroy({1} *{0}) {{
\tdevice_destroy({0});
}}
"""
        return function.format(self.get_underscore_name(),
                               self.get_camel_case_name())

    def get_c_response_expected_functions(self):
        function = """
int {0}_get_response_expected({1} *{0}, uint8_t function_id, bool *ret_response_expected) {{
\treturn device_get_response_expected({0}->p, function_id, ret_response_expected);
}}

int {0}_set_response_expected({1} *{0}, uint8_t function_id, bool response_expected) {{
\treturn device_set_response_expected({0}->p, function_id, response_expected);
}}

int {0}_set_response_expected_all({1} *{0}, bool response_expected) {{
\treturn device_set_response_expected_all({0}->p, response_expected);
}}
"""
        return function.format(self.get_underscore_name(),
                              self.get_camel_case_name())

    def get_c_method_functions(self):
        function_version = """
int {0}_get_api_version({1} *{0}, uint8_t ret_api_version[3]) {{
\treturn device_get_api_version({0}->p, ret_api_version);
}}
"""

        function = """
int {0}_{1}({2} *{0}{3}) {{
\tDevicePrivate *device_p = {0}->p;
\t{5}_ request;{6}
\tint ret;{9}

\tret = packet_header_create(&request.header, sizeof(request), {4}, device_p->ipcon_p, device_p);

\tif (ret < 0) {{
\t\treturn ret;
\t}}
{7}

\tret = device_send_request(device_p, (Packet *)&request, {10});
{8}

\treturn ret;
}}
"""

        function_ret = """
\tif (ret < 0) {{
\t\treturn ret;
\t}}
{2}
"""

        device_name = self.get_underscore_name()
        c = self.get_camel_case_name()

        functions = ''
        for packet in self.get_packets('function'):
            packet_name = packet.get_underscore_name()
            params = packet.get_c_parameter_list()
            fid = '{0}_FUNCTION_{1}'.format(self.get_upper_case_name(),
                                            packet.get_upper_case_name())
            f = packet.get_camel_case_name()
            h, needs_i = packet.get_c_struct_list()
            if len(packet.get_elements('out')) > 0:
                g = '\n\t' + f + 'Response_ response;'
                rl, needs_i2 = packet.get_c_return_list()
                i = function_ret.format(f, device_name, rl)
                r = '(Packet *)&response'
            else:
                g = ''
                i = ''
                needs_i2 = False
                r = 'NULL'
            if needs_i or needs_i2:
                k = '\n\tint i;'
            else:
                k = ''

            functions += function.format(device_name, packet_name, c, params, fid, f, g, h, i, k, r)

        return function_version.format(device_name, c) + functions

    def get_c_register_callback_function(self):
        function = """
void {0}_register_callback({1} *{0}, uint8_t id, void *callback, void *user_data) {{
\tdevice_register_callback({0}->p, id, callback, user_data);
}}
"""
        return function.format(self.get_underscore_name(), self.get_camel_case_name())

    def get_c_callback_wrapper_functions(self):
        function = """
static void {0}_callback_wrapper_{1}(DevicePrivate *device_p, Packet *packet) {{
\t{3}CallbackFunction callback_function;
\tvoid *user_data = device_p->registered_callback_user_data[{7}];{9}{8}
\t*(void **)(&callback_function) = device_p->registered_callbacks[{7}];

\tif (callback_function == NULL) {{
\t\treturn;
\t}}
{6}
\tcallback_function({5}{4}user_data);
}}
"""

        functions = ''
        for packet in self.get_packets('callback'):
            a = self.get_underscore_name()
            b = packet.get_underscore_name()
            c = self.get_camel_case_name()
            d = packet.get_camel_case_name()
            e = ''
            f_list = []
            for element in packet.get_elements():
                f_list.append("callback->{0}".format(element.get_underscore_name()))
            f = ', '.join(f_list)
            if len(f_list) > 0:
                e = ', '
            endian_list = []
            i = ''
            for element in packet.get_elements():
                if element.get_item_size() > 1:
                    if element.get_cardinality() > 1:
                        i = '\n\tint i;'
                        endian_list.append('\tfor (i = 0; i < {2}; i++) callback->{0}[i] = leconvert_{1}_from(callback->{0}[i]);' \
                                           .format(element.get_underscore_name(), element.get_type(), element.get_cardinality()))
                    else:
                        endian_list.append('\tcallback->{0} = leconvert_{1}_from(callback->{0});'.format(element.get_underscore_name(), element.get_type()))
            endian = '\n'.join(endian_list)
            if len(endian) > 0:
                endian = '\n' + endian + '\n'
            fid = '{0}_CALLBACK_{1}'.format(self.get_upper_case_name(),
                                            packet.get_upper_case_name())
            if len(f_list) > 0:
                cb = '\n\t{0}Callback_ *callback = ({0}Callback_ *)packet;'.format(d)
            else:
                cb = '\n\t(void)packet;'

            functions += function.format(a, b, c, d, e, f, endian, fid, cb, i)

        return functions

    def get_c_include_h(self):
        include = """{0}
#ifndef {1}_{2}_H
#define {1}_{2}_H

#include "ip_connection.h"

/**
 * \defgroup {4}{3} {3} {4}
 */

/**
 * \ingroup {4}{3}
 *
 * {5}
 */
typedef Device {3};
"""

        date = datetime.datetime.now().strftime("%Y-%m-%d")
        version = common.get_changelog_version(self.get_generator().get_bindings_root_directory())
        upper_type = self.get_category().upper()
        upper_name = self.get_upper_case_name()

        return include.format(common.gen_text_star.format(date, *version),
                              upper_type,
                              upper_name,
                              self.get_camel_case_name(),
                              self.get_category(),
                              self.get_description())

    def get_c_end_h(self):
        return "\n#endif\n"

    def get_c_typedefs(self):
        typedef = """
typedef void (*{0}CallbackFunction)({1});
"""

        typedefs = '\n'

        for packet in self.get_packets('callback'):
            name = packet.get_camel_case_name()
            c_type_list = []

            for element in packet.get_elements():
                if element.get_cardinality() > 1:
                    c_type_list.append('{0}[{1}]'.format(element.get_c_type(True), element.get_cardinality()))
                else:
                    c_type_list.append(element.get_c_type(True))

            typedefs += typedef.format(name, ', '.join(c_type_list + ['void *']))

        return typedefs

    def get_c_create_declaration(self):
        create = """
/**
 * \ingroup {2}{1}
 *
 * Creates the device object \c {0} with the unique device ID \c uid and adds
 * it to the IPConnection \c ipcon.
 */
void {0}_create({1} *{0}, const char *uid, IPConnection *ipcon);
"""
        return create.format(self.get_underscore_name(),
                             self.get_camel_case_name(),
                             self.get_category())

    def get_c_destroy_declaration(self):
        destroy = """
/**
 * \ingroup {2}{1}
 *
 * Removes the device object \c {0} from its IPConnection and destroys it.
 * The device object cannot be used anymore afterwards.
 */
void {0}_destroy({1} *{0});
"""
        return destroy.format(self.get_underscore_name(),
                              self.get_camel_case_name(),
                              self.get_category())

    def get_c_response_expected_declarations(self):
        response_expected = """
/**
 * \ingroup {2}{1}
 *
 * Returns the response expected flag for the function specified by the
 * \c function_id parameter. It is *true* if the function is expected to
 * send a response, *false* otherwise.
 *
 * For getter functions this is enabled by default and cannot be disabled,
 * because those functions will always send a response. For callback
 * configuration functions it is enabled by default too, but can be disabled
 * via the {0}_set_response_expected function. For setter functions it is
 * disabled by default and can be enabled.
 *
 * Enabling the response expected flag for a setter function allows to
 * detect timeouts and other error conditions calls of this setter as well.
 * The device will then send a response for this purpose. If this flag is
 * disabled for a setter function then no response is send and errors are
 * silently ignored, because they cannot be detected.
 */
int {0}_get_response_expected({1} *{0}, uint8_t function_id, bool *ret_response_expected);

/**
 * \ingroup {2}{1}
 *
 * Changes the response expected flag of the function specified by the
 * \c function_id parameter. This flag can only be changed for setter
 * (default value: *false*) and callback configuration functions
 * (default value: *true*). For getter functions it is always enabled and
 * callbacks it is always disabled.
 *
 * Enabling the response expected flag for a setter function allows to detect
 * timeouts and other error conditions calls of this setter as well. The device
 * will then send a response for this purpose. If this flag is disabled for a
 * setter function then no response is send and errors are silently ignored,
 * because they cannot be detected.
 */
int {0}_set_response_expected({1} *{0}, uint8_t function_id, bool response_expected);

/**
 * \ingroup {2}{1}
 *
 * Changes the response expected flag for all setter and callback configuration
 * functions of this device at once.
 */
int {0}_set_response_expected_all({1} *{0}, bool response_expected);
"""
        return response_expected.format(self.get_underscore_name(),
                                        self.get_camel_case_name(),
                                        self.get_category())

    def get_c_method_declarations(self):
        func_version = """
/**
 * \ingroup {2}{1}
 *
 * Returns the API version (major, minor, release) of the bindings for this
 * device.
 */
int {0}_get_api_version({1} *{0}, uint8_t ret_api_version[3]);
"""
        func = """
/**
 * \ingroup {5}{2}
 *
 * {4}
 */
int {0}_{1}({2} *{0}{3});
"""

        a = self.get_underscore_name()
        c = self.get_camel_case_name()

        funcs = ''
        for packet in self.get_packets('function'):
            b = packet.get_underscore_name()
            d = packet.get_c_parameter_list()
            doc = packet.get_c_formatted_doc()

            funcs += func.format(a, b, c, d, doc, self.get_category())

        return func_version.format(a, c, self.get_category()) + funcs

    def get_c_register_callback_declaration(self):
        if self.get_callback_count() == 0:
            return '\n'

        func = """
/**
 * \ingroup {2}{1}
 *
 * Registers a callback with ID \c id to the function \c callback. The
 * \c user_data will be given as a parameter of the callback.
 */
void {0}_register_callback({1} *{0}, uint8_t id, void *callback, void *user_data);
"""
        return func.format(self.get_underscore_name(), self.get_camel_case_name(), self.get_category())

    def get_c_source(self):
        source  = self.get_c_include_c()
        source += self.get_c_typedefs()
        source += self.get_c_structs()
        source += self.get_c_callback_wrapper_functions()
        source += self.get_c_create_function()
        source += self.get_c_destroy_function()
        source += self.get_c_response_expected_functions()
        source += self.get_c_register_callback_function()
        source += self.get_c_method_functions()

        return source

    def get_c_header(self):
        header  = self.get_c_include_h()
        header += self.get_c_function_id_defines()
        header += self.get_c_callback_defines()
        header += self.get_c_constants()
        header += self.get_c_device_identifier_define()
        header += self.get_c_create_declaration()
        header += self.get_c_destroy_declaration()
        header += self.get_c_response_expected_declarations()
        header += self.get_c_register_callback_declaration()
        header += self.get_c_method_declarations()
        header += self.get_c_end_h()

        return header

class CBindingsPacket(c_common.CPacket):
    def get_c_formatted_doc(self):
        text = common.select_lang(self.get_doc()[1])
        link = '{{@link {0}_{1}}}'
        link_c = '{{@link {0}_CALLBACK_{1}}}'

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

        for other_packet in self.get_device().get_packets():
            name_false = ':func:`{0}`'.format(other_packet.get_camel_case_name())
            if other_packet.get_type() == 'callback':
                name = other_packet.get_upper_case_name()
                name_right = link_c.format(self.get_device().get_upper_case_name(), name)
            else:
                name = other_packet.get_underscore_name()
                name_right = link.format(self.get_device().get_underscore_name(), name)

            text = text.replace(name_false, name_right)

        if self.get_type() == 'callback':
            plist = self.get_c_parameter_list()[2:].replace('*ret_', '')
            if len(plist) > 0:
                plist += ', '
            text = 'Signature: \code void callback({0}void *user_data) \endcode\n'.format(plist) + text

        text = text.replace('.. note::', '\\note')
        text = text.replace('.. warning::', '\\warning')

        text = common.handle_rst_word(text)
        text = common.handle_rst_if(text, self.get_device())
        text += common.format_since_firmware(self.get_device(), self)

        return '\n * '.join(text.strip().split('\n'))

    def get_c_struct_list(self):
        struct_list = ''
        needs_i = False

        for element in self.get_elements('in'):
            sf = 'request'

            if element.get_type() == 'string':
                temp = '\n\tstrncpy({0}.{1}, {1}, {2});\n'
                struct_list += temp.format(sf, element.get_underscore_name(), element.get_cardinality())
            elif element.get_cardinality() > 1:
                if element.get_item_size() > 1:
                    needs_i = True
                    struct_list += '\n\tfor (i = 0; i < {3}; i++) {0}.{1}[i] = leconvert_{2}_to({1}[i]);' \
                                   .format(sf, element.get_underscore_name(), element.get_type(), element.get_cardinality())
                else:
                    temp = '\n\tmemcpy({0}.{1}, {1}, {2} * sizeof({3}));'
                    struct_list += temp.format(sf,
                                               element.get_underscore_name(),
                                               element.get_cardinality(),
                                               element.get_c_type(False))
            elif element.get_item_size() > 1:
                struct_list += '\n\t{0}.{1} = leconvert_{2}_to({1});'.format(sf, element.get_underscore_name(), element.get_type())
            else:
                struct_list += '\n\t{0}.{1} = {1};'.format(sf, element.get_underscore_name())

        return struct_list, needs_i

    def get_c_return_list(self):
        return_list = ''
        needs_i = False

        for element in self.get_elements('out'):
            sf = 'response'

            if element.get_type() == 'string':
                temp = '\tstrncpy(ret_{0}, {1}.{0}, {2});\n'
                return_list += temp.format(element.get_underscore_name(), sf, element.get_cardinality())
            elif element.get_cardinality() > 1:
                if element.get_item_size() > 1:
                    needs_i = True
                    return_list += '\tfor (i = 0; i < {3}; i++) ret_{0}[i] = leconvert_{2}_from({1}.{0}[i]);\n' \
                                   .format(element.get_underscore_name(), sf, element.get_type(), element.get_cardinality())
                else:
                    temp = '\tmemcpy(ret_{0}, {1}.{0}, {2} * sizeof({3}));\n'
                    return_list += temp.format(element.get_underscore_name(),
                                               sf,
                                               element.get_cardinality(),
                                               element.get_c_type(False))
            elif element.get_item_size() > 1:
                return_list += '\t*ret_{0} = leconvert_{2}_from({1}.{0});\n'.format(element.get_underscore_name(), sf, element.get_type())
            else:
                return_list += '\t*ret_{0} = {1}.{0};\n'.format(element.get_underscore_name(), sf)

        return return_list, needs_i

class CBindingsGenerator(common.BindingsGenerator):
    def __init__(self, *args, **kwargs):
        common.BindingsGenerator.__init__(self, *args, **kwargs)

        self.released_files_name_prefix = 'c'

    def get_device_class(self):
        return CBindingsDevice

    def get_packet_class(self):
        return CBindingsPacket

    def get_element_class(self):
        return c_common.CElement

    def generate(self, device):
        file_name = '{0}_{1}'.format(device.get_category().lower(), device.get_underscore_name())

        c = open(os.path.join(self.get_bindings_root_directory(), 'bindings', file_name + '.c'), 'wb')
        c.write(device.get_c_source())
        c.close()

        h = open(os.path.join(self.get_bindings_root_directory(), 'bindings', file_name + '.h'), 'wb')
        h.write(device.get_c_header())
        h.close()

        if device.is_released():
            self.released_files.append(file_name + '.c')
            self.released_files.append(file_name + '.h')

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', CBindingsGenerator, False)

if __name__ == "__main__":
    generate(os.getcwd())
