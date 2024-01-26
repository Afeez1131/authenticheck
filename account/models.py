from django.db import models
from django.contrib.auth.models import User
import uuid

# class SetupProgress()


class OneTimeLogin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.TextField()
    attempt = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}: {self.token}"
    