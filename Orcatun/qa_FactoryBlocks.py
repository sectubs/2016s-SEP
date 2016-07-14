import BlockFactory
import unittest
import logging
import sys
from ConfigStore import Config
from tun_handler import TunHandler
from grc_gnuradio import wxgui as grc_wxgui
from random import randint

class qa_FactoryBlocks(unittest.TestCase):

    def setUp(self):
        conf = dict()
        conf['c'] = "/etc/orcatun/orcatun.conf"
        conf['s'] = 48000
        conf['r'] = 20000
        conf['t'] = 21000
        conf['d'] = "10.8.0.1"
        conf['l'] = "10.8.0.2"
        conf['n'] = "orca"
        conf['v'] = False
        conf['i'] = 3
        self.config = Config(conf)


    def test_interpolator(self):
        try:
            log = logging.getLogger('master')
            log.setLevel(logging.INFO)
            ch = logging.NullHandler()
            log.addHandler(ch)
            tun = TunHandler("resample")
            tun.set_ip_adresses(self.config.getLocalIP(),
            self.config.getDestIP())
            bf = BlockFactory.BlockFactory(self.config, tun, None)
            interpol = bf.make_resampler(1, 2)
            tun.kill()
            self.assertTrue(True)
        except:
            self.assertFalse(True)
   
    def test_lowpassfrqfilter(self):
        try:
            log = logging.getLogger('master')
            log.setLevel(logging.INFO)
            ch = logging.NullHandler()
            log.addHandler(ch)
            tun = TunHandler("lowpass")
            tun.set_ip_adresses(self.config.getLocalIP(),
            self.config.getDestIP())
            bf = BlockFactory.BlockFactory(self.config, tun, None)
            test = bf.make_lowpassfrqfilter()
            tun.kill()
            self.assertTrue(True)
        except:
            self.assertFalse(True)
        
    def test_bandpassfrqfilter(self):
        try:
            log = logging.getLogger('master')
            log.setLevel(logging.INFO)
            ch = logging.NullHandler()
            log.addHandler(ch)
            tun = TunHandler("bandpass")
            tun.set_ip_adresses(self.config.getLocalIP(),
            self.config.getDestIP())
            bf = BlockFactory.BlockFactory(self.config, tun, None)
            test = bf.make_bandpassfilter()
            tun.kill()
            self.assertTrue(True)
        except:
            self.assertFalse(True)
        
    def test_make_fft_filter(self):
        try:
            log = logging.getLogger('master')
            log.setLevel(logging.INFO)
            ch = logging.NullHandler()
            log.addHandler(ch)
            tun = TunHandler("fft")
            tun.set_ip_adresses(self.config.getLocalIP(),
            self.config.getDestIP())
            bf = BlockFactory.BlockFactory(self.config, tun, None)
            test = bf.make_fft_filter()
            tun.kill()
            self.assertTrue(True)
        except:
            self.assertFalse(True)
        
    def test_gfsk_mod(self):
        try:
            log = logging.getLogger('master')
            log.setLevel(logging.INFO)
            ch = logging.NullHandler()
            log.addHandler(ch)
            tun = TunHandler("gfsk")
            tun.set_ip_adresses(self.config.getLocalIP(),
            self.config.getDestIP())
            bf = BlockFactory.BlockFactory(self.config, tun, None)
            test = bf.make_gfsk_mod()
            tun.kill()
            self.assertTrue(True)
        except:
            self.assertFalse(True)
        
    def test_gfsk_demod(self):
        try:
            log = logging.getLogger('master')
            log.setLevel(logging.INFO)
            ch = logging.NullHandler()
            log.addHandler(ch)
            tun = TunHandler("demod")
            tun.set_ip_adresses(self.config.getLocalIP(),
            self.config.getDestIP())
            bf = BlockFactory.BlockFactory(self.config, tun, None)
            test = bf.make_gfsk_demod()
            tun.kill()
            self.assertTrue(True)
        except:
            self.assertFalse(True)
        
    def test_str_to_tgstr(self):
        try:
            log = logging.getLogger('master')
            log.setLevel(logging.INFO)
            ch = logging.NullHandler()
            log.addHandler(ch)
            tun = TunHandler("strtgstr")
            tun.set_ip_adresses(self.config.getLocalIP(),
            self.config.getDestIP())
            bf = BlockFactory.BlockFactory(self.config, tun, None)
            test = bf.make_str_to_tgstr()
            tun.kill()
            self.assertTrue(True)
        except:
            self.assertFalse(True)
        
    def test_multiplyconst(self):
        try:
            log = logging.getLogger('master')
            log.setLevel(logging.INFO)
            ch = logging.NullHandler()
            log.addHandler(ch)
            tun = TunHandler("multiply")
            tun.set_ip_adresses(self.config.getLocalIP(),
            self.config.getDestIP())
            bf = BlockFactory.BlockFactory(self.config, tun, None)
            test = bf.multiply_const((1, ))
            tun.kill()
            self.assertTrue(True)
        except:
            self.assertFalse(True)
        
    def test_float_to_complex(self):
        try:
            log = logging.getLogger('master')
            log.setLevel(logging.INFO)
            ch = logging.NullHandler()
            log.addHandler(ch)
            tun = TunHandler("flocm")
            tun.set_ip_adresses(self.config.getLocalIP(),
            self.config.getDestIP())
            bf = BlockFactory.BlockFactory(self.config, tun, None)
            test = bf.float_to_complex(1)
            tun.kill()
            self.assertTrue(True)
        except:
            self.assertFalse(True)

if __name__ == '__main__':
    unittest.main(exit="false")
