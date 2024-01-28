from django.core.management import BaseCommand, CommandError
from core.models import Product, Business, ProductInstance
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from core.enums import CategoryChoices
import random

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--id", type=int)
        parser.add_argument("--product", type=int)
        parser.add_argument("--instance", type=int)

    def handle(self, *args, **options):
        product_count = options.get("product", "")
        instance_count = options.get("instance", "")
        pk = options.get("id", "")
        if not product_count or not instance_count or not pk:
            raise CommandError("You need specify the number of records to create '--count 20'")
        user = User.objects.get(pk=pk)
        try:
            business = user.business
        except Business.DoesNotExist:
            business,_ = Business.objects.get_or_create(user=user, name="Ganaf PLC.", description="Description",
            address="Address", phone="08105506043", website="dangote.ng", email="dangote@ng.com")
        for c in range(product_count):
            name = f'Prod-{uuid.uuid4().hex[:6]}'
            price = random.randint(1000, 10000)
            sl = random.randint(365, 1000)
            choice = random.choice(CategoryChoices.choices)[0]
            product = Product.objects.create(business=business, name=name,
            description='Product description', price=price, shelf_life=sl,
            category=choice)
        products = Product.objects.all()
        for count in range(instance_count):
            product = random.choice(products)
            ProductInstance.objects.create(product=product, manufactured=timezone.now())
            print(f"Product : {product} created")
        print("=========done===========")
