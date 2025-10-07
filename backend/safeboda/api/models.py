from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('rider', 'Rider'),
        ('driver', 'Driver'),
        ('admin', 'Admin'),
    ]
    
    username = None
    names = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='rider')
    status = models.CharField(max_length=20, default='active')
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['names', 'phone']

    def __str__(self):
        return f"{self.names} ({self.role})"



class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Driver: {self.user.names}"



class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.origin} → {self.destination}"



class Ride(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='rides')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='rides')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ride {self.id} by {self.driver.user.names}"



class DriverRoute(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='routes')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='drivers')

    class Meta:
        unique_together = ('driver', 'route')

    def __str__(self):
        return f"{self.driver.user.names} - {self.route.origin} → {self.route.destination}"
