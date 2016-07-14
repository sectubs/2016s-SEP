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

import numpy as np
from gnuradio import gr
import dpkt
from tun_handler import TunHandler
from packet_handler import PacketHandler
import pmt


##
# @author Johannes Heidtmann
# @author Paul Schmidt
# @author Leonhard Schulze
# @brief This Class acts as a source,
# getting IP packets from a TUN Device and writing them to a stream,
# converting them to OT packets if a flag is set
# @details TODO
class tun_source_b(gr.sync_block):
    ##
    # Construct a new TUN Source
    # @param tun_handler TunHandler instance used
    # @param len_tag_key tag name used to mark packet lengths
    # @param use_ot_packets flag used to enable OT packet conversion
    def __init__(self, tun_handler, len_tag_key, use_ot_packets):
        gr.sync_block.__init__(self,
                               name="tun_source_b",
                               in_sig=None,
                               out_sig=[np.byte])
        self.tun_handler = tun_handler #TunHandler(tun_name)
        self.len_tag_key = len_tag_key
        self.use_ot_packets = use_ot_packets

    ##
    # Main work function called by GNURadio
    # @param input_items input streams
    # @param output_items output streams
    # @return number of byte processed
    def work(self, input_items, output_items):
        out = output_items[0]

        # Get single IP packet from TUN Device
        buf = self.tun_handler.read()
        if self.use_ot_packets:
            # Create smaller OT packet from IP packet
            #packet = PacketHandler.to_ot(buf[4:])
            packet = PacketHandler.to_ot(buf)
        else:
            #packet = dpkt.ip.IP(buf[4:])
            packet = dpkt.ip.IP(buf)

        # TODO: DEBUG message, remove in production
        print "TUN Source: ", PacketHandler.show(packet)

        # Write packet to output buffer
        result = np.fromstring(str(packet), dtype=np.uint8)
        print "Packetlänge source "+ str(len(result))
        out[:len(result)] = result

        # Write length tag to output buffer
        self.add_item_tag(0, self.nitems_written(0),
                          pmt.string_to_symbol(self.len_tag_key),
                          pmt.from_long(len(result)),
                          pmt.PMT_NIL)

        return len(result)
