###############################################################################
#
#   Script to output HPGL to HP plotter over RS232
#
###############################################################################
#
#   2023 - December - Henk-Johan
#           - first version of the demo script
#
###############################################################################

import time
import serial                     
import sys


###############################################################################

file = 'my_amazing_plotfile_with_HPGL_in_it.plt'


###############################################################################
# penmode = 'auto'        # let plotter use carrousel with pens -> to be debugged
# penmode = 'manual'      # let uses change the pens -> to be debugged
penmode = 'ignore'      # use only one pen and ignore pen changes


###############################################################################
print('-'*80)
print('Plotter')
print('-'*80)


###############################################################################
# serialport settings
'''
Baud    B1  0
        B2  1
        B3  0
        B4  1
A4/A3       0
MET/USA     1
D/Y         0
Parity  S1  0
        S2  0
'''
ser = serial.Serial(
    port        = 'COM9',
    baudrate    = 9600,
    parity      = serial.PARITY_NONE,
    stopbits    = serial.STOPBITS_ONE,
    bytesize    = serial.EIGHTBITS,
    timeout     = 2
    )


###############################################################################
# check if the serial port is open
if ser.is_open:
    print('Serial port open OK')
else:
    print('Could not open serial port')
    sys.exit(0)


###############################################################################
# open the plot file and go line by line
totalcounter = 0
counter = 0
# open the plot file to check total plot lines so we can display a percentage of the progress
f = open(file, 'r')
for line in f:
    totalcounter += 1
f.close()    
# plot whole file
f = open(file, 'r')
for line in f:
    # check if we are in pen ignore mode
    if penmode == 'ignore':
        for pencounter in range(1,7,1):
            penname = 'SP' + str(pencounter) + ';'
            if penname in line:
                line = line.replace(penname, '')
                print(counter, penmode, penname, 'removed')
    # check if we are in pen manual mode so that user can change pens
    if penmode == 'manual':
        for pencounter in range(1,7,1):
            penname = 'SP' + str(pencounter) + ';'
            if penname in line:
                line = line.replace(penname, '')
                print(counter, penmode, penname, 'needs to be inserted in the holder')
                input("Press Enter to continue...")

    # print what we are doing and where we are
    print(counter, '\t', round(counter/totalcounter*100,1), '\t', line.strip() )

    # check if we need to wait for the plotter to work through the buffer
    state = ser.getCTS()    
    if state == False:
        print(counter, '\t\t\t', 'Sleeping level', 1, 0.5, 'second')
        time.sleep(0.5)

    state = ser.getCTS()    
    if state == False:
        print(counter, '\t\t\t', 'Sleeping level', 2, 1, 'second')
        time.sleep(1)

    state = ser.getCTS()    
    if state == False:
        print(counter, '\t\t\t', 'Sleeping level', 3, 2, 'second')
        time.sleep(2)

    state = ser.getCTS()    
    if state == False:
        print(counter, '\t\t\t', 'Sleeping level', 4, 5, 'second')
        time.sleep(5)

    state = ser.getCTS()    
    if state == False:
        print(counter, '\t\t\t', 'Sleeping lLevel', 5, 10, 'seconds')
        time.sleep(10)

    state = ser.getCTS()    
    if state == False:
        print(counter, '\t\t\t', 'Sleeping lLevel', 6, 10, 'seconds')
        time.sleep(10)

    # build array to transmit and then send a new line of data to the plotter buffer
    ar = []
    for letter in line:
        ar.append(ord(letter))
    transmit = bytearray(ar)
    trbytes = ser.write(transmit)
    if trbytes != len(transmit):
        print('ERROR : not all bytes transmitted over RS232')

    # some waiting times for the initial lines where the plotter
    # needs some time to setup and check things
    if counter < 1:
        # initial setup
        if penmode == 'auto':
            # give time to select the correct pen from the caroussel
            time.sleep(14)
        else:
            # no need for much additional time as no pen change is needed
            # only setup time
            time.sleep(1)
    else:
        # every line has a little sleep
        time.sleep(0.05)

    # up the counter and on to the next line
    counter += 1


###############################################################################
# plotting complete
print('-'*80)
print('Plotting completed')
print('-'*80)