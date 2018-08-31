import numpy as np
import math
import matplotlib.pyplot as plt
# the animation modules from matplotlib
import matplotlib.animation as animation
import matplotlib.patches as patches

import subprocess as sp
import sys
sys.path.append('./modules/')
from importlib import reload
import graphDist
import notepicker as npkr
reload(npkr)
import writeCmixSco_WT as write_wt

# ===========================================================
# READ IN THE DATA FILE ! ! !

breath = np.loadtxt("../2_data/data_examples/breath_BH_y1701_1.txt")
time = breath[:,0]
temp_C = breath[:,1]
humidity = breath[:,2]

plot_data = 0
if plot_data == 1:
    # PLOT THE DATA AS CURVES...
    fig = plt.figure(figsize=(10,8))

    plt.subplot(2,1,1)
    plt.plot(time,humidity,'b-')
    #plt.xlabel('time')
    plt.ylabel('H humidity [%]')

    plt.subplot(2,1,2)
    plt.plot(time,temp_C,'r-')
    plt.xlabel('time [seconds] ')
    plt.ylabel('T temperature [C]')

    plt.show()

dt =  time[-1]-time[-2]
print(dt)
print(len(time))
print(dt*len(time))
print(time[-1])

# determine the time for the soundtrack
movie_dur = 30.0
time_movie = np.linspace(0.0,movie_dur,len(time))

# (1) determine the pitches to be found in the interpolated data
n_octaves_total = 2.0
root_note  = 220.0
top_note = root_note*(2**n_octaves_total)
interval = 2.0**(1./12.)
notes2find = np.logspace(np.log2(root_note), np.log2(top_note), num=3*12, base=2.0)

# (2) Interpolate the y-values to a range of frequency (using notepicker !)
p1_in_freq = npkr.interpvals_to_freqs(temp_C,notes2find)

# (3) Find where in time these values occur, use these as our start times and durations.
# this is the owecianizer:
times, notes, durations = npkr.findroots(time_movie,p1_in_freq,notes2find)

# (4) scale the note durations
# (this changes the total time of the soundtrack *only* because of the last note,
# i.e. does not change the start times)
scale_note_dur = 0.95
durs = durations*scale_note_dur

# ==================================================
# plot the results:
plot_notes = 1
if plot_notes==1:
    fig2 = plt.figure(figsize=(10,8))
    plt.plot(times,notes,'ko')

    for ind,t in enumerate(times):
        plt.plot([t,t],[min(notes),notes[ind]],'k-',linewidth=0.5)
        plt.plot([0,t],[notes[ind],notes[ind]],'r-',linewidth=0.5)

    plt.xlabel('score time')
    plt.ylabel('pitches (T temperature)')
    plt.show()

# ==================================================
# GENERATE THE RTcmix score ! (alternate to generating the midi score)
base_name = 'breath_Temp_WT_test'
tones_dict = {}
tones_dict['times'] = np.asarray(times)
tones_dict['notes'] = np.asarray(notes)
tones_dict['durs'] = np.asarray(durs)
tones_dict['amps'] = np.ones(len(notes))*2000
tones_dict['pans'] = np.ones(len(notes))*0.5

score_name = write_wt.writesco(tones_dict,base_name)

cmix_cmd = 'CMIX < ' + score_name
print(cmix_cmd)
# play the sound !
runCMIX = sp.Popen(cmix_cmd, shell=True) # if can only be called from a shell, use shell=True
runCMIX.wait() # not sure what this does.



# NOT USED
# owecianizer version:
# sp = owc.owecianizer(x=time_movie, y=temp_C, notes2find=notes2find)
# notes, times, durs, yvalues_in_freq = sp.findroots()
