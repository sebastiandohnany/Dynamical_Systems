import matplotlib; matplotlib.use("TkAgg")  # for rendering
import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# data
a = [[-1, 2, -2],
     [2, 4, -1]]
init_state = [10, 0]
visible = (0, 1)
t_span = (0, 8)


# integration
def system(t, state):
    derivatives = np.zeros_like(state)
    for i in range(len(derivatives)):
        derivatives[i] += a[i][0]
        for j in range(0, len(derivatives)):
            derivatives[i] += a[i][j+1]*state[j]
    return derivatives


result = spi.solve_ivp(system, t_span, init_state, max_step=0.1)

# animation
timeFig = plt.figure(1)
timeAx = plt.axes()

timeIms = []
for t in range(len(result.t)):
    im1 = timeAx.plot(result.t[0:t], result.y[visible[0]][0:t], c='blue', animated=True)
    im2 = timeAx.plot(result.t[0:t], result.y[visible[1]][0:t], c='red', animated=True)
    timeIms.append(im1 + im2)

timeAni = animation.ArtistAnimation(timeFig, timeIms, interval=1, blit=True,
                                repeat_delay=1000)


# phaseFig = plt.figure(2)
# phaseAx = plt.axes()
#
#
# phaseAx.plot(result.y[visible[0]], result.y[visible[1]])

plt.show()
