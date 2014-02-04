This ZIP contains a script to interact with all Tinkerforge Bricks and
Bricklets (tinkerforge), a corresponding Bash Completion script
(tinkerforge-bash-completion.sh) and all available Shell examples (in
examples/).

To get Bash Completion to work the tinkerforge script has to be in PATH. For
example by copying it to /usr/local/bin/. The Bash Completion script
tinkerforge-bash-completion.sh has to be in /etc/bash_completion.d/. Bash
Completion can then be reloaded by:

 . /etc/bash_completion

All examples are meant for typical Unix shells such as Bash. They will work
on Linux and Mac OS X as they are. There are Bash ports for Windows that allow
to run the examples unmodified, too.

Documentation for the API can be found at

 http://www.tinkerforge.com/en/doc/Software/API_Bindings_Shell.html#api-documentation-and-examples
