from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': "form-control form-control-lg"}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': "form-control form-control-lg"}))


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': "form-control form-control-lg"}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': "form-control form-control-lg"}))
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'class': "form-control form-control-lg"}))
    password2 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'class': "form-control form-control-lg"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


