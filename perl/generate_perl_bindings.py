#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perl Bindings Generator
Copyright (C) 2013-2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014-2015, 2017 Matthias Bolte <matthias@tinkerforge.com>

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

import sys
import os

sys.path.append(os.path.split(os.getcwd())[0])
import common
import perl_common

class PerlBindingsDevice(perl_common.PerlDevice):
    def get_perl_package(self):
        template = """{0}
=pod

=encoding utf8

=head1 NAME

Tinkerforge::{1}{2} - {3}

=cut

package Tinkerforge::{1}{2};
"""

        return template.format(self.get_generator().get_header_comment('hash'),
                               self.get_camel_case_category(),
                               self.get_camel_case_name(),
                               common.select_lang(self.get_description()))

    def get_perl_use(self):
        template = """
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
"""

        return template.format(self.get_device_identifier(),
                               self.get_long_display_name())

    def get_perl_constants(self):
        callbacks = []
        template = """
=item CALLBACK_{0}

This constant is used with the register_callback() subroutine to specify
the CALLBACK_{0} callback.

=cut

use constant CALLBACK_{0} => {1};"""

        for packet in self.get_packets('callback'):
            callbacks.append(template.format(packet.get_upper_case_name(), packet.get_function_id()))

        for packet in self.get_packets('callback'):
            if packet.has_high_level():
                callbacks.append(template.format(packet.get_upper_case_name(skip=-2), -packet.get_function_id()))

        if self.get_long_display_name() == 'RS232 Bricklet':
            callbacks.append("""
=item CALLBACK_READ_CALLBACK

This constant is used with the register_callback() subroutine to specify
the CALLBACK_READ_CALLBACK callback.

=cut

use constant CALLBACK_READ_CALLBACK => &CALLBACK_READ; # for backward compatibility
""")
            callbacks.append("""
=item CALLBACK_ERROR_CALLBACK

This constant is used with the register_callback() subroutine to specify
the CALLBACK_ERROR_CALLBACK callback.

=cut

use constant CALLBACK_ERROR_CALLBACK => &CALLBACK_ERROR; # for backward compatibility
""")

        function_ids = []
        template = """
=item FUNCTION_{0}

This constant is used with the get_response_expected(), set_response_expected()
and set_response_expected_all() subroutines.

=cut

use constant FUNCTION_{0} => {1};"""

        for packet in self.get_packets('function'):
            function_ids.append(template.format(packet.get_upper_case_name(), packet.get_function_id()))

        constants = '\n'
        template = 'use constant {0}_{1} => {2};\n'

        for constant_group in self.get_constant_groups():
            for constant in constant_group.get_constants():
                if constant_group.get_type() == 'char':
                    value = "'{0}'".format(constant.get_value())
                else:
                    value = str(constant.get_value())

                constants += template.format(constant_group.get_upper_case_name(),
                                             constant.get_upper_case_name(),
                                             value)

        return '\n'.join(callbacks) + '\n' + '\n'.join(function_ids) + constants + "\n\n=back\n"

    def get_perl_new_subroutine(self):
        template = """
=head1 FUNCTIONS

=over

=item new()

Creates an object with the unique device ID *uid* and adds it to
the IP Connection *ipcon*.

=cut

sub new
{{
	my ($class, $uid, $ipcon) = @_;

	my $self = Tinkerforge::Device->_new($uid, $ipcon, [{0}, {1}, {2}]);
"""
        response_expecteds = []

        for packet in self.get_packets('function'):
            if len(packet.get_elements(direction='out')) > 0:
                flag = '_RESPONSE_EXPECTED_ALWAYS_TRUE'
            elif packet.get_doc_type() in ['ccf', 'llf']:
                flag = '_RESPONSE_EXPECTED_TRUE'
            else:
                flag = '_RESPONSE_EXPECTED_FALSE'

            response_expecteds.append('\t$self->{{response_expected}}->{{&FUNCTION_{0}}} = Tinkerforge::Device->{1};'
                                      .format(packet.get_upper_case_name(), flag))

        callbacks = []

        if len(self.get_packets('callback')) > 0:
            for packet in self.get_packets('callback'):
                callbacks.append('\t$self->{{callback_formats}}->{{&CALLBACK_{0}}} = \'{1}\';'
                                 .format(packet.get_upper_case_name(), packet.get_perl_format_list('out')))

        high_level_callbacks = []
        template2 = '\t$self->{{high_level_callbacks}}->{{&CALLBACK_{0}}} = shared_clone([shared_clone({{{3}}}), shared_clone([{4}]), shared_clone({{fixed_length => {1}, single_chunk => {2}}}), undef]);'

        for packet in self.get_packets('callback'):
            stream = packet.get_high_level('stream_*')

            if stream != None:
                roles_by_name = []
                roles_by_index = []

                for i, element in enumerate(packet.get_elements(direction='out')):
                    if element.get_role() != None:
                        roles_by_name.append('{0} => {1}'.format(element.get_role(), i))
                        roles_by_index.append("'{0}'".format(element.get_role()))
                    else:
                        roles_by_index.append('undef')

                high_level_callbacks.append(template2.format(packet.get_upper_case_name(skip=-2),
                                                             stream.get_fixed_length(default='undef'),
                                                             1 if stream.has_single_chunk() else 0,
                                                             ', '.join(roles_by_name),
                                                             ', '.join(roles_by_index)))

        return template.format(*self.get_api_version()) + '\n' + \
               '\n'.join(response_expecteds) + '\n\n' + \
               '\n'.join(callbacks) + '\n\n' + \
               '\n'.join(high_level_callbacks) + """

	bless($self, $class);

	return $self;
}

"""

    def get_perl_subroutines(self):
        methods = ''

        # normal and low-level
        multiple_return = """
=item {0}()

{1}

=cut

sub {0}
{{
	my ($self{2}) = @_;

	return $self->_send_request(&FUNCTION_{3}, [{4}], '{5}', '{6}');
}}
"""
        single_return = """
=item {0}()

{1}

=cut

sub {0}
{{
	my ($self{2}) = @_;

	return $self->_send_request(&FUNCTION_{3}, [{4}], '{5}', '{6}');
}}
"""
        no_return = """
=item {0}()

{1}

=cut

sub {0}
{{
	my ($self{2}) = @_;

	$self->_send_request(&FUNCTION_{3}, [{4}], '{5}', '{6}');
}}
"""

        for packet in self.get_packets('function'):
            subroutine_name = packet.get_underscore_name()
            function_id_constant = subroutine_name.upper()
            parameters = packet.get_perl_parameters()

            if len(parameters) > 0:
                parameters_arg = ', ' + parameters
            else:
                parameters_arg = ''

            doc = packet.get_perl_formatted_doc()
            device_in_format = packet.get_perl_format_list('in')
            device_out_format = packet.get_perl_format_list('out')

            elements = len(packet.get_elements(direction='out'))

            if elements > 1:
                methods += multiple_return.format(subroutine_name, doc, parameters_arg, function_id_constant, parameters, device_in_format, device_out_format)
            elif elements == 1:
                methods += single_return.format(subroutine_name, doc, parameters_arg, function_id_constant, parameters, device_in_format, device_out_format)
            else:
                methods += no_return.format(subroutine_name, doc, parameters_arg, function_id_constant, parameters, device_in_format, device_out_format)

        # high-level
        template_stream_in = """
sub {underscore_name}
{{
    my ($self{high_level_parameters}) = @_;

    if(scalar(@{{${stream_underscore_name}}}) > {stream_max_length})
    {{
        croak(Tinkerforge::Error->_new(Tinkerforge::Error->INVALID_PARAMETER, '{stream_name} can be at most {stream_max_length} items long'));
    }}
{result_variable}
    my ${stream_underscore_name}_length = scalar(@{{${stream_underscore_name}}});
    my ${stream_underscore_name}_chunk_offset = 0;

    if(${stream_underscore_name}_length == 0)
    {{
        my ${stream_underscore_name}_chunk_data = [{chunk_padding}] x {chunk_cardinality};

        {result_assignment}$self->{underscore_name}_low_level({parameters});
    }}
    else
    {{
        lock(${{$self->{{stream_lock_ref}}}});

        while(${stream_underscore_name}_chunk_offset < ${stream_underscore_name}_length)
        {{
            my ${stream_underscore_name}_chunk_data = [];
            my ${stream_underscore_name}_chunk_length = ${stream_underscore_name}_length - ${stream_underscore_name}_chunk_offset;

            if(${stream_underscore_name}_chunk_length > {chunk_cardinality}) {{
                ${stream_underscore_name}_chunk_length = {chunk_cardinality};
            }}

            for(my $i = 0; $i < ${stream_underscore_name}_chunk_length; $i++) {{
                push(@{{${stream_underscore_name}_chunk_data}}, @{{${stream_underscore_name}}}[${stream_underscore_name}_chunk_offset + $i]);
            }}

            if(scalar(@{{${stream_underscore_name}_chunk_data}}) < {chunk_cardinality})
            {{
                push(@{{${stream_underscore_name}_chunk_data}}, ({chunk_padding}) x ({chunk_cardinality} - scalar(@{{${stream_underscore_name}_chunk_data}})));
            }}

            {result_assignment}$self->{underscore_name}_low_level({parameters});
            ${stream_underscore_name}_chunk_offset += {chunk_cardinality};
        }}
    }}{result_return}
}}
"""
        template_stream_in_fixed_length = """
sub {underscore_name}
{{
    my ($self{high_level_parameters}) = @_;{result_variable}
    my ${stream_underscore_name}_length = {fixed_length};
    my ${stream_underscore_name}_chunk_offset = 0;

    if(scalar(@{{${stream_underscore_name}}}) != ${stream_underscore_name}_length)
    {{
        croak(Tinkerforge::Error->_new(Tinkerforge::Error->INVALID_PARAMETER, '{stream_name} has to be exactly '.${stream_underscore_name}_length.' items long'));
    }}

    lock(${{$self->{{stream_lock_ref}}}});

    while(${stream_underscore_name}_chunk_offset < ${stream_underscore_name}_length)
    {{
        my ${stream_underscore_name}_chunk_data = [];
        my ${stream_underscore_name}_chunk_length = ${stream_underscore_name}_length - ${stream_underscore_name}_chunk_offset;

        if(${stream_underscore_name}_chunk_length > {chunk_cardinality}) {{
            ${stream_underscore_name}_chunk_length = {chunk_cardinality};
        }}

        for(my $i = 0; $i < ${stream_underscore_name}_chunk_length; $i++) {{
            push(@{{${stream_underscore_name}_chunk_data}}, @{{${stream_underscore_name}}}[${stream_underscore_name}_chunk_offset + $i]);
        }}

        if(scalar(@{{${stream_underscore_name}_chunk_data}}) < {chunk_cardinality})
        {{
            push(@{{${stream_underscore_name}_chunk_data}}, ({chunk_padding}) x ({chunk_cardinality} - scalar(@{{${stream_underscore_name}_chunk_data}})));
        }}

        {result_assignment}$self->{underscore_name}_low_level({parameters});
        ${stream_underscore_name}_chunk_offset += {chunk_cardinality};
    }}{result_return}
}}
"""
        template_stream_in_short_write = """
sub {underscore_name}
{{
    my ($self{high_level_parameters}) = @_;

    if(scalar(@{{${stream_underscore_name}}}) > {stream_max_length})
    {{
        croak(Tinkerforge::Error->_new(Tinkerforge::Error->INVALID_PARAMETER, '{stream_name} can be at most {stream_max_length} items long'));
    }}
{result_variable}
    my ${stream_underscore_name}_length = scalar(@{{${stream_underscore_name}}});
    my ${stream_underscore_name}_chunk_offset = 0;
    my ${stream_underscore_name}_written = 0;

    if(${stream_underscore_name}_length == 0)
    {{
        my ${stream_underscore_name}_chunk_data = [{chunk_padding}] x {chunk_cardinality};

        {result_assignment}$self->{underscore_name}_low_level({parameters});
        {chunk_written_0}
    }}
    else
    {{
        lock(${{$self->{{stream_lock_ref}}}});

        while(${stream_underscore_name}_chunk_offset < ${stream_underscore_name}_length)
        {{
            my ${stream_underscore_name}_chunk_data = [];
            my ${stream_underscore_name}_chunk_length = ${stream_underscore_name}_length - ${stream_underscore_name}_chunk_offset;

            if(${stream_underscore_name}_chunk_length > {chunk_cardinality})
            {{
                ${stream_underscore_name}_chunk_length = {chunk_cardinality};
            }}

            for(my $i = 0; $i < ${stream_underscore_name}_chunk_length; $i++)
            {{
                push(@{{${stream_underscore_name}_chunk_data}}, @{{${stream_underscore_name}}}[${stream_underscore_name}_chunk_offset + $i]);
            }}

            if(scalar(@{{${stream_underscore_name}_chunk_data}}) < {chunk_cardinality})
            {{
                push(@{{${stream_underscore_name}_chunk_data}}, ({chunk_padding}) x ({chunk_cardinality} - scalar(@{{${stream_underscore_name}_chunk_data}})));
            }}

            {result_assignment}$self->{underscore_name}_low_level({parameters});
            {chunk_written_n}

            if({chunk_written_test} < {chunk_cardinality})
            {{
                last; # either last chunk or short write
            }}

            ${stream_underscore_name}_chunk_offset += {chunk_cardinality};
        }}
    }}
{result_return}
}}
"""
        template_stream_in_short_write_chunk_written = ['${stream_underscore_name}_written = $ret;',
                                                        '${stream_underscore_name}_written += $ret;',
                                                        '$ret']
        template_stream_in_short_write_array_chunk_written = ['${stream_underscore_name}_written = $ret[{chunk_written_index}];',
                                                              '${stream_underscore_name}_written += $ret[{chunk_written_index}];',
                                                              '$ret[{chunk_written_index}]']
        template_stream_in_short_write_result = """
    return ${stream_underscore_name}_written;"""
        template_stream_in_short_write_array_result = """
    return ({result_fields});"""
        template_stream_in_single_chunk = """
sub {underscore_name}
{{
    my ($self{high_level_parameters}) = @_;
    my ${stream_underscore_name}_length = scalar(@{{${stream_underscore_name}}});
    my ${stream_underscore_name}_data = [];

    push(@{{${stream_underscore_name}_data}}, @{{${stream_underscore_name}}}); # copy so we can potentially extend it

    if(${stream_underscore_name}_length > {chunk_cardinality})
    {{
        croak(Tinkerforge::Error->_new(Tinkerforge::Error->INVALID_PARAMETER, '{stream_name} can be at most {chunk_cardinality} items long'));
    }}

    if(${stream_underscore_name}_length < {chunk_cardinality})
    {{
        push(@{{${stream_underscore_name}_data}}, ({chunk_padding}) x ({chunk_cardinality} - ${stream_underscore_name}_length));
    }}

    return $self->{underscore_name}_low_level({parameters});
}}
"""
        template_stream_out = """
sub {underscore_name}
{{
    my ($self{high_level_parameters}) = @_;{fixed_length}

    lock(${{$self->{{stream_lock_ref}}}});

    my @ret = $self->{underscore_name}_low_level({parameters});{dynamic_length_1}
    my ${stream_underscore_name}_chunk_offset = $ret[{chunk_offset_index}];
{chunk_offset_check}{chunk_offset_check_my}${stream_underscore_name}_out_of_sync = ${stream_underscore_name}_chunk_offset != 0;
    {chunk_offset_check_indent}{chunk_offset_check_my}${stream_underscore_name}_data = $ret[{chunk_data_index}];{chunk_offset_check_end}

    while(!${stream_underscore_name}_out_of_sync && scalar(@{{${stream_underscore_name}_data}}) < ${stream_underscore_name}_length)
    {{
        @ret = $self->{underscore_name}_low_level({parameters});{dynamic_length_2}
        ${stream_underscore_name}_chunk_offset = $ret[{chunk_offset_index}];
        ${stream_underscore_name}_out_of_sync = ${stream_underscore_name}_chunk_offset != scalar(@{{${stream_underscore_name}_data}});
        push(@{{${stream_underscore_name}_data}}, @{{$ret[{chunk_data_index}]}});
    }}

    if(${stream_underscore_name}_out_of_sync) # discard remaining stream to bring it back in-sync
    {{
        while(${stream_underscore_name}_chunk_offset + {chunk_cardinality} < ${stream_underscore_name}_length)
        {{
            @ret = $self->{underscore_name}_low_level({parameters});{dynamic_length_3}
            ${stream_underscore_name}_chunk_offset = $ret[{chunk_offset_index}];
        }}

        croak(Tinkerforge::Error->_new(Tinkerforge::Error->STREAM_OUT_OF_SYNC, '{stream_name} stream is out-of-sync'));
    }}
{result}
}}
"""
        template_stream_out_fixed_length = """
    my ${stream_underscore_name}_length = {fixed_length};"""
        template_stream_out_dynamic_length = """
{{indent}}${stream_underscore_name}_length = $ret[{length_index}];"""
        template_stream_out_chunk_offset_check = """    my ${stream_underscore_name}_out_of_sync = undef;
    my ${stream_underscore_name}_data = undef;

    if(${stream_underscore_name}_chunk_offset == (1 << {shift_size}) - 1) # maximum chunk offset -> stream has no data
    {{
        ${stream_underscore_name}_length = 0;
        ${stream_underscore_name}_chunk_offset = 0;
        ${stream_underscore_name}_out_of_sync = 0;
        ${stream_underscore_name}_data = [];
    }}
    else
    {{
        """
        template_stream_out_single_chunk = """
sub {underscore_name}
{{
    my ($self{high_level_parameters}) = @_;
    my @ret = $self->{underscore_name}_low_level({parameters});
{result}
}}
"""
        template_stream_out_result = """
    splice(@{{${stream_underscore_name}_data}}, ${stream_underscore_name}_length);

    return ${stream_underscore_name}_data;"""
        template_stream_out_array_result = """
    splice(@{{${stream_underscore_name}_data}}, ${stream_underscore_name}_length);

    return ({result_fields});"""
        template_stream_out_single_chunk_result = """
    splice(@{{$ret[{chunk_data_index}]}}, $ret[{length_index}]);

    return $ret[{chunk_data_index}];"""
        template_stream_out_single_chunk_array_result = """
    splice(@{{$ret[{chunk_data_index}]}}, $ret[{length_index}]);

    return ({result_fields});"""

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

                length_element = stream_in.get_length_element()

                if length_element != None:
                    stream_max_length = (1 << int(length_element.get_type().replace('uint', ''))) - 1
                else:
                    stream_max_length = stream_in.get_fixed_length()

                if stream_in.has_short_write():
                    if len(packet.get_elements(direction='out')) < 2:
                        chunk_written_0 = template_stream_in_short_write_chunk_written[0].format(stream_underscore_name=stream_in.get_underscore_name())
                        chunk_written_n = template_stream_in_short_write_chunk_written[1].format(stream_underscore_name=stream_in.get_underscore_name())
                        chunk_written_test = template_stream_in_short_write_chunk_written[2].format(stream_underscore_name=stream_in.get_underscore_name())
                    else:
                        chunk_written_index = None

                        for i, element in enumerate(packet.get_elements(direction='out')):
                            if element.get_role() == 'stream_chunk_written':
                                chunk_written_index = i
                                break

                        chunk_written_0 = template_stream_in_short_write_array_chunk_written[0].format(stream_underscore_name=stream_in.get_underscore_name(),
                                                                                                       chunk_written_index=chunk_written_index)
                        chunk_written_n = template_stream_in_short_write_array_chunk_written[1].format(stream_underscore_name=stream_in.get_underscore_name(),
                                                                                                       chunk_written_index=chunk_written_index)
                        chunk_written_test = template_stream_in_short_write_array_chunk_written[2].format(stream_underscore_name=stream_in.get_underscore_name(),
                                                                                                          chunk_written_index=chunk_written_index)

                else:
                    chunk_written_0 = ''
                    chunk_written_n = ''
                    chunk_written_test = ''

                result_elements = packet.get_elements(direction='out', high_level=True)

                if len(result_elements) == 0:
                    result_variable = ''
                    result_assignment = ''
                    result_return = ''
                elif len(result_elements) == 1:
                    result_variable = '\n    my $ret = undef;'
                    result_assignment = '$ret = '

                    if stream_in.has_short_write():
                        result_return = template_stream_in_short_write_result.format(stream_underscore_name=stream_in.get_underscore_name())
                    else:
                        result_return = '\n\n    return $ret;'
                else:
                    result_variable = '\n    my @ret = undef;'
                    result_assignment = '@ret = '

                    if stream_in.has_short_write():
                        fields = []

                        for element in packet.get_elements(direction='out', high_level=True):
                            if element.get_role() == 'stream_written':
                                fields.append('${0}_written'.format(stream_in.get_underscore_name()))
                            else:
                                index = None

                                for i, other in enumerate(packet.get_elements(direction='out')):
                                    if other.get_name() == element.get_name():
                                        index = i
                                        break

                                fields.append('$ret[{0}]'.format(index))

                        result_return = template_stream_in_short_write_array_result.format(result_fields=', '.join(fields))
                    else:
                        result_return = '\n\n    return @ret;'

                methods += template.format(underscore_name=packet.get_underscore_name().replace('_low_level', ''),
                                           parameters=packet.get_perl_parameters(),
                                           high_level_parameters=common.wrap_non_empty(', ', packet.get_perl_parameters(high_level=True), ''),
                                           stream_name=stream_in.get_name(),
                                           stream_underscore_name=stream_in.get_underscore_name(),
                                           stream_max_length=stream_max_length,
                                           fixed_length=stream_in.get_fixed_length(default='nil'),
                                           chunk_cardinality=stream_in.get_chunk_data_element().get_cardinality(),
                                           chunk_padding=stream_in.get_chunk_data_element().get_perl_default_item_value(),
                                           chunk_written_0=chunk_written_0,
                                           chunk_written_n=chunk_written_n,
                                           chunk_written_test=chunk_written_test,
                                           result_variable=result_variable,
                                           result_assignment=result_assignment,
                                           result_return=result_return)
            elif stream_out != None:
                length_index = None
                chunk_offset_index = None
                chunk_data_index = None

                for i, element in enumerate(packet.get_elements(direction='out')):
                    if element.get_role() == 'stream_length':
                        length_index = i
                    elif element.get_role() == 'stream_chunk_offset':
                        chunk_offset_index = i
                    elif element.get_role() == 'stream_chunk_data':
                        chunk_data_index = i

                if stream_out.get_fixed_length() != None:
                    fixed_length = template_stream_out_fixed_length.format(stream_underscore_name=stream_out.get_underscore_name(),
                                                                           fixed_length=stream_out.get_fixed_length())
                    dynamic_length = ''
                    shift_size = int(stream_out.get_chunk_offset_element().get_type().replace('uint', ''))
                    chunk_offset_check = template_stream_out_chunk_offset_check.format(stream_underscore_name=stream_out.get_underscore_name(),
                                                                                       shift_size=shift_size)
                    chunk_offset_check_indent = '    '
                    chunk_offset_check_my = ''
                    chunk_offset_check_end = '\n    }'
                else:
                    fixed_length = ''
                    dynamic_length = template_stream_out_dynamic_length.format(stream_underscore_name=stream_out.get_underscore_name(),
                                                                               length_index=length_index)
                    chunk_offset_check = '    '
                    chunk_offset_check_indent = ''
                    chunk_offset_check_my = 'my '
                    chunk_offset_check_end = ''

                if len(packet.get_elements(direction='out', high_level=True)) < 2:
                    if stream_out.has_single_chunk():
                        result = template_stream_out_single_chunk_result.format(chunk_data_index=chunk_data_index,
                                                                                length_index=length_index)
                    else:
                        result = template_stream_out_result.format(stream_underscore_name=stream_out.get_underscore_name())
                else:
                    fields = []

                    for element in packet.get_elements(direction='out', high_level=True):
                        if element.get_role() == 'stream_data':
                            if stream_out.has_single_chunk():
                                fields.append('$ret[{0}]'.format(chunk_data_index, length_index))
                            else:
                                fields.append('${0}_data'.format(stream_out.get_underscore_name()))
                        else:
                            index = None

                            for i, other in enumerate(packet.get_elements(direction='out')):
                                if other.get_name() == element.get_name():
                                    index = i
                                    break

                            fields.append('$ret[{0}]'.format(index))

                    if stream_out.has_single_chunk():
                        result = template_stream_out_single_chunk_array_result.format(chunk_data_index=chunk_data_index,
                                                                                      length_index=length_index,
                                                                                      result_fields=', '.join(fields))
                    else:
                        result = template_stream_out_array_result.format(stream_underscore_name=stream_out.get_underscore_name(),
                                                                         result_fields=', '.join(fields))

                if stream_out.has_single_chunk():
                    template = template_stream_out_single_chunk
                else:
                    template = template_stream_out

                methods += template.format(underscore_name=packet.get_underscore_name().replace('_low_level', ''),
                                           parameters=packet.get_perl_parameters(),
                                           high_level_parameters=common.wrap_non_empty(', ', packet.get_perl_parameters(high_level=True), ''),
                                           stream_name=stream_out.get_name(),
                                           stream_underscore_name=stream_out.get_underscore_name(),
                                           fixed_length=fixed_length,
                                           dynamic_length_1=dynamic_length.format(indent='    ' * 1 + 'my '),
                                           dynamic_length_2=dynamic_length.format(indent='    ' * 2),
                                           dynamic_length_3=dynamic_length.format(indent='    ' * 3),
                                           chunk_offset_check=chunk_offset_check,
                                           chunk_offset_check_indent=chunk_offset_check_indent,
                                           chunk_offset_check_my=chunk_offset_check_my,
                                           chunk_offset_check_end=chunk_offset_check_end,
                                           chunk_cardinality=stream_out.get_chunk_data_element().get_cardinality(),
                                           length_index=length_index,
                                           chunk_offset_index=chunk_offset_index,
                                           chunk_data_index=chunk_data_index,
                                           result=result)

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
    def get_perl_parameters(self, high_level=False):
        params = []

        for element in self.get_elements(direction='in', high_level=high_level):
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

        for element in self.get_elements(direction=io):
            forms.append(element.get_perl_pack_format())

        return ' '.join(forms)

class PerlBindingsGenerator(common.BindingsGenerator):
    def get_bindings_name(self):
        return 'perl'

    def get_bindings_display_name(self):
        return 'Perl'

    def get_device_class(self):
        return PerlBindingsDevice

    def get_packet_class(self):
        return PerlBindingsPacket

    def get_element_class(self):
        return perl_common.PerlElement

    def generate(self, device):
        filename = '{0}{1}.pm'.format(device.get_camel_case_category(), device.get_camel_case_name())

        with open(os.path.join(self.get_bindings_root_directory(), 'bindings', filename), 'w') as f:
            f.write(device.get_perl_source())

        if device.is_released():
            self.released_files.append(filename)

def generate(bindings_root_directory):
    common.generate(bindings_root_directory, 'en', PerlBindingsGenerator)

if __name__ == "__main__":
    generate(os.getcwd())
