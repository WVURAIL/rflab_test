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
# 
# Import the visa libraries
import visa
import pyvisa
import socket
import numpy as py
import os

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

# The following function takes the raw data file data, which is an IEEE binary 
#block, and interprets the header. The header tells us how many bytes are
#in the file. The function strips off the header and outputs the 
#remaining data to be saved to a user defined file type.
def binblock_raw(data_in):

#Grab the beginning section of the data file, which will contain the header.
    Header = str(data_in[0:12])
    print("Header is " + str(Header))

#Find the start position of the IEEE header, which starts with a '#'.
    startpos = Header.find("#")
    print("Start Position reported as " + str(startpos))

#Check for problem with start position.
    if startpos < 0:
        raise IOError("No start of block found")

#Find the number that follows '#' symbol. This is the number of digits in the block length.
    Size_of_Length = int(Header[startpos+1])
    print("Size of Length reported as " + str(Size_of_Length))

##Now that we know how many digits are in the size value, get the size of the data file.
    Image_Size = int(Header[startpos+2:startpos+2+Size_of_Length])
    print("Number of bytes in file are: " + str(Image_Size))

# Get the length from the header
    offset = startpos+Size_of_Length+2

# Extract the data out into a list.
    return data_in[offset:offset+Image_Size]

# load .csa file, used for the purpose of troubleshooting. If running from the measurement state
#    myFieldFox.open("MMEM:STOR:SNP:DATA '190611_8_13.s2p'")    
#    myFieldFox.write("MMEM:STOR:SNP:DATA '190611_8_13.s2p'")
    myFieldFox.open("MMEM:STOR:SNP:DATA '611191_HIGH.s2p'")    
    myFieldFox.write("MMEM:STOR:SNP:DATA '611191_HIGH.s2p'")
    myFieldFox.close()
    
# Enter a file name and directory where file will be saved to, this can be modified for any
os.getcwd()
script_dir = os.path.dirname('C:\\Users\\Jacob\\Documents\\Python Scripts') #<-- absolute dir the script is in
dir = 'C:\\Users\\Jacob\\Documents\\Python Scripts\\LAN_Transfer\\61119'
if os.path.exists(dir):
    pass
else:
    os.makedirs(dir)
abs_file_path = os.path.join(script_dir, dir)
#print(abs_file_path)
 
# Reads block data from the specified file location.
myFieldFox.write("MMEMory:DATA? '611191_HIGH.s2p'")
raw_file = myFieldFox.read_raw()
 
#Creating location to write myFieldFox data to and then saving and closing the location.   
path = 'C:\\Users\\Jacob\\Documents\\Python Scripts\\LAN_Transfer\\61119\\190611_1_23.s2p'
AO = open(path, 'wb')
AO.write(raw_file)
AO.close()

#Saving the produced images as .png files at specified locations
import skrf as rf
import matplotlib.pyplot as plt
rs = rf.Network(path)

#plot the s parameters 

#S11 = rs.plot_s_db(0,0)
#S21 = rs.plot_s_db(1,0)
#plt.savefig('C:\\Users\\Jacob\\Documents\\Python Scripts\\LAN_Transfer\\61119\\190611_8_13.jpg')

S12 = rs.plot_s_db(0,1)
S22 = rs.plot_s_db(1,1)
plt.savefig('C:\\Users\\Jacob\\Documents\\Python Scripts\\LAN_Transfer\\61119\\190611_1_23.jpg')

rs.plot_s_db()
plt.savefig('C:\\Users\\Jacob\\Documents\\Python Scripts\\LAN_Transfer\\61119\\190611_1_23a.jpg')

#plot a smith chart of s11, s12, s21, s22
#smith = rs.plot_s_smith(lw=1)
#plt.title('Smith Chart')
#plt.savefig('C:\\Users\\Jacob\\Documents\\Python Scripts\\LAN_Transfer\\61119\\190611_3s.jpg')

print (Errcheck())
myFieldFox.close()