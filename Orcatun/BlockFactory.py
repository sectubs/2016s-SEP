from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import wxgui
from gnuradio import gr
from grc_gnuradio import wxgui as grc_wxgui
from gnuradio.wxgui import fftsink2
from grc_gnuradio import blks2 as grc_blks2
from gnuradio.filter import firdes
import ConfigParser
import logging
# import tunsink
# import tunsource
import wx
import sys
import orcatun
from gnuradio.wxgui import waterfallsink2
from gnuradio.fft import window

#used for debug
from optparse import OptionParser
from gnuradio.eng_option import eng_option

#TODO:
# 1. Implement new protocol standarts (always)

##
# Builds blocks used for audio transmission
# @author : Marcel Dube
# @brief This class generates blocks used to build protocol blocks
class BlockFactory:
    
    ##
    # Initialize BlockFactory
    # and set some Variables for the Resulting Blocks
    # @param config OrcaTUNs config Object
    # @param tun_handler A TunHandler Object
    # @param tk_context A tk_context 
    def __init__(self, config, tun_handler, tk_context):
        ## The calling OrcaTUN Instance's config
        self.config = config
        ## The TunHandler to be used in the Flowgraphs
        self.tun_handler = tun_handler
        ## A tk Frame, used to display Graphs
        self.tk_context = tk_context

        self.waterfall = config.showWaterfall
        self.FFTIN = config.showFFTin
        self.FFTOUT = config.showFFTout

        ## Transition width between permitted bandwith and blocked bandwith
        self.transistion = transistion = 100
        ## Samples per Symbol 
        self.sps = sps = 5
        ## Bandwidth to be passed through when receiving
        self.sideband_rx = sideband_rx = 100
        ## Bandwidth to be passed through when sending
        self.sideband = sideband = 1000
        ## Payload Length (Bytes)
        self.payload = payload = 21
        ## Interpolation
        self.interpolation_lvl = self.config.getInterFactor()
        ## Array of Factors to be used by the Resamplers
        self.interpolation_values = self.get_resampler_values(self.interpolation_lvl)
        #Sampl rate
        self.samp_rate = samp_rate = config.getSamplingRate()#48000
        
	#TOREMOVE
        self._crcpolynom_config = ConfigParser.ConfigParser()
        
        self._crcpolynom_config.read("default")
        try: crcpolynom = self._crcpolynom_config.get("main", "key")
        except: crcpolynom = "0001000000100001"
        self.crcpolynom = crcpolynom
        ## Receiving Frequency
        self.carrier_b = carrier_b = self.config.getReceiveFreq()
        ## Sending Frequency
        self.carrier_a = carrier_a = self.config.getTransmitFreq()
        
	#ToRemove
        self._accesscode_config = ConfigParser.ConfigParser()
        
        self._accesscode_config.read("default")
        try: accesscode = self._accesscode_config.get("main", "key")
        except: accesscode = "1010110011011101101001001110001011110010100011000010000011111100"
        ## Accesscode
        self.accesscode = accesscode
        
        #DEBUG
        self.blocks_message_debug_0 = blocks.message_debug()

	self.ot = str(self.config.getOt())
	self.crc = True

    ##############################################################################################
    # Top blocks
    # Creates already assmbled top_blocks to use within protocoll
    ##############################################################################################

    def omniblock(self):
        log = logging.getLogger('master.BlockFactory')
        t = self.vars_sender()
        
        ##################################################
        # Blocks
        ##################################################

        #FFT OUT
        if self.FFTOUT:
            if self.tk_context != None:
                t.wxgui_fftsink2_0_0 = self.make_fftsink(self.tk_context, 'FFT Out')
            else:
                t.wxgui_fftsink2_0_0 = self.make_fftsink(t, 'FFT Out')
            t.Add(t.wxgui_fftsink2_0_0.win)

        #Tun
        if self.tun_handler != None:
            t.orcatun_tun_source_b_0 = orcatun.tun_source_b(self.tun_handler, "packet_len",self.ot)
        else:
            log.error("No TunHandler specified")
            sys.exit(1)

        #Ration resampler & interpolator
        t.rational_resampler_xxx_0_2_0  = self.make_resampler(self.interpolation_values[0], 1)
        t.rational_resampler_xxx_0_2    = self.make_resampler(self.interpolation_values[1], 1)
        t.rational_resampler_xxx_0_1    = self.make_resampler(self.interpolation_values[2], 1)
        t.rational_resampler_xxx_0_0    = self.make_resampler(self.interpolation_values[3], 1)
        t.rational_resampler_xxx_0      = self.make_resampler(self.interpolation_values[4], 1)

        t.orcatun_frame_encoder_0 = orcatun.frame_encoder("packet_len", self.crc)
  
        #Bandpassfilter
        t.freq_xlating_fir_filter_xxx_0 = self.make_bandfrqfilter()
        
        #GFSK Mod
        t.digital_gfsk_mod_0 = self.make_gfsk_mod()

         #Complex to real number converter
        t.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        
        #Audio sink
        t.audio_sink_0 = audio.sink(self.samp_rate, "", True)

        ##################################################
        # Connections
        ##################################################
        t.connect((t.blocks_complex_to_real_0, 0), (t.audio_sink_0, 0))    
        t.connect((t.digital_gfsk_mod_0, 0), (t.rational_resampler_xxx_0, 0))    
        t.connect((t.freq_xlating_fir_filter_xxx_0, 0), (t.blocks_complex_to_real_0, 0))
        if self.FFTOUT:
            t.connect((t.freq_xlating_fir_filter_xxx_0, 0), (t.wxgui_fftsink2_0_0, 0))
        t.connect((t.orcatun_frame_encoder_0, 0), (t.digital_gfsk_mod_0, 0))    
        t.connect((t.rational_resampler_xxx_0, 0), (t.rational_resampler_xxx_0_0, 0))    
        t.connect((t.rational_resampler_xxx_0_0, 0), (t.rational_resampler_xxx_0_1, 0))    
        t.connect((t.rational_resampler_xxx_0_1, 0), (t.rational_resampler_xxx_0_2, 0))    
        t.connect((t.rational_resampler_xxx_0_2, 0), (t.rational_resampler_xxx_0_2_0, 0))    
        t.connect((t.rational_resampler_xxx_0_2_0, 0), (t.freq_xlating_fir_filter_xxx_0, 0))    
        t.connect((t.orcatun_tun_source_b_0, 0), (t.orcatun_frame_encoder_0, 0))



        ##################################################
        # Blocks - build blocks for their functionality
        ##################################################

        #FFT In Block
        if self.FFTIN:
            if self.tk_context != None:
                t.wxgui_fftsink2_0 = self.make_fftsink(self.tk_context, "FFT IN")
            else: #Set the ownership accordingly
                t.wxgui_fftsink2_0 = self.make_fftsink(t, "FFT IN")
            t.Add(t.wxgui_fftsink2_0.win)


        if self.waterfall:
            t.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	t.GetWin(),
        	baseband_freq=0,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=self.samp_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Waterfall Plot", )
            t.Add(t.wxgui_waterfallsink2_0.win)

	t.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "packet_len")

        #Tunsink
        if self.tun_handler != None:
            print 1
            t.orcatun_tun_sink_pdu_0 = orcatun.tun_sink_pdu(self.tun_handler, "True")
        else: #implement tun_handler
            log.error("No TunHandler specified")
            sys.exit(1)

        #Decimator resampler
        t.rational_resampler_xxx_0_0_0_3 = self.make_resampler(1, self.interpolation_values[4] )
        t.rational_resampler_xxx_0_0_0_2 = self.make_resampler(1, self.interpolation_values[3] )
        t.rational_resampler_xxx_0_0_0_1 = self.make_resampler(1, self.interpolation_values[2] )
        t.rational_resampler_xxx_0_0_0_0 = self.make_resampler(1, self.interpolation_values[1] )
        t.rational_resampler_xxx_0_0_0 = self.make_resampler(1, self.interpolation_values[0] )

        #frame decoder
        t.orcatun_frame_decoder_0 = orcatun.frame_decoder("packet_len", self.samp_rate, True)
        
        #Low pass frequence filter
        t.freq_xlating_fir_filter_xxx_0_0 = self.make_lowpassfrqfilter()

        #Complex bandpass filter
        t.fft_filter_xxx_0 = self.make_fft_filter()
        t.fft_filter_xxx_0.declare_sample_delay(0)

        #GFSK demod
        t.digital_gfsk_demod_0 = self.make_gfsk_demod()

        #Multiply constance
        t.blocks_multiply_const_vxx_0 = self.multiply_const((1, ))
        #float o complex
        t.blocks_float_to_complex_0 = self.float_to_complex(1)

        #File sinks (currently made here
        #t.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, "./rec.txt", False)
        #t.blocks_file_sink_0.set_unbuffered(True)
        
        #Audio source
        t.audio_source_0 = audio.source(self.samp_rate, "", True)

	#DEBUG
	t.blocks_message_debug_0 = blocks.message_debug()


        ##################################################
        # Connections - Relate blocks to each other
        ##################################################
        t.connect((t.audio_source_0, 0), (t.blocks_float_to_complex_0, 0))
        if self.waterfall:
            t.connect((t.blocks_float_to_complex_0, 0), (t.wxgui_waterfallsink2_0, 0)) 
        t.connect((t.blocks_float_to_complex_0, 0), (t.blocks_multiply_const_vxx_0, 0))    
        t.connect((t.blocks_multiply_const_vxx_0, 0), (t.fft_filter_xxx_0, 0))    
        t.connect((t.digital_gfsk_demod_0, 0), (t.orcatun_frame_decoder_0, 0))    
        t.connect((t.fft_filter_xxx_0, 0), (t.freq_xlating_fir_filter_xxx_0_0, 0))    
        t.connect((t.freq_xlating_fir_filter_xxx_0_0, 0), (t.rational_resampler_xxx_0_0_0, 0))
        if self.FFTIN:
            t.connect((t.freq_xlating_fir_filter_xxx_0_0, 0), (t.wxgui_fftsink2_0, 0))    
        #t.connect((t.orcatun_frame_decoder_0, 0), (t.blocks_file_sink_0, 0))    
        t.connect((t.orcatun_frame_decoder_0, 0), (t.blocks_tagged_stream_to_pdu_0, 0))
	t.msg_connect((t.blocks_tagged_stream_to_pdu_0, 'pdus'), (t.orcatun_tun_sink_pdu_0, 'packet'))
	#t.msg_connect((t.blocks_tagged_stream_to_pdu_0, 'pdus'), (t.blocks_message_debug_0, 'print_pdu'))  
        t.connect((t.rational_resampler_xxx_0_0_0, 0), (t.rational_resampler_xxx_0_0_0_0, 0))    
        t.connect((t.rational_resampler_xxx_0_0_0_0, 0), (t.rational_resampler_xxx_0_0_0_2, 0))    
        t.connect((t.rational_resampler_xxx_0_0_0_1, 0), (t.digital_gfsk_demod_0, 0))    
        t.connect((t.rational_resampler_xxx_0_0_0_2, 0), (t.rational_resampler_xxx_0_0_0_3, 0))    
        t.connect((t.rational_resampler_xxx_0_0_0_3, 0), (t.rational_resampler_xxx_0_0_0_1, 0)) 
	
	#t.msg_connect((t.blocks_tagged_stream_to_pdu_0, 'pdus'), (t.blocks_message_debug_0, 'print'))
        return t


    ##
    # Creates a sender top_block
    def sender(self):
        log = logging.getLogger('master.BlockFactory')
        t = self.vars_sender()
        
        ##################################################
        # Blocks
        ##################################################

        #FFT OUT
        print self.FFTOUT
        if self.FFTOUT:
            if self.tk_context != None:
                t.wxgui_fftsink2_0_0 = self.make_fftsink(self.tk_context, 'FFT Out')
            else:
                t.wxgui_fftsink2_0_0 = self.make_fftsink(t, 'FFT Out')
            t.Add(t.wxgui_fftsink2_0_0.win)

        #Tun
        if self.tun_handler != None:
            t.orcatun_tun_source_b_0 = orcatun.tun_source_b(self.tun_handler, "packet_len","True")
        else:
            log.error("No TunHandler specified")
            sys.exit(1)

        #Ration resampler & interpolator
        t.rational_resampler_xxx_0_2_0  = self.make_resampler(self.interpolation_values[0], 1)
        t.rational_resampler_xxx_0_2    = self.make_resampler(self.interpolation_values[1], 1)
        t.rational_resampler_xxx_0_1    = self.make_resampler(self.interpolation_values[2], 1)
        t.rational_resampler_xxx_0_0    = self.make_resampler(self.interpolation_values[3], 1)
        t.rational_resampler_xxx_0      = self.make_resampler(self.interpolation_values[4], 1)

        t.orcatun_frame_encoder_0 = orcatun.frame_encoder("packet_len", True)
  
        #Bandpassfilter
        t.freq_xlating_fir_filter_xxx_0 = self.make_bandfrqfilter()
        
        #GFSK Mod
        t.digital_gfsk_mod_0 = self.make_gfsk_mod()

         #Complex to real number converter
        t.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        
        #Audio sink
        t.audio_sink_0 = audio.sink(self.samp_rate, "", True)

        ##################################################
        # Connections
        ##################################################
        t.connect((t.blocks_complex_to_real_0, 0), (t.audio_sink_0, 0))    
        t.connect((t.digital_gfsk_mod_0, 0), (t.rational_resampler_xxx_0, 0))    
        t.connect((t.freq_xlating_fir_filter_xxx_0, 0), (t.blocks_complex_to_real_0, 0))
        if self.FFTOUT:
            t.connect((t.freq_xlating_fir_filter_xxx_0, 0), (t.wxgui_fftsink2_0_0, 0))
        t.connect((t.orcatun_frame_encoder_0, 0), (t.digital_gfsk_mod_0, 0))    
        t.connect((t.rational_resampler_xxx_0, 0), (t.rational_resampler_xxx_0_0, 0))    
        t.connect((t.rational_resampler_xxx_0_0, 0), (t.rational_resampler_xxx_0_1, 0))    
        t.connect((t.rational_resampler_xxx_0_1, 0), (t.rational_resampler_xxx_0_2, 0))    
        t.connect((t.rational_resampler_xxx_0_2, 0), (t.rational_resampler_xxx_0_2_0, 0))    
        t.connect((t.rational_resampler_xxx_0_2_0, 0), (t.freq_xlating_fir_filter_xxx_0, 0))    
        t.connect((t.orcatun_tun_source_b_0, 0), (t.orcatun_frame_encoder_0, 0))
        return t

    ##
    # Creates a receiver top_block
    def receiver(self):
        log = logging.getLogger('master.BlockFactory')
        t = self.vars_receive()

        ##################################################
        # Blocks - build blocks for their functionality
        ##################################################

        #FFT In Block
        if self.FFTIN:
            if self.tk_context != None:
                t.wxgui_fftsink2_0 = self.make_fftsink(self.tk_context, "FFT IN")
            else: #Set the ownership accordingly
                t.wxgui_fftsink2_0 = self.make_fftsink(t, "FFT IN")
            t.Add(t.wxgui_fftsink2_0.win)


        if self.waterfall:
            t.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	t.GetWin(),
        	baseband_freq=0,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=self.samp_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Waterfall Plot", )
            t.Add(t.wxgui_waterfallsink2_0.win)

	t.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "packet_len")

        #Tunsink
        if self.tun_handler != None:
            t.orcatun_tun_sink_pdu_0 = orcatun.tun_sink_pdu(self.tun_handler, str(self.ot))
        else: #implement tun_handler
            log.error("No TunHandler specified")
            sys.exit(1)

        #Decimator resampler
        t.rational_resampler_xxx_0_0_0_3 = self.make_resampler(1, self.interpolation_values[4] )
        t.rational_resampler_xxx_0_0_0_2 = self.make_resampler(1, self.interpolation_values[3] )
        t.rational_resampler_xxx_0_0_0_1 = self.make_resampler(1, self.interpolation_values[2] )
        t.rational_resampler_xxx_0_0_0_0 = self.make_resampler(1, self.interpolation_values[1] )
        t.rational_resampler_xxx_0_0_0 = self.make_resampler(1, self.interpolation_values[0] )

        #frame decoder
        t.orcatun_frame_decoder_0 = orcatun.frame_decoder("packet_len", self.samp_rate, self.crc)
        
        #Low pass frequence filter
        t.freq_xlating_fir_filter_xxx_0_0 = self.make_lowpassfrqfilter()

        #Complex bandpass filter
        t.fft_filter_xxx_0 = self.make_fft_filter()
        t.fft_filter_xxx_0.declare_sample_delay(0)

        #GFSK demod
        t.digital_gfsk_demod_0 = self.make_gfsk_demod()

        #Multiply constance
        t.blocks_multiply_const_vxx_0 = self.multiply_const((1, ))
        #float o complex
        t.blocks_float_to_complex_0 = self.float_to_complex(1)

        #File sinks (currently made here
        #t.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, "./rec.txt", False)
        #t.blocks_file_sink_0.set_unbuffered(True)
        
        #Audio source
        t.audio_source_0 = audio.source(self.samp_rate, "", True)

	#DEBUG
	t.blocks_message_debug_0 = blocks.message_debug()


        ##################################################
        # Connections - Relate blocks to each other
        ##################################################
        t.connect((t.audio_source_0, 0), (t.blocks_float_to_complex_0, 0))
        if self.waterfall:
            t.connect((t.blocks_float_to_complex_0, 0), (t.wxgui_waterfallsink2_0, 0)) 
        t.connect((t.blocks_float_to_complex_0, 0), (t.blocks_multiply_const_vxx_0, 0))    
        t.connect((t.blocks_multiply_const_vxx_0, 0), (t.fft_filter_xxx_0, 0))    
        t.connect((t.digital_gfsk_demod_0, 0), (t.orcatun_frame_decoder_0, 0))    
        t.connect((t.fft_filter_xxx_0, 0), (t.freq_xlating_fir_filter_xxx_0_0, 0))    
        t.connect((t.freq_xlating_fir_filter_xxx_0_0, 0), (t.rational_resampler_xxx_0_0_0, 0))
        if self.FFTIN:
            t.connect((t.freq_xlating_fir_filter_xxx_0_0, 0), (t.wxgui_fftsink2_0, 0))    
        #t.connect((t.orcatun_frame_decoder_0, 0), (t.blocks_file_sink_0, 0))    
        t.connect((t.orcatun_frame_decoder_0, 0), (t.blocks_tagged_stream_to_pdu_0, 0))
	t.msg_connect((t.blocks_tagged_stream_to_pdu_0, 'pdus'), (t.orcatun_tun_sink_pdu_0, 'packet'))
	t.msg_connect((t.blocks_tagged_stream_to_pdu_0, 'pdus'), (t.blocks_message_debug_0, 'print_pdu'))  
        t.connect((t.rational_resampler_xxx_0_0_0, 0), (t.rational_resampler_xxx_0_0_0_0, 0))    
        t.connect((t.rational_resampler_xxx_0_0_0_0, 0), (t.rational_resampler_xxx_0_0_0_2, 0))    
        t.connect((t.rational_resampler_xxx_0_0_0_1, 0), (t.digital_gfsk_demod_0, 0))    
        t.connect((t.rational_resampler_xxx_0_0_0_2, 0), (t.rational_resampler_xxx_0_0_0_3, 0))    
        t.connect((t.rational_resampler_xxx_0_0_0_3, 0), (t.rational_resampler_xxx_0_0_0_1, 0)) 
	
	#t.msg_connect((t.blocks_tagged_stream_to_pdu_0, 'pdus'), (t.blocks_message_debug_0, 'print'))
        return t



    ##
    # Creates a pre-filled top_block to become a sender
    # @return a top_block with already set variables
    def vars_sender(self):
        if self.waterfall or self.FFTIN or self.FFTOUT:
            t = grc_wxgui.top_block_gui(title="OrcaTUN")
            _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
            t.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))
        else:
            t = gr.top_block()

        ##################################################
        # Variables
        ##################################################
        t.transistion = self.transistion 
        t.sps = self.sps
        t.sideband_rx = self.sideband_rx 
        t.sideband = self.sideband 
        t.samp_rate = self.samp_rate
        #t.payload = self.payload
        #t.interpolation = self.interpolation
        #t._crcpolynom_config = self._crcpolynom_config
        #t.crcpolynom = self.crcpolynom     
        #t.crcpolynom = self.crcpolynom
        t.carrier_b = self.carrier_b
        t.carrier_a = self.carrier_a
        #t._accesscode_config = self._accesscode_config
        #t.accesscode = self.accesscode
        return t

    ##
    # Creates a pre-filled top_block to become a receiver
    # @return a top_block with already set variables
    def vars_receive(self):
        if self.waterfall or self.FFTIN or self.FFTOUT:
            t = grc_wxgui.top_block_gui(title="OrcaTUN")
            _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
            t.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))
        else:
            t = gr.top_block()

        ##################################################
        # Variables
        ##################################################
        t.transistion = self.transistion 
        t.sps = self.sps
        t.sideband_rx = self.sideband_rx 
        #t.sideband = self.sideband 
        t.samp_rate = self.samp_rate
        #t.payload = self.payload
        #t.interpolation = self.interpolation
        #t._crcpolynom_config = self._crcpolynom_config
        #t.crcpolynom = self.crcpolynom     
        #t.crcpolynom = self.crcpolynom
        t.carrier_b = self.carrier_b
        #t.carrier_a = self.carrier_a
        #t._accesscode_config = self._accesscode_config
        #t.accesscode = self.accesscode

        return t



        
    ##############################################################################################
    #Automated Blocks
    #Maker function, which builds blocks for protocol usage, directly for their respective purpose
    #Blocks, which serve multiple uses are getting attention here
    ##############################################################################################

    ##
    #Creates a decimation resampler
    # @return a rational resampler block for decimation
    def decimator(self):
        return self.make_resampler(1, self.interpolation);
    ##
    #Creates an interpolating resampler
    # @return a rational resampler block for nterpolation
    def interpolator(self):
        return self.make_resampler(self.interpolation_values[2], 1);

    ##############################################################################################
    #Std Blocks
    #Pre-filled block consructions with config state.
    #They are automated, if there are no branched uses.
    ##############################################################################################


    ## Creates a FFT sink.
    # @param caller The calling instance to set window ownership properly
    # @param title Title of the instance (Title of block dispalyed in window)
    # @return a new fft sink block
    def make_fftsink(self, caller, title):
        return self.raw_fftsink(caller, title, 0, 10, 10, 0, 2.0, self.samp_rate, 1024, 30, False, None, False)

        
    ## Creates a rational resampler
    # @param interpol interpolation amount
    # @param decim  decimation amount
    # @return  rational resampler block
    def make_resampler(self, interpol, decim):
        return self.raw_resampler(interpol, decim, None, None);

    ## Creates a low pass frequency filter
    # @return a lowpass filter block
    def make_lowpassfrqfilter(self):
        return self.raw_frq_filter(1, self.make_lowpassfilter(), self.carrier_b, self.samp_rate)

    ## Creates a band pass frequency filter
    # @return a bandpass filter block
    def make_bandfrqfilter(self):
        return self.raw_frq_filter(1, self.make_bandpassfilter(), -self.carrier_a, self.samp_rate)

    ## Creates a simple lowpass filter block
    # @return a simple lowpassfilter
    def make_lowpassfilter(self):
        return self.raw_lowpassfilter(1, self.samp_rate, self.sideband_rx, 100)

    ## Creates a simple band pass filter
    # @return a simple bandpassfilter
    def make_bandpassfilter(self):
        return self.raw_bandpassfilter(
            0.50,
            self.samp_rate,
            self.carrier_a-self.sideband,
            self.carrier_a+self.sideband,
            self.transistion
            )

    ## Creates an fft filter block (a more complex bandpass filter)
    # @return a fft_filter block
    def make_fft_filter(self):
        return self.raw_fft_filter(1, self.make_complex_bandpass(), 1)

    ## Creates a complex bandpass filter
    # @return a complex banpass filter block
    def make_complex_bandpass(self):
        return self.raw_complex_bandpass(
            1.0,
            self.samp_rate,
            self.carrier_b-self.sideband_rx,
            self.carrier_b+self.sideband_rx,
            self.transistion,
            100,
            firdes.WIN_HAMMING,
            6.76
            )

    ## Creates a digital gfsk mod
    # @return a gfsk block for modulation
    def make_gfsk_mod(self):
        return self.raw_gfsk_mod(self.sps, 1.0,  0.35, False, False)

    ## Creates a digital gfsk demoduller
    # @return a gfsk block for demodulation
    def make_gfsk_demod(self):
        return self.raw_gfsk_demod(self.sps, 1.0, 0.175, 0.5, 0.005, 0.0, False, False)

    ## Creates a block to convert stream to a tagged stream
    # @return a stream_to_tagged_stream block
    def make_str_to_tgstr(self):
        return self.raw_str_to_tgtstr(gr.sizeof_char, 1, 64, "packet_len")

    ## Sets up a multipy const block
    # @param a constance range
    # @return a multiply constance vcc block
    def multiply_const(self, a):
        return blocks.multiply_const_vcc(a)

    ##Sets up flaot to complex block
    # @param a transversion value
    # @return a flaot to complex block
    def float_to_complex(self, a):
        return blocks.float_to_complex(a)
    
    ##############################################################################################
    #Raw Block Maker
    #Mostly wrapped constructors. The idea is to sort input parameter and tell for wat they are, as
    # GnuRadio documentation is a mess. No Warranty
    ##############################################################################################

    # Comments in this section are incomplete.
    # Here are mostly wrapped constuctors with the only purpose to make them

    ## A raw fftsink (window graph)
    # @param caller The GUI parent for widget
    # @param title The Title on the gui
    # @param baseband Baseband frq
    # @param y_div y points per div
    # @param y_divs the number of divs
    # @param reflv reference level
    # @param refscl reference scale
    # @param smpr Sample Rate
    # @param size the fft size
    # @param rate the fft rate
    # @param avg average value
    # @param avg_alpha average alpha value
    # @param peak_hold Wether peak_hold is activated or not
    # @return A fftsink block
    def raw_fftsink(self, caller, title, baseband, y_div, y_divs, reflv,
                     refscl, smpr, size, rate, avg, avg_alpha, peak_hold):
        return fftsink2.fft_sink_c(
        	caller.GetWin(),
        	baseband_freq=baseband,
        	y_per_div=y_div,
        	y_divs=y_divs,
        	ref_level=reflv,
        	ref_scale=refscl,
        	sample_rate=smpr,
        	fft_size=size,
        	fft_rate=rate,
        	average=avg,
        	avg_alpha=avg_alpha,
        	title=title,
        	peak_hold=peak_hold,
        )
        

    ## A Raw resampler block
    # @param intpol interpolation value
    # @param decim decimation value
    # @param tps taps
    # @param fractional fractional resampling
    # @return a rational resampler block
    def raw_resampler(self, intpol, decim, tps, fractional):
        return filter.rational_resampler_ccc(
                    interpolation=intpol,
                    decimation=decim,
                    taps=tps,
                    fractional_bw=fractional,
               )
    
    ## Creates a frequency filter.
    # @param filt Inner filter
    # @param carrier Carrier frequency
    # @param sample_rate  rate the sample rate
    # @param const Decimation
    # @return a frequency filter block wtih the set parameters
    def raw_frq_filter(self, const, filt, carrier, sample_rate):
        return filter.freq_xlating_fir_filter_ccc(
            const,
            filt,
            carrier,
            sample_rate)
    
    ## A raw low pass filter
    # @param const decimation
    # @param samp_rate sample rate
    # @param sideband_rx sideband frequency
    # @param transistion transistion
    # @return a lowpassfitler block, with the input parameters
    def raw_lowpassfilter(self, const, samp_rate, sideband_rx, transistion):
        return filter.firdes.low_pass(const, samp_rate, sideband_rx, transistion)
    
    ## A raw bandpass filter
    # @param const decimation
    # @param samp_rate sample rate
    # @param lowpass lowpass frequency (lower border) to filter
    # @param highpass highpass filter (upper border) to filter
    # @param transition transissiton
    # @return a bandpassfitler
    def raw_bandpassfilter(self, const, samp_rate, lowpass, highpass, transition):
        return firdes.band_pass (const, samp_rate,lowpass, highpass, transition)

    
    ## Creates a frequency filter
    # @param 'const' : decimation
    # @param 'filters' : internal filter
    # @param 'transition' : transistion
    # @return a raw frequency filter block with the declared parameters
    def raw_fft_filter(self, const, filters, transition):
        return filter.fft_filter_ccc(const, filters, transition)

    ## Cretaes a more complex bandpassfitler block
    # @param a undocumentad dependency paramter 1 
    # @param samp_rate sample rate
    # @param lowpass lowpass frequency (lower border) to filter
    # @param highpass highpass filter (upper border) to filter
    # @param transistion transisition
    # @param b undocumentad dependency paramter 2 
    # @param symbol symbols to filter
    # @param c undocumentad dependency paramter 3 
    # @return a complex bandpassfilter block
    def raw_complex_bandpass(self, a, samp_rate, lowpass, highpass, transistion, b, symbol, c):
        return firdes.complex_band_pass_2(a, samp_rate, lowpass, highpass, transistion, b, symbol, c)

    ## creates a gfsk mod block
    # @param sps Samples per second
    # @param sensi sensitivity
    # @param bts gaussian filter bandwith * symbol time
    # @param isVerbose wether it is verbode or not
    # @param make_log wether it should log or not
    # @return a gfsk block
    def raw_gfsk_mod(self, sps, sensi, bts, isVerbose, make_log):
        return digital.gfsk_mod(
        	samples_per_symbol=self.sps,
        	sensitivity=sensi,
        	bt=bts,
        	verbose=isVerbose,
        	log=make_log,
                )

    ## Creates a gfsk mod block
    # @param sps Samples per second
    # @param sensi sensitivity
    # @param gain mu gain
    # @param smu starting mu (fractional delay)
    # @param orl omega relative limit
    # @param frqerr error bit rate as fraction
    # @param isVerbose wether it is verbode or not
    # @param make_log wether it should log or not
    # @return a gfsk demod block
    def raw_gfsk_demod(self, sps, sensi, gain, smu, orl, frqerr, isVerbose, make_log):
        return digital.gfsk_demod(
        	samples_per_symbol=self.sps,
        	sensitivity=sensi,
        	gain_mu=gain,
        	mu=smu,
        	omega_relative_limit=orl,
        	freq_error=frqerr,
        	verbose=isVerbose,
        	log=make_log,
        )

    ## creates a stream to tagged stream block
    # @param size size of buffer 
    # @param a undocumentad dependency paramter 1 
    # @param b undocumentad dependency paramter 2
    # @param title title of the stream
    # @return a stream to tagged  stream block
    def raw_str_to_tgtstr(self, size, a, b, title):
        return blocks.stream_to_tagged_stream(size, a, b, title)

    def get_resampler_values(self,inter):
        synthetic       = [1,2,2,5,3] #60
        risky           = [2,2,2,3,3] #72 
        medium          = [1,5,5,4,1] #100
        conservative    = [5,5,3,2,1] #150
        safe            = [3,3,3,3,3] #243
        if inter == 1:
            return synthetic
        if inter == 2:
            return risky
        if inter == 3:
            return medium
        if inter == 4:
            return conservative
        if inter == 5:
            return safe


    
##############################################################################################
        
