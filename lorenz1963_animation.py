import numpy as np
from scipy import integrate

import matplotlib
matplotlib.use('TkAgg')

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation

N_trajectories = 1


def lorentz_deriv(value, t0, sigma=10., beta=8./3, rho=28.0):
    """Compute the time-derivative of a Lorentz system."""
    x, y, z = value
    x_dot = sigma * (y - x)
    y_dot = x * (rho - z) - y
    z_dot = x * y - beta * z
    return [ x_dot, y_dot, z_dot ]

# Choose random starting points, uniformly distributed from -15 to 15
np.random.seed(1)
x0 = -15 + 30 * np.random.random((N_trajectories, 3))
#x0 = -15 + 1 * np.random.random((N_trajectories, 3))

# Solve for the trajectories
t = np.linspace(0, 5, 2000)
x_t = np.asarray([integrate.odeint(lorentz_deriv, x0i, t) for x0i in x0])

# Set up figure & 3D axis for animation
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.axis('off')

# choose a different color for each trajectory
colors = plt.cm.jet(np.linspace(0, 1, N_trajectories))

# set up lines and points
lines = sum([ax.plot([], [], [], '-', c=c) for c in colors], [])
pts = sum([ax.plot([], [], [], 'o', c=c) for c in colors], [])

# prepare the axes limits
ax.set_xlim((-25, 25))
ax.set_ylim((-35, 35))
ax.set_zlim((5, 55))

# set point-of-view: specified by (altitude degrees, azimuth degrees)
ax.view_init(30, 0)

# initialization function: plot the background of each frame
def init():
    for line, pt in zip(lines, pts):
        line.set_data([], [])
        line.set_3d_properties([])

        pt.set_data([], [])
        pt.set_3d_properties([])
    return lines + pts

# animation function.  This will be called sequentially with the frame number
def animate(i):
    # we'll step ten time-steps per frame.  This leads to nice results.
    i = (2 * i) % x_t.shape[1]

    for line, pt, xi in zip(lines, pts, x_t):
        x, y, z = xi[:i].T
        line.set_data(x, y)
        line.set_3d_properties(z)

        pt.set_data(x[-1:], y[-1:])
        pt.set_3d_properties(z[-1:])

    ax.view_init(30, 0.2 * i)
    fig.canvas.draw()
    return lines + pts


# Setting the axes properties
ax.set_xlim3d([-25, 25])
ax.set_xlabel('X')

ax.set_ylim3d([-35, 35])
ax.set_ylabel('Y')

ax.set_zlim3d([5, 55])
ax.set_zlabel('Z')

ax.set_title('Lorenz 1963 Model ')

# instantiate the animator.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=1000, interval=10, blit=False)

# Save as mp4. This requires mplayer or ffmpeg to be installed
anim.save('video_lorenz.mp4', fps=20, extra_args=['-vcodec', 'libx264'])

plt.show()
