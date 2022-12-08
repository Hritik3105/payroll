from django import forms
from payrollapp.models import *


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(
    attrs={
    'class':'form-control',
    'placeholder':'Email'
    }
))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
        'class':'form-control',
        'placeholder':'Password'
        }
    ))

    class Meta:
        model = User
        fields = ["email","password"]
        

