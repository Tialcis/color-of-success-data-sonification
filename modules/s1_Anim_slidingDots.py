# all the packages and modules we'll need for now. will import more later.
import numpy as np
import math
import matplotlib.pyplot as plt

# the animation modules from matplotlib
import matplotlib.animation as animation
import matplotlib.patches as patches

import sys
sys.path.append('./modules/')
from importlib import reload
import graphDist
import notepicker as npkr
reload(npkr)

# ===========================================================
# READ IN THE DATA FILE ! ! !
#breath = np.loadtxt("./data/breath_CW2.txt")
breath = np.loadtxt("../2_data/data_examples/breath_BH_y1701_1.txt")
time = breath[:,0]
temp_C = breath[:,1]
humidity = breath[:,2]

dt =  time[-1]-time[-2]
print(dt)
print(len(time))
print(dt*len(time))
print(time[-1])

# ===========================================================
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

# ==================================================
# initialize the objects
fig2 = plt.figure(figsize=(6,6))
axes1 = plt.subplot(1,1,1)

axes1.plot(temp_C,humidity,'b-')
axes1.set_xlabel('T, temperature [C]')
axes1.set_ylabel('H, humidity [%]')


# here we are using the class above to scale the ellipse axes to the data so they are round dots.
rad_pix = 20
dot1_width = graphDist.GraphDist(rad_pix, axes1, True)
dot1_height = graphDist.GraphDist(rad_pix, axes1, False)
patch1 = patches.Ellipse((temp_C[0], humidity[0]), dot1_width, dot1_height, fc='red')

# ===================================================
# initialize what will move in the animation
def init():
    patch1.center = (temp_C[0], humidity[0])
    axes1.add_patch(patch1)
    return patch1

# ===================================================
# define what will move in the animation
def animate(i): # is this (i) needed for the animate function
    x , y = temp_C[i], humidity[i]
    patch1.center = (x , y)
    axes1.add_patch(patch1)
    return patch1,

# ====================================================
# RUN the animation !
# flag to determine whether movie gets viewed (0) or recorded (1), not both.
view_or_write = 1
# to save, you must first install ffmpeg (and then restart the notebook engine)
path_to_save = './'
movie_name = 's1_slidingDot.mp4'
movie_dur = 30.0 # in seconds

# figure out the movie frame interval
n_frames = len(humidity)
print('num frames = ' + str(n_frames))
print('movie_dur = ' + str(movie_dur))
frame_interval_sec = movie_dur/n_frames
print('frame_interval = ' + str(frame_interval_sec))
fps_ideal = 1./frame_interval_sec
print('frames per sec = ' + str(fps_ideal))

if view_or_write==0:
    interv = (1000)*(dt)/5
    print(interv)
elif view_or_write==1:
    interv = frame_interval_sec
    print(interv)

anim = animation.FuncAnimation(fig2, animate,
                               init_func=init,
                               frames=len(humidity),
                               interval=interv) #,repeat=False)
#                               blit=True)

if view_or_write==0:
    plt.show()
elif view_or_write==1:
    anim.save(path_to_save+movie_name, fps=fps_ideal, extra_args=['-vcodec', 'h264','-pix_fmt', 'yuv420p'])

#ani = animation.FuncAnimation(fig, animate, np.arange(0, len(time)-1), interval=interv, init_func=init)# ,blit=True)
