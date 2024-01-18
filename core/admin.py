from django.contrib import admin
from .models import Business, Product, ProductInstance


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "website", "email", "created"]
    list_filter = ["created"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "created", "shelf_life"]
    list_filter = ["created"]


@admin.register(ProductInstance)
class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ["product", "manufactured", "expiry_date"]
    list_filter = ["manufactured", "expiry_date"]