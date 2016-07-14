#!/usr/bin/python2.7
import dpkt
##
# @author Johannes Heidtmann
# @brief This class provides an OrcaTUN Packet format used to transmit IP Packet data with less overhead
# @details Since OrcaTUN is used for simple Point2Point connections, many information defined in the IP header
# aren't needed and might be stripped off, reducing the header size to 5 byte (IP header are at >= 20 byte)
class OT(dpkt.Packet):
    ## list of tuples describing the OT header
    __hdr__ = (
        ('id', 'H', 0),
        ('off', 'H', 0),
        ('p', 'B', 0)
    )

    @property
    def rf(self):
        return (self.off >> 15) & 0x1

    @rf.setter
    def rf(self, rf):
        self.off = (self.off & ~dpkt.ip.IP_RF) | (rf << 15)

    @property
    def df(self):
        return (self.off >> 14) & 0x1

    @df.setter
    def df(self, df):
        self.off = (self.off & ~dpkt.ip.IP_DF) | (df << 14)

    @property
    def mf(self):
        return (self.off >> 13) & 0x1

    @mf.setter
    def mf(self, mf):
        self.off = (self.off & ~dpkt.ip.IP_MF) | (mf << 13)

    @property
    def offset(self):
        return (self.off & dpkt.ip.IP_OFFMASK) << 3

    @offset.setter
    def offset(self, offset):
        self.off = (self.off & ~dpkt.ip.IP_OFFMASK) | (offset >> 3)
