#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl Bindings Generator
Copyright (C) 2013-2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014-2015 Matthias Bolte <matthias@tinkerforge.com>

generate_perl_bindings.py: Generator for Perl bindings

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
from apt.package import Package

sys.path.append(os.path.split(os.getcwd())[0])
import common
import perl_common

class PerlBindingsDevice(perl_common.PerlDevice):
    def get_perl_package(self):
        package = """
{0}
=pod

=encoding utf8

=head1 NAME

Tinkerforge::{1}{2} - {3}

=cut

package Tinkerforge::{1}{2};
"""
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        version = common.get_changelog_version(self.get_generator().get_bindings_root_directory())

        return package.format(common.gen_text_hash.format(date, *version),
                              self.get_camel_case_category(),
                              self.get_camel_case_name(),
                              self.get_description())

    def get_perl_use(self):
        return """
use strict;
use warnings;
use Carp;
use threads;
use threads::shared;
use parent 'Tinkerforge::Device';
use Tinkerforge::IPConnection;
use Tinkerforge::Error;

=head1 CONSTANTS

=over

=item DEVICE_IDENTIFIER

This constant is used to identify a {1}.

The get_identity() subroutine and the CALLBACK_ENUMERATE callback of the
IP Connection have a device_identifier parameter to specify the Brick's or
Bricklet's type.

=cut

use constant DEVICE_IDENTIFIER => {0};

=item DEVICE_DISPLAY_NAME

This constant represents the display name of a {1}.

=cut

use constant DEVICE_DISPLAY_NAME => '{1}';
""".format(self.get_device_identifier(),
           self.get_long_display_name())

    def get_perl_constants(self):
        callbacks = []
        callback = """
=item CALLBACK_{0}

This constant is used with the register_callback() subroutine to specify
the CALLBACK_{0} callback.

=cut

use constant CALLBACK_{0} => {1};"""

        for packet in self.get_packets('callback'):
            callbacks.append(callback.format(packet.get_upper_case_name(), packet.get_function_id()))

        function_ids = []
        function_id = """
=item FUNCTION_{0}

This constant is used with the get_response_expected(), set_response_expected()
and set_response_expected_all() subroutines.

=cut

use constant FUNCTION_{0} => {1};"""
        for packet in self.get_packets('function'):
            function_ids.append(function_id.format(packet.get_upper_case_name(), packet.get_function_id()))

        str_constants = '\n'
        str_constant = 'use constant {0}_{1} => {2};\n'
        for constant_group in self.get_constant_groups():
            for constant in constant_group.get_constants():
                if constant_group.get_type() == 'char':
                    value = "'{0}'".format(constant.get_value())
                else:
                    value = str(constant.get_value())

                str_constants += str_constant.format(constant_group.get_upper_case_name(),
                                                     constant.get_upper_case_name(),
                                                     value)

        return '\n'.join(callbacks) + '\n' + '\n'.join(function_ids) + str_constants + "\n\n=back\n"

    def get_perl_new_subroutine(self):
        dev_new = """
=head1 FUNCTIONS

=over

=item new()

Creates an object with the unique device ID *uid* and adds it to
the IP Connection *ipcon*.

=cut

sub new
{{
\tmy ($class, $uid, $ipcon) = @_;

\tmy $self = Tinkerforge::Device->_new($uid, $ipcon, [{0}, {1}, {2}]);
"""
        response_expecteds = []

        for packet in self.get_packets():
            if packet.get_type() == 'callback':
                prefix = 'CALLBACK_'
                flag = '_RESPONSE_EXPECTED_ALWAYS_FALSE'
            elif len(packet.get_elements('out')) > 0:
                prefix = 'FUNCTION_'
                flag = '_RESPONSE_EXPECTED_ALWAYS_TRUE'
            elif packet.get_doc_type() == 'ccf':
                prefix = 'FUNCTION_'
                flag = '_RESPONSE_EXPECTED_TRUE'
            else:
                prefix = 'FUNCTION_'
                flag = '_RESPONSE_EXPECTED_FALSE'

            response_expecteds.append('\t$self->{{response_expected}}->{{&{0}{1}}} = Tinkerforge::Device->{2};'.format(prefix, packet.get_upper_case_name(), flag))

        callbacks = []

        if len(self.get_packets('callback')) > 0:
            for packet in self.get_packets('callback'):
                callbacks.append('\t$self->{{callback_formats}}->{{&CALLBACK_{0}}} = \'{1}\';'.format(packet.get_upper_case_name(), packet.get_perl_format_list('out')))

        return dev_new.format(*self.get_api_version()) + '\n' + '\n'.join(response_expecteds) + '\n\n' + '\n'.join(callbacks) + """

\tbless($self, $class);

\treturn $self;
}

"""

    def get_perl_subroutines(self):
        multiple_return = """
=item {0}()

{1}

=cut

sub {0}
{{
\tmy ($self{2}) = @_;

\treturn $self->_send_request(&FUNCTION_{3}, [{4}], '{5}', '{6}');
}}
"""
        single_return = """
=item {0}()

{1}

=cut

sub {0}
{{
\tmy ($self{2}) = @_;

\treturn $self->_send_request(&FUNCTION_{3}, [{4}], '{5}', '{6}');
}}
"""
        no_return = """
=item {0}()

{1}

=cut

sub {0}
{{
\tmy ($self{2}) = @_;

\t$self->_send_request(&FUNCTION_{3}, [{4}], '{5}', '{6}');
}}
"""
        methods = ''
        cls = self.get_perl_class_name()
        for packet in self.get_packets('function'):
            subroutine_name = packet.get_underscore_name()
            function_id_constant = subroutine_name.upper()
            parameters = packet.get_perl_parameter_list()

            if len(parameters) > 0:
                parameters_arg = ', ' + parameters
            else:
                parameters_arg = ''

            doc = packet.get_perl_formatted_doc()
            device_in_format = packet.get_perl_format_list('in')
            device_out_format = packet.get_perl_format_list('out')

            elements = len(packet.get_elements('out'))

            if elements > 1:
                methods += multiple_return.format(subroutine_name, doc, parameters_arg, function_id_constant, parameters, device_in_format, device_out_format)
            elif elements == 1:
                methods += single_return.format(subroutine_name, doc, parameters_arg, function_id_constant, parameters, device_in_format, device_out_format)
            else:
                methods += no_return.format(subroutine_name, doc, parameters_arg, function_id_constant, parameters, device_in_format, device_out_format)

        return methods

    def get_perl_source(self):
        source  = self.get_perl_package()
        source += self.get_perl_use()
        source += self.get_perl_constants()
        source += self.get_perl_new_subroutine()
        source += self.get_perl_subroutines()
        source += "=back\n=cut\n\n1;\n"

        return source

class PerlBindingsPacket(common.Packet):
    def get_perl_parameter_list(self):
        params = []

        for element in self.get_elements('in'):
            params.append('$' + element.get_underscore_name())

        return ', '.join(params)

    def get_perl_formatted_doc(self):
        text = common.select_lang(self.get_doc_text())

        def format_parameter(name):
            return name # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return text.strip()

    def get_perl_format_list(self, io):
        forms = []

        for element in self.get_elements(io):
            forms.append(element.get_perl_pack_format())

        return ' '.join(forms)

class PerlBindingsGenerator(common.BindingsGenerator):
    released_files_name_prefix = 'perl'

    def get_bindings_name(self):
        return 'perl'

    def get_device_class(self):
        return PerlBindingsDevice

    def get_packet_class(self):
        return PerlBindingsPacket

    def get_element_class(self):
        return perl_common.PerlElement

    def generate(self, device):
        filename = '{0}{1}.pm'.format(device.get_camel_case_category(), device.get_camel_case_name())

        pm = open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename), 'wb')
        pm.write(device.get_perl_source())
        pm.close()

        if device.is_released():
            self.released_files.append(filename)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', PerlBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
