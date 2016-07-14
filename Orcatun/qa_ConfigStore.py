#!/usr/bin/python2.7
import unittest
import logging
import sys
from ConfigStore import Config

class qa_ConfigStore(unittest.TestCase):

    def setUp(self):
        conf = dict()
        conf['c'] = "/etc/orcatun/orcatun.conf"
        conf['s'] = 48000
        conf['r'] = 20000
        conf['t'] = 21000
        conf['d'] = "10.8.0.1"
        conf['l'] = "10.8.0.2"
        conf['n'] = "orca"
        conf['v'] = True
        conf['i'] = 3
        self.config = Config(conf)
        log = logging.getLogger('master')
        log.setLevel(logging.INFO)
        ch = logging.NullHandler()
        log.addHandler(ch)

    def test_set_interpolation_values(self):
        for i in (1,2,3,4,5):
            self.config.setInter(i)
            self.assertEqual(self.config.getInterFactor(),i)

    def test_bad_interpolation_values(self):
        for i in (0,6,'a','b'):
            with self.assertRaises(SystemExit):
                self.config.setInter(i)

    def test_set_verbosity_values(self):
        for i in ("True","1"):
            self.config.setVerbosity(i)
            self.assertEqual(self.config.getVerbosity(),True)

    def test_bad_verbosity_values(self):
        for i in ("False","0","2","nicht true"):
            self.config.setVerbosity(i)
            self.assertEqual(self.config.getVerbosity(),False)

    def test_set_fft_in_values(self):
        for i in ("True","1"):
            self.config.setFFTin(i)
            self.assertEqual(self.config.showFFTin,True)

    def test_bad_fft_in_values(self):
        for i in ("False","0","2","nicht true"):
            self.config.setFFTin(i)
            self.assertEqual(self.config.showFFTin,False)

    def test_set_fft_out_values(self):
        for i in ("True","1"):
            self.config.setFFTout(i)
            self.assertEqual(self.config.showFFTout,True)

    def test_bad_fft_out_values(self):
        for i in ("False","0","2","nicht true"):
            self.config.setFFTout(i)
            self.assertEqual(self.config.showFFTout,False)

    def test_check_sampling_rate_values(self):
        for i in (32000,44100,48000):
            self.config.values['s'] = i
            self.config.checkSamplingRate()
            self.assertEqual(self.config.getSamplingRate(),i)

    def test_bad_check_sampling_rate_values(self):
        for i in (0,6,'a','b'):
            with self.assertRaises(SystemExit):
                self.config.values['s'] = i
                self.config.checkSamplingRate()

    def test_bad_check_frequency_values(self):
        for i in ('r','t'):
            for j  in (24002,24001):
                with self.assertRaises(SystemExit):
                    self.config.values[i] = j
                    self.config.checkFrequency(i)

    def test_bad_check_ip_values(self):
        for i in ('l','d'):
            for j  in ("10.8.0.1.2","256.1.1.1","a"):
                with self.assertRaises(SystemExit):
                    self.config.values[i] = j
                    self.config.checkIP(i)

if __name__ == '__main__':
    unittest.main(exit="false")
