from django.shortcuts import HttpResponseRedirect
from core.models import Business
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

class UserHasBusinessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        if request.user.is_authenticated:
            has_business = Business.objects.filter(user=request.user).exists()
            logger.info(f"{request.path}, {reverse('core:create_profile')}")
            if not has_business and request.path != reverse('account:logout') and request.path != reverse('core:create_profile'):
                return HttpResponseRedirect(reverse('core:create_profile'))
    
        response = self.get_response(request)
        return response