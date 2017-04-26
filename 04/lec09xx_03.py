import numpy as np
import matplotlib.pyplot as plt
# import mlab module to use MATLAB commands with the same names
import matplotlib.mlab as mlab
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

plt.style.use('ggplot')


# define init function for FuncAnimation
def init():
    global R, V, W, Rs, Vs, Ws, time
    R[:, :] = 0.0  # shape is (number, 3) x y z
    V[:, :] = 0.0
    W[:, :] = 0.0
    Rs[:, :, :, ] = 0.0  # shape is (num_steps, number, 3)
    Vs[:, :, :] = 0.0
    Ws[:, :, :] = 0.0
    time[:] = 0.0
    title.set_text('simulation')
    line.set_data([], [])  # set line data to show the trajectory
    line.set_3d_properties([])  # add z-data separatedly for 3d plot
    # set position current (x,y) position data for all particles
    particles.set_data([], [])
    # add current z data of particles to get 3d plot
    particles.set_3d_properties([])
    # return listed objects that will be drawn by FuncAnimation
    return particles, title, line


# Define animate function for FuncAnimation
def animate(i):
    global R, V, W, Rs, Vs, Ws, time
    time[i] = i * dt  # store time in each step in an array time
    W = std * np.random.randn(nump, dim)  # generate an array of random forces
    V = V * (1 - zeta / m * dt) + W / m  # update velocity via Ea (F9)
    R = R + V * dt  # update position
    Rs[i, :, :] = R  # store current position in step i
    Vs[i, :, :] = V  # store current velocity at step i
    Ws[i, :, :] = W  # store current random force as step i
    title.set_text(" t = {:.4f}s".format(time[i]))
    line.set_data(Rs[:i + 1, n, 0], Rs[:i + 1, n, 1])  # set line in  2D (x,y)
    # add z axis to set the line in 3D
    line.set_3d_properties(Rs[:i + 1, n, 2])
    # set the current position of all the particle in 3D
    particles.set_data(R[:, 0], R[:, 1])
    # add z axis to set the particle in 3d
    particles.set_3d_properties(R[:, 2])
    return particles, title, line  # return listed objects that will be draw

# set parameters and initialize variables
dim = 3  # x,y,z
nump = 1000  # number of particle
nums = 1024  # number of simulation steps

dt = 0.05
zeta = 1.0  # friction constant
m = 1.0  # mass
kBT = 1.0
std = np.sqrt(2 * kBT * zeta * dt)  # sigma
np.random.seed(0)
R = np.zeros((nump, dim))
V = np.zeros((nump, dim))
W = np.zeros((nump, dim))
Rs = np.zeros((nums, nump, dim))
Vs = np.zeros((nums, nump, dim))
Ws = np.zeros((nums, nump, dim))
time = np.zeros((nums,))

# perform and animate the simuation

fig = plt.figure(figsize=(10, 10))  # set fig size 10, 10 inch
ax = fig.add_subplot(111, projection='3d')
box = 40
ax.set_xlim((-box / 2.0, box / 2.0))
ax.set_ylim((-box / 2.0, box / 2.0))
ax.set_zlim((-box / 2.0, box / 2.0))
ax.set_xlabel('x', fontsize=20)
ax.set_ylabel('y', fontsize=20)
ax.set_zlabel('z', fontsize=20)

ax.view_init(elev=12, azim=120)
particles, = ax.plot([], [], [], 'ro', ms=8, alpha=0.5)  # define object
title = ax.text(-180, 0, 250, r'', transform=ax.transAxes,
                va='center')  # define object title
line, = ax.plot([], [], [], 'b', lw=1, alpha=0.8)  # define object line
n = 0  # trajectry line is plotted for the n-th particle
anim = animation.FuncAnimation(
    fig, func=animate, init_func=init, frames=nums, interval=5, blit=True, repeat=False)

# if your have ffmpeg installed on yout machine
# you can save the animation by uncomment the last line
# you may install ffmpeg by typing the following command in command prompt
# conda install -c menpo ffmpeg
