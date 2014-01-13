use 5.006;
use strict;
use warnings FATAL => 'all';
use ExtUtils::MakeMaker;

WriteMakefile(
    NAME                => 'Tinkerforge',
    AUTHOR              => q{Ishraq Ibne Ashraf <ishraq@tinkerforge.com>},
    VERSION_FROM        => './lib/Tinkerforge/IPConnection.pm',
    ABSTRACT_FROM       => './lib/Tinkerforge/IPConnection.pm',
    ($ExtUtils::MakeMaker::VERSION >= 6.3002
      ? ('LICENSE'=> 'perl')
      : ()),
    PL_FILES            => {},
    BUILD_REQUIRES => {
        'Test::More' => 0,
    },
    PREREQ_PM => {
        'Test::More' => 0,
        'Thread::Queue' => 3.02,
    },
    dist                => { COMPRESS => 'gzip -9f', SUFFIX => 'gz', },
    clean               => { FILES => 'Tinkerforge-*' },
);

