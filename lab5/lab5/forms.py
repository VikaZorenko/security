from django import forms
from django.contrib.auth import get_user_model


class Userform(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Enter Username'}
        ), required=True, max_length=50)
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class':'form-control','placeholder':'Enter email id'}
        ), required=True, max_length=50)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Enter First Name'}
        ), required=True, max_length=50)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Enter Last Name'}
        ), required=True, max_length=50)
    password_no_hash = forms.CharField(label="Password:", widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder':'Enter Password', 'oninput': 'setPasswordHash(event)', 'onchange': 'setPasswordStrength(event)'}
        ), required=True)
    password = forms.CharField(widget=forms.HiddenInput(), max_length=64, required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
