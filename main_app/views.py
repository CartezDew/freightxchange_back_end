from rest_framework import generics, status, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import BrokerProfile, CarrierProfile, Offer, Load
from .serializers import UserSerializer, LoadSerializer, OfferSerializer, CarrierProfileSerializer, BrokerProfileSerializer

class Landing(APIView):
    def get(self, request):
        content = {'message': 'Welcome to FreightXchange api home route!'}
        return Response(content)
    
#User Registration 
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])

        # Automatically create profile (customize based on role input)
        role = request.data.get('role')  # 'carrier' or 'broker'
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
        
        
# User Login
class LoginView(APIView): 
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user: 
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# class VerifyUserView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get(self, request):
#         user = User.objects.get(username=request.user)
#         refresh = RefreshToken.for_user(request.user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'user': UserSerializer(user).data
#         })

class CarrierProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = CarrierProfile.objects.all()
    serializer_class = CarrierProfileSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

class BrokerProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = BrokerProfile.objects.all()
    serializer_class = BrokerProfileSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]
        
class LoadListCreateView(generics.ListCreateAPIView):
    queryset = Load.objects.all()
    serializer_class = LoadSerializer
    permissions_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        try:
            broker_profile = self.request.user.broker_profile
        except BrokerProfile.DoesNotExist:
            raise serializers.ValidationError("No broker profile found for this user.")
        serializer.save(broker=broker_profile)
    
    # def perform_create(self, serializer):
    #   serializer.save(user=self.request.user)
 
class LoadDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Load.objects.all()
    serializer_class = LoadSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]
    

          
# class LoadDetailView(generics.RetrieveUpddateDestroyAPIView):
#     serializer_class = LoadSerializer 
#     lookup_field = 'id'
    
#     def get_queryset(self):
#         user = self.request.user
#         return Load.objects.filter(user=user)
    
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
        
#      # bid or broker or carrier, one for each?  bid_not_associated = Bid.objects.exclude(id_in=intance.bids.all())
#      # bid_serializer = BidSerializer(bids_not_associated, many=True)
     
#      return Response({
#          'load': serializer.data,
#          'bids_not_associated': bids_serializer.data
#      })
        
#     def perform_update(self, serializer):
#         load = self.get_object()
#         if load.user != self.request.user: 
#             raise PermissionDenied({"message": "You do not have permission to edit this Load."})
#         serializer.save()
        
#     def perform_destory(self, instance):
#         if instance.user != self.request.user: 
#             raise PermissionDenied({"message": "You do not have permission to delete this Load."})
#         instance.delete()
        
class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        try:
            carrier_profile = self.request.user.carrier_profile
        except CarrierProfile.DoesNotExist:
            raise serializers.ValidationError("No carrier profile found for this user.")
        serializer.save(carrier=carrier_profile)
