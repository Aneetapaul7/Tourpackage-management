from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.conf import settings

User = get_user_model()

class PackageImage(models.Model):
    package = models.ForeignKey('Package', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='package_images/')
    caption = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.package.title}"

class Package(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    EXPIRED = 'expired'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (EXPIRED, 'Expired'),
    ]

    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='packages')
    title = models.CharField(max_length=200)
    description = models.TextField()
    destination = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration_days = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='package_images/', null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.expiry_date and timezone.now() > self.expiry_date:
            self.status = self.EXPIRED
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        return self.status == self.APPROVED and (not self.expiry_date or timezone.now() <= self.expiry_date)

    def get_images(self):
        return self.images.all()

class Booking(models.Model):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
        (COMPLETED, 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    travel_date = models.DateField()
    number_of_people = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    special_requests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.package.title}"

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.package.price * self.number_of_people
        super().save(*args, **kwargs)