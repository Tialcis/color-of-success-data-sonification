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

xpos = 1.00
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


diversityArray = thePOCs[0]+thePOCs[1]+thePOCs[2]+thePOCs[3]+thePOCs[4]+theBinary[0]+theBinary[1]+theBinary[2]+theBinary[3]+theBinary[4]

# plt.subplot(1,1,1)
# plt.scatter(index, diversityArray)
# plt.xlabel('Movies 2006-2015 ')
# plt.ylabel('Diversity Points')
# # im = plt.imread("popcorn.jpg")
# # implot = plt.imshow(im, zorder=0)
# # plt.imshow(img, zorder=0)

# plt.show()
ind = 75
num_vals = 20

poc_vec = np.linspace(np.min(diversityArray),np.max(diversityArray),num_vals)
def color_getter(poc_val):
    #cmap = plt.get_cmap('inferno')
    cmap = cm.copper_r
    color_vec = np.linspace(0,1,num_vals)
    color_ind = np.interp(poc_val,poc_vec,color_vec)
    dot_col_T = cmap(color_ind)
    return dot_col_T

col0 = color_getter(diversityArray[ind])
print('dot_col_T = ' + str(col0) )

n_frames = 1000
print('num frames = ' + str(n_frames))
anim_dur = 98.0 # in seconds
print('anim_dur = ' + str(anim_dur))
frame_interval_sec = anim_dur/n_frames
print('frame_interval = ' + str(frame_interval_sec))
fps_ideal = 1./frame_interval_sec
print('frames per sec = ' + str(fps_ideal))

# ANIMATE 
# %matplotlib auto

# flag to determine whether anim gets viewed (0) or recorded (1), not both. 
view_or_write = 1

# to save, you must first install ffmpeg (and then restart the notebook engine)
anim_name = 'PocFunFinal.mp4'

fig2 = plt.figure(figsize=(5,5))

ax2 = fig2.add_subplot(111, aspect='equal')
bg_square = patches.Rectangle((0.0, 0.0),1.0,1.0,facecolor="blue")
ax2.add_patch(bg_square)
ax2.get_xaxis().set_visible(False)
ax2.get_yaxis().set_visible(False)

# img = plt.imread("popcorn.jpg")
# ax = fig2.add_subplot(111, aspect='equal')
# ax.imshow(img)

xpos = 1.00
# Creates a list containing 100 lists, each of 5 items, all set to 0
h = 100
w = 5;
Matrix = [[0 for x in range(w)] for y in range(h)]
movie = 0

for x in xPositions:
	print(movie)
	col = []
	col = color_getter(diversityArray[movie])
	divPoint = int(diversityArray[i]/2) 
	Matrix[movie][0] = patches.Circle((x, 0.90),0.075,facecolor="white")
	Matrix[movie][1] = patches.Circle((x, 0.70),0.075,facecolor="white")
	Matrix[movie][2] = patches.Circle((x, 0.50),0.075,facecolor="white")
	Matrix[movie][3] = patches.Circle((x, 0.30),0.075,facecolor="white")
	Matrix[movie][4] = patches.Circle((x, 0.10),0.075,facecolor="white")

	movie+=1
for i in range(0,100):
	print(movie)
	col = []
	col = color_getter(diversityArray[i])
	divPoint = int(diversityArray[i]/2) 
	ypos = 0.90
	for x in range(0,divPoint):
		Matrix[i][x] = patches.Circle((xPositions[i], ypos),0.1,facecolor=col)
		ypos -= .2
		ax2.add_patch(Matrix[i][x]);
	for x in range(divPoint,5):
		Matrix[i][x] = patches.Circle((xPositions[i], ypos),0.1,facecolor="blue")
		ypos -= .2
		ax2.add_patch(Matrix[i][x]);
# ===================================================
# initialize what will move in the animation
def init():

	return Matrix,

# ===================================================
# define what will move in the animation
def animate(i): # is this (i) needed for the animate function ? 
	print(i)
	for move in range(0,100):
		xPositions[move]-= 0.01
	for q in range(0,100):
		ypos = 0.90
		for x in range(0,5):
			Matrix[q][x].center = xPositions[q],ypos
			# ax2.add_patch(Matrix[i][x]);
			ypos -= 0.2  
	return Matrix,

if view_or_write==0:
    interv = (1000)*(dt)/5  
    print(interv)
elif view_or_write==1:
    interv = frame_interval_sec
    print(interv)

anim = animation.FuncAnimation(fig2, animate, 
                               init_func=init, 
                               frames=1000, 
                               interval=interv) #,repeat=False) 
#                               blit=True)

if view_or_write==0:
    plt.show()
elif view_or_write==1:
    anim.save(anim_name, fps=fps_ideal, dpi=480, extra_args=['-vcodec', 'h264','-pix_fmt', 'yuv420p'])
