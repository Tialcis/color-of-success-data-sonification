# these functions are used for "sampling" the data for sound: extracting discrete pitch values and durations
import numpy as np
from bisect import bisect_left
from scipy import interpolate as interp
import copy

# first map the original data values to a new range that reflects the range of notes or frequencies. 
# then call this as 
# sp = Spline(x1, data_in_freqvals) # this interpolates the data smoothly over x1, whatever x is (time or space) 
# values = mNotes # (the values at which notes or pitches are defined-- can be chromatic or not, right?
# roots = sp.findroots(values) # this locates the times and indexes on the data curve at which the mNotes values occur

class Spline:
    def __init__(self, x, y, s=3):
        self.x = x
        self.y = y
        self.s = s
        self.tck, self.u = interp.splprep([self.x, self.y], s=s)
    
    def findroots(self, values):
        roots = []
        for v in values:
            tck = copy.deepcopy(self.tck)
            tck[1][1] = tck[1][1] - v
            t = tck[0]
            c = np.concatenate( (tck[1][1], np.array([0]*(len(t)-len(tck[1][1])), dtype=tck[1][1].dtype)))
            # z, m, ierr = interp.fitpack.dfitpack.sproot(t, c)
            z, m, ierr = interp.dfitpack.sproot(t, c)
            if m > 0:
                x, y = interp.splev(z[:m], self.tck)
                #roots += [[x[i], y[i]] for i in xrange(len(x))]
                roots += [[x[i], y[i]] for i in range(len(x))]
        roots = sorted(roots, key = lambda r: r[0])
        roots = np.asarray(roots)
        return roots
    
# define parameters dictionary
# bkh @cw: wtf is this? what does it do and why ? ? 
class structtype():
    pass

# THIS will be necessary when using non-chromatic scales 
# bkh @cw : why is this necessary? when is it used? 

#    Assumes myList is sorted. Returns closest value to myNumber.
#    If two numbers are equally close, return the smallest number.

def takeClosest(myList, myNumber):
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return after
    else:
       return before
