from .models import Business, Product, ProductInstance
from django.http import JsonResponse
from django.contrib.auth.decorator import login_required


@login_required
def product_instances_chart_data(request):
    """
    {'products': ['Prod-0dc5ee', 'Prod-d0865a', 'Prod-fdb96f', 'Prod-f9736f', 'Prod-317588', 'Prod-a76187', 'Prod-89e03d', 'Prod-55cf12', 'Prod-b700e0', 'Prod-95c529'], 'instances': [5, 3, 5, 2, 5, 60, 4, 4, 8, 4]}
    """
    business = Business.objects.get(user=request.user)
    products = business.product_set.all()
    chart_data = {"products": [], "instances": []}
    for product in products:
        instances_count = product.productinstance_set.count()
        chart_data["products"].append(product.name)
        chart_data["instances"].append(instances_count)
    print(chart_data)
    return JsonResponse(chart_data)