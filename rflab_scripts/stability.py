import numpy as np
import matplotlib.pyplot as plt
import glob
import skrf.plotting as skplt
import skrf as rf
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-label', '--plt_label', nargs = '+', action = 'store', type = str, default = None, help = 'Labels for the plot legend. List them without quotes or parentheses and do not separate them with commas. The files are read in alphabetically, so put these in the same order the files will be read, e.g. -label label1 label2 label3. If you set this to auto (e.g. -label auto) than the plots will be labeled with the filenames')
parser.add_argument('-dir', '--set_directory', action = 'store', type = str , default = '~/Desktop', help = 'The directory that the files are located. This is also the directory the files will be saved.')
parser.add_argument('-stab_xlim', '--set_stab_xlim', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum x values that are plotted for S11. List them without quotes or parentheses and do not separate them with commas, e.g. -stab_xlim 0 2')
parser.add_argument('-stab_ylim', '--set_stab_ylim', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum y values that are plotted for S11. List them without quotes or parentheses and do not separate them with commas, e.g. -stab_ylim 0 2')
args = parser.parse_args()

plt_label = args.plt_label
stab_xlim = args.set_stab_xlim
stab_ylim = args.set_stab_ylim

dir = args.set_directory #the directory where all of your files are located and where the pdf's and jpeg's are saved
dir_length = len(dir)

sim_filenames = glob.glob(dir + '/*Real_Imag.s2p')#make a list of the simulated noise figure files
meas_filenames = glob.glob(dir + '/*L.s2p')#make a list of the measured noise figure files


def read_realimag_data(filename, s):
    ant = rf.Network(filename)
    com = []
    freq = ant.f/1e9
    for y in range(len(ant)):
        if s == 's11':
            real = ant.s_re[y][0][0]
            imag = ant.s_im[y][0][0]
            com.append(complex(float(real), float(imag)))
        if s == 's12':
            real = ant.s_re[y][0][1]
            imag = ant.s_im[y][0][1]
            com.append(complex(float(real), float(imag)))
        if s == 's21':
            real = ant.s_re[y][1][0]
            imag = ant.s_im[y][1][0]
            com.append(complex(float(real), float(imag)))
        if s == 's22':
            real = ant.s_re[y][1][1]
            imag = ant.s_im[y][1][1]
            com.append(complex(float(real), float(imag)))
        com_np = np.array(com)
    return(com_np, freq)

def realimag(filename):
    s11, freq = read_realimag_data(filename, 's11')
    s12, freq = read_realimag_data(filename, 's12')
    s21, freq = read_realimag_data(filename, 's21')
    s22, freq = read_realimag_data(filename, 's22')
    return(s11,s12,s21,s22,freq)

def CalcMuStabFactor(filename) :
    s11, s12, s21, s22, freq = realimag(filename)
    mu = (1-np.abs(s11)**2)/(np.abs(s22 - np.conj(s11)* (s11*s22 - s12*s21)) + np.abs(s12*s21))
    return(mu, freq)

def CalcKStabFactor(filename) :
    s11, s12, s21, s22, freq = realimag(filename)
    k = (1-np.abs(s11)**2 - np.abs(s22)**2 + np.abs(s11*s22 - s12*s21)**2)/(2*np.abs(s21)*np.abs(s12))
    return (k, freq)

def gen_stab_fact_plot(freq, stab_factor, label, freq_title) :
    skplt.plot_rectangular(freq, stab_factor, x_label = 'Frequency (GHz)', y_label = 'Stability Factor', title = 'Stability Factor' + freq_title, label = label)

def plot_stab_fact(meas_filenames, stab_xlim, stab_ylim, freq_title) :
    x = 0
    while x < len(meas_filenames) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        mu, freq = CalcMuStabFactor(meas_filenames[x])
        k, freq = CalcKStabFactor(meas_filenames[x])
        gen_stab_fact_plot(freq, mu, label, freq_title)
        gen_stab_fact_plot(freq, k, label, freq_title)
        x += 1
    ax = plt.gca()
    ax.set_xlim(stab_xlim)
    ax.set_ylim(stab_ylim)
    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()

def plot_stab_fact_meas_sim(meas_filenames, sim_filenames, stab_xlim, stab_ylim, freq_title) :
    x = 0
    while x < len(meas_filenames) :
        mu, freq = CalcMuStabFactor(meas_filenames[x])
        k, freq = CalcKStabFactor(meas_filenames[x])
        if plt_label == None :
            label = None
            gen_stab_fact_plot(freq, mu, label, freq_title)
            gen_stab_fact_plot(freq, k, label, freq_title)
        elif plt_label[0] == 'auto' :
            label = meas_filenames[x][dir_length:-4]
            gen_stab_fact_plot(freq, mu, label, freq_title)
            gen_stab_fact_plot(freq, k, label, freq_title)
        else :
            gen_stab_fact_plot(freq, mu, plt_label[x] + ' mu', freq_title)
            gen_stab_fact_plot(freq, k, plt_label[x] + ' k', freq_title)
        x += 1
    z = 0
    while z < len(sim_filenames) :
        mu, freq = CalcMuStabFactor(sim_filenames[z])
        k, freq = CalcKStabFactor(sim_filenames[z])
        if plt_label == None :
            label = None
            gen_stab_fact_plot(freq, mu, label, freq_title)
            gen_stab_fact_plot(freq, k, label, freq_title)
        elif plt_label[0] == 'auto' :
            label = sim_filenames[z][dir_length:-4]
            gen_stab_fact_plot(freq, mu, label, freq_title)
            gen_stab_fact_plot(freq, k, label, freq_title)
        else :
            gen_stab_fact_plot(freq, mu, plt_label[x] + ' mu', freq_title)
            gen_stab_fact_plot(freq, k, plt_label[x] + ' k', freq_title)
        x += 1
        z += 1
    ax = plt.gca()
    ax.set_xlim(stab_xlim)
    ax.set_ylim(stab_ylim)
    skplt.func_on_all_figs(plt.grid, alpha = 0.5)
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()


#-----------------------------------------------------------------------------------------------------------------

def ChangePlotLimits(stab_xlim, stab_ylim):
    if stab_xlim is not None :
        stab_xlim = stab_xlim
    else:
        stab_xlim = None

    if stab_ylim is not None :
        stab_ylim = stab_ylim
    else:
        stab_ylim = None
    return(stab_xlim, stab_ylim)


#-----------------------------------------------------------------------------------------------------------------

if sim_filenames == [] :
    if __name__ == "__main__":
        if stab_ylim == None:
            stab_ylim = [0.6,2]
            freq_title = ''
            plot_stab_fact(meas_filenames, stab_xlim, stab_ylim, freq_title)
        else:
            stab_ylim = stab_ylim
            freq_title = ''
            plot_stab_fact(meas_filenames, stab_xlim, stab_ylim, freq_title)
        stab_xlim = [[0.4,0.8],[0,1]]
        stab_ylim = [[0.6,2]]
        freq_title = [' (0.4-0.8MHz)', ' (0-1GHz)']
        for x in range(len(freq_title)):
            plot_stab_fact(meas_filenames, stab_xlim[x], stab_ylim[0], freq_title[x])

else :
    if __name__ == "__main__":
        if stab_ylim == None:
            stab_ylim = [0.6,2]
            freq_title = ''
            plot_stab_fact_meas_sim(meas_filenames, sim_filenames, stab_xlim, stab_ylim, freq_title)
        else:
            stab_ylim = stab_ylim
            freq_title = ''
            plot_stab_fact_meas_sim(meas_filenames, sim_filenames, stab_xlim, stab_ylim, freq_title)
        stab_xlim = [[0.4,0.8],[0,1]]
        stab_ylim = [[0.6,2]]
        freq_title = [' (0.4-0.8MHz)', ' (0-1GHz)']
        for x in range(len(freq_title)):
            plot_stab_fact_meas_sim(meas_filenames, sim_filenames, stab_xlim[x], stab_ylim[0], freq_title[x])