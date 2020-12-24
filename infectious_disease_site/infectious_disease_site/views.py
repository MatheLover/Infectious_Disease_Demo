from django.http import HttpResponse

from django.shortcuts import render


def home(request):
    return HttpResponse("<h1>Infectious Disease Visualization System</h1>")