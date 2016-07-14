#!/usr/bin/python2.7
import sys
import logging
##
# @author Leonhard Matthias Schulze
# @brief This Class takes care of storing and supplying Variables for OrcaTun. 
# It also assures that the  Values are valid
# @details TODO


class Config:
    ##
    # Construct a new ConfigStore
    # @param values A Python Dict containing Parameters from the Command Line or a file.
    def __init__(self, values):
        ##Dictionary containing unsanitized options
        self.values = values
        ##Destination IP Address
        self.destIP = ""
        ##Local IP Address
        self.localIP = ""
        ##Frequency to listen on
        self.receiveFrequency = ""
        ##Frequency to send on
        self.transmitFrequency = ""
        ##Name for the TUN-Device
        self.name = ""
        ##Path to Config
        self.confPath = ""
        ##Output verbosity
        self.verbosity = ""
        ##Audio Device Samplingrate
        self.samplingRate = ""
        ##Interpolation
        self.interFaktor = ""
        ##Use OrcaTUN Packets
        self.useOTPackets = ""
        ##Show waterfall
        self.showWaterfall = ""
        ##Show FFTin
        self.showFFTin = ""
        ##Show FFTout
        self.showFFTout = ""
        self.setAttributes(self.values)
        log = logging.getLogger('master.orcatun')
        log.info("Parsed Config without errors!")
        if self.verbosity is True:
            log.setLevel(logging.DEBUG)
            self.printSelf()

    ##
    # getter for Destination IP
    def getDestIP(self):
        return self.destIP

    ##
    # getter for Local IP
    def getLocalIP(self):
        return self.localIP

    ##
    # getter for InterFactor
    def getInterFactor(self):
        return self.interFaktor

    ##
    # getter for Receivefrequency
    def getReceiveFreq(self):
        return self.receiveFrequency

    ##
    # getter for Transmitfrequency
    def getTransmitFreq(self):
        return self.transmitFrequency

    ##
    # getter for TUN-Device name
    def getName(self):
        return self.name

    ##
    # getter for Configpath
    def getConfPath(self):
        return self.confPath

    ##
    # getter for verbosity
    def getVerbosity(self):
        return self.verbosity

    ##
    # getter for Samplingrate
    def getSamplingRate(self):
        return self.samplingRate

    ##
    # getter for UseOTPackets
    def getOt(self):
        return self.useOTPackets

    ##
    # Pretty Print all the Values
    def printSelf(self):
        log = logging.getLogger('master.orcatun')
        log.debug("Config:             " + self.confPath)
        log.debug("Transmit Frequency: " + str(self.transmitFrequency))
        log.debug("Receive Frequency:  " + str(self.receiveFrequency))
        log.debug("Sampling Rate:      " + str(self.samplingRate))
        log.debug("Name:               " + self.name)
        log.debug("Local IP:           " + self.localIP)
        log.debug("Destination IP:     " + self.destIP)
        log.debug("Verbose Output:     " + str(self.verbosity))
        log.debug("Waterfall graph:    " + str(self.showWaterfall))
        log.debug("FFTin graph:        " + str(self.showFFTin))
        log.debug("FFTout graph:       " + str(self.showFFTout))
        log.debug("Interpolation:      " + str(self.interFaktor))
        log.debug("Use OT Packets:     " + str(self.useOTPackets))

    ##
    # Iterate over unsanitized Values, check for errors and set them as instance Attributes
    # @param values Parameters read from Config or Command Line
    def setAttributes(self, values):
        try:
            for key in values:
                if key == 'c':
                    self.confPath = values['c']
                if key == 's':
                    self.checkSamplingRate()

                if key == 'r':
                    self.checkFrequency('r')
                    self.receiveFrequency = int(values['r'])

                if key == 't':
                    self.checkFrequency('t')
                    self.transmitFrequency = int(values['t'])

                if key == 'd':
                    self.checkIP(key)
                    self.destIP = values[key]

                if key == 'l':
                    self.checkIP(key)
                    self.localIP = values[key]

                if key == 'n':
                    self.name = str(values['n'])

                if key == 'v':
                    self.setVerbosity(values['v'])

                if key == 'in':
                    self.setFFTin(values['in'])

                if key == 'o':
                    self.setFFTout(values['o'])

                if key == 'i':
                    self.setInter(values['i'])

                if key == 'ot':
                    self.setUseOTPackets(values['ot'])

                if key == 'w':
                    self.setWaterfall(values['w'])

        except KeyError as error:
            log = logging.getLogger('master.orcatun')
            log.error("Option not set")
            log.error(error)
            sys.exit(1)

    def setWaterfall(self, buf):
        if str(buf) == "True" or str(buf) == "1":
            self.showWaterfall = True
        else:
            self.showWaterfall = False

    ##
    # Set FFTin variable
    def setFFTin(self, buf):
        if str(buf) == "True" or str(buf) == "1":
            self.showFFTin = True
        else:
            self.showFFTin = False

    ##
    # Set FFTout variable
    def setFFTout(self, buf):
        if str(buf) == "True" or str(buf) == "1":
            self.showFFTout = True
        else:
            self.showFFTout = False

    ##
    # Set Interpolation Factor
    def setInter(self, ifaktor):
        log = logging.getLogger('master.orcatun')
        if ifaktor < 6 and ifaktor > 0:
            out = "Interpolation set to level " + str(ifaktor)
            log.debug(out)
            self.interFaktor = ifaktor
        else:
            log.error("Interpolation invalid. Valid Range is 1-5")
            sys.exit(1)

    ##
    # set chosen verbosity
    def setVerbosity(self, buf):
        if str(buf) == "True" or str(buf) == "1":
            self.verbosity = True
        else:
            self.verbosity = False

    ##
    # set chosen verbosity
    def setUseOTPackets(self, buf):
        if str(buf) == "True" or str(buf) == "1":
            self.useOTPackets = True
        else:
            self.useOTPackets = False

    ##
    # check if the specified Frequency is valid and set it
    # @param key key for the Frequency to check/set
    def checkFrequency(self, key):
        log = logging.getLogger('master.orcatun')
        if key == 'r':
            buf = 'Receive Frequency'
        elif key == 't':
            buf = 'Transmit Frequency'

        if self.samplingRate == "":
            self.checkSamplingRate()
        halfSamp = self.samplingRate / 2
        try:
            if int(self.values[key]) > halfSamp:
                raise ValueError(buf + " is bigger than Sampling Rate / 2")
        except ValueError as error:
            log.error("Frequenz too high")
            log.error(error)
            sys.exit(1)

    ##
    # check if the specified Samplingrate is valid and set it
    def checkSamplingRate(self):
        log = logging.getLogger('master.orcatun')
        try:
            srInt = int(self.values['s'])
            if srInt != 32000 and srInt != 44100 and srInt != 48000:
                raise ValueError("Sampling Rate must be either 32000 or 48000")
            self.samplingRate = srInt
        except ValueError as error:
            log.error("Sampling too low")
            log.error(error)
            sys.exit(1)

    ##
    # check if the specified IP is a valid IPv4 and set it
    # @param key key for the IP to check/set
    def checkIP(self, key):
        log = logging.getLogger('master.orcatun')
        if key == 'd':
            buf = 'Destination IP'
        else:
            buf = 'Local IP'

        parts = self.values[key].split(".")
        try:
            if len(parts) != 4:
                raise ValueError(buf + ': not a Valid IPv4 Address')
            for i in parts:
                intTest = int(i)
                if intTest < 0 or intTest > 255:
                    raise ValueError(buf + ': ' + i + ' Not in IPv4 range')

        except ValueError as error:
            log.error(error)
            sys.exit(1)
