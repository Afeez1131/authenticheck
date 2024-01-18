from django import forms
from .models import Business, Product, ProductInstance


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ["name", "description", "address", "phone", "website", "email"]
        labels = {
            "name": "Business Name",
            "description": "About Business",
            "address": "Location",
            "phone": "Business Hotline",
            "website": "Website URL",
            "email": "Business Email"
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Business Name"}),
            "description": forms.TextArea(attrs={"class": "form-control", "placeholder": "Business Description", "rows": "5", "cols": "10"}),
            "address": forms.TextArea(attrs={"class": "form-control", "placeholder": "Business Address", "rows": "5", "cols": "10"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Business Phone"}),
            "website": forms.TextInput(attrs={"class": "form-control", "placeholder": "Business Website"}),
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "Business E-mail"}),

        }