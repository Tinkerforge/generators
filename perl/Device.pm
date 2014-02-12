# Copyright (C) 2013 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
#
# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

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
use constant RESPONSE_EXPECTED_INVALID_FUNCTION_ID => 0;
use constant RESPONSE_EXPECTED_ALWAYS_TRUE => 1; # GETTER
use constant RESPONSE_EXPECTED_ALWAYS_FALSE => 2; # CALLBACK
use constant RESPONSE_EXPECTED_TRUE => 3; # SETTER
use constant RESPONSE_EXPECTED_FALSE => 4; # SETTER; DEFAULT

# lock(s)
our $DEVICE_LOCK :shared;

# the constructor
sub new
{
	my ($class, $uid, $ipcon) =  @_;

	my $self :shared = shared_clone({uid => base58_decode($uid),
									 ipcon => shared_clone($ipcon),
									 api_version => [0, 0, 0],
									 registered_callbacks => shared_clone({}),
									 callback_formats => shared_clone({}),
									 expected_response_sequence_number => undef,
									 expected_response_function_id => undef,
									 response_queue => Thread::Queue->new(),
									 request_lock => undef,
									 auth_key => undef,
									 response_expected => shared_clone({Tinkerforge::IPConnection->FUNCTION_ENUMERATE =>
																		&RESPONSE_EXPECTED_ALWAYS_FALSE,
																		Tinkerforge::IPConnection->CALLBACK_ENUMERATE =>
																		&RESPONSE_EXPECTED_ALWAYS_FALSE})});

	bless($self, $class);

	return $self;
}

sub base58_decode
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

sub send_request
{
	lock($Tinkerforge::Device::DEVICE_LOCK);

	my ($self, $device, $function_id, $data, $form_data, $form_return) = @_;

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
	$packet_header = $device->{super}->{ipcon}->create_packet_header($device, $length, $function_id);

	my $_seq = $device->{super}->{ipcon}->get_seq_from_data($packet_header);

	$device->{super}->{expected_response_sequence_number} = share($_seq);
	$device->{super}->{expected_response_function_id} = share($function_id);

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

	$device->{super}->{ipcon}->ipconnection_send($packet);

	#checking whether response is expected
	if($device->get_response_expected($function_id))
	{
		#waiting for response
		$response_packet = $device->{super}->{response_queue}->dequeue_timed($device->{super}->{ipcon}->{timeout});

		if(defined($response_packet))
		{
			if(defined($form_return))
			{
				if(length($response_packet) >= 8)
				{
                    my $_err_code = $device->{super}->{ipcon}->get_err_from_data($response_packet);
                    if($_err_code != 0)
                    {
                        my $_fid = $device->{super}->{ipcon}->get_fid_from_data($response_packet);

                        if($_err_code == 1)
                        {
                            croak(Tinkerforge::Error->new(Tinkerforge::IPConnection->ERROR_INVALID_PARAMETER, "Got invalid parameter for function $_fid"));
                            return 1;
                        }
                        elsif($_err_code == 2)
                        {
                            croak(Tinkerforge::Error->new(Tinkerforge::IPConnection->ERROR_FUNCTION_NOT_SUPPORTED, "Function $_fid is not supported"));
                            return 1;
                        }    
                        else
                        {
                            croak(Tinkerforge::Error->new(Tinkerforge::IPConnection->ERROR_UNKNOWN_ERROR, "Function $_fid returned an unknown error"));
                            return 1;
                        }     
                    }
					my $response_packet_payload = $device->{super}->{ipcon}->get_payload_from_data($response_packet);
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
            croak(Tinkerforge::Error->new(Tinkerforge::IPConnection->ERROR_INVALID_PARAMETER, "Did not receive response for function $function_id in time"));
		}
	}

	return 1;
}

1;
