use 5.006;
use strict;
use warnings FATAL => 'all';
use ExtUtils::MakeMaker;

WriteMakefile(
    NAME                => 'Tinkerforge',
    AUTHOR              => q{Ishraq Ibne Ashraf <ishraq@tinkerforge.com>},
    VERSION_FROM        => 'lib/Tinkerforge.pm',
    ABSTRACT_FROM       => 'lib/Tinkerforge.pm',
    LICENSE             => 'Public Domain (CC0 1.0)',
    BUILD_REQUIRES => {
        'Test::More' => 0,
    },
    PREREQ_PM => {
        'Test::More' => 0,
        'Thread::Queue' => 3.02,
        'Thread::Semaphore' => 0,
        'IO::Socket::INET' => 0,
    },
    dist                => { COMPRESS => 'gzip -9f', SUFFIX => 'gz', },
    clean               => { FILES => 'Tinkerforge-*' },
);

