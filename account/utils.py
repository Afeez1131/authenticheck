from django.contrib.auth.models import User
from account.models import OneTimeLogin
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)


def generate_token(uid):
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return ""
    return default_token_generator.make_token(user)

def create_one_time_login(uid, token):
    """
    would create/update one time login token for the user

    Args:
        uid (int): User ID
        token (token): generated token for the User
    """
    try:
        user = User.objects.get(id=uid)
        otl = OneTimeLogin.objects.get(user=user)
    except OneTimeLogin.DoesNotExist:
        otl = OneTimeLogin.objects.create(user=user)
    otl.token = token
    otl.save()
    return


def increment_login_attempt(token):
    """
    would increment the attempt on the OneTimeLogin with the token passed.
    once it reaches 3 trials, revoke the token

    Args:
        token (token): Token associated with the OneTimeLogin.
    """
    try:
        otl = OneTimeLogin.objects.get(token=token)
    except OneTimeLogin.DoesNotExist:
        logger.info(f"invalid token")
        return None
    if otl.attempt < 3:
        otl.attempt += 1
    else:
        logger.info(f"Attempt is =3, revoke token.")
        token = generate_token(otl.user.id)
        otl.token = token
        otl.attempt = 0
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