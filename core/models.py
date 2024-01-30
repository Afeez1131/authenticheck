from django.db import models
import uuid
from datetime import timedelta, datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from core.qrcode_manager import QrCodeGenerator, generate_secret_key
from .enums import CategoryChoices


class Business(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=155)
    description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=50)
    website = models.URLField(max_length=155)
    email = models.EmailField(max_length=155)
    secret = models.BinaryField(null=True, blank=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.email}"
    
    def save(self, *args, **kwargs):
        if not self.secret:
            self.secret = generate_secret_key()
        return super().save(*args, **kwargs)


def product_upload_path(instance, filename):
    name = f"{instance.name}_qr{filename[-4:]}"
    slg_name = slugify(instance.name)
    return f"products/{slg_name}/qrcode/{name}"

class Product(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=155)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False)
    shelf_life = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=50, choices=CategoryChoices.choices)
    secret = models.BinaryField(null=True, blank=True, unique=True)
    qr = models.FileField(upload_to=product_upload_path, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name} - ({self.price})"

    def save(self, *args, **kwargs):
        if not self.secret:
            self.secret = generate_secret_key()
        if not self.qr:
            manager = QrCodeGenerator(self.secret)
            ec = manager.encode_content(self.unique_code)
            qr = manager.generate_qr(ec)
            self.qr = qr
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("-id",)

#f"products/{slg_name}/qrcodes/{name}"
def product_instance_upload_path(instance, filename):
    product_name = slugify(instance.product.name)
    count = instance.product.productinstance_set.count() + 1
    unique_filename = f"{product_name}_instance_{count}{filename[-4:]}"
    return f"products/{product_name}/instances/{unique_filename}"


class ProductInstance(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    manufactured = models.DateTimeField()
    expiry_date = models.DateTimeField()
    secret = models.BinaryField(null=True, blank=True, unique=True)
    qr = models.FileField(upload_to=product_instance_upload_path, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - ({self.manufactured.date()} - {self.expiry_date.date()})"

    def save(self, *args, **kwargs):
        if not self.secret:
            self.secret = generate_secret_key()
        if not self.qr:
            manager = QrCodeGenerator(self.secret)
            data = f"{self.id}::{self.product.unique_code}"
            encoded_data = manager.encode_content(data)
            qr = manager.generate_qr(encoded_data)
            self.qr = qr
            
        self.expiry_date = self.manufactured + timedelta(days=self.product.shelf_life)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created", )