from django.shortcuts import render
from .models import Matrix
from . import integration

import math

from .forms import DataForm


def home(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DataForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # save the data to database
            # cartesianAnimation = cartesianAnimation(form)
            size = int(math.sqrt(len(form.cleaned_data)))
            data = [[0 for i in range(size)] for i in range(size)]
            for a in form.cleaned_data:
                data[int(a[1])][int(a[2])] = form.cleaned_data[a]
            anim = integration.Animation()
            anim.createCartesianAnimation(data)
            # ...
            # redirect to a new URL:
            return render(request, 'visualiser.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DataForm()

    return render(request, 'visualiser.html', {'form': form})


# def cartesianAnimation(form):
#     # form -> data
#     cartesianAnimation = integration.createCartesianAnimation()
#     return cartesianAnimation
