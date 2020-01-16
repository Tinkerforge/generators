# Copyright (C) 2013 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
# Copyright (C) 2014, 2019-2020 Matthias Bolte <matthias@tinkerforge.com>
#
# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

=pod

=encoding utf8

=head1 NAME

Tinkerforge::Device - Base class for all Bricks and Bricklets (for internal use only)

=cut

# package definition
package Tinkerforge::Device;

# using modules
use POSIX qw(floor ceil);
use strict;
use warnings;
use Carp;
use threads;
use threads::shared;
use Thread::Queue;
use Math::BigInt;
use Tinkerforge::IPConnection;
use Tinkerforge::Error;
use Tinkerforge::DeviceDisplayNames qw(get_device_display_name);

# constants
use constant _RESPONSE_EXPECTED_ALWAYS_TRUE => 1; # getter
use constant _RESPONSE_EXPECTED_TRUE => 2; # setter
use constant _RESPONSE_EXPECTED_FALSE => 3; # setter,default

use constant _DEVICE_IDENTIFIER_CHECK_PENDING => 0;
use constant _DEVICE_IDENTIFIER_CHECK_MATCH => 1;
use constant _DEVICE_IDENTIFIER_CHECK_MISMATCH => 2;

# the constructor
sub _new
{
	my ($class, $uid, $ipcon, $api_version, $device_identifier, $device_display_name) =  @_;

	my $self :shared = shared_clone({uid => _base58_decode($uid),
	                                 uid_string => shared_clone($uid),
	                                 ipcon => shared_clone($ipcon),
	                                 api_version => shared_clone($api_version),
	                                 device_identifier => shared_clone($device_identifier),
	                                 device_display_name => shared_clone($device_display_name),
	                                 device_identifier_lock_ref => undef,
	                                 device_identifier_check => shared_clone(&_DEVICE_IDENTIFIER_CHECK_PENDING),
	                                 wrong_device_dsisplay_name => shared_clone('?'),
	                                 registered_callbacks => shared_clone({}),
	                                 callback_formats => shared_clone({}),
	                                 high_level_callbacks => shared_clone({}),
	                                 expected_response_sequence_number => undef,
	                                 expected_response_function_id => undef,
	                                 response_queue => Thread::Queue->new(),
	                                 device_lock_ref => undef,
	                                 request_lock_ref => undef,
	                                 response_expected => shared_clone({}),
	                                 stream_lock_ref => undef});

	bless($self, $class);

	my $device_identifier_lock :shared;
	my $device_lock :shared;
	my $request_lock :shared;
	my $stream_lock :shared;

	$self->{device_identifier_lock_ref} = \$device_identifier_lock;
	$self->{device_lock_ref} = \$device_lock;
	$self->{request_lock_ref} = \$request_lock;
	$self->{stream_lock_ref} = \$stream_lock;

	$self->{ipcon}->{devices}->{$self->{uid}} = $self;

	return $self;
}

sub _base58_decode
{
	my ($encoded) = @_;

	my @BASE58 = qw(1 2 3 4 5 6 7 8 9
					a b c d e f g h i
					j k m n o p q r s
					t u v w x y z A B
					C D E F G H J K L
					M N P Q R S T U V
					W X Y Z);

	my $remaining = $encoded;
	my $i = 0;
	my %BASE58 = map {$_ => $i++} @BASE58;
	my $value = Math::BigInt->new(0);
	my $base = Math::BigInt->new(1);

	while (length($remaining) > 0)
	{
		my $digit = chop $remaining;
		my $index = $BASE58{$digit};

		if (!defined($index))
		{
			croak(Tinkerforge::Error->_new(Tinkerforge::Error->INVALID_UID, "UID '$encoded' contains invalid character"));
		}

		my $next = $base->copy();

		$next->bmul($index);
		$value->badd($next);
		$base->bmul(58);
	}

	if ($value->bcmp(0xFFFFFFFF) > 0)
	{
		croak(Tinkerforge::Error->_new(Tinkerforge::Error->INVALID_UID, "UID '$encoded' is too big"));
	}

	if ($value->is_zero())
	{
		croak(Tinkerforge::Error->_new(Tinkerforge::Error->INVALID_UID, "UID '$encoded' is empty or maps to zero"));
	}

	return $value->numify();
}

sub _send_request
{
	my ($self, $function_id, $data, $form_data, $form_return) = @_;

	lock(${$self->{request_lock_ref}});

	my $packet_header = undef;
	my $packed_data = undef;
	my $packet = undef;
	my $length = undef;
	my $response_packet = undef;

	if(scalar(@{$data}) > 0 && $form_data ne '')
	{
		my @form_data_arr = split(' ', $form_data);

		if((scalar(@form_data_arr)) == (scalar(@{$data})))
		{
			my $i = 0;

			for(; $i < scalar(@{$data}); $i++)
			{
				if(split('', $form_data_arr[$i]) > 1)
				{
					# Cardinality greater than 1
					my @form_data_arr_tmp = split('', $form_data_arr[$i]);
					# Getting the numeric value from data form
					my ($form_pack_numeric) = $form_data_arr[$i] =~ /(\d+)/;

					# Strings should be treated different even if its in Z<count> form
					if($form_data_arr_tmp[0] eq 'Z')
					{
						# Getting the first number from the data form string
						my ($char_count) = $form_data =~ /(\d+)/;
						# Because with Z20 the 20th character will be NULL
						$packed_data .= substr(pack('Z'.($char_count+1), @{$data}[$i]), 0, 20);

						next;
					}
					elsif($form_data_arr_tmp[0] eq '?')
					{
						my $n = ceil($form_pack_numeric / 8);
						my @bool_array_bits = (0) x $n;

						for(my $j = 0; $j < $form_pack_numeric; $j++)
						{
							if (${@{$data}[$i]}[$j])
							{
								$bool_array_bits[floor($j / 8)] |= 1 << ($j % 8);
							}
						}

						for(my $j = 0; $j < $n; $j++)
						{
							$packed_data .= pack("C", $bool_array_bits[$j]);
						}
					}
					else
					{
						my $j = 0;

						for(; $j < $form_pack_numeric; $j ++)
						{
							$packed_data .= pack("$form_data_arr_tmp[0]", @{@{$data}[$i]}[$j]);
						}
					}
				}

				if(split('', $form_data_arr[$i]) == 1)
				{
					if($form_data_arr[$i] eq '?')
					{
						$packed_data .= pack("C", @{$data}[$i]);
					}
					else
					{
						$packed_data .= pack("$form_data_arr[$i]", @{$data}[$i]);
					}
				}
			}
		}

		$length = 8 + length($packed_data);
	}
	else
	{
		$length = 8;
	}

	# creating a packet header for the request
	$packet_header = $self->{ipcon}->_create_packet_header($self, $length, $function_id);

	my $_seq = $self->{ipcon}->_get_seq_from_data($packet_header);

	$self->{expected_response_sequence_number} = share($_seq);
	$self->{expected_response_function_id} = share($function_id);

	if($length > 8) # means there is data in payload
	{
		$packet = $packet_header.$packed_data;
	}
	else # means no data in payload
	{
		$packet = $packet_header;
	}

	$self->{ipcon}->_ipcon_send($packet);

	# checking whether response is expected
	if($self->get_response_expected($function_id))
	{
		# waiting for response
		$response_packet = $self->{response_queue}->dequeue_timed($self->{ipcon}->{timeout});

		if(defined($response_packet))
		{
			if(defined($form_return))
			{
				if(length($response_packet) >= 8)
				{
					my $_err_code = $self->{ipcon}->_get_err_from_data($response_packet);

					if($_err_code != 0)
					{
						my $_fid = $self->{ipcon}->_get_fid_from_data($response_packet);

						if($_err_code == 1)
						{
							croak(Tinkerforge::Error->_new(Tinkerforge::Error->INVALID_PARAMETER, "Got invalid parameter for function $_fid"));
							return 1;
						}
						elsif($_err_code == 2)
						{
							croak(Tinkerforge::Error->_new(Tinkerforge::Error->FUNCTION_NOT_SUPPORTED, "Function $_fid is not supported"));
							return 1;
						}
						else
						{
							croak(Tinkerforge::Error->_new(Tinkerforge::Error->UNKNOWN_ERROR, "Function $_fid returned an unknown error"));
							return 1;
						}
					}

					my $response_packet_payload = $self->{ipcon}->_get_payload_from_data($response_packet);

					return $self->{ipcon}->_dispatch_response($response_packet_payload, $form_return, undef, undef);
				}
			}
		}
		else
		{
			croak(Tinkerforge::Error->_new(Tinkerforge::Error->TIMEOUT, "Did not receive response for function $function_id in time"));
		}
	}

	return 1;
}

sub _check_device_identifier
{
	my ($self) = @_;

	if($self->{device_identifier_check} == &_DEVICE_IDENTIFIER_CHECK_MATCH)
	{
		return 1;
	}

	lock(${$self->{device_identifier_lock_ref}});

	if($self->{device_identifier_check} == &_DEVICE_IDENTIFIER_CHECK_PENDING)
	{
		my ($uid, $connected_uid, $position, $hardware_version, $firmware_version, $device_identifier, $enumeration_type) =
		    $self->_send_request(255, [], '', 'Z8 Z8 a C3 C3 S'); # get_identity

		if($device_identifier == $self->{device_identifier})
		{
			$self->{device_identifier_check} = shared_clone(&_DEVICE_IDENTIFIER_CHECK_MATCH);
		}
		else
		{
			$self->{device_identifier_check} = shared_clone(&_DEVICE_IDENTIFIER_CHECK_MISMATCH);
			$self->{wrong_device_dsisplay_name} = get_device_display_name($device_identifier);
		}
	}

	if ($self->{device_identifier_check} == &_DEVICE_IDENTIFIER_CHECK_MISMATCH) {
		croak(Tinkerforge::Error->_new(Tinkerforge::Error->WRONG_DEVICE_TYPE,
		      "UID $self->{uid_string} belongs to a $self->{wrong_device_dsisplay_name} instead of the expected $self->{device_display_name}"));
	}

	return 1;
}

=head1 FUNCTIONS

=over

=item register_callback()

Registers the given $function name with the given $callback_id.

=cut

sub register_callback
{
	my ($self, $callback_id, $function) = @_;

	lock(${$self->{device_lock_ref}});

	$self->{registered_callbacks}->{$callback_id} = '&'.caller.'::'.$function;
}

=item get_api_version()

Returns the API version (major, minor, revision) of the bindings for
this device.

=cut

sub get_api_version
{
	my ($self) = @_;

	return $self->{api_version};
}

=item get_response_expected()

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

sub get_response_expected
{
	my ($self, $function_id) = @_;

	lock(${$self->{device_lock_ref}});

	if(!defined($self->{response_expected}->{$function_id}))
	{
		croak(Tinkerforge::Error->_new(Tinkerforge::Error->INVALID_FUNCTION_ID, "Function ID $function_id is unknown"));
	}

	if($self->{response_expected}->{$function_id} == &_RESPONSE_EXPECTED_ALWAYS_TRUE ||
	   $self->{response_expected}->{$function_id} == &_RESPONSE_EXPECTED_TRUE)
	{
		return 1;
	}
	else
	{
		return 0;
	}
}

=item set_response_expected()

Changes the response expected flag of the function specified by the
*function_id* parameter. This flag can only be changed for setter
(default value: *false*) and callback configuration functions
(default value: *true*). For getter functions it is always enabled.

Enabling the response expected flag for a setter function allows to
detect timeouts and other error conditions calls of this setter as
well. The device will then send a response for this purpose. If this
flag is disabled for a setter function then no response is send and
errors are silently ignored, because they cannot be detected.

=cut

sub set_response_expected
{
	my ($self, $function_id, $response_expected) = @_;

	lock(${$self->{device_lock_ref}});

	if(!defined($self->{response_expected}->{$function_id}))
	{
		croak(Tinkerforge::Error->_new(Tinkerforge::Error->INVALID_FUNCTION_ID, "Function ID $function_id is unknown"));
	}

	if($self->{response_expected}->{$function_id} != &_RESPONSE_EXPECTED_TRUE &&
	   $self->{response_expected}->{$function_id} != &_RESPONSE_EXPECTED_FALSE)
	{
		croak(Tinkerforge::Error->_new(Tinkerforge::Error->INVALID_FUNCTION_ID, "Response-Exepcted for function ID $function_id cannot be changed"));
	}

	if($response_expected)
	{
		$self->{response_expected}->{$function_id} = &_RESPONSE_EXPECTED_TRUE;
	}
	else
	{
		$self->{response_expected}->{$function_id} = &_RESPONSE_EXPECTED_FALSE;
	}
}

=item set_response_expected_all()

Changes the response expected flag for all setter and callback
configuration functions of this device at once.

=cut

sub set_response_expected_all
{
	my ($self, $response_expected) = @_;

	lock(${$self->{device_lock_ref}});

	foreach my $function_id (keys %{$self->{response_expected}})
	{
		if($self->{response_expected}->{$function_id} == &_RESPONSE_EXPECTED_TRUE ||
		   $self->{response_expected}->{$function_id} == &_RESPONSE_EXPECTED_FALSE)
		{
			if($response_expected)
			{
				$self->{response_expected}->{$function_id} = &_RESPONSE_EXPECTED_TRUE;
			}
			else
			{
				$self->{response_expected}->{$function_id} = &_RESPONSE_EXPECTED_FALSE;
			}
		}
	}
}

=back
=cut

1;
