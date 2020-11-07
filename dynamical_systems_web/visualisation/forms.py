from django import forms
from . import models
from .models import System


class FormA(forms.ModelForm):
    class Meta:
        model = models.ParamA
        exclude = ['system']


class FormC(forms.ModelForm):
    class Meta:
        model = models.ParamC
        exclude = ['system']


class FormSystem(forms.Form):
    system = forms.ModelChoiceField(queryset=System.objects.all(), initial=0)


