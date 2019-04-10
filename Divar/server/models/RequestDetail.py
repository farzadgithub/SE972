from django.db import models


class RequestDetail(models.Model):
    ip = models.CharField(max_length=15)
    time = models.DateTimeField(auto_now_add=True)
    browser = models.CharField(max_length=100)
    is_authenticated = models.BooleanField(default=False)
    username = models.CharField(max_length=100, default='')
