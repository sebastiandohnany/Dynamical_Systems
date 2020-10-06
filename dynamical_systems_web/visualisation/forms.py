from django import forms

class DataForm(forms.Form):
    a00 = forms.FloatField(label='a00')
    a01 = forms.FloatField(label='a01')
    a02 = forms.FloatField(label='a02')

    a10 = forms.FloatField(label='a10')
    a11 = forms.FloatField(label='a11')
    a12 = forms.FloatField(label='a12')

    a20 = forms.FloatField(label='a20')
    a21 = forms.FloatField(label='a21')
    a22 = forms.FloatField(label='a22')