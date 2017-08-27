#!/usr/bin/python3

import genwsprcode as g
import RPi.GPIO as GPIO
import time
import sys
from optparse import OptionParser
from random import randrange

wspr_freq={ '2190m' : '137500',
            '630m' : '475700',
            '160m' : '1838100',
            '80m' : '3594100',
            '60m' : '5288700', 
            '40m' : '7040100',
            '30m' : '10140200',
            '20m' : '14097100',
            '17m' : '18106100',
            '15m' : '21096100',
            '12m' : '24926100',
            '10m' : '28126100',
            '6m' : '50294500',
            '2m' : '144490000'
           }

# set variables
W_CLK=18
FQ_UD=23
DATA=24
RESET=25
freq_shift=12000/8192
offset=0
WORD1='00000001'#W0 multiplier6x, power up
WORD0='00000101'#W0 power down, multiplier6x

# setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(W_CLK,GPIO.OUT)
GPIO.setup(FQ_UD,GPIO.OUT)
GPIO.setup(DATA,GPIO.OUT)
GPIO.setup(RESET,GPIO.OUT) 

GPIO.output(DATA,0)

def reset():
    GPIO.output(RESET,1)
    GPIO.output(RESET,0)
    GPIO.output(W_CLK,1)
    GPIO.output(W_CLK,0)
    GPIO.output(FQ_UD,1)
    GPIO.output(FQ_UD,0)

def AD9851(freq,WORD,symbol):
    if freq > 70000000:
        print('AD9851: frequency must be lower than 70 mHz',file=sys.stderr) 
        sys.exit(-1)
    fsk=symbol*freq_shift #frequency shift key
    freq_word_int=int((freq+fsk)*(2**32)/(6*30e6+offset)) ##6xrefclock turned on in WORD0 
    FREQWORD='{0:032b}'.format(freq_word_int)
    SERIALWORD=WORD+FREQWORD
    for i in range(39,-1,-1):
        GPIO.output(W_CLK,0)
        if int(SERIALWORD[i]):
            GPIO.output(DATA,1)
        GPIO.output(W_CLK,1)
        GPIO.output(DATA,0)
        GPIO.output(W_CLK,0)
    GPIO.output(FQ_UD,1)
    GPIO.output(FQ_UD,0)
    return()

usage='wspr.py [options] callsign grid power[dBm] frequency1[Hz] <frequency2>...'
usage_freq='frequency in Hz or standard WSPR frequency e.g. "14097100" or "10m"' 

p = OptionParser(usage=usage)
p.add_option('-n','--no-delay', action='store_true', dest='nowait',
             help='Transmit immediately, do not wait for a WSPR TX window. '+\
             ' Used for testing only'
             )
p.add_option('-r','--repeat', action='store_true', dest='repeat',
             help='Repeat endless untill ctrl-c is pressed'
             )
p.add_option('-o','--offset', action='store_true', dest='offset',
             help='Add a random offset between -80 and 80 Hz from center frequency'
             )
p.add_option('-t','--testtone', action='store_true', dest='tone',
             help='Simply output a test tone at the specified frequency. '+\
             'For debugging and to verify calibration'
             )


(opts, args) = p.parse_args()


if opts.tone:
    frequencies = args[0:len(args)]
else:
    try:
        callsign = args[0]
        grid = args[1]
        power =args[2]
        frequencies = args[3:len(args)]
    except:
        print('Malformed arguments.',file=sys.stderr)
        print(usage, file=sys.stderr)
        sys.exit(-1)
 

    #frequency=int(frequency)    
    symbols=g.Genwsprcode(callsign,grid,power)
    symbols=symbols.rstrip(',')
    ##print('symbols\n',symbols)
    symbols=symbols.split(',')

reset()
if not opts.nowait or not opts.tone:
    print('Waiting for next WSPR TX window...')


while True:
    for frequency in frequencies:  #get the frequencies from the list
        try:
            frequency=int(wspr_freq[frequency]) #get known WSPR frequency
        except:
            try:
                frequency=int(frequency) #else it must be an integer value
            except:
                print('Malformed frequency.',file=sys.stderr) 
                print(usage_freq, file=sys.stderr)
                sys.exit(-1)
        
        if not opts.nowait: # check wether nowait
            past_time_window = (time.time() % 120)
            time.sleep(120-past_time_window)

        if frequency==0:
            print('Skipping transmission on:',time.strftime('%H:%M:%S',time.gmtime(time.time())))
            time.sleep(110)
        elif opts.tone:
            print('Start of test tone on:',time.strftime('%H:%M:%S',time.gmtime(time.time())))
            print('Frequency: {0:,.0f} Hz'.format(frequency))
            AD9851(frequency,WORD1,0)
            time.sleep(120)
            #AD9851(frequency,WORD0,0)
            reset()
            print('End of test tone on:',time.strftime('%H:%M:%S',time.gmtime(time.time())))
        else:
            if opts.offset:
                frequency=frequency+randrange(-80,81)

            print('Start of transmission on:',time.strftime('%H:%M:%S',time.gmtime(time.time())))
            print('Frequency: {0:,.0f} Hz'.format(frequency))

            for x in symbols: #modulate the symbols
                AD9851(frequency,WORD1,int(x))
                #print(x, end=',')
                time.sleep((1/freq_shift)-time.time() % (1/freq_shift))
            #AD9851(frequency,WORD0,int(x))
            reset()
            print('End of transmission on:',time.strftime('%H:%M:%S',time.gmtime(time.time())))
    if not opts.repeat:
        break
    
  
