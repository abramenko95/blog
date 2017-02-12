from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'required':''}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [ 'middle_name', 'phone_number', 'about', 'avatar' ]
        widgets = {
            forms.TextInput(attrs={'enctype':'multipart/form-data'})
        }