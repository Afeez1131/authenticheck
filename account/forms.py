from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    email = forms.EmailField(max_length=155, required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Email'}))
    password = forms.CharField(max_length=155, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(max_length=155, required=True, 
    label='Confirm Password', 
    widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Repeat Password'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', '')
        password = cleaned_data.get('password', '')
        confirm_password = cleaned_data.get('confirm_password', '')
        if User.objects.filter(email__iexact=email).exists():
            self.add_error('email', 'User with this Email exists.')
        if password != confirm_password:
            self.add_error('password', 'Password and Confirm Password not the same')
        if password and confirm_password and password == confirm_password:
            try:
                validate_password(password)
            except ValidationError as e:
                self.add_error('password', str(e))
        return {"username": email, "password": password, "email": email}
        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=55,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control form-control-lg', 
                                       'placeholder': 'Username'
                                       }
                            ))
    password = forms.CharField(max_length=55,
                               widget=forms.PasswordInput(
                                   attrs={
                                       'class': 'form-control form-control-lg', 
                                       'placeholder': 'Password'
                                       }
                            ))
    

class OneTimeLoginForm(forms.Form):
    email = forms.CharField(max_length=155,
                            label="Email used for Registration",
                            widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg',
                                                           'placeholder': 'E-mail'}))
    

    # def clean(self):
    #     email = self.cleaned_data.get('email', '')
    #     if not User.objects.filter(email=email).exists()
    
"""
generics.edit.FormView:
- user when you are working with a form that you are not calling save on, 
i.e form.save()
- use in situation where you are getting the form fields for processing by yoursefl and 
e.g. Login, Registration.

CreateView:
different between CreateVIew and FormView is that you can call .save on a CreateView
- you can also get the field for processing by yourself,
- can also be used in Login, Registration view, but not efficient.
"""