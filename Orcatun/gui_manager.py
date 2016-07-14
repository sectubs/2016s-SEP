##
# @author: Nico Weil, Tobias Breuer, Lukas Schulz
# @brief Provides GUI components and respective methods
from Tkinter import *
import main 
import sys
import os
from threading import Thread
import logging
from log_manager import Log_manager
import ScrolledText
import tkFileDialog


##Create the Graphic User Interface
class GUI_manager():

    ##
    # Construct gui_m instance containing:
    # Variables, frames, widgets
    def __init__(self, master):
        ## Dict temporarily storing parameters
        self.tempStore = {"c":"",
                         "s":"",
                         "r":"",
                         "t":"",
                         "d":"",
                         "l":"",
                         "n":"",
                          "i":"",
                         "v":True,
                          "w":False,
                          "in":False,
                          "o":False
                          }

        ## Variables:
        self.orcaThread =None
        ##Main
        self.master = master
        ##Transmitfrequency
        self.frq_tx = IntVar()
        ##Receivefrequency
        self.frq_rx = IntVar()
        ##Local IP Address
        self.ip_local = StringVar()
        ##Destination IP Address
        self.ip_dest = StringVar()
        ##Output verbosity
        self.verbosity = IntVar()
        #set boolean for verbosity False
        self.verbosity.set(0)
        ##Audio Device Samplingrate
        self.samplingRate = IntVar()
        ##Name for TUN-Device
        self.tun_name = StringVar()
        ##Path to Config
        self.conf_path = StringVar()
        ##Boolean determining whteher waterfall graph is displayed
        self.showWaterfall = BooleanVar()
        self.showWaterfall.set(False)
        ##Boolean determining whether input graph (FFT) is displayed
        self.showFFTin = BooleanVar()
        self.showFFTin.set(False)
        ##Boolean determining whether output graph (FFT) is displayed
        self.showFFTout = BooleanVar()
        self.showFFTout.set(False)
        ##Interpolation
        self.inter = IntVar()

        ##Possible values for sampling rate
        self.sampling_rate_values = ["32000", "44100", "48000"]
        ##Possible interpolation values
        self.inter_values = ["1", "2", "3", "4", "5"]

        ## Frames (used as containers for widgets):
        ##Main-Frame
        self.input_frame = Frame(master)
        self.input_frame.grid(
                ##row to put Object into
                row=0,
                ##column to put Object into
                column=0)
        ##Button-Frame
        self.button_frame = Frame(master)
        self.button_frame.grid(row=0,
                column=1)
        ##Text-Frame
        self.text_frame = Frame(master)
        self.text_frame.grid(row=1,
                column=0,
                columnspan=2)
        ##Output-Text
        self.output_txt = ScrolledText.ScrolledText(master,
                width = 90,
                height=26,
                state='disabled')
        self.output_txt.grid(in_=self.text_frame, sticky = W)


        ##Log-Manager
        self.log_m = Log_manager(self.output_txt)

        ##Local IP Frame
        self.ip_local_frame = Frame(self.input_frame)
        self.ip_local_frame.grid(row=0,column=0)
        ##Destination IP Frame:
        self.ip_dest_frame = Frame(self.input_frame)
        self.ip_dest_frame.grid(row=1)
        ##TX-Frequency Frame
        self.freq_tx_frame = Frame(self.input_frame)
        self.freq_tx_frame.grid(row=2,column=0)
        ##RX-Frequency Frame
        self.freq_rx_frame = Frame(self.input_frame)
        self.freq_rx_frame.grid(row=3,column=0)
        ##Tun-Name Frame
        self.tun_frame = Frame(self.input_frame)
        self.tun_frame.grid(row=4)
        ##Samplingrate Frame
        self.samplingr_frame = Frame(self.input_frame)
        self.samplingr_frame.grid(row=5)
        ##Interpolation frame
        self.inter_frame = Frame(self.input_frame)
        self.inter_frame.grid(row = 6)
        #Annotation: Info text gridded in last row of input_frame

        ##Default width for Labels
        self.labelwidth=15
        ##Default x-axis Padding
        self.xpad = 2
        ##Default Buttonwidth
        self.buttonwidth=15

        ## Transmitfrequency-Label
        self.tx_lbl = Label(self.freq_tx_frame,
                width = self.labelwidth,
                anchor=W,
                height = 1,
                text = "TX:")
        self.tx_lbl.grid(row=0,
                column=0 ,
                padx = self.xpad)

        ## Transmitfrequency-Entry
   	self.tx_entry = Entry(self.freq_tx_frame,
                width = 5)
        self.tx_entry.grid(row=0,column=1)

	## Transmitfrequency-Slider
        self.scale_tx = Scale(self.freq_tx_frame,
                from_ = 0,
                to = 24000,
                orient = HORIZONTAL,
                sliderlength = 20,
                length = 115,
                resolution = 100,
                variable = self.frq_tx,
                showvalue = 0)
        self.scale_tx.grid(row=0,
                column=2)

	## Receivefrequency-Label
        self.rx_lbl = Label(self.freq_rx_frame,
                width = self.labelwidth,
                anchor=W,
                height = 1,
                text = "RX:")
        self.rx_lbl.grid(row=0,
                column=0 ,
                padx = self.xpad)

        ## Receivefrequency-Entry
        self.rx_entry = Entry(self.freq_rx_frame,
                width = 5)
        self.rx_entry.grid(row=0,
                column=1)

 	## Receivefrequency-Slider
        self.scale_rx = Scale(self.freq_rx_frame,
                from_ = 0,
                to = 24000,
                orient = HORIZONTAL,
                sliderlength = 20,
                length = 115,
                resolution = 100,
                variable = self.frq_rx,
                showvalue = 0)
        self.scale_rx.grid(row=0,
                column=2)

	## TUN-Name-Label
        self.tun_name_lbl = Label(self.tun_frame,
                width = self.labelwidth,
                anchor=W,height = 1 ,
                text = "TUN-Device Name:")
        self.tun_name_lbl.grid(row=0,
                column=0 ,
                padx = self.xpad)

        ## TUN-Name-Entry
        self.tun_name_entry = Entry(self.tun_frame)
        self.tun_name_entry.grid(row=0,
                column=1)

       	## Local IP Address Label
        self.ip_local_lbl = Label(self.ip_local_frame,
                width = self.labelwidth,
                anchor=W,
                text = "Local IP:")
        self.ip_local_lbl.grid(row=0,
                column=0,
                sticky=W ,
                padx = self.xpad)

        ## Locale IP Address Entry
        self.ip_local_entry = Entry(self.ip_local_frame,
                width = 20)
        self.ip_local_entry.grid(row=0,
                column=1)

	## Destination IP Address Label
        self.ip_dest_lbl = Label(self.ip_dest_frame,
                width = self.labelwidth,
                anchor=W,text = "Destination IP:")
        self.ip_dest_lbl.grid(row=0,column=0 ,
                padx = self.xpad)

        ## Destination IP Address Entry
        self.ip_dest_entry = Entry(self.ip_dest_frame,
                width = 20)
        self.ip_dest_entry.grid(row=0,
                column=1)

        ## Run-Button
        self.run_b = Button(self.button_frame,
                text = 'Start OrcaTUN' ,
                width = self.buttonwidth,
                command = self.runOrcatun)
        self.run_b.grid(row=3,
                column = 0)

        ## Quit-Button
        self.quit_b = Button(self.button_frame,
                text = 'Quit' ,
                width = self.buttonwidth,
                command = self.closeWindow)
        self.quit_b.grid(row=3,
                column=1)

        ## Reset-Button
        self.reset_b = Button(self. button_frame,
                text = 'Set default values' ,
                width = self.buttonwidth,
                command = self.setDefaults)
        self.reset_b.grid(row=2,
                column=1)

	## Path to Config Entry
        self.conf_path_entry = Button(self.button_frame ,
                width = self.buttonwidth,
                height =1,
                command = self.loadConfig,
                text="Press to Load Config")
        self.conf_path_entry.grid(row=2,
                column = 0)

        ## Waterfall checkbox
        self.waterfall_check = Checkbutton(self.button_frame,
                text = 'Show waterfall graph',
                anchor=W,
                variable = self.showWaterfall,
                onvalue = True,
                offvalue = False)
        self.waterfall_check.grid(row=0,
                column=0)

        ## FFTin checkbox
        self.fftin_check = Checkbutton(self.button_frame,
                text = 'Show input graph (FFT)',
                anchor = W,
                variable = self.showFFTin,
                onvalue = True,
                offvalue = False)
        self.fftin_check.grid(row = 0, column = 1)

        ## FFTout checkbox
        self.fftout_check = Checkbutton(self.button_frame,
                text = 'Show output graph (FFT)',
                anchor = W,
                variable = self.showFFTout,
                onvalue = True,
                offvalue = False)
        self.fftout_check.grid(row = 1, column = 0)

        ## Verbosity Checkbox
        self.verbosity_check = Checkbutton(self.button_frame,
                text = 'Verbose Output',
                anchor=W,
                variable = self.verbosity,
                onvalue = True,
                offvalue = False)
        self.verbosity_check.grid(row=1,
                column=1)

	## Path to Config Entry
        self.conf_path_entry = Button(self.button_frame ,
                width = self.buttonwidth,
                height =1,
                command = self.loadConfig,
                text="Press to Load Config")
        self.conf_path_entry.grid(row=2,
                column = 0)

        # Label widgets:


        ##Samplingrate-Label
        self.samplingRate_lbl = Label(self.samplingr_frame,
                width = self.labelwidth,
                anchor=W,
                height = 1,
                text = "SamplingRate:")
        self.samplingRate_lbl.grid(row=0,
                column=0,
                padx = self.xpad)

        ##Samplingrate-Dropdown
        self.samplingRate_size_dd = OptionMenu(self.samplingr_frame,
                self.samplingRate,
                *self.sampling_rate_values)
        self.samplingRate_size_dd.config(width=15)
        self.samplingRate_size_dd.grid(row=0,
                column=1)

        
        ##Interpolation drop-down menu
        self.inter_dd = OptionMenu(self.inter_frame,
                                   self.inter,
                                   *self.inter_values)
        self.inter_dd.config(width = 15)
        self.inter_dd.grid(row = 0, column = 1)

        ##Interpolation label:
        self.inter_lbl = Label(self.inter_frame,
                               width = self.labelwidth,
                               anchor = W,
                               height = 1,
                               text = "Interpolation:"
                               )
        self.inter_lbl.grid(row = 0, column = 0)

        ##Info label:
        self.info_lbl = Label(self.input_frame,
                              height = 1,
                              text = "Press return to confirm values.")
        self.info_lbl.grid(row = 7)
                

        ## Configuartions:
        ##Transmitfrequency-Trace
        self.frq_tx.trace("w",
                self.txTrace)
        ##Receivefrequency-Trace
        self.frq_rx.trace("w",
                self.rxTrace)
        ##Bind Transmitfrequency-Entry
        self.tx_entry.bind("<Return>",
                self.returnPressed)
        ##Bind Receivefrequency-Entry
        self.rx_entry.bind("<Return>",
                self.returnPressed)
        ##Bind Local IP Address Entry
        self.ip_local_entry.bind("<Return>",
                self.returnPressed)
        ##Bind Destination IP Address Entry
        self.ip_dest_entry.bind("<Return>",
                self.returnPressed)
        ##Bind TUN-Name-Entry
        self.tun_name_entry.bind("<Return>",
                self.returnPressed)
        ##Bind Path to Config Entry
        self.conf_path_entry.bind("<Return>",
                self.returnPressed)
        self.inter_dd.bind("<Return>",
                           self.returnPressed)
        ##Attach log_m to master logger
        log = logging.getLogger('master')
        log.addHandler(self.log_m)
        ##Set default values
        self.setDefaults()
    ##
    # Choose file from disk and write into button
    def loadConfig(self):
        confpath = tkFileDialog.askopenfilename(filetypes = (("Config Files", "*.conf")
                                                            ,("All Files", "*.*")))
        if confpath:
            try:
                self.conf_path = confpath
                self.conf_path_entry.config(text = confpath)
            except:
                log.error("Error while loading Config.")
                
    ##
    # Check sampling rate (has to be >freq/2)
    def checkSR(self):
        if int(self.samplingRate.get()) >= 2*int(self.tx_entry.get()) and int(self.samplingRate.get()) >= 2*int(self.rx_entry.get()):
            return
        else:
            raise ValueError('Sampling rate must at least be twice as large as the bigger frequency')

    ##
    # Check TX frequency and throw exception in case it is invalid
    def checkTxFreq(self):
        log = logging.getLogger('master.gui')
        try:
            freqtx = int(self.tx_entry.get())
        except ValueError:
            raise ValueError('TX frequency must be an integer value.')

        if 0 < freqtx and freqtx <= 24000:
            return
        else:
            raise ValueError('TX frequency must be in range 0<f<=24000')
        
    ##
    # Check RX frequency and throw exception in case it is invalid
    def checkRxFreq(self):
        log = logging.getLogger('master.gui')
        try:
            freqrx = int(self.rx_entry.get())
        except ValueError:
            raise ValueError('RX frequency must be an integer value.')

        if 0 < freqrx and freqrx <= 24000:
            return
        else:
            raise ValueError('RX frequency must be in range 0<f<=24000')
    
    
    ##
    # Check local IP address and throw exception in case it is invalid
    def checkLocalIp(self):
        log = logging.getLogger('master.gui')
        parts = str(self.ip_local_entry.get()).split(".")
        try:
            if len(self.ip_local_entry.get()) == 0:
                raise ValueError('Enter a local IP address.')
            if len(parts) != 4 :
                raise ValueError('Local IP not a Valid IPv4 address')
            for i in parts:
                intTest = int(i)
                if intTest < 0 or intTest > 255:
                    raise ValueError('Local IP is no valid IPv4 address.')
            return
        except ValueError:
            raise ValueError('Local IP is no valid IPv4 address.')

    ##
    # Check destination IP address ad throw exception in case it is invalid
    def checkDestIp(self):
        log = logging.getLogger('master.gui')
        parts = str(self.ip_dest_entry.get()).split(".")
        try:
            if len(self.ip_dest_entry.get()) == 0:
                raise ValueError('Enter a destination IP address')
            if len(parts) != 4 :
                raise ValueError('Destination IP is not a Valid IPv4 address')
            for i in parts:
                intTest = int(i)
                if intTest < 0 or intTest > 255:
                    raise ValueError('Destination IP is no valid IPv4 address.')
            return
        except ValueError:
            raise ValueError('Destination IP is no valid IPv4 address.')

    ##
    # Check TUN daveice name
    def checkTunName(self):
        if len(self.tun_name_entry.get()) == 0:
            raise ValueError('TUN device name must at least have one character')
        return

    ##
    # Check all parameters
    def checkAllParameters(self):
        log = logging.getLogger('master.gui')
        try:
            self.checkTxFreq()
            self.checkRxFreq()
            self.checkLocalIp()
            self.checkDestIp()
            self.checkTunName()
            self.checkSR()
            return True
        except:
            return False
        
    ##
    # Run Orcatun
    def runOrcatun(self):
        log = logging.getLogger('master.gui')
        if self.checkAllParameters() == True :
            log.info("Strating OrcaTUN")
            #Simulate return:
            self.returnPressed('<Return>')
            orc = Thread(
                      group=None,
                      target=main.run,
                      name=None,
                      args=(self.tempStore,)) #hier spaeter dict
            orc.start()
            self.orcaThread = orc
            self.run_b.config(text = 'Stop OrcaTUN', command = self.stopOrcatun)
        else :
            log.info("Please enter correct parameters.")

    def saveViaButton(self):
        print "test"
        return self.tempStore

        ##try:
            ##self.configStore.setAttributes()
        ##except:
            ##self.log_m.writeToLog("Saving to file failed.")

    ##
    # Stop OrcaTun
    def stopOrcatun(self):
        log = logging.getLogger('master.gui')
        try:
            os.system('ip link delete ' + self.tempStore["n"])
            main.killTun(self.orcaThread)
           # self.orcaThread. #terminate()
            self.run_b.config( text = 'Start OrcaTUN', command = self.runOrcatun)
        except AttributeError:
            log.info("Stopped Orcatun")
            pass
        self.run_b.config( text = 'Start OrcaTUN', command = self.runOrcatun)

    ##
    # Destroy master-widget and thus exit GUI
    def closeWindow(self):
        self.stopOrcatun()
        self.master.destroy()
        
    ##
    # Synchronize TX entry field with frq_tx (IntVar()-component)
    # @param *args Parameter passed on to the trace-method, determines the mode it is used in
    def txTrace(self, *args):
        self.tx_entry.delete('0', len(self.tx_entry.get()))
        self.tx_entry.insert('0', self.frq_tx.get())

    ##
    # Synchronize RX entry field with frq_rx (IntVar()-component)
    # @param *args Parameter passed on to the trace-method, determines the mode it is used in
    def rxTrace(self, *args):
        self.rx_entry.delete('0', len(self.rx_entry.get()))
        self.rx_entry.insert('0', self.frq_rx.get())

    ##
    # Method handles the following:
    #
    # Check parameters
    # Change background colour in case parameter is invalid
    # Print acknowlegement/error message
    # Synchronize scale with respective entry field
    # @param event Internal event (such as return being pressed)
    def returnPressed(self, event):
        log = logging.getLogger('master')
        log.setLevel(logging.DEBUG)
        log.addHandler(self.log_m)
        log = logging.getLogger('master.gui')

        checkComplete = True
        
        try:
            self.checkTxFreq()
            self.tx_entry.config(bg = "white")
            self.tempStore["t"] = int(self.tx_entry.get())
            self.scale_tx.set(self.tx_entry.get())
            log.info("TX frequency saved.")
        except ValueError, e:
            checkComplete = False
            self.tx_entry.config(bg = "tomato")
            log.info(str(e))

        try:
            self.checkRxFreq()
            self.rx_entry.config(bg = "white")
            self.tempStore["r"] = int(self.rx_entry.get())
            self.scale_rx.set(self.rx_entry.get())
            log.info("RX frequency saved.")
        except ValueError, e:
            checkComplete = False
            self.rx_entry.config(bg = "tomato")
            log.info(str(e))

        try:
            self.checkLocalIp()
            self.rx_entry.config(bg = "white")
            self.tempStore["l"] = str(self.ip_local_entry.get())
            log.info("Local IP address saved.")
        except UnboundLocalError:
            checkComplete = False
            log.info("Enter a local IP address.")
        except ValueError, e:
            checkComplete = False
            self.ip_local_entry.config(bg = "tomato")
            log.info(str(e))

        try:
            self.checkDestIp()
            self.ip_dest_entry.config(bg = "white")
            self.tempStore["d"] = str(self.ip_dest_entry.get())
            log.info("Destination IP address saved.")
        except UnboundLocalError:
            checkComplete = False
            log.info("Enter a local IP address.")
        except ValueError, e:
            checkComplete = False
            self.ip_dest_entry.config(bg = "tomato")
            log.info(str(e))

        try:
            self.checkTunName()
            self.tun_name_entry.config(bg = "white")
            self.tempStore["n"] = str(self.tun_name_entry.get())
            log.info("TUN name saved.")
        except ValueError, e:
            checkComplete = False
            self.tun_name_entry.config(bg = "tomato")
            log.debug(str(e))

        try:
            self.checkSR()
            self.samplingRate_size_dd.config(bg = "grey84")
            self.tempStore["s"] = int(self.samplingRate.get())
            log.info("Sampling rate saved.")
        except ValueError, e:
            checkComplete = False
            if len(self.tx_entry.get()) != 0 and len(self.rx_entry.get()) != 0:
                self.samplingRate_size_dd.config(bg = "tomato")
            log.info(str(e))

        self.tempStore["v"] = str(self.verbosity.get())
        self.tempStore["w"] = self.showWaterfall.get()
        self.tempStore["in"] = self.showFFTin.get()
        self.tempStore["o"] = self.showFFTout.get()
        self.tempStore["i"] = int(self.inter.get())

        if checkComplete == True:
            if self.orcaThread == None:
                log.info("Parameters succesfully saved into dict.")
            else:
                log.info("Parameters succesfully saved into dict. You need to restart Orcatun before they are applied.")

    ##
    # Reset both displayed and temporarily saved values to 0
    def setDefaults(self):
        self.tempStore = {"c":"",
                         "s":"48000",
                         "r":"19000",
                         "t":"20000",
                         "d":"10.8.0.1",
                         "l":"10.8.0.2",
                         "n":"tun0",
                          "i":"3",
                         "v":True,
                          "w":False,
                          "in":False,
                          "o":False}

        log = logging.getLogger('master')
        log.setLevel(logging.DEBUG)
        log.addHandler(self.log_m)
        log = logging.getLogger('master.gui')
        ##Reset entry fields
        self.ip_dest_entry.delete('0', len(self.ip_dest_entry.get()))
        self.ip_dest_entry.insert('0', self.tempStore["d"])
        self.ip_local_entry.delete('0', len(self.ip_local_entry.get()))
        self.ip_local_entry.insert('0', self.tempStore["l"])
        self.tun_name_entry.delete('0', len(self.tun_name_entry.get()))
        self.tun_name_entry.insert('0', self.tempStore["n"])
        ##Reset frequency sliders
        self.frq_tx.set(self.tempStore["t"])
        self.frq_rx.set(self.tempStore["r"])
        self.scale_tx.set(self.frq_tx.get())
        self.scale_rx.set(self.frq_rx.get())
        ##Reset sampling rate and interpolation
        self.samplingRate.set("44100")
        self.inter.set(self.inter_values[2])
        ##Reset check boxes
        self.showWaterfall.set(False)
        self.showFFTin.set(False)
        self.showFFTout.set(False)
        self.verbosity.set(True)

        log.info("Parameters set to defaults.")
