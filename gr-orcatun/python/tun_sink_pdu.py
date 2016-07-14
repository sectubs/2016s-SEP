#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#
# @author Johannes Heidtmann
# @brief This Class acts as a sink,
# getting IP/OT packets from pdu messages,
# converting them from OT to IP packets if a flag is set,
# and writing them to a given TUN Device
# @details TODO

from gnuradio import gr
import pmt
import dpkt
from packet_handler import PacketHandler
from tun_handler import TunHandler

class tun_sink_pdu(gr.sync_block):
    ##
    # Construct a new TUN Sink
    # @param tun_handler TunHandler instance used
    # @param use_ot_packets flag used to enable OT packet conversion
    def __init__(self, tun_handler, use_ot_packets):
        gr.sync_block.__init__(self,
                               name="tun_sink_pdu",
                               in_sig=None,
                               out_sig=None)

        self.tun_handler = tun_handler
        self.use_ot_packets = use_ot_packets

        # Set up message port
        self.msg_buf_in = pmt.intern("packet")
        self.message_port_register_in(self.msg_buf_in)
        self.set_msg_handler(self.msg_buf_in, self.handle_msg)

    ##
    # Function called by GNURadio on arrival of new messages,
    # actual work happens here
    # @param msg incoming message
    def handle_msg(self, msg):
        buf = pmt.to_python(msg)[1]
        # Cast numpy buf to string to prevent doomsday
        buf = ''.join(map(chr, buf))
        if self.use_ot_packets:
            addr = self.tun_handler.tun.addr
            dstaddr = self.tun_handler.tun.dstaddr

            packet = PacketHandler.to_ip(buf, dstaddr, addr)
        else:
            packet = dpkt.ip.IP(buf)

        # TODO: DEBUG message, remove in production
        print "TUN Sink: ", PacketHandler.show(packet)

        # Write packet to TUN Device
        #print len(str(packet))
        # TODO:  IFF_NO_PI (remove 4 byte)
        #self.tun_handler.write(' ' * 4 + str(packet))
        self.tun_handler.write(str(packet))

    ##
    # Legacy gr.sync_block work function, doesn't get called as we don't have sources/sinks
    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        out[:] = in0
        return len(output_items[0])
