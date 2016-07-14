#!/usr/bin/python2.7
from pytun import TunTapDevice, IFF_TUN, IFF_NO_PI
import logging
import sys


##
# @author Leonhard Schulze, Johannes Heidtmann
# @brief Provides a wrapper for the persistent TUN Device with advanced functions
# @details TODO: mehr.


class TunHandler(object):
    ##
    # Construct a new TunHandler
    # @param name Name of the TUN Device being used
    def __init__(self, name):
        log = logging.getLogger('master.packet_handler')
        try:
            # Create TunTapDevice with name specified by constructor and TUN/NoPacketInfo flags
            self.tun = TunTapDevice(name=name, flags=(IFF_TUN | IFF_NO_PI))
        except Exception as e:
            log.error('Unable to open TUN Device. ' + str(e))
            sys.exit(-1)

        self.tun.mtu = 1200
        self.tun.up()
        log.info("TUN Device successfully opened")

    ##
    # Close the TUN device gracefully (requires root)
    def kill(self):
        log = logging.getLogger('master.TunHandler')
        self.tun.down()
        log.info("TUN Device successfully closed")

    ##
    # Read an IP packet from the device
    def read(self):
        buf = self.tun.read(self.tun.mtu)
        return buf

    ##
    # Send an IP packet to the device
    # @param buf The packet to be send in Plaintext
    def write(self, buf):
        print(buf)
        self.tun.write(buf)

    ##
    # Configure IP addresses of persistent TUN device (requires root)
    # @param src Local IP address
    # @param dst Destination IP address
    # @staticmethod
    def set_ip_adresses(self, local, dst):
        self.tun.addr = local
        self.tun.dstaddr = dst