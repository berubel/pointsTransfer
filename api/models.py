from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password

# Create your models here.

class User(AbstractUser, AbstractBaseUser):

    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    REQUIRED_FIELDS = []

    enrollment = models.CharField(max_length=7, blank=False, null=False)
    name = models.CharField(max_length=256, blank=False, null=False)
    course = models.CharField(max_length=256, blank=False, null=False)
    image = models.URLField(max_length=256, blank=True, null=True)
    balance = models.IntegerField(default=0, editable=True)

class Receipt(models.Model):
    transfer_value = models.IntegerField(blank=False, null=False)
    user = models.CharField(max_length=7, blank=False, null=False)
    name = models.CharField(max_length=256, blank=False, null=False)
    course = models.CharField(max_length=256, blank=False, null=False)
    transfer_user = models.CharField(max_length=7, blank=False, null=False)
    transfer_name = models.CharField(max_length=256, blank=False, null=False)
    transfer_course = models.CharField(max_length=256, blank=False, null=False)
    date = models.DateTimeField(auto_now=True)

