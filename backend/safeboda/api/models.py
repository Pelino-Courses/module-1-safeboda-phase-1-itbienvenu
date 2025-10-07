from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('rider', 'Rider'),
        ('driver', 'Driver'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.username} ({self.user_type})"



class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=50, unique=True)
    moto_registration = models.CharField(max_length=50, unique=True)
    is_verified = models.BooleanField(default=False)
    rating = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.moto_registration}"



class Rider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rider_profile')
    default_payment_method = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username



class Ride(models.Model):
    STATUS_CHOICES = (
        ('requested', 'Requested'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE, related_name='rides')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='rides')
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    fare = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.rider.user.username} -> {self.destination} ({self.status})"


class RideRating(models.Model):
    ride = models.OneToOneField(Ride, on_delete=models.CASCADE, related_name='rating')
    driver_rating = models.PositiveSmallIntegerField(default=0)  # 1-5 scale
    rider_rating = models.PositiveSmallIntegerField(default=0)   # 1-5 scale
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Rating for Ride {self.ride.id}"

class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=255, blank=True)


class Payment(models.Model):
    ride = models.OneToOneField(Ride, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='pending')

class DriverLocation(models.Model):
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    last_updated = models.DateTimeField(auto_now=True)
