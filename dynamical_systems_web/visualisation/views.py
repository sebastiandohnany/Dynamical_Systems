from django.shortcuts import render

from django.conf import settings
from . import animator
import math
from . import forms
from . import models
import os


def home(request):
    # if a POST (new data)
    if request.method == 'POST':

        # create a form instance and populate it with data from the request
        param_a = models.ParamA.objects.get(pk=1)  # default to the first
        form_a = forms.FormA(request.POST, instance=param_a)

        # check whether the form is valid and process the data
        if form_a.is_valid():

            # add the data to a system and save
            new_form_a = form_a.save(commit=False)
            new_form_a.system = models.System.objects.get(pk=1)
            new_form_a.save()

            # create animations
            filenames = createAnimations()
            cartesian_animation = settings.MEDIA_URL + filenames[0]

            return render(request, 'visualiser.html', {'form_a': form_a, 'cartesian_animation': cartesian_animation})

    # if a GET
    else:

        # prepare form from db
        param_a = models.ParamA.objects.get(pk=1)  # default to the first
        form_a = forms.FormA(instance=param_a)

        # create animations
        filenames = createAnimations()
        cartesian_animation = settings.MEDIA_URL + filenames[0]

    return render(request, 'visualiser.html', {'form_a': form_a, 'cartesian_animation': cartesian_animation})


def findNewestFiles():
    files = sorted(os.listdir(settings.MEDIA_ROOT))
    cartesian_files = []
    phase_files = []
    for file in files:
        if "cartesianAnimation" in file:
            cartesian_files.append(file)
        elif "phaseAnimation" in file:
            phase_files.append(file)

    return cartesian_files[-1], phase_files[-1]


def parseA():
    """
    Parser for ParamA table in database.
    :return: Matrix of parameters.
    """

    param_a = models.ParamA.objects.get(pk=1)  # default to the first

    # size of the data
    fields = param_a._meta.fields
    number_of_parameters = len(fields) - 2
    square_size = int(math.sqrt(number_of_parameters))

    # prepare to store the data
    a = [[0.0 for i in range(square_size)] for i in range(square_size)]

    # get the data
    for i in range(square_size):
        for j in range(square_size):
            field_name = f'a{i}{j}'
            a[i][j] = getattr(param_a, field_name)

    print(a)

    return a


def createAnimations():
    """
    Creates animator object, sets parameters and calls to generate animations.
    """
    # prepare animator
    anim = animator.Animation()
    # a
    a = parseA()
    anim.set_a(a)
    # create
    filenames = anim.createAnimations()

    return filenames
