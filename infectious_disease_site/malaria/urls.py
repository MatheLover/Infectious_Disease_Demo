from django.urls import path

from . import views
urlpatterns = [
    path('malaria_home.html/', views.malaria_home_view, name='malaria_home'),
    path('malaria_map.html/', views.malaria_map_view, name='malaria_map')
]