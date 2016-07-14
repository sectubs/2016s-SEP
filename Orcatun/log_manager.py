##
# @author Nico Weil
# @details
# Manages log-widget (basic text widget) independently from other
# classes (thus can be used to display any message)
# 
import sys
import logging
from Tkinter import *
##
# Provides a Handler (see logging.Handler) for Outputting text to a GUI
#
class Log_manager(logging.Handler):

    ##
    # Contsruct new instance of this class consisting of
    # a text widget and a scrollbar
    # @param text A Tkinter  ScrolledText Area for Outputting Text
    def __init__(self, text):
        logging.Handler.__init__(self)
        ## A ScrolledText Wideget
        self.log=text
        log_format = logging.Formatter('%(levelname)s - %(message)s')
        ## Log Format
        self.setFormatter = log_format
        ## Logging Level
        self.setLevel(logging.DEBUG)

    ##
    # Receive a Message and append it to self.log
    # @ param raw_msg
    def emit(self,raw_msg):
        msg = self.format(raw_msg) + '\n'
        self.log.configure(state = NORMAL)
        self.log.insert(END, msg)
        self.log.configure(state = DISABLED)
        self.log.yview(END)
