# ==================================
# functions for interpolating notes !
import numpy as np
from scipy import interpolate as interp

def interpvals_to_freqs(p1,mNotes):
    y_min = min(p1)
    y_max = max(p1)
    # linear array of the possible data values
    #y_interp = np.linspace(y_min, y_max+(y_max-y_min)/len(self.mNotes), len(self.mNotes))
    p_interp = np.linspace(y_min, y_max, len(mNotes))
    p1_in_freq = np.interp(p1, p_interp, mNotes)
    return p1_in_freq

def findroots(time,p1_in_freq,mNotes):
    roots, notes = [], []
    x = time
    y = p1_in_freq
    values = mNotes

    for v in values:
        cs = interp.CubicSpline(x, y - v)
        v_roots = cs.roots()
        #v_roots = np.delete(v_roots,-1)
        for r in v_roots:
            if(r > 0):
                roots.append(r)
                notes.append(v)

    # Sort the notes according to occurence
    notes = np.asarray([x for (y,x) in sorted(zip(roots, notes))])
    times = np.asarray(sorted(roots))

    times_trim = times[times <= time[-1]]
    notes_trim = notes[times <= time[-1]]
    durations = times_trim[1:]-times_trim[:-1]
    # need to make durations the same length
    durs = np.zeros(len(notes_trim))
    durs[0:-1] = durations
    durs[-1] = time[-1] - times_trim[-1]
    del durations
    durations = durs
    return times_trim, notes_trim, durations

# make chords from the data.. output of owecianizer... 
def makeDataChord(mNotes,time,times,notes):
    ch_notes = []
    ch_times = []
    ch_durs = []

    for i,note in enumerate(mNotes):
        a = []
        a = times[notes==note]
        #print(a)
        if len(a)%2==0:
            #print('even')
            for i in range(len(a)):
                if (i)%2==0:
                    dur_a = a[i+1]-a[i]
                    ch_notes.append(note)
                    ch_times.append(a[i])
                    ch_durs.append(dur_a)
        elif len(a)%2==1:
            #print('odd')
            for i in range(len(a)):
                if i<len(a)-1:
                    if (i)%2==0:
                        dur_a = a[i+1]-a[i]
                        ch_notes.append(note)
                        ch_times.append(a[i])
                        ch_durs.append(dur_a)
                if len(a)==1:
                    dur_a = time[-1] - times[i]
                    ch_notes.append(note)
                    ch_times.append(a[i])
                    ch_durs.append(dur_a)

    return ch_notes, ch_times, ch_durs
