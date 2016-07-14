#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: tun_source Test
# Author: Johannes Heidtmann
# Generated: Mon Jul  4 13:52:58 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import orcatun
import wx


class tun_source_test(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="tun_source Test")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Blocks
        ##################################################
        self.orcatun_tun_source_b_0 = orcatun.tun_source_b("tun3", "packet_len", True)
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "packet_len")
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_char*1, "tun_source_debug", ""); self.blocks_tag_debug_0.set_display(True)
        self.blocks_message_debug_0 = blocks.message_debug()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.blocks_message_debug_0, 'print_pdu'))    
        self.connect((self.orcatun_tun_source_b_0, 0), (self.blocks_tag_debug_0, 0))    
        self.connect((self.orcatun_tun_source_b_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))    


def main(top_block_cls=tun_source_test, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
