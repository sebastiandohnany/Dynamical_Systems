from django.shortcuts import render
from django.http import HttpResponse
from .models import Matrix


def home(request):
    return render(request, 'visualiser.html')
