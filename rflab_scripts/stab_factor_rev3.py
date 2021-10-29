import numpy as np
import math
import pylab
import matplotlib.pyplot as plt
import antpy

board1 = []
with open('AMP1L.txt') as f:
    for row in f:
        board1.append(row.split())

board2 = [] #LOGMAG DATA IS IN DB/ANGLE SO NO NEED TO CONVERT ANYTHING!
with open('A2BL.txt') as f:
    for row in f:
        board2.append(row.split())


S11_board1_side1_dB_list = []
S21_board1_side1_dB_list = []
S12_board1_side1_dB_list = []
S22_board1_side1_dB_list = []


S11_board2_side1_box_dB_list = []
S21_board2_side1_box_dB_list = []
S12_board2_side1_box_dB_list = []
S22_board2_side1_box_dB_list = []


S_freq_meas = []
x = 0
while x < len(board2):
    S_freq_meas.append(float(board2[x][0]))
    S11_board1_side1_dB_list.append(float(board1[x][1]))
    S21_board1_side1_dB_list.append(float(board1[x][3]))
    S12_board1_side1_dB_list.append(float(board1[x][5]))
    S22_board1_side1_dB_list.append(float(board1[x][7]))
    S11_board2_side1_box_dB_list.append(float(board2[x][1]))
    S21_board2_side1_box_dB_list.append(float(board2[x][3]))
    S12_board2_side1_box_dB_list.append(float(board2[x][5]))
    S22_board2_side1_box_dB_list.append(float(board2[x][7]))
    x+=1


#MAKE NUMPY ARRAYS
S_freq_meas_nparray = np.array(S_freq_meas)
S11_board1_side1_dB_list_nparray = np.array(S11_board1_side1_dB_list)
S21_board1_side1_dB_list_nparray = np.array(S21_board1_side1_dB_list)
S12_board1_side1_dB_list_nparray = np.array(S12_board1_side1_dB_list)
S22_board1_side1_dB_list_nparray = np.array(S22_board1_side1_dB_list)

S11_board2_side1_box_dB_list_nparray = np.array(S11_board2_side1_box_dB_list)
S21_board2_side1_box_dB_list_nparray = np.array(S21_board2_side1_box_dB_list)
S12_board2_side1_box_dB_list_nparray = np.array(S12_board2_side1_box_dB_list)
S22_board2_side1_box_dB_list_nparray = np.array(S22_board2_side1_box_dB_list)



#SOLVE FOR THE MAGNITUDE
mag_S11_board1_side1_dB_list_nparray = np.zeros(len(S11_board1_side1_dB_list_nparray))
mag_S21_board1_side1_dB_list_nparray = np.zeros(len(S21_board1_side1_dB_list_nparray))
mag_S12_board1_side1_dB_list_nparray = np.zeros(len(S12_board1_side1_dB_list_nparray))
mag_S22_board1_side1_dB_list_nparray = np.zeros(len(S22_board1_side1_dB_list_nparray))

mag_S11_board2_side1_box_dB_list_nparray = np.zeros(len(S11_board2_side1_box_dB_list_nparray))
mag_S21_board2_side1_box_dB_list_nparray = np.zeros(len(S21_board2_side1_box_dB_list_nparray))
mag_S12_board2_side1_box_dB_list_nparray = np.zeros(len(S12_board2_side1_box_dB_list_nparray))
mag_S22_board2_side1_box_dB_list_nparray = np.zeros(len(S22_board2_side1_box_dB_list_nparray))

mag_S11_board1_side1_dB_list_nparray = 10**(S11_board1_side1_dB_list_nparray/20)
mag_S21_board1_side1_dB_list_nparray = 10**(S21_board1_side1_dB_list_nparray/20)
mag_S12_board1_side1_dB_list_nparray = 10**(S12_board1_side1_dB_list_nparray/20)
mag_S22_board1_side1_dB_list_nparray = 10**(S22_board1_side1_dB_list_nparray/20)

mag_S11_board2_side1_box_dB_list_nparray = 10**(S11_board2_side1_box_dB_list_nparray/20)
mag_S21_board2_side1_box_dB_list_nparray = 10**(S21_board2_side1_box_dB_list_nparray/20)
mag_S12_board2_side1_box_dB_list_nparray = 10**(S12_board2_side1_box_dB_list_nparray/20)
mag_S22_board2_side1_box_dB_list_nparray = 10**(S22_board2_side1_box_dB_list_nparray/20)


mag_S11_board1_side1_dB_list_nparray_avg = np.zeros(len(board2)/20)
x = 0
i = 0
while i < (len(board2)/20):
    mag_S11_board1_side1_dB_list_nparray_avg[i] = np.mean(mag_S11_board1_side1_dB_list_nparray[x:x+19]) #this works but I think I need to average them before I solve for the magnitude 4/15/16
    x += 20
    i += 1

#SOLVE FOR THE STABILITY FACTOR - K
board1_side1_stab_factor = antpy.CalcStabFactor(mag_S11_board1_side1_dB_list_nparray,mag_S21_board1_side1_dB_list_nparray,mag_S12_board1_side1_dB_list_nparray,mag_S22_board1_side1_dB_list_nparray)


board2_side1_stab_factor = antpy.CalcStabFactor(mag_S11_board2_side1_box_dB_list_nparray,mag_S21_board2_side1_box_dB_list_nparray,mag_S12_board2_side1_box_dB_list_nparray,mag_S22_board2_side1_box_dB_list_nparray)

#PLOT THE STABILITY FACTOR - K
plt.plot(S_freq_meas_nparray/1e9,board1_side1_stab_factor, label = 'board1')

plt.plot(S_freq_meas_nparray/1e9,board2_side1_stab_factor, label = 'board2')

plt.title('Stability Factor for Boards 1 and 2')
plt.xlabel('Frequency (GHz)')
plt.ylabel('Stability Factor')
plt.legend(loc = 'best')
plt.ylim((-5,3))
plt.savefig('stab_factor_rev3.pdf', dpi = 300)
plt.show()