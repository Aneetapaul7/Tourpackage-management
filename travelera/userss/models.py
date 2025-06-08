from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('vendor', 'Vendor'),
        ('customer', 'Customer'),
    )

    # Common fields for all users
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.user_type == 'vendor':
            self.is_vendor = True
            self.is_customer = False
        elif self.user_type == 'customer':
            self.is_customer = True
            self.is_vendor = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_full_name()} ({self.phone_number})" if self.get_full_name() else self.username


class Vendor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Additional customer-specific fields can be added here if needed

    def __str__(self):
        return self.user.get_full_name()