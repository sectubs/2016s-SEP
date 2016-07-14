import logging
import argparse
import unittest
import sys
from ParamReader import unsafeParamReader
from tun_handler import TunHandler
from ConfigStore import Config
from threading import Thread
from grc_gnuradio import wxgui as grc_wxgui
import BlockFactory
from random import randint

class qa_BlockFactory(unittest.TestCase):

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

    def test_no_params(self):
        try:
             bf = BlockFactory.BlockFactory(None, None ,None)
             self.assertFalse(True)
        except:
            self.assertTrue(True)

    def test_sender(self):
        log = logging.getLogger('master')
        log.setLevel(logging.INFO)
        ch = logging.NullHandler()
        log.addHandler(ch)
        tun = TunHandler("sender")
        tun.set_ip_adresses(self.config.getLocalIP(),
        self.config.getDestIP())
        bf = BlockFactory.BlockFactory(self.config, tun, None)
        send = bf.sender()

        self.assertEqual(send.transistion, 100)
        self.assertEqual(send.sps, 5)
        self.assertEqual(send.sideband_rx, 100)
        self.assertEqual(send.sideband, 1000)
        self.assertEqual(send.samp_rate, self.config.getSamplingRate())
        self.assertEqual(send.carrier_a, self.config.getTransmitFreq())
        self.assertEqual(send.carrier_b, self.config.getReceiveFreq())
           
        tun.kill()

    def test_receiver(self):
        log = logging.getLogger('master')
        log.setLevel(logging.INFO)
        ch = logging.NullHandler()
        log.addHandler(ch)
        tun = TunHandler("receiver")
        tun.set_ip_adresses(self.config.getLocalIP(),
        self.config.getDestIP())
        bf = BlockFactory.BlockFactory(self.config, tun, None)
        rec = bf.receiver()

        self.assertEqual(rec.transistion, 100)
        self.assertEqual(rec.sps, 5)
        self.assertEqual(rec.sideband_rx, 100)
        self.assertEqual(rec.samp_rate, self.config.getSamplingRate())
        self.assertEqual(rec.carrier_b, self.config.getReceiveFreq())

        tun.kill()
        

    def test_omni(self):
        log = logging.getLogger('master')
        log.setLevel(logging.INFO)
        ch = logging.NullHandler()
        log.addHandler(ch)
        tun = TunHandler("omni")
        tun.set_ip_adresses(self.config.getLocalIP(),
        self.config.getDestIP())
        bf = BlockFactory.BlockFactory(self.config, tun, None)
        omni = bf.omniblock()

        self.assertEqual(omni.transistion, 100)
        self.assertEqual(omni.sps, 5)
        self.assertEqual(omni.sideband_rx, 100)
        self.assertEqual(omni.sideband, 1000)
        self.assertEqual(omni.samp_rate, self.config.getSamplingRate())
        self.assertEqual(omni.carrier_a, self.config.getTransmitFreq())
        self.assertEqual(omni.carrier_b, self.config.getReceiveFreq())
            
        tun.kill()



if __name__ == '__main__':
    unittest.main()
