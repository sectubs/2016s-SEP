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

import numpy
from gnuradio import gr
import pmt

class multiply_length_pdu(gr.sync_block):
    """
    Multiplies the value of len_tag_key by 8
    """
    def __init__(self, len_tag_key):
        gr.sync_block.__init__(self,
            name="multiply_length_pdu",
            in_sig=None,
            out_sig=None)
        
        self.len_tag_key = len_tag_key
        
        # Set up message port
        self.msg_buf_in = pmt.intern("in")
        self.message_port_register_in(self.msg_buf_in)

        self.msg_buf_out = pmt.intern("out")
        self.message_port_register_out(self.msg_buf_out)

        self.set_msg_handler(self.msg_buf_in, self.handle_msg)

    ##
    # Multiplies the len_tag_key value of a pdu by 8
    # @param msg incoming message
    def handle_msg(self, msg):
        if pmt.dict_has_key(msg, pmt.intern(self.len_tag_key)):
            packet_len = pmt.to_python(msg)[self.len_tag_key]
            msg = pmt.dict_delete(msg, pmt.intern(self.len_tag_key))
            msg = pmt.dict_add(msg, pmt.intern(self.len_tag_key), pmt.from_long(packet_len * 8))
            
        self.message_port_pub(self.msg_buf_out, msg)

    ##
    # Legacy gr.sync_block work function, doesn't get called as we don't have sources/sinks
    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        out[:] = in0
        return len(output_items[0])

