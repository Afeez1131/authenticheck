import logging
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.views import LogoutView
from braces.views import LoginRequiredMixin
from django.template.loader import render_to_string
from account.models import OneTimeLogin
from account.utils import create_one_time_login, generate_token, send_html_mail
from .forms import OneTimeLoginForm, RegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.conf import settings

logger = logging.getLogger(__name__)


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = "account/register.html"
    success_url = reverse_lazy("account:login")

    def form_valid(self, form):
        User.objects.create_user(**form.cleaned_data)
        messages.success(self.request, "Registration Successful")
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

registration = RegistrationView.as_view()


class LoginView(FormView):
    form_class = LoginForm
    template_name = "account/login.html"
    success_url = reverse_lazy("core:dashboard")

    def form_valid(self, form):
        username = form.cleaned_data.get("username", "")
        _next = self.request.GET.get("next", "")
        password = form.cleaned_data.get("password", "")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            if _next:
                return HttpResponseRedirect(_next)
            else:
                return super().form_valid(form)
        messages.error(self.request, "Username and/or password incorrect")
        return super().form_invalid(form)


login_user = LoginView.as_view()


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse("account:login"))


logout_user = LogoutView.as_view()


class SendOneTimeLoginView(FormView):
    template_name = "account/send_one_time_login.html"
    form_class = OneTimeLoginForm

    def get_success_url(self):
        logger.info("in the success URL.")
        messages.success(
            self.request,
            "An email containing your One Time Password would be sent to the mail provided if valid.",
        )
        return HttpResponseRedirect(self.request.build_absolute_uri())

    def form_valid(self, form):
        email = form.cleaned_data.get("email", "")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return super().form_valid(form)
        token = generate_token(user.id)
        create_one_time_login(user.id, token)
        login_link = self.request.build_absolute_uri(
            reverse("account:one_time_login", args=[token])
        )
        context = {"user": user, "login_link": login_link}
        html = render_to_string("account/one_time_login_mail.html", context)
        plain = render_to_string("account/one_time_login_mail.txt", context)
        logger.info(f"{plain}")
        subject = "One-Time Login Request"
        send_html_mail(subject, settings.SERVER_EMAIL, user.email, html, plain)
        return super().form_valid(form)


send_one_time_login = SendOneTimeLoginView.as_view()


class OneTimeLoginView(FormView):
    template_name = "account/one_time_login.html"
    form_class = OneTimeLoginForm
    success_url = reverse_lazy("core:dashboard")
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email", "")
        token = self.kwargs.get("token", "")
        logger.info(f'email: {email}, token:  {token}')
        try:
            otl = OneTimeLogin.objects.get(token=token, user__email=email)
        except OneTimeLogin.DoesNotExist:
            logger.info("does not exist.")
            messages.error(self.request, "invalid request")
            return HttpResponseRedirect(self.request.build_absolute_uri())
        user = otl.user        
        if token and default_token_generator.check_token(otl.user, token):
            otl.delete()
            login(self.request, user)
            return super().post(request, *args, **kwargs)
        else:
            messages.error(self.request, "invalid request")
        return HttpResponseRedirect(self.request.build_absolute_uri())
        # return super().post(request, *args, **kwargs)



one_time_login = OneTimeLoginView.as_view()
