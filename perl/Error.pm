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

# overloading function stringify()
use overload ('""' => 'stringify');

# the constructor
sub new
{
    my ($class, $code, $message) =  @_;
    my $self = {code => $code, message => $message};
    bless($self, $class);

    return $self;
}

# function stringify() to overload with
sub stringify
{
    my $self = shift;

    return shortmess($self->{message});
}

1;
