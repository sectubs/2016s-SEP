#!/usr/bin/python2.7

##
# Reads unsafe parameters from CLI and config
class unsafeParamReader:
    ##
    # Construct a new object of this class
    # @param args command line options from argparse 
    def __init__(self,args):
        ## path to orcaTUNs default Config
        self.DEFAULT_CONF="/etc/orcatun/orcatun.conf"
        ## Dictionary holding all specified options from config and command line
        self.values = dict() 
        self.addArgs(args)
        if 'c' not in self.values:
            ## Path to the config file being used
            self.conf_path = self.DEFAULT_CONF
            self.addValue('c',self.DEFAULT_CONF)
        else:
            self.conf_path = self.values['c']

        self.readConf(self.conf_path)
        #TODO: pruefen, warum f nicht aus der config gesetzt wird
        ## A TunHandler object
        #self.tun = Handler(self.values['name'], self.values['local'], self.values['dest'])
    
    ##
    # Read values from a config file
    # @param conf_path Path to the config
    def readConf(self, conf_path):
        with open(conf_path) as conf:
            for line in conf:
                if line[0] != '#' and line != '\n':
                    (key, value) = line.split(':')
                    self.addValue(key, value)

    ##
    # Adds a key/value pair to values
    # @param key The key
    # @param value The value
    def addValue(self, key, value):
        key = key.strip()
        value = value.strip()
        if key not in self.values:
            try:
                x = int(value)
                self.values[key] =x
            except ValueError:
                self.values[key] = value

    ##
    # Adds the arguments returned by argparse to values
    # @param args A namespace object returned by argparse
    # @details Namespace objects, also known as Strings with many parentheses,
    # need to be brought into a suitable form, before the arguments can be processed
    def addArgs(self, args):
        par = str(args)
        par = par.replace('Namespace','')
        par = par.replace('(','')
        par = par.replace(')','')
        par = par.replace('[','')
        par = par.replace(']','')
        par = par.replace('\'','')
        splitted = par.split(",")
        for i in splitted:
                key, val = i.split('=')
                if val != "None":
                    self.addValue(key,val)

    ## Get values
    # @return values
    def getValues(self):
        return self.values
