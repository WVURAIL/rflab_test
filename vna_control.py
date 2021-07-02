#!/usr/bin/env python
# coding: utf-8
# # VNA Control 
# # # All commands http://na.support.keysight.com/pna/help/latest/Programming/GP-IB_Command_Finder/
FieldFox Programming Guide (keysight.com) http://na.support.keysight.com/fieldfox/help/Programming/webhelp/FFProgrammingHelp.htm
##############################################################################
#   import python packages 

get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import time
import pyvisa as visa
import csv
import time

##############################################################################
# load visa library 
rm=visa.ResourceManager('C:\\Windows\\System32\\visa64.dll')  # windows
# TODO linux
# https://edadocs.software.keysight.com/kkbopen/linux-io-libraries-faq-589309025.html
# https://www.keysight.com/us/en/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html click linux 
# 
print(rm.list_resources()) # find connected instrument and get instrument address
instrument_address = rm.list_resources()

VNA = rm.open_resource(instrument_address[0]) # load  instrument object
VNA.write('*IDN?')
IDN=VNA.read()
print(IDN)
VNA.timeout =  10000

# # select NA mode
# ```
# Relevant Modes
#  ALL
#  
# Parameters
#   
#  
# <string>
#  Operating Mode. Case-sensitive. Choose from the modes that are installed on your FieldFox:
# 
# "CAT"
# 
# "IQ"
# 
# "NA"
# 
# "SA"
# 
# "Power Meter"
# 
# "VVM"
# 
# "Pulse Measurements"
# 
# "ERTA"
#  
# Examples
#  INST "NA";*OPC?
#  ```
# 
# common commands: http://na.support.keysight.com/pna/help/latest/Programming/GP-IB_Command_Finder/Common_Commands.htm

print(VNA.query('INSTrument:CATalog?')) # print available modes of intrsument
VNA.write('INST "NA";*OPC?') # set in network analyzer mode  
if VNA.read()[0] == '1':
    print("Successfully set NA mode")

##########################################################################
def set_freq_lims(start, stop):    
	""" 
		Set frequency limits of measurement
		Commands:
		http://na.support.keysight.com/pna/help/latest/Programming/GP-IB_Command_Finder/Sense/Frequency.htm
	"""
    VNA.write('SENSe:FREQuency:STARt ' + str(start))
    VNA.write('SENSe:FREQuency:STOp ' + str(stop))
    
def check_power_mode():
	"""
	CHECK POWER MODE
	"""
	
    print(f"Current Output power is {VNA.query('SOURce:POWer:ALC:MODE?')} ")
def set_power_mode(output_power, nominal_power = -15):
    print(f"Setting output power to {output_power}")
    VNA.write('SOURce:POWer:ALC:MODE ' + str(output_power))
    check_power_mode()
    if str(output_power) == "MAN":
        print(f"Setting nominal power level {nominal_power}")
        
  
def measure_s_parameter(measurement, output_power,start_freq, stop_freq, serial_num="LNA1"):
    print("setting frequency limits")
    set_freq_lims(start_freq,stop_freq)
    check_power_mode()
    set_power_mode(output_power)
    print(f"Measuring {measurement} with Output mode {output_power}")
    VNA.write(':CALCulate:PARameter1:DEFine ' + measurement)
    # http://na.support.keysight.com/pna/help/latest/Programming/GP-IB_Command_Finder/Calculate/Parameter.htm COMMANDS FOR MEASUREMENT PARAMETERS
    VNA.write(':CALCulate:SELected:FORMat MLOGarithmic')
    # MLINear, MLOGarithmic, PHASe, UPHase 'Unwrapped phase, IMAGinary,REAL
    # POLar SMITh, SADMittance 'Smith Admittance, SWR, GDELay 'Group Delay
    # http://na.support.keysight.com/pna/help/latest/Programming/GP-IB_Command_Finder/Calculate/Format_Calc.htm
    time.sleep(1)
    VNA.write(':DISPlay:WINDow:TRACe:Y:SCALe:AUTO') # scaling plot on the VNA screen
	  #### OTHER VNA COMMANDS THAT CONTROL THE SCREEN
	  # http://na.support.keysight.com/pna/help/latest/Programming/GP-IB_Command_Finder/Display.htm#yauto
	  ##########
    data = VNA.query('CALCulate:DATA:FDaTa?') 
    ### http://na.support.keysight.com/pna/help/latest/Programming/GP-IB_Command_Finder/Calculate/Data.htm # COMMANDS TO SAVE DATA
    data = np.asarray(data.split(',')[:-1])   
    data = np.array([float(i.lower()) for i in data])
    plt.figure()
    plt.plot(np.linspace(start_freq/1e6,stop_freq/1e6,data.shape[-1]),data)
    plt.xlabel("MHz")
    plt.ylabel("dBm")
    plt.title(f"{measurement}_{serial_num}")
    print(f"DONE measuring {measurement}")
    plt.savefig(f"{serial_num}_{measurement}.png")
    VNA.write(':CALCulate:SELected:FORMat REAL')
    time.sleep(1)
    data_real = VNA.query('CALCulate:DATA:SDaTa?')
    data_real = np.asarray(data_real.split(',')[:-1])   
    VNA.write(':CALCulate:SELected:FORMat IMAG')
    time.sleep(1)
    data_imag = VNA.query('CALCulate:DATA:SDaTa?')
    data_imag = np.asarray(data_imag.split(',')[:-1])   
    data_raw = np.array([float(i[0].lower())+float(i[1].lower())*1j  for i in zip(data_real,data_imag)])
    plt.show()
    return data, data_raw

# ```
# For NA Mode:
# Reverse measurements are available ONLY with full S-parameter option.
# 
# S11 - Forward reflection measurement
# 
# S21 - Forward transmission measurement
# 
# S12 - Reverse transmission
# 
# S22 - Reverse reflection
# 
# A - A receiver measurement
# 
# B - B receiver measurement
# 
# R1 - Port 1 reference receiver measurement
# 
# R2 - Port 2 reference receiver measurement
# ```
# In[ ]:

##########################################################################
## set start and stop freq

start_freq = 1e7
stop_freq = 2e9
set_freq_lims(start_freq,stop_freq)



S11, S11_raw = measure_s_parameter("S11", output_power="LOW",start_freq=start_freq, stop_freq=stop_freq)
S21, S21_raw = measure_s_parameter("S21", output_power="LOW", start_freq=start_freq, stop_freq=stop_freq)
S12, s12_raw = measure_s_parameter("S12", output_power="HIGH", start_freq=start_freq, stop_freq=stop_freq)
S22, S22_raw = measure_s_parameter("S22", output_power="HIGH", start_freq=start_freq,stop_freq= stop_freq)
plt.figure()

plt.plot(np.linspace(start_freq/1e6,stop_freq/1e6,S11.shape[-1]), S11, label="S11")
plt.plot(np.linspace(start_freq/1e6,stop_freq/1e6,S12.shape[-1]), S12, label="S12")
plt.plot(np.linspace(start_freq/1e6,stop_freq/1e6,S22.shape[-1]), S22, label="S22")
plt.legend()
plt.show()

