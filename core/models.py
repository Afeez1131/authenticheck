from django.db import models
import uuid
from datetime import timedelta, datetime
from django.utils import timezone
from django.contrib.auth.models import User
from .enums import CategoryChoices


class Business(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=155)
    description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=50)
    website = models.URLField(max_length=155)
    email = models.EmailField(max_length=155)
    secret = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.email}"


class Product(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=155)
    short_name = models.CharField(max_length=50, unique=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False)
    shelf_life = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=50, choices=CategoryChoices.choices)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name} - ({self.short_name})"

    def save(self, *args, **kwargs):
        if not self.short_name:
            self.short_name = self.generate_short_name()
        return super().save(*args, **kwargs)

    def generate_short_name(self):
        counter = 3
        name_parts = self.name.split(" ")
        short_name = "-".join([part[:counter] for part in name_parts])
        while Product.objects.filter(short_name=short_name).exists():
            counter += 1
            short_name = "-".join([part[:counter] for part in name_parts])
        return short_name

    class Meta:
        ordering = ("-id",)


class ProductInstance(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    manufactured = models.DateTimeField()
    expiry_date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - ({self.manufactured.date()} - {self.expiry_date.date()})"

    def save(self, *args, **kwargs):
        self.expiry_date = self.manufactured + timedelta(days=self.product.shelf_life)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("-id", )