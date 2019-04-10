from django.db import models


class Captcha(models.Model):
    captcha_ip = models.CharField(max_length=15)
    captcha_text = models.CharField(max_length=100)


class LoginAttempts(models.Model):
    ip = models.CharField(max_length=15)
    user = models.CharField(max_length=100)
    failed_attempts = models.IntegerField()
