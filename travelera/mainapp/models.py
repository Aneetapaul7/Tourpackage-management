
from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']


class Destination(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    image = models.ImageField(upload_to='destinations/')
    duration_days = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.country}"

    @property
    def display_name(self):
        return f"{self.name}, {self.country}"

    @property
    def duration_text(self):
        return f"{self.duration_days} days"