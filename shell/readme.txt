This zip contains a Python script to interact with all Tinkerforge Bricks
and Bricklets (tinkerforge), a corresponding Bash Completion script
(tinkerforge-bash-completion.sh) and all available Shell examples (in examples/).

To get Bash Completion to work the tinkerforge script has to be in PATH and
the Bash Completion Script tinkerforge-bash-completion.sh has to be in
/etc/bash_completion.d/.

All examples are meant for typical Unix shells such as Bash. They will work
on Linux and Mac OS X as they are. There are Bash ports for Windows that allow
to run the examples unmodified, too.

If the examples should be used from the Windows Command Prompt cmd.exe then
the shebang line #!/bin/sh has to be removed and all lines starting with
tinkerforge have to be prefixed with python. So this:

 #!/bin/sh
 tinkerforge enumerate

becomes this:

 python tinkerforge enumerate

Finally, the file extension has to be changed from .sh to .bat or .cmd.

Documentation for the API can be found at http://www.tinkerforge.com/en/doc/index.html
