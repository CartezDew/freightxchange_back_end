from django.contrib.auth.models import User
from django.db import models
# from datetime import date


class Load(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loads')
    pickup_location = models.CharField(max_length=100)
    delivery_location = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    equipment_requirements = models.CharField(max_length=255)
    pickup_date = models.DateField()
    delivery_date = models.DateField()
    commodity = models.CharField(max_length=255)
    
def __str__(self):
        return f'Load for {self.user.username} - {self.pickup_location} → {self.delivery_location}'    