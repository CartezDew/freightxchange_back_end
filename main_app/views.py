from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer

class Landing(APIView):
    def get(self, request):
        content = {'message': 'Welcome to FreightXchange api home route!'}
        return Response(content)
    
#User Registration 

        
        
#User Login
# class LoginView(APIView): 
#     permission_classes = [permissions.AllowAny]
    
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#         if user: 
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'user': UserSerializer(user).data
#             })
#         return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

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
        
# class LoadList(generics.ListCreateAPIView):
#     serializer_class = LoadSerializer
#     permissions_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         user = self.request.user
#         return Load.objects.filter(user=user)
    
# class LoadDetail(generics.RetrieveUpddateDestroyAPIView):
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
        
# class 
    