from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
    return render(request, 'homepage/home.html')

def about_view(request):
    return render(request, 'homepage/about.html')