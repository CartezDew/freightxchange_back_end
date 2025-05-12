from rest_framework import generics, status, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import BrokerProfile, CarrierProfile, Offer, Load
from .serializers import UserSerializer, LoadSerializer, OfferSerializer, CarrierProfileSerializer, BrokerProfileSerializer


class IsCarrierOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return hasattr(request.user, 'carrier_profile') and obj.id == request.user.carrier_profile.id

class IsBrokerOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return hasattr(request.user, 'broker_profile') and obj.id == request.user.broker_profile.id


class Landing(APIView):
    def get(self, request):
        return Response({'message': 'Welcome to FreightXchange api home route!'})


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])

        role = request.data.get('role')
        if role == 'carrier':
            CarrierProfile.objects.create(user=user)
        elif role == 'broker':
            BrokerProfile.objects.create(user=user)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': response.data
        })


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            if hasattr(user, 'broker_profile'):
                role = 'broker'
                profile_id = user.broker_profile.id
            elif hasattr(user, 'carrier_profile'):
                role = 'carrier'
                profile_id = user.carrier_profile.id
            else:
                role = None
                profile_id = None

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
                'role': role,
                'profile_id': profile_id
            })

        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CarrierProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = CarrierProfile.objects.all()
    serializer_class = CarrierProfileSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated, IsCarrierOwner]

class BrokerProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = BrokerProfile.objects.all()
    serializer_class = BrokerProfileSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated, IsBrokerOwner]


class LoadListCreateView(generics.ListCreateAPIView):
    queryset = Load.objects.all()
    serializer_class = LoadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            broker_profile = self.request.user.broker_profile
        except BrokerProfile.DoesNotExist:
            raise serializers.ValidationError("No broker profile found for this user.")
        serializer.save(broker=broker_profile)

class LoadDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Load.objects.all()
    serializer_class = LoadSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]


class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            carrier_profile = self.request.user.carrier_profile
        except CarrierProfile.DoesNotExist:
            raise serializers.ValidationError("No carrier profile found for this user.")
        serializer.save(carrier=carrier_profile)

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]
