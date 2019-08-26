#Importing data from Touchstone (SnP) file
import skrf as rf
import os
import sys 
import matplotlib.pyplot as plt

#Must import data from flash drive
os.getcwd()
usbdir=input("Please Input USB Flashdrive Directory '(e.g. E:)'\n")
sdir = os.path.dirname(usbdir) #<-- absolute dir the script is in

#Insert LNA Label Number
lna_num = "\\" + input("Input LNA Label Number:\n")

#Authenticate Desired File Path
dir = input("Please input path to final file destination:\n") + lna_num
#Example: C:\\Users\\Jacob\\Documents\\Python Scripts\\LAN_Transfer\\190611

#Check for pre-existing path, merge if necessary
if os.path.exists(dir):
    pass
else:
    os.makedirs(dir)
abs_file_path = os.path.join(sdir, dir)


# Reads block data from the specified file location.
'''
###LOW POWER BLOCK from 13###
'''
#Low Power Setting  
#open flashdrive path as bytes
usbf_13L = open(sdir + lna_num + '_13L.s2p', 'rb')

#PC path location
path_low = dir + lna_num + '_13L.s2p'

with open(path_low, 'wb') as AO:
    AO.write(usbf_13L.read())
    
#Saving the produced images as .png files at specified locations
rs = rf.Network(path_low)
#Plot S21 for rs

plt.tight_layout()
my_dpi=96
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
#Low Power Setting
#open flashdrive path as bytes
usbf_23L = open(sdir + lna_num + '_23L.s2p', 'rb')


path_low2 = dir + lna_num + '_23L.s2p'
plt.tight_layout()
my_dpi=96

with open(path_low2, 'wb') as AO:
    AO.write(usbf_23L.read())
    
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
#High Power Setting
#open flashdrive path as bytes
usbf_13H = open(sdir + lna_num + '_13H.s2p', 'rb')


path_13H = dir + lna_num + '_13H.s2p'
with open(path_13H, 'wb') as AO2:
    AO2.write(usbf_13H.read())
    
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
#High Power Setting
#open flashdrive path as bytes
usbf_23H = open(sdir + lna_num + '_23H.s2p', 'rb')


path_23H = dir + lna_num + '_23H.s2p'
with open(path_23H, 'wb') as AO2:
    AO2.write(usbf_23H.read())
    
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
