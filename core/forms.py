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
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Business Description", "rows": "5", "cols": "10"}),
            "address": forms.Textarea(attrs={"class": "form-control", "placeholder": "Business Address", "rows": "5", "cols": "10"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Business Phone"}),
            "website": forms.TextInput(attrs={"class": "form-control", "placeholder": "Business Website"}),
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "Business E-mail"}),

        }


class ProductForms(forms.ModelForm):
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
            "price": forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Product Price"}),
            "shelf_life": forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Product Expected Shelf Life"}),
            "category": forms.Select(attrs={'class': 'form-select'})
        }
    
    def clean(self):
        name = self.cleaned_data.get('name', '')
        price = self.cleaned_data.get('price', '')
        shelf_life = self.cleaned_data.get('shelf_life', '')

        if not self.instance.pk and Product.objects.get(name=name).exists():
            raise forms.ValidationError({'name': f'Product with name {name} exists.'})
        try:
            price = int(price)
        except ValueError:
            raise forms.ValidationError({'price': f'Invalid Price {price}'})

        try:
            shelf_life = int(shelf_life)
        except ValueError:
            raise forms.ValidationError({'price': f'Invalid Shelf Life {shelf_life}'})
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
        manufactured = self.cleaned_data.get("manufactured", "")
        if timezone.now().date() > manufactured.date():
            raise forms.ValidationError({"manufactured": "Manufactured date cannot be before today."})
        return self.cleaned_data