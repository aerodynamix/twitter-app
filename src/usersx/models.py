from django.db import models
from django.conf import settings
from datetime import datetime

get_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')

class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    city = models.CharField(max_length=30, null = True)
    modified_time = models.CharField(max_length=40, default=get_time)
    token = models.CharField(max_length=500, null=True)
    following = models.ManyToManyField(
        'self', related_name='followers', symmetrical=False, blank=True)
