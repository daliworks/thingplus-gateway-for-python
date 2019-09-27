#!/usr/bin/python

import logging
import time
import spidev
import numpy as np 
from threading import *

class   SCA103T(Thread):
    def __init__(self, _config):
        Thread.__init__(self)
        self.sens_ = { 'SCA103T-D04' : 6554.0 }
        self.config_ = {
            'bus' : 0,
            'device': 0,
            'mode': 3,
            'speed' : 500000
        }
        self.spi_ = spidev.SpiDev()

        if _config != None:
            self.setConfig(_config)

    def setConfig(self, _config):
        try:
	        if _config.get('bus') != None:
	            self.config_['bus'] = _config.get('bus')
	    
	        if _config.get('device') != None:
	            self.config_['device'] = _config.get('device')
	    
	        if _config.get('mode') != None:
	            self.config_['mode'] = _config.get('bus')
	    
	        if _config.get('speed') != None:
	            self.config_['speed'] = _config.get('speed')
        except Exception as err:
            logging.error('Invalid config : %s'%err)  
	    
    def run(self):
	    self.spi_.open(self.config_['bus'], self.config_['device'])	# open(bus, device)
	    self.spi_.mode = self.config_['mode']
	    self.spi_.max_speed_hz = self.config_['speed'] 			# set transfer speed
        
	    while True:
		    data=self.spi_.xfer2([0x10, 0x00, 0x00])
		    x = (data[1] << 3) + (data[2] >> 5)
		    data=self.spi_.xfer2([0x11, 0x00, 0x00])
		    y = (data[1] << 3) + (data[2] >> 5)

		    out = (x - y) 
		    a = np.arcsin(out /self.sens_['SCA103T-D04'])
		    d = a / np.pi * 180

		    print x, y, d
		    time.sleep(1)

	    self.spi_.close()
