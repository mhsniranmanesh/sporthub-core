from django.db import models
from profiles.models import User
from django.utils import timezone


class PasswordReset(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    token = models.CharField(max_length=50, blank=False)
    is_used = models.BooleanField(default=False)