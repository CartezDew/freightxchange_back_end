from django.urls import path
from .views import Landing, CreateUserView, LoginView, LogoutView, ProfileView, LoadList, OfferView, CreateLoad, LoadDetail, EditLoad, DeleteLoad

urlpatterns = [
    path ('', Landing.as_view(), name='landing'),
    path ('/register', CreateUserView.as_view(), name='register'),
    path ('/login', LoginView.as_view(), name='login'),
    path ('/logout', LogoutView.as_view(), name='logout'),
    path ('/profile/:Id', ProfileView.as_view(), name='profile'),
    path ('/loads', LoadList.as_view(), name='loads'),
    path ('/offer/:offerId', OfferView.as_view(), name='offers'),
    path ('/loads/new', CreateLoad.as_view(), name='create-load'),
    path ('/loads/:loadID/', LoadDetail.as_view(), name='load-detail'),
    path ('/loads/:loadID/edit', EditLoad.as_view(), name='edit-load'),
    path ('/loads/:loadID/delete', DeleteLoad.as_view(), name='delete-load'),
]
