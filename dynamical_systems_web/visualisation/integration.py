# import matplotlib; matplotlib.use("TkAgg")  # for rendering
import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

class Animation():
    # DEFAULT DATA

    a = [[-1, 2, -2, 0, 0, 0],
         [2, 4, -1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]

    init_state = [10, 0]
    visible = (0, 1)
    t_span = (0, 8)


    # INTEGRATION

    def system(self, t, state):
        derivatives = np.zeros_like(state)
        for i in range(len(derivatives)):
            derivatives[i] += self.a[i][0]
            for j in range(0, len(derivatives)):
                derivatives[i] += self.a[i][j+1]*state[j]
        return derivatives

    def integrate(self):
        result = spi.solve_ivp(self.system, self.t_span, self.init_state, max_step=0.1)
        return result





    # CARTESIAN ANIMATION

    def animateCartesian(self, result):

        timeFig = plt.figure(1)
        timeAx = plt.axes()

        timeIms = []
        for t in range(len(result.t)):
            im1 = timeAx.plot(result.t[0:t], result.y[self.visible[0]][0:t], c='blue', animated=True)
            im2 = timeAx.plot(result.t[0:t], result.y[self.visible[1]][0:t], c='red', animated=True)
            timeIms.append(im1 + im2)

        timeAni = animation.ArtistAnimation(timeFig, timeIms, interval=50, blit=True,
                                        repeat_delay=1000)

        return timeAni


    # phaseFig = plt.figure(2)
    # phaseAx = plt.axes()
    #
    #
    # phaseAx.plot(result.y[visible[0]], result.y[visible[1]])



    def createCartesianAnimation(self, data):
        self.a = data
        print(data)
        result = self.integrate()
        animation = self.animateCartesian(result)
        animation.save("static/cartesianAnimation.mp4")
        # HTMLanimation = animation.to_html5_video()

