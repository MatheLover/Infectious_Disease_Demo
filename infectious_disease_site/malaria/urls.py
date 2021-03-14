from django.urls import path

from . import views

urlpatterns = [
    path('malaria_home.html/', views.malaria_home_view, name='malaria_home'),
    path('malaria_map.html/', views.malaria_map_view, name='malaria_map'),
    path('malaria_annual_stat.html/', views.malaria_annual_stat_view, name='malaria_annual_stat'),
    path('malaria_annual_stat_map.html', views.malaria_annual_stat_map_view, name='malaria_annual_stat_map'),
    path('malaria_cumulative_stat.html', views.malaria_cumulative_stat_view, name='malaria_cumulative_stat'),
    path('malaria_cumulative_stat_map.html', views.malaria_cumulative_stat_map_view, name='malaria_cumulative_stat_map')
]
