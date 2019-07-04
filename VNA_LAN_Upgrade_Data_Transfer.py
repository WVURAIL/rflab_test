# -*- coding: utf-8 -*-
"""
Created on Fri May 17 15:47:55 2019

@author: Jacob
"""

# -*- coding: utf-8 -*-
# Python for Test and Measurement

# Requires VISA installed on controlling PC
# 'http://www.keysight.com/find/visa'
#
# Requires PyVISA to use VISA in Python
# 'http://pyvisa.sourceforge.net/pyvisa/'

# Keysight IO Libraries 18.x 64-Bit Keysight VISA (as primary)
# Anaconda Python 4.4.0 32 bit
# pyvisa 3.6.x

##"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Example Description: 
# A python sample program utilizing pyvisa to connect and control a FieldFox 
# Family Vector Network Analyzer. 
#
# The application performs the following:
# Imports the pyvisa libraries and operating system dependent functionality;
# Establishes a visa resource manager;
# Opens a connection to the FieldFox based on the instrument's VISA address as acquired via Keysight Connection Expert
# Sets the visa time out (increasing the timeout as compared to the default). 
# Clears the event status register and clears the error queue;
# Queries the instrument via the '*IDN?' identification query;
# Defines an error check function and checks the system error queue;
# Defines a binblock function for obtaining header information
# Saves a user configured and calibrated S2P Touchstone file to the current media selected on the FieldFox
# Utilizes the MMEM:DATA? query command to query the file bytes as a binary bin block transfer 
# (required for the MMEM:DATA? command). 
# 
# Writes the Touchstone *.S2P file to the controlling PC saving the file 


# Import the visa libraries
import visa
import pyvisa
import socket
import numpy as py
import os
import skrf as rf
import matplotlib.pyplot as plt

# Open a VISA resource manager pointing to the installation folder for the Keysight Visa libraries. 
rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll') 

# Based on the resource manager, open a session to a specific VISA resource string as provided via
# Keysight Connection Expert
# ALTER LINE BELOW - Updated VISA resource string to match your specific configuration
myFieldFox = rm.open_resource('TCPIP0::192.168.1.1::inst0::INSTR') 

#Set Timeout - 10 seconds
myFieldFox.timeout = 10000

# Clear the event status registers and empty the error queue
myFieldFox.write("*CLS")

# Query identification string *IDN? 
myFieldFox.write("*IDN?")
print (myFieldFox.read())

# Define Error Check Function
def Errcheck():
    myError = []
    ErrorList = myFieldFox.query("SYST:ERR?").split(',')
    Error = ErrorList[0]
    while int(Error)!=0:
        print ("Error #: " + ErrorList[0])
        print ("Error Description: " + ErrorList[1])
        myError.append(ErrorList[0])
        myError.append(ErrorList[1])
        ErrorList = myFieldFox.query("SYST:ERR?").split(',')
        Error = ErrorList[0]
        myError = list(myError)
        return myError

 
print(Errcheck())
 
    
# Enter a file name and directory where file will be saved to, this can be modified for any
os.getcwd()
script_dir = os.path.dirname('C:\\Users\\Jacob\\Documents\\Python Scripts') #<-- absolute dir the script is in
'''
Insert LNA Label Number Below. Additionally, change the file name symmetrically 
in the myFieldFox.write() lines at the beginning of each Power setting varient block.
5 Changes in all need made per LNA file transfer.
'''
lna_num = '\\190611_12'

#Authenticate Desired File Path
dir = 'C:\\Users\\Jacob\\Documents\\Python Scripts\\LAN_Transfer\\190611' + lna_num
if os.path.exists(dir):
    pass
else:
    os.makedirs(dir)
abs_file_path = os.path.join(script_dir, dir)
 

# Reads block data from the specified file location.
'''
###LOW POWER BLOCK from 13###
'''

myFieldFox.write("MMEMory:DATA? '190611_12_13L.s2p'")
raw_file_13L = myFieldFox.read_raw()

#Creating location to write myFieldFox data to and then saving and closing the location.
#Low Power Setting   
path_low = dir + lna_num + '_13L.s2p'
plt.tight_layout()
my_dpi=96

with open(path_low, 'wb') as AO:
    AO.write(raw_file_13L)
    
#Saving the produced images as .png files at specified locations
rs = rf.Network(path_low)
#Plot S21 for rs

S21 = rs.plot_s_db(1,0)
plt.savefig(dir + lna_num + '_13L.jpg', bbox_inches="tight", dpi=my_dpi*10)
plt.close()
    
rs.plot_s_db()
plt.savefig(dir + lna_num + '_13LA.jpg', dpi=my_dpi*10)
plt.close()


# Reads block data from the specified file location.
'''
###LOW POWER BLOCK from 23###
'''
myFieldFox.write("MMEMory:DATA? '190611_12_23L.s2p'")
raw_file_23L = myFieldFox.read_raw()

#Creating location to write myFieldFox data to and then saving and closing the location.
#Low Power Setting   
path_low2 = dir + lna_num + '_23L.s2p'
plt.tight_layout()
my_dpi=96

with open(path_low2, 'wb') as AO:
    AO.write(raw_file_23L)
    
#Saving the produced images as .png files at specified locations
rs2 = rf.Network(path_low2)
#Plot S21 for rs

S21 = rs2.plot_s_db(1,0)
plt.savefig(dir + lna_num + '_23L.jpg', bbox_inches="tight", dpi=my_dpi*10)
plt.close()
    
rs2.plot_s_db()
plt.savefig(dir + lna_num + '_23LA.jpg', dpi=my_dpi*10)
plt.close()


'''
###HIGH POWER BLOCK from 13###
'''
myFieldFox.write("MMEMory:DATA? '190611_12_13H.s2p'")
raw_file_13H = myFieldFox.read_raw() 

#High Power Setting
path_13H = dir + lna_num + '_13H.s2p'
with open(path_13H, 'wb') as AO2:
    AO2.write(raw_file_13H)
    
rs3 = rf.Network(path_13H)
#Plot S11, S12, S22
S11 = rs3.plot_s_db(0,0)
S12 = rs3.plot_s_db(0,1)
S22 = rs3.plot_s_db(1,1)
plt.savefig(dir + lna_num + '_13H.jpg', dpi=my_dpi*10)
plt.close()
#Plot all
rs3.plot_s_db()
plt.savefig(dir + lna_num + '_13HA.jpg', dpi=my_dpi*10)
plt.close()


'''
###HIGH POWER BLOCK from 23###
'''
myFieldFox.write("MMEMory:DATA? '190611_12_23H.s2p'")
raw_file_23H = myFieldFox.read_raw() 

#High Power Setting
path_23H = dir + lna_num + '_23H.s2p'
with open(path_23H, 'wb') as AO2:
    AO2.write(raw_file_23H)
    
rs4 = rf.Network(path_23H)
#Plot S11, S12, S22
S11 = rs4.plot_s_db(0,0)
S12 = rs4.plot_s_db(0,1)
S22 = rs4.plot_s_db(1,1)
plt.savefig(dir + lna_num + '_23H.jpg', dpi=my_dpi*10)
plt.close()
#Plot all
rs4.plot_s_db()
plt.savefig(dir + lna_num + '_23HA.jpg', dpi=my_dpi*10)
plt.close()

'''
plot a smith chart of s11, s12, s21, s22
smith = rs.plot_s_smith(lw=1)
plt.title('Smith Chart')
plt.savefig('C:\\Users\\Jacob\\Documents\\Python Scripts\\LAN_Transfer\\61119\\190611_3s.jpg')
'''


print (Errcheck())
myFieldFox.close()