#!/usr/bin/python

import serial
import binascii
import struct
import time
import datetime
import math
import trace
from threading import *

def haversine(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2
   
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))

class   UBlox(Thread):
    def __init__(self, _config = None):
        Thread.__init__(self)
        self.trace = trace.Trace(self)
        self.config_ = {
            'serial' : {
                'port' : '/dev/ttyACM0',
                'baudrate' : 115200,
                'parity' : 'none',
                'stopbits' : 1,
                'databits' : 8
            }
        }
        self.base_ = (None, None)
        self.latest_ = (None, None)
        self.serial_ = serial.Serial()

        self.setConfig(_config)

        self.trace.info('Create UBlox')

    def setConfig(self, _config):
        if _config is not None:
            try:
                self.config_.update(_config)
            except Exception as err:
                self.trace.error('Invalid config')

    def run(self):
        if self.connect():
  	        self.readData(0)

    def connect(self):
        self.serial_.baudrate = self.config_['serial']['baudrate']
        
        self.serial_.port = self.config_['serial']['port']
        if self.config_['serial']['parity'] == 0:
            self.serial_.parity = serial.PARITY_NONE
        elif self.config_['serial']['parity'] == 1:
            self.serial_.parity = serial.PARITY_ODD
        elif self.config_['serial']['parity'] == 2:
            self.serial_.parity = serial.PARITY_EVEN

        if self.config_['serial']['stopbits'] == 1:
            self.serial_.stopbits = serial.STOPBITS_ONE
        elif self.config_['serial']['stopbits'] == 2:
            self.serial_.stopbits = serial.STOPBITS_TWO

        if self.config_['serial']['databits'] == 8:
            self.serial_.bytesize = serial.EIGHTBITS

        try:
            self.serial_.open()
            return  True
        except Exception as err:
            self.trace.error('Serial open failed : %s'%err);
            return  False

    def readData(self, running_time = 0):
        now = datetime.datetime.now()

        receive_buffer = b''

        while True:
            receive_buffer = self.serial_.readline(200)
            index = receive_buffer.find("$GNGGA")

            if index > 0:
                fields = receive_buffer[index:].split(',')
                if len(fields) > 4:
                    try:
                        if (fields[2] != '') and (fields[4] != ''):
                            if self.base_[0] is None:
                                self.base_ = float(fields[2]) / 100, float(fields[4]) / 100
                            else:
                                current = float(fields[2]) / 100, float(fields[4]) / 100
                                distance =  haversine(self.base_, current)
                                self.trace.debug('%f,%f -> %f,%f : %f'%(self.base_[0], self.base_[1], current[0], current[1], distance))
                    except Exception as err:
                        self.trace.error('Invalid payload : %s - %s'%(err, receive_buffer[index:]))
	            
	
