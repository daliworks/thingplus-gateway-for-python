#!/usr/bin/python

import numpy as np
from scipy import signal                                                                                
import math
import serial
import binascii
import struct
import time
import datetime
import trace
from threading import *

class   Alps(Thread):
    def __init__(self, _config = None):
        Thread.__init__(self)
        self.config_ = {
            'serial' : {
                'port' : '/dev/ttyUSB0',
                'baudrate' : 921600,
                'parity' : 'none',
                'stopbits' : 1,
                'databits' : 8
            }
        }

        self.trace = trace.Trace()
        self.trace.name = 'ALPS'

        self.serial_ = serial.Serial()
        self.running_time_ = 1800
        self.time_table_ = []

    def isValid(self, data):
        data_array = bytearray(data)
        sum = 0 
        for byte in data_array[:len(data_array)-1]:
            sum += byte

        return  (sum % 256) == data_array[len(data_array) - 1]

    def setTimeTable(self, _time_table):
        _time_table.sort()
        self.time_table_ = _time_table
        self.trace.debug(self.time_table_)

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
            logging.error('Serial open failed : %s'%err);
            return  False

    def run(self):
        if self.connect():
            if len(self.time_table_) != 0:
                while True:
                    for item in self.time_table_:
                        now = datetime.datetime.now()
                        seconds = now.hour * 60 * 60 + now.minute * 60 + now.second
                        if seconds < (item * 60 * 60):
                            sleep_time = (item * 60 * 60) - seconds
                            self.trace.debug('Sleep : %d:%02d:%02d'%((sleep_time / 60 / 60), (sleep_time / 60) % 60, (sleep_time % 60)))
                            time.sleep(sleep_time)
                            self.readData(self.running_time_)
                    now = datetime.datetime.now()
                    seconds = now.hour * 60 * 60 + now.minute * 60 + now.second
                    sleep_time = (24 * 60 * 60) - seconds
                    self.trace.debug('Sleep : %d:%02d:%02d'%((sleep_time / 60 / 60), (sleep_time / 60) % 60, (sleep_time % 60)))
                    time.sleep(sleep_time)
            else: 
                self.readData(0)
                


    def readData(self, running_time = 0):
        now = datetime.datetime.now()
        data_file = open('%d%02d%02d%02d%02d%02d.csv'%(now.year, now.month, now.day, now.hour, now.minute, now.second), 'at')
        previous_datetime = now 

        k_cpt = 0     # computing temp number
        k_fft = 1
        array_cpt = np.array([])
        array_fft = np.array([])
        t_cpt = np.array({})
        i_cpt = 1024 / 32 * 10     # 10 : distributed computing interval, 10sec
        i_fft = 6                  # i_cpt * i_fft : fft interval, sec
        j_fft = 0
        j_freq = 0
        L_fft_sec = float(60)         # sec
        Fs = 1024

        forever = False
        start_time = time.time()
        receive_buffer = b''

        while (running_time == 0) or (time.time() < (start_time + running_time)):
            receive_buffer = receive_buffer + self.serial_.read(200)

            if (len(receive_buffer) >= 3) and (receive_buffer[0:3] != b'\xff\xc2\x81'):
                for i in range(len(receive_buffer) - 2):
                    if receive_buffer[i:i+3] == b'\xff\xc2\x81':
                        receive_buffer = receive_buffer[i:]

            if len(receive_buffer) >= 196:
                data = receive_buffer[:196]
                receive_buffer = receive_buffer[196:]

                now = datetime.datetime.now()
                timestamp = time.time()
                if self.isValid(data):
                    array_cpt_temp_x = np.array([])
                    array_cpt_temp_y = np.array([])
                    array_cpt_temp_z = np.array([])
                    line = '%s'%timestamp
                    for i in range(3, 195, 6): 
                        x = struct.unpack('<h', data[i:i+2])[0]
                        y = struct.unpack('<h', data[i+2:i+4])[0]
                        z = struct.unpack('<h', data[i+4:i+6])[0]
                        line = line + ',%d,%d,%d'%(x,y,z)
                        array_cpt_temp_x = np.append(array_cpt_temp_x, x)
                        array_cpt_temp_y = np.append(array_cpt_temp_y, y)
                        array_cpt_temp_z = np.append(array_cpt_temp_z, z)
                    #self.trace.debug(line)
                    line = line + '\n'

                    if previous_datetime.hour != now.hour:
                        data_file.close()
                        data_file = open('%d%02d%02d%02d%02d%02d.csv'%(now.year, now.month, now.day, now.hour, now.minute, now.second), 'at')

                    #data_file.write(line)

                    # fft
                    if (k_fft >= i_fft*(1-(L_fft_sec/60))) and (k_fft < i_fft):
                        array_fft = np.append(array_fft,array_cpt_temp_x)
                    elif k_fft % i_fft == 0:
                        L_fft = len(array_fft)        # Length of signal
                        #print(L_fft)
                        #NFFT = L_fft      # ?? NFFT=2^nextpow2(length(y))  ??
                        #k = np.arange(NFFT)
    
                        ################# PSD #################
                        array_fft=array_fft - np.mean(array_fft)
                        data_arranged=signal.detrend(array_fft)
                        L_fft=float(len(data_arranged))
                        Mdata_Ndivision = 6
                        NFFT_psd_Mdata_temp=L_fft / Mdata_Ndivision
                        for k in np.arange(1,100).reshape(-1):
                            NFFT_psd_Mdata=2 ** k
                            if NFFT_psd_Mdata >= NFFT_psd_Mdata_temp:
                                break
    
                        Noverlap= float(3) / 4
                        # overlap
                        Ndivision=int(math.ceil(1 + (L_fft / NFFT_psd_Mdata - 1) / (1 - Noverlap)))
                        LminusOverlap=NFFT_psd_Mdata - (NFFT_psd_Mdata * Noverlap)
                        xStart=np.arange(1,(Ndivision * LminusOverlap),LminusOverlap) - 1
                        xEnd=xStart + NFFT_psd_Mdata
                        Mdata_division_temp=np.zeros((int(xEnd[0]),Ndivision))
                        for k in range(0,Ndivision-1):
                            Mdata_division_temp[0:NFFT_psd_Mdata, k]=data_arranged[int(xStart[k]):int(xEnd[k])]
                        Mdata_division_temp[0:int(L_fft)-int(xStart[-1]),Ndivision-1]=data_arranged[int(xStart[-1]):int(L_fft)]
    
                        # window, square
                        L_window=len(Mdata_division_temp[:,0])
                        Window=np.hamming(L_window)
                        Mdata_window=np.zeros((int(xEnd[0]),Ndivision))
                        for k in range(0,Ndivision):
                            Mdata_window[:,k] = Mdata_division_temp[:,k] * Window
                        Mdata_fft=np.zeros((int(xEnd[0]),Ndivision), dtype=np.complex)
                        Mdata_Y=np.zeros((int(xEnd[0]/2+1),Ndivision))
                        for k in range(0,Ndivision):
                            Mdata_fft[:,k]=np.fft.fft(Mdata_window[:,k],NFFT_psd_Mdata) ** 2
                            try:
                                Mdata_Y[:,k]=2 * abs(Mdata_fft[0:int(NFFT_psd_Mdata / 2 + 1), k])
                            except Exception as err:
                                print('Exception : %s'%err)
                                print('k type is %s'%type(k))
                                print('NFFT_psd_Mdata type is %s'%type(NFFT_psd_Mdata))
                        Mdata_square_Ysum=Mdata_Y.sum(axis = 1) / (NFFT_psd_Mdata * Fs)
                        PSD_saved = Mdata_square_Ysum[0:50]

                        index_max = np.argmax(PSD_saved) 
                        print('PSD[{0}] = {1}Hz,{2}'.format(index_max, (index_max+1) * 0.25 ,PSD_saved[index_max]))
                        #print(PSD_saved)
                        
                        # graph
                        f_Mdata= (Fs / 2) * np.linspace(0,1,NFFT_psd_Mdata / 2 + 1)
                        # plt.plot(f_Mdata,Mdata_square_Ysum)
                        # plt.show()
                        # exit()
    
                        ################# FFT #################
                        # Y = np.fft.fft(array_fft)/NFFT        # fft computing and normaliation
                        # Y = Y[range(math.trunc(NFFT/2))]          # single sied frequency range
                        # amplitude_Hz = 2*abs(Y)
                        # print(amplitude_Hz)
                        # print(len(amplitude_Hz))
                        # k_fft = 1
                        # array_fft = np.array([])
                    if ('f_Mdata' in locals()) and (j_freq == 0):
                        #data_file_PSD_freq_name = ('%d%02d%02d%02d%02d%02d_PSD_freq.csv'%(now.year, now.month, now.day, now.hour, now.minute, now.second))
                        #data_file_PSD_freq = open(data_file_PSD_freq_name,'at')
                        #/csv.writer(data_file_PSD_freq).writerow(f_Mdata)
                        #data_file_PSD_freq.close()
                        j_freq = j_freq + 1

                    # save PSD, cpt data
                    if k_fft % i_fft == 0:
                        #line_PSD = PSD_saved + '\n'
                        #print(line_PSD)
                        #data_file_PSD.write(line_PSD)
                        #data_file_PSD = open(data_file_PSD_name,"at")
                        #csv.writer(data_file_PSD).writerow(PSD_saved)
                        #data_file_PSD.close()

                        k_fft = 1
                        #print(array_fft.size)
                        #data_file_PSD_data = open(data_file_PSD_data_name,"at")
                        #csv.writer(data_file_PSD_data).writerow(array_fft)
                        #data_file_PSD_data.close()
    
                        array_fft = np.array([])


                    # distributed computing
                    k_cpt = k_cpt + 1
                    if k_cpt % i_cpt != 0:
                        array_cpt = np.append(array_cpt,array_cpt_temp_x)
                    elif k_cpt % i_cpt == 0:
                        data_max = max(abs(array_cpt))
                        data_rms = np.sqrt(np.mean(array_cpt**2))

                        array_cpt = np.array([])
                        k_cpt = 0
                        line_cptData_cpt = '%f'%(data_max) + ',%f'%(data_rms)

                        k_fft = k_fft + 1

                        #print(k_fft,i_fft*(1-(L_fft_sec/60)))

                elif len(data) != 0:
                    sefl.trace.error('Invalid : %s'%(binascii.hexlify(data)))

                previous_datetime = now 

        data_file.close()
