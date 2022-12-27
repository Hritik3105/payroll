from django.forms import ModelForm
from django import forms
from payrollapp.models import *


class AddCreateForm(ModelForm):
    username = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter your name'
        }
    ))
    
    email = forms.CharField(required = True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter your address'
        }
    ))
    password = forms.CharField(required = True,widget=forms.PasswordInput(
        attrs={
        'class':'form-control',
        'placeholder':'Enter your password'
        }
    ))

   
    class Meta:
        model = User
        fields = ["username","email","password"]


    def clean(self):
 
        # data from the form is fetched using super function
        super(AddCreateForm, self).clean()
         
        # extract the username and text field from the data
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
 
        # conditions to be met for the username length
        if username == "":
            self._errors['username'] = self.error_class([
                'This Field is required'])
        if email == "":
            self._errors['email'] = self.error_class([
                'This Field is required'])
        if password == "":
            self._errors['password'] = self.error_class([
                'This Field is required'])
 
        # return any errors if found
        return self.cleaned_data



        
        