import numpy as np
import matplotlib.pyplot as plt
import glob
import skrf.plotting as skplt
import skrf as rf
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-label', '--plt_label', nargs = '+', action = 'store', type = str, default = None, help = 'Labels for the plot legend. List them without quotes or parentheses and do not separate them with commas. The files are read in alphabetically, so put these in the same order the files will be read, e.g. -label label1 label2 label3. If you set this to auto (e.g. -label auto) than the plots will be labeled with the filenames')
parser.add_argument('-dir', '--set_directory', action = 'store', type = str , default = '~/Desktop', help = 'The directory that the files are located. This is also the directory the files will be saved.')
parser.add_argument('-freq', '--set_freq', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum x values that are plotted for S11. List them without quotes or parentheses and do not separate them with commas, e.g. -stab_xlim 0 2')
args = parser.parse_args()

plt_label = args.plt_label
freq_lim = args.set_freq

dir = args.set_directory #the directory where all of your files are located and where the pdf's and jpeg's are saved
dir_length = len(dir)

sim_filenames = glob.glob(dir + '/*Real_Imag.s2p')#make a list of the simulated noise figure files
meas_filenames = glob.glob(dir + '/*L.s2p')#make a list of the measured noise figure files


def read_realimag_data(filename, s):
    ant = rf.Network(filename)
    com = []
    freq = ant.f/1e9
    for y in range(len(ant)):
        if s == 'S11':
            real = ant.s_re[y][0][0]
            imag = ant.s_im[y][0][0]
            com.append(complex(float(real), float(imag)))
        if s == 'S12':
            real = ant.s_re[y][0][1]
            imag = ant.s_im[y][0][1]
            com.append(complex(float(real), float(imag)))
        if s == 'S21':
            real = ant.s_re[y][1][0]
            imag = ant.s_im[y][1][0]
            com.append(complex(float(real), float(imag)))
        if s == 'S22':
            real = ant.s_re[y][1][1]
            imag = ant.s_im[y][1][1]
            com.append(complex(float(real), float(imag)))
        com_np = np.array(com)
    return(com_np, freq)

def realimag(filename):
    s11, freq = read_realimag_data(filename, 'S11')
    s12, freq = read_realimag_data(filename, 'S12')
    s21, freq = read_realimag_data(filename, 'S21')
    s22, freq = read_realimag_data(filename, 'S22')
    return(s11,s12,s21,s22,freq)


def gen_smith_plot(sparam, title, label) :
    skplt.plot_smith(sparam, title = title, label = label)

def plt_smith(meas_filenames, freq_title, freq_min, freq_max) :
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(meas_filenames[x])
        gen_smith_plot(S11, 'S11 Smith', label)
        x += 1
    ax = plt.gca()
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()

    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(meas_filenames[x])
        gen_smith_plot(S12, 'S12 Smith', label)
        x += 1
    ax = plt.gca()
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()

    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(meas_filenames[x])
        gen_smith_plot(S21, 'S21 Smith', label)
        x += 1
    ax = plt.gca()
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()

    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(meas_filenames[x])
        gen_smith_plot(S22, 'S22 Smith', label)
        x += 1
    ax = plt.gca()
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()

def plt_smith_freq(meas_filenames, freq_title, freq_min, freq_max):#Smith plots 400-800MHz
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(meas_filenames[x])
        range = np.where((freq > freq_min) & (freq < freq_max))[0] #gives the indices for the data between 400 & 800 MHz
        y = 0
        S11_range = []
        while y < len(range):
            S11_range.append(S11[range[y]])
            y += 1
        S11_range_np = np.array(S11_range)
        gen_smith_plot(S11_range_np, 'S11 Smith ' + freq_title, label)
        x += 1
    ax = plt.gca()
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()
    
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(meas_filenames[x])
        range = np.where((freq > freq_min) & (freq < freq_max))[0] #gives the indices for the data between 400 & 800 MHz
        y = 0
        S12_range = []
        while y < len(range):
            S12_range.append(S12[range[y]])
            y += 1
        S12_range_np = np.array(S12_range)
        gen_smith_plot(S12_range_np, 'S12 Smith ' + freq_title, label)
        x += 1
    ax = plt.gca()
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()

    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(meas_filenames[x])
        range = np.where((freq > freq_min) & (freq < freq_max))[0] #gives the indices for the data between 400 & 800 MHz
        y = 0
        S21_range = []
        while y < len(range):
            S21_range.append(S21[range[y]])
            y += 1
        S21_range_np = np.array(S21_range)
        gen_smith_plot(S21_range_np, 'S21 Smith ' + freq_title, label)
        x += 1
    ax = plt.gca()
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()
    
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(meas_filenames[x])
        range = np.where((freq > freq_min) & (freq < freq_max))[0] #gives the indices for the data between 400 & 800 MHz
        y = 0
        S22_range = []
        while y < len(range):
            S22_range.append(S22[range[y]])
            y += 1
        S22_range_np = np.array(S22_range)
        gen_smith_plot(S22_range_np, 'S22 Smith ' + freq_title, label)
        x += 1
    ax = plt.gca()
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()


def plt_smith_meas_sim(meas_filenames, sim_filenames, freq_title, freq_min, freq_max) :
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(meas_filenames[x])
        gen_smith_plot(S11, 'S11 Smith', label)
        x += 1
    z = 0
    while z < len(sim_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_filenames[z][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(sim_filenames[z])
        gen_smith_plot(S11, 'S11 Smith', label)
        x += 1
        z += 1
    ax = plt.gca()
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()

    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(meas_filenames[x])
        gen_smith_plot(S12, 'S12 Smith', label)
        x += 1
    z = 0
    while z < len(sim_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_filenames[z][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(sim_filenames[z])
        gen_smith_plot(S12, 'S12 Smith', label)
        x += 1
        z += 1
    ax = plt.gca()
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()
    
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(meas_filenames[x])
        gen_smith_plot(S21, 'S21 Smith', label)
        x += 1
    z = 0
    while z < len(sim_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_filenames[z][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(sim_filenames[z])
        gen_smith_plot(S21, 'S21 Smith', label)
        x += 1
        z += 1
    ax = plt.gca()
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()

    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(meas_filenames[x])
        gen_smith_plot(S22, 'S22 Smith', label)
        x += 1
    z = 0
    while z < len(sim_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_filenames[z][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(sim_filenames[z])
        gen_smith_plot(S22, 'S22 Smith', label)
        x += 1
        z += 1
    ax = plt.gca()
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()
    
def plt_smith_meas_sim_freq(meas_filenames, sim_filenames, freq_title, freq_min, freq_max) :#Smith plots 400-800MHz
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(meas_filenames[x])
        range = np.where((freq > freq_min) & (freq < freq_max))[0] #gives the indices for the data between 400 & 800 MHz
        y = 0
        S11_range = []
        while y < len(range):
            S11_range.append(S11[range[y]])
            y += 1
        S11_range_np = np.array(S11_range)
        gen_smith_plot(S11_range_np, 'S11 Smith ' + freq_title, label)
        x += 1
    z = 0
    while z < len(sim_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_filenames[z][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(sim_filenames[z])
        range = np.where((freq > freq_min) & (freq < freq_max))[0] #gives the indices for the data between 400 & 800 MHz
        y = 0
        S11_range = []
        while y < len(range):
            S11_range.append(S11[range[y]])
            y += 1
        S11_range_np = np.array(S11_range)
        gen_smith_plot(S11_range_np, 'S11 Smith ' + freq_title, label)
        x += 1
        z += 1
    ax = plt.gca()
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()
    
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(meas_filenames[x])
        range = np.where((freq > freq_min) & (freq < freq_max))[0] #gives the indices for the data between 400 & 800 MHz
        y = 0
        S12_range = []
        while y < len(range):
            S12_range.append(S12[range[y]])
            y += 1
        S12_range_np = np.array(S12_range)
        gen_smith_plot(S12_range_np, 'S12 Smith ' + freq_title, label)
        x += 1
    z = 0
    while z < len(sim_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_filenames[z][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(sim_filenames[z])
        range = np.where((freq > freq_min) & (freq < freq_max))[0] #gives the indices for the data between 400 & 800 MHz
        y = 0
        S12_range = []
        while y < len(range):
            S12_range.append(S12[range[y]])
            y += 1
        S12_range_np = np.array(S12_range)
        gen_smith_plot(S12_range_np, 'S12 Smith ' + freq_title, label)
        x += 1
        z += 1
    ax = plt.gca()
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()

    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(meas_filenames[x])
        range = np.where((freq > freq_min) & (freq < freq_max))[0] #gives the indices for the data between 400 & 800 MHz
        y = 0
        S21_range = []
        while y < len(range):
            S21_range.append(S21[range[y]])
            y += 1
        S21_range_np = np.array(S21_range)
        gen_smith_plot(S21_range_np, 'S21 Smith ' + freq_title, label)
        x += 1
    z = 0
    while z < len(sim_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_filenames[z][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(sim_filenames[z])
        range = np.where((freq > freq_min) & (freq < freq_max))[0] #gives the indices for the data between 400 & 800 MHz
        y = 0
        S21_range = []
        while y < len(range):
            S21_range.append(S21[range[y]])
            y += 1
        S21_range_np = np.array(S21_range)
        gen_smith_plot(S21_range_np, 'S21 Smith ' + freq_title, label)
        x += 1
        z += 1
    ax = plt.gca()
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()
    
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(meas_filenames[x])
        range = np.where((freq > freq_min) & (freq < freq_max))[0] #gives the indices for the data between 400 & 800 MHz
        y = 0
        S22_range = []
        while y < len(range):
            S22_range.append(S22[range[y]])
            y += 1
        S22_range_np = np.array(S22_range)
        gen_smith_plot(S22_range_np, 'S22 Smith ' + freq_title, label)
        x += 1
    z = 0
    while z < len(sim_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_filenames[z][dir_length:-4]
        else :
            label = plt_label[x]
        S11, S12, S21, S22, freq = realimag(sim_filenames[z])
        range = np.where((freq > freq_min) & (freq < freq_max))[0] #gives the indices for the data between 400 & 800 MHz
        print range[0]
        print range[len(range)]
        y = 0
        S22_range = []
        while y < len(range):
            S22_range.append(S22[range[y]])
            y += 1
        S22_range_np = np.array(S22_range)
        gen_smith_plot(S22_range_np, 'S22 Smith ' + freq_title, label)
        x += 1
        z += 1
    ax = plt.gca()
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()


#-----------------------------------------------------------------------------------------------------------------

if sim_filenames == [] :
    if __name__ == "__main__":
        freq_title = ''
        freq_min = None
        freq_max = None
        plt_smith(meas_filenames, freq_title, freq_min, freq_max)
        freq_title = ['(400-800MHz)', '(0-1GHz)']
        freq_min = [0.4, 0]
        freq_max = [0.8, 1]
        for x in range(len(freq_title)):
            plt_smith_freq(meas_filenames, freq_title[x], freq_min[x], freq_max[x])

else :
    if __name__ == "__main__":
        freq_title = ''
        freq_min = None
        freq_max = None
        plt_smith_meas_sim(meas_filenames, sim_filenames, freq_title, freq_min, freq_max)
        freq_title = ['(400-800MHz)', '(0-1GHz)']
        freq_min = [0.4, 0]
        freq_max = [0.8, 1]
        for x in range(len(freq_title)):
            plt_smith_meas_sim_freq(meas_filenames, sim_filenames, freq_title[x], freq_min[x], freq_max[x])