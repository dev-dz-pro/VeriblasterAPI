from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
    def __str__(self):
        return self.email


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    machine_uid = models.UUIDField(unique=True)
    expire = models.DateTimeField(default=timezone.now, blank=True)
    leads_orderd_date = models.DateTimeField(default=None, null=True, blank=True)
    def __str__(self):
        return str(self.machine_uid) + ' | ' + self.user.email


class Leads(models.Model):
    phone = models.CharField(max_length=17)
    def __str__(self):
        return self.phone
    


