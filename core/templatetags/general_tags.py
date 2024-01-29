from django import template
from datetime import datetime, timedelta

from django.urls import reverse
from core.models import Product, ProductInstance
from django.template.defaultfilters import timesince
from core.utils import to_percent

register = template.Library()


@register.simple_tag
def percentage_increase_or_decrease():
    today_instances = ProductInstance.objects.filter(created__date=datetime.now().date()).count() or 0
    yesterday = datetime.now().date() - timedelta(days=1)
    yesterday_instances = ProductInstance.objects.filter(created__date=yesterday).count() or 0
    today_percent = to_percent(today_instances)
    yesterday_percent = to_percent(yesterday_instances)
    print('here: ', today_percent, yesterday_percent)
    diff = today_percent - yesterday_percent
    return '{:.2f}'.format(diff)
    
    
@register.filter
def is_positive(number):
    return number >= 0

    
@register.filter
def abbr_timesince(value):
    time_difference = timesince(value)
    time_difference = time_difference.replace("hour", "Hr").replace("minute", "Min")
    return time_difference


@register.simple_tag
def is_active(request, view_name):
    url = reverse(view_name)
    if request.path == url:
        return 'active'
    return ''