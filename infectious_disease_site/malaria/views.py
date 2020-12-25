from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def malaria_home_view(request):
    return render(request, 'malaria/malaria_home.html')