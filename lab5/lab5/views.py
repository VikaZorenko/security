from django.shortcuts  import render
from .forms import Userform
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from myapp.serializers import SensitiveDataSerializer


def registration(request):
    if request.method == 'POST':
        form = Userform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            get_user_model().objects.create_user(username = username, first_name = first_name, last_name = last_name, email= email, password= password)
            return HttpResponseRedirect('/')
    else:
        form = Userform()
    return render(request, 'registration.html', {'form':form})


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'oninput': 'setPasswordHash(event)'}), required=True, strip=False)
    password_hash = forms.CharField(widget=forms.HiddenInput(), max_length=64, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password_hash = self.cleaned_data.get('password_hash')

        if username is not None and password_hash:
            self.user_cache = authenticate(self.request, username=username, password=password_hash)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


def homepage_view(request):
    return render(request, 'home.html', {})


class DataAPIView(RetrieveUpdateDestroyAPIView, LoginRequiredMixin):
    serializer_class = SensitiveDataSerializer

    def get_object(self):
        return self.request.user.sensitive_data

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
