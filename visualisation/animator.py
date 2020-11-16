# module imports
from django.conf import settings
from datetime import datetime

# maths imports
import scipy.integrate as spi
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# rendering and file settings
matplotlib.use('Agg')
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)


class Animation:
    """
    Integral calculation and animation module. Has default data which can be changed with setters and
    has a triggering method createAnimations() which runs a new calculation and generates animation mp4's
    with time signature.
    """

    # DEFAULT DATA
    c = [0, 0, 0, 0, 0]  # constants

    a = [[2, 3, 0, 0, 0],
         [-3, -1, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0]]  # linear

    init_state = [10, 15, 0, 0, 0]  # for all functions
    visible = (0, 1)  # choose two functions
    t_span = (0, 5)

    result = []

    # INTEGRATION
    def system(self, t, state):
        derivatives = np.zeros_like(state)  # prepare for new derivative values

        # constant
        for i in range(len(derivatives)):
            # adding value of the constant parameter
            derivatives[i] += self.c[i]

        # linear
        for i in range(len(derivatives)):
            for j in range(len(derivatives)):
                # adding value of the linear parameter multiplied with a corresponding function
                derivatives[i] += self.a[i][j] * state[j]

        return derivatives

    def integrate(self):
        result = spi.solve_ivp(self.system, self.t_span, self.init_state, max_step=0.1)
        self.result = result

    # CARTESIAN ANIMATION
    def animateCartesian(self):

        fig = plt.figure()  # prepare figure
        ax = plt.axes()  # prepare axes

        ims = []
        for t in range(len(self.result.t)):
            im1 = ax.plot(self.result.t[0:t], self.result.y[self.visible[0]][0:t], c='blue', animated=True)
            im2 = ax.plot(self.result.t[0:t], self.result.y[self.visible[1]][0:t], c='red', animated=True)
            ims.append(im1 + im2)

        time_ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                             repeat_delay=1000)

        return time_ani

    # PHASE ANIMATION
    def animatePhase(self):

        fig = plt.figure()  # prepare figure
        ax = plt.axes()  # prepare axes

        ims = []
        for t in range(len(self.result.t)):
            im = ax.plot(self.result.y[self.visible[0]][0:t], self.result.y[self.visible[1]][0:t],
                         c='blue', animated=True)
            ims.append(im)

        phase_ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                              repeat_delay=1000)

        return phase_ani


    def set_c(self, c):
        self.c = c

    def set_a(self, a):
        self.a = a

    def createAnimations(self, cartesian=True, phase=True):
        # integrate
        self.integrate()

        # timestamp
        timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")

        filenames = ()

        # cartesian
        if cartesian:
            cartesian_animation = self.animateCartesian()

            cartesian_filename = f"cartesianAnimation_{timestamp}.mp4"
            cartesian_fullname = f"{settings.MEDIA_ROOT}/{cartesian_filename}"

            cartesian_animation.save(cartesian_fullname, writer=writer)

            filenames += (cartesian_filename,)

        # phase
        if phase:
            phase_animation = self.animatePhase()

            phase_filename = f"phaseAnimation_{timestamp}.mp4"
            phase_fullname = f"{settings.MEDIA_ROOT}/{phase_filename}"

            phase_animation.save(phase_fullname, writer=writer)

            filenames += (phase_filename,)

        return filenames


# # testing
# anim = Animation()
# anim.integrate()
#
# # c = anim.animateCartesian()
# # c_filename = f"cartesianAnimation_test.mp4"
# # c_fullname = f"../animations/{c_filename}"
# # c.save(c_fullname, writer=writer)
#
# p = anim.animatePhase()
# p_filename = f"phaseAnimation_test.mp4"
# p_fullname = f"../animations/{p_filename}"
# p.save(p_fullname, writer=writer)
