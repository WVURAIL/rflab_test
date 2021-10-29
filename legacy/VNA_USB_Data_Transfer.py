# -*- coding: utf-8 -*-
"""
Created on Mon May 20 16:48:55 2019

@author: Jacob
"""

#Importing data from Touchstone (SnP) file
import skrf as rf
import os
import sys 
import matplotlib.pyplot as plt

#Must import data from flash drive E
script_dir = os.path.dirname('E:\\') #<-- absolute dir the script is in
x = os.listdir(script_dir)

rel_path = "5_23_HIGH_0207191.s2p"
abs_file_path = os.path.join(script_dir, (rel_path), ('5_23_LOW_0207191.s2p'))
print(abs_file_path)
#sys.path.insert(0, 'E:\\')

#def chunks(l, n):
#    n = 100
#    #"""Yield successive n-sized chunks from l."""
#    for i in range(0, len(l), n):
#        yield l[i:i + n]
#        
#import pprint
#pprint.pprint(list(chunks(range(10, 75), 10)))

#Network strips, formats data per skrf design
rs = rf.Network('E:\\5_23_HIGH_0207191.s2p')
rs_1 = rf.Network('E:\\5_23_LOW_0207191.s2p')
#change db to deg to auto convert graphs to degrees from dB


#Plot S11, S12, S22, S21
#rs.plot_s_db()
#
#Plot a specific S parameter by adjusting m and n
#rs.plot_s_db(m=int(input("\nSelect Output Path Value\n"))
#            ,n=int(input("\nSelect Input Path Value\n")))

rs.plot_s_db(1,1)
rs.plot_s_db(0,1)
#rs_1.plot_s_db(0,0)
#rs_1.plot_s_db(1,0)

#plt.title('S', +'m', +'n')
#(m=0,n=1)=S12 (Smn) due to Python starting at 0

#smith chart with lw being line width and m/n being specific parameter to map
#rs.plot_s_smith(lw=1)
#plt.title('Cluttered Smith Chart')

#We will come back to this mess
#fig = plt.figure()
#a = fig.add_subplot(1, 2, 1)
#b = fig.add_subplot(1, 2, 2)
#c = fig.add_subplot (1, 2, 3)
#a.plot(plot1)
#b.plot(plot2)
#c.plot(plot3)
#plt.show()

#Shows available options and specification for flash drives files containing "example"
#opt_specs= rf.read_all('E:\\', contains='000')
#print(opt_specs)

