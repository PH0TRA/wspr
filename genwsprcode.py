#!/usr/bin/env python
#
# $Id$
#
# genwspr
#
# A program which generates the tone sequence needed for a particular 
# beacon message.
#
##Very little error checking is done on this, so you better make sure
##that the callsign and gridsquare are of the appropriate form.
##
##Callsigns must be 2x3, 1x3, 2x1, or 1x2 for the purposes of this 
##code.
##
##Original code written by Mark VandeWettering K6HX https://github.com/brainwagon/genwspr

#converted to module for Python3 july 2017 by Marc Burgmeijer PH0TRA

import sys, os, re, string 


syncv = [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0,
1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0,
0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1,
0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1,
0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0,
0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0,
0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0]


class Genwsprcode:
    '''A program which generates the tone sequence needed for a particular beacon message.''' 

    def __new__(self, callsign, grid, power):
        self.__callsign=callsign
        self.__grid=grid 
        self.__power=power  
    
        def normalizecallsign(callsign):
            callsign = list(callsign)
            idx = None
            for i, ch in enumerate(callsign):
                if ch in string.digits:
                    idx = i
            newcallsign = 6 * [" "]
            newcallsign[2-idx:2-idx+len(callsign)] = callsign
            return ''.join(newcallsign)

        def encodecallsign(callsign):
            callsign=callsign.upper()
            callsign = normalizecallsign(callsign)
            lds = string.digits + string.ascii_uppercase + " "
            ld = string.digits + string.ascii_uppercase
            d = string.digits
            ls = string.ascii_uppercase + " "
            acc = lds.find(callsign[0])
            acc *= len(ld)
            acc += ld.find(callsign[1])
            acc *= len(d)
            acc += d.find(callsign[2])
            acc *= len(ls)
            acc += ls.find(callsign[3])
            acc *= len(ls)
            acc += ls.find(callsign[4])
            acc *= len(ls)
            acc += ls.find(callsign[5])
            return tobin(acc, 28) 

        def tobin(v, l):
            return('{0:0{width}b}'.format(v,width=l)) 

        def grid2ll(grid):
            if gridsquarepat.match(grid):
                # go ahead and decode it.
                p = (ord(grid[0])-ord('A'))
                p *= 10
                p += (ord(grid[2])-ord('0'))
                p *= 24
                if len(grid) == 4:
                    p += 12
                else:
                    p += (ord(grid[4])-ord('a')) + 0.5
                lng = (p / 12) - 180.0
                p = (ord(grid[1])-ord('A'))
                p *= 10
                p += (ord(grid[3])-ord('0'))
                p *= 24
                if len(grid) == 4:
                    p += 12
                else:
                    p += (ord(grid[5])-ord('a')) + 0.5
                lat = (p / 24) - 90.0
                return (lat, lng)
            else:               
                raise RuntimeError('Malformed grid referense ',grid)

        def encodegrid(grid):
            grid=grid.upper()
            lat, long = grid2ll(grid)
            long = int((180 - long) / 2.0)
            lat = int(lat + 90.)
            return tobin(long * 180 + lat, 15)

        def encodepower(power):
            if power.isdigit() and len(power)==2:
                power = int(power)
                power = power + 64
                return tobin(power, 7)
            else:               
                raise RuntimeError('Malformed power value ',power)
        
        def convolver(bit ,acc): 
            acc = ((acc << 1) & 0xFFFFFFFF) | bit 
            return parity(acc & 0xf2d05351), parity(acc & 0xe4613c47), acc
        
        def encode(l):
            f = []
            acc=0
            l = list(map(lambda x : int(x), list(l)))
            for x in l:
                b0, b1, acc = convolver(x, acc)
                f.append(b0)
                f.append(b1)
            return f
        
        def parity(x):
            sx = x 
            even = 0
            while x:
                even = 1 - even
                x = x & (x - 1)
            return even
        
        def bitstring(x):
            return ''.join([str((x>>i)&1) for i in (7, 6, 5, 4, 3, 2, 1, 0)])

        def bitreverse(x):
            bs = bitstring(x)
            return int(bs[::-1], 2)

        gridsquarepat = re.compile("[A-R][A-R][0-9][0-9]([a-x][a-x])?$")

        idx = range(0, 256)

        ridx = list(filter(lambda x : x < 162, map(lambda x : bitreverse(x), idx))) 

        usage="genwspr [options] callsign grid power"

        try:
                callsign, grid, power ## need to check power format
        except:
                print("Malformed arguments.",file=sys.stderr)
                print(usage, file=sys.stderr)
                sys.exit(-1)

        callsign = encodecallsign(callsign)
        grid = encodegrid(grid)
        power = encodepower(power)
        message = callsign + grid + power + 31 * '0'

        message =  encode(message)

        # interleave...
        imessage = 162 * [0]

        for x in range(162):
            imessage[ridx[x]] = message[x]  ## python 2.7
        
        t = [ "%d," % (2*x+y) for x, y in zip(imessage, syncv) ]

        symbols=''.join(t)

        return(symbols)

        # $Log$
