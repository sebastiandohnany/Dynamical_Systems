from django import forms
from visualisation import models


class FormA(forms.ModelForm):
    class Meta:
        model = models.ParamA
        exclude = ['system']


