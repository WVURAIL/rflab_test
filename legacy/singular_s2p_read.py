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
path = 'C:\\Users\\Jacob\\Documents\\Python Scripts\\LAN_Transfer\\190611'
if dir==path:
    pass
else:
    os.path.join(dir, path)

#open file locations for momentary usage
path1 = open(path + "\\190611_1\\190611_1_13L.s2p", 'rb')
path2 = open(path + "\\190611_2\\190611_2_13L.s2p", 'rb')
      
#Add path to opperating Network    
rs = rf.Network(path1)
rs2 = rf.Network(path2)

#Graph s-parameters with specified LNA number added to end of variable label
S21_1 = rs.plot_s_db(1,0)
S21_2 = rs2.plot_s_db(1,0)
plt.savefig(path + "\\190620_1_13L_UP.jpg")
plt.close()


'''
Must switch the lists from path1 and path2 files to arrays
'''
with open(path + "\\190611_1\\190611_1_13L.s2p", 'rb') as file1, open(path + "\\190611_2\\190611_2_13L.s2p", 'rb') as file2:
    list1 = file1.read()
    list2 = file2.read()
    #array1 = np.asarray(list1)
    #array2 = np.asarray(list2)
    

'''
Strip header, compare string lengths, and pad with zeros
'''
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

lsdata = len(a)
lsdata2 = len(b)

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
#We shall now compare the data and determine the difference between
#the standard and the object subject to scrutiny 
with open(path + "\\190620_1_13L.s2p",'rb') as path1, open(path + "\\190620_1_13H.s2p", 'rb') as path2:
    first_list=list(path1)
    second_list=list(path2)
    para_ntwk = [rs, rs2]
    mean_ntwk = rf.average(para_ntwk)
    print(mean_ntwk)
    import operator
    para_diff = [i - j for i, j in zip(list(path1), list(path2))]
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

     
'''    
with ExitStack() as stack:
    files = [stack.enter_context(open(i, "r")) for i in filenames]
    for rows in zip(*files):
        # rows is now a tuple containing one row from each file
        layer = rf.NetworkSet(files)
        layer.plot_s_db()
        plt.savefig("C:\\Users\\Jacob\\Documents\\Python Scripts\\LAN_Transfer\\190620\\190620_1_13L_UP.jpg")
'''