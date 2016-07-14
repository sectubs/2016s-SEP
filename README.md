##OrcaTUN - Ultrasonic Networking
OrcaTUN allows the user to connect to other Computers using
Sound. It sends all the Traffic to a specified IP through
the Speakers and receives trough the Mircophone.

###Usage
If you already installed OrcaTun just open a Terminal
and enter

`orcatun `

For a List of advanced Options and help try

`orcatun -h`

or read the Manpage

`man orcatun`

##Installation
You can create a Package for Ubuntu by running 

`./build_package.sh ` 

in the package Folder.


Alternatively you can copy all the Files to their Places
by running 

`./install.sh`

in the Orcatun Folder.
This is mostly useful for Developement.

###Dependencies

1. python2.7
2. python-pip2
3. Gnuradio >= 3.7.9
4. swig

All these Packages are available in Ubuntu 16.04's official Sources.

Python2.7 is included with Ubuntu by default.
You can install the others using:

`# apt install python-pip2 gnuradio swig`

Additionally you need to install [pytun](https://github.com/montag451/pytun)
and [dpkt](https://pypi.python.org/pypi/dpkt) using pip:

`# pip2 install python-pytun dpkt`

We also reccomend dedicated Microphones and Speakers.

###Documentation
We used Doxygen-Style Comments for our code.
To gernerate detailed Documentation you can run 

`doxygen Doxyfile`

in the doc Folder.

###License
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.

For detailed info see LICENSE.
