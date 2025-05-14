from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CarrierProfile, BrokerProfile, Load, Offer

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # You could auto-create one or both profile types here (optional)
        # CarrierProfile.objects.create(user=user) or BrokerProfile.objects.create(user=user)
        return user

class CarrierProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarrierProfile
        fields = '__all__'

class BrokerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrokerProfile
        fields = '__all__'

class LoadSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='broker.company_name', read_only=True)
    pickupCity = serializers.CharField(source='pickup_city')
    pickupState = serializers.CharField(source='pickup_state')
    deliveryCity = serializers.CharField(source='delivery_city')
    deliveryState = serializers.CharField(source='delivery_state')
    equipmentRequirements = serializers.CharField(source='equipment_requirements')
    pickupDate = serializers.DateField(source='pickup_date')
    deliveryDate = serializers.DateField(source='delivery_date')

    class Meta:
        model = Load
        fields = [
            'id',
            'company_name',
            'pickupCity',
            'pickupState',
            'deliveryCity',
            'deliveryState',
            'rate',
            'equipmentRequirements',
            'pickupDate',
            'deliveryDate',
            'commodity',
            'broker',  
        ]
        read_only_fields = ['broker']


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ['carrier']