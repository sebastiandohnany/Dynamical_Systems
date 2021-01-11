from django.shortcuts import render

from django.conf import settings
from visualisation.logic import animator, parser
from visualisation.models import forms
from visualisation import models
import os
import shutil


# ============================
# HELPER
# ============================

def copyParameter(obj, new_system):
    obj.pk = None
    obj.system = new_system
    obj.save()


# ============================
# VIEW
# ============================
def home(request):

    if 'system' in request.session:
        system = models.System.objects.get(name=request.session['system'])
    else:
        system = models.System.objects.all()[0]

    # ============================
    # NEW SYSTEM
    # ============================
    if request.method == 'POST' and 'new_system' in request.POST:
        form_new_system = forms.NewSystem(request.POST)
        if form_new_system.is_valid():
            new_system, created = models.System.objects.get_or_create(name=form_new_system.cleaned_data['name'])
            if created:
                copyParameter(system.parama, new_system)
                copyParameter(system.paramc, new_system)
                copyParameter(system.initialvalues, new_system)
                copyParameter(system.timespan, new_system)
                copyParameter(system.visible, new_system)
                copyParameter(system.integrationmaxstep, new_system)
                copyParameter(system.description, new_system)

                system = new_system
                request.session['system'] = new_system.name

    form_new_system = forms.NewSystem()

    # ============================
    # POST: VISUALISE
    # ============================
    if request.method == 'POST' and 'visualise' in request.POST:

        # create form instances and populate them with data from the request
        form_system = forms.FormSystem(initial={'system': system})
        form_a = forms.FormA(request.POST, instance=system.parama, prefix="form_a")
        form_c = forms.FormC(request.POST, instance=system.paramc, prefix="form_c")
        form_initialvalues = forms.FormInitialValues(request.POST, instance=system.initialvalues, prefix="form_initialvalues")
        form_timespan = forms.FormTimeSpan(request.POST, instance=system.timespan, prefix="form_timespan")
        form_visible = forms.FormVisible(request.POST, instance=system.visible, prefix="form_visible")
        form_ims = forms.FormIntegrationMaxStep(request.POST, instance=system.integrationmaxstep, prefix="form_integrationmaxstep")
        form_description = forms.FormDescription(request.POST, instance=system.description, prefix="form_description")

        # check whether the forms are valid and process the data
        if form_a.is_valid() and form_c.is_valid() and form_initialvalues.is_valid() and form_timespan.is_valid() and form_visible.is_valid() and form_ims.is_valid() and form_description.is_valid():

            # save the forms
            form_a.save()
            form_c.save()
            form_initialvalues.save()
            form_timespan.save()
            form_visible.save()
            form_ims.save()
            form_description.save()

            # create animations
            filenames = createAnimations(system)
            cartesian_animation = settings.MEDIA_URL + filenames[0]
            phase_animation = settings.MEDIA_URL + filenames[1]

            return render(request, 'visualiser.html', {'form_a': form_a, 'form_c': form_c, 'form_system': form_system,
                                                       'form_new_system': form_new_system,
                                                       'form_initialvalues': form_initialvalues,
                                                       'form_timespan': form_timespan,
                                                       'form_visible': form_visible,
                                                       'form_ims': form_ims,
                                                       'form_description': form_description,
                                                       'cartesian_animation': cartesian_animation,
                                                       'phase_animation': phase_animation})

    # ============================
    # GET: ANIMATIONS
    # ============================
    else:

        # change system
        if request.method == 'POST' and 'change_system' in request.POST:
            form_system = forms.FormSystem(request.POST)
            if form_system.is_valid():
                system = form_system.cleaned_data['system']
                request.session['system'] = system.name

        # prepare forms from db
        form_system = forms.FormSystem(initial={'system': system})
        form_a = forms.FormA(instance=system.parama, prefix="form_a")
        form_c = forms.FormC(instance=system.paramc, prefix="form_c")
        form_initialvalues = forms.FormInitialValues(instance=system.initialvalues, prefix="form_initialvalues")
        form_timespan = forms.FormTimeSpan(instance=system.timespan, prefix="form_timespan")
        form_visible = forms.FormVisible(instance=system.visible, prefix="form_visible")
        form_ims = forms.FormIntegrationMaxStep(instance=system.integrationmaxstep, prefix="form_integrationmaxstep")
        form_description = forms.FormDescription(instance=system.description, prefix="form_description")

        # fetch animations or create
        try:
            filenames = findFiles(system.name)
            assert(filenames[0] != None)
            assert(filenames[1] != None)
        except:
            filenames = createAnimations(system)

        cartesian_animation = settings.MEDIA_URL + filenames[0]
        phase_animation = settings.MEDIA_URL + filenames[1]


    return render(request, 'visualiser.html', {'form_a': form_a, 'form_c': form_c, 'form_system': form_system,
                                               'form_new_system': form_new_system,
                                               'form_initialvalues': form_initialvalues,
                                               'form_timespan': form_timespan,
                                               'form_visible': form_visible,
                                               'form_ims': form_ims,
                                               'form_description': form_description,
                                               'cartesian_animation': cartesian_animation,
                                               'phase_animation': phase_animation})


# ============================
# ANIMATION
# ============================
def createAnimations(system):
    """
    Creates animator object, sets parameters and calls to generate animations.
    """
    # delete previous animations
    removeFiles(system.name)
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
    filenames = anim.createAnimations(system.name)

    return filenames


# ============================
# FILE HANDLING
# ============================
def findFiles(name):
    files = sorted(os.listdir(settings.MEDIA_ROOT))
    cartesian_files = [None]
    phase_files = [None]
    for file in files:
        if f"{name}_cartesianAnimation" in file:
            cartesian_files.append(file)
        elif f"{name}_phaseAnimation" in file:
            phase_files.append(file)

    return cartesian_files[-1], phase_files[-1]


def removeFiles(name):
    folder = settings.MEDIA_ROOT
    for filename in os.listdir(folder):
        if name in filename:
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
