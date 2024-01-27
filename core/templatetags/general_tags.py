from django import template
from django.contrib import messages as django_messages
import json

register = template.Library()


@register.simple_tag(takes_context=True)
def custom_messages(context):
    request = context.get('request')
    data = []
    for message in django_messages.get_messages(request):
        data.append({
            'tags': message.tags,
            'message': message.message
        })
    print(json.dumps(data), type(json.dumps(data)))
    return json.dumps(data)