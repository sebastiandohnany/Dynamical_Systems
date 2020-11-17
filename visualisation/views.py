from django.shortcuts import render

from django.conf import settings
from . import animator
from . import forms
from . import models
import os
import shutil

from . import parser


# CURRENT SYSTEM LOGIC

system = None



# ============================
# VIEW
# ============================

def home(request):
    global system

    if not system:
        system = models.System.objects.get_or_create(name="Dance")[0]

    if request.method == 'POST' and 'new_system' in request.POST:
        form_new_system = forms.NewSystem(request.POST)
        if form_new_system.is_valid():
            new_system, created = models.System.objects.get_or_create(name=form_new_system.cleaned_data['name'])
            if created:
                system.parama.pk = None
                system.parama.system = new_system
                system.parama.save()
                system.paramc.pk = None
                system.paramc.system = new_system
                system.paramc.save()
                system.initialvalues.pk = None
                system.initialvalues.system = new_system
                system.initialvalues.save()
                system.timespan.pk = None
                system.timespan.system = new_system
                system.timespan.save()
                system.visible.pk = None
                system.visible.system = new_system
                system.visible.save()
                system.integrationmaxstep.pk = None
                system.integrationmaxstep.system = new_system
                system.integrationmaxstep.save()

                system = new_system

    form_new_system = forms.NewSystem()

    # if a POST to visualise
    if request.method == 'POST' and 'visualise' in request.POST:

        # create form instances and populate them with data from the request
        form_system = forms.FormSystem(initial={'system': system})
        form_a = forms.FormA(request.POST, instance=system.parama, prefix="form_a")
        form_c = forms.FormC(request.POST, instance=system.paramc, prefix="form_c")
        form_initialvalues = forms.FormInitialValues(request.POST, instance=system.initialvalues, prefix="form_initialvalues")
        form_timespan = forms.FormTimeSpan(request.POST, instance=system.timespan, prefix="form_timespan")
        form_visible = forms.FormVisible(request.POST, instance=system.visible, prefix="form_visible")
        form_ims = forms.FormIntegrationMaxStep(request.POST, instance=system.integrationmaxstep, prefix="form_integrationmaxstep")

        # check whether the forms are valid and process the data
        if form_a.is_valid() and form_c.is_valid() and form_initialvalues.is_valid() and form_timespan.is_valid() and form_visible.is_valid() and form_ims.is_valid():

            # save the forms
            form_a.save()
            form_c.save()
            form_initialvalues.save()
            form_timespan.save()
            form_visible.save()
            form_ims.save()

            # create animations
            filenames = createAnimations()
            cartesian_animation = settings.MEDIA_URL + filenames[0]
            phase_animation = settings.MEDIA_URL + filenames[1]

            return render(request, 'visualiser.html', {'form_a': form_a, 'form_c': form_c, 'form_system': form_system,
                                                       'form_new_system': form_new_system,
                                                       'form_initialvalues': form_initialvalues,
                                                       'form_timespan': form_timespan,
                                                       'form_visible': form_visible,
                                                       'form_ims': form_ims,
                                                       'cartesian_animation': cartesian_animation,
                                                       'phase_animation': phase_animation})

    # if a GET or POST with new SYSTEM
    else:
        if request.method == 'POST' and 'system' in request.POST:
            form_system = forms.FormSystem(request.POST)
            if form_system.is_valid():
                system = form_system.cleaned_data['system']

        # prepare forms from db
        form_system = forms.FormSystem(initial={'system': system})
        form_a = forms.FormA(instance=system.parama, prefix="form_a")
        form_c = forms.FormC(instance=system.paramc, prefix="form_c")
        form_initialvalues = forms.FormInitialValues(instance=system.initialvalues, prefix="form_initialvalues")
        form_timespan = forms.FormTimeSpan(instance=system.timespan, prefix="form_timespan")
        form_visible = forms.FormVisible(instance=system.visible, prefix="form_visible")
        form_ims = forms.FormIntegrationMaxStep(instance=system.integrationmaxstep, prefix="form_integrationmaxstep")

        # create animations
        filenames = createAnimations()
        cartesian_animation = settings.MEDIA_URL + filenames[0]
        phase_animation = settings.MEDIA_URL + filenames[1]

        # #TESTING
        # cartesian_animation = settings.MEDIA_URL + findNewestFiles()[0]
        # phase_animation = settings.MEDIA_URL + findNewestFiles()[1]

    return render(request, 'visualiser.html', {'form_a': form_a, 'form_c': form_c, 'form_system': form_system,
                                               'form_new_system': form_new_system,
                                               'form_initialvalues': form_initialvalues,
                                               'form_timespan': form_timespan,
                                               'form_visible': form_visible,
                                               'form_ims': form_ims,
                                               'cartesian_animation': cartesian_animation,
                                               'phase_animation': phase_animation})


# ============================
# ANIMATION
# ============================
def createAnimations():
    """
    Creates animator object, sets parameters and calls to generate animations.
    """
    # delete previous animations
    removeFiles()
    # prepare animator
    anim = animator.Animation()
    # a
    a = parser.parseA(system)
    anim.set_a(a)
    # c
    c = parser.parseC(system)
    anim.set_c(c)
    # initial values
    iv = parser.parseIV(system)
    anim.set_iv(iv)
    # timespan
    ts = parser.parseTS(system)
    anim.set_ts(ts)
    # visible
    v = parser.parseV(system)
    anim.set_v(v)
    # integration max step
    ims = parser.parseIMS(system)
    anim.set_ims(ims)

    # create
    filenames = anim.createAnimations()

    return filenames


# ============================
# FILE HANDLING
# ============================
def findNewestFiles():
    files = sorted(os.listdir(settings.MEDIA_ROOT))
    cartesian_files = [None]
    phase_files = [None]
    for file in files:
        if "cartesianAnimation" in file:
            cartesian_files.append(file)
        elif "phaseAnimation" in file:
            phase_files.append(file)

    return cartesian_files[-1], phase_files[-1]


def removeFiles():
    folder = settings.MEDIA_ROOT
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
