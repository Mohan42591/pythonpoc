

from django import forms 
 

class Googlemapsform(forms.Form):
    name = forms.CharField(label='Enter your name', max_length=100)
    