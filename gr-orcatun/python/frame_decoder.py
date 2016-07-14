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
# @brief Extracts paylout out of frame stream
# @details Hierarchical block for the frame decoding of OrcaTUN.
#    Creates a tagged stream with the payload of frames.
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
import orcatun

class frame_decoder(gr.hier_block2):
    """
    Hierarchical block for the frame decoding of OrcaTUN.
    Creates a tagged stream with the payload of frames.
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
        - samp_rate The sample rate
    
    Input: Frames in unpacked bytes with one relevant bit
    Output: Packed payload
    """
    def __init__(self,len_tag_key, samp_rate, enable_crc):
        gr.hier_block2.__init__(self,
            "frame_decoder",
            gr.io_signature(1, 1, gr.sizeof_char),  # Input signature
            gr.io_signature(1, 1, gr.sizeof_char)) # Output signature
            
        self.len_tag_key = len_tag_key
        self.samp_rate = samp_rate
        
        # Set correlator. FIXME Modifiable access code
        self.digital_correlate_access_code_tag_bb_0 \
            = digital.correlate_access_code_tag_bb(
            "1010110011011101101001001110001011110010100011000010000011111100",
             0, "access")
        
        self.digital_header_payload_demux_0 = digital.header_payload_demux(
    	  32,           # header size
    	  1,            # bits per symbol
    	  0,            # guard interval
    	  len_tag_key, # length tag key
    	  "access",     # trigger tag key
    	  False,        # no idea
    	  gr.sizeof_char, # item format
    	  "rx_time",    # timing tag key (irrelevant)
              samp_rate, # sample rate
              (""),     # special tag keys
        )
        
        self.digital_packet_headerparser_b_default_0  \
            = digital.packet_headerparser_b(32, len_tag_key)
        
        self.blocks_repack_bits_bb_0  \
            = blocks.repack_bits_bb(1, 8, len_tag_key, 
                                    False, gr.GR_MSB_FIRST)
        if enable_crc:
            self.digital_crc32_bb_0  \
                = digital.crc32_bb(True, len_tag_key, True)
        
        # Debug
        self.tag_debug_correlator = blocks.tag_debug(gr.sizeof_char*1, 
                                    "Access code found.", "access");
        #self.tag_debug_header = blocks.tag_debug(gr.sizeof_char*1, 
        #                            "Header correctly obtained", len_tag_key);
        self.tag_debug_packet = blocks.tag_debug(gr.sizeof_char*1, 
                                    "Packet correctly obtained.", len_tag_key);
        
        # Debug Message after the header was found 
        #self.blocks_message_debug_0 = blocks.message_debug()
        #self.blocks_tagged_stream_to_pdu_0 \
        #    = blocks.tagged_stream_to_pdu(blocks.byte_t, len_tag_key)
        
        # PDU Tag Multiplier
        self.multiplay_length = orcatun.multiply_length_pdu(len_tag_key)
        
        ##################################################
        # Connections
        ##################################################
        
        # Correlator to Header/Payload Demux
        # Correlator triggers the HPD with stream tags
        self.connect((self.digital_correlate_access_code_tag_bb_0, 0), 
                     (self.digital_header_payload_demux_0, 0))
        
        self.connect((self.digital_correlate_access_code_tag_bb_0, 0),
                     (self.tag_debug_correlator,0))
        
        # HPD to Header Parser
        # Extracts the information from the header...
        self.connect((self.digital_header_payload_demux_0, 0), 
                     (self.digital_packet_headerparser_b_default_0, 0))
        
        # ... and pass it back to the HPD
        #self.msg_connect((self.digital_packet_headerparser_b_default_0, 
        #                  'header_data'), 
        #                 (self.digital_header_payload_demux_0, 
        #                  'header_data'))
        self.msg_connect((self.digital_packet_headerparser_b_default_0,
                          'header_data'),
                         (self.multiplay_length, 'in'))
        self.msg_connect((self.multiplay_length, 'out'),
                         (self.digital_header_payload_demux_0, 
                          'header_data'))
        
        
        # HPD payload to Repacker
        self.connect((self.digital_header_payload_demux_0, 1), 
                     (self.blocks_repack_bits_bb_0, 0))
        
        # Repacker to Stream CRC32
        # to check the CRC
        if enable_crc:
            self.connect((self.blocks_repack_bits_bb_0, 0), 
                         (self.digital_crc32_bb_0, 0))
        
        
        # Connect input and output
        self.connect((self,0), (self.digital_correlate_access_code_tag_bb_0, 0))
        if enable_crc:
            self.connect((self.digital_crc32_bb_0, 0), (self,0))
        else:
            self.connect((self.blocks_repack_bits_bb_0, 0), (self,0))
        
        
        # Debug
        if enable_crc:
            self.connect((self.digital_crc32_bb_0, 0), (self.tag_debug_packet, 0))
        
        #self.connect((self.blocks_repack_bits_bb_0, 0), (self.tag_debug_header,0))
        
        
        # Debug print whole packet. Regardless if CRC was correct or not.
        #self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_tagged_stream_to_pdu_0,0))
        #self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), 
        #    (self.blocks_message_debug_0, 'print_pdu'))
        #self.msg_connect((self.digital_packet_headerparser_b_default_0,'header_data'), 
        #    (self.blocks_message_debug_0, 'print_pdu'))
