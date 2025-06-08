from django.db import models
from django.contrib.auth import get_user_model
from packages.models import Package
from django.utils import timezone

User = get_user_model()


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

    class Meta:
        ordering = ['-booking_date']