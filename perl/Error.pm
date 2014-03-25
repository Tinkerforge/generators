# Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
# Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>
#
# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

=pod

=encoding utf8

=head1 NAME

Tinkerforge::Error - Used for all error reporting

=cut

# package definition
package Tinkerforge::Error;

# using modules
use strict;
use warnings;
use Carp qw(shortmess);
$Carp::Internal{ (__PACKAGE__) }++;

=head1 CONSTANTS

=over
=cut

=item ALREADY_CONNECTED

Possible return value of the get_code() subroutine.

=cut

use constant ALREADY_CONNECTED => 11;

=item NOT_CONNECTED

Possible return value of the get_code() subroutine.

=cut

use constant NOT_CONNECTED => 12;

=item CONNECT_FAILED

Possible return value of the get_code() subroutine.

=cut

use constant CONNECT_FAILED => 13;

=item NO_THREAD

Possible return value of the get_code() subroutine.

=cut

use constant NO_THREAD => 14;

=item INVALID_FUNCTION_ID

Possible return value of the get_code() subroutine.

=cut

use constant INVALID_FUNCTION_ID => 21;

=item TIMEOUT

Possible return value of the get_code() subroutine.

=cut

use constant TIMEOUT => 31;

=item INVALID_PARAMETER

Possible return value of the get_code() subroutine.

=cut

use constant INVALID_PARAMETER => 41;

=item FUNCTION_NOT_SUPPORTED

Possible return value of the get_code() subroutine.

=cut

use constant FUNCTION_NOT_SUPPORTED => 42;

=item UNKNOWN_ERROR

Possible return value of the get_code() subroutine.

=cut

use constant UNKNOWN_ERROR => 43;

=back
=cut

# overloading function stringify()
use overload ('""' => '_stringify');

=head1 FUCNTIONS

=over
=cut

# the constructor
sub _new
{
    my ($class, $code, $message) =  @_;
    my $self = {code => $code, message => $message};
    bless($self, $class);

    return $self;
}

# function stringify() to overload with
sub _stringify
{
    my $self = shift;

    return shortmess($self->{message});
}

=item get_code()

Returns the code of this error.

=cut

sub get_code
{
	my ($self) = @_;

	return $self->{code};
}

=item get_message()

Returns the message of this error.

=cut

sub get_message
{
	my ($self) = @_;

	return $self->{message};
}

=back
=cut

1;
