from .models import Product, ProductInstance
from django.db.models import Count
from django.contrib.auth.models import User
import cairosvg
import uuid


def create_short_name(product_name):
    counter = 3
    name_parts = product_name.split(" ")
    short_name = "-".join([part[:counter] for part in name_parts])
    while Product.objects.filter(short_name=short_name).exists():
        counter += 1
        short_name = "-".join([part[:counter] for part in name_parts])
    return short_name



def to_percent(amount):
    return amount / 100


def top_nine_product(uid):
    user = User.objects.get(id=uid)
    top_ten = ProductInstance.objects.filter(product__business__user=user).values('product').annotate(total_count=Count('product')).order_by('-total_count')[:9]
    product_ids = [item['product'] for item in top_ten]
    products_mapping = {pk: Product.objects.get(pk=pk) for pk in product_ids}
    for item in top_ten:
        item['product'] = products_mapping.get(item['product'])
    return top_ten
    
    
def redirect_to_referrer(request, redirect_to):
    referer = request.META.get('HTTP_REFERER', '')
    if referer and referer != request.build_absolute_uri():
        print('referer: ', referer, request.build_absolute_uri())
        return referer
    return redirect_to


def svg_to_png(svg):
    """
    convert an svg file to png

    Args:
        svg (svg): An svg file to be converted to png

    Returns:
        _type_: png object
    """
    with svg.open() as file:
        svg_content = file.read()
    png_content = cairosvg.svg2png(bytestring=svg_content)
    return png_content