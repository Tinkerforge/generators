#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl Bindings Generator
Copyright (C) 2013-2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>

generator_perl_bindings.py: Generator for Perl bindings

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
package {1};
=comment
        {2}
=cut
"""
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        version = common.get_changelog_version(self.get_generator().get_bindings_root_directory())
        package_name = self.get_category() + self.get_camel_case_name()

        return package.format(common.gen_text_hash.format(date, *version),
                              package_name, self.get_description())

    def get_perl_use(self):
        return """
use Tinkerforge::Device;
use strict;
use warnings;
use Carp;
use threads::shared;

use constant DEVICE_IDENTIFIER => {0};
""".format(self.get_device_identifier())

    def get_perl_constants(self):
        cbs = ''
        cb = 'use constant CALLBACK_{0} => {1};\n'
        for packet in self.get_packets('callback'):
            cbs += cb.format(packet.get_upper_case_name(), packet.get_function_id())

        function_ids = '\n'
        function_id = 'use constant FUNCTION_{0} => {1};\n'
        for packet in self.get_packets('function'):
            function_ids += function_id.format(packet.get_upper_case_name(), packet.get_function_id())

        str_constants = '\n'
        str_constant = 'use constant {0}_{1} => {2};\n'
        constants = self.get_constants()
        for constant in constants:
            for definition in constant.definitions:
                if constant.type == 'char':
                    value = "'{0}'".format(definition.value)
                else:
                    value = str(definition.value)

                str_constants += str_constant.format(constant.name_uppercase,
                                                     definition.name_uppercase,
                                                     value)+''
        return cbs + function_ids + str_constants

    def get_perl_new_subroutine(self):
        dev_new = """
sub new
{{
=comment
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
=cut
    my ($class, $host, $port) = @_;

    my $self :shared = shared_clone({{super => shared_clone(new Device($host,$port)),
                                     api_version => [{0}, {1}, {2}],
"""
        response_expected = '                                     response_expected => shared_clone({'

        for idx, packet in enumerate(self.get_packets()):
            if packet.get_type() == 'callback':
                prefix = 'CALLBACK_'
                flag = 'RESPONSE_EXPECTED_ALWAYS_FALSE'
            elif len(packet.get_elements('out')) > 0:
                prefix = 'FUNCTION_'
                flag = 'RESPONSE_EXPECTED_ALWAYS_TRUE'
            elif packet.get_doc()[0] == 'ccf':
                prefix = 'FUNCTION_'
                flag = 'RESPONSE_EXPECTED_TRUE'
            else:
                prefix = 'FUNCTION_'
                flag = 'RESPONSE_EXPECTED_FALSE'

            if idx == 0:
                response_expected += '&{0}{1} => Device->{2},\n' \
                    .format(prefix, packet.get_upper_case_name(), flag)
            if idx > 0 and idx != len(self.get_packets()) - 1:
                response_expected += '                                                                        &{0}{1} => Device->{2},\n' \
                    .format(prefix, packet.get_upper_case_name(), flag)
            if idx == len(self.get_packets()) - 1:
                response_expected += '                                                                        &{0}{1} => Device->{2}}})' \
                    .format(prefix, packet.get_upper_case_name(), flag)

        dev_new = dev_new.format(*self.get_api_version()) + response_expected

        if len(self.get_packets('callback')) > 0:
            cbs = ',\n                                    callback_formats => shared_clone({'

            for idx, packet in enumerate(self.get_packets('callback')):
                if idx == 0:
                    cb = "&CALLBACK_{0} => '{1}',\n"
                if idx > 0 and idx != len(self.get_packets()) - 1:
                    cb = "                                                                      &CALLBACK_{0} => '{1}',\n"
                if idx == len(self.get_packets('callback')) - 1:
                    cb = "                                                                      &CALLBACK_{0} => '{1}'}})}});\n\n"

                cbs += cb.format(packet.get_upper_case_name(),
                                 packet.get_perl_format_list('out'))
        else:
            cbs = '});\n'

        reg_ipcon_str = '    $self->{super}->{ipcon}->{devices}->{$self->{super}->{uid}} = $self;\n\n'
        reg_api_ver_str = '    $self->{super}->{api_version} = $self->{api_version};\n\n'
        bless_str = '    bless($self, $class);\n\n'
        return_str = '    return $self;\n}\n'

        return dev_new + cbs + reg_ipcon_str + reg_api_ver_str + bless_str + return_str

    def get_perl_subroutines(self):
        multiple_return = """
sub {0}
{{
=comment
        {1}
=cut
    lock($Device::DEVICE_LOCK);

    my ($self{2}) = @_;

    return $self->{{super}}->send_request($self, &FUNCTION_{3}, [{4}], '{5}', '{6}');
 }}
"""
        single_return = """
sub {0}
{{
=comment
        {1}
=cut
    lock($Device::DEVICE_LOCK);

    my ($self{2}) = @_;

    return $self->{{super}}->send_request($self, &FUNCTION_{3}, [{4}], '{5}', '{6}');
}}
"""
        no_return = """
sub {0}
{{
=comment
        {1}
=cut
    lock($Device::DEVICE_LOCK);

    my ($self{2}) = @_;

    $self->{{super}}->send_request($self, &FUNCTION_{3}, [{4}], '{5}', '{6}');
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

    def get_perl_common_device_subroutines(self):
        return """

sub register_callback
{
=comment
        Registers a callback with ID *id* to the function *callback*.
=cut
    lock($Device::DEVICE_LOCK);

    my ($self, $id, $callback) = @_;

    $self->{super}->{registered_callbacks}->{$id} = '&'.caller.'::'.$callback;
}

sub get_api_version
{
=comment
        Returns the API version (major, minor, revision) of the bindings for
        this device.
=cut
    my ($self) = @_;

    return $self->{super}->{api_version};
}

sub get_response_expected
{
=comment
        Returns the response expected flag for the function specified by the
        *function_id* parameter. It is *true* if the function is expected to
        send a response, *false* otherwise.

        For getter functions this is enabled by default and cannot be disabled,
        because those functions will always send a response. For callback
        configuration functions it is enabled by default too, but can be
        disabled via the set_response_expected function. For setter functions
        it is disabled by default and can be enabled.

        Enabling the response expected flag for a setter function allows to
        detect timeouts and other error conditions calls of this setter as
        well. The device will then send a response for this purpose. If this
        flag is disabled for a setter function then no response is send and
        errors are silently ignored, because they cannot be detected.
=cut
    lock($Device::DEVICE_LOCK);

    my ($self, $function_id) = @_;

    if(defined($self->{response_expected}->{$function_id}))
    {
        return $self->{response_expected}->{$function_id};
    }
    else
    {
        croak('Unknown function');
    }
}

sub set_response_expected
{
=comment
        Changes the response expected flag of the function specified by the
        *function_id* parameter. This flag can only be changed for setter
        (default value: *false*) and callback configuration functions
        (default value: *true*). For getter functions it is always enabled
        and callbacks it is always disabled.

        Enabling the response expected flag for a setter function allows to
        detect timeouts and other error conditions calls of this setter as
        well. The device will then send a response for this purpose. If this
        flag is disabled for a setter function then no response is send and
        errors are silently ignored, because they cannot be detected.
=cut
    lock($Device::DEVICE_LOCK);

    my ($self, $function_id, $response_expected) = @_;

    if(defined($self->{response_expected}->{$function_id}) &&
      ($self->{response_expected}->{$function_id} != Device->RESPONSE_EXPECTED_ALWAYS_TRUE ||
       $self->{response_expected}->{$function_id} != Device->RESPONSE_EXPECTED_ALWAYS_FALSE))
    {
       if($response_expected == Device->RESPONSE_EXPECTED_TRUE ||
          $response_expected == Device->RESPONSE_EXPECTED_FALSE)
       {
           $self->{response_expected}->{$function_id} = $response_expected;
       }
       else
       {
           croak('Unknown value');
       }
    }
    else
    {
        croak('Unknown function or value');
    }
}

sub set_response_expected_all
{
=comment
        Changes the response expected flag for all setter and callback
        configuration functions of this device at once.
=cut
    lock($Device::DEVICE_LOCK);

    my ($self, $response_expected) = @_;

    foreach my $key (sort keys $self->{response_expected})
    {
        if($response_expected == Device->RESPONSE_EXPECTED_TRUE ||
           $response_expected == Device->RESPONSE_EXPECTED_FALSE)
        {
            if($self->{response_expected}->{$key} != Device->RESPONSE_EXPECTED_ALWAYS_TRUE ||
               $self->{response_expected}->{$key} != Device->RESPONSE_EXPECTED_ALWAYS_FALSE)
            {
                $self->{response_expected}->{$key} = $response_expected;
            }
        }
        else
        {
            croak('Unknown value');
        }
    }
}

"""

    def get_perl_source(self):
        source  = self.get_perl_package()
        source += self.get_perl_use()
        source += self.get_perl_constants()
        source += self.get_perl_new_subroutine()
        source += self.get_perl_subroutines()
        source += self.get_perl_common_device_subroutines()
        source += "1;\n"

        return source

class PerlBindingsPacket(common.Packet):
    def get_perl_parameter_list(self):
        params = []

        for element in self.get_elements('in'):
            params.append('$' + element.get_underscore_name())

        return ', '.join(params)

    def get_perl_formatted_doc(self):
        text = common.select_lang(self.get_doc()[1])

        def format_parameter(name):
            return name # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)
        text += common.format_since_firmware(self.get_device(), self)

        return '\n        '.join(text.strip().split('\n'))

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
        file_name = '{0}{1}.pm'.format(device.get_category(), device.get_camel_case_name())

        pm = open(os.path.join(self.get_bindings_root_directory(), 'bindings', file_name), 'wb')
        pm.write(device.get_perl_source())
        pm.close()

        if device.is_released():
            self.released_files.append(file_name)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', PerlBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
