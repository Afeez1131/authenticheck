from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("register/", views.registration, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("one-time-login", views.send_one_time_login, name="send_one_time_login"),
    path("login/<token>", views.one_time_login, name="one_time_login"),
]
