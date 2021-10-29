import numpy as np
import matplotlib.pyplot as plt
import glob
import skrf.plotting as skplt
import skrf as rf
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-label', '--plt_label', nargs = '+', action = 'store', type = str, default = None, help = 'Labels for the plot legend. List them without quotes or parentheses and do not separate them with commas. The files are read in alphabetically, so put these in the same order the files will be read, e.g. -label label1 label2 label3. If you set this to auto (e.g. -label auto) than the plots will be labeled with the filenames')
parser.add_argument('-dir', '--set_directory', action = 'store', type = str , default = '~/Desktop', help = 'The directory that the files are located. This is also the directory the files will be saved.')
parser.add_argument('-s11_xlim', '--set_s11_xlim', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum x values that are plotted for S11. List them without quotes or parentheses and do not separate them with commas, e.g. -s11_xlim 0 2')
parser.add_argument('-s11_ylim', '--set_s11_ylim', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum y values that are plotted for S11. List them without quotes or parentheses and do not separate them with commas, e.g. -s11_ylim 0 2')
parser.add_argument('-s12_xlim', '--set_s12_xlim', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum x values that are plotted for S12. List them without quotes or parentheses and do not separate them with commas, e.g. -s12_xlim 0 2')
parser.add_argument('-s12_ylim', '--set_s12_ylim', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum y values that are plotted for S12. List them without quotes or parentheses and do not separate them with commas, e.g. -s12_ylim 0 2')
parser.add_argument('-s21_xlim', '--set_s21_xlim', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum x values that are plotted for S21. List them without quotes or parentheses and do not separate them with commas, e.g. -s21_xlim 0 2')
parser.add_argument('-s21_ylim', '--set_s21_ylim', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum y values that are plotted for S21. List them without quotes or parentheses and do not separate them with commas, e.g. -s21_ylim 0 2')
parser.add_argument('-s22_xlim', '--set_s22_xlim', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum x values that are plotted for S22. List them without quotes or parentheses and do not separate them with commas, e.g. -s22_xlim 0 2')
parser.add_argument('-s22_ylim', '--set_s22_ylim', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum y values that are plotted for S22. List them without quotes or parentheses and do not separate them with commas, e.g. -s22_ylim 0 2')
parser.add_argument('-s11_ylim_400to800', '--set_s11_ylim_400to800', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum y values that are plotted for S11. List them without quotes or parentheses and do not separate them with commas, e.g. -s11_ylim_400to800 0 2')
parser.add_argument('-s12_ylim_400to800', '--set_s12_ylim_400to800', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum y values that are plotted for S11. List them without quotes or parentheses and do not separate them with commas, e.g. -s12_ylim_400to800 0 2')
parser.add_argument('-s21_ylim_400to800', '--set_s21_ylim_400to800', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum y values that are plotted for S11. List them without quotes or parentheses and do not separate them with commas, e.g. -s21_ylim_400to800 0 2')
parser.add_argument('-s22_ylim_400to800', '--set_s22_ylim_400to800', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum y values that are plotted for S11. List them without quotes or parentheses and do not separate them with commas, e.g. -s22_ylim_400to800 0 2')
parser.add_argument('-s11_ylim_0to1', '--set_s11_ylim_0to1', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum y values that are plotted for S11. List them without quotes or parentheses and do not separate them with commas, e.g. -s11_ylim_0to1 0 2')
parser.add_argument('-s12_ylim_0to1', '--set_s12_ylim_0to1', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum y values that are plotted for S11. List them without quotes or parentheses and do not separate them with commas, e.g. -s12_ylim_0to1 0 2')
parser.add_argument('-s21_ylim_0to1', '--set_s21_ylim_0to1', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum y values that are plotted for S11. List them without quotes or parentheses and do not separate them with commas, e.g. -s21_ylim_0to1 0 2')
parser.add_argument('-s22_ylim_0to1', '--set_s22_ylim_0to1', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum y values that are plotted for S11. List them without quotes or parentheses and do not separate them with commas, e.g. -s22_ylim_0to1 0 2')
parser.add_argument('-cal', '--set_cal_component', action = 'store', type = str, default = None, choices = ('ZX60-P103LN+', 'ZX60-P33ULN+', 'ZX60-3018G-S+'), help = 'Choose the minicircuit component that you used as a calibrator - only set this if you would like to plot the simulated data')
args = parser.parse_args()

plt_label = args.plt_label
s11_xlim = args.set_s11_xlim
s11_ylim = args.set_s11_ylim
s12_xlim = args.set_s12_xlim
s12_ylim = args.set_s12_ylim
s21_xlim = args.set_s21_xlim
s21_ylim = args.set_s21_ylim
s22_xlim = args.set_s22_xlim
s22_ylim = args.set_s22_ylim
s11_ylim_400to800 = args.set_s11_ylim_400to800
s12_ylim_400to800 = args.set_s12_ylim_400to800
s21_ylim_400to800 = args.set_s21_ylim_400to800
s22_ylim_400to800 = args.set_s22_ylim_400to800
s11_ylim_0to1 = args.set_s11_ylim_0to1
s12_ylim_0to1 = args.set_s12_ylim_0to1
s21_ylim_0to1 = args.set_s21_ylim_0to1
s22_ylim_0to1 = args.set_s22_ylim_0to1

dir = args.set_directory #the directory where all of your files are located and where the pdf's and jpeg's are saved
dir_length = len(dir)

txt_sim_filenames = glob.glob(dir + '/*gain*.txt')#make a list of the simulated s-parameter text files
sim_filenames = glob.glob(dir + '/*sim.s2p')#make a list of the simulated s-parameter files
meas_filenames = glob.glob(dir + '/*.s2p')#make a list of the measured s-parameter files
dBm40_filenames = glob.glob(dir + '/*-40dBm*.s2p')#make a list of the measured s-parameter files when the power was set to -40dBm

if args.set_cal_component is not None :
    minicircuit_component = args.set_cal_component
    if minicircuit_component == 'ZX60-P103LN+':
        cal_nf_filenames = glob.glob('/Users/brittanyjohnstone/Dropbox/Kevin_Research/brjohnstone/WVU/minicircuit_components/ZX60-P103LN+/ZX60-P103LN+_S2P/ZX60-P103LN+_5V_Plus25DegC_Unit1.s2p')
    else :
        cal_nf_filenames = glob.glob('/Users/brittanyjohnstone/Desktop/Research/Kevin/WVU/minicircuit_components/' + minicircuit_component + '/*nf_sim.txt')
else:
    cal_nf_filenames = None
    minicircuit_component = None

#ALWAYS SAVE THE VNA DATA FROM 2 MHZ TO 6 GHZ WITH 1600 DATA POINT RESOLUTION SO THAT THE INDEXES FOR 400-800 MHZ ARE ALWAYS THE SAME
#READ LOGMAG DATA

def read_sparam_data(filename, s):
    ant = rf.Network(filename)
    sparam = np.zeros(len(ant))
    freq = ant.f/1e9
    for y in range(len(ant)):
        if s == 's11':
            sparam[y] = ant.s_db[y][0][0]
        if s == 's12':
            sparam[y] = ant.s_db[y][0][1]
        if s == 's21':
            sparam[y] = ant.s_db[y][1][0]
        if s == 's22':
            sparam[y] = ant.s_db[y][1][1]
    return(sparam, freq)

def read_sparam_data_txt(filename):
    data = []
    with open(filename) as f:
        for row in f:
            data.append(row.strip().split())
    freq = np.zeros(len(data)-1)
    gain = np.zeros(len(data)-1)
    i = 0
    while i < (len(data)-1):
        freq[i] = float(data[i+1][0])/1e9
        gain[i] = float(data[i+1][1])
        i += 1
    return(freq, gain)

def gen_logmag_plot(freq, sparam, y_label, title, label):
    skplt.plot_rectangular(freq, sparam, x_label = 'Frequency (GHz)', y_label = y_label, title = title, label = label)

def plot_gain_sim_txt(filename, xlim, ylim):
    freq, gain = read_sparam_data_txt(filename)
    skplt.plot_rectangular(freq, gain, x_label = 'Frequency (GHz)', y_label = 'Simulated S21 (dB)', title = 'Simulated Gain from ADS')

    ax = plt.gca()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()

def plot_s21_diff(dBm40filenames, xlim, ylim, title):
    s21_40_side1, freq_side1_40 = read_sparam_data(dBm40filenames[0], 's21')
    s21_40_side2, freq_side2_40 = read_sparam_data(dBm40filenames[1], 's21')
    s21_diff = s21_40_side1 - s21_40_side2
    
    if plt_label == None :
        label = None
    elif plt_label[0] == 'auto' :
        label = dBm40filenames[0][dir_length:-4]
    else :
        label = plt_label[x]
    gen_logmag_plot(freq_side1_40, s21_diff, 'S21 Difference (dB)', 'S21 Difference' + title, label = label)

    ax = plt.gca()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()


def plot_logmag_data(meas_filenames, s11_xlim, s11_ylim, s12_xlim, s12_ylim, s21_xlim, s21_ylim, s22_xlim, s22_ylim):
    if cal_nf_filenames != None :
        s11_cal, freq_cal = read_sparam_data(cal_nf_filenames[0], 's11')
        s12_cal, freq_cal = read_sparam_data(cal_nf_filenames[0], 's12')
        s21_cal, freq_cal = read_sparam_data(cal_nf_filenames[0], 's21')
        s22_cal, freq_cal = read_sparam_data(cal_nf_filenames[0], 's22')
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        s11, freq = read_sparam_data(meas_filenames[x], 's11')
        gen_logmag_plot(freq, s11, 'S11 (dB)', 'S11', label = label) #plot s11
        if cal_nf_filenames != None and x == 1 :
            gen_logmag_plot(freq_cal, s11_cal, 'S11 (dB)', 'S11', label = str(minicircuit_component))
        x += 1
    ax = plt.gca()
    ax.set_xlim(s11_xlim)
    ax.set_ylim(s11_ylim)

    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()

    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        s12, freq = read_sparam_data(meas_filenames[x], 's12')
        gen_logmag_plot(freq, s12, 'S12 (dB)', 'S12', label = label) #plot s12
        if cal_nf_filenames != None and x == 1 :
            gen_logmag_plot(freq_cal, s12_cal, 'S12 (dB)', 'S12', label = str(minicircuit_component))
        x += 1
    ax = plt.gca()
    ax.set_xlim(s12_xlim)
    ax.set_ylim(s12_ylim)
    
    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()

    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        s21, freq = read_sparam_data(meas_filenames[x], 's21')
        gen_logmag_plot(freq, s21, 'S21 (dB)', 'S21', label = label) #plot s21
        if cal_nf_filenames != None and x == 1 :
            gen_logmag_plot(freq_cal, s21_cal, 'S21 (dB)', 'S21', label = str(minicircuit_component))
        x += 1
    ax = plt.gca()
    ax.set_xlim(s21_xlim)
    ax.set_ylim(s21_ylim)

    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()

    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        s22, freq = read_sparam_data(meas_filenames[x], 's22')
        gen_logmag_plot(freq, s22, 'S22 (dB)', 'S22', label = label) #plot s22
        if cal_nf_filenames != None and x == 1 :
            gen_logmag_plot(freq_cal, s22_cal, 'S22 (dB)', 'S22', label = str(minicircuit_component))
        x += 1
    ax = plt.gca()
    ax.set_xlim(s22_xlim)
    ax.set_ylim(s22_ylim)

    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()


#def plot_logmag_data_freq_range(meas_filenames, s11_xlim, s11_ylim, s12_xlim, s12_ylim, s21_xlim, s21_ylim, s22_xlim, s22_ylim, title):
def plot_logmag_data_freq_range(meas_filenames, s11_xlim, s12_xlim, s21_xlim, s22_xlim, title, s11_ylim, s12_ylim, s21_ylim, s22_ylim):
    if cal_nf_filenames != None :
        s11_cal, freq_cal = read_sparam_data(cal_nf_filenames[0], 's11')
        s12_cal, freq_cal = read_sparam_data(cal_nf_filenames[0], 's12')
        s21_cal, freq_cal = read_sparam_data(cal_nf_filenames[0], 's21')
        s22_cal, freq_cal = read_sparam_data(cal_nf_filenames[0], 's22')
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        s11, freq = read_sparam_data(meas_filenames[x], 's11')
        gen_logmag_plot(freq, s11, 'S11 (dB)', 'S11 ' + title, label = label) #plot s11
        if cal_nf_filenames != None and x == 1:
            gen_logmag_plot(freq_cal, s11_cal, 'S11 (dB)', 'S11 ' + title, label = str(minicircuit_component))
        x += 1
    ax = plt.gca()
    if s11_xlim == None :
        s11_xlim = [0.4, 0.8]
    else :
        s11_xlim = s11_xlim
    ax.set_xlim(s11_xlim)
    ax.set_ylim(s11_ylim)

    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()
    
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        s12, freq = read_sparam_data(meas_filenames[x], 's12')
        gen_logmag_plot(freq, s12, 'S12 (dB)', 'S12 ' + title, label = label) #plot s12
        if cal_nf_filenames != None and x == 1:
            gen_logmag_plot(freq_cal, s12_cal, 'S12 (dB)', 'S12 ' + title, label = str(minicircuit_component))
        x += 1
    ax = plt.gca()
    if s12_xlim == None :
        s12_xlim = [0.4, 0.8]
    else :
        s12_xlim = s12_xlim
    ax.set_xlim(s12_xlim)
    ax.set_ylim(s12_ylim)

    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()

    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        s21, freq = read_sparam_data(meas_filenames[x], 's21')
        gen_logmag_plot(freq, s21, 'S21 (dB)', 'S21 ' + title, label = label) #plot s21
        if cal_nf_filenames != None and x == 1:
            gen_logmag_plot(freq_cal, s21_cal, 'S21 (dB)', 'S21 ' + title, label = str(minicircuit_component))
        x += 1
    ax = plt.gca()
    if s21_xlim == None :
        s21_xlim = [0.4, 0.8]
    else :
        s21_xlim = s21_xlim
    ax.set_xlim(s21_xlim)
    ax.set_ylim(s21_ylim)
    
    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()
    
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        s22, freq = read_sparam_data(meas_filenames[x], 's22')
        gen_logmag_plot(freq, s22, 'S22 (dB)', 'S22 ' + title, label = label) #plot s22
        if cal_nf_filenames != None and x == 1:
            gen_logmag_plot(freq_cal, s22_cal, 'S22 (dB)', 'S22 ' + title, label = str(minicircuit_component))
        x += 1
    ax = plt.gca()
    if s22_xlim == None :
        s22_xlim = [0.4, 0.8]
    else :
        s22_xlim = s22_xlim
    ax.set_xlim(s22_xlim)
    ax.set_ylim(s22_ylim)

    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()

#--------------------------------------------------------------------------------------------------------
#plot simulated data
def plot_logmag_data_meas_sim(meas_filenames, sim_filenames, s11_xlim, s11_ylim, s12_xlim, s12_ylim, s21_xlim, s21_ylim, s22_xlim, s22_ylim):
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        s11, freq = read_sparam_data(meas_filenames[x], 's11')
        gen_logmag_plot(freq, s11, 'S11 (dB)', 'S11', label = label) #plot s11
        x += 1
    z = 0
    while z < len(sim_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_filenames[z][dir_length:-4]
        else:
            label = plt_label[x]
        s11_sim, freq_sim = read_sparam_data(sim_filenames[z], 's11')
        gen_logmag_plot(freq_sim, s11_sim, 'S11 (dB)', 'S11', label = label) #plot s11 sim
        x += 1
        z += 1
    ax = plt.gca()
    ax.set_xlim(s11_xlim)
    ax.set_ylim(s11_ylim)

    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()
    
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        s12, freq = read_sparam_data(meas_filenames[x], 's12')
        gen_logmag_plot(freq, s12, 'S12 (dB)', 'S12', label = label) #plot s12
        x += 1
    z = 0
    while z < len(sim_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_filenames[z][dir_length:-4]
        else:
            label = plt_label[x]
        s12_sim, freq_sim = read_sparam_data(sim_filenames[z], 's12')
        gen_logmag_plot(freq_sim, s12_sim, 'S12 (dB)', 'S12', label = label) #plot s12 sim
        x += 1
        z += 1
    ax = plt.gca()
    ax.set_xlim(s12_xlim)
    ax.set_ylim(s12_ylim)

    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()

    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        s21, freq = read_sparam_data(meas_filenames[x], 's21')
        gen_logmag_plot(freq, s21, 'S21 (dB)', 'S21', label = label) #plot s21
        x += 1
    z = 0
    while z < len(sim_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_filenames[z][dir_length:-4]
        else:
            label = plt_label[x]
        s21_sim, freq_sim = read_sparam_data(sim_filenames[z], 's21')
        gen_logmag_plot(freq_sim, s21_sim, 'S21 (dB)', 'S21', label = label) #plot s21 sim
        x += 1
        z += 1
    ax = plt.gca()
    ax.set_xlim(s21_xlim)
    ax.set_ylim(s21_ylim)
    
    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()
    
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        s22, freq = read_sparam_data(meas_filenames[x], 's22')
        gen_logmag_plot(freq, s22, 'S22 (dB)', 'S22', label = label) #plot s22
        x += 1
    z = 0
    while z < len(sim_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_filenames[z][dir_length:-4]
        else:
            label = plt_label[x]
        s22_sim, freq_sim = read_sparam_data(sim_filenames[z], 's22')
        gen_logmag_plot(freq_sim, s22_sim, 'S22 (dB)', 'S22', label = label) #plot s22 sim
        x += 1
        z += 1
    ax = plt.gca()
    ax.set_xlim(s22_xlim)
    ax.set_ylim(s22_ylim)

    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()


#def plot_logmag_data_freq_range_meas_sim(meas_filenames, sim_filenames, s11_xlim, s11_ylim, s12_xlim, s12_ylim, s21_xlim, s21_ylim, s22_xlim, s22_ylim, title):
def plot_logmag_data_freq_range_meas_sim(meas_filenames, sim_filenames, s11_xlim, s12_xlim, s21_xlim, s22_xlim, title):
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        s11, freq = read_sparam_data(meas_filenames[x], 's11')
        gen_logmag_plot(freq, s11, 'S11 (dB)', 'S11 ' + title, label = label) #plot s11
        x += 1
    z = 0
    while z < len(sim_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_filenames[z][dir_length:-4]
        else:
            label = plt_label[x]
        s11_sim, freq_sim = read_sparam_data(sim_filenames[z], 's11')
        gen_logmag_plot(freq_sim, s11_sim, 'S11 (dB)', 'S11 ' + title, label = label) #plot s11 sim
        x += 1
        z += 1
    ax = plt.gca()

    ax.set_xlim(s11_xlim)
    ax.set_ylim(s11_ylim)

    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()
    
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        s12, freq = read_sparam_data(meas_filenames[x], 's12')
        gen_logmag_plot(freq, s12, 'S12 (dB)', 'S12 ' + title, label = label) #plot s12
        x += 1
    z = 0
    while z < len(sim_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_filenames[z][dir_length:-4]
        else:
            label = plt_label[x]
        s12_sim, freq_sim = read_sparam_data(sim_filenames[z], 's12')
        gen_logmag_plot(freq_sim, s12_sim, 'S12 (dB)', 'S12 ' + title, label = label) #plot s11 sim
        x += 1
        z += 1
    ax = plt.gca()

    ax.set_xlim(s12_xlim)
    ax.set_ylim(s12_ylim)
    
    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()
    
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        s21, freq = read_sparam_data(meas_filenames[x], 's21')
        gen_logmag_plot(freq, s21, 'S21 (dB)', 'S21 ' + title, label = label) #plot s21
        x += 1
    z = 0
    while z < len(sim_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_filenames[z][dir_length:-4]
        else:
            label = plt_label[x]
        s21_sim, freq_sim = read_sparam_data(sim_filenames[z], 's21')
        gen_logmag_plot(freq_sim, s21_sim, 'S21 (dB)', 'S21 ' + title, label = label) #plot s11 sim
        x += 1
        z += 1
    ax = plt.gca()

    ax.set_xlim(s21_xlim)
    ax.set_ylim(s21_ylim)
    
    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()
    
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        s22, freq = read_sparam_data(meas_filenames[x], 's22')
        gen_logmag_plot(freq, s22, 'S22 (dB)', 'S22 ' + title, label = label) #plot s22
        x += 1
    z = 0
    while z < len(sim_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_filenames[z][dir_length:-4]
        else:
            label = plt_label[x]
        s22_sim, freq_sim = read_sparam_data(sim_filenames[z], 's22')
        gen_logmag_plot(freq_sim, s22_sim, 'S22 (dB)', 'S22 ' + title, label = label) #plot s11 sim
        x += 1
        z += 1
    ax = plt.gca()

    ax.set_xlim(s22_xlim)
    ax.set_ylim(s22_ylim)

    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf'])
    plt.clf()


#-----------------------------------------------------------------------------------------------------------------

def ChangePlotLimits(s11_xlim, s11_ylim, s12_xlim, s12_ylim, s21_xlim, s21_ylim, s22_xlim, s22_ylim, s11_ylim_400to800, s12_ylim_400to800, s21_ylim_400to800, s22_ylim_400to800, s11_ylim_0to1, s12_ylim_0to1, s21_ylim_0to1, s22_ylim_0to1):
    if s11_xlim is not None :
        s11_xlim = s11_xlim
    else:
        s11_xlim = None

    if s11_ylim is not None :
        s11_ylim = s11_ylim
    else:
        s11_ylim = None

    if s12_xlim is not None :
        s12_xlim = s12_xlim
    else:
        s12_xlim = None

    if s12_ylim is not None :
        s12_ylim = s12_ylim
    else:
        s12_ylim = None

    if s21_xlim is not None :
        s21_xlim = s21_xlim
    else:
        s21_xlim = None

    if s21_ylim is not None :
        s21_ylim = s21_ylim
    else:
        s21_ylim = None

    if s22_xlim is not None :
        s22_xlim = s22_xlim
    else:
        s22_xlim = None

    if s22_ylim is not None :
        s22_ylim = s22_ylim
    else:
        s22_ylim = None

    if s11_ylim_400to800 is not None :
        s11_ylim_400to800 = s11_ylim_400to800
    else:
        s11_ylim_400to800 = None

    if s12_ylim_400to800 is not None :
        s12_ylim_400to800 = s12_ylim_400to800
    else:
        s12_ylim_400to800 = None

    if s21_ylim_400to800 is not None :
        s21_ylim_400to800 = s21_ylim_400to800
    else:
        s21_ylim_400to800 = None

    if s22_ylim_400to800 is not None :
        s22_ylim_400to800 = s22_ylim_400to800
    else:
        s22_ylim_400to800 = None

    if s11_ylim_0to1 is not None :
        s11_ylim_0to1 = s11_ylim_0to1
    else:
        s11_ylim_0to1 = None

    if s12_ylim_0to1 is not None :
        s12_ylim_0to1 = s12_ylim_0to1
    else:
        s12_ylim_0to1 = None

    if s21_ylim_0to1 is not None :
        s21_ylim_0to1 = s21_ylim_0to1
    else:
        s21_ylim_0to1 = None

    if s22_ylim_0to1 is not None :
        s22_ylim_0to1 = s22_ylim_0to1
    else:
        s22_ylim_0to1 = None

    return(s11_xlim, s11_ylim, s12_xlim, s12_ylim, s21_xlim, s21_ylim, s22_xlim, s22_ylim, s11_ylim_400to800, s12_ylim_400to800, s21_ylim_400to800, s22_ylim_400to800, s11_ylim_0to1, s12_ylim_0to1, s21_ylim_0to1, s22_ylim_0to1)



#-----------------------------------------------------------------------------------------------------------------

if meas_filenames == [] and sim_filenames == []:
    if __name__ == "__main__":
        print 'No simulated or measured files to plot'
elif sim_filenames == []:
    if __name__ == "__main__":
        s11_xlim, s11_ylim, s12_xlim, s12_ylim, s21_xlim, s21_ylim, s22_xlim, s22_ylim, s11_ylim_400to800, s12_ylim_400to800, s21_ylim_400to800, s22_ylim_400to800, s11_ylim_0to1, s12_ylim_0to1, s21_ylim_0to1, s22_ylim_0to1 = ChangePlotLimits(s11_xlim, s11_ylim, s12_xlim, s12_ylim, s21_xlim, s21_ylim, s22_xlim, s22_ylim, s11_ylim_400to800, s12_ylim_400to800, s21_ylim_400to800, s22_ylim_400to800, s11_ylim_0to1, s12_ylim_0to1, s21_ylim_0to1, s22_ylim_0to1)
        plot_logmag_data(meas_filenames, s11_xlim, s11_ylim, s12_xlim, s12_ylim, s21_xlim, s21_ylim, s22_xlim, s22_ylim)
        title = ['(400-800MHz)', '(0-1GHz)']
        s11_xlim = [[0.4,0.8], [0,1]]
        s12_xlim = [[0.4,0.8], [0,1]]
        s21_xlim = [[0.4,0.8], [0,1]]
        s22_xlim = [[0.4,0.8], [0,1]]
        
        for x in range(len(title)):
            if s11_ylim_400to800 != None and x == 0 :
                s11_ylim = s11_ylim_400to800
            if s12_ylim_400to800 != None and x == 0 :
                s12_ylim = s12_ylim_400to800
            if s21_ylim_400to800 != None and x == 0 :
                s21_ylim = s21_ylim_400to800
            if s22_ylim_400to800 != None and x == 0 :
                s22_ylim = s22_ylim_400to800
            if s11_ylim_0to1 != None and x == 1 :
                s11_ylim = s11_ylim_0to1
            if s12_ylim_0to1 != None and x == 1 :
                s12_ylim = s12_ylim_0to1
            if s21_ylim_0to1 != None and x == 1 :
                s21_ylim = s21_ylim_0to1
            if s22_ylim_0to1 != None and x == 1 :
                s22_ylim = s22_ylim_0to1
            plot_logmag_data_freq_range(meas_filenames, s11_xlim[x], s12_xlim[x], s21_xlim[x], s22_xlim[x], title[x], s11_ylim, s12_ylim, s21_ylim, s22_ylim)
else:
    if __name__ == "__main__":
        s11_xlim, s11_ylim, s12_xlim, s12_ylim, s21_xlim, s21_ylim, s22_xlim, s22_ylim = ChangePlotLimits(s11_xlim, s11_ylim, s12_xlim, s12_ylim, s21_xlim, s21_ylim, s22_xlim, s22_ylim)
        plot_logmag_data_meas_sim(meas_filenames, sim_filenames, s11_xlim, s11_ylim, s12_xlim, s12_ylim, s21_xlim, s21_ylim, s22_xlim, s22_ylim)
        title = ['(400-800MHz)', '(0-1GHz)']
        s11_xlim = [[0.4,0.8], [0,1]]
        #s11_ylim = [[-10,0],[-10,0]]
        s12_xlim = [[0.4,0.8], [0,1]]
        #s12_ylim = [[-50,-10],[-50,-10]]
        s21_xlim = [[0.4,0.8], [0,1]]
        #s21_ylim = [[8,20],[0,30]]
        s22_xlim = [[0.4,0.8], [0,1]]
        #s22_ylim = [[-15,0],[-15,0]]
        for x in range(len(title)):
            #plot_logmag_data_freq_range_meas_sim(meas_filenames, sim_filenames, s11_xlim[x], s11_ylim[x], s12_xlim[x], s12_ylim[x], s21_xlim[x], s21_ylim[x], s22_xlim[x], s22_ylim[x], title[x])
            plot_logmag_data_freq_range_meas_sim(meas_filenames, sim_filenames, s11_xlim[x], s12_xlim[x], s21_xlim[x], s22_xlim[x], title[x])

                     
if len(dBm40_filenames) == 2:
    freq_title = [' (0.4-0.8MHz)', ' (0-1GHz)', ' (0-6GHz)']
    xlim = [[0.4, 0.8], [0,1], [0,6]]
    ylim = [[0, 2]]
    for x in range(len(freq_title)):
        plot_s21_diff(dBm40_filenames, xlim[x], ylim[0], freq_title[x])

if txt_sim_filenames == [] :
    if __name__ == "__main__":
        print 'No simulated text files to plot'
else:
    if __name__ == "__main__":
        xlim = [[0.4, 0.8]]
        ylim = [[10, 20]]
        plot_gain_sim_txt(txt_sim_filenames[0], xlim[0], ylim[0])