from django.urls import path
from . import views
from . import ajax as ajax_views

app_name = 'core'

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("create-profile", views.create_profile, name='create_profile'),
    path("profile", views.business_profile, name='profile'),
    path("products", views.products, name='products'),
    path("update-product", views.update_product, name='update_product'),
    path("delete-product", views.delete_product, name='delete_product'),
    path("products/<int:pk>", views.product_instances, name='product_instances'),
    path("update-instance", views.update_product_instance, name='update_product_instance'),
    path("delete-instance", views.delete_product_instance, name='delete_product_instance'),
    
    path("download-qr/<model_name>", views.download_qr, name='download_qr'),
    path("download-qr-png/<model_name>", views.download_qr_png, name='download_qr_png'),
    
    
    # ajax
    path('product-instance-chart', ajax_views.product_instances_chart_data),
    path("500", views.http_500),
]