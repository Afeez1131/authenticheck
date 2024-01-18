from .models import Product
import uuid


def create_short_name(product_name):
    counter = 3
    name_parts = product_name.split(" ")
    short_name = "-".join([part[:counter] for part in name_parts])
    while Product.objects.filter(short_name=short_name).exists():
        counter += 1
        short_name = "-".join([part[:counter] for part in name_parts])
    return short_name