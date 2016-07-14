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
# @brief Tests the Frame decoder by comparing the output with the encoders
#        input
# @details The decoder is linked with the encoder. The output of the decoder
#          will be compared with the input of the encoder

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from frame_decoder import frame_decoder
from frame_encoder import frame_encoder

class qa_frame_decoder (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None
    
    ##
    # Test decoder with given payload and access code
    # @param payload The given payload
    # @param access_code  The access code of the decoder 
    def check_frame(self, payload, access_code, enable_crc):
        
        ##
        # Print Info
        print "----------------------------------------------------------------------"
        print "Testing with:"
        print "Payload: ", payload
        print "Access code: ", access_code
        print "CRC enabled: ", enable_crc
        
        ##
        # Set up Blocks
        src = blocks.vector_source_b(payload)
        to_tagged_stream = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 
                                  len(payload), "packet_len")
        encoder = frame_encoder("packet_len", enable_crc)
        repacker = blocks.repack_bits_bb(8, 1, "", False, gr.GR_MSB_FIRST)
        decoder = frame_decoder("frame_len", 48000, enable_crc)
        dst = blocks.vector_sink_b()
        
        ##
        # Connect Blocks
        self.tb.connect(src,to_tagged_stream)
        self.tb.connect(to_tagged_stream, encoder)
        self.tb.connect(encoder, repacker)
        self.tb.connect(repacker, decoder)
        self.tb.connect(decoder, dst)
        self.tb.run ()
        
        ##
        # Check, if received payload matches original payload
        self.assertEqual(payload, dst.data(), "Received Payload does not match with original")
        print "Frame correct."
        
    def test_001_t (self):
        # set up fg
        payload = (3, 4, 5, 2, 3, 5, 7)
        access_code = (172, 221, 164, 226, 242, 140, 32, 252)
        self.check_frame(payload, access_code, False)
        
    def test_002_t (self):
        # set up fg
        payload = (3, 4)
        access_code = (172, 221, 164, 226, 242, 140, 32, 252)
        self.check_frame(payload, access_code, False)
        
    def test_003_t (self):
        # set up fg
        payload = (3, 4, 5, 2, 3, 5, 7, 9, 10, 254)
        access_code = (172, 221, 164, 226, 242, 140, 32, 252)
        self.check_frame(payload, access_code, True)


if __name__ == '__main__':
    gr_unittest.run(qa_frame_decoder, None)
