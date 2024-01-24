from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("create-profile", views.create_profile, name='create_profile'),
    path("update-profile", views.profile, name='profile'),
    path("products", views.products, name='products'),
    path("product-instances", views.product_instances, name='product_instances'),
    path("500", views.http_500),
]