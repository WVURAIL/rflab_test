# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 20:10:04 2019

@author: Jacob
"""


import skrf as rf
import matplotlib.pyplot as plt
import os
import numpy as np

#Check cwd and merge desired path if difference exists
dir = os.getcwd()
combo="\\190611_2&3L"
my_dpi=96
path = 'C:\\Users\\Jacob\\Documents\\Python Scripts\\LAN_Transfer\\190611'
if dir==path:
    pass
else:
    os.path.join(dir, path)
    
p1 = path + "\\190611_2\\190611_2_13L.s2p"
p2 = path + "\\190611_3\\190611_3_13L.s2p"

'''
Create paths and use skrf module to create workable arrays
'''
rs = rf.Network(p1)
rs2 = rf.Network(p2)
p1_s21 = rs.s21
p2_s21 = rs2.s21
p1a=p1_s21.s_db[:]
p2a=p2_s21.s_db[:]


'''
Change arrays from 3d to workable 2d
'''
p1a=p1a.reshape(1001, 1)
p2a=p2a.reshape(1001, 1)
p3a=p2a - p1a

'''
Plot deviation and savefig to file
'''
fig_dir= path + combo 
if os.path.exists(fig_dir):
    pass
else:
    os.makedirs(fig_dir)
    
plt.axhline(y=0.0, color='k', linestyle='-')
x=np.linspace(2000000 ,2000000001, 1001)
p3s=p3a.tolist()
plt.xlabel('Frequency(Hz)')
plt.ylabel('dB')
plt.plot(x, p3s, label='190611_2&3L')
plt.legend(loc='best')
plt.savefig(fig_dir + combo + '.jpg', dpi=my_dpi*10)
plt.close()

result=np.column_stack((x,p3s))
np.savetxt(fig_dir + combo + '.s2p', result, header=('Left Column is Frequency(Hz)\n' 
                                                     'Right Column is the difference of 190611_3 and 190611_2 in dB\n'
                                                     'Saved to file using np.savetxt\n'
                                                     'Data formatted as ndarray in Python 3'))

if len(p3a[:]) > 1:
    p3a_max=np.amax(p3a)
    p3a_max_loc=np.where(p3a == p3a_max)
    cord = list(zip(p3a_max_loc[0], p3a_max_loc[1]))
    y=("\nThe max deviation is %s located at %s\n" %(p3a_max, cord))
    if p3a_max>1:
        print(y)
        print('\nWARNING: Deviation Exceeds Reccommended Parameters\n')
    else:
        print('\nSUCCESS: Deviation is Acceptable\n')

'''
ALL CODE BELOW THIS POINT IS SENSELESS RAMBLING THROUGH WHICH THE ABOVE CODE WAS CREATED.
'''      
        
        

'''
open file locations for momentary usage
'''
'''
pa = open(path + "\\190611_2\\190611_2_13L.s2p", 'rb')
pb = open(path + "\\190611_3\\190611_3_13L.s2p", 'rb')
'''
#path alpha, path bravo

'''
Switch from Wrapper to lists and arrays
'''
'''
la=pa.read()
lb=pb.read()
'''
#list alpha, list bravo
'''
#Was attempting to remodel into a string that could be reformatted into a .s2p file
#This rabbit hole, luckily, was terminated by the discovery that plt could use current
#formatting and re-introduction into the rs.Network was unneeded.

aa=np.asarray(la)
ab=np.asarray(lb)
#array alpha, array bravo
'''        
        
        
        
'''
Strip header, compare string lengths, and pad with zeros
'''
'''
alpha = list1.decode()
#should be str
header = alpha.split('50\r\n')
###used del since we want to remove the entire first portion of the header###
del header[0]

beta = list2.decode()
header2 = beta.split('50\r\n')
del header2[0]

lsdata = len(header)
lsdata2 = len(header2)
'''


'''
This bit needs some help to account for potentially different counts for the test
'''
'''
if lsdata != lsdata2:
    if lsdata < lsdata2:
        pdata = np.pad(sdata, (lsdata2 - lsdata), 'constant')
        print(pdata)
    else:
        pdata2 = np.pad(sdata2, (lsdata - lsdata2), 'constant')
        print(pdata2)
else:
    pass
'''

'''
Add path to opperating Network and Graph s-parameters with specified 
LNA number added to end of variable label   
'''                           
'''
S21_1 = rs.plot_s_db(1,0)
S21_2 = rs2.plot_s_db(1,0)
plt.savefig(path + "\\190620_2&3_13L_UP.jpg")
plt.close()
'''


'''
###Working, Simple Code###

import skrf as rf
import matplotlib.pyplot as plt
import os
import numpy as np

#Check cwd and merge desired path if difference exists
dir = os.getcwd()
path = 'C:\\Users\\Jacob\\Documents\\Python Scripts\\LAN_Transfer\\190611'
if dir==path:
    pass
else:
    os.path.join(dir, path)

#open file locations for momentary usage
path1 = open(path + "\\190611_2\\190611_2_13L.s2p", 'rb')
path2 = open(path + "\\190611_3\\190611_3_13L.s2p", 'rb')

list1 = path1.read()
list2 = path2.read()

a = list1.decode()
#should be str
header = a.split('50\r\n')
del header[0]
#used del since we want to remove the entire first portion of the header
sdata = header #rename new stripped data

b = list2.decode()
header2 = b.split('50\r\n')
del header2[0]
sdata2 = header2
'''



'''
stat, p = ttest_ind(alpha, beta)
print('Statistics=%.3f, p=%.3f' % (stat, p))
'''

'''
#Interpret the results
devitation = 0.02 #db
if p>deviation:
    print('\nCaution: Result Variance Critical\n')
    break
else:
    print('\nProceed: Requirements Satisfied\n')
'''
