from django.contrib.auth.models import User
from django.db import models
# from datetime import date
      
class CarrierProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carrier_profile')
    company_name = models.CharField(max_length=100)
    license_id = models.CharField(max_length=50)
    authority_id = models.CharField(max_length=50)
    equipment_type = models.CharField(max_length=255)
    
    def __str__ (self):
        return f"Carrier profile: {self.user.username}"
      
class BrokerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='broker_profile')
    company_name = models.CharField(max_length=100)
    policy_id = models.CharField(max_length=50)
    authority_id = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Broker profile: {self.user.username}"


class Load(models.Model):
    broker = models.ForeignKey(BrokerProfile, on_delete=models.CASCADE, related_name='loads')
    # title = models.CharField(max_length=200)
    pickup_city = models.CharField(max_length=200)
    pickup_state = models.CharField(max_length=200)
    delivery_city = models.CharField(max_length=200)
    delivery_state= models.CharField(max_length=200)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    equipment_requirements = models.CharField(max_length=255)
    pickup_date = models.DateField()
    delivery_date = models.DateField()
    commodity = models.CharField(max_length=255)
    
def __str__(self):
        return f'Load for {self.user.username} - {self.pickup_city} → {self.delivery_city}'
    
class Offer(models.Model):
    carrier = models.ForeignKey(CarrierProfile, on_delete=models.CASCADE, related_name='offers')
    load = models.ForeignKey(Load, on_delete=models.CASCADE, related_name='offers')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    submitted_at = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Offer {self.id} for load {self.load.id}'

