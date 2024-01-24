from django.contrib.auth.models import User
from account.models import OneTimeLogin
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)


def create_one_time_login(uid, token):
    try:
        user = User.objects.get(id=uid)
        otl = OneTimeLogin.objects.get(user=user)
    except OneTimeLogin.DoesNotExist:
        otl = OneTimeLogin.objects.create(user=user)
    otl.token = token
    otl.save()
    return


def send_html_mail(subject, from_email, to_email, html_message, plain_message):
    if not isinstance(to_email, (list, tuple)):
        to_email = [to_email]
    email = EmailMultiAlternatives(subject, plain_message, from_email, to_email)
    email.attach_alternative(html_message, 'text/html')
    try:
        email.send()
    except Exception as e:
        logger.info(f"Error: {str(e)}")
    return