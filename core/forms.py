from django import forms
from .models import Business, Product, ProductInstance
from django.utils import timezone
from datetime import timedelta


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ["name",  "phone", "website", "email", "address", "description",]
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
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Business Description", "rows": "5", "cols": "10"}),
            "address": forms.Textarea(attrs={"class": "form-control", "placeholder": "Business Address", "rows": "5", "cols": "10"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Business Phone"}),
            "website": forms.TextInput(attrs={"class": "form-control", "placeholder": "Business Website"}),
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "Business E-mail"}),

        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "shelf_life", "category"]
        labels = {
            "name": "Product Name",
            "description": "Product Description",
            "price": "Price of Product",
            "shelf_life": "Shelf Life of Product",
            "category": "Product Category"
        }
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Product Name"}),
            "description": forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Product Description", "rows": 5, "cols": 10}),
            "price": forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Product Price", "min": 0}),
            "shelf_life": forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Product Expected Shelf Life", "min": 0}),
            "category": forms.Select(attrs={'class': 'select2 w-100'})
        }
    
    def clean(self):
        self.cleaned_data = super().clean()
        name = self.cleaned_data.get('name', '')
        price = self.cleaned_data.get('price', '')
        shelf_life = self.cleaned_data.get('shelf_life', '')
        if not self.instance.pk and name and Product.objects.filter(name=name).exists():
            self.add_error('name', f'Product with name {name} exists.')
        try:
            shelf_life = int(shelf_life)
        except ValueError:
            self.add_error('shelf_life', f'Invalid Shelf Life {shelf_life}')
        try:
            price = int(price)
        except ValueError:
            self.add_error('price', f'Invalid Price {price}')
        
        return self.cleaned_data


class ProductInstanceForm(forms.ModelForm):
    class Meta:
        model = ProductInstance
        fields = ["product", "manufactured"]
        labels = {
            "product": "Product",
            "manufactured": "Manufactured Date",
        }
        widgets = {
            "product": forms.Select(attrs={'class': 'form-select'}),
            "manufactured": forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def clean(self):
        self.cleaned_data = super().clean()
        manufactured = self.cleaned_data.get("manufactured", "")
        if not manufactured:
            self.add_error('manufactured', "Manufactured field is compulsory.")
        # if manufactured and manufactured.date() != timezone.now().date():
        #     self.add_error("manufactured", "Manufactured date should be the same as today.")
        return self.cleaned_data