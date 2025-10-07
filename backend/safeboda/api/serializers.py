from rest_framework import serializers
from .models import User, DriverRequest, Driver, Ride, Route, DriverRoute

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'role', 'status', 'is_active']

class DriverRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverRequest
        fields = ['id', 'user', 'status', 'created_at']

class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Driver
        fields = ['id', 'user', 'license', 'created_at']

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'driver', 'price', 'created_at']

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'origin', 'destination']

class DriverRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverRoute
        fields = ['id', 'driver', 'route']
