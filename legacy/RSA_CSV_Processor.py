import csv
import os
import numpy as np
import matplotlib.pyplot as plt

dir=os.getcwd()
#Set base to the directory from which one will be working
base = "C:\\Users\\Jacob\\Documents\\SignalVu\\"
if dir==base:
    pass
else:
    os.path.join(dir, base)
    
'''
File Selection Module:
In this module, the filenames to be compared will be entered by the user, then the full file-
paths will be generated as "filepath" and "filepath1".
'''
infile=input("\nPlease enter filename of source "ON" to initiate the process:\n")
#infile="GBO_Feed9_LNAB_HOT.csv"
filepath=base+infile


infile=input("\nPlease enter filename of source "OFF" to compare data:\n")
#infile1="GBO_Feed9_LNAB_COLD.csv"
filepath1=base+infile1

'''
The below definition opens the filepaths, runs multiple counters based on line placement, 
skips unwanted data, then returns the usable portions.
'''
def read_spectrum_csv(filename='filename.csv'):
  with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    data_count = 0
    skip_count = 0
    nskip = 3
    found_traces = False
    found_trace1 = False
    ndata = 801 #find this in file!
    #Creates a 
    power_data = np.zeros(ndata)
    freq_data = np.zeros(ndata)
    for row in csv_reader:
        if found_traces == False:
            #print(f'Processed {line_count} lines.')
            try:
                if row[0] == "[Traces]":
                    print(f'found traces: {", ".join(row)}')
                    line_count += 1
                    found_traces = True
                else:
                    line_count += 1
            except:
                line_count += 1
        else:
            if found_trace1 == False:
                if row[0] == "Trace 1":
                    found_trace1 = True
                    line_count += 1
                    print(f'found trace 1: {", ".join(row)}')
            else:
                if skip_count < nskip:
                    if skip_count == 0:
                        ndata = int(row[1])
                        power_data = np.zeros(ndata)
                        freq_data = np.zeros(ndata)
                    skip_count += 1
                    line_count += 1
                    print(f'skipping data is: {", ".join(row)}')
                else:
                    if data_count < ndata:
                        #print(f'data is: {", ".join(row)}')
                        power_data[data_count] = row[0]
                        freq_data[data_count] = row[1]
                        line_count += 1
                        data_count += 1
                    else:
                        break
                    
    print(f'Processed {line_count} lines.')
    #print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
  return freq_data, power_data
                          

#This module references both inputs of the def read_spectrum_csv and then evaluates the desired filepath.
freq_data_on, power_data_on = read_spectrum_csv(filepath)
freq_data_off, power_data_off = read_spectrum_csv(filepath1)


temp_data_on=295.9 #This is the kelvin representation of the local temperature
temp_data_off=50.0 #This value should be considered constant                       

'''
Calculations
'''
#enr is the Excessive Noise Ratio in dB (due to log10)
enr=10*np.log10((temp_data_on - temp_data_off)/temp_data_off)
print('ENR Value: %s\n' %enr)
#enr = 5.26 #use full table, just linear should be fine
#Y-factor method used to calculate the ratio of measured (linear) noise power at the DUT
Y = power_data_on - power_data_off #dB
#Noise Factor w/o units
nf = 10.0*np.log10(10**(enr/10.0)/(10**(Y/10.0)-1))
#difference between "Hot" and "Cold"
pwr_dif=np.abs(power_data_on-power_data_off) #is this cheating?
#temperature of "Device Under Test"
temp_DUT=temp_data_off*(10**(nf/10) - 1)
#print(temp_DUT)
                          
'''
Graphs for comparison
'''
#Plot freq and power for both "Hot" (ON) and "Cold" (OFF) and compare them on a figure
plt.plot(freq_data_on,power_data_on)
plt.plot(freq_data_off,power_data_off)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power (dB)')
plt.title('ON vs OFF')
plt.figure()
plt.clf()

#Plot freq_data_on vs power_data_on
plt.plot(freq_data_on, power_data_on)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power (dB)')
plt.title('ON: Freq vs Power')
plt.figure()
plt.clf()
  
#Plot freq_data_off vs power_data_off
plt.plot(freq_data_off, power_data_off)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power (dB)')
plt.title('OFF: Freq vs Power')
plt.figure()
plt.clf()
   
#Plot freq_data_on vs the power difference (power_data_on - power_data_off)
plt.plot(freq_data_on, pwr_dif)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power (dB)')
plt.title('Freq vs Power Difference')
plt.ylim(0,12)
plt.figure()
plt.clf()

#Plot of freq_data_on vs the noise figure
plt.plot(freq_data_on, nf)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Noise (dB)')
plt.title('Freq vs Noise Figure')
#plt.ylim(0,12)
plt.figure()
plt.clf()

#Plot of something...to be continued 
plt.plot(freq_data_on, (temp_data_off*(10**(nf/10) - 1) - temp_data_off)/2)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Temp of DUT (K)')
plt.title('Freq vs Temperature')
plt.ylim(0,1000)
plt.figure()
plt.clf()