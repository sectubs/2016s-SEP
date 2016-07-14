## Ultrasonic Espionage made easy
A common and easy security network measure is to isolate a senstive computer from outside -- commonly known as an *Air gap*. There is no cable to this computer, no connection, nothing. However, the security team made one mistake, the computer has speakers and a microphone. Mallory, a smart hacker, achieved that OrcaTUN was installed with the operating system before isolating the sensitive computer. She is now able to obtain sensitive information continously by just using *inaudible* sound. Nobody would notice the security breach.

##OrcaTUN - Ultrasonic Networking
OrcaTUN -- developed by students of the Institute of System Security -- allows the user to connect to other computers by providing a standard network tunnel via TUN -- of course only for legitimate intentions. Regular applications like Netcat or SSH can communicate with each other just as they would do over the Internet. No special adaptions are necessary. OrcaTUN sends all the traffic to a specified IP through the speakers and in turn receives traffic trough the mircophone. 

###Usage
If you already installed OrcaTun, just open a terminal
and enter

`orcatun `

For a list of advanced options and help try

`orcatun -h`

or read the Manpage

`man orcatun`

##Installation
You can create a Package for Ubuntu by running 

`./build_package.sh ` 

in the package Folder.


Alternatively you can copy all the files to their places
by running 

`./install.sh`

in the Orcatun folder.
This is mostly useful for developement.

###Dependencies

1. python2.7
2. python-pip2
3. Gnuradio >= 3.7.9
4. swig

All these packages are available in Ubuntu 16.04's official sources.

Python2.7 is included with Ubuntu by default.
You can install the others using:

`# apt install python-pip2 gnuradio swig`

Additionally you need to install [pytun](https://github.com/montag451/pytun)
and [dpkt](https://pypi.python.org/pypi/dpkt) using pip:

`# pip2 install python-pytun dpkt`

We also recommend dedicated microphones and speakers.

###Documentation
We used Doxygen-Style comments for our code.
To generate detailed documentation, you can run 

`doxygen Doxyfile`

in the doc Folder.

###License
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.

For detailed info see LICENSE.
