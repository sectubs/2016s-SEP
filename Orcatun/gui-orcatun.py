#!/usr/bin/python2.7
##
# @author: Nico Weil
# Main GUI class combining gui dependencies (log function and gui_manager)

from gui_manager import GUI_manager
from log_manager import Log_manager
from Tkinter import *
import logging


# Create root widget, independant log-widget, gui-manager and parameter-manager
master = Tk()
master.title("OrcaTUN GUI")
#img = PhotoImage(file = 'weirdorca.png')
#master.tk.call('wm', 'iconphoto', master._w, img)
gui_m = GUI_manager(master)

# Add widgets to master; master widget runs as mainloop and terminates only
# in case master is closed/quit button is pressed
gui_m.master.mainloop()

print "Terminated"
