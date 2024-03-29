import numpy as np

import pylab

from scipy.io import loadmat

from matplotlib.patches import Circle


def loadRangeData(filename):
    '''

    Loads antenna range data file and parses the pertinent info

    Returns frequencies, angles, S11 and S21 in dB.

    '''

    mat = loadmat(filename+'.mat')

    freq = mat['frequency'][0]

    s11 = mat['S11'][0]

    print s11

    angle = mat['degree'][0]*np.pi/180.0

    s21s = mat['S21']

    s21s = 20.0*np.log10(s21s)

    return freq, angle, s11, s21s


def loadNetworkS11(filename):
    '''

    Loads a text file for S11 from the Network Analyzer

    '''

    mat = np.loadtxt(filename, delimiter=',')

    freq = mat[:, 0]/1e9

    s11 = mat[:, 1]+1.0j*mat[:, 2]

    return freq, s11


def plotS11(freq, s11, startFreq=0.5, stopFreq=0.85, fileout='ant_data.txt '):

    frequencies = (freq > startFreq) & (freq < stopFreq)

    plot_s_smith(s11[frequencies], fileout[:-4])

    s11mag = 20*np.log10(np.abs(s11))

    pylab.plot(freq[frequencies], s11mag[frequencies])

    pylab.xlabel('frequency (GHz)')

    pylab.ylabel('S11 (db)')

    pylab.title('Return Loss')

    pylab.savefig(fileout[:-4] + '_s11_plot.pdf', dpi=300)

    pylab.clf()


def overplotS21(angle, s21, label1):

    dbplot = s21 + 30

    dbplot[(dbplot < 0)] = 0

    pylab.polar(angle, dbplot, label=label1)

    lines, labels = pylab.rgrids((5, 10, 15, 20, 25, 30, 35, 40),

                                 ('-25', '-20', '-15', '-10', '-5', '0', '5', '10'))


def overplotS21rect(angle, s21, label1):

    pylab.plot(angle, s21, label=label1)


def getFrequencies(freq, startFreq, stopFreq):

    fr = np.arange(startFreq, stopFreq+0.05, 0.1)

    frequencies = []

    for f in fr:

        frequencies.append(np.where(freq > f)[0][0])

    frequencies = np.array(frequencies)

    return frequencies


def plotResults(filename, startFreq=0.5, stopFreq=0.8, centerFreq=0.65):
    '''

    Plots antenna range data file.  startFreq and stopFreq are the range of 

    frequencies to overplot

    '''

    freq, angle, s11, s21All = loadRangeData(filename)

    s11 = 20*np.log10(np.abs(s11))

    #best_match = where(s11 == s11.min())[0][0]

    best_match = np.where(freq > centerFreq)[0][0]

    #frequencies = ( freq > 1.8 ) & (freq < 2.0)

    #fr = freq[frequencies]

    fr = np.arange(startFreq, stopFreq+0.05, 0.1)

    frequencies = []

    for f in fr:

        frequencies.append(np.where(freq > f)[0][0])

    frequencies = np.array(frequencies)

    # print freq[frequencies]

    print 'Best match Frequency ', freq[best_match]

    pylab.plot(freq, s11)

    pylab.xlabel('frequency (GHz)')

    pylab.ylabel('S11 (db)')

    pylab.title('Return Loss')

    pylab.savefig(filename + '_s11_plot.pdf', dpi=300)

    pylab.clf()

    pylab.plot(freq, s11)

    pylab.xlim(startFreq, stopFreq)

    pylab.ylim(-20, 0)

    pylab.xlabel('frequency (GHz)')

    pylab.ylabel('S11 (db)')

    #pylab.title('Antenna Match')

    pylab.savefig(filename + '_s11_plot_zoom.pdf', dpi=300)

    pylab.clf()

    s21db = s21All[:, best_match]

    print 'max gain: ', s21db.max()

    dbplot = s21db + 30  # (40-s21db.max())

    dbplot[(dbplot < 0)] = 0

    pylab.polar(angle, dbplot)

    lines, labels = pylab.rgrids((5, 10, 15, 20, 25, 30, 35, 40),

                                 ('-25', '-20', '-15', '-10', '-5', '0', '5', '10'))

    # lines, labels = pylab.rgrids( ( 15,20,25,30,35,40,45,50),

    #                       ( '-25', '-20','-15','-10','-5','0','5','10' ))

    pylab.savefig(

        filename + '_'+'{0:.3f}'.format(freq[best_match])

        + 'GHz_s21_pattern.pdf', dpi=300)

    pylab.clf()

    s21s = s21All[:, frequencies]

    s21s = s21s + 30.0  # (40-s21s.max())

    s21s[(s21s < 0)] = 0

    freqs = freq[frequencies]

    # print s21s.shape

    for i, frequency in enumerate(freqs):

        pylab.polar(angle, s21s[:, i], label=str(frequency)[:3]+'GHz')

    lines, labels = pylab.rgrids((5, 10, 15, 20, 25, 30, 35, 40),

                                 ('-25', '-20', '-15', '-10', '-5', '0', '5', '10'))

    # lines, labels = pylab.rgrids( (5, 10, 15,20,25,30,35,40),

    #                   ('-35', '-30', '-25', '-20','-15','-10','-5','0' ))

    pylab.legend(loc=(1, -0.1))

    pylab.savefig(

        filename + '_'+str(startFreq)+'-'+str(stopFreq) +

        'GHz_s21_pattern_all.pdf',

        dpi=300)

    pylab.clf()


def smith(smithR=1, chart_type='z', ax=None):
    '''

    FROM scikit-rf package

    plots the smith chart of a given radius



    Parameters

    -----------

    smithR : number

            radius of smith chart

    chart_type : ['z','y']

            Contour type. Possible values are

             * *'z'* : lines of constant impedance

             * *'y'* : lines of constant admittance

    ax : matplotlib.axes object

            existing axes to draw smith chart on





    '''

    # TODO: fix this function so it doesnt suck

    if ax == None:

        ax1 = pylab.gca()

    else:

        ax1 = ax

    # contour holds matplotlib instances of: pathes.Circle, and lines.Line2D, which

    # are the contours on the smith chart

    contour = []

    # these are hard-coded on purpose,as they should always be present

    rHeavyList = [0, 1]

    xHeavyList = [1, -1]

    # TODO: fix this

    # these could be dynamically coded in the future, but work good'nuff for now

    rLightList = pylab.logspace(3, -5, 9, base=.5)

    xLightList = pylab.hstack(
        [pylab.logspace(2, -5, 8, base=.5), -1*pylab.logspace(2, -5, 8, base=.5)])

    # cheap way to make a ok-looking smith chart at larger than 1 radii

    if smithR > 1:

        rMax = (1.+smithR)/(1.-smithR)

        rLightList = pylab.hstack([pylab.linspace(0, rMax, 11), rLightList])

    if chart_type is 'y':

        y_flip_sign = -1

    else:

        y_flip_sign = 1

    # loops through Light and Heavy lists and draws circles using patches

    # for analysis of this see R.M. Weikles Microwave II notes (from uva)

    for r in rLightList:

        center = (r/(1.+r)*y_flip_sign, 0)

        radius = 1./(1+r)

        contour.append(Circle(center, radius, ec='grey', fc='none'))

    for x in xLightList:

        center = (1*y_flip_sign, 1./x)

        radius = 1./x

        contour.append(Circle(center, radius, ec='grey', fc='none'))

    for r in rHeavyList:

        center = (r/(1.+r)*y_flip_sign, 0)

        radius = 1./(1+r)

        contour.append(Circle(center, radius, ec='black', fc='none'))

    for x in xHeavyList:

        center = (1*y_flip_sign, 1./x)

        radius = 1./x

        contour.append(Circle(center, radius, ec='black', fc='none'))

    # clipping circle

    clipc = Circle([0, 0], smithR, ec='k', fc='None', visible=True)

    ax1.add_patch(clipc)

    # draw x and y axis

    ax1.axhline(0, color='k', lw=.1, clip_path=clipc)

    ax1.axvline(1*y_flip_sign, color='k', clip_path=clipc)

    ax1.grid(0)

    # set axis limits

    ax1.axis('equal')

    ax1.axis(smithR*np.array([-1., 1., -1., 1.]))

    # loop though contours and draw them on the given axes

    for currentContour in contour:

        cc = ax1.add_patch(currentContour)

        cc.set_clip_path(clipc)


def plot_s_smith(s11, filename, r=1, ax=None, show_legend=True,

                 chart_type='z', *args, **kwargs):
    '''

    Function taken FROM scikit-rf package and modified to work here...



    plots the scattering parameter on a smith chart



    ##just takes array of scattering params and plots them

    plots indecies `m`, `n`, where `m` and `n` can be integers or

    lists of integers.





    Parameters

    -----------

    m : int, optional

            first index

    n : int, optional

            second index

    ax : matplotlib.Axes object, optional

            axes to plot on. in case you want to update an existing

            plot.

    show_legend : boolean, optional

            to turn legend show legend of not, optional

    *args : arguments, optional

            passed to the matplotlib.plot command

    **kwargs : keyword arguments, optional

            passed to the matplotlib.plot command





    See Also

    --------

    plot_vs_frequency_generic - generic plotting function

    smith -  draws a smith chart



    Examples

    ---------

    >>> myntwk.plot_s_smith()

    >>> myntwk.plot_s_smith(m=0,n=1,color='b', marker='x')

    '''

    # TODO: prevent this from re-drawing smith chart if one alread

    # exists on current set of axes

    # get current axis if user doesnt supply and axis

    if ax is None:

        ax = pylab.gca()

    M = [0]

    N = [0]

    if 'label' not in kwargs.keys():

        generate_label = True

    else:

        generate_label = False

    for m in M:

        for n in N:

            # set the legend label for this trace to the networks name if it

            # exists, and they didnt pass a name key in the kwargs

            if generate_label:

                if pylab.rcParams['text.usetex']:

                    label_string = '$S_{'+repr(m+1) + repr(n+1)+'}$'

                else:

                    label_string = 'S'+repr(m+1) + repr(n+1)

                kwargs['label'] = label_string

            # plot the desired attribute vs frequency

            if len(ax.patches) == 0:

                smith(ax=ax, smithR=r, chart_type=chart_type)

            ax.plot(s11.real,  s11.imag, *args, **kwargs)

    # draw legend

    if show_legend:

        ax.legend()

    ax.axis(np.array([-1, 1, -1, 1])*r)

    ax.set_xlabel('Real')

    ax.set_ylabel('Imaginary')

    ax.set_title(filename)

    pylab.savefig(filename +

                  '_s11_smith.pdf', dpi=300)

    pylab.clf()


def getImpedance(s11):

    z = 50.0*(1+s11)/(1-s11)

    return z


if __name__ == "__main__":

    import sys

    FILENAME = sys.argv[1]

    #FILENAME = 'Pol2_Eplane'

    freq, angle, s11, s21All = loadRangeData(FILENAME)

    frequencies = (freq > 0.5) & (freq < 1.5)

    plot_s_smith(s11[frequencies], FILENAME)

    z = getImpedance(s11)

    # for i, line in enumerate(z):

    #    print freq[i], line

    plotResults(FILENAME, startFreq=0.4, stopFreq=0.8, centerFreq=0.75)


def CalcComplexImpedance(real, imag):
    complex_z = []
    for x in range(0, len(real)):
        Zo = 50  # 50 Ohms
        Zreal = Zo*(((1-(real[x]**2)-(imag[x]**2))) /
                    (((1-real[x])**2)+(imag[x]**2)))
        Zimag = Zo*((2*imag[x])/(((1-real[x])**2)+(imag[x]**2)))

        complex_z.append(complex(Zreal, Zimag))
    return(complex_z)

# def CalcStabFactor(mag_s11,mag_s21,mag_s12,mag_s22) :
#    delta = np.zeros(len(mag_s11))
#    k_numerator = np.zeros(len(mag_s11))
#    k_denomenator = np.zeros(len(mag_s11))
#    stab_factor = np.zeros(len(mag_s11))
#    delta = mag_s11*mag_s22 - mag_s12*mag_s21
#    k_numerator = 1 - mag_s11**2 - mag_s22**2 + delta**2
#    k_denomenator = 2 * mag_s12 * mag_s21
#    stab_factor = k_numerator/k_denomenator
#    return(stab_factor)


# can only be used for one file, this worked in the program hirax_balun_v.4_cutboard.py 6/20/16
def CalcKStabFactor(mag_s11, mag_s21, mag_s12, mag_s22, s11, s21, s12, s22):
    mag_delta = mag_s11*mag_s22 - mag_s12*mag_s21
    k_numerator = 1 - mag_s11**2 - mag_s22**2 + mag_delta**2
    s12timess21_mag = mag_s12*mag_s21
    k_denominator = 2 * s12timess21_mag
    k_stab_factor = k_numerator/k_denominator
    return(k_stab_factor)


def CalcMuStabFactor(mag_s11, mag_s21, mag_s12, mag_s22, s11, s21, s12, s22, smith_filenames):
    freq, S11_nparray, S21_nparray, S12_nparray, S22_nparray, file_len = make_all_plots.read_smith_data_from_files(
        smith_filenames)
    mu_numerator = 1 - mag_s11**2

    mag_delta = mag_s11*mag_s22 - mag_s12*mag_s21
    mu_denominator = 2 * s12timess21_mag
    mu_stab_factor = k_numerator/k_denominator
    return(mu_stab_factor)


def read_logmag_data_from_files(file):
    x = 0
    logmag_data = []
    with open(file) as f:
        for row in f:
            logmag_data.append(row.split())
        x += 1
    m = 0
    freq = []
    S11 = []
    S21 = []
    S12 = []
    S22 = []
    while m < len(logmag_data):
        freq.append(float(logmag_data[m][0]))
        S11.append(float(logmag_data[m][1]))
        S21.append(float(logmag_data[m][3]))
        S12.append(float(logmag_data[m][5]))
        S22.append(float(logmag_data[m][7]))
        m += 1
    return (freq, S11, S21, S12, S22)


def read_smith_data_from_files(file):
    x = 0
    smith_data = []
    with open(file) as f:
        for row in f:
            smith_data.append(row.split())
        x += 1
    m = 0
    freq = []
    S11 = []
    S21 = []
    S12 = []
    S22 = []
    while m < len(smith_data):
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
    return (freq, S11_nparray, S21_nparray, S12_nparray, S22_nparray)


def read_nf_data_from_files(file):
    x = 0
    nf_data = []
    with open(file) as f:
        for row in f:
            nf_data.append(row.strip().split(','))
        x += 1
    m = 0
    freq = []
    gain = []
    nf = []
    while m < len(nf_data):
        freq.append(float(nf_data[m][0]))
        gain.append(float(nf_data[m][1]))
        nf.append(float(nf_data[m][2]))
        m += 1
    freq_nparray = np.array(freq)
    gain_nparray = np.array(gain)
    nf_nparray = np.array(nf)
    return (freq_nparray, gain_nparray, nf_nparray)


def read_nf_data_from_ADS_files(file):
    x = 0
    nf_data = []
    with open(file) as f:
        for row in f:
            nf_data.append(row.strip().split())
        x += 1
    m = 0
    freq = []
    gamma = []
    nf = []
    phase_angle = []
    noise_resistance = []
    while m < len(nf_data):
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
    return (freq_nparray, nf_nparray, gamma_nparray, phase_angle_nparray, noise_resistance_nparray)
