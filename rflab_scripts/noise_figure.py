import numpy as np
import matplotlib.pyplot as plt
import glob
import skrf.plotting as skplt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-label', '--plt_label', nargs = '+', action = 'store', type = str, default = None, help = 'Labels for the plot legend. List them without quotes or parentheses and do not separate them with commas. The files are read in alphabetically, so put these in the same order the files will be read, e.g. -label label1 label2 label3. If you set this to auto (e.g. -label auto) than the plots will be labeled with the filenames')
parser.add_argument('-dir', '--set_directory', action = 'store', type = str , default = '~/Desktop', help = 'The directory that the files are located. This is also the directory the files will be saved.')
parser.add_argument('-ymin', '--set_ymin', action = 'store', type = float, default = None, help = 'Sets the minimum x value that is plotted')
parser.add_argument('-ymax', '--set_ymax', action = 'store', type = float, default = None, help = 'Sets the maximum x value that is plotted')
parser.add_argument('-xmin', '--set_xmin', action = 'store', type = float, default = None, help = 'Sets the minimum y value that is plotted')
parser.add_argument('-xmax', '--set_xmax', action = 'store', type = float, default = None, help = 'Sets the maximum y value that is plotted')
parser.add_argument('-xlim', '--set_xlim', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum x values that are plotted. List them without quotes or parentheses and do not separate them with commas, e.g. -xlim 0 2')
parser.add_argument('-ylim', '--set_ylim', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum y values that are plotted. List them without quotes or parentheses and do not separate them with commas, e.g. -ylim 0 2')
parser.add_argument('-gain_xlim', '--set_gain_xlim', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum x values that are plotted. List them without quotes or parentheses and do not separate them with commas, e.g. -xlim 0 2')
parser.add_argument('-gain_ylim', '--set_gain_ylim', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum y values that are plotted. List them without quotes or parentheses and do not separate them with commas, e.g. -ylim 0 2')
parser.add_argument('-cal', '--set_cal_component', action = 'store', type = str, default = None, choices = ('ZX60-P103LN+', 'ZX60-P33ULN+', 'ZX60-3018G-S+'), help = 'Choose the minicircuit component that you used as a calibrator - only set this if you would like to plot the simulated data')
args = parser.parse_args()

plt_label = args.plt_label
xmin = args.set_xmin
xmax = args.set_xmax
ymin = args.set_ymin
ymax = args.set_ymax
xlim = args.set_xlim
ylim = args.set_ylim
gain_xlim = args.set_gain_xlim
gain_ylim = args.set_gain_ylim


dir = args.set_directory #the directory where all of your files are located and where the pdf's and jpeg's are saved
dir_length = len(dir)

sim_nf_filenames = glob.glob(dir + '/*nf2.txt')#make a list of the simulated noise figure files
meas_nf_filenames = glob.glob(dir + '/*hp8970b_nf.npy')#make a list of the measured noise figure files

if args.set_cal_component is not None :
    minicircuit_component = args.set_cal_component
    cal_nf_filenames = glob.glob('/Users/brittanyjohnstone/Desktop/Research/Kevin/WVU/minicircuit_components/' + minicircuit_component + '/*nf_sim.txt')
else:
    cal_nf_filenames = None
    minicircuit_component = None

#READ MEASURED NOISE FIGURE DATA
def read_nf_data_from_mult_files(meas_filenames) :
    x = 0
    freq = []
    gain = []
    nf = []
    file_len = []
    while x < len(meas_nf_filenames):
        noise = np.load(meas_nf_filenames[x]) #load the npy file created by hp8970b.py
        index = 0
        while index < len(noise) :
            freq.append(float(noise[index][0])) #frequency from npy file
            gain.append(float(noise[index][1])) #noise figure in dB from npy file
            nf.append(float(noise[index][2]))
            index += 1
        file_len.append(int(index))
        x += 1
    freq_nparray = np.array(freq)
    gain_nparray = np.array(gain)
    nf_nparray = np.array(nf)
    return(freq_nparray, gain_nparray, nf_nparray, file_len)



#READ SIMULATED NOISE FIGURE DATA
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
                if y != 0 :
                    nf_data.append(row.split())
                    y += 1
                else:
                    y += 1
            file_len.append(int(y-1))
            x += 1
    tot_file_len = sum(file_len)
    m = 0
    freq = []
    nf = []
    #gamma = []
    #phase_angle = []
    #noise_resistance = []
    while m < tot_file_len :
        if nf_data[m] != []:
            freq.append(float(nf_data[m][0]))
            nf.append(float(nf_data[m][1]))
            m += 1
        else:
            m += 1
        #gamma.append(float(nf_data[m][2]))
        #phase_angle.append(float(nf_data[m][3]))
        #noise_resistance.append(float(nf_data[m][4]))
    freq_nparray = np.array(freq)
    nf_nparray = np.array(nf)
    #gamma_nparray = np.array(gamma)
    #phase_angle_nparray = np.array(phase_angle)
    #noise_resistance_nparray = np.array(noise_resistance)
    return (freq_nparray, nf_nparray, file_len) #gamma_nparray, phase_angle_nparray, noise_resistance_nparray, file_len)

#-----------------------------------------------------------------------------------------------------------------

#NOISE FIGURE
#Plots just the measured nf data
def plot_nf_no_sim(meas_nf_filenames, cal_nf_filenames, plt_label, title, minicircuit_component, xmin, xmax, ymin, ymax, xlim, ylim, dir_length) :
    nf_freq, gain, nf, file_len = read_nf_data_from_mult_files(meas_nf_filenames)
    if cal_nf_filenames is not None:
        cal_freq_nparray, cal_nf_nparray, cal_gamma_nparray, cal_phase_angle_nparray, cal_noise_resistance_nparray, cal_sim_file_len = read_nf_data_from_mult_ADS_files(cal_nf_filenames)
    z = 0
    while z < len(file_len) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_nf_filenames[z][dir_length:-4]
        else :
            label = plt_label[z]
        if z == 0:
            skplt.plot_rectangular(nf_freq[0:file_len[z]]/1e9, nf[0:file_len[z]], x_label = 'Frequency (GHz)', y_label = 'Noise Figure (dB)', title = title, label = label)
            z += 1
        else :
            skplt.plot_rectangular(nf_freq[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])]/1e9, nf[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])], x_label = 'Frequency (GHz)', y_label = 'Noise Figure (dB)', title = title, label = label)
            z += 1
    if cal_nf_filenames is not None :
        x = 0
        while x < len(cal_sim_file_len) : #plot the simulated calibrator nf data
            skplt.plot_rectangular(cal_freq_nparray[0:cal_sim_file_len[x]]/1e9, cal_nf_nparray[0:cal_sim_file_len[x]], x_label = 'Frequency (GHz)', y_label = 'Noise Figure (dB)', title = title, label = minicircuit_component + ' sim')
            x += 1

    skplt.func_on_all_figs(plt.grid, alpha = 0.5) #alpha changes how dark the gridlines are, the larger alpha is the darker the lines are

    x1,x2,y1,y2 = plt.axis()

    if xlim == None :
        if xmin == None and xmax == None :
            xlim = [0,1]
        elif xmin == None and xmax is not None :
            xlim = [0, xmax]
        elif xmin is not None and xmax == None :
            xlim = [xmin, 1]
        else :
            xlim = [xmin, xmax]
    else:
        xlim = xlim

    if ylim == None :
        if ymin == None and ymax == None :
            ylim = [0,1.4]
        elif ymin == None and ymax is not None :
            ylim = [0, ymax]
        elif ymin is not None and ymax == None :
            ylim = [ymin, 1.4]
        else :
            ylim = [ymin, ymax]
    else:
        ylim = ylim

    ax = plt.gca()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()

#Plots just the measured gain data
def plot_nfgain_no_sim(meas_nf_filenames, cal_nf_filenames, plt_label, minicircuit_component, gain_xlim, gain_ylim, dir_length) :
    nf_freq, gain, nf, file_len = read_nf_data_from_mult_files(meas_nf_filenames)
    
    if cal_nf_filenames is not None:
        cal_freq_nparray, cal_nf_nparray, cal_gamma_nparray, cal_phase_angle_nparray, cal_noise_resistance_nparray, cal_sim_file_len = read_nf_data_from_mult_ADS_files(cal_nf_filenames)
    z = 0
    while z < len(file_len) :
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_nf_filenames[z][dir_length:-4]
        else :
            label = plt_label[z]
        if z == 0:
            skplt.plot_rectangular(nf_freq[0:file_len[z]]/1e9, gain[0:file_len[z]], x_label = 'Frequency (GHz)', y_label = 'HP8970b Gain (dB)', title = 'HP8970b Gain', label = label)
            z += 1
        else :
            skplt.plot_rectangular(nf_freq[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])]/1e9, gain[sum(file_len[0:z]):(sum(file_len[0:z]) + file_len[z])], x_label = 'Frequency (GHz)', y_label = 'HP8970b Gain (dB)', title = 'HP8970b Gain', label = label)
            z += 1

    skplt.func_on_all_figs(plt.grid, alpha = 0.5) #alpha changes how dark the gridlines are, the larger alpha is the darker the lines are
    
    x1,x2,y1,y2 = plt.axis()
    
    if gain_xlim == None :
        gain_xlim = [x1,x2]
    else:
        gain_xlim = gain_xlim

    if gain_ylim == None :
        gain_ylim = [y1, y2]
    else:
        gain_ylim = gain_ylim
    ax = plt.gca()
    ax.set_xlim(gain_xlim)
    ax.set_ylim(gain_ylim)
    
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()


#Plots both simulated and measured data
def plot_nf_meas_and_sim(meas_nf_filenames, sim_nf_filenames, cal_nf_filenames, plt_label, title, minicircuit_component, xmin, xmax, ymin, ymax, xlim, ylim, dir_length) :
    nf_freq, gain, nf, meas_file_len = read_nf_data_from_mult_files(meas_nf_filenames)
    freq_nparray, nf_nparray, sim_file_len = read_nf_data_from_mult_ADS_files(sim_nf_filenames)
    if cal_nf_filenames is not None:
        cal_freq_nparray, cal_nf_nparray, cal_gamma_nparray, cal_phase_angle_nparray, cal_noise_resistance_nparray, cal_sim_file_len = read_nf_data_from_mult_ADS_files(cal_nf_filenames)
    z = 0
    while z < len(meas_file_len) : #plot the measured nf data
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = meas_nf_filenames[z][dir_length:-4]
        else :
            label = plt_label[z]
        if z == 0:
            skplt.plot_rectangular(nf_freq[0:meas_file_len[z]]/1e9, nf[0:meas_file_len[z]], x_label = 'Frequency (GHz)', y_label = 'Noise Figure (dB)', title = title, label = label) #plots the measured nf data from the first file
            #print nf[0:file_len[z]]
            z += 1
        else :
            skplt.plot_rectangular(nf_freq[sum(meas_file_len[0:z]):(sum(meas_file_len[0:z]) + meas_file_len[z])]/1e9, nf[sum(meas_file_len[0:z]):(sum(meas_file_len[0:z]) + meas_file_len[z])], x_label = 'Frequency (GHz)', y_label = 'Noise Figure (dB)', title = title, label = label) #plots the measured nf data from the rest of the files
            z += 1
    x = 0
    while x < len(sim_file_len) : #plot the simulated nf data
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_nf_filenames[x][dir_length:-4]
        else :
            label = plt_label[z]
        if x == 0:
            skplt.plot_rectangular(freq_nparray[0:sim_file_len[x]]/1e9, nf_nparray[0:sim_file_len[x]], x_label = 'Frequency (GHz)', y_label = 'Noise Figure (dB)', title = title, label = label) #plots the simulated nf data from the first file
            z += 1
            x += 1
        else :
            skplt.plot_rectangular(freq_nparray[sum(sim_file_len[0:x]):(sum(sim_file_len[0:x]) + sim_file_len[x])]/1e9, nf_nparray[sum(sim_file_len[0:x]):(sum(sim_file_len[0:x]) + sim_file_len[x])], x_label = 'Frequency (GHz)', y_label = 'Noise Figure (dB)', title = title, label = label) #plots the simulated nf data from the rest of the files
            z += 1
            x += 1
    if cal_nf_filenames is not None :
        x = 0
        while x < len(cal_sim_file_len) : #plot the simulated calibrator nf data
            skplt.plot_rectangular(cal_freq_nparray[0:cal_sim_file_len[x]]/1e9, cal_nf_nparray[0:cal_sim_file_len[x]], x_label = 'Frequency (GHz)', y_label = 'Noise Figure (dB)', title = title, label = minicircuit_component + ' sim')
            x += 1
    skplt.func_on_all_figs(plt.grid, alpha = 0.5) #alpha changes how dark the gridlines are, the larger alpha is the darker the lines are
    
    x1,x2,y1,y2 = plt.axis()

    if xlim == None :
        if xmin == None and xmax == None :
            xlim = [0,1]
        elif xmin == None and xmax is not None :
            xlim = [0, xmax]
        elif xmin is not None and xmax == None :
            xlim = [xmin, 1]
        else :
            xlim = [xmin, xmax]
    else:
        xlim = xlim
    
    if ylim == None :
        if ymin == None and ymax == None :
            ylim = [0,1.4]
        elif ymin == None and ymax is not None :
            ylim = [0, ymax]
        elif ymin is not None and ymax == None :
            ylim = [ymin, 1.4]
        else :
            ylim = [ymin, ymax]
    else:
        ylim = ylim
    
    ax = plt.gca()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()


#Plots just the simulated data
def plot_nf_sim(sim_nf_filenames, cal_nf_filenames, plt_label, title, minicircuit_component, xmin, xmax, ymin, ymax, xlim, ylim, dir_length) :
    nf_freq, gain, nf, meas_file_len = read_nf_data_from_mult_files(meas_nf_filenames)
    freq_nparray, nf_nparray, sim_file_len = read_nf_data_from_mult_ADS_files(sim_nf_filenames)
    if cal_nf_filenames is not None:
        cal_freq_nparray, cal_nf_nparray, cal_gamma_nparray, cal_phase_angle_nparray, cal_noise_resistance_nparray, cal_sim_file_len = read_nf_data_from_mult_ADS_files(cal_nf_filenames)
    x = 0
    while x < len(sim_file_len) : #plot the simulated nf data
        if plt_label == None :
            label = None
        elif plt_label[0] == 'auto' :
            label = sim_nf_filenames[x][dir_length:-4]
        else :
            label = plt_label[x]
        if x == 0:
            skplt.plot_rectangular(freq_nparray[0:sim_file_len[x]]/1e9, nf_nparray[0:sim_file_len[x]], x_label = 'Frequency (GHz)', y_label = 'Noise Figure (dB)', title = title, label = label) #plots the simulated nf data from the first file
            x += 1
        else :
            skplt.plot_rectangular(freq_nparray[sum(sim_file_len[0:x]):(sum(sim_file_len[0:x]) + sim_file_len[x])]/1e9, nf_nparray[sum(sim_file_len[0:x]):(sum(sim_file_len[0:x]) + sim_file_len[x])], x_label = 'Frequency (GHz)', y_label = 'Noise Figure (dB)', title = title, label = label) #plots the simulated nf data from the rest of the files
            x += 1
    if cal_nf_filenames is not None :
        x = 0
        while x < len(cal_sim_file_len) : #plot the simulated calibrator nf data
            skplt.plot_rectangular(cal_freq_nparray[0:cal_sim_file_len[x]]/1e9, cal_nf_nparray[0:cal_sim_file_len[x]], x_label = 'Frequency (GHz)', y_label = 'Noise Figure (dB)', title = title, label = minicircuit_component + ' sim')
            x += 1
    skplt.func_on_all_figs(plt.grid, alpha = 0.5) #alpha changes how dark the gridlines are, the larger alpha is the darker the lines are

    x1,x2,y1,y2 = plt.axis()
    
    if xlim == None :
        if xmin == None and xmax == None :
            xlim = [0,1]
        elif xmin == None and xmax is not None :
            xlim = [0, xmax]
        elif xmin is not None and xmax == None :
            xlim = [xmin, 1]
        else :
            xlim = [xmin, xmax]
    else:
        xlim = xlim
    
    if ylim == None :
        if ymin == None and ymax == None :
            ylim = [0,1.4]
        elif ymin == None and ymax is not None :
            ylim = [0, ymax]
        elif ymin is not None and ymax == None :
            ylim = [ymin, 1.4]
        else :
            ylim = [ymin, ymax]
    else:
        ylim = ylim
    
    ax = plt.gca()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
#plt.show()
    
    skplt.save_all_figs(dir, format = ['pdf', 'jpeg'])
    plt.clf()



#Set the plot parameters
def ChangePlotParams(xmin, xmax, ymin, ymax, xlim, ylim, gain_xlim, gain_ylim) :
    #if plt_label[0] == 'auto' :
    #   plt_label = 'auto'
    #print plt_label
    #elif plt_label == None :
    #   plt_label = None
    #else :
    #   plt_label = plt_label
    #print plt_label

    if xmin is not None:
        xmin = xmin
    else:
        xmin = None
    
    if xmax is not None:
        xmax = xmax
    else:
        xmax = None
    
    if ymin is not None:
        ymin = ymin
    else:
        ymin = None
    
    if ymax is not None:
        ymax = ymax
    else:
        ymax = None
    
    if xlim is not None :
        xlim = xlim
    else:
        xlim = None
    
    if ylim is not None :
        ylim = ylim
    else:
        ylim = None

    if gain_xlim is not None :
        gain_xlim = gain_xlim
    else:
        gain_xlim = None

    if gain_ylim is not None :
        gain_ylim = gain_ylim
    else:
        gain_ylim = None


    return(plt_label, xmin, xmax, ymin, ymax, xlim, ylim, gain_xlim, gain_ylim)


#-----------------------------------------------------------------------------------------------------------------

if meas_nf_filenames == [] and sim_nf_filenames == []:
    if __name__ == "__main__":
        print 'No simulated or measured files to plot'
else:
    if sim_nf_filenames == []:
        if __name__ == "__main__":
            plt_label, xmin, xmax, ymin, ymax, xlim, ylim, gain_xlim, gain_ylim = ChangePlotParams(args.set_xmin, args.set_xmax, args.set_ymin, args.set_ymax, args.set_xlim, args.set_ylim, args.set_gain_xlim, args.set_gain_ylim)
            title = ['Noise Figure (0-1GHz)', 'Noise Figure (0-1.8GHz)', 'Noise Figure (0.4-0.8GHz)']
            xlim_set = [[0,1], [0,1.8], [0.4,0.8]]
            ylim_set = [[0,1.4]]
            for x in range(len(title)):
                plot_nf_no_sim(meas_nf_filenames, cal_nf_filenames, plt_label, title[x], minicircuit_component, xmin, xmax, ymin, ymax, xlim_set[x], ylim_set[0], dir_length)
            if (xlim is not None) or (ylim is not None) or (xmin is not None) or (xmax is not None) or (ymin is not None) or (ymax is not None):
                title = 'Noise Figure'
                plot_nf_sim(sim_nf_filenames, cal_nf_filenames, plt_label, title, minicircuit_component, xmin, xmax, ymin, ymax, xlim, ylim, dir_length)
            plot_nfgain_no_sim(meas_nf_filenames, cal_nf_filenames, plt_label, minicircuit_component, gain_xlim, gain_ylim, dir_length)

    elif meas_nf_filenames == []:
        if __name__ == "__main__":
            plt_label, xmin, xmax, ymin, ymax, xlim, ylim, gain_xlim, gain_ylim = ChangePlotParams(args.set_xmin, args.set_xmax, args.set_ymin, args.set_ymax, args.set_xlim, args.set_ylim, args.set_gain_xlim, args.set_gain_ylim)
            title = ['Noise Figure (0-1GHz)', 'Noise Figure (0-6GHz)', 'Noise Figure (0.4-0.8GHz)']
            xlim_set = [[0,1], [0,6], [0.4,0.8]]
            ylim_set = [[0,1.4]]
            for x in range(len(title)):
                plot_nf_sim(sim_nf_filenames, cal_nf_filenames, plt_label, title[x], minicircuit_component, xmin, xmax, ymin, ymax, xlim_set[x], ylim_set[0], dir_length)
            if (xlim is not None) or (ylim is not None) or (xmin is not None) or (xmax is not None) or (ymin is not None) or (ymax is not None):
                title = 'Noise Figure'
                plot_nf_sim(sim_nf_filenames, cal_nf_filenames, plt_label, title, minicircuit_component, xmin, xmax, ymin, ymax, xlim, ylim, dir_length)
    else :
        if __name__ == "__main__":
            plt_label, xmin, xmax, ymin, ymax, xlim, ylim, gain_xlim, gain_ylim = ChangePlotParams(args.set_xmin, args.set_xmax, args.set_ymin, args.set_ymax, args.set_xlim, args.set_ylim, args.set_gain_xlim, args.set_gain_ylim)
            title = ['Noise Figure (0-1GHz)', 'Noise Figure (0-6GHz)', 'Noise Figure (0.4-0.8GHz)']
            xlim_set = [[0,1], [0,6], [0.4,0.8]]
            ylim_set = [[0,1.4]]
            for x in range(len(title)):
                plot_nf_meas_and_sim(meas_nf_filenames, sim_nf_filenames, cal_nf_filenames, plt_label, title[x], minicircuit_component, xmin, xmax, ymin, ymax, xlim_set[x], ylim_set[0], dir_length)
            if (xlim is not None) or (ylim is not None) or (xmin is not None) or (xmax is not None) or (ymin is not None) or (ymax is not None):
                title = 'Noise Figure'
                plot_nf_meas_and_sim(meas_nf_filenames, sim_nf_filenames, cal_nf_filenames, plt_label, title, minicircuit_component, xmin, xmax, ymin, ymax, xlim, ylim, dir_length)
            plot_nfgain_no_sim(meas_nf_filenames, cal_nf_filenames, plt_label, minicircuit_component, gain_xlim, gain_ylim, dir_length)