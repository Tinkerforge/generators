#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
C/C++ Bindings Generator
Copyright (C) 2016 Olaf Lüke <olaf@tinkerforge.com>

generate_comcu_stubs.py: Generator for communication API stubs
                         for co-processor Bricklets

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
import datetime
import shutil
from sets import Set

sys.path.append(os.path.split(os.getcwd())[0])
import common
import c_common

class COMCUBindingsDevice(common.Device):
    def get_h_constants(self):
        constant_format = '#define {prefix}_{constant_group_upper_case_name}_{constant_upper_case_name} {constant_value}'
        char_format="'{0}'"
        constants = []

        for i, constant_group in enumerate(self.get_constant_groups()[0:-3]): # Remove last 3 constant groups (bootloader constants)
            if i != 0:
                constants.append('')
            for constant in constant_group.get_constants():
                if constant_group.get_type() == 'char':
                    value = char_format.format(constant.get_value())
                else:
                    value = str(constant.get_value())

                constants.append(constant_format.format(constant_group_upper_case_name=constant_group.get_upper_case_name(),
                                                        constant_group_camel_case_name=constant_group.get_camel_case_name(),
                                                        constant_upper_case_name=constant.get_upper_case_name(),
                                                        constant_camel_case_name=constant.get_camel_case_name(),
                                                        constant_value=value,
                                                        prefix=self.get_upper_case_name()))

        return constants

    def get_h_defines(self):
        define_function =  '#define FID_{0} {1}'
        define_callback =  '#define FID_CALLBACK_{0} {1}'

        defines = []
        for packet in self.get_packets('function'):
            if packet.get_function_id() < 200:
                defines.append(define_function.format(packet.get_upper_case_name(), packet.get_function_id()))

        defines.append('')
        for packet in self.get_packets('callback'):
            if packet.get_function_id() < 200:
                defines.append(define_callback.format(packet.get_upper_case_name(), packet.get_function_id()))

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
                        c_type = element.get_c_type(False)
                        if element.get_cardinality() > 1:
                            struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                                      element.get_underscore_name(),
                                                                      element.get_cardinality());
                        else:
                            struct_body += '\t{0} {1};\n'.format(c_type, element.get_underscore_name())

                    structs.append(struct_temp.format(struct_body, packet.get_camel_case_name(), '_Callback'))
                    continue

                struct_body = ''

                for element in packet.get_elements(direction='in'):
                    c_type = element.get_c_type(False)

                    if element.get_cardinality() > 1:
                        struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                                  element.get_underscore_name(),
                                                                  element.get_cardinality());
                    else:
                        struct_body += '\t{0} {1};\n'.format(c_type, element.get_underscore_name())

                structs.append(struct_temp.format(struct_body, packet.get_camel_case_name(), ''))

                if len(packet.get_elements(direction='out')) == 0:
                    continue

                struct_body = ''

                for element in packet.get_elements(direction='out'):
                    c_type = element.get_c_type(False)

                    if element.get_cardinality() > 1:
                        struct_body += '\t{0} {1}[{2}];\n'.format(c_type,
                                                                  element.get_underscore_name(),
                                                                  element.get_cardinality());
                    else:
                        struct_body += '\t{0} {1};\n'.format(c_type, element.get_underscore_name())

                structs.append(struct_temp.format(struct_body, packet.get_camel_case_name(), '_Response'))

        return structs

    def get_h_function_prototypes(self):
        prototype =  'BootloaderHandleMessageResponse {0}(const {1} *data);'
        prototype_with_response =  'BootloaderHandleMessageResponse {0}(const {1} *data, {2} *response);'
        prototypes = []

        for packet in self.get_packets('function'):
            if packet.get_function_id() < 200 and not packet.is_part_of_callback_value():
                if len(packet.get_elements(direction='out')) == 0:
                    prototypes.append(prototype.format(packet.get_underscore_name(), packet.get_camel_case_name()))
                else:
                    prototypes.append(prototype_with_response.format(packet.get_underscore_name(), packet.get_camel_case_name(), packet.get_camel_case_name() + '_Response'))

        return prototypes

    def get_h_callback_prototypes(self):
        prototype = 'bool handle_{0}_callback(void);'

        prototypes = []
        for packet in self.get_packets('callback'):
            if packet.get_function_id() < 200:
                prototypes.append(prototype.format(packet.get_underscore_name()))

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
                callback_list.append(callback.format(packet.get_underscore_name()))

        return callback_list

    def get_c_cases(self):
        case =  '\t\tcase FID_{0}: return {1}(message);'
        case_with_response = '\t\tcase FID_{0}: return {1}(message, response);'
        case_cv =  '\t\tcase FID_{0}: return {1}(message, &callback_value_{2});'
        case_cv_with_response = '\t\tcase FID_{0}: return {1}(message, response, &callback_value_{2});'
        cases = []

        for packet in self.get_packets('function'):
            if packet.get_function_id() < 200:
                if packet.is_part_of_callback_value():
                    if not 'corresponding_getter' in packet.raw_data:
                        callback_value_function_name = 'get_callback_value'
                    elif packet.raw_data['name'].startswith('Get '):
                        callback_value_function_name = 'get_callback_value_callback_configuration'
                    else:
                        callback_value_function_name = 'set_callback_value_callback_configuration'

                    if len(packet.get_elements(direction='out')) == 0:
                        cases.append(case_cv.format(packet.get_upper_case_name(), callback_value_function_name, packet.get_callback_value_underscore_name()))
                    else:
                        cases.append(case_cv_with_response.format(packet.get_upper_case_name(), callback_value_function_name, packet.get_callback_value_underscore_name()))
                else:
                    if len(packet.get_elements(direction='out')) == 0:
                        cases.append(case.format(packet.get_upper_case_name(), packet.get_underscore_name()))
                    else:
                        cases.append(case_with_response.format(packet.get_upper_case_name(), packet.get_underscore_name()))

        return cases

    def get_c_functions(self):
        function_with_response = """BootloaderHandleMessageResponse {0}(const {1} *data, {2} *response) {{
\tresponse->header.length = sizeof({2});

\treturn HANDLE_MESSAGE_RESPONSE_NEW_MESSAGE;
}}
"""

        function = """BootloaderHandleMessageResponse {0}(const {1} *data) {{

\treturn HANDLE_MESSAGE_RESPONSE_EMPTY;
}}
"""
        functions = []

        for packet in self.get_packets('function'):
            if packet.get_function_id() < 200 and not packet.is_part_of_callback_value():
                if len(packet.get_elements(direction='out')) == 0:
                    functions.append(function.format(packet.get_underscore_name(), packet.get_camel_case_name()))
                else:
                    functions.append(function_with_response.format(packet.get_underscore_name(), packet.get_camel_case_name(), packet.get_camel_case_name() + '_Response'))

        return functions

    def get_c_callbacks(self):
        callback = """
bool handle_{0}_callback(void) {{
\tstatic bool is_buffered = false;
\tstatic {1}_Callback cb;

\tif(!is_buffered) {{
\t\ttfp_make_default_header(&cb.header, bootloader_get_uid(), sizeof({1}_Callback), FID_CALLBACK_{2});
\t\t// TODO: Implement {1} callback handling

\t\treturn false;
\t}}

\tif(bootloader_spitfp_is_send_possible(&bootloader_status.st)) {{
\t\tbootloader_spitfp_send_ack_and_message(&bootloader_status, (uint8_t*)&cb, sizeof({1}_Callback));
\t\tis_buffered = false;
\t\treturn true;
\t}} else {{
\t\tis_buffered = true;
\t}}

\treturn false;
}}"""

        callback_cv = """
bool handle_{0}_callback(void) {{
\treturn handle_callback_value_callback(&callback_value_{1}, FID_CALLBACK_{2});
}}"""

        callbacks = []
        for packet in self.get_packets('callback'):
            if packet.get_function_id() < 200:
                if packet.is_part_of_callback_value():
                    callbacks.append(callback_cv.format(packet.get_underscore_name(), packet.get_callback_value_underscore_name(), packet.get_upper_case_name()))
                else:
                    callbacks.append(callback.format(packet.get_underscore_name(), packet.get_camel_case_name(), packet.get_upper_case_name()))

        return callbacks

    def get_c_callback_value_include(self):
        callback_values = Set()
        for packet in self.get_packets('function'):
            if packet.get_function_id() < 200 and packet.is_part_of_callback_value():
                callback_values.add(packet.get_callback_value_underscore_name())

        if len(callback_values) == 0:
            return ''

        cv = """#include "bricklib2/utility/callback_value.h"

{0}
"""
        cv_declaration = ''
        for callback_value in callback_values:
            cv_declaration += 'CallbackValue callback_value_{0};\n'.format(callback_value)

        return cv.format(cv_declaration)

    def get_c_callback_value_init(self):
        callback_values = Set()
        for packet in self.get_packets('function'):
            if packet.get_function_id() < 200 and packet.is_part_of_callback_value():
                callback_values.add(packet.get_callback_value_underscore_name())

        if len(callback_values) == 0:
            return ''

        cv = """\t// TODO: Add proper functions
{0}
"""
        cv_declaration = ''
        for callback_value in callback_values:
            cv_declaration += '\tcallback_value_init(&callback_value_{0}, NULL);;\n'.format(callback_value)

        return cv.format(cv_declaration)


class COMCUBindingsPacket(c_common.CPacket):
    pass

class COMCUBindingsGenerator(common.BindingsGenerator):
    c_file = """/* {0}-bricklet
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
{7}
BootloaderHandleMessageResponse handle_message(const void *message, void *response) {{
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
    h_file = """/* {0}-bricklet
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
#include "bricklib2/bootloader/bootloader.h"

// Default functions
BootloaderHandleMessageResponse handle_message(const void *data, void *response);
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
        return 'c'

    def get_bindings_display_name(self):
        return 'CO MCU'

    def get_device_class(self):
        return COMCUBindingsDevice

    def get_packet_class(self):
        return COMCUBindingsPacket

    def get_element_class(self):
        return c_common.CElement

    def copy_templates_to(self, folder_dst):
        folder_src = os.path.join(self.get_bindings_root_directory(), 'comcu_templates')
        shutil.copytree(os.path.join(folder_src, 'software'), os.path.join(folder_dst, 'software'))
        shutil.copytree(os.path.join(folder_src, 'hardware'),  os.path.join(folder_dst, 'hardware'))
        shutil.copytree(os.path.join(folder_src, 'datasheets'),  os.path.join(folder_dst, 'datasheets'))

    def fill_templates(self, folder, device_name_dash, device_name, device_identifier, year, name, email, callback_value):
        for dname, dirs, files in os.walk(folder):
            for fname in files:
                fpath = os.path.join(dname, fname)
                with open(fpath, "r") as f:
                    s = f.read()
                s = s.replace("""<<<DEVICE_NAME_DASH>>>""", device_name_dash)
                s = s.replace("""<<<DEVICE_NAME_READABLE>>>""", device_name)
                s = s.replace("""<<<DEVICE_IDENTIFIER>>>""", str(device_identifier))
                s = s.replace("""<<<YEAR>>>""", str(year))
                s = s.replace("""<<<NAME>>>""", name)
                s = s.replace("""<<<EMAIL>>>""", email)
                s = s.replace("""<<<CMAKE_SOURCE_CALLBACK_VALUE>>>""", callback_value)
                with open(fpath, "w") as f:
                    f.write(s)

    def generate(self, device):
        folder = os.path.join(self.get_bindings_root_directory(), 'comcu_output', '{0}_{1}'.format(device.get_underscore_category(), device.get_underscore_name()))
        try:
            shutil.rmtree(folder) # first we delete the comcu output if it already exists for this device
        except:
            pass # It is OK if the directory does not exist...

        os.mkdir(folder)

        device_name_dash = device.get_underscore_name().replace('_', '-')
        year = datetime.datetime.now().year
        name = device.get_author().split("<")[0].rstrip()             #author syntax: Firstname Lastname <email>
        email = device.get_author().split("<")[1].replace(">","")
        callback_value = ''
        if device.has_callback_value():
            callback_value = """\t"${PROJECT_SOURCE_DIR}/src/bricklib2/utility/callback_value.c"\n"""

        self.copy_templates_to(folder)
        self.fill_templates(folder, device_name_dash, device.get_name(), device.get_device_identifier(), year, name, email, callback_value)

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

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', COMCUBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
