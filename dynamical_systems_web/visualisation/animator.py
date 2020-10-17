import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib
matplotlib.use('Agg')
from datetime import datetime
from django.conf import settings



class Animation():

    a = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

    init_state = [10, 0, 2] # for all functions
    visible = (0 ,1) # choose two functions
    t_span = (0, 6)



    # INTEGRATION

    def system(self, t, state):
        derivatives = np.zeros_like(state)
        for i in range(len(derivatives)):
            for j in range(len(derivatives)):
                derivatives[i] += self.a[i][j]*state[j]
        return derivatives

    def integrate(self):
        result = spi.solve_ivp(self.system, self.t_span, self.init_state, max_step=0.1)
        return result



    # CARTESIAN ANIMATION

    def animateCartesian(self, result):

        timeFig = plt.figure()
        timeAx = plt.axes()

        timeIms = []
        for t in range(len(result.t)):
            im1 = timeAx.plot(result.t[0:t], result.y[self.visible[0]][0:t], c='blue', animated=True)
            im2 = timeAx.plot(result.t[0:t], result.y[self.visible[1]][0:t], c='red', animated=True)
            timeIms.append(im1 + im2)

        timeAni = animation.ArtistAnimation(timeFig, timeIms, interval=50, blit=True,
                                        repeat_delay=1000)

        return timeAni



    # PHASE ANIMATION

    # phaseFig = plt.figure(2)
    # phaseAx = plt.axes()
    #
    #
    # phaseAx.plot(result.y[visible[0]], result.y[visible[1]])

    def set_a(self, a):
        self.a = a

    def createAnimations(self):
        result = self.integrate()

        # cartesian
        animation = self.animateCartesian(result)

        timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        filename = f"cartesianAnimation_{timestamp}.mp4"
        fullname = f"{settings.MEDIA_ROOT}/{filename}"

        animation.save(fullname)

        # phase
        filenames = filename,

        return filenames
