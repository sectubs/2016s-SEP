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
# @author Leonhard Schulze
# @author Paul Schmidt
# @author Johannes Heidtmann
# @brief This Class acts as a sink,
# getting IP/OT packets from a stream,
# converting them from OT to IP packets if a flag is set,
# and writing them to a given TUN Device
# @details TODO

import numpy as np
from gnuradio import gr
from tun_handler import TunHandler
from packet_handler import PacketHandler

class tun_sink_b(gr.sync_block):
    ##
    # Construct a new TUN Sink
    # @param tun_name Name of the TUN Device used
    # @param len_tag_key tag name used to detect packet lengths
    # @param use_ot_packets flag used to enable OT packet conversion
    def __init__(self, tun_name, len_tag_key, use_ot_packets):
        gr.tagged_stream_block.__init__(self,
                                        name="tun_sink_b",
                                        in_sig=[np.byte],
                                        out_sig=None,
                                        length_tag_name=len_tag_key)
    ##
    # Main work function called by GNURadio
    # @param input_items input streams
    # @param output_items output streams
    # @return number of byte processed
    def work(self, input_items, output_items):
        in0 = input_items[0]
        print "Paketlänge sink "+str(len(input_items[0]) )
        # signal processing
        return len(input_items[0])

