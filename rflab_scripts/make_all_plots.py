import numpy as np
import matplotlib.pyplot as plt
import antpy
import pylab as plb
import numpy as npy
import glob
import sys
from matplotlib.patches import Circle   # for drawing smith chart
from matplotlib.pyplot import quiver
from matplotlib import rcParams
#from matplotlib.lines import Line2D            # for drawing smith chart

#dir = sys.argv[0]
#sparam_filenames = glob.glob('/Users/brittanyjohnstone/Desktop/Research/Kevin/WVU/' + dir + '/*L.txt')




#ALWAYS SAVE THE VNA DATA FROM 2 MHZ TO 6 GHZ WITH 1000 DATA POINT RESOLUTION SO THAT THE INDEXES FOR 400-800 MHZ ARE ALWAYS THE SAME
#READ LOGMAG DATA
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
                #if y >= 0 :
                logmag_data.append(row.split())
                y += 1
                #else :
                #   y += 1
            file_len.append(int(y))
            x += 1
    tot_file_len = sum(file_len)
    m = 0
    freq = []
    S11 = []
    S21 = []
    S12 = []
    S22 = []
    for m in range(tot_file_len):
        freq.append(float(logmag_data[m][0]))
        S11.append(float(logmag_data[m][1]))
        S21.append(float(logmag_data[m][3]))
        S12.append(float(logmag_data[m][5]))
        S22.append(float(logmag_data[m][7]))
        m += 1
        #while m < tot_file_len :
        #freq.append(float(logmag_data[m + 13][0]))
        #S11.append(float(logmag_data[m + 13][1]))
        #S21.append(float(logmag_data[m + 13][3]))
        #S12.append(float(logmag_data[m + 13][5]))
        #S22.append(float(logmag_data[m + 13][7]))
#m += 1
    freq_nparray = np.array(freq)
    S11_nparray = np.array(S11)
    S21_nparray = np.array(S21)
    S12_nparray = np.array(S12)
    S22_nparray = np.array(S22)
    return(freq_nparray, freq, S11_nparray, S21_nparray, S12_nparray, S22_nparray, logmag_data_name_array, file_len, tot_file_len)

#READ SMITH DATA
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
                #   if y >= 0 :
                smith_data.append(row.split())
                y += 1
            #   else :
        #y += 1
            file_len.append(int(y))
            x += 1
    tot_file_len = sum(file_len)
    m = 0
    freq = []
    S11 = []
    S21 = []
    S12 = []
    S22 = []
    while m < tot_file_len : #for m in range(tot_file_len):
        freq.append(float(smith_data[m][0]))
        S11.append(complex(float(smith_data[m][1]), float(smith_data[m][2])))
        S21.append(complex(float(smith_data[m][3]), float(smith_data[m][4])))
        S12.append(complex(float(smith_data[m][5]), float(smith_data[m][6])))
        S22.append(complex(float(smith_data[m][7]), float(smith_data[m][8])))
        m += 1
    freq_nparray = np.array(freq)
    S11_nparray = np.array(S11)
    S21_nparray = np.array(S21)
    S12_nparray = np.array(S12)
    S22_nparray = np.array(S22)
    return (freq_nparray, S11_nparray, S21_nparray, S12_nparray, S22_nparray, file_len)

#READ MEASURED NOISE FIGURE DATA
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


#-----------------------------------------------------------------------------------------------------------------

#PLOT_RECTANGULAR, PLOT_COMPLEX_RECTANGULAR, SMITH, PLOT_SMITH & SAVE_ALL_FIGS IS FROM SKRF
def plot_rectangular(x, y, x_label=None, y_label=None, title=None,
                     show_legend=True, axis='tight', ax=None, limits= None, ylim = None, *args, **kwargs):
    '''
    plots rectangular data and optionally label axes.
        
    Parameters
    ------------
    z : array-like, of complex data
        data to plot
    x_label : string
        x-axis label
    y_label : string
        y-axis label
    title : string
        plot title
    show_legend : Boolean
        controls the drawing of the legend
    ax : :class:`matplotlib.axes.AxesSubplot` object
        axes to draw on
    *args,**kwargs : passed to pylab.plot
        
        '''
    if ax is None:
        ax = plb.gca()
    
    my_plot = ax.plot(x, y, *args, **kwargs)

    if x_label is not None:
        ax.set_xlabel(x_label)
    
    if y_label is not None:
        ax.set_ylabel(y_label)

    if title is not None:
        ax.set_title(title)

    if show_legend:
        # only show legend if they provide a label
        if 'label' in kwargs:
            ax.legend()
    if 'grid' in kwargs :
        ax.grid()
    
    if axis is not None:
        ax.autoscale(True, 'x', True)
        ax.autoscale(True, 'y', False)
    else :
        ax.axis([xmin, xmax, ymin, ymax])

    if limits is not None:
        ax.set_xlim([limits[0], limits[1]])
    if ylim is not None:
        ax.set_ylim([ylim[0], ylim[1]])
    if plb.isinteractive():
        plb.draw()

    return my_plot


def plot_complex_rectangular(z, x_label='Real', y_label='Imag',
                             title=None, show_legend=True, axis='equal', ax=None,
                             *args, **kwargs):
    '''
        plot complex data on the complex plane
        
        Parameters
        ------------
        z : array-like, of complex data
        data to plot
        x_label : string
        x-axis label
        y_label : string
        y-axis label
        title : string
        plot title
        show_legend : Boolean
        controls the drawing of the legend
        ax : :class:`matplotlib.axes.AxesSubplot` object
        axes to draw on
        *args,**kwargs : passed to pylab.plot
        
        See Also
        ----------
        plot_rectangular : plots rectangular data
        plot_complex_rectangular : plot complex data on complex plane
        plot_polar : plot polar data
        plot_complex_polar : plot complex data on polar plane
        plot_smith : plot complex data on smith chart
        
        '''
    x = npy.real(z)
    y = npy.imag(z)
    plot_rectangular(x=x, y=y, x_label=x_label, y_label=y_label,
        title=title, show_legend=show_legend, axis=axis,
        ax=ax, *args, **kwargs)


def smith(smithR=1, chart_type = 'z', draw_labels = False, border=False,
          ax=None):
    '''
        plots the smith chart of a given radius
        
        Parameters
        -----------
        smithR : number
        radius of smith chart
        chart_type : ['z','y']
        Contour type. Possible values are
        * *'z'* : lines of constant impedance
        * *'y'* : lines of constant admittance
        draw_labels : Boolean
        annotate real and imaginary parts of impedance on the
        chart (only if smithR=1)
        border : Boolean
        draw a rectangular border with axis ticks, around the perimeter
        of the figure. Not used if draw_labels = True
        
        ax : matplotlib.axes object
        existing axes to draw smith chart on
        
        
        '''
    ##TODO: fix this function so it doesnt suck
    if ax == None:
        ax1 = plb.gca()
    else:
        ax1 = ax
    
    # contour holds matplotlib instances of: pathes.Circle, and lines.Line2D, which
    # are the contours on the smith chart
    contour = []

    # these are hard-coded on purpose,as they should always be present
    rHeavyList = [0,1]
    xHeavyList = [1,-1]
    
    #TODO: fix this
    # these could be dynamically coded in the future, but work good'nuff for now
    if not draw_labels:
        rLightList = plb.logspace(3,-5,9,base=.5)
        xLightList = plb.hstack([plb.logspace(2,-5,8,base=.5), -1*plb.logspace(2,-5,8,base=.5)])
    else:
        rLightList = plb.array( [ 0.2, 0.5, 1.0, 2.0, 5.0 ] )
        xLightList = plb.array( [ 0.2, 0.5, 1.0, 2.0 , 5.0, -0.2, -0.5, -1.0, -2.0, -5.0 ] )
    
    # cheap way to make a ok-looking smith chart at larger than 1 radii
    if smithR > 1:
        rMax = (1.+smithR)/(1.-smithR)
        rLightList = plb.hstack([ plb.linspace(0,rMax,11)  , rLightList ])

    if chart_type is 'y':
        y_flip_sign = -1
    else:
        y_flip_sign = 1
    # loops through Light and Heavy lists and draws circles using patches
    # for analysis of this see R.M. Weikles Microwave II notes (from uva)
    for r in rLightList:
        center = (r/(1.+r)*y_flip_sign,0 )
        radius = 1./(1+r)
        contour.append( Circle( center, radius, ec='grey',fc = 'none'))
    for x in xLightList:
        center = (1*y_flip_sign,1./x)
        radius = 1./x
        contour.append( Circle( center, radius, ec='grey',fc = 'none'))

    for r in rHeavyList:
        center = (r/(1.+r)*y_flip_sign,0 )
        radius = 1./(1+r)
        contour.append( Circle( center, radius, ec= 'black', fc = 'none'))
    for x in xHeavyList:
        center = (1*y_flip_sign,1./x)
        radius = 1./x
        contour.append( Circle( center, radius, ec='black',fc = 'none'))

    # clipping circle
    clipc = Circle( [0,0], smithR, ec='k',fc='None',visible=True)
    ax1.add_patch( clipc)
    
    #draw x and y axis
    ax1.axhline(0, color='k', lw=.1, clip_path=clipc)
    ax1.axvline(1*y_flip_sign, color='k', clip_path=clipc)
    ax1.grid(0)
    #set axis limits
    ax1.axis('equal')
    ax1.axis(smithR*npy.array([-1.1, 1.1, -1.1, 1.1]))
    
    
    if not border:
        ax1.yaxis.set_ticks([])
        ax1.xaxis.set_ticks([])
        for loc, spine in ax1.spines.items():
            spine.set_color('none')


    if draw_labels:
        #Clear axis
        ax1.yaxis.set_ticks([])
        ax1.xaxis.set_ticks([])
        for loc, spine in ax1.spines.items():
            spine.set_color('none')

        #Will make annotations only if the radius is 1 and it is the impedance smith chart
        if smithR is 1 and y_flip_sign is 1:
            #Make room for annotation
            ax1.axis(smithR*npy.array([-1., 1., -1.2, 1.2]))
            
            #Annotate real part
            for value in rLightList:
                rho = (value - 1)/(value + 1)
                ax1.annotate(str(value), xy=((rho-0.12)*smithR, 0.01*smithR), \
                             xytext=((rho-0.12)*smithR, 0.01*smithR))
            
            #Annotate imaginary part
            deltax = plb.array([-0.17, -0.14, -0.06,  0., 0.02, -0.2, -0.2, -0.08, 0., 0.03])
            deltay = plb.array([0., 0.03, 0.01, 0.02, 0., -0.02, -0.06, -0.09, -0.08, -0.05])
            for value, dx, dy in zip(xLightList, deltax, deltay):
                #Transforms from complex to cartesian and adds a delta to x and y values
                rhox = (-value**2 + 1)/(-value**2 - 1) * smithR * y_flip_sign + dx
                rhoy = (-2*value)/(-value**2 - 1) * smithR + dy
                #Annotate value
                ax1.annotate(str(value) + 'j', xy=(rhox, rhoy), xytext=(rhox, rhoy))
            
            #Annotate 0 and inf
            ax1.annotate('0.0', xy=(-1.15, -0.02), xytext=(-1.15, -0.02))
            ax1.annotate('$\infty$', xy=(1.02, -0.02), xytext=(1.02, -0.02))

    # loop though contours and draw them on the given axes
    for currentContour in contour:
        cc=ax1.add_patch(currentContour)
        cc.set_clip_path(clipc)


def plot_smith(s, smith_r=1, chart_type='z', x_label='Real',
               y_label='Imaginary', title=None, show_legend=True,
               axis='equal', ax=None, force_chart = False, *args, **kwargs):
    '''
        plot complex data on smith chart
        
        Parameters
        ------------
        s : complex array-like
        reflection-coeffient-like data to plot
        smith_r : number
        radius of smith chart
        chart_type : ['z','y']
        Contour type for chart.
        * *'z'* : lines of constant impedance
        * *'y'* : lines of constant admittance
        x_label : string
        x-axis label
        y_label : string
        y-axis label
        title : string
        plot title
        show_legend : Boolean
        controls the drawing of the legend
        axis_equal: Boolean
        sets axis to be equal increments (calls axis('equal'))
        force_chart : Boolean
        forces the re-drawing of smith chart
        ax : :class:`matplotlib.axes.AxesSubplot` object
        axes to draw on
        *args,**kwargs : passed to pylab.plot
        
        See Also
        ----------
        plot_rectangular : plots rectangular data
        plot_complex_rectangular : plot complex data on complex plane
        plot_polar : plot polar data
        plot_complex_polar : plot complex data on polar plane
        plot_smith : plot complex data on smith chart
        '''
    
    if ax is None:
        ax = plb.gca()
    
    # test if smith chart is already drawn
    if not force_chart:
        if len(ax.patches) == 0:
            smith(ax=ax, smithR = smith_r, chart_type=chart_type)

    plot_complex_rectangular(s, x_label=x_label, y_label=y_label,
        title=title, show_legend=show_legend, axis=axis,
        ax=ax, *args, **kwargs)
    
    ax.axis(smith_r*npy.array([-1.1, 1.1, -1.1, 1.1]))
    if plb.isinteractive():
        plb.draw()

def save_all_figs(dir = './', format=None, replace_spaces = True, echo = True):
    '''
    Save all open Figures to disk.
        
    Parameters
    ------------
    dir : string
        path to save figures into
    format : None, or list of strings
        the types of formats to save figures as. The elements of this
        list are passed to :matplotlib:`savefig`. This is a list so that
        you can save each figure in multiple formats.
    echo : bool
        True prints filenames as they are saved
    '''
    if dir[-1] != '/':
        dir = dir + '/'
    for fignum in plb.get_fignums():
        fileName = plb.figure(fignum).get_axes()[0].get_title()
        if replace_spaces:
            fileName = fileName.replace(' ','_')
        if fileName == '':
            fileName = 'unnamedPlot'
        if format is None:
            plb.savefig(dir+fileName)
            if echo:
                print((dir+fileName))
        else:
            for fmt in format:
                plb.savefig(dir+fileName+'.'+fmt, format=fmt)
                if echo:
                    print((dir+fileName+'.'+fmt))
saf = save_all_figs

#-----------------------------------------------------------------------------------------------------------------

#LOGMAG PLOTS WITHOUT SIMULATED DATA

#plot S11
def plt_s11_logmag_mult(sparam_filenames, my_label, title, s11_ylim, dir):#, limits) :
    freq_nparray, freq, S11, S21, S12, S22, logmag_data_name_array, file_len, tot_file_len = read_logmag_data_from_mult_files(sparam_filenames)
    if s11_ylim is not None:
        ylim = [s11_ylim[0], s11_ylim[1]]
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_rectangular(freq_nparray[x:file_len[x]]/1e9, S11[x:file_len[x]], x_label = 'Frequency (GHz)', y_label = 'S21 (dB)', title = title, ylim = ylim, label = my_label[x])
            x += 1
        else :
            plot_rectangular(freq_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])]/1e9, S11[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], x_label = 'Frequency (GHz)', y_label = 'S11 (dB)', title = title, ylim = ylim, label = my_label[x])
            x += 1
    save_all_figs( dir = dir, format = ['pdf', 'jpeg'])
    plb.clf()

#plot S21
def plt_s21_logmag_mult(sparam_filenames, my_label, title, s21_ylim, dir):#, limits) :
    freq_nparray, freq, S11, S21, S12, S22, logmag_data_name_array, file_len, tot_file_len = read_logmag_data_from_mult_files(sparam_filenames)
    if s21_ylim is not None:
        ylim = [s21_ylim[0], s21_ylim[1]]
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_rectangular(freq_nparray[x:file_len[x]]/1e9, S21[x:file_len[x]], x_label = 'Frequency (GHz)', y_label = 'S21 (dB)', title = title, ylim = ylim, label = my_label[x])
            x += 1
        else :
            plot_rectangular(freq_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])]/1e9, S21[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], x_label = 'Frequency (GHz)', y_label = 'S21 (dB)', title = title, ylim = ylim, label = my_label[x])
            x += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()

#plot S12
def plt_s12_logmag_mult(sparam_filenames, my_label, title, s12_ylim, dir):#, limits) :
    freq_nparray, freq, S11, S21, S12, S22, logmag_data_name_array, file_len, tot_file_len = read_logmag_data_from_mult_files(sparam_filenames)
    if s12_ylim is not None:
        ylim = [s12_ylim[0], s12_ylim[1]]
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_rectangular(freq_nparray[x:file_len[x]]/1e9, S12[x:file_len[x]], x_label = 'Frequency (GHz)', y_label = 'S12 (dB)', title = title, ylim = ylim, label = my_label[x])
            x += 1
        else :
            plot_rectangular(freq_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])]/1e9, S12[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], x_label = 'Frequency (GHz)', y_label = 'S12 (dB)', title = title, ylim = ylim, label = my_label[x])
            x += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()

#plot S22
def plt_s22_logmag_mult(sparam_filenames, my_label, title, s22_ylim, dir):#, limits) :
    freq_nparray, freq, S11, S21, S12, S22, logmag_data_name_array, file_len, tot_file_len = read_logmag_data_from_mult_files(sparam_filenames)
    if s22_ylim is not None:
        ylim = [s22_ylim[0], s22_ylim[1]]
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_rectangular(freq_nparray[x:file_len[x]]/1e9, S22[x:file_len[x]], x_label = 'Frequency (GHz)', y_label = 'S22 (dB)', title = title, ylim = ylim, label = my_label[x])
            x += 1
        else :
            plot_rectangular(freq_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])]/1e9, S22[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], x_label = 'Frequency (GHz)', y_label = 'S22 (dB)', title = title, ylim = ylim, label = my_label[x])
            x += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()


#plot S11, S21, S12 & S22
def plt_logmag_mult(logmag_filenames, my_label, s11_ylim, s21_ylim, s12_ylim, s22_ylim, dir) :
    title = ['S11 Logmag', 'S21 Logmag', 'S12 Logmag', 'S22 Logmag']
    plt_s11_logmag_mult(logmag_filenames, my_label, title[0], s11_ylim, dir)
    plb.clf()
    plt_s21_logmag_mult(logmag_filenames, my_label, title[1], s21_ylim, dir)
    plb.clf()
    plt_s12_logmag_mult(logmag_filenames, my_label, title[2], s12_ylim, dir)
    plb.clf()
    plt_s22_logmag_mult(logmag_filenames, my_label, title[3], s22_ylim, dir)
    plb.clf()


#-----------------------------------------------------------------------------------------------------------------

#LOGMAG PLOTS WITH SIMULATED DATA

#plot S11
def plt_s11_logmag_meas_sim_mult(sparam_filenames, sim_sparam_filenames, my_label, title, s11_ylim, dir):#, limits) :
    freq_nparray, freq, S11, S21, S12, S22, logmag_data_name_array, file_len, tot_file_len = read_logmag_data_from_mult_files(sparam_filenames)
    sim_freq_nparray, sim_freq, sim_S11, sim_S21, sim_S12, sim_S22, sim_logmag_data_name_array, sim_file_len, sim_tot_file_len = read_logmag_data_from_mult_files(sim_sparam_filenames)
    if s11_ylim is not None:
        ylim = [s11_ylim[0], s11_ylim[1]]
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_rectangular(freq_nparray[x:file_len[x]]/1e9, S11[x:file_len[x]], x_label = 'Frequency (GHz)', y_label = 'S11 (dB)', title = title, ylim = ylim, label = my_label[x])
            x += 1
        else :
            plot_rectangular(freq_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])]/1e9 , S11[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], x_label = 'Frequency (GHz)', y_label = 'S11 (dB)', title = title, ylim = ylim, label = my_label[x])
            x += 1
    y = 0
    while y < len(sim_file_len) :
        if y == 0:
            plot_rectangular(sim_freq_nparray[y:sim_file_len[y]]/1e9, sim_S11[y:sim_file_len[y]], x_label = 'Frequency (GHz)', y_label = 'S11 (dB)', title = title, ylim = ylim, label = my_label[x])
            y += 1
            x += 1
        else :
            plot_rectangular(sim_freq_nparray[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])]/1e9 , sim_S11[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])], x_label = 'Frequency (GHz)', y_label = 'S11 (dB)', title = title, ylim = ylim, label = my_label[x])
            y += 1
            x += 1
    save_all_figs(dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()

#plot S21
def plt_s21_logmag_meas_sim_mult(sparam_filenames, sim_sparam_filenames, my_label, title, s21_ylim, dir):#, limits) :
    freq_nparray, freq, S11, S21, S12, S22, logmag_data_name_array, file_len, tot_file_len = read_logmag_data_from_mult_files(sparam_filenames)
    sim_freq_nparray, sim_freq, sim_S11, sim_S21, sim_S12, sim_S22, sim_logmag_data_name_array, sim_file_len, sim_tot_file_len = read_logmag_data_from_mult_files(sim_sparam_filenames)
    if s21_ylim is not None:
        ylim = [s21_ylim[0], s21_ylim[1]]
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_rectangular(freq_nparray[x:file_len[x]]/1e9, S21[x:file_len[x]], x_label = 'Frequency (GHz)', y_label = 'S21 (dB)', title = title, ylim = ylim, label = my_label[x])
            x += 1
        else :
            plot_rectangular(freq_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])]/1e9 , S21[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], x_label = 'Frequency (GHz)', y_label = 'S21 (dB)', title = title, ylim = ylim, label = my_label[x])
            x += 1
    y = 0
    while y < len(sim_file_len) :
        if y == 0:
            plot_rectangular(sim_freq_nparray[y:sim_file_len[y]]/1e9, sim_S21[y:sim_file_len[y]], x_label = 'Frequency (GHz)', y_label = 'S21 (dB)', title = title, ylim = ylim, label = my_label[x])
            y += 1
            x += 1
        else :
            plot_rectangular(sim_freq_nparray[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])]/1e9 , sim_S21[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])], x_label = 'Frequency (GHz)', y_label = 'S21 (dB)', title = title, ylim = ylim, label = my_label[x])
            y += 1
            x += 1
    save_all_figs(dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()

#plot S12
def plt_s12_logmag_meas_sim_mult(sparam_filenames, sim_sparam_filenames, my_label, title, s12_ylim, dir):#, limits) :
    freq_nparray, freq, S11, S21, S12, S22, logmag_data_name_array, file_len, tot_file_len = read_logmag_data_from_mult_files(sparam_filenames)
    sim_freq_nparray, sim_freq, sim_S11, sim_S21, sim_S12, sim_S22, sim_logmag_data_name_array, sim_file_len, sim_tot_file_len = read_logmag_data_from_mult_files(sim_sparam_filenames)
    if s12_ylim is not None:
        ylim = [s12_ylim[0], s12_ylim[1]]
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_rectangular(freq_nparray[x:file_len[x]]/1e9, S12[x:file_len[x]], x_label = 'Frequency (GHz)', y_label = 'S12 (dB)', title = title, ylim = ylim, label = my_label[x])
            x += 1
        else :
            plot_rectangular(freq_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])]/1e9 , S12[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], x_label = 'Frequency (GHz)', y_label = 'S12 (dB)', title = title, ylim = ylim, label = my_label[x])
            x += 1
    y = 0
    while y < len(sim_file_len) :
        if y == 0:
            plot_rectangular(sim_freq_nparray[y:sim_file_len[y]]/1e9, sim_S12[y:sim_file_len[y]], x_label = 'Frequency (GHz)', y_label = 'S12 (dB)', title = title, ylim = ylim, label = my_label[x])
            y += 1
            x += 1
        else :
            plot_rectangular(sim_freq_nparray[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])]/1e9 , sim_S12[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])], x_label = 'Frequency (GHz)', y_label = 'S12 (dB)', title = title, ylim = ylim, label = my_label[x])
            y += 1
            x += 1
    save_all_figs(dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()

#plot S22
def plt_s22_logmag_meas_sim_mult(sparam_filenames, sim_sparam_filenames, my_label, title, s22_ylim, dir):#, limits) :
    freq_nparray, freq, S11, S21, S12, S22, logmag_data_name_array, file_len, tot_file_len = read_logmag_data_from_mult_files(sparam_filenames)
    sim_freq_nparray, sim_freq, sim_S11, sim_S21, sim_S12, sim_S22, sim_logmag_data_name_array, sim_file_len, sim_tot_file_len = read_logmag_data_from_mult_files(sim_sparam_filenames)
    if s22_ylim is not None:
        ylim = [s22_ylim[0], s22_ylim[1]]
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_rectangular(freq_nparray[x:file_len[x]]/1e9, S22[x:file_len[x]], x_label = 'Frequency (GHz)', y_label = 'S22 (dB)', title = title, ylim = ylim, label = my_label[x])
            x += 1
        else :
            plot_rectangular(freq_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])]/1e9 , S22[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], x_label = 'Frequency (GHz)', y_label = 'S22 (dB)', title = title, ylim = ylim, label = my_label[x])
            x += 1
    y = 0
    while y < len(sim_file_len) :
        if y == 0:
            plot_rectangular(sim_freq_nparray[y:sim_file_len[y]]/1e9, sim_S22[y:sim_file_len[y]], x_label = 'Frequency (GHz)', y_label = 'S22 (dB)', title = title, ylim = ylim, label = my_label[x])
            y += 1
            x += 1
        else :
            plot_rectangular(sim_freq_nparray[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])]/1e9 , sim_S22[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])], x_label = 'Frequency (GHz)', y_label = 'S22 (dB)', title = title, ylim = ylim, label = my_label[x])
            y += 1
            x += 1
    save_all_figs(dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()


#plot S11, S21, S12 & S22
def plt_logmag_meas_sim_mult(logmag_filenames, sim_logmag_filenames, my_label, s11_ylim, s21_ylim, s12_ylim, s22_ylim, dir) :
    title = ['S11 Logmag Measured and Simulated', 'S21 Logmag Measured and Simulated', 'S12 Logmag Measured and Simulated', 'S22 Logmag Measured and Simulated']
    plt_s11_logmag_meas_sim_mult(logmag_filenames, sim_logmag_filenames, my_label, title[0], s11_ylim, dir)
    plb.clf()
    plt_s21_logmag_meas_sim_mult(logmag_filenames, sim_logmag_filenames, my_label, title[1], s21_ylim, dir)
    plb.clf()
    plt_s12_logmag_meas_sim_mult(logmag_filenames, sim_logmag_filenames, my_label, title[2], s12_ylim, dir)
    plb.clf()
    plt_s22_logmag_meas_sim_mult(logmag_filenames, sim_logmag_filenames, my_label, title[3], s22_ylim, dir)
    plb.clf()


#-----------------------------------------------------------------------------------------------------------------

#LOGMAG PLOTS WITH SIMULATED DATA (400-800MHz)

#plot S11
def plt_s11_logmag_meas_sim_mult_freq_range(sparam_filenames, sim_sparam_filenames, my_label, title, limits, s11_ylim, dir) :
    freq_nparray, freq, S11, S21, S12, S22, logmag_data_name_array, file_len, tot_file_len = read_logmag_data_from_mult_files(sparam_filenames)
    sim_freq_nparray, sim_freq, sim_S11, sim_S21, sim_S12, sim_S22, sim_logmag_data_name_array, sim_file_len, sim_tot_file_len = read_logmag_data_from_mult_files(sim_sparam_filenames)
    if s11_ylim is not None:
        ylim = [s11_ylim[0], s11_ylim[1]]
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_rectangular(freq_nparray[x:file_len[x]]/1e6, S11[x:file_len[x]], x_label = 'Frequency (MHz)', y_label = 'S11 (dB)', title = title, limits = limits, ylim = ylim, label = my_label[x])
            x += 1
        else :
            plot_rectangular(freq_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])]/1e6 , S11[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], x_label = 'Frequency (MHz)', y_label = 'S11 (dB)', title = title, limits = limits, ylim = ylim, label = my_label[x])
            x += 1
    y = 0
    while y < len(sim_file_len) :
        if y == 0:
            plot_rectangular(sim_freq_nparray[y:sim_file_len[y]]/1e6, sim_S11[y:sim_file_len[y]], x_label = 'Frequency (MHz)', y_label = 'S11 (dB)', title = title, limits = limits, ylim = ylim, label = my_label[x])
            y += 1
            x += 1
        else :
            plot_rectangular(sim_freq_nparray[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])]/1e6 , sim_S11[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])], x_label = 'Frequency (MHz)', y_label = 'S11 (dB)', title = title, limits = limits, ylim = ylim, label = my_label[x])
            y += 1
            x += 1
    save_all_figs(dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()

#plot S21
def plt_s21_logmag_meas_sim_mult_freq_range(sparam_filenames, sim_sparam_filenames, my_label, title, limits, s21_ylim, dir) :
    freq_nparray, freq, S11, S21, S12, S22, logmag_data_name_array, file_len, tot_file_len = read_logmag_data_from_mult_files(sparam_filenames)
    sim_freq_nparray, sim_freq, sim_S11, sim_S21, sim_S12, sim_S22, sim_logmag_data_name_array, sim_file_len, sim_tot_file_len = read_logmag_data_from_mult_files(sim_sparam_filenames)
    if s21_ylim is not None:
        ylim = [s21_ylim[0], s21_ylim[1]]
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_rectangular(freq_nparray[x:file_len[x]]/1e6, S21[x:file_len[x]], x_label = 'Frequency (MHz)', y_label = 'S21 (dB)', title = title, limits = limits, ylim = s21_ylim, label = my_label[x])
            x += 1
        else :
            plot_rectangular(freq_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])]/1e6 , S21[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], x_label = 'Frequency (MHz)', y_label = 'S21 (dB)', title = title, limits = limits, ylim = s21_ylim, label = my_label[x])
            x += 1
    y = 0
    while y < len(sim_file_len) :
        if y == 0:
            plot_rectangular(sim_freq_nparray[y:sim_file_len[y]]/1e6, sim_S21[y:sim_file_len[y]], x_label = 'Frequency (MHz)', y_label = 'S21 (dB)', title = title, limits = limits, ylim = s21_ylim, label = my_label[x])
            y += 1
            x += 1
        else :
            plot_rectangular(sim_freq_nparray[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])]/1e6 , sim_S21[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])], x_label = 'Frequency (MHz)', y_label = 'S21 (dB)', title = title, limits = limits, ylim = s21_ylim, label = my_label[x])
            y += 1
            x += 1
    save_all_figs(dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()

#plot S12
def plt_s12_logmag_meas_sim_mult_freq_range(sparam_filenames, sim_sparam_filenames, my_label, title, limits, s12_ylim, dir) :
    freq_nparray, freq, S11, S21, S12, S22, logmag_data_name_array, file_len, tot_file_len = read_logmag_data_from_mult_files(sparam_filenames)
    sim_freq_nparray, sim_freq, sim_S11, sim_S21, sim_S12, sim_S22, sim_logmag_data_name_array, sim_file_len, sim_tot_file_len = read_logmag_data_from_mult_files(sim_sparam_filenames)
    if s12_ylim is not None:
        ylim = [s12_ylim[0], s12_ylim[1]]
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_rectangular(freq_nparray[x:file_len[x]]/1e6, S12[x:file_len[x]], x_label = 'Frequency (MHz)', y_label = 'S12 (dB)', title = title, limits = limits, ylim = s12_ylim, label = my_label[x])
            x += 1
        else :
            plot_rectangular(freq_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])]/1e6 , S12[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], x_label = 'Frequency (MHz)', y_label = 'S12 (dB)', title = title, limits = limits, ylim = s12_ylim, label = my_label[x])
            x += 1
    y = 0
    while y < len(sim_file_len) :
        if y == 0:
            plot_rectangular(sim_freq_nparray[y:sim_file_len[y]]/1e6, sim_S12[y:sim_file_len[y]], x_label = 'Frequency (MHz)', y_label = 'S12 (dB)', title = title, limits = limits, ylim = s12_ylim, label = my_label[x])
            y += 1
            x += 1
        else :
            plot_rectangular(sim_freq_nparray[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])]/1e6 , sim_S12[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])], x_label = 'Frequency (MHz)', y_label = 'S12 (dB)', title = title, limits = limits, ylim = s12_ylim, label = my_label[x])
            y += 1
            x += 1
    save_all_figs(dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()

#plot S22
def plt_s22_logmag_meas_sim_mult_freq_range(sparam_filenames, sim_sparam_filenames, my_label, title, limits, s22_ylim, dir) :
    freq_nparray, freq, S11, S21, S12, S22, logmag_data_name_array, file_len, tot_file_len = read_logmag_data_from_mult_files(sparam_filenames)
    sim_freq_nparray, sim_freq, sim_S11, sim_S21, sim_S12, sim_S22, sim_logmag_data_name_array, sim_file_len, sim_tot_file_len = read_logmag_data_from_mult_files(sim_sparam_filenames)
    if s22_ylim is not None:
        ylim = [s22_ylim[0], s22_ylim[1]]
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_rectangular(freq_nparray[x:file_len[x]]/1e6, S22[x:file_len[x]], x_label = 'Frequency (MHz)', y_label = 'S22 (dB)', title = title, limits = limits, ylim = s22_ylim, label = my_label[x])
            x += 1
        else :
            plot_rectangular(freq_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])]/1e6 , S22[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], x_label = 'Frequency (MHz)', y_label = 'S22 (dB)', title = title, limits = limits, ylim = s22_ylim, label = my_label[x])
            x += 1
    y = 0
    while y < len(sim_file_len) :
        if y == 0:
            plot_rectangular(sim_freq_nparray[y:sim_file_len[y]]/1e6, sim_S22[y:sim_file_len[y]], x_label = 'Frequency (MHz)', y_label = 'S22 (dB)', title = title, limits = limits, ylim = s22_ylim, label = my_label[x])
            y += 1
            x += 1
        else :
            plot_rectangular(sim_freq_nparray[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])]/1e6 , sim_S22[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])], x_label = 'Frequency (MHz)', y_label = 'S22 (dB)', title = title, limits = limits, ylim = s22_ylim, label = my_label[x])
            y += 1
            x += 1
    save_all_figs(dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()


#plot S11, S21, S12 & S22
def plt_logmag_meas_sim_mult_freq_range(logmag_filenames, sim_logmag_filenames, my_label, limits, s11_ylim, s21_ylim, s12_ylim, s22_ylim, dir) :
    title = ['S11 Logmag Measured and Simulated (400-800MHz)', 'S21 Logmag Measured and Simulated (400-800MHz)', 'S12 Logmag Measured and Simulated(400-800MHz)', 'S22 Logmag Measured and Simulated(400-800MHz)']
    plt_s11_logmag_meas_sim_mult_freq_range(logmag_filenames, sim_logmag_filenames, my_label, title[0], limits, s11_ylim, dir)
    plb.clf()
    plt_s21_logmag_meas_sim_mult_freq_range(logmag_filenames, sim_logmag_filenames, my_label, title[1], limits, s21_ylim, dir)
    plb.clf()
    plt_s12_logmag_meas_sim_mult_freq_range(logmag_filenames, sim_logmag_filenames, my_label, title[2], limits, s12_ylim, dir)
    plb.clf()
    plt_s22_logmag_meas_sim_mult_freq_range(logmag_filenames, sim_logmag_filenames, my_label, title[3], limits, s22_ylim, dir)
    plb.clf()

#-----------------------------------------------------------------------------------------------------------------

#SMITH PLOTS
#plot S11
def plt_s11_smith_mult(smith_filenames, my_label, title, dir) :
    freq, S11_nparray, S21_nparray, S12_nparray, S22_nparray, file_len = read_smith_data_from_files(smith_filenames)
    tot_file_len = sum(file_len)
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_smith(S11_nparray[x:file_len[x]], title = title, label = my_label[x])
            x += 1
        else :
            plot_smith(S11_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], title = title, label = my_label[x])
            x += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()

#plot S21
def plt_s21_smith_mult(smith_filenames, my_label, title, dir) :
    freq, S11_nparray, S21_nparray, S12_nparray, S22_nparray, file_len = read_smith_data_from_files(smith_filenames)
    tot_file_len = sum(file_len)
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_smith(S21_nparray[x:file_len[x]], title = title, label = my_label[x])
            x += 1
        else :
            plot_smith(S21_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], title = title, label = my_label[x])
            x += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()

#plot S12
def plt_s12_smith_mult(smith_filenames, my_label, title, dir) :
    freq, S11_nparray, S21_nparray, S12_nparray, S22_nparray, file_len = read_smith_data_from_files(smith_filenames)
    tot_file_len = sum(file_len)
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_smith(S12_nparray[x:file_len[x]], title = title, label = my_label[x])
            x += 1
        else :
            plot_smith(S12_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], title = title, label = my_label[x])
            x += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()

#plot S22
def plt_s22_smith_mult(smith_filenames, my_label, title, dir) :
    freq, S11_nparray, S21_nparray, S12_nparray, S22_nparray, file_len = read_smith_data_from_files(smith_filenames)
    tot_file_len = sum(file_len)
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_smith(S22_nparray[x:file_len[x]], title = title, label = my_label[x])
            x += 1
        else :
            plot_smith(S22_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], title = title, label = my_label[x])
            x += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()

#plot S11, S21, S12 & S22
def plt_smith_mult(smith_filenames, my_label, dir) :
    title = ['S11 Smith', 'S21 Smith', 'S12 Smith', 'S22 Smith']
    plt_s11_smith_mult(smith_filenames, my_label, title[0], dir)
    plb.clf()
    plt_s21_smith_mult(smith_filenames, my_label, title[1], dir)
    plb.clf()
    plt_s12_smith_mult(smith_filenames, my_label, title[2], dir)
    plb.clf()
    plt_s22_smith_mult(smith_filenames, my_label, title[3], dir)
    plb.clf()


#-----------------------------------------------------------------------------------------------------------------

#SMITH PLOTS WITH MEASURED AND SIMULATED

#plot S11
def plt_s11_smith_meas_sim_mult(smith_filenames, sim_smith_filenames, my_label, title, dir) :
    freq, S11_nparray, S21_nparray, S12_nparray, S22_nparray, file_len = read_smith_data_from_files(smith_filenames)
    sim_freq, sim_S11_nparray, sim_S21_nparray, sim_S12_nparray, sim_S22_nparray, sim_file_len = read_smith_data_from_files(sim_smith_filenames)
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_smith(S11_nparray[x:file_len[x]], title = title, label = my_label[x])
            x += 1
        else :
            plot_smith(S11_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], title = title, label = my_label[x])
            x += 1
    y = 0
    while y < len(sim_file_len) :
        if y == 0:
            plot_smith(sim_S11_nparray[y:sim_file_len[y]], title = title, label = my_label[x])
            x += 1
            y += 1
        else :
            plot_smith(sim_S11_nparray[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])], title = title, label = my_label[x])
            x += 1
            y += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()

#plot S21
def plt_s21_smith_meas_sim_mult(smith_filenames, sim_smith_filenames, my_label, title, dir) :
    freq, S11_nparray, S21_nparray, S12_nparray, S22_nparray, file_len = read_smith_data_from_files(smith_filenames)
    sim_freq, sim_S11_nparray, sim_S21_nparray, sim_S12_nparray, sim_S22_nparray, sim_file_len = read_smith_data_from_files(sim_smith_filenames)
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_smith(S21_nparray[x:file_len[x]], title = title, label = my_label[x])
            x += 1
        else :
            plot_smith(S21_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], title = title, label = my_label[x])
            x += 1
    y = 0
    while y < len(sim_file_len) :
        if y == 0:
            plot_smith(sim_S21_nparray[y:sim_file_len[y]], title = title, label = my_label[x])
            x += 1
            y += 1
        else :
            plot_smith(sim_S21_nparray[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])], title = title, label = my_label[x])
            x += 1
            y += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()

#plot S12
def plt_s12_smith_meas_sim_mult(smith_filenames, sim_smith_filenames, my_label, title, dir) :
    freq, S11_nparray, S21_nparray, S12_nparray, S22_nparray, file_len = read_smith_data_from_files(smith_filenames)
    sim_freq, sim_S11_nparray, sim_S21_nparray, sim_S12_nparray, sim_S22_nparray, sim_file_len = read_smith_data_from_files(sim_smith_filenames)
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_smith(S12_nparray[x:file_len[x]], title = title, label = my_label[x])
            x += 1
        else :
            plot_smith(S12_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], title = title, label = my_label[x])
            x += 1
    y = 0
    while y < len(sim_file_len) :
        if y == 0:
            plot_smith(sim_S12_nparray[y:sim_file_len[y]], title = title, label = my_label[x])
            x += 1
            y += 1
        else :
            plot_smith(sim_S12_nparray[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])], title = title, label = my_label[x])
            x += 1
            y += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()

#plot S22
def plt_s22_smith_meas_sim_mult(smith_filenames, sim_smith_filenames, my_label, title, dir) :
    freq, S11_nparray, S21_nparray, S12_nparray, S22_nparray, file_len = read_smith_data_from_files(smith_filenames)
    sim_freq, sim_S11_nparray, sim_S21_nparray, sim_S12_nparray, sim_S22_nparray, sim_file_len = read_smith_data_from_files(sim_smith_filenames)
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_smith(S22_nparray[x:file_len[x]], title = title, label = my_label[x])
            x += 1
        else :
            plot_smith(S22_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], title = title, label = my_label[x])
            x += 1
    y = 0
    while y < len(sim_file_len) :
        if y == 0:
            plot_smith(sim_S22_nparray[y:sim_file_len[y]], title = title, label = my_label[x])
            x += 1
            y += 1
        else :
            plot_smith(sim_S22_nparray[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])], title = title, label = my_label[x])
            x += 1
            y += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()


#plot S11, S21, S12 & S22
def plt_smith_meas_sim_mult(smith_filenames, sim_smith_filenames, my_label, dir) :
    title = ['S11 Smith Measured and Simulated', 'S21 Smith Measured and Simulated', 'S12 Smith Measured and Simulated', 'S22 Smith Measured and Simulated']
    plt_s11_smith_meas_sim_mult(smith_filenames, sim_smith_filenames, my_label, title[0], dir)
    plt_s21_smith_meas_sim_mult(smith_filenames, sim_smith_filenames, my_label, title[1], dir)
    plt_s12_smith_meas_sim_mult(smith_filenames, sim_smith_filenames, my_label, title[2], dir)
    plt_s22_smith_meas_sim_mult(smith_filenames, sim_smith_filenames, my_label, title[3], dir)
    plb.clf()


#-----------------------------------------------------------------------------------------------------------------

#FUNCTION THAT JUST GRABS THE INDICES THAT ARE BETWEEN 400 & 800 MHz
def freq_400to800(freq_nparray):
    range = np.where((freq_nparray/1e6 >= 400) & (freq_nparray/1e6 <= 800))[0]
    return range

#SMITH PLOTS WITH MEASURED AND SIMULATED (400-800MHz)

#plot S11
def plt_s11_smith_meas_sim_mult_freq_range(smith_filenames, sim_smith_filenames, my_label, title, dir) :
    freq_nparray, S11_nparray, S21_nparray, S12_nparray, S22_nparray, file_len = read_smith_data_from_files(smith_filenames)
    sim_freq_nparray, sim_S11_nparray, sim_S21_nparray, sim_S12_nparray, sim_S22_nparray, sim_file_len = read_smith_data_from_files(sim_smith_filenames)
   
    meas_freq_range = freq_400to800(freq_nparray)
    sim_freq_range = freq_400to800(sim_freq_nparray)

    x = 0
    i = 0
    while x < len(file_len)-1 :
        for i in range(len(meas_freq_range)) :
            if i != 0 :
                if (meas_freq_range[i-1] != meas_freq_range[i]-1) or (i == len(meas_freq_range)-1):
                    if x == 0 :
                        if i != len(meas_freq_range)-1 :
                            plot_smith(S11_nparray[meas_freq_range[x]:meas_freq_range[i-1]], title = title, label = my_label[x])
                            x += 1
                            i += 1
                            y = i
                        else :
                            plot_smith(S11_nparray[meas_freq_range[x]:meas_freq_range[i]], title = title, label = my_label[x])
                            x += 1
                    else :
                        if i != len(meas_freq_range)-1 :
                            plot_smith(S11_nparray[meas_freq_range[y]:meas_freq_range[i-1]], title = title, label = my_label[x])
                            x += 1
                            i += 1
                            y = i
                        else :
                            plot_smith(S11_nparray[meas_freq_range[y]:meas_freq_range[i]], title = title, label = my_label[x])
                            x += 1
            else :
                i += 1

    z = 0
    i = 0
    y = 0
    for z in range(len(sim_file_len)) :
        for i in range(len(sim_freq_range)) :
            if i != 0 :
                if (sim_freq_range[i-1] != sim_freq_range[i]-1) or (i == len(sim_freq_range)-1):
                    if z == 0 :
                        if i != len(sim_freq_range)-1 :
                            plot_smith(sim_S11_nparray[sim_freq_range[z]:sim_freq_range[i-1]], title = title, label = my_label[x])
                            z += 1
                            i += 1
                            y = i
                            x += 1
                        else :
                            plot_smith(sim_S11_nparray[sim_freq_range[z]:sim_freq_range[i]], title = title, label = my_label[x])
                            x += 1
                    else :
                        if i != len(meas_freq_range)-1 :
                            plot_smith(sim_S11_nparray[sim_freq_range[y]:sim_freq_range[i-1]], title = title, label = my_label[x])
                            z += 1
                            i += 1
                            y = i
                            x += 1
                        else :
                            plot_smith(sim_S11_nparray[sim_freq_range[y]:sim_freq_range[i]], title = title, label = my_label[x])
                            x += 1
            else :
                i += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])


#plot S21
def plt_s21_smith_meas_sim_mult_freq_range(smith_filenames, sim_smith_filenames, my_label, title, dir) :
    freq_nparray, S11_nparray, S21_nparray, S12_nparray, S22_nparray, file_len = read_smith_data_from_files(smith_filenames)
    sim_freq_nparray, sim_S11_nparray, sim_S21_nparray, sim_S12_nparray, sim_S22_nparray, sim_file_len = read_smith_data_from_files(sim_smith_filenames)
    
    meas_freq_range = freq_400to800(freq_nparray)
    sim_freq_range = freq_400to800(sim_freq_nparray)
    
    x = 0
    i = 0
    while x < len(file_len)-1 :
        for i in range(len(meas_freq_range)) :
            if i != 0 :
                if (meas_freq_range[i-1] != meas_freq_range[i]-1) or (i == len(meas_freq_range)-1):
                    if x == 0 :
                        if i != len(meas_freq_range)-1 :
                            plot_smith(S21_nparray[meas_freq_range[x]:meas_freq_range[i-1]], title = title, label = my_label[x])
                            x += 1
                            i += 1
                            y = i
                        else :
                            plot_smith(S21_nparray[meas_freq_range[x]:meas_freq_range[i]], title = title, label = my_label[x])
                            x += 1
                    else :
                        if i != len(meas_freq_range)-1 :
                            plot_smith(S21_nparray[meas_freq_range[y]:meas_freq_range[i-1]], title = title, label = my_label[x])
                            x += 1
                            i += 1
                            y = i
                        else :
                            plot_smith(S21_nparray[meas_freq_range[y]:meas_freq_range[i]], title = title, label = my_label[x])
                            x += 1
            else :
                i += 1

    z = 0
    i = 0
    y = 0
    for z in range(len(sim_file_len)) :
        for i in range(len(sim_freq_range)) :
            if i != 0 :
                if (sim_freq_range[i-1] != sim_freq_range[i]-1) or (i == len(sim_freq_range)-1):
                    if z == 0 :
                        if i != len(sim_freq_range)-1 :
                            plot_smith(sim_S21_nparray[sim_freq_range[z]:sim_freq_range[i-1]], title = title, label = my_label[x])
                            z += 1
                            i += 1
                            y = i
                            x += 1
                        else :
                            plot_smith(sim_S21_nparray[sim_freq_range[z]:sim_freq_range[i]], title = title, label = my_label[x])
                            x += 1
                    else :
                        if i != len(meas_freq_range)-1 :
                            plot_smith(sim_S21_nparray[sim_freq_range[y]:sim_freq_range[i-1]], title = title, label = my_label[x])
                            z += 1
                            i += 1
                            y = i
                            x += 1
                        else :
                            plot_smith(sim_S21_nparray[sim_freq_range[y]:sim_freq_range[i]], title = title, label = my_label[x])
                            x += 1
            else :
                i += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])


#plot S12
def plt_s12_smith_meas_sim_mult_freq_range(smith_filenames, sim_smith_filenames, my_label, title, dir) :
    freq_nparray, S11_nparray, S21_nparray, S12_nparray, S22_nparray, file_len = read_smith_data_from_files(smith_filenames)
    sim_freq_nparray, sim_S11_nparray, sim_S21_nparray, sim_S12_nparray, sim_S22_nparray, sim_file_len = read_smith_data_from_files(sim_smith_filenames)
    
    meas_freq_range = freq_400to800(freq_nparray)
    sim_freq_range = freq_400to800(sim_freq_nparray)
    
    x = 0
    i = 0
    while x < len(file_len)-1 :
        for i in range(len(meas_freq_range)) :
            if i != 0 :
                if (meas_freq_range[i-1] != meas_freq_range[i]-1) or (i == len(meas_freq_range)-1):
                    if x == 0 :
                        if i != len(meas_freq_range)-1 :
                            plot_smith(S12_nparray[meas_freq_range[x]:meas_freq_range[i-1]], title = title, label = my_label[x])
                            x += 1
                            i += 1
                            y = i
                        else :
                            plot_smith(S12_nparray[meas_freq_range[x]:meas_freq_range[i]], title = title, label = my_label[x])
                            x += 1
                    else :
                        if i != len(meas_freq_range)-1 :
                            plot_smith(S12_nparray[meas_freq_range[y]:meas_freq_range[i-1]], title = title, label = my_label[x])
                            x += 1
                            i += 1
                            y = i
                        else :
                            plot_smith(S12_nparray[meas_freq_range[y]:meas_freq_range[i]], title = title, label = my_label[x])
                            x += 1
            else :
                i += 1

    z = 0
    i = 0
    y = 0
    for z in range(len(sim_file_len)) :
        for i in range(len(sim_freq_range)) :
            if i != 0 :
                if (sim_freq_range[i-1] != sim_freq_range[i]-1) or (i == len(sim_freq_range)-1):
                    if z == 0 :
                        if i != len(sim_freq_range)-1 :
                            plot_smith(sim_S12_nparray[sim_freq_range[z]:sim_freq_range[i-1]], title = title, label = my_label[x])
                            z += 1
                            i += 1
                            y = i
                            x += 1
                        else :
                            plot_smith(sim_S12_nparray[sim_freq_range[z]:sim_freq_range[i]], title = title, label = my_label[x])
                            x += 1
                    else :
                        if i != len(meas_freq_range)-1 :
                            plot_smith(sim_S12_nparray[sim_freq_range[y]:sim_freq_range[i-1]], title = title, label = my_label[x])
                            z += 1
                            i += 1
                            y = i
                            x += 1
                        else :
                            plot_smith(sim_S12_nparray[sim_freq_range[y]:sim_freq_range[i]], title = title, label = my_label[x])
                            x += 1
            else :
                i += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])


#plot S22
def plt_s22_smith_meas_sim_mult_freq_range(smith_filenames, sim_smith_filenames, my_label, title, dir) :
    freq_nparray, S11_nparray, S21_nparray, S12_nparray, S22_nparray, file_len = read_smith_data_from_files(smith_filenames)
    sim_freq_nparray, sim_S11_nparray, sim_S21_nparray, sim_S12_nparray, sim_S22_nparray, sim_file_len = read_smith_data_from_files(sim_smith_filenames)
    
    meas_freq_range = freq_400to800(freq_nparray)
    sim_freq_range = freq_400to800(sim_freq_nparray)
    
    x = 0
    i = 0
    while x < len(file_len)-1 :
        for i in range(len(meas_freq_range)) :
            if i != 0 :
                if (meas_freq_range[i-1] != meas_freq_range[i]-1) or (i == len(meas_freq_range)-1):
                    if x == 0 :
                        if i != len(meas_freq_range)-1 :
                            plot_smith(S22_nparray[meas_freq_range[x]:meas_freq_range[i-1]], title = title, label = my_label[x])
                            x += 1
                            i += 1
                            y = i
                        else :
                            plot_smith(S22_nparray[meas_freq_range[x]:meas_freq_range[i]], title = title, label = my_label[x])
                            x += 1
                    else :
                        if i != len(meas_freq_range)-1 :
                            plot_smith(S22_nparray[meas_freq_range[y]:meas_freq_range[i-1]], title = title, label = my_label[x])
                            x += 1
                            i += 1
                            y = i
                        else :
                            plot_smith(S22_nparray[meas_freq_range[y]:meas_freq_range[i]], title = title, label = my_label[x])
                            x += 1
            else :
                i += 1

    z = 0
    i = 0
    y = 0
    for z in range(len(sim_file_len)) :
        for i in range(len(sim_freq_range)) :
            if i != 0 :
                if (sim_freq_range[i-1] != sim_freq_range[i]-1) or (i == len(sim_freq_range)-1):
                    if z == 0 :
                        if i != len(sim_freq_range)-1 :
                            plot_smith(sim_S22_nparray[sim_freq_range[z]:sim_freq_range[i-1]], title = title, label = my_label[x])
                            z += 1
                            i += 1
                            y = i
                            x += 1
                        else :
                            plot_smith(sim_S22_nparray[sim_freq_range[z]:sim_freq_range[i]], title = title, label = my_label[x])
                            x += 1
                    else :
                        if i != len(meas_freq_range)-1 :
                            plot_smith(sim_S22_nparray[sim_freq_range[y]:sim_freq_range[i-1]], title = title, label = my_label[x])
                            z += 1
                            i += 1
                            y = i
                            x += 1
                        else :
                            plot_smith(sim_S22_nparray[sim_freq_range[y]:sim_freq_range[i]], title = title, label = my_label[x])
                            x += 1
            else :
                i += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])

#plot S11, S21, S12 & S22
def plt_smith_meas_sim_mult_freq_range(smith_filenames, sim_smith_filenames, my_label, dir) :
    title = ['S11 Smith Measured and Simulated (400-800MHz)', 'S21 Smith Measured and Simulated (400-800MHz)', 'S12 Smith Measured and Simulated (400-800MHz)', 'S22 Smith Measured and Simulated (400-800MHz)']
    plt_s11_smith_meas_sim_mult_freq_range(smith_filenames, sim_smith_filenames, my_label, title[0], dir)
    plb.clf()
    plt_s21_smith_meas_sim_mult_freq_range(smith_filenames, sim_smith_filenames, my_label, title[1], dir)
    plb.clf()
    plt_s12_smith_meas_sim_mult_freq_range(smith_filenames, sim_smith_filenames, my_label, title[2], dir)
    plb.clf()
    plt_s22_smith_meas_sim_mult_freq_range(smith_filenames, sim_smith_filenames, my_label, title[3], dir)
    plb.clf()


#-----------------------------------------------------------------------------------------------------------------

#NOISE FIGURE
#the following plots the noise figure for just the measured data, this works with only one measured file.
def plot_nf_no_sim(meas_nf_filenames, plt_label, xlim = None, ylim = None) :
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
    plt.title('Noise Figure', fontsize = 16)
    plt.xlabel('Frequency (GHz)', fontsize = 16)
    plt.ylabel('Noise Figure (dB)', fontsize = 16)
    plt.grid()
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    plt.savefig('Noise_Figure_meas_(10MHz-1500MHz).pdf')
    plt.savefig('Noise_Figure_meas_(10MHz-1500MHz).jpeg')
    plb.clf()


def plot_nf_meas_and_sim(meas_nf_filenames, sim_nf_filenames, plt_label, xlim= None, ylim=None) :
    nf_freq, gain, nf, meas_file_len = read_nf_data_from_mult_files(meas_nf_filenames)
    freq_nparray, nf_nparray, gamma_nparray, phase_angle_nparray, noise_resistance_nparray, sim_file_len = read_nf_data_from_mult_ADS_files(sim_nf_filenames)
    z = 0
    while z < len(meas_file_len) : #plot the measured nf data
        if z == 0:
            plt.plot(nf_freq[0:meas_file_len[z]]/1e9, nf[0:meas_file_len[z]], label = plt_label[z]) #plots the measured nf data from the first file
            #print nf[0:file_len[z]]
            z += 1
        else :
            plt.plot(nf_freq[sum(meas_file_len[0:z]):(sum(meas_file_len[0:z]) + meas_file_len[z])]/1e9, nf[sum(meas_file_len[0:z]):(sum(meas_file_len[0:z]) + meas_file_len[z])], label = plt_label[z]) #plots the measured nf data from the rest of the files
            z += 1
    x = 0
    while x < len(sim_file_len) : #plot the simulated nf data
        if x == 0:
            plt.plot(freq_nparray[0:sim_file_len[x]]/1e9, nf_nparray[0:sim_file_len[x]], label = plt_label[z]) #plots the simulated nf data from the first file
            z += 1
            x += 1
        else :
            plt.plot(freq_nparray[sum(sim_file_len[0:x]):(sum(sim_file_len[0:x]) + sim_file_len[x])]/1e9, nf_nparray[sum(sim_file_len[0:x]):(sum(sim_file_len[0:x]) + sim_file_len[x])], label = plt_label[z]) #plots the simulated nf data from the rest of the files
            z += 1
            x += 1
    plt.legend(loc = 'best')
    plt.title('Noise Figure', fontsize = 16)
    plt.xlabel('Frequency (GHz)', fontsize = 16)
    plt.ylabel('Noise Figure (dB)', fontsize = 16)
    plt.grid()
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    plt.savefig('Noise_Figure_meas&sim_(10MHz-1500MHz).pdf')
    plt.savefig('Noise_Figure_meas&sim_(10MHz-1500MHz).jpeg')
    plb.clf()

#-----------------------------------------------------------------------------------------------------------------

#STABILITY FACTOR, K
#K = (1-mag(S11)^2-mag(S22)^2+mag(delta)^2)/(2*mag(S21*S12)) #the equation for the stability factor, k
#delta = S11*S22 - S12*S21 #the equation for delta, used in calculating the stability factor, k
#equation for k found at http://www.microwaves101.com/encyclopedias/stability-factor

def CalcKStabFactor(realimag_filenames) :
    freq_realimag_np, s11_realimag_np, s21_realimag_np, s12_realimag_np, s22_realimag_np, realimag_file_len = read_smith_data_from_files(realimag_filenames)
    k = (1-np.abs(s11_realimag_np)**2 - np.abs(s22_realimag_np)**2 + np.abs(s11_realimag_np*s22_realimag_np - s12_realimag_np*s21_realimag_np)**2)/(2*np.abs(s21_realimag_np)*np.abs(s12_realimag_np))
    return (k, realimag_file_len, freq_realimag_np)

def CalcKStabFactor_meas_sim(meas_realimag_filenames, sim_realimag_filenames) :
    meas_k_stab_factor, file_len, freq_nparray = CalcKStabFactor(meas_realimag_filenames)
    sim_k_stab_factor, sim_file_len, sim_freq_nparray = CalcKStabFactor(sim_realimag_filenames)
    return(meas_k_stab_factor, file_len, freq_nparray, sim_k_stab_factor, sim_file_len, sim_freq_nparray)


#the following plots the k stability factor for just the measured data, this works with more than one measured file or just one measured file.
def plot_stab_fact_meas(realimag_filenames, title, my_label, ylim, dir) :
    k_stab_factor, file_len, freq_nparray = CalcKStabFactor(realimag_filenames)
    mu, mu_file_len, freq_np_mu = CalcMuStabFactor(realimag_filenames)
    x = 0
    while x < len(file_len) :
        if x == 0:
            plot_rectangular(freq_nparray[x:file_len[x]]/1e9, k_stab_factor[x:file_len[x]], x_label = 'Frequency (GHz)', y_label = 'Stability Factor', title = title[0], ylim = ylim, label = my_label[x])
            x += 1
        else :
            plot_rectangular(freq_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])]/1e9 , k_stab_factor[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], x_label = 'Frequency (GHz)', y_label = 'Stability Factor', title = title[0], ylim = ylim, label = my_label[x])
            x += 1
    y = 0
    while y < len(mu_file_len) :
        if y == 0:
            plot_rectangular(freq_np_mu[y:mu_file_len[y]]/1e9, mu[y:mu_file_len[y]], x_label = 'Frequency (GHz)', y_label = 'Stability Factor', title = title[0], ylim = ylim, label = my_label[x])
            x += 1
            y += 1
        else :
            plot_rectangular(freq_np_mu[sum(mu_file_len[0:y]):(sum(mu_file_len[0:y])+mu_file_len[y])]/1e9 , mu[sum(mu_file_len[0:y]):(sum(mu_file_len[0:y])+mu_file_len[y])], x_label = 'Frequency (GHz)', y_label = 'Stability Factor', title = title[0], ylim = ylim, label = my_label[x])
            x += 1
            y += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()


#the following plots the k stability factor for the measured and simulated data, this works with more than one file or just one file.
def plot_stab_fact_meas_sim(realimag_filenames, sim_realimag_filenames, title, my_label, ylim, dir) :
    k_stab_factor, file_len, freq_nparray, sim_k_stab_factor, sim_file_len, sim_freq_nparray = CalcKStabFactor_meas_sim(realimag_filenames, sim_realimag_filenames)
    x = 0
    if ylim is not None:
        ylim = [ylim[0], ylim[1]]
    while x < len(file_len) : #plot the measured stability factor
        if x == 0:
            plot_rectangular(freq_nparray[x:file_len[x]]/1e9, k_stab_factor[x:file_len[x]], x_label = 'Frequency (GHz)', y_label = 'Stability Factor, K', title = title[0], ylim = ylim, label = my_label[x])
            x += 1
        else :
            plot_rectangular(freq_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])]/1e9 , k_stab_factor[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], x_label = 'Frequency (GHz)', y_label = 'Stability Factor, K', title = title[0], ylim = ylim, label = my_label[x])
            x += 1
    y = 0
    while y < len(sim_file_len) : #plot the simulated stability factor
        if y == 0:
            plot_rectangular(sim_freq_nparray[y:sim_file_len[y]]/1e9, sim_k_stab_factor[y:sim_file_len[y]], x_label = 'Frequency (GHz)', y_label = 'Stability Factor, K', title = title[0], ylim = ylim, label = my_label[x])
            x += 1
            y += 1
        else :
            plot_rectangular(sim_freq_nparray[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])]/1e9 , sim_k_stab_factor[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])], x_label = 'Frequency (GHz)', y_label = 'Stability Factor, K', title = title[0], ylim = ylim, label = my_label[x])
            x += 1
            y += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()

#the following plots the k stability factor for the measured and simulated data, this works with more than one file or just one file.
def plot_stab_fact_meas_sim_limits(realimag_filenames, sim_realimag_filenames, title, my_label, limits, ylim, dir) :
    k_stab_factor, file_len, freq_nparray, sim_k_stab_factor, sim_file_len, sim_freq_nparray = CalcKStabFactor_meas_sim(realimag_filenames, sim_realimag_filenames)
    x = 0
    if ylim is not None:
        ylim = [ylim[0], ylim[1]]
    while x < len(file_len) : #plot the measured stability factor
        if x == 0:
            plot_rectangular(freq_nparray[x:file_len[x]]/1e9, k_stab_factor[x:file_len[x]], x_label = 'Frequency (GHz)', y_label = 'Stability Factor, K (10MHz-1GHz)', title = title[0], limits = limits, ylim = ylim, label = my_label[x])
            x += 1
        else :
            plot_rectangular(freq_nparray[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])]/1e9 , k_stab_factor[sum(file_len[0:x]):(sum(file_len[0:x])+file_len[x])], x_label = 'Frequency (GHz)', y_label = 'Stability Factor, K (10MHz-1GHz)', title = title[0], limits = limits, ylim = ylim, label = my_label[x])
            x += 1
    y = 0
    while y < len(sim_file_len) : #plot the simulated stability factor
        if y == 0:
            plot_rectangular(sim_freq_nparray[y:sim_file_len[y]]/1e9, sim_k_stab_factor[y:sim_file_len[y]], x_label = 'Frequency (GHz)', y_label = 'Stability Factor, K (10MHz-1GHz)', title = title[0], limits = limits, ylim = ylim, label = my_label[x])
            x += 1
            y += 1
        else :
            plot_rectangular(sim_freq_nparray[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])]/1e9 , sim_k_stab_factor[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])], x_label = 'Frequency (GHz)', y_label = 'Stability Factor, K (10MHz-1GHz)', title = title[0], limits = limits, ylim = ylim, label = my_label[x])
            x += 1
            y += 1
    save_all_figs( dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()

#-----------------------------------------------------------------------------------------------------------------

#STABILITY FACTOR, MU

#mu = {1-|S11|^2} / {|S22 - conj(S11)*Delta| + |S12 * S21|}

def CalcMuStabFactor(realimag_filenames) :
    freq_realimag_np, s11_realimag_np, s21_realimag_np, s12_realimag_np, s22_realimag_np, realimag_file_len = read_smith_data_from_files(realimag_filenames)
    mu = (1-np.abs(s11_realimag_np)**2)/(np.abs(s22_realimag_np - np.conj(s11_realimag_np)* (s11_realimag_np*s22_realimag_np - s12_realimag_np*s21_realimag_np)) + np.abs(s12_realimag_np*s21_realimag_np))
    return(mu, realimag_file_len, freq_realimag_np)

def CalcMuStabFactor_meas_sim(meas_realimag_filenames, sim_realimag_filenames) :
    meas_mu_stab_factor, meas_file_len, freq_nparray = CalcMuStabFactor(meas_realimag_filenames)
    sim_mu_stab_factor, sim_file_len, sim_freq_nparray = CalcMuStabFactor(sim_realimag_filenames)
    return(meas_mu_stab_factor, meas_file_len, freq_nparray, sim_mu_stab_factor, sim_file_len, sim_freq_nparray)


#the following plots the mu stability factor for the measured and simulated data, this works with more than one file or just one file.
def plot_mu_meas_sim(meas_realimag_filenames, sim_realimag_filenames, title, my_label, ylim, dir) :
    meas_mu, meas_file_len, freq_nparray, sim_mu_stab_factor, sim_file_len, sim_freq_nparray = CalcMuStabFactor_meas_sim(meas_realimag_filenames, sim_realimag_filenames)
    x = 0
    if ylim is not None:
        ylim = [ylim[0], ylim[1]]
    while x < len(meas_file_len) : #plot the measured stability factor
        if x == 0:
            plot_rectangular(freq_nparray[x:meas_file_len[x]]/1e9, meas_mu[x:meas_file_len[x]], x_label = 'Frequency (GHz)', y_label = 'Stability Factor, Mu', title = title[0], ylim = ylim, label = my_label[x])
            x += 1
        else :
            plot_rectangular(freq_nparray[sum(meas_file_len[0:x]):(sum(meas_file_len[0:x])+meas_file_len[x])]/1e9 , meas_mu[sum(meas_file_len[0:x]):(sum(meas_file_len[0:x])+meas_file_len[x])], x_label = 'Frequency (GHz)', y_label = 'Stability Factor, Mu', title = title[0], ylim = ylim, label = my_label[x])
            x += 1
    y = 0
    while y < len(sim_file_len) : #plot the simulated stability factor
        if y == 0:
            plot_rectangular(sim_freq_nparray[y:sim_file_len[y]]/1e9, sim_mu_stab_factor[y:sim_file_len[y]], x_label = 'Frequency (GHz)', y_label = 'Stability Factor, Mu', title = title[0], ylim = ylim, label = my_label[x])
            x += 1
            y += 1
        else :
            plot_rectangular(sim_freq_nparray[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])]/1e9 , sim_mu_stab_factor[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])], x_label = 'Frequency (GHz)', y_label = 'Stability Factor, Mu', title = title[0], ylim = ylim, label = my_label[x])
            x += 1
            y += 1
    save_all_figs(dir = dir, format = ['pdf' , 'jpeg'])
    plb.clf()


#the following plots the mu stability factor for the measured and simulated data, this works with more than one file or just one file.
def plot_mu_meas_sim_limits(meas_realimag_filenames, sim_realimag_filenames, title, my_label, limits, ylim, dir) :
    meas_mu, meas_file_len, freq_nparray, sim_mu_stab_factor, sim_file_len, sim_freq_nparray = CalcMuStabFactor_meas_sim(meas_realimag_filenames, sim_realimag_filenames)
    x = 0
    if ylim is not None:
        ylim = [ylim[0], ylim[1]]
    while x < len(meas_file_len) : #plot the measured stability factor
        if x == 0:
            plot_rectangular(freq_nparray[x:meas_file_len[x]]/1e9, meas_mu[x:meas_file_len[x]], x_label = 'Frequency (GHz)', y_label = 'Stability Factor, Mu (10MHz-1GHz)', title = title[0], limits = limits, ylim = ylim, label = my_label[x])
            x += 1
        else :
            plot_rectangular(freq_nparray[sum(meas_file_len[0:x]):(sum(meas_file_len[0:x])+meas_file_len[x])]/1e9 , meas_mu[sum(meas_file_len[0:x]):(sum(meas_file_len[0:x])+meas_file_len[x])], x_label = 'Frequency (GHz)', y_label = 'Stability Factor, Mu (10MHz-1GHz)', title = title[0], limits = limits, ylim = ylim, label = my_label[x])
            x += 1
    y = 0
    while y < len(sim_file_len) : #plot the simulated stability factor
        if y == 0:
            plot_rectangular(sim_freq_nparray[y:sim_file_len[y]]/1e9, sim_mu_stab_factor[y:sim_file_len[y]], x_label = 'Frequency (GHz)', y_label = 'Stability Factor, Mu (10MHz-1GHz)', title = title[0], limits = limits, ylim = ylim, label = my_label[x])
            x += 1
            y += 1
        else :
            plot_rectangular(sim_freq_nparray[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])]/1e9 , sim_mu_stab_factor[sum(sim_file_len[0:y]):(sum(sim_file_len[0:y])+sim_file_len[y])], x_label = 'Frequency (GHz)', y_label = 'Stability Factor, Mu (10MHz-1GHz)', title = title[0], limits = limits, ylim = ylim, label = my_label[x])
            x += 1
            y += 1
    save_all_figs(dir = dir, format = ['pdf', 'jpeg'])
    plb.clf()