import numpy as np
import matplotlib.pyplot as plt
import glob
import skrf.plotting as skplt
import skrf as rf
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-label', '--plt_label', nargs = '+', action = 'store', type = str, default = None, help = 'Labels for the plot legend. List them without quotes or parentheses and do not separate them with commas. The files are read in alphabetically, so put these in the same order the files will be read, e.g. -label label1 label2 label3. If you set this to auto (e.g. -label auto) than the plots will be labeled with the filenames')
parser.add_argument('-f', '--filename', action = 'store', type = str , default = '~/Desktop', help = 'The directory that the files are located. This is also the directory the files will be saved.')
parser.add_argument('-freq', '--set_freq', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum x values that are plotted. List them without quotes or parentheses and do not separate them with commas, e.g. -freq 400000000 800000000')
parser.add_argument('-db', '--set_db_scale', nargs = '+', action = 'store', type = float, default = None, help = 'Sets the minimum and maximum x values that are plotted. List them without quotes or parentheses and do not separate them with commas, e.g. -db -20 20')
args = parser.parse_args()


def plot_file(filename):
    n = rf.Network(filename)
    n.plot_s_db()




#-----------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    plt_label = args.plt_label
    freq_lim = args.set_freq
    db_lim = args.set_db_scale
    print(freq_lim)
    print(db_lim)
    meas_filename = args.filename
    plot_file(meas_filename)
    if freq_lim:
        plt.xlim(freq_lim[0], freq_lim[1])
    if db_lim:
        plt.ylim(db_lim[0], db_lim[1])
    plt.savefig( meas_filename+'.pdf' )