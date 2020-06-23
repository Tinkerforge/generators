#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Co-MCU Firmware Stubs Generator
Copyright (C) 2019 Olaf Lüke <olaf@tinkerforge.com>

generate_tng_stubs.py: Generator for communication API stubs
                       for TNG modules

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

if sys.hexversion < 0x3050000:
    print('Python >= 3.5 required')
    sys.exit(1)

import os
import datetime
import shutil
import math
import importlib.util

def create_generators_module():
    generators_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
    generators_spec = importlib.util.spec_from_file_location('generators', os.path.join(generators_dir, '__init__.py'))
    generators_module = importlib.util.module_from_spec(generators_spec)

    generators_spec.loader.exec_module(generators_module)

    sys.modules['generators'] = generators_module

if 'generators' not in sys.modules:
    create_generators_module()

from generators import common
from generators.c import c_common

class TNGStubDevice(common.Device):
    def get_h_constants(self):
        constant_format = '#define {device_name}_{constant_group_name}_{constant_name} {constant_value}'
        constants = []

        for i, constant_group in enumerate(self.get_constant_groups()):
            if constant_group.is_virtual():
                continue

            if i != 0:
                constants.append('')

            for constant in constant_group.get_constants():
                if constant_group.get_type() == 'char':
                    value = "'{0}'".format(constant.get_value())
                elif constant_group.get_type() == 'bool':
                    value = str(constant.get_value()).lower()
                else:
                    value = str(constant.get_value())

                constants.append(constant_format.format(device_name=self.get_name().upper,
                                                        constant_group_name=constant_group.get_name().upper,
                                                        constant_name=constant.get_name().upper,
                                                        constant_value=value))

        return constants

    def get_h_defines(self):
        define_function =  '#define FID_{0} {1}'
        define_callback =  '#define FID_CALLBACK_{0} {1}'

        defines = []
        for packet in self.get_packets('function'):
            if packet.get_function_id() < 200:
                defines.append(define_function.format(packet.get_name().upper, packet.get_function_id()))

        defines.append('')
        for packet in self.get_packets('callback'):
            if packet.get_function_id() < 200:
                defines.append(define_callback.format(packet.get_name().upper, packet.get_function_id()))

        return defines

    def get_h_structs(self):
        struct_temp = """typedef struct {{
\tTFPMessageHeader header;
{0}}} __attribute__((__packed__)) {1}{2};
"""

        structs = []
        for packet in self.get_packets():
            if packet.get_function_id() < 200 and not packet.is_part_of_callback_value():
                if packet.get_type() == 'callback':
                    struct_body = ''
                    for element in packet.get_elements():
                        c_type = element.get_c_type('default')
                        cardinality = element.get_cardinality()
                        if cardinality > 1:
                            if c_type == 'bool':
                                c_type = 'uint8_t'
                                cardinality = int(math.ceil(cardinality/8.0))
                            struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                                      element.get_name().under,
                                                                      cardinality);
                        else:
                            struct_body += '\t{0} {1};\n'.format(c_type, element.get_name().under)

                    structs.append(struct_temp.format(struct_body, packet.get_name().camel, '_Callback'))
                    continue

                struct_body = ''

                for element in packet.get_elements(direction='in'):
                    c_type = element.get_c_type('default')

                    cardinality = element.get_cardinality()
                    if cardinality > 1:
                        if c_type == 'bool':
                            c_type = 'uint8_t'
                            cardinality = int(math.ceil(cardinality/8.0))
                        struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                                  element.get_name().under,
                                                                  cardinality);
                    else:
                        struct_body += '\t{0} {1};\n'.format(c_type, element.get_name().under)

                structs.append(struct_temp.format(struct_body, packet.get_name().camel, ''))

                if len(packet.get_elements(direction='out')) == 0:
                    continue

                struct_body = ''

                for element in packet.get_elements(direction='out'):
                    c_type = element.get_c_type('default')

                    cardinality = element.get_cardinality()
                    if cardinality > 1:
                        if c_type == 'bool':
                            c_type = 'uint8_t'
                            cardinality = int(math.ceil(cardinality/8.0))

                        struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                                  element.get_name().under,
                                                                  cardinality);
                    else:
                        struct_body += '\t{0} {1};\n'.format(c_type, element.get_name().under)

                structs.append(struct_temp.format(struct_body, packet.get_name().camel, '_Response'))

        return structs

    def get_h_function_prototypes(self):
        prototype =  'TNGHandleMessageResponse {0}(const {1} *data);'
        prototype_with_response =  'TNGHandleMessageResponse {0}(const {1} *data, {2} *response);'
        prototypes = []

        for packet in self.get_packets('function'):
            if packet.get_function_id() < 200 and not packet.is_part_of_callback_value():
                if len(packet.get_elements(direction='out')) == 0:
                    prototypes.append(prototype.format(packet.get_name().under, packet.get_name().camel))
                else:
                    prototypes.append(prototype_with_response.format(packet.get_name().under, packet.get_name().camel, packet.get_name().camel + '_Response'))

        return prototypes

    def get_h_callback_prototypes(self):
        prototype = 'bool handle_{0}_callback(void);'

        prototypes = []
        for packet in self.get_packets('callback'):
            if packet.get_function_id() < 200:
                prototypes.append(prototype.format(packet.get_name().under))

        return prototypes

    def get_h_callback_list(self):
        callback_tick_wait_ms = '#define COMMUNICATION_CALLBACK_TICK_WAIT_MS {0}'
        callback_tick_handler_num = '#define COMMUNICATION_CALLBACK_HANDLER_NUM {0}'
        callback = '\thandle_{0}_callback, \\'

        num = 0
        for packet in self.get_packets('callback'):
            if packet.get_function_id() < 200:
                num += 1

        callback_list = []
        callback_list.append(callback_tick_wait_ms.format(1))
        callback_list.append(callback_tick_handler_num.format(num))
        callback_list.append('#define COMMUNICATION_CALLBACK_LIST_INIT \\')

        for packet in self.get_packets('callback'):
            if packet.get_function_id() < 200:
                callback_list.append(callback.format(packet.get_name().under))

        return callback_list

    def get_c_cases(self):
        case =  '\t\tcase FID_{0}: return {1}(message);'
        case_with_response = '\t\tcase FID_{0}: return {1}(message, response);'
        case_cv =  '\t\tcase FID_{0}: return {1}_{2}(message, &callback_value_{3});'
        case_cv_with_response = '\t\tcase FID_{0}: return {1}_{2}(message, response, &callback_value_{3});'
        cases = []

        for packet in self.get_packets('function'):
            if packet.get_function_id() < 200:
                if packet.is_part_of_callback_value():
                    c_type = packet.get_elements()[-1].get_c_type('default')

                    if not 'corresponding_getter' in packet.raw_data:
                        callback_value_function_name = 'get_callback_value'
                    elif packet.raw_data['name'].startswith('Get '):
                        callback_value_function_name = 'get_callback_value_callback_configuration'
                    else:
                        callback_value_function_name = 'set_callback_value_callback_configuration'

                    if len(packet.get_elements(direction='out')) == 0:
                        cases.append(case_cv.format(packet.get_name().upper, callback_value_function_name, c_type, packet.get_callback_value_name()))
                    else:
                        cases.append(case_cv_with_response.format(packet.get_name().upper, callback_value_function_name, c_type, packet.get_callback_value_name()))
                else:
                    if len(packet.get_elements(direction='out')) == 0:
                        cases.append(case.format(packet.get_name().upper, packet.get_name().under))
                    else:
                        cases.append(case_with_response.format(packet.get_name().upper, packet.get_name().under))

        return cases

    def get_c_functions(self):
        function_with_response = """TNGHandleMessageResponse {0}(const {1} *data, {2} *response) {{
\tresponse->header.length = sizeof({2});

\treturn HANDLE_MESSAGE_RESPONSE_NEW_MESSAGE;
}}
"""

        function = """TNGHandleMessageResponse {0}(const {1} *data) {{

\treturn HANDLE_MESSAGE_RESPONSE_EMPTY;
}}
"""
        functions = []

        for packet in self.get_packets('function'):
            if packet.get_function_id() < 200 and not packet.is_part_of_callback_value():
                if len(packet.get_elements(direction='out')) == 0:
                    functions.append(function.format(packet.get_name().under, packet.get_name().camel))
                else:
                    functions.append(function_with_response.format(packet.get_name().under, packet.get_name().camel, packet.get_name().camel + '_Response'))

        return functions

    def get_c_callbacks(self):
        callback = """
bool handle_{0}_callback(void) {{
\tstatic bool is_buffered = false;
\tstatic {1}_Callback cb;

\tif(!is_buffered) {{
\t\ttfp_make_default_header(&cb.header, tng_get_uid(), sizeof({1}_Callback), FID_CALLBACK_{2});
\t\t// TODO: Implement {1} callback handling

\t\treturn false;
\t}}

\tif(usb_send((uint8_t*)&cb, sizeof({1}_Callback))) {{
\t\tis_buffered = false;
\t\treturn true;
\t}} else {{
\t\tis_buffered = true;
\t}}

\treturn false;
}}"""

        callback_cv = """
bool handle_{0}_callback(void) {{
\treturn handle_callback_value_callback_{1}(&callback_value_{2}, FID_CALLBACK_{3});
}}"""

        callbacks = []
        for packet in self.get_packets('callback'):
            if packet.get_function_id() < 200:
                if packet.is_part_of_callback_value():
                    c_type = packet.get_elements()[-1].get_c_type('default')
                    callbacks.append(callback_cv.format(packet.get_name().under, c_type, packet.get_callback_value_name(), packet.get_name().upper))
                else:
                    callbacks.append(callback.format(packet.get_name().under, packet.get_name().camel, packet.get_name().upper))

        return callbacks

    def get_c_callback_value_include(self):
        callback_values = set()
        for packet in self.get_packets('function'):
            if packet.get_function_id() < 200 and packet.is_part_of_callback_value():
                c_type = packet.get_elements()[-1].get_c_type('default')
                callback_values.add((c_type, packet.get_callback_value_name()))

        if len(callback_values) == 0:
            return ''

        cv = """#include "bricklib2/utility/callback_value.h"

{0}
"""
        cv_declaration = ''
        for callback_value in callback_values:
            cv_declaration += 'CallbackValue_{0} callback_value_{1};\n'.format(*callback_value)

        return cv.format(cv_declaration)

    def get_c_callback_value_init(self):
        callback_values = set()
        for packet in self.get_packets('function'):
            if packet.get_function_id() < 200 and packet.is_part_of_callback_value():
                c_type = packet.get_elements()[-1].get_c_type('default')
                callback_values.add((c_type, packet.get_callback_value_name()))

        if len(callback_values) == 0:
            return ''

        cv = """\t// TODO: Add proper functions
{0}
"""
        cv_declaration = ''
        for callback_value in callback_values:
            cv_declaration += '\tcallback_value_init_{0}(&callback_value_{1}, NULL);;\n'.format(*callback_value)

        return cv.format(cv_declaration)

class TNGStubGenerator(common.Generator):
    c_file = """/* tng-{0}
 * Copyright (C) {1} {2} <{3}>
 *
 * communication.c: TFP protocol message handling
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

#include "communication.h"

#include "bricklib2/utility/communication_callback.h"
#include "bricklib2/protocols/tfp/tfp.h"
#include "bricklib2/tng/usb_stm32/usb.h
{7}
TNGHandleMessageResponse handle_message(const void *message, void *response) {{
\tswitch(tfp_get_fid_from_message(message)) {{
{4}
\t\tdefault: return HANDLE_MESSAGE_RESPONSE_NOT_SUPPORTED;
\t}}
}}


{5}


{6}

void communication_tick(void) {{
\tcommunication_callback_tick();
}}

void communication_init(void) {{
{8}\tcommunication_callback_init();
}}
"""
    h_file = """/* tng-{0}
 * Copyright (C) {1} {2} <{3}>
 *
 * communication.h: TFP protocol message handling
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

#ifndef COMMUNICATION_H
#define COMMUNICATION_H

#include <stdint.h>
#include <stdbool.h>

#include "bricklib2/protocols/tfp/tfp.h"
#include "bricklib2/tng/tng.h"

// Default functions
TNGHandleMessageResponse handle_message(const void *data, void *response);
void communication_tick(void);
void communication_init(void);

// Constants
{4}

// Function and callback IDs and structs
{5}

{6}

// Function prototypes
{7}

// Callbacks
{8}

{9}


#endif
"""

    def get_bindings_name(self):
        return 'stubs'

    def get_bindings_display_name(self):
        return 'Co-MCU Firmware Stubs'

    def get_device_class(self):
        return TNGStubDevice

    def get_packet_class(self):
        return c_common.CPacket

    def get_element_class(self):
        return c_common.CElement

    def get_doc_null_value_name(self):
        return 'NULL'

    def get_doc_formatted_param(self, element):
        return element.get_name().under

    def copy_templates_to(self, folder_dst):
        folder_src = os.path.join(self.get_root_dir(), 'tng_templates')
        shutil.copytree(os.path.join(folder_src, 'software'), os.path.join(folder_dst, 'software'))
        shutil.copy(os.path.join(folder_src, '.gitignore'), os.path.join(folder_dst))
        shutil.copy(os.path.join(folder_src, 'README.rst'), os.path.join(folder_dst))

        if os.path.isdir(os.path.join(folder_src, 'hardware')):
            shutil.copytree(os.path.join(folder_src, 'hardware'),  os.path.join(folder_dst, 'hardware'))
        else:
            os.mkdir(os.path.join(folder_dst, 'hardware'))

        if os.path.isdir(os.path.join(folder_src, 'datasheets')):
            shutil.copytree(os.path.join(folder_src, 'datasheets'),  os.path.join(folder_dst, 'datasheets'))
        else:
            os.mkdir(os.path.join(folder_dst, 'datasheets'))

    # FIXME: use specialize_template instead
    def fill_templates(self, folder, device_name_dash, device_name_display, device_identifier, year, name, email, callback_value_define):
        for dname, dirs, files in os.walk(folder):
            for fname in files:
                fpath = os.path.join(dname, fname)
                with open(fpath, "r") as f:
                    s = f.read()

                device_name_display_readme = device_name_display + '\n' + '='*len(device_name_display)

                s = s.replace("""<<<DEVICE_NAME_DASH>>>""", device_name_dash)
                s = s.replace("""<<<DEVICE_NAME_READABLE>>>""", device_name_display)
                s = s.replace("""<<<DEVICE_NAME_READABLE_README>>>""", device_name_display_readme)
                s = s.replace("""<<<DEVICE_IDENTIFIER>>>""", str(device_identifier))
                s = s.replace("""<<<YEAR>>>""", str(year))
                s = s.replace("""<<<NAME>>>""", name)
                s = s.replace("""<<<EMAIL>>>""", email)
                s = s.replace("""<<<CALLBACK_VALUE_DEFINE>>>""", callback_value_define)
                with open(fpath, "w") as f:
                    f.write(s)

    def prepare(self):
        if self.get_config_name().space == 'Tinkerforge':
            name = 'tng'
        else:
            name = 'tng_' + self.get_config_name().under

        common.recreate_dir(os.path.join(self.get_root_dir(), name))

    def generate(self, device):
        if not device.is_tng():
            return

        folder = os.path.join(self.get_root_dir(), 'tng', device.get_name().dash)
        device_name_dash = device.get_name().dash
        year = datetime.datetime.now().year
        name = device.get_author().split("<")[0].rstrip()             #author syntax: Firstname Lastname <email>
        email = device.get_author().split("<")[1].replace(">","")
        callback_value_define = ''

        if device.has_callback_value():
            c_type = 'FIXME'
            for packet in device.get_packets('function'):
                if packet.get_function_id() < 200:
                    if packet.is_part_of_callback_value():
                        c_type = packet.get_elements()[-1].get_c_type('default')
                        break

            callback_value_define = """\n#define CALLBACK_VALUE_TYPE CALLBACK_VALUE_TYPE_{0}\n""".format(c_type.replace('_t', '').upper())

        self.copy_templates_to(folder)
        self.fill_templates(folder, device_name_dash, device.get_long_display_name(), device.get_device_identifier(), year, name, email, callback_value_define)

        h_constants = device.get_h_constants()
        h_defines = device.get_h_defines()
        h_structs = device.get_h_structs()
        h_function_prototypes = device.get_h_function_prototypes()
        h_callback_prototypes = device.get_h_callback_prototypes()
        h_callback_list = device.get_h_callback_list()
        c_cases = device.get_c_cases()
        c_functions = device.get_c_functions()
        c_callbacks = device.get_c_callbacks()

        h_constants_string = '\n'.join(h_constants)
        h_defines_string = '\n'.join(h_defines)
        h_structs_string = '\n'.join(h_structs)
        h_function_prototypes_string = '\n'.join(h_function_prototypes)
        h_callback_prototypes_string = '\n'.join(h_callback_prototypes)
        h_callback_list_string = '\n'.join(h_callback_list)
        c_cases_string = '\n'.join(c_cases)
        c_functions_string = '\n'.join(c_functions)
        c_callbacks_string = '\n'.join(c_callbacks)
        c_callback_value_include_string = device.get_c_callback_value_include()
        c_callback_value_init_string = device.get_c_callback_value_init()

        with open(os.path.join(folder, 'software', 'src', 'communication.c'), 'w') as c:
            c.write(self.c_file.format(device_name_dash, year, name, email, c_cases_string, c_functions_string, c_callbacks_string, c_callback_value_include_string, c_callback_value_init_string))

        with open(os.path.join(folder, 'software', 'src', 'communication.h'), 'w') as h:
            h.write(self.h_file.format(device_name_dash, year, name, email, h_constants_string, h_defines_string, h_structs_string, h_function_prototypes_string, h_callback_prototypes_string, h_callback_list_string))

def generate(root_dir):
    common.generate(root_dir, 'en', TNGStubGenerator)

if __name__ == '__main__':
    generate(os.getcwd())
