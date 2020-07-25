from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)
    logo_thumb = models.ImageField()
    address = models.CharField(max_length=255)
    email = models.EmailField(verbose_name="email", max_length=255)
    phone = models.CharField(max_length=225)
    competetionList = models.TextField()
