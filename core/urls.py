from django.urls import path
from . import views
from . import ajax as ajax_views

app_name = 'core'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("create-profile", views.create_profile, name='create_profile'),
    path("profile", views.business_profile, name='profile'),
    path("products", views.products, name='products'),
    path("product-instances", views.product_instances, name='product_instances'),
    
    # ajax
    path('product-instance-chart', ajax_views.product_instances_chart_data),
    path("500", views.http_500),
]