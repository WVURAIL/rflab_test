############################################
# @Purpose:measure_two_port_s_paramters.py: A script measure 2 port S parameters. can easily be extended.
#
# @Authors: Pranav Sanghavi and Joseph Shepard
#
# @Date: 9/13/2021
###############################################

import numpy as np
import skrf as rf
import matplotlib.pyplot as plt
import time
import pyvisa as visa
import time
import os
from sys import exit


def set_freq_lims(start, stop):
    """
    set_freq_lims [Set frequency limits of measurement]
    [GP-IB Commands:
    http://na.support.keysight.com/pna/help/latest/Programming/GP-IB_Command_Finder/Sense/Frequency.htm]
    Parameters
    ----------
    start : [float]
        [in Hz]
    stop : [fload]
        [in Hz]
    """
    VNA.write('SENSe:FREQuency:STARt ' + str(start))
    VNA.write('SENSe:FREQuency:STOp ' + str(stop))


def check_power_mode():
    """
    CHECK POWER MODE
    """
    print(f"Current Output power is {VNA.query('SOURce:POWer:ALC:MODE?')}")


def set_power_mode(output_power, nominal_power=-15):
    """
    set_power_mode [set power level for your measurement]
    [set power, can be "HIGH", "LOW" or "MAN" if "MAN" ie manual set `nominal power`]
    Parameters
    ----------
    output_power : [str]
        ["HIGH", "LOW" or "MAN"]
    nominal_power : int, optional
        [description], by default -15dB
        Source power/attenuator level.
        N9912A: 0 to -31 dB in 1 dB steps
        N9923A: 0 to -47 dB in .5 dB steps
        All other models: Set power level from +3 to -45 dBm in .1 dB steps.
    """
    print(f"Setting output power to {output_power}")
    VNA.write('SOURce:POWer:ALC:MODE ' + str(output_power))
    check_power_mode()
    if str(output_power) == "MAN":
        print(f"Setting nominal power/attenuation level {nominal_power}")
        VNA.write('SOURce:POWer ' + str(nominal_power))


def measure_s_parameter(measurement, serial_num, start_freq, stop_freq, output_power, nominal_power=-15, plot=False):
    """
    measure_s_parameter [measures S parameter of choice]
    [S11, S12, S21, S22, for given power level. ]
    Parameters
    ----------
    measurement :[str]]
        ["S11", "S12", "S21", "S22"]
    serial_num : [str]
        [ID of device being measured]
    start_freq : [float]
        [in Hz]
    stop_freq : [float]
        [in Hz]
    output_power : [str]
        ["HIGH", "LOW" or "MAN"]
    nominal_power : [float]
        [in dB]
    Returns
    -------
    [tuple of nd.array]
        [(data, data_raw) where data is the log magnitude and the data_raw is the complex measurement]
    """
    print("setting frequency limits")
    set_freq_lims(start_freq, stop_freq)
    check_power_mode()

    if output_power == "MAN":
        input(f"Enter nominal power in dBm :")
    set_power_mode(output_power, nominal_power)
    print(f"Measuring {measurement} with Output mode {output_power}")
    VNA.write(':CALCulate:PARameter1:DEFine ' + measurement)
    # http://na.support.keysight.com/pna/help/latest/Programming/GP-IB_Command_Finder/Calculate/Parameter.htm COMMANDS FOR MEASUREMENT PARAMETERS
    VNA.write(':CALCulate:SELected:FORMat MLOGarithmic')
    # MLINear, MLOGarithmic, PHASe, UPHase 'Unwrapped phase, IMAGinary,REAL
    # POLar SMITh, SADMittance 'Smith Admittance, SWR, GDELay 'Group Delay
    # http://na.support.keysight.com/pna/help/latest/Programming/GP-IB_Command_Finder/Calculate/Format_Calc.htm
    time.sleep(1)
    # scaling plot on the VNA screen
    VNA.write(':DISPlay:WINDow:TRACe:Y:SCALe:AUTO')
    # OTHER VNA COMMANDS THAT CONTROL THE SCREEN
    # http://na.support.keysight.com/pna/help/latest/Programming/GP-IB_Command_Finder/Display.htm#yauto
    ##########
    data = VNA.query('CALCulate:DATA:FDaTa?')
    # http://na.support.keysight.com/pna/help/latest/Programming/GP-IB_Command_Finder/Calculate/Data.htm # COMMANDS TO SAVE DATA
    data = data_real = np.asarray(data.split(
        ',')[:-1] + [data.split(',')[-1][:-1]])
    data = np.array([float(i.lower()) for i in data])
    print(f"DONE measuring {measurement}")

    if plot:
        plt.figure()
        plt.plot(np.linspace(start_freq/1e6,
                             stop_freq/1e6, data.shape[-1]), data)
        plt.xlabel("MHz")
        plt.ylabel("dBm")
        plt.title(f"{measurement}_{serial_num}")
        plt.show()
        plt.savefig(
            f"{PLOT_DIR}{measurement}_{serial_num}.png")

    VNA.write(':CALCulate:SELected:FORMat REAL')
    time.sleep(1)
    data_real = VNA.query('CALCulate:DATA:FDaTa?')
    data_real = np.asarray(data_real.split(
        ',')[:-1] + [data_real.split(',')[-1][:-1]])
    VNA.write(':CALCulate:SELected:FORMat IMAG')
    time.sleep(1)
    data_imag = VNA.query('CALCulate:DATA:FDaTa?')
    data_imag = np.asarray(data_imag.split(
        ',')[:-1] + [data_imag.split(',')[-1][:-1]])
    data_raw = np.array([float(i[0].lower())+float(i[1].lower())
                         * 1j for i in zip(data_real, data_imag)])
    return data, data_raw


def intialize_network_analyzer():
    global VNA
    ##############################################################################
    # load visa library
    rm = visa.ResourceManager() # pyvisa shoudl automatically find libraries if not can specify the library as below
    #rm = visa.ResourceManager(VISA_LIB_FILE_PATH)  # windows
    # TODO linux
    # https://edadocs.software.keysight.com/kkbopen/linux-io-libraries-faq-589309025.html
    # https://www.keysight.com/us/en/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html click linux
    #
    # find connected instrument and get instrument address
    print(rm.list_resources())
    instrument_address = rm.list_resources()
    # load  instrument object
    VNA = rm.open_resource(instrument_address[0])
    VNA.write('*IDN?')
    IDN = VNA.read()
    print(IDN)
    VNA.timeout = 10000
    # # select NA mode
    # ```
    # Relevant Modes
    #  ALL
    #
    # Parameters
    #
    #
    # <string>
    #  Operating Mode. Case-sensitive. Choose from the modes that are installed on your FieldFox:
    #
    # "CAT"
    # "IQ"
    # "NA"
    # "SA"
    # "Power Meter"
    # "VVM"
    # "Pulse Measurements"
    # "ERTA"
    #
    # Examples
    #  INST "NA";*OPC?
    #  ```
    #
    # common commands: http://na.support.keysight.com/pna/help/latest/Programming/GP-IB_Command_Finder/Common_Commands.htm

    # print available modes of instrument
    print(VNA.query('INSTrument:CATalog?'))

    VNA.write('INST "NA";*OPC?')  # set in network analyzer mode

    if VNA.read()[0] == '1':
        print("Successfully set NA mode")

    # ```
    # For NA Mode:
    # Reverse measurements are available ONLY with full S-parameter option.
    #
    # S11 - Forward reflection measurement
    # S21 - Forward transmission measurement
    # S12 - Reverse transmission
    # S22 - Reverse reflection
    # A - A receiver measurement
    # B - B receiver measurement
    # R1 - Port 1 reference receiver measurement
    # R2 - Port 2 reference receiver measurement
    # ```

def execute_measurement(start_freq, stop_freq):
    """
    execute_measurement [Get two port S parameters from the network analyzer]
    [saves touchstone files in TOUCHSTONE_DIR]
    Parameters
    ----------
    start_freq : [float]
        [in Hz]
    stop_freq : [float]
        [in Hz]
    """
    KEEP_MEASURING = True
    while KEEP_MEASURING:
        con = input(
            "Please Connect the VNAs and ensure it is powered on! Once connected press y: ")
        if con == 'y':
            intialize_network_analyzer()

        ##########################################################################
        # set start and stop freq
            set_freq_lims(start_freq, stop_freq)
        ##########################################################################

            serial_num = input("Please Enter Device Serial Number: ")
            z = input("Please Connect VNA to Device! Press Enter when Finished: ")
            serial_num_1 = serial_num

            output_power = "LOW"
            #nominal_power=-15
            m = "S11"
            S11, S11_raw = measure_s_parameter(
                m, serial_num_1, start_freq, stop_freq, output_power, nominal_power=-15, plot=False)
            output_power = "LOW"
            #nominal_power=-15
            m = "S12"
            S12, S12_raw = measure_s_parameter(
                m, serial_num_1, start_freq, stop_freq, output_power, nominal_power=-15, plot=False)
            output_power = "LOW"
            #nominal_power=-15
            m = "S21"
            S21, S21_raw = measure_s_parameter(
                m, serial_num_1, start_freq, stop_freq, output_power, nominal_power=-15, plot=False)
            output_power = "LOW"
            #nominal_power=-15
            m = "S22"
            S22, S22_raw = measure_s_parameter(
                m, serial_num_1, start_freq, stop_freq, output_power, nominal_power=-15, plot=False)

            f = np.linspace(start_freq, stop_freq, S11_raw.shape[-1])

            s = np.zeros((len(f), 2, 2))+1.0j
            s[:, 0, 0] = S11_raw
            s[:, 0, 1] = S12_raw
            s[:, 1, 0] = S21_raw
            s[:, 1, 1] = S22_raw

            nw = rf.Network(name=f"{serial_num_1}", s=s, frequency=f, z0=50)
            nw.write_touchstone(
                filename=f"{serial_num_1}", dir=f"{TOUCHSTONE_DIR}")
            #nw.plot_s_db(label=f"{serial_num_1}")
            #plt.show()
            #plt.savefig(f"{PLOT_DIR}{serial_num}.png")
        i = input("Finished? Press 0. Test another Device? Press 1 : ")
        if i == '1':
            KEEP_MEASURING = True
        else:
            KEEP_MEASURING = False
            print("Measurement Done!")


if __name__ == "__main__":

    # TODO : add argument parsers
    start_freq = 1e7
    stop_freq = 2e9

    if start_freq > stop_freq:
        print("start frequency is greater than stop freq. fix and rerun")
        exit()

    VISA_LIB_FILE_PATH = "C:\\Windows\\System32\\visa64.dll"
    PARENT_DIR = "C:\\Users\\RadioLab\\Desktop\\Testing\\"

    PLOT_DIR = PARENT_DIR + "S_Plots\\"
    TOUCHSTONE_DIR = PARENT_DIR + "Touchstone_Files"
    SMITH_PLOT_DIR = PARENT_DIR + "Smith_Charts\\"

    # create appropriate dirs
    if not os.path.exists(PLOT_DIR):
        os.makedirs(PLOT_DIR)
    if not os.path.exists(TOUCHSTONE_DIR):
        os.makedirs(TOUCHSTONE_DIR)
    if not os.path.exists(SMITH_PLOT_DIR):
        os.makedirs(SMITH_PLOT_DIR)

    execute_measurement(start_freq, stop_freq)
