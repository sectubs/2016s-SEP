#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import logging
import argparse
import sys
from ParamReader import unsafeParamReader
from tun_handler import TunHandler
from ConfigStore import Config
from threading import Thread
import BlockFactory
from Tkinter import * 
import os
import signal


##
# Initialize the Commandline Interface using argparse
def getArgs():
    parser = argparse.ArgumentParser(description='Ultrasonic Networking with OrcaTun!')
    parser.add_argument('-s', metavar ='Sampling Rate',
            help='specify the Sampling Rate to use',
            nargs =1, type=int)

    parser.add_argument('-c', metavar ='Config',
            help='specify the path to a config File',
            nargs=1, type=str)

    parser.add_argument('-r', metavar='receive',
            help='specify the receive Frequency',
            nargs=1, type=int)

    parser.add_argument('-t', metavar='transmit',
            help='specify the transmit Frequency',
            nargs = 1, type=int)

    parser.add_argument('-d', metavar='Destination',
            help='Destination IP-Address',
            nargs=1)

    parser.add_argument('-l', metavar='Local',
            help='Local Tun-Device IP-Address',
            nargs=1)

    parser.add_argument('-n', metavar='Name',
            help='Name for the Tun-Device',
            nargs=1)

    parser.add_argument('-v',
            help='Increase Verbosity',
            action ="store_true")

    parser.add_argument('-in',
            help='Show FFT IN Graph',
            action ="store_true")
    
    parser.add_argument('-o',
            help='Show FFT Out Graph',
            action ="store_true")

    parser.add_argument('-w',
            help='Show Waterfall Graph',
            action ="store_true")

    parser.add_argument('-ot',
                        help='Use OT Packets',
                        action="store_true")
    
    parser.add_argument('-i',
            help='Specify Interpolation (1-5).',
            nargs=1, type=int)

    args = parser.parse_args()
    return args

tun = None

def killTun (tun):
    tun.kill()

def run(values):

    log = logging.getLogger('master.orcatun')
    log.info("Starting OrcaTun!")
    if values is None:
        args = getArgs()
        conf = unsafeParamReader(args)
        values = conf.getValues()
    sane_config = Config(values)
    tun = TunHandler(sane_config.getName())
    tun.set_ip_adresses(sane_config.getLocalIP(),
            sane_config.getDestIP())
    #master = Tk()
    #master.title("FFTS")
    bf = BlockFactory.BlockFactory(sane_config, tun, None)
    #NEW OMNIBLOCK
    send = bf.omniblock()

    if  sane_config.showWaterfall or sane_config.showFFTin or sane_config.showFFTout:
        send.Start(True)
        send.Wait()
    else:
        send.start()
        try:
            raw_input('Press Enter to quit: ')
            print "workde"
        except:
            pass
        tun.kill()
        os._exit(0)
        #os.kill(os.getpid(), signal.SIGINT)

    #TROLOLOLOL
   ## snd = Thread(group=None,
   #         target=send.run,
   #         name=None,
   #         args=())
   # snd.start()
   # print "vorher"
   # receive = bf.receiver()
   # rec = Thread(group=None,
   #         target=receive.run,
   #         name=None,
   #         args=())
   # rec.start()
   # print "nachher"
    ##
    #TODO: auf blockfactory warten, und dann hier in 2 threads starten

def print_msg():
    print '\033[94m'
    print "                                                      "
    print "                                                      "
    print "              MM                                      "
    print "               MM8                     :$8+ZZI:       "
    print "               .MMM7            :=MMMMMMMMMMMMMMMI    "
    print "                MMMMM:     IMMMMMMMMMN    MMMMMMMMZ   "
    print "                 MMMMMM?MMMMMMMMMMM     MMMMN=~.  .   "
    print "                 =MMMMMMMMMMMMMMMMMMMMMM         .    "
    print "                  MMMMMMMMMMMMMMMMMMMM:         $     "
    print "                 DMMMMMMMMMMMMMMMMMMM         Z       "
    print "                ,MMMMMMMMMMMMMMMMMMMM       8.        "
    print "               M MMMMMMMMMMMMMMMMMMMMM    DM          "
    print "              MMMMMMMMMMMMMMMMMMMMMMM   .MMMM         "
    print "             MMMMMMMMMMMMMMMMMMMMMMM    MMMMMM        "
    print "            MMMMMMMMMMMMMMMMMIMMMM,      MMMMD        "
    print "           ,MMMMMMMMMMMMMMMMMMMM$.~                   "
    print "           MMMMMMMMMMMMMMMMMMD  .                     "
    print "          MMMM?   ?MMMMMMMMMM D.                      "
    print "         .MMM7       NMMMMM +                         "
    print "         MMMM            .N                           "
    print "         MMMM           O                             "
    print "        :MMMM  ,MM    7            OrcaTUN            "
    print "        MMMMM~MMMM  O                                 " 
    print "        MMMMMMMMM D                                   "
    print "°º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤"
    print ""
    print '\033[0m'


##
# @author Leonhard Schulze
# @brief The entrypoint for Orcatun
#  @details
# This script handles the following: @n
# parsing command line parameters @n
# reading from configs @n
# starting the rest of the Programm @n
# supplying Parameters and Settings given by the User @n
if __name__=='__main__':
    print_msg()
    log = logging.getLogger('master')
    log.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    run(None)


