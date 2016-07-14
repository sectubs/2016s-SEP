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
# @brief Creates frames out of a tagged stream
# @details Hierarchical block for the frame encoding of OrcaTUN.
#    Creates frames out of a tagged stream.
#    One Frame consists of:
#        - An access code (up to 64 bit)
#        - A header from the default packet header generator
#            - Bits 0-11: Frame length
#            - Bits 12-23: Sequence number
#            - Bits 24-31: 8-Bit CRC for the header
#        - Payload
#        - CRC32
#   Furthermore, two garbage bytes are added at the start and at the front
#    and at the end.

from gnuradio import gr, digital, blocks

class frame_encoder(gr.hier_block2):
    # FIXME Add Whitening/Scramblingto randomize the output
    #       and thus achieve better demodulation
    # FIXME Modifiable access code 
    """
    Hierarchical block for the frame encoding of OrcaTUN.
    Creates frames out of a tagged stream.
    One Frame consists of:
        - An access code (up to 64 bit)
        - A header from the default packet header generator
            - Bits 0-11: Frame length
            - Bits 12-23: Sequence number
            - Bits 24-31: 8-Bit CRC for the header
        - Payload
        - CRC32
    
    Furthermore, two garbage bytes are added at the start and at the front
    and at the end.
    
    Args:
        - len_tag_key The tag key holding the length
    
    Input: Packed bytes with stream tags and the payload length
    Output: Described frames 
    """
    ##
    # Construct a new Frame Encoder
    # @param len_tag_key The stream tag holding the frame size
    def __init__(self, len_tag_key, enable_crc):
        gr.hier_block2.__init__(self,
            "frame_encoder",
            gr.io_signature(1, 1, gr.sizeof_char),  # Input signature
            gr.io_signature(1, 1, gr.sizeof_char)) # Output signature
        
        self.len_tag_key = len_tag_key
        
        # For header creation
        self.digital_packet_headergenerator_bb_default_0 \
                = digital.packet_headergenerator_bb(32, self.len_tag_key)
        
        # Place CRC 32bit after payload
        if enable_crc:
            self.digital_crc32_bb_0 = digital.crc32_bb(False, self.len_tag_key, 
                                                       True)
        
        # Tagged stream blocks
        
        # Combine access code, header and payload
        self.blocks_tagged_stream_mux_0  \
                = blocks.tagged_stream_mux(gr.sizeof_char*1, self.len_tag_key, 0)
        
        # Multiply Size in payload stream
        #self.blocks_tagged_stream_multiply_length_0 \
        #        = blocks.tagged_stream_multiply_length(gr.sizeof_char*1, 
        #                                               self.len_tag_key, 8)
        
        self.blocks_stream_to_tagged_stream_1 \
                = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 64, 
                                                 self.len_tag_key)
        
        # Repacker
        self.blocks_repack_bits_bb_garbage  \
            = blocks.repack_bits_bb(8, 1, "", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_access  \
            = blocks.repack_bits_bb(8, 1, "", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_payload  \
            = blocks.repack_bits_bb(8, 1, len_tag_key, False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_complete  \
            = blocks.repack_bits_bb(1, 8, "", False, gr.GR_MSB_FIRST)
        
        self.access_code_vector  \
            = blocks.vector_source_b((172, 221, 164, 226,242, 140, 32, 252), 
                                      True, 1, [])
        
        # Debug
        # Print complete Payload with packet
        #self.blocks_message_debug_0 = blocks.message_debug()
        #self.blocks_tagged_stream_to_pdu_0 \
        #    = blocks.tagged_stream_to_pdu(blocks.byte_t, len_tag_key)
        
        
        # Garbage bytes
        self.garbage_vector  \
            = blocks.vector_source_b((159, 200), 
                                      True, 1, [])
        self.stream_to_tagged_garbage \
                = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 16, 
                                                 self.len_tag_key)
        
        ##################################################
        # Connections
        ##################################################
        
        # Garbage up front
        
        self.connect((self.garbage_vector, 0), 
                     (self.blocks_repack_bits_bb_garbage, 0))
        
        self.connect((self.blocks_repack_bits_bb_garbage, 0), 
                     (self.stream_to_tagged_garbage, 0))
        
        self.connect((self.stream_to_tagged_garbage, 0), 
                     (self.blocks_tagged_stream_mux_0, 0))
        
        # And at the back
        self.connect((self.stream_to_tagged_garbage, 0), 
                     (self.blocks_tagged_stream_mux_0, 4))
        
        # Access code path
        
        self.connect((self.access_code_vector, 0), 
                     (self.blocks_repack_bits_bb_access, 0))
        
        self.connect((self.blocks_repack_bits_bb_access, 0), 
                     (self.blocks_stream_to_tagged_stream_1, 0))
        
        self.connect((self.blocks_stream_to_tagged_stream_1, 0), 
                     (self.blocks_tagged_stream_mux_0, 1))
        
        # Payload path
        
        if enable_crc:
            self.connect((self.digital_crc32_bb_0, 0), 
                         (self.blocks_repack_bits_bb_payload, 0))
        
        
        self.connect((self.blocks_repack_bits_bb_payload, 0), 
                     (self.blocks_tagged_stream_mux_0, 3))
        if enable_crc:
            self.connect((self.digital_crc32_bb_0, 0), 
                         (self.digital_packet_headergenerator_bb_default_0, 0))
        
        # Debug
        # Print complete packet with payload
        #if enable_crc:
        #    self.connect((self.digital_crc32_bb_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        #else:
        #    self.connect((self, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        
        #self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), 
        #                 (self.blocks_message_debug_0, 'print_pdu'))
            
        
        
        # Header path
        
        self.connect((self.digital_packet_headergenerator_bb_default_0, 0), 
                     (self.blocks_tagged_stream_mux_0, 2))
        
        # Output
        
        self.connect((self.blocks_tagged_stream_mux_0, 0), 
                     (self.blocks_repack_bits_bb_complete, 0))
        
        # Connect Input and out
        if enable_crc:
            self.connect((self,0), (self.digital_crc32_bb_0, 0))
        else:
            self.connect((self,0), (self.digital_packet_headergenerator_bb_default_0, 0))
            self.connect((self,0), (self.blocks_repack_bits_bb_payload, 0))
        
        self.connect((self.blocks_repack_bits_bb_complete, 0), (self,0))
        
