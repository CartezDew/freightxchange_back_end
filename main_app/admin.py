from django.contrib import admin
# import your models here
from .models import Load, BrokerProfile, CarrierProfile, Offer

# Register your models here
admin.site.register(Load)
admin.site.register(BrokerProfile)
admin.site.register(CarrierProfile)
admin.site.register(Offer)
