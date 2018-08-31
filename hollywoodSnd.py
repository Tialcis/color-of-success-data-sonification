import sys
sys.path.append('./modules/')
import os

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

from importlib import reload
from matplotlib import cm
import notepicker
import writeCmixSco_WT
reload(writeCmixSco_WT)
import writeCmixSco_GRAN
reload(writeCmixSco_GRAN)

from sklearn.cluster import KMeans
from subprocess import Popen
import subprocess as sp

# READ IN THE DATA FILE ! ! !

movies = pd.read_csv("../2_data/hollywood_data/newDataNewOrder.csv", delimiter=",")
moviesMoney = pd.read_csv("../2_data/hollywood_data/moviesMoney.csv", delimiter=",")

numMovies = 100

order = np.asarray(movies['order'])
gender = np.asarray(movies['gender'])
races = np.asarray(movies['races'])
isPoc = np.asarray(movies['poc'])
gross = np.asarray(moviesMoney['gross'])

index = np.zeros(numMovies)
x = 0
while x < numMovies:
	np.put(index, x, x+1)
	x = x + 1

xpos = 0.50
xPositions = []
for move in range(0,100):
	xPositions.append(xpos)
	xpos += 0.2

#I'm going to create two lists of Numpy Arrays. One of 5 arrays with POC vals and another with 5 arrays of gender vals
thePOCs = []
theBinary = []
count = 0

# For all 5 actors
while count < 5:
	thePOCs.append(np.zeros(numMovies))
	theBinary.append(np.zeros(numMovies))
	#Set the POC values for each in dif arrays
	for i in range(0,numMovies):
		if isPoc[i+(numMovies*count)] == 0:
			continue
		else:
			np.put(thePOCs[count], i, 1)

	#Set the gender values in another array
	for i in range(0,numMovies):
		if gender[i+(numMovies*count)] == "m":
			continue
		else:
			np.put(theBinary[count], i, 1)
	count = count + 1

print(thePOCs[1])
print(theBinary[1])

diversityArray = thePOCs[0]+thePOCs[1]+thePOCs[2]+thePOCs[3]+thePOCs[4]
genderArray = theBinary[0]+theBinary[1]+theBinary[2]+theBinary[3]+theBinary[4]

modes = {
    'ionian':[2,2,1,2,2,2,1],
    'dorian':[2,1,2,2,2,1,2],
    'phrygian':[1,2,2,2,1,2,2],
    'lydian':[2,2,2,1,2,2,1],
    'mixolydian':[2,2,1,2,2,1,2],
    'aeolian':[2,1,2,2,1,2,2],
    'lochrian':[1,2,2,1,2,2,2]
}

intervals = [0] + modes['phrygian'] + modes['phrygian'] # + modes['mixolydian']
print(intervals)
elements = np.cumsum(intervals[:-1])
print(elements)

C4 = 440.0 * 2**(3/12-1)
print(C4)

C5 = 523.251

def notename2freq(k,v,f0):
    freqs = f0*2**(v+k/12)
    return freqs

pitches = notename2freq(elements,-1,C4)
print(pitches)

reload(notepicker)
dur = 20.0
scale_note_dur = 1.0

div_freq = notepicker.interpvals_to_freqs(diversityArray,pitches)

indices, notes, durs = notepicker.findroots(index,div_freq,pitches)

for t in range(len(indices)):
    if indices[t] > index[-1]:
        indices[t] = index[-1]

ch_notes, ch_times, ch_durs = notepicker.makeDataChord(pitches,index,indices,notes)

for i in range(len(ch_notes)):
    plt.plot([ch_times[i],ch_times[i]+ch_durs[i]],[ch_notes[i],ch_notes[i]],'k-', linewidth=0.5)

reload(writeCmixSco_WT)
reload(writeCmixSco_GRAN)
base_name = 'test_dataChords2'
trim = -3
tones_dict = {}
tones_dict['times'] = np.asarray(ch_times[:trim])
tones_dict['notes'] = np.asarray(ch_notes[:trim])
tones_dict['durs'] = np.asarray(ch_durs[:trim])
tones_dict['amps'] = np.ones(len(ch_notes[:trim]))*2000
tones_dict['pans'] = np.ones(len(ch_notes[:trim]))*0.5

score_name = writeCmixSco_WT.writesco(tones_dict,base_name)
# score_name = writeCmixSco_GRAN.writeCmixSco_GRAN(tones_dict,base_name)
cmix_cmd = 'CMIX < ' + score_name
print(cmix_cmd)

# the ! tells the notebook to run a command in the terminal
os.system("pwd")
os.system("ls *.sco")
# or if that doesnt work, try this: 
ls_output = sp.check_output(['pwd'])

print(ls_output)
# but THIS works better ! 
os.system("pwd")

runCMIX = sp.Popen(cmix_cmd, shell=True) # if can only be called from a shell, use shell=True
runCMIX.wait()

#And again for the women
pitches2 = notename2freq(elements,-1,C6)
print(pitches2)

reload(notepicker)

gend_freq = notepicker.interpvals_to_freqs(genderArray,pitches2)

indices2, notes2, durs2 = notepicker.findroots(index,gend_freq,pitches2)

for t in range(len(indices2)):
    if indices2[t] > index[-1]:
        indices2[t] = index[-1]

ch_notes2, ch_times2, ch_durs2 = notepicker.makeDataChord(pitches2,index,indices2,notes2)

for i in range(len(ch_notes2)):
    plt.plot([ch_times2[i],ch_times2[i]+ch_durs2[i]],[ch_notes2[i],ch_notes2[i]],'k-', linewidth=0.5)

reload(writeCmixSco_WT)
reload(writeCmixSco_GRAN)
base_name = 'test_dataChords3'
trim = -3
tones_dict2 = {}
tones_dict2['times'] = np.asarray(ch_times2[:trim])
tones_dict2['notes'] = np.asarray(ch_notes2[:trim])
tones_dict2['durs'] = np.asarray(ch_durs2[:trim])
tones_dict2['amps'] = np.ones(len(ch_notes2[:trim]))*2000
tones_dict2['pans'] = np.ones(len(ch_notes2[:trim]))*0.5

score_name = writeCmixSco_WT.writesco(tones_dict2,base_name)
# score_name = writeCmixSco_GRAN.writeCmixSco_GRAN(tones_dict,base_name)
cmix_cmd = 'CMIX < ' + score_name
print(cmix_cmd)

# the ! tells the notebook to run a command in the terminal
os.system("pwd")
os.system("ls *.sco")
# or if that doesnt work, try this: 
ls_output = sp.check_output(['pwd'])

print(ls_output)
# but THIS works better ! 
os.system("pwd")

runCMIX2 = sp.Popen(cmix_cmd, shell=True) # if can only be called from a shell, use shell=True
runCMIX2.wait()

print("hopefully i just wrote your sound file; is it here?")
os.system("ls *.wav")


# img = plt.imread("popcorn.jpg")
# ax = plt.subplot()
# ax.imshow(img)