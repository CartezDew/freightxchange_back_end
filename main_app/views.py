# main_app/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to FreightXchange!")
