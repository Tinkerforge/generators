# Copyright (C) 2013 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
# Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>
#
# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

=pod

=encoding utf8

=head1 NAME

Tinkerforge::IPConnection - TCP/IP connection handling

=cut

# package definition
package Tinkerforge::IPConnection;

# using modules
use strict;
use warnings;
use Carp;
use threads;
use threads::shared;
use Thread::Queue;
use Thread::Semaphore;
use IO::Socket::INET;
use Socket qw(IPPROTO_TCP TCP_NODELAY MSG_NOSIGNAL);
use POSIX qw(dup getpid);
use Fcntl;
use Digest::HMAC_SHA1 qw(hmac_sha1);
use Time::HiRes qw(gettimeofday);
use Tinkerforge::Device;
use Tinkerforge::Error;

=head1 CONSTANTS

=over

=item CALLBACK_ENUMERATE

This constant is used with the register_callback() subroutine to specify
the CALLBACK_ENUMERATE callback.

=cut

use constant CALLBACK_ENUMERATE => 253;

=item CALLBACK_CONNECTED

This constant is used with the register_callback() subroutine to specify
the CALLBACK_CONNECTED callback.

=cut

use constant CALLBACK_CONNECTED => 0;

=item CALLBACK_DISCONNECTED

This constant is used with the register_callback() subroutine to specify
the CALLBACK_DISCONNECTED callback.

=cut

use constant CALLBACK_DISCONNECTED => 1;

=item ENUMERATION_TYPE_AVAILABLE

Possible value for $enumeration_type parameter of CALLBACK_ENUMERATE callback.

=cut

use constant ENUMERATION_TYPE_AVAILABLE => 0;

=item ENUMERATION_TYPE_CONNECTED

Possible value for $enumeration_type parameter of CALLBACK_ENUMERATE callback.

=cut

use constant ENUMERATION_TYPE_CONNECTED => 1;

=item ENUMERATION_TYPE_DISCONNECTED

Possible value for $enumeration_type parameter of CALLBACK_ENUMERATE callback.

=cut

use constant ENUMERATION_TYPE_DISCONNECTED => 2;

=item CONNECT_REASON_REQUEST

Possible value for $connect_reason parameter of CALLBACK_CONNECTED callback.

=cut

use constant CONNECT_REASON_REQUEST => 0;

=item CONNECT_REASON_AUTO_RECONNECT

Possible value for $connect_reason parameter of CALLBACK_CONNECTED callback.

=cut

use constant CONNECT_REASON_AUTO_RECONNECT => 1;

=item DISCONNECT_REASON_REQUEST

Possible value for $disconnect_reason parameter of CALLBACK_DISCONNECTED callback.

=cut

use constant DISCONNECT_REASON_REQUEST => 0;

=item DISCONNECT_REASON_ERROR

Possible value for $disconnect_reason parameter of CALLBACK_DISCONNECTED callback.

=cut

use constant DISCONNECT_REASON_ERROR => 1;

=item DISCONNECT_REASON_SHUTDOWN

Possible value for $disconnect_reason parameter of CALLBACK_DISCONNECTED callback.

=cut

use constant DISCONNECT_REASON_SHUTDOWN => 2;

=item CONNECTION_STATE_DISCONNECTED

Possible return value of the get_connection_state() subroutine.

=cut

use constant CONNECTION_STATE_DISCONNECTED => 0;

=item CONNECTION_STATE_CONNECTED

Possible return value of the get_connection_state() subroutine.

=cut

use constant CONNECTION_STATE_CONNECTED => 1;

=item CONNECTION_STATE_PENDING

Possible return value of the get_connection_state() subroutine.

=cut

use constant CONNECTION_STATE_PENDING => 2;

=back
=cut

use constant _FUNCTION_ENUMERATE => 254;
use constant _FUNCTION_DISCONNECT_PROBE => 128;

use constant _BROADCAST_UID => 0;

use constant _QUEUE_EXIT => 0;
use constant _QUEUE_META => 1;
use constant _QUEUE_PACKET => 2;

use constant _DISCONNECT_PROBE_INTERVAL => 5;

# the local socket variable, the actual socket
my $local_socket = undef;
my $local_socket_id = 0;

sub _init_local_socket
{
	my ($self) = @_;

	lock(${$self->{local_socket_lock_ref}});

	# clear values copied over by threads->create(). this has to be
	# called first from every thread.
	#
	# FIXME 1: this sharing model will create problems with user-created
	#          threads as they won't call this and will have their local
	#          copies not properly initialized

	if (defined($local_socket)) {
		$local_socket->close();
	}

	$local_socket = undef;
	$local_socket_id = 0;

	# ensure that current thread has valid local socket
	$self->_get_local_socket();

	# indicate that local socket got updated
	$self->{local_socket_handshake}->up();
}

sub _get_local_socket
{
	my ($self) = @_;

	lock(${$self->{local_socket_lock_ref}});

	if ($self->{socket_id} != $local_socket_id)
	{
		if (defined($local_socket))
		{
			$local_socket->close();
		}

		$local_socket = IO::Socket::INET->new();
		$local_socket_id = $self->{socket_id};

		$local_socket->fdopen(dup($self->{socket_fileno}), '+>>');
	}

	return $local_socket;
}

=head1 FUNCTIONS

=over

=item new()

Creates an IP Connection object that can be used to enumerate the available
devices. It is also required for the constructor of Bricks and Bricklets.

=cut

# the constructor
sub new
{
	my ($class) = @_;

	my $self :shared = shared_clone({host => undef,
	                                 port => undef,
	                                 timeout => 2.5,
	                                 next_sequence_number => 0, # protected by SEQUENCE_NUMBER_LOCK
	                                 next_authentication_nonce => 0, # protected by AUTHENTICATION_LOCK
	                                 auto_reconnect => 1,
	                                 auto_reconnect_allowed => 0,
	                                 auto_reconnect_pending => 0,
	                                 devices => shared_clone({}),
	                                 registered_callbacks => shared_clone({}),
	                                 socket_fileno => undef, # protected by SOCKET_LOCK
	                                 socket_id => 0,
	                                 receive_flag => 0,
	                                 receive_thread => undef,
	                                 disconnect_probe_flag => 0,
	                                 disconnect_probe_thread => undef,
	                                 disconnect_probe_queue => undef,
	                                 callback_thread => undef,
	                                 callback_queue => undef,
	                                 local_socket_handshake => undef,
	                                 socket_lock_ref => undef,
	                                 local_socket_lock_ref => undef,
	                                 send_lock_ref => undef,
	                                 sequence_number_lock_ref => undef,
	                                 authentication_lock_ref => undef, # protectes authentication handshake
	                                 brickd => undef
	                                });

	bless($self, $class);

	my $socket_lock :shared;
	my $local_socket_lock :shared;
	my $send_lock :shared;
	my $sequence_number_lock :shared;
	my $authentication_lock :shared;

	$self->{socket_lock_ref} = \$socket_lock;
	$self->{local_socket_lock_ref} = \$local_socket_lock;
	$self->{send_lock_ref} = \$send_lock;
	$self->{sequence_number_lock_ref} = \$sequence_number_lock;
	$self->{authentication_lock_ref} = \$authentication_lock;

	$self->_brickd_create();

	return $self;
}

=item connect()

Creates a TCP/IP connection to the given $host and $port. The host and port
can refer to a Brick Daemon or to a WIFI/Ethernet Extension.

Devices can only be controlled when the connection was established
successfully.

Blocks until the connection is established and throws an exception if there
is no Brick Daemon or WIFI/Ethernet Extension listening at the given
host and port.

=cut

sub connect
{
	my ($self, $host, $port) = @_;

	lock(${$self->{socket_lock_ref}});

	if(defined($self->{socket_fileno}))
	{
		croak(Tinkerforge::Error->_new(Tinkerforge::Error->ALREADY_CONNECTED,
		                               "Already connected to $self->{host}:$self->{host}"));
	}
	else
	{
		$self->{host} = $host;
		$self->{port} = $port;

		$self->_connect_unlocked(0);
	}

	return 1;
}

# NOTE: assumes that SOCKET_LOCK is locked
sub _connect_unlocked
{
	my ($self, $is_auto_reconnect) = @_;

	# create callback queue and thread
	if(!defined($self->{callback_thread}))
	{
		$self->{local_socket_handshake} = Thread::Semaphore->new(0);

		# FIXME: need packet_dispatch_allowed handling for the callback thread
		$self->{callback_queue} = Thread::Queue->new();
		$self->{callback_thread} = shared_clone(threads->create(\&_callback_thread_subroutine,
		                                                        $self, $self->{callback_queue}));

		if(!defined($self->{callback_thread}))
		{
			croak(Tinkerforge::Error->_new(Tinkerforge::Error->NO_THREAD,
			                               'Could not create callback thread'));
		}

		$self->{local_socket_handshake}->down();
	}

	# create socket
	$self->{socket_fileno} = undef;

	my $socket = IO::Socket::INET->new(PeerAddr => $self->{host},
	                                   PeerPort => $self->{port},
	                                   Proto => 'tcp',
	                                   Type => SOCK_STREAM,
	                                   Blocking => 1);
	my $error = $!;

	if(!defined($socket))
	{
		if (!$is_auto_reconnect)
		{
			# destroy callback thread
			$self->{callback_queue}->enqueue([&_QUEUE_EXIT, undef, undef, undef]);
			$self->{callback_thread}->join();
			$self->{callback_thread} = undef;
		}

		croak(Tinkerforge::Error->_new(Tinkerforge::Error->CONNECT_FAILED,
		                               "Could not connect to $self->{host}:$self->{port}: $error"));
	}

	eval
	{
		$socket->setsockopt(IPPROTO_TCP, TCP_NODELAY, 1);

		$| = 1; # enable autoflush
		if (defined(&{"MSG_NOSIGNAL"}))
		{
			$socket->send('', MSG_NOSIGNAL);
		}
		else
		{
			$socket->send('');
		}

		$self->{socket_fileno} = dup($socket->fileno());
	};
	$error = $!;

	eval
	{
		$socket->close();
	};

	if($error)
	{
		if (!$is_auto_reconnect)
		{
			# destroy callback thread
			$self->{callback_queue}->enqueue([&_QUEUE_EXIT, undef, undef, undef]);
			$self->{callback_thread}->join();
			$self->{callback_thread} = undef;
		}

		# destroy socket
		$self->_destroy_socket();

		croak(Tinkerforge::Error->_new(Tinkerforge::Error->CONNECT_FAILED,
		                               "Could not connect to $self->{host}:$self->{port}: $error"));
	}

	$self->{socket_id}++;

	$self->_init_local_socket();

	# create disconnect probe thread
	$self->{local_socket_handshake} = Thread::Semaphore->new(0);

	$self->{disconnect_probe_flag} = 1;
	$self->{disconnect_probe_queue} = Thread::Queue->new();
	$self->{disconnect_probe_thread} = shared_clone(threads->create(\&_disconnect_probe_thread_subroutine,
	                                                                $self, $self->{disconnect_probe_queue}));

	if(!defined($self->{disconnect_probe_thread}))
	{
		if (!$is_auto_reconnect)
		{
			# destroy callback thread
			$self->{callback_queue}->enqueue([&_QUEUE_EXIT, undef, undef, undef]);
			$self->{callback_thread}->join();
			$self->{callback_thread} = undef;
		}

		# destroy socket
		$self->_destroy_socket();

		croak(Tinkerforge::Error->_new(Tinkerforge::Error->NO_THREAD,
		                               'Could not create disconnect probe thread'));
	}

	$self->{local_socket_handshake}->down();

	# create receive thread. this has to be done after all other threads have
	# been created, because the receive thread will do a blocking recv() call
	# and while the call blocks the socket cannot be copied using Strawberry
	# Perl and Active State Perl. but perl will have to copy the socket during
	# the creation of a new thread and will then deadlock. so to avoid this
	# problem all threads have to be created before the first recv() call.
	#
	# FIXME: this only covers one case. if the user creates a thread then this
	#        one will deadlock on Windows if the receive thread is doing a
	#        blocking recv() call. another case is the user calling a setter or
	#        getter after an auto-reconnect. the IPConnection takes case of
	#        its own threads to have a valid local socket before starting to
	#        receive data. but the program main thread or user-created threads
	#        will update their local sockets (via _get_local_socket) later while
	#        the receive thread is already blocking the socket. this creates
	#        a deadlock on Windows again. http://perlmonks.org/?node_id=1078634
	#
	# NOTE:  all this applies to Strawberry Perl and Active State Perl only.
	#        with Cygwin's Perl everything works as expected.
	$self->{local_socket_handshake} = Thread::Semaphore->new(0);

	$self->{receive_flag} = 1;
	$self->{receive_thread} = shared_clone(threads->create(\&_receive_thread_subroutine, $self));

	if(!defined($self->{receive_thread}))
	{
		# destroy socket
		$self->_disconnect_unlocked();

		if (!$is_auto_reconnect)
		{
			# destroy callback thread
			$self->{callback_queue}->enqueue([&_QUEUE_EXIT, undef, undef, undef]);
			$self->{callback_thread}->join();
			$self->{callback_thread} = undef;
		}

		croak(Tinkerforge::Error->_new(Tinkerforge::Error->NO_THREAD,
		                               'Could not create receive thread'));
	}

	$self->{local_socket_handshake}->down();

	$self->{auto_reconnect_pending} = 0;
	$self->{auto_reconnect_allowed} = 0;

	# trigger connected callback
	if ($is_auto_reconnect)
	{
		$self->{callback_queue}->enqueue([&_QUEUE_META, &CALLBACK_CONNECTED,
		                                  &CONNECT_REASON_AUTO_RECONNECT, undef]);
	}
	else
	{
		$self->{callback_queue}->enqueue([&_QUEUE_META, &CALLBACK_CONNECTED,
		                                  &CONNECT_REASON_REQUEST, undef]);
	}

	$! = undef; # FIXME: workaround some Perl code polluting $!

	return 1;
}

=item disconnect()

Disconnects the TCP/IP connection from the Brick Daemon or the WIFI/Ethernet
Extension.

=cut

sub disconnect
{
	my ($self) = @_;

	my $callback_queue = undef;
	my $callback_thread = undef;

	if (1) {
		lock(${$self->{socket_lock_ref}});

		$self->{auto_reconnect_allowed} = 0;

		if ($self->{auto_reconnect_pending})
		{
			# abort pending auto-reconnect
			$self->{auto_reconnect_pending} = 0;
		}
		else
		{
			if (!defined($self->{socket_fileno}))
			{
				croak(Tinkerforge::Error->_new(Tinkerforge::Error->NOT_CONNECTED,
				                               'Not connected'));
			}

			$self->_disconnect_unlocked();
		}

		# destroy callback thread
		$callback_queue = $self->{callback_queue};
		$callback_thread = $self->{callback_thread};

		$self->{callback_queue} = undef;
		$self->{callback_thread} = undef;
	}

	# do this outside of socket_mutex to allow calling (dis-)connect from
	# the callbacks while blocking on the join call here
	$callback_queue->enqueue([&_QUEUE_META, &CALLBACK_DISCONNECTED,
	                          &DISCONNECT_REASON_REQUEST, undef]);
	$callback_queue->enqueue([&_QUEUE_EXIT, undef, undef, undef]);

	if (threads->self() != $callback_thread)
	{
		$callback_thread->join();
	}
	else
	{
		threads->self()->detach(); # detach, join() won't be called in this situation
	}

	$callback_thread = undef;

	# NOTE: no further cleanup of the callback queue and thread here, the
	# callback thread is doing this on exit

	return 1;
}

# NOTE: assumes that SOCKET_LOCK is locked
sub _disconnect_unlocked
{
	my ($self) = @_;

	# destroy disconnect probe thread
	$self->{disconnect_probe_queue}->enqueue(&_QUEUE_EXIT);
	$self->{disconnect_probe_thread}->join();
	$self->{disconnect_probe_thread} = undef;

	# FIXME: need packet_dispatch_allowed handling for the callback thread here

	# destroy receive thread (1/2)
	if(defined($self->{receive_thread}))
	{
		$self->{receive_flag} = 0;
	}

	# shutdown socket
	my $socket = $self->_get_local_socket();

	eval
	{
		$socket->shutdown(2);
	};

	# destroy receive thread (2/2)
	if(defined($self->{receive_thread}))
	{
		$self->{receive_thread}->join();
		$self->{receive_thread} = undef;
	}

	# destroy socket
	eval
	{
		$socket->close();
	};

	$self->{socket_fileno} = undef;

	return 1;
}

# NOTE: assumes that SOCKET_LOCK is locked
sub _destroy_socket
{
	my ($self) = @_;

	if (defined($self->{socket_fileno}))
	{
		my $socket = $self->_get_local_socket();

		eval
		{
			$socket->shutdown(2);
		};
		eval
		{
			$socket->close();
		};
	}

	$self->{socket_fileno} = undef;
}

sub _read_uint32_non_blocking
{
	my ($self, $filename) = @_;

	my $fh = undef;

	if (!defined(sysopen($fh, $filename, O_RDONLY | O_NONBLOCK)))
	{
		return undef;
	}

	my $bytes = undef;

	if (sysread($fh, $bytes, 4) != 4)
	{
		close($fh);

		return undef;
	}

	close($fh);

	return unpack('(V)<', $bytes);
}

# FIXME: this code is not ideal on Windows. if the script happens to run
#        under Cygwin then there will be a /dev/[u]random to use. otherwise
#        it'll fall back to the current time on Windows. there seems to be
#        no easy way to call CryptGenRandom from Perl here. on the other hand
#        the Perl bindings only work correct on Cygwin anyway, so this isn't
#        a huge problem currently.
sub _get_random_uint32
{
	my ($self) = @_;

	my $r = $self->_read_uint32_non_blocking('/dev/urandom');

	if (defined($r))
	{
		return $r;
	}

	$r = $self->_read_uint32_non_blocking('/dev/random');

	if (defined($r))
	{
		return $r;
	}

	my ($seconds, $microseconds) = gettimeofday();

	return (($seconds << 26 | $seconds >> 6) + $microseconds + getpid()) & 0xFFFFFFFF;
}

use constant _BRICK_DAEMON_FUNCTION_GET_AUTHENTICATION_NONCE => 1;
use constant _BRICK_DAEMON_FUNCTION_AUTHENTICATE => 2;

sub _brickd_create
{
	my ($self) = @_;

	$self->{brickd} = Tinkerforge::Device->_new('2', $self, [2, 0, 0]);
	$self->{brickd}->{response_expected}->{&_BRICK_DAEMON_FUNCTION_GET_AUTHENTICATION_NONCE} = Tinkerforge::Device->_RESPONSE_EXPECTED_ALWAYS_TRUE;
	$self->{brickd}->{response_expected}->{&_BRICK_DAEMON_FUNCTION_AUTHENTICATE} = Tinkerforge::Device->_RESPONSE_EXPECTED_TRUE;
}

sub _brickd_get_authentication_nonce
{
	my ($self) = @_;

	return $self->{brickd}->_send_request(&_BRICK_DAEMON_FUNCTION_GET_AUTHENTICATION_NONCE, [], '', 'C4');
}

sub _brickd_authenticate
{
	my ($self, $clientNonce, $digest) = @_;

	$self->{brickd}->_send_request(&_BRICK_DAEMON_FUNCTION_AUTHENTICATE, [$clientNonce, $digest], 'C4 C20', '');
}

=item authenticate()

Performs an authentication handshake with the connected Brick Daemon or
WIFI/Ethernet Extension. If the handshake succeeds the connection switches
from non-authenticated to authenticated state and communication can
continue as normal. If the handshake fails then the connection gets closed.
Authentication can fail if the wrong secret was used or if authentication
is not enabled at all on the Brick Daemon or the WIFI/Ethernet Extension.

For more information about authentication see
http://www.tinkerforge.com/en/doc/Tutorials/Tutorial_Authentication/Tutorial.html

=cut

sub authenticate
{
	my ($self, $secret) = @_;

	lock(${$self->{authentication_lock_ref}});

	if ($self->{next_authentication_nonce} == 0)
	{
		$self->{next_authentication_nonce} = $self->_get_random_uint32();
	}

	my @serverNonceArray = $self->_brickd_get_authentication_nonce();
	my $serverNonce = \@serverNonceArray;
	my $serverNonceBytes = pack('C4', @serverNonceArray);
	my $clientNonceNumber = $self->{next_authentication_nonce}++;
	my $clientNonceBytes = pack('V', $clientNonceNumber);
	my $clientNonce = [unpack('C4', $clientNonceBytes)];
	my $digestBytes = hmac_sha1($serverNonceBytes . $clientNonceBytes, $secret);
	my $digest = [unpack('C20', $digestBytes)];

	$self->_brickd_authenticate($clientNonce, $digest);
}

=item get_connection_state()

Can return the following states:

* IPConnection->CONNECTION_STATE_DISCONNECTED (0): No connection is established.
* IPConnection->CONNECTION_STATE_CONNETED (1): A connection to the Brick Daemon
  or the WIFI/Ethernet Extension  is established.
* IPConnection->CONNECTION_STATE_PENDING (2): IP Connection is currently trying
  to connect.

=cut

sub get_connection_state
{
	my ($self) = @_;

	if(defined($self->{socket_fileno}))
	{
		return &CONNECTION_STATE_CONNECTED;
	}
	elsif($self->{auto_reconnect_pending})
	{
		return &CONNECTION_STATE_PENDING;
	}
	else
	{
		return &CONNECTION_STATE_DISCONNECTED;
	}
}

=item set_auto_reconnect()

Enables or disables auto-reconnect. If auto-reconnect is enabled,
the IP Connection will try to reconnect to the previously given
host and port, if the connection is lost.

Default value is 1.

=cut

sub set_auto_reconnect
{
	my ($self, $auto_reconnect) = @_;

	$self->{auto_reconnect} = $auto_reconnect;

	if (!$self->{auto_reconnect})
	{
		# abort potentially pending auto reconnect
		$self->{auto_reconnect_allowed} = 0;
	}
}

=item get_auto_reconnect()

Returns 1 if auto-reconnect is enabled, 0 otherwise.

=cut

sub get_auto_reconnect
{
	my ($self) = @_;

	return $self->{auto_reconnect};
}

=item set_timeout()

Sets the timeout in seconds for getters and for setters for which the
response expected flag is activated.

Default timeout is 2.5.

=cut

sub set_timeout
{
	my ($self, $timeout) = @_;

	if ($timeout < 0)
	{
		croak(Tinkerforge::Error->_new(Tinkerforge::Error->INVALID_PARAMETER, 'Timeout cannot be negative'));
	}

	$self->{timeout} = $timeout;

}

=item get_timeout()

Returns the timeout as set by set_timeout().

=cut

sub get_timeout
{
	my ($self) = @_;

	return $self->{timeout};
}

=item enumerate()

Broadcasts an enumerate request. All devices will respond with an enumerate
callback.

=cut

sub enumerate
{
	my ($self) = @_;

	$self->_ipcon_send($self->_create_packet_header(undef, 8, &_FUNCTION_ENUMERATE));
}

=item register_callback()

Registers a callback with ID $id to the function named $callback.

=back
=cut

sub register_callback
{
	my ($self, $function_id, $function_name) = @_;

	$self->{registered_callbacks}->{$function_id} = '\&'.caller.'::'.$function_name;
}

sub _create_packet_header
{
	my ($self, $device, $length, $function_id) = @_;

	my $uid = &_BROADCAST_UID;
	my $seq_res_oth = $self->_get_next_sequence_number() << 4;
	my $err_fut = undef;

	if(defined($device))
	{
		$uid = $device->{uid};

		if($device->get_response_expected($function_id))
		{
			#setting response expected bit
			$seq_res_oth |= (1<<3);
		}
		else
		{
			#clearing response expected bit
			$seq_res_oth &= ~(1<<3);
		}

		#clearing other_options bits
		$seq_res_oth &= ~(1<<0);
		$seq_res_oth &= ~(1<<1);
		$seq_res_oth &= ~(1<<2);

		$err_fut = 0;
		#clearing error_code bits
		$err_fut &= ~(1<<6);
		$err_fut &= ~(1<<7);

		#clearing future_use bits
		$err_fut &= ~(1<<0);
		$err_fut &= ~(1<<1);
		$err_fut &= ~(1<<2);
		$err_fut &= ~(1<<3);
		$err_fut &= ~(1<<4);
		$err_fut &= ~(1<<5);

		return pack('(V C C C C)<', $uid, $length, $function_id, $seq_res_oth, $err_fut);
	}
	else
	{
		#clearing response expected bit
		$seq_res_oth &= ~(1<<3);

		#clearing other_options bits
		$seq_res_oth &= ~(1<<0);
		$seq_res_oth &= ~(1<<1);
		$seq_res_oth &= ~(1<<2);

		$err_fut = 0;
		#clearing error_code bits
		$err_fut &= ~(1<<6);
		$err_fut &= ~(1<<7);

		#clearing future_use bits
		$err_fut &= ~(1<<0);
		$err_fut &= ~(1<<1);
		$err_fut &= ~(1<<2);
		$err_fut &= ~(1<<3);
		$err_fut &= ~(1<<4);
		$err_fut &= ~(1<<5);

		return pack('(V C C C C)<', $uid, $length, $function_id, $seq_res_oth, $err_fut);
	}

	return 1;
}

sub _get_next_sequence_number
{
	my ($self) = @_;

	lock(${$self->{sequence_number_lock_ref}});

	if($self->{next_sequence_number} >= 0 && $self->{next_sequence_number} < 15)
	{
		$self->{next_sequence_number}++;
		return $self->{next_sequence_number};
	}
	else
	{
		$self->{next_sequence_number} = 1;
		return $self->{next_sequence_number};
	}

	return 1;
}

# NOTE: assumes that SOCKET_LOCK is locked if disconnect_immediately is 1
sub _handle_disconnect_by_peer
{
	my ($self, $disconnect_reason, $socket_id, $disconnect_immediately) = @_;

	$self->{auto_reconnect_allowed} = 1;

	if ($disconnect_immediately) {
		$self->_disconnect_unlocked();
	}

	$self->{callback_queue}->enqueue([&_QUEUE_META, &CALLBACK_DISCONNECTED,
	                                  $disconnect_reason, $socket_id]);
}

sub _ipcon_send
{
	my ($self, $packet) = @_;

	lock(${$self->{socket_lock_ref}});

	if(!defined($self->{socket_fileno}))
	{
		croak(Tinkerforge::Error->_new(Tinkerforge::Error->NOT_CONNECTED, 'Not connected'));
	}

	my $rc;
	eval
	{
		lock(${$self->{send_lock_ref}});

		$| = 1; # enable autoflush
		if (defined(&{"MSG_NOSIGNAL"}))
		{
			$rc = $self->_get_local_socket()->send($packet, MSG_NOSIGNAL);
		}
		else
		{
			$rc = $self->_get_local_socket()->send($packet);
		}
	};
	if(!defined($rc))
	{
		$self->_handle_disconnect_by_peer(&DISCONNECT_REASON_ERROR, 0, 1);

		croak(Tinkerforge::Error->_new(Tinkerforge::Error->NOT_CONNECTED, 'Not connected'));
	}

	$self->{disconnect_probe_flag} = 0;

	return 1;
}

sub _get_uid_from_data
{
	my ($self, $data) = @_;

	my @data_arr = undef;

	@data_arr = split('', $data);

	if(scalar(@data_arr) >= 8)
	{
		return unpack('(V)<', $data_arr[0].$data_arr[1].$data_arr[2].$data_arr[3]);
	}

	return 1;
}

sub _get_len_from_data
{
	my ($self, $data) = @_;

	my @data_arr = undef;

	@data_arr = split('', $data);

	if(scalar(@data_arr) >= 8)
	{
		return unpack('(C)<', $data_arr[4]);
	}

	return 1;
}

sub _get_fid_from_data
{
	my ($self, $data) = @_;

	my @data_arr = undef;

	@data_arr = split('', $data);

	if(scalar(@data_arr) >= 8)
	{
		return unpack('(C)<', $data_arr[5]);
	}

	return 1;
}

sub _get_seq_from_data
{
	my ($self, $data) = @_;

	my @data_arr = undef;
	my @bit_arr = undef;
	my $seq = undef;

	@data_arr = split('', $data);

	if(scalar(@data_arr) >= 8)
	{
		@bit_arr = split('', unpack('(b8)<', $data_arr[6]));
		$seq = $bit_arr[7].$bit_arr[6].$bit_arr[5].$bit_arr[4];
		return oct("0b$seq");
	}

	return 1;
}

sub _get_err_from_data
{
	my ($self, $data) = @_;

	my @data_arr = undef;
	my @bit_arr = undef;
	my $err = undef;

	@data_arr = split('', $data);

	if(scalar(@data_arr) >= 8)
	{
		@bit_arr = split('', unpack('(b8)<', $data_arr[7]));
		$err = $bit_arr[7].$bit_arr[6];
		return oct("0b$err");
	}

	return 1;
}

sub _get_payload_from_data
{
	my ($self, $data) = @_;

	my @data_arr = undef;
	my $payload = undef;

	@data_arr = split('', $data);

	if(scalar(@data_arr) > 8)
	{
		for(my $i = 8; $i < scalar(@data_arr); $i++)
		{
			$payload .= $data_arr[$i];
		}
		return $payload;
	}

	return 1;
}

sub _handle_packet
{
	my ($self, $packet) = @_;

	$self->{disconnect_probe_flag} = 0;

	my $fid = $self->_get_fid_from_data($packet);
	my $seq = $self->_get_seq_from_data($packet);

	if($seq == 0 && $fid == &CALLBACK_ENUMERATE)
	{
		if(defined($self->{registered_callbacks}->{&CALLBACK_ENUMERATE}))
		{
			$self->{callback_queue}->enqueue([&_QUEUE_PACKET, $packet, undef, undef]);
		}
		return 1;
	}

	my $uid = $self->_get_uid_from_data($packet);

	if(!defined($self->{devices}->{$uid}))
	{
		#response from unknown device, ignoring
		return 1;
	}

	if($seq == 0)
	{
		if(defined($self->{devices}->{$uid}))
		{
			my $_device = $self->{devices}->{$uid};
			my $_err_code = $_device->{ipcon}->_get_err_from_data($packet);

			if($_err_code != 0)
			{
				if($_err_code == 1)
				{
					croak(Tinkerforge::Error->_new(Tinkerforge::Error->INVALID_PARAMETER,
					                               "Got invalid parameter for function $fid"));
					return 1;
				}
				elsif($_err_code == 2)
				{
					croak(Tinkerforge::Error->_new(Tinkerforge::Error->FUNCTION_NOT_SUPPORTED,
					                               "Function $fid is not supported"));
					return 1;
				}
				else
				{
					croak(Tinkerforge::Error->_new(Tinkerforge::Error->UNKNOWN_ERROR,
					                               "Function $fid returned an unknown error"));
					return 1;
				}
			}
			$self->{callback_queue}->enqueue([&_QUEUE_PACKET, $packet, undef, undef]);
		}
		return 1;
	}

	my $_fid = $self->{devices}->{$uid}->{expected_response_function_id};
	my $_seq = $self->{devices}->{$uid}->{expected_response_sequence_number};

	if($$_fid == $fid && $$_seq == $seq)
	{
		$self->{devices}->{$uid}->{response_queue}->enqueue($packet);
		return 1;
	}

	return 1;
}

# thread subroutines

sub _receive_thread_subroutine
{
	my ($self) = @_;

	$self->_init_local_socket();

	my $data = '';
	my @data_arr = ();
	my $data_pending_flag = undef;
	my $socket_id = $self->{socket_id};

	while($self->{receive_flag})
	{
		my $rc = $self->_get_local_socket()->recv($data, 8192);
		my $error = $!;
		my $len = length($data);

		if(!$self->{receive_flag})
		{
			last;
		}

		if(!defined($rc))
		{
			threads->self()->detach(); # detach, join() won't be called in this situation
			$self->_handle_disconnect_by_peer(&DISCONNECT_REASON_ERROR, $socket_id, 0);
			last;
		}

		if(length($data) == 0)
		{
			threads->self()->detach(); # detach, join() won't be called in this situation
			$self->_handle_disconnect_by_peer(&DISCONNECT_REASON_SHUTDOWN, $socket_id, 0);
			last;
		}

		if($data_pending_flag)
		{
			@data_arr = (@data_arr, split('', $data));
			goto MORE_BYTES_TO_PROCCESS;
		}
		else
		{
			@data_arr = split('', $data);

			MORE_BYTES_TO_PROCCESS:

			if(scalar(@data_arr) >= 8)
			{
				my $i = undef;

				for($i = 8; $i <= unpack('C', $data_arr[4])-1; $i++)
				{
					if(defined($data_arr[$i]))
					{
						next;
					}
					else
					{
						last;
					}
				}

				if($i == unpack('C', $data_arr[4]))
				{
					my $packet_to_handle = join('', @data_arr[0 .. (unpack('C', $data_arr[4]))-1]);
					my $len = unpack('C', $data_arr[4]);

					$self->_handle_packet($packet_to_handle);

					while($len > 0)
					{
						shift (@data_arr);
						$len --;
					}

					if(scalar(@data_arr) == 0)
					{
						$data_pending_flag = undef;
						next;
					}
					elsif(scalar(@data_arr) >= 8)
					{
						goto MORE_BYTES_TO_PROCCESS;
					}
					elsif(scalar(@data_arr) != 0 && scalar(@data_arr) < 8 )
					{
						$data_pending_flag = 1;
						next;
					}
					else
					{
						next;
					}
				}
				elsif($i < unpack('C', $data_arr[4]))
				{
					$data_pending_flag = 1;
					goto next;
				}
				else
				{
					next;
				}
			}
			elsif(scalar(@data_arr) != 0)
			{
				#the header is incomplete
				$data_pending_flag = 1;
				next;
			}
			else
			{
				next;
			}
		}
	}

	return 1;
}

sub _callback_thread_subroutine
{
	my ($self, $callback_queue) = @_;

	$self->_init_local_socket();

	while(1)
	{
		my ($kind, $data_or_callback, $reason, $socket_id) = @{$callback_queue->dequeue()};

		if($kind == &_QUEUE_EXIT)
		{
			last;
		}
		elsif($kind == &_QUEUE_META)
		{
			$self->_dispatch_meta($data_or_callback, $reason, $socket_id);
		}
		elsif($kind == &_QUEUE_PACKET)
		{
			$self->_dispatch_packet($data_or_callback);
		}
	}

	return 1;
}

sub _dispatch_meta
{
	my ($self, $callback, $reason, $socket_id) = @_;

	if(!defined($callback) || !defined($reason))
	{
		return 1;
	}

	if($callback == &CALLBACK_CONNECTED)
	{
		if(defined($self->{registered_callbacks}->{&CALLBACK_CONNECTED}))
		{
			eval("$self->{registered_callbacks}->{&CALLBACK_CONNECTED}($reason);");
			return 1;
		}
	}
	elsif($callback == &CALLBACK_DISCONNECTED)
	{
		# need to do this here, the receive loop is not allowed to
		# hold the socket mutex because this could cause a deadlock
		# with a concurrent call to the (dis-)connect function
		if($reason != &DISCONNECT_REASON_REQUEST)
		{
			lock(${$self->{socket_lock_ref}});

			# don't close the socket if it got disconnected or
			# reconnected in the meantime
			if (defined($self->{socket_fileno}) && $self->{socket_id} == $socket_id)
			{
				# destroy disconnect probe thread
				$self->{disconnect_probe_queue}->enqueue(&_QUEUE_EXIT);
				$self->{disconnect_probe_thread}->join();
				$self->{disconnect_probe_thread} = undef;

				# destroy socket
				$self->_destroy_socket();
			}
		}

		if(defined($self->{registered_callbacks}->{&CALLBACK_DISCONNECTED}))
		{
			eval("$self->{registered_callbacks}->{&CALLBACK_DISCONNECTED}($reason);");
		}

		if ($reason != &DISCONNECT_REASON_REQUEST &&
			$self->{auto_reconnect} &&
			$self->{auto_reconnect_allowed})
		{
			$self->{auto_reconnect_pending} = 1;

			my $retry = 1;

			# block here until reconnect. this is okay, there is no
			# callback to deliver when there is no connection
			while ($retry)
			{
				$retry = 0;

				if (1) {
					lock(${$self->{socket_lock_ref}});

					if ($self->{auto_reconnect_allowed} && !defined($self->{socket_fileno}))
					{
						eval
						{
							$self->_connect_unlocked(1);
						};
						if($!)
						{
							$retry = 1;
						}
					}
					else
					{
						$self->{auto_reconnect_pending} = 0;
					}
				}

				if ($retry)
				{
					# wait a moment to give another thread a chance to
					# interrupt the auto-reconnect
					select(undef, undef, undef, 0.1);
				}
			}
		}
	}

	return 1;
}

sub _dispatch_packet
{
	my ($self, $packet) = @_;

	my $uid = $self->_get_uid_from_data($packet);
	my $len = $self->_get_len_from_data($packet);
	my $fid = $self->_get_fid_from_data($packet);
	my $payload = $self->_get_payload_from_data($packet);

	if($fid == &CALLBACK_ENUMERATE)
	{
		if(defined($self->{registered_callbacks}->{&CALLBACK_ENUMERATE}))
		{
			my $form_unpack = 'Z8 Z8 Z C3 C3 S C';
			my @form_unpack_arr = split(' ', $form_unpack);
			my @copy_info_arr;
			my $copy_info_arr_len;
			my $copy_from_index = 0;
			my $arguments_arr_index = 0;
			my $anon_arr_index = 0;
			my @return_arr;
			my @arguments_arr = unpack($form_unpack, $payload);

			if(scalar(@form_unpack_arr) > 1)
			{
				foreach(@form_unpack_arr)
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

					foreach(@form_unpack_arr)
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
						$i ++;
					}

					eval("$self->{registered_callbacks}->{&CALLBACK_ENUMERATE}(\@return_arr)");

					return 1;
				}

				if($copy_info_arr_len == 0)
				{
					my @return_arr = unpack($form_unpack, $payload);
					my $i = 0;

					foreach(@form_unpack_arr)
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
						$i ++;
					}

					eval("$self->{registered_callbacks}->{&CALLBACK_ENUMERATE}(\@return_arr)");
				}
			}

			if(scalar(@form_unpack_arr) == 1)
			{
				my @form_unpack_arr_0_arr = split('', $form_unpack_arr[0]);

				if(scalar(@form_unpack_arr_0_arr) > 1)
				{
					my @unpack_tmp_arr = unpack($form_unpack, $payload);

					if($form_unpack_arr_0_arr[0] eq 'a')
					{
						my @return_arr = split('', $unpack_tmp_arr[0]);
						eval("$self->{registered_callbacks}->{&CALLBACK_ENUMERATE}(\@return_arr)");
					}
					if($form_unpack_arr_0_arr[0] eq 'Z')
					{
						my @return_arr = @unpack_tmp_arr;
						eval("$self->{registered_callbacks}->{&CALLBACK_ENUMERATE}($return_arr[0])");
					}
					my @return_arr = @unpack_tmp_arr;
					eval("$self->{registered_callbacks}->{&CALLBACK_ENUMERATE}(\@return_arr)");
				}
				if(scalar(@form_unpack_arr_0_arr) == 1)
				{
					eval("$self->{registered_callbacks}->{&CALLBACK_ENUMERATE}(unpack($form_unpack, $payload))");
				}
			}
		}
		return 1;
	}

	if(!defined($self->{devices}->{$uid}))
	{
		return 1;
	}

	if(defined($self->{devices}->{$uid}->{registered_callbacks}->{$fid}))
	{
		my @callback_format_arr = split(' ', $self->{devices}->{$uid}->{callback_formats}->{$fid});

		if(scalar(@callback_format_arr) > 1)
		{
			my @callback_return_arr = unpack($self->{devices}->{$uid}->{callback_formats}->{$fid}, $payload);
			eval("$self->{devices}->{$uid}->{registered_callbacks}->{$fid}(\@callback_return_arr)");
		}

		if(scalar(@callback_format_arr) == 1)
		{
			my $_payload_unpacked = unpack($self->{devices}->{$uid}->{callback_formats}->{$fid}, $payload);
			eval("$self->{devices}->{$uid}->{registered_callbacks}->{$fid}($_payload_unpacked)");
		}

		if(scalar(@callback_format_arr) == 0)
		{
			eval("$self->{devices}->{$uid}->{registered_callbacks}->{$fid}()");
		}
	}

	return 1;
}

sub _disconnect_probe_thread_subroutine
{
	my ($self) = @_;

	$self->_init_local_socket();

	while(1)
	{
		my $data = $self->{disconnect_probe_queue}->dequeue_timed(&_DISCONNECT_PROBE_INTERVAL);

		if(defined($data) && $data == &_QUEUE_EXIT)
		{
			last;
		}

		if ($self->{disconnect_probe_flag}) {
			my $packet = $self->_create_packet_header(undef, 8, &_FUNCTION_DISCONNECT_PROBE);

			my $rc;
			eval
			{
				lock(${$self->{send_lock_ref}});

				$| = 1; # enable autoflush
				if (defined(&{"MSG_NOSIGNAL"}))
				{
					$rc = $self->_get_local_socket()->send($packet, MSG_NOSIGNAL);
				}
				else
				{
					$rc = $self->_get_local_socket()->send($packet);
				}
			};
			if(!defined($rc))
			{
				$self->_handle_disconnect_by_peer(&DISCONNECT_REASON_ERROR, $self->{socket_id}, 0);
				last;
			}
		}
		else
		{
			$self->{disconnect_probe_flag} = 1;
		}
	}

	return 1;
}

1;
