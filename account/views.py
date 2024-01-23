from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.views import LogoutView
from braces.views import LoginRequiredMixin
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'account/register.html'

    def form_valid(self, form):
        messages.success(self.request, 'User Created success')
        return super().form_valid(form)
    
registration = RegistrationView.as_view()


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'
    success_url = reverse_lazy('core:dashboard')

    def form_valid(self, form):
        username = form.cleaned_data.get('username', '')
        password = form.cleaned_data.get('password', '')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.requeest, user)
            return super().form_valid(form)
        messages.error(self.request, "Username and/or password incorrect")
        return super().form_invalid(form)
    
login_user = LoginView.as_view()


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('account:login'))

logout_user = LogoutView.as_view()