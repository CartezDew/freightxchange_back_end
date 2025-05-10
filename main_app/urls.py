from django.urls import path
from .views import Landing, CreateUserView, LoginView, CarrierProfileDetailView, BrokerProfileDetailView, LoadListCreateView, LoadDetailView, OfferListCreateView, OfferDetailView

urlpatterns = [
    path ('', Landing.as_view(), name='landing'),
    path ('register/', CreateUserView.as_view(), name='register'),
    path ('login/', LoginView.as_view(), name='login'),
   
    #Profiles 
    path ('carrier-profiles/<int:id>/', CarrierProfileDetailView.as_view(), name='carrier-profile-detail'),
    path ('broker-profiles/<int:id>/', BrokerProfileDetailView.as_view(), name='broker-profile-detail'),
    
    #Loads
    path ('loads/', LoadListCreateView.as_view(), name='loads'),
    path ('loads/<int:id>/', LoadDetailView.as_view(), name='load-detail'),
    
    #Offers
    path ('offers/', OfferListCreateView.as_view(), name='offers-list-create'),
    path ('offers/<int:id>/', OfferDetailView.as_view(), name='offer-detail'),
]
