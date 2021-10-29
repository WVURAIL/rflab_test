import numpy as np
import matplotlib.pyplot as plt
import antpy

#ALWAYS SAVE THE VNA DATA FROM 2 MHZ TO 6 GHZ WITH 1000 DATA POINT RESOLUTION SO THAT THE INDEXES FOR 400-800 MHZ ARE ALWAYS THE SAME
def read_logmag_data_from_mult_files(meas_logmag_filenames):
    x = 0
    logmag_data = []
    logmag_data_name_array = []
    file_len = []
    tot_file_len = []
    while x < len(meas_logmag_filenames) :
        with open(meas_logmag_filenames[x]) as f:
            y = 0
            logmag_data_name = str(meas_logmag_filenames[x])
            logmag_data_name = logmag_data_name[:-4] + '_logmag'
            logmag_data_name_array.append(str(logmag_data_name))
            for row in f:
                logmag_data.append(row.split())
                y += 1
            file_len.append(int(y))
            x += 1
    tot_file_len = sum(file_len)
    m = 0
    freq = []
    S11 = []
    S21 = []
    S12 = []
    S22 = []
    while m < tot_file_len :
        freq.append(float(logmag_data[m][0]))
        S11.append(float(logmag_data[m][1]))
        S21.append(float(logmag_data[m][3]))
        S12.append(float(logmag_data[m][5]))
        S22.append(float(logmag_data[m][7]))
        m += 1
    return(freq, S11, S21, S12, S22, logmag_data_name_array, file_len, tot_file_len)
def plot_S11_logmag(meas_logmag_filenames, plt_title, plt_label) :
    freq, S11, S21, S12, S22, logmag_data_name_array, file_len, tot_file_len = read_logmag_data_from_mult_files(meas_logmag_filenames)
    z = 0
    freq_nparray = np.array(freq)
    while z < len(file_len) :
        if z == 0:
            plt.plot(freq_nparray[0:file_len[z]]/1e9, S11[0:file_len[z]], label = plt_label[z])
            z += 1
        else :
            plt.plot(freq_nparray[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])]/1e9, S11[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])], label = plt_label[z])
            z += 1
    plt.legend(loc = 'best')
    plt.title('S11 ' + str(plt_title[0]), fontsize = 16)
    plt.xlabel('Frequency (GHz)', fontsize = 16)
    plt.ylabel('S11 (dB)', fontsize = 16)
    plt.grid()
#plt.xlim([0,1])
#plt.ylim([0,1])
    plt.savefig('S11_(2MHz-6GHz)_logmag.pdf')
    plt.clf()
def plot_S21_logmag(meas_logmag_filenames, plt_title, plt_label) :
    freq, S11, S21, S12, S22, logmag_data_name_array, file_len, tot_file_len = read_logmag_data_from_mult_files(meas_logmag_filenames)
    z = 0
    freq_nparray = np.array(freq)
    while z < len(file_len) :
        if z == 0:
            plt.plot(freq_nparray[0:file_len[z]]/1e9, S21[0:file_len[z]], label = plt_label[z])
            z += 1
        else :
            plt.plot(freq_nparray[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])]/1e9, S21[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])], label = plt_label[z])
            z += 1
    plt.legend(loc = 'best')
    plt.title('S21 ' + str(plt_title[0]), fontsize = 16)
    plt.xlabel('Frequency (GHz)', fontsize = 16)
    plt.ylabel('S21 (dB)', fontsize = 16)
    plt.grid()
#plt.xlim([0,1])
#plt.ylim([10,35])
    plt.savefig('S21_(2MHz-6GHz)_logmag.pdf')
    plt.clf()
def plot_S12_logmag(meas_logmag_filenames, plt_title, plt_label) :
    freq, S11, S21, S12, S22, logmag_data_name_array, file_len, tot_file_len = read_logmag_data_from_mult_files(meas_logmag_filenames)
    z = 0
    freq_nparray = np.array(freq)
    while z < len(file_len) :
        if z == 0:
            plt.plot(freq_nparray[0:file_len[z]]/1e9, S12[0:file_len[z]], label = plt_label[z])
            z += 1
        else :
            plt.plot(freq_nparray[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])]/1e9, S12[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])], label = plt_label[z])
            z += 1
    plt.legend(loc = 'best')
    plt.title('S12 ' + str(plt_title[0]), fontsize = 16)
    plt.xlabel('Frequency (GHz)', fontsize = 16)
    plt.ylabel('S12 (dB)', fontsize = 16)
    plt.grid()
#plt.xlim([0,1])
#plt.ylim([0,1])
    plt.savefig('S12_(2MHz-6GHz)_logmag.pdf')
    plt.clf()
def plot_S22_logmag(meas_logmag_filenames, plt_title, plt_label) :
    freq, S11, S21, S12, S22, logmag_data_name_array, file_len, tot_file_len = read_logmag_data_from_mult_files(meas_logmag_filenames)
    z = 0
    freq_nparray = np.array(freq)
    while z < len(file_len) :
        if z == 0:
            plt.plot(freq_nparray[0:file_len[z]]/1e9, S22[0:file_len[z]], label = plt_label[z])
            z += 1
        else :
            plt.plot(freq_nparray[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])]/1e9, S22[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])], label = plt_label[z])
            z += 1
    plt.legend(loc = 'best')
    plt.title('S22 ' + str(plt_title[0]), fontsize = 16)
    plt.xlabel('Frequency (GHz)', fontsize = 16)
    plt.ylabel('S22 (dB)', fontsize = 16)
    plt.grid()
#plt.xlim([0,1])
#plt.ylim([0,1])
    plt.savefig('S22_(2MHz-6GHz)_logmag.pdf')
    plt.clf()
def plot_S_params_logmag(meas_logmag_filenames, plt_title, plt_label) :
    plt_s11 = plot_S11_logmag(meas_logmag_filenames, plt_title, plt_label)
    plt_s21 = plot_S21_logmag(meas_logmag_filenames, plt_title, plt_label)
    plt_s12 = plot_S12_logmag(meas_logmag_filenames, plt_title, plt_label)
    plt_s22 = plot_S22_logmag(meas_logmag_filenames, plt_title, plt_label)
#SMITH DATA
def read_smith_data_from_files(smith_filenames):
    x = 0
    smith_data = []
    smith_data_name_array = []
    file_len = []
    tot_file_len = []
    while x < len(smith_filenames) :
        with open(smith_filenames[x]) as f:
            y = 0
            smith_data_name = str(smith_filenames)
            smith_data_name = smith_data_name[:-4] + '_smith'
            smith_data_name_array.append(str(smith_data_name))
            for row in f:
                smith_data.append(row.split())
                y += 1
            file_len.append(int(y))
            x += 1
    tot_file_len = sum(file_len)
    m = 0
    freq = []
    S11 = []
    S21 = []
    S12 = []
    S22 = []
    while m < tot_file_len :
        freq.append(float(smith_data[m][0]))
        S11.append(complex(float(smith_data[m][1]), float(smith_data[m][2])))
        S21.append(complex(float(smith_data[m][3]), float(smith_data[m][4])))
        S12.append(complex(float(smith_data[m][5]), float(smith_data[m][6])))
        S22.append(complex(float(smith_data[m][7]), float(smith_data[m][8])))
        m += 1
    S11_nparray = np.array(S11)
    S21_nparray = np.array(S21)
    S12_nparray = np.array(S12)
    S22_nparray = np.array(S22)
    return (freq, S11_nparray, S21_nparray, S12_nparray, S22_nparray, file_len)
def plot_S11_smith_mult_files(smith_filenames, plt_title, plt_label) :
    freq, S11_nparray, S21_nparray, S12_nparray, S22_nparray, file_len = read_smith_data_from_files(smith_filenames)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    antpy.smith(ax = ax1)
    z = 0
    while z < len(file_len) :
        if z == 0:
            ax1.plot(S11_nparray.real[0:file_len[z]], S11_nparray.imag[0:file_len[z]], label = plt_label[z])
            z += 1
        else :
            ax1.plot(S11_nparray.real[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])], S11_nparray.imag[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])], label = plt_label[z])
            z += 1
    plt.legend(loc = 'best')
    fig.suptitle('S11 ' + str(plt_title[0]), fontsize = 16, y = 0.94)
    plt.xlabel('Real', fontsize = 16)
    plt.ylabel('Imaginary', fontsize = 16)
    #plt.grid()
    plt.gcf().subplots_adjust(bottom=0.19, top=0.87) #adjusts plotting area so title isn't cut off
    plt.savefig('S11_(2MHz-6GHz)_smith.pdf', dpi = 300)
    plt.clf()
#plt.show()
#NOISE FIGURE DATA
def read_nf_data_from_mult_files(meas_nf_filenames) :
    x = 0
    nf_data = []
    nf_data_name_array = []
    file_len = []
    tot_file_len = []
    while x < len(meas_nf_filenames) :
        with open(meas_nf_filenames[x]) as f:
            y = 0
            nf_data_name = str(meas_nf_filenames[x])
            nf_data_name = nf_data_name[:-4] + '_nf'
            nf_data_name_array.append(str(nf_data_name))
            for row in f:
                nf_data.append(row.split(','))
                y += 1
            file_len.append(int(y))
            x += 1
    tot_file_len = sum(file_len)
    m = 0
    freq_nf = []
    gain = []
    nf = []
    while m < tot_file_len :
        freq_nf.append(float(nf_data[m][0]))
        gain.append(float(nf_data[m][1]))
        nf.append(float(nf_data[m][2]))
        m += 1
    freq_nf_nparray = np.array(freq_nf)
    gain_nparray = np.array(gain)
    nf_nparray = np.array(nf)
    return(freq_nf_nparray, gain_nparray, nf_nparray, file_len)
def plot_nf_no_sim(meas_nf_filenames, plt_title, plt_label) :
    nf_freq, gain, nf, file_len = read_nf_data_from_mult_files(meas_nf_filenames)
    z = 0
    while z < len(file_len) :
        if z == 0:
            plt.plot(nf_freq[0:file_len[z]]/1e9, nf[0:file_len[z]], label = plt_label[z])
            z += 1
        else :
            plt.plot(nf_freq[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])]/1e9, nf[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])], label = plt_label[z])
            z += 1
    plt.legend(loc = 'best')
    plt.title('Noise Figure ' + str(plt_title[0]), fontsize = 16)
    plt.xlabel('Frequency (GHz)', fontsize = 16)
    plt.ylabel('Noise Figure (dB)', fontsize = 16)
    plt.grid()
    #plt.xlim([0,1])
    plt.ylim([0,2])
    plt.savefig('Noise_Figure_' + str(plt_title[0]) + '_(10MHz-1500MHz).pdf')
    plt.clf()
def read_nf_data_from_mult_ADS_files(sim_nf_filenames):
    x = 0
    nf_data = []
    sim_nf_data_name_array = []
    file_len = []
    tot_file_len = []
    while x < len(sim_nf_filenames) :
        with open(sim_nf_filenames[x]) as f:
            y = 0
            sim_nf_data_name = str(sim_nf_filenames[x])
            sim_nf_data_name = sim_nf_data_name[:-4] + '_nf'
            sim_nf_data_name_array.append(str(sim_nf_data_name))
            for row in f:
                nf_data.append(row.split())
                y += 1
            file_len.append(int(y))
            x += 1
    tot_file_len = sum(file_len)
    m = 0
    freq = []
    nf = []
    gamma = []
    phase_angle = []
    noise_resistance = []
    while m < tot_file_len :
        freq.append(float(nf_data[m][0]))
        nf.append(float(nf_data[m][1]))
        gamma.append(float(nf_data[m][2]))
        phase_angle.append(float(nf_data[m][3]))
        noise_resistance.append(float(nf_data[m][4]))
        m += 1
    freq_nparray = np.array(freq)
    gamma_nparray = np.array(gamma)
    nf_nparray = np.array(nf)
    phase_angle_nparray = np.array(phase_angle)
    noise_resistance_nparray = np.array(noise_resistance)
    return (freq_nparray, nf_nparray, gamma_nparray, phase_angle_nparray, noise_resistance_nparray, file_len)
def plot_nf_meas_and_sim(meas_nf_filenames, sim_nf_filenames, plt_title, plt_label, sim_label) :
    nf_freq, gain, nf, file_len = read_nf_data_from_mult_files(meas_nf_filenames)
    freq_nparray, nf_nparray, gamma_nparray, phase_angle_nparray, noise_resistance_nparray, sim_file_len = read_nf_data_from_mult_ADS_files(sim_nf_filenames)
    z = 0
    while z < len(file_len) : #plot the measured nf data
        if z == 0:
            plt.plot(nf_freq[0:file_len[z]]/1e9, nf[0:file_len[z]], label = plt_label[z]) #plots the measured nf data from the first file
            z += 1
        else :
            plt.plot(nf_freq[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])]/1e9, nf[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])], label = plt_label[z]) #plots the measured nf data from the rest of the files
            z += 1
    z = 0
    while z < len(file_len) : #plot the simulated nf data
        if z == 0:
            plt.plot(freq_nparray[0:sim_file_len[z]]/1e9, nf_nparray[0:sim_file_len[z]], label = sim_label[z]) #plots the simulated nf data from the first file
            z += 1
        else :
            plt.plot(freq_nparray[sum(sim_file_len[0:z]):(sum(sim_file_len[0:z]) + sim_file_len[z])]/1e9, nf_nparray[sum(sim_file_len[0:z]):(sum(sim_file_len[0:z]) + sim_file_len[z])], label = sim_label[z]) #plots the simulated nf data from the rest of the files
            z += 1
    plt.legend(loc = 'best')
    plt.title('Noise Figure ' + str(plt_title[0]), fontsize = 16)
    plt.xlabel('Frequency (GHz)', fontsize = 16)
    plt.ylabel('Noise Figure (dB)', fontsize = 16)
    plt.grid()
    plt.xlim([0,1])
    plt.ylim([0,2])
    plt.savefig('Noise_Figure_meas&sim' + str(plt_title[0]) + '_(10MHz-1500MHz).pdf')
    plt.clf()
#-----------------------------------------------------------------------------------------------------------------
sparam_filenames = ['B3S2_CUT_changed_input_induc&cap_150nH_100pF_L.txt', 'B3S2_CUT_L.txt']
smith_filenames = ['B3S2_CUT_changed_input_induc&cap_150nH_100pF_S.txt', 'B3S2_CUT_S.txt']
sim_nf_filenames = ['hirax_balun_v4_cutboard_L3(150nH)_C4(100pF)_50Ohmterm1_final_Real_Imag_nf.txt', 'demo_board_ver4_final_470nH_rev1_50Ohmterm1_plusBiasT_combined_s2p_final_Real_Imag_nf.txt']
meas_nf_filenames = ['board3_side2_original_design_nf_cutboard_with_foam_060816.txt', 'board3_side2_original_design_nf_cutboard_with_foam_attempt2_060816.txt']
title = ['B3S2']
label = ['B3S2 rev0', 'B3S2 rev1']
sim_label = ['1', '2']
#freq, S11, S21, S12, S22 = read_smith_data_from_files(smith_filenames)
#print len(freq)
plot_S11_smith_mult_files(smith_filenames, label, title)
#plot_nf_meas_and_sim(meas_nf_filenames, sim_nf_filenames, title, label, sim_label)