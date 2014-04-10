Tinkerforge Perl Bindings
=========================

This ZIP contains the Perl support for all Tinkerforge Bricks and Bricklets
(Tinkerforge.tar.gz), the source of the CPAN package (source/) and all available
Perl examples (examples/).

There are known deadlock problems on Windows with Strawberry Perl and Active
State Perl. The recommended workaround is to use Cygwin's Perl that doesn't
suffer from this problem (see http://perlmonks.org/?node_id=1078634).

A CPAN package will be available soon. Then it will be possible to install
the Perl bindings support from CPAN.

Yon can also install the local version of the CPAN package by unpacking
Tinkerforge.tar.gz and running the following commands:

 perl Makefile.PL
 make
 make test
 make install

You can also use the source directly, just create a folder for your project and
copy the Tinkerforge/ folder from source/ and the example you want to try in
there (e.g. the Stepper configuration example from,
examples/brick/stepper/example_configuration.pl)

 example_folder/
  -> Tinkerforge/
  -> example_configuration.pl

You have to add a line on top of the file example_configuration.pl:

 use lib './';

After that, the example can be executed again.

API Documentation and Examples
------------------------------

Links to the API documentation for the IP Connection, Bricks and Bricklets as
well as the examples from this ZIP file can be found at

 http://www.tinkerforge.com/en/doc/Software/API_Bindings_Perl.html#api-documentation-and-examples
