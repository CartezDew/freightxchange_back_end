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

class OfferSerializer(serializers.ModelSerializer):
    carrier_name = serializers.CharField(source='carrier.company_name', read_only=True)
    broker_company = serializers.SerializerMethodField()
<<<<<<< Updated upstream
    rate = serializers.DecimalField(source='load.rate', max_digits=10, decimal_places=2, read_only=True)
=======
>>>>>>> Stashed changes

    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ['carrier', 'submitted_at', 'carrier_name', 'broker_company', 'rate']

    def get_broker_company(self, obj):
        return obj.load.broker.company_name if obj.load and obj.load.broker else None

    def validate(self, data):
        # Ensure a declined offer must have a reason
        if data.get('status') == 'declined' and not data.get('declined_reason'):
            raise serializers.ValidationError({
                'declined_reason': 'A declined reason must be provided when status is declined.'
            })
        return data

    def get_broker_company(self, obj):
        # Traverse: Offer -> Load -> Broker -> company_name
        return obj.load.broker.company_name if obj.load and obj.load.broker else None

class LoadSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='broker.company_name', read_only=True)
    offers = OfferSerializer(many=True, read_only=True)

    class Meta:
        model = Load
        fields = '__all__'
        read_only_fields = ['broker']

