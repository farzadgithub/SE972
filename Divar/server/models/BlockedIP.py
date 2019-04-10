from django.db import models


class BlockedIP(models.Model):
    ip = models.CharField(max_length=100)
