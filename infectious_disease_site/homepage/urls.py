from django.urls import path

from . import views

urlpatterns = [
    path('home.html/', views.home_view, name='home'),
    path('about.html/', views.about_view, name='about')
]