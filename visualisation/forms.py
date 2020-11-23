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


class FormInitialValues(forms.ModelForm):
    class Meta:
        model = models.InitialValues
        exclude = ['system']


class FormTimeSpan(forms.ModelForm):
    class Meta:
        model = models.TimeSpan
        exclude = ['system']


class FormVisible(forms.ModelForm):
    class Meta:
        model = models.Visible
        exclude = ['system']


class FormIntegrationMaxStep(forms.ModelForm):
    class Meta:
        model = models.IntegrationMaxStep
        exclude = ['system']



class FormSystem(forms.Form):
    system = forms.ModelChoiceField(queryset=System.objects.all())


class NewSystem(forms.Form):
    name = forms.CharField(initial='New System')


class FormDescription(forms.ModelForm):
    class Meta:
        model = models.Description
        exclude = ['system']




