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
            self.add_error('password', 'Password not the same')
            self.add_error('confirm_password', 'Password not the same')
        if password and confirm_password and password == confirm_password:
            try:
                validate_password(password)
            except ValidationError as e:
                self.add_error('password', str(e))
                self.add_error('confirm_password', str(e))
        return cleaned_data
        

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