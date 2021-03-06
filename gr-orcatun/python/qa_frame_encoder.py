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
# @author Paul Schmidt
# @brief Tests the Frame Encoder based on its output
# @details Based on the input the frame will be checked on correctness
#          by different factors like the saved payload and payload length


from gnuradio import gr, gr_unittest
from gnuradio import blocks
from frame_encoder import frame_encoder
from struct import *

class qa_frame_encoder (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None
    
    ##
    # Check if the encoder constructs a correct frame
    # @param payload The given payload
    # @param access_code The access code to use 
    def check_frame(self, payload, access_code, enable_crc):
        
        ##
        # Print Info
        print "----------------------------------------------------------------------"
        print "Testing with:"
        print "Payload: ", payload
        print "Access code: ", access_code
        print "CRC enabled: ", enable_crc
        
        if enable_crc:
            crc_length = 4
        else:
            crc_length = 0
        
        ##
        # Set up BlockS
        src = blocks.vector_source_b(payload)
        to_tagged_stream = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 
                                  len(payload), "packet_len")
        encoder = frame_encoder("packet_len", enable_crc)
        dst = blocks.vector_sink_b()
        
        ##
        # Connect Blocks
        self.tb.connect(src,to_tagged_stream)
        self.tb.connect(to_tagged_stream, encoder)
        self.tb.connect(encoder, dst)
        self.tb.run ()
        
        
        ##
        # Check access code
        result_data = dst.data()
        self.assertEqual(result_data[2:10], access_code,
                        "Access code wrong")
        print "Access code correct."
        
        ##
        # Check Payload
        self.assertEqual(result_data[14:(14 + len(payload))],
                         payload, "Payload wrong")
        print "Payload correct."
        
        ##
        # Extract LSB-Length from header and form convert to MSB
        length_rev = result_data[10]
        i = 0
        length = 0
        while i < 8:
            length = (length<<1)|(length_rev>>i & 0x1)
            i = i+1
        
        ##
        # Check Payload length in header
        self.assertEqual((length-crc_length), len(payload),
                         "Payload length wrong")
        print "Payload length correct."
    
    
    def test_001_t (self):
        # set up fg
        payload = (3, 4, 5, 2, 3, 5, 7)
        access_code = (172, 221, 164, 226, 242, 140, 32, 252)
        self.check_frame(payload, access_code, True)
    
    def test_002_t (self):
        payload = (3, 4, 5)
        access_code = (172, 221, 164, 226, 242, 140, 32, 252)
        self.check_frame(payload, access_code, False)
    
    def test_003_t (self):
        payload = (1,2)
        access_code = (172, 221, 164, 226, 242, 140, 32, 252)
        self.check_frame(payload, access_code, True)

if __name__ == '__main__':
    gr_unittest.run(qa_frame_encoder, None)
