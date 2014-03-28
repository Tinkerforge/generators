# Copyright (C) 2013 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
# Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>
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
use strict;
use warnings;
use Carp;
use threads;
use threads::shared;
use Thread::Queue;
use Tinkerforge::IPConnection;
use Tinkerforge::Error;

# constants
use constant _RESPONSE_EXPECTED_INVALID_FUNCTION_ID => 0;
use constant _RESPONSE_EXPECTED_ALWAYS_TRUE => 1; # GETTER
use constant _RESPONSE_EXPECTED_ALWAYS_FALSE => 2; # CALLBACK
use constant _RESPONSE_EXPECTED_TRUE => 3; # SETTER
use constant _RESPONSE_EXPECTED_FALSE => 4; # SETTER; DEFAULT

# the constructor
sub _new
{
	my ($class, $uid, $ipcon, $api_version) =  @_;

	my $self :shared = shared_clone({uid => _base58_decode($uid),
	                                 ipcon => shared_clone($ipcon),
	                                 api_version => shared_clone($api_version),
	                                 registered_callbacks => shared_clone({}),
	                                 callback_formats => shared_clone({}),
	                                 expected_response_sequence_number => undef,
	                                 expected_response_function_id => undef,
	                                 response_queue => Thread::Queue->new(),
	                                 device_lock_ref => undef,
	                                 request_lock_ref => undef,
	                                 response_expected => shared_clone({Tinkerforge::IPConnection->_FUNCTION_ENUMERATE => &_RESPONSE_EXPECTED_ALWAYS_FALSE,
	                                                                    Tinkerforge::IPConnection->CALLBACK_ENUMERATE => &_RESPONSE_EXPECTED_ALWAYS_FALSE})});

	bless($self, $class);

	my $device_lock :shared;
	my $request_lock :shared;

	$self->{device_lock_ref} = \$device_lock;
	$self->{request_lock_ref} = \$request_lock;

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

	my $i = 0;
	my %BASE58 = map{ $_ => $i++} @BASE58;

	my $decoded = 0;
	my $multi = 1;
	my $base = @BASE58;

	while (length($encoded) > 0)
	{
		my $digit = chop $encoded;
		$decoded += $multi * $BASE58{$digit};
		$multi *= $base;
	}

	return $decoded;
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

					my $j = 0;

					for(; $j < $form_pack_numeric; $j ++)
					{
						$packed_data .= pack("$form_data_arr_tmp[0]", @{@{$data}[$i]}[$j]);
					}
				}
				if(split('', $form_data_arr[$i]) == 1)
				{
					$packed_data .= pack("$form_data_arr[$i]", @{$data}[$i]);
				}
			}
		}
		$length = 8 + length($packed_data);
	}
	else
	{
		$length = 8;
	}

	#creating a packet header for the request
	$packet_header = $self->{ipcon}->_create_packet_header($self, $length, $function_id);

	my $_seq = $self->{ipcon}->_get_seq_from_data($packet_header);

	$self->{expected_response_sequence_number} = share($_seq);
	$self->{expected_response_function_id} = share($function_id);

	#means there is data in payload
	if($length > 8)
	{
		$packet = $packet_header.$packed_data;
	}
	#means no data in payload
	else
	{
		$packet = $packet_header;
	}

	$self->{ipcon}->_ipcon_send($packet);

	#checking whether response is expected
	if($self->get_response_expected($function_id))
	{
		#waiting for response
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
					my @form_return_arr = split(' ', $form_return);

					if(scalar(@form_return_arr) > 1)
					{
						my @copy_info_arr;
						my $copy_info_arr_len;
						my $copy_from_index = 0;
						my $arguments_arr_index = 0;
						my $anon_arr_index = 0;
						my @return_arr;
						my @arguments_arr = unpack('('.$form_return.')<', $response_packet_payload);

						foreach(@form_return_arr)
						{
							my $count = $_;
							my @form_single_arr = split('', $_);

							if($form_single_arr[0] eq 'c' ||
							   $form_single_arr[0] eq 'C' ||
							   $form_single_arr[0] eq 's' ||
							   $form_single_arr[0] eq 'S' ||
							   $form_single_arr[0] eq 'l' ||
							   $form_single_arr[0] eq 'L' ||
							   $form_single_arr[0] eq 'q' ||
							   $form_single_arr[0] eq 'Q' ||
							   $form_single_arr[0] eq 'f')
							{
								if(scalar(@form_single_arr) > 1)
								{
									$count =~ s/[^\d]//g;
									push(@copy_info_arr, [$copy_from_index, $count]);
									$copy_from_index += $count;

									next;
								}
								else
								{
									$copy_from_index ++;
								}
							}
							else
							{
								$copy_from_index ++;
							}
						}

						$copy_info_arr_len = scalar(@copy_info_arr);

						if($copy_info_arr_len > 0)
						{
							while($arguments_arr_index < scalar(@arguments_arr))
							{
								if(scalar(@copy_info_arr) > 0)
								{
									if($copy_info_arr[0][0] == $arguments_arr_index)
									{
										my $anon_arr_iterator = $copy_info_arr[0][0];

										if($anon_arr_index == 0)
										{
											$anon_arr_index = $anon_arr_iterator;
										}

										$return_arr[$anon_arr_index] = [];

										for(; $anon_arr_iterator < ($copy_info_arr[0][0]+$copy_info_arr[0][1]); $anon_arr_iterator++)
										{
											push($return_arr[$anon_arr_index], $arguments_arr[$anon_arr_iterator]);
										}

										$anon_arr_index ++;
										$arguments_arr_index += $copy_info_arr[0][1];
										shift(@copy_info_arr);
									}
									else
									{
										push(@return_arr, $arguments_arr[$arguments_arr_index]);
										$anon_arr_index ++;
										$arguments_arr_index ++;
									}
								}
								else
								{
									push(@return_arr, $arguments_arr[$arguments_arr_index]);
									$arguments_arr_index ++;
								}
							}

							my $i = 0;

							foreach(@form_return_arr)
							{
								my @form_single_arr = split('', $_);

								if($form_single_arr[0] eq 'a' && scalar(@form_single_arr) > 1)
								{
									my @string_to_split_arr = split('', $return_arr[$i]);
									$return_arr[$i] = [];

									foreach(@string_to_split_arr)
									{
										push($return_arr[$i], $_);
									}
								}

								$i++;
							}

							return @return_arr;
						}

						if($copy_info_arr_len == 0)
						{
							my @return_arr = unpack($form_return, $response_packet_payload);
							my $i = 0;

							foreach(@form_return_arr)
							{
								my @form_single_arr = split('', $_);

								if($form_single_arr[0] eq 'a' && scalar(@form_single_arr) > 1)
								{
									my @string_to_split_arr = split('', $return_arr[$i]);
									$return_arr[$i] = [];

									foreach(@string_to_split_arr)
									{
										push($return_arr[$i], $_);
									}
								}

								$i++;
							}

							return @return_arr;
						}
					}

					if(scalar(@form_return_arr) == 1)
					{
						my @form_return_arr_0_arr = split('', $form_return_arr[0]);

						if(scalar(@form_return_arr_0_arr) > 1)
						{
							my @return_arr_tmp = unpack($form_return, $response_packet_payload);

							if($form_return_arr_0_arr[0] eq 'a')
							{
								my @return_arr = split('', $return_arr_tmp[0]);
								return \@return_arr;
							}

							if($form_return_arr_0_arr[0] eq 'Z')
							{
								my $return_arr = @return_arr_tmp;
								return $return_arr;
							}

							my @return_arr = @return_arr_tmp;
							return @return_arr;
						}

						if(scalar(@form_return_arr_0_arr) == 1)
						{
							return unpack($form_return, $response_packet_payload);
						}
					}
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

=head1 FUNCTIONS

=over

=item register_callback()

Registers a callback with ID $id to the function named $callback.

=cut

sub register_callback
{
	my ($self, $id, $callback) = @_;

	lock(${$self->{device_lock_ref}});

	$self->{registered_callbacks}->{$id} = '&'.caller.'::'.$callback;
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

	if (!defined($self->{response_expected}->{$function_id}))
	{
		croak(Tinkerforge::Error->_new(Tinkerforge::Error->INVALID_FUNCTION_ID, "Function ID $function_id is unknown"));
	}

	if ($self->{response_expected}->{$function_id} == &_RESPONSE_EXPECTED_ALWAYS_TRUE ||
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
(default value: *true*). For getter functions it is always enabled
and callbacks it is always disabled.

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

	if (!defined($self->{response_expected}->{$function_id}))
	{
		croak(Tinkerforge::Error->_new(Tinkerforge::Error->INVALID_FUNCTION_ID, "Function ID $function_id is unknown"));
	}

	if ($self->{response_expected}->{$function_id} != &_RESPONSE_EXPECTED_TRUE &&
	    $self->{response_expected}->{$function_id} != &_RESPONSE_EXPECTED_FALSE)
	{
		croak(Tinkerforge::Error->_new(Tinkerforge::Error->INVALID_FUNCTION_ID, "Response-Exepcted for function ID $function_id cannot be changed"));
	}

	if ($response_expected)
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

	foreach my $function_id (keys $self->{response_expected})
	{
		if ($self->{response_expected}->{$function_id} == &_RESPONSE_EXPECTED_TRUE ||
		    $self->{response_expected}->{$function_id} == &_RESPONSE_EXPECTED_FALSE)
		{
			if ($response_expected)
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
