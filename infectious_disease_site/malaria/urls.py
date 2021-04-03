from django.urls import path

from . import views

urlpatterns = [
    path('malaria_home.html/', views.malaria_home_view, name='malaria_home'),
    path('malaria_map.html/', views.malaria_map_view, name='malaria_map'),
    path('malaria_annual_stat.html/', views.malaria_annual_stat_view, name='malaria_annual_stat'),
    path('malaria_annual_stat_map.html', views.malaria_annual_stat_map_view, name='malaria_annual_stat_map'),
    path('malaria_cumulative_stat.html', views.malaria_cumulative_stat_view, name='malaria_cumulative_stat'),
    path('malaria_cumulative_stat_map.html', views.malaria_cumulative_stat_map_view,
         name='malaria_cumulative_stat_map'),
    path('malaria_environmental_factor.html', views.malaria_environmental_factor_view,
         name='malaria_environmental_factor'),
    path('malaria_rainfall.html', views.malaria_rainfall_view,
         name='malaria_rainfall_map'),
    path('malaria_rainfall_scatterplot.html', views.malaria_rainfall_scatterplot_view,
         name='malaria_rainfall_scatterplot'),
    path('malaria_rainfall_map.html', views.malaria_rainfall_map_view,
         name='malaria_rainfall_map'),

    path('malaria_socioeconomic_factor.html', views.malaria_socioeconomic_factor_view,
         name='malaria_socioeconomic_factor'),

    path('malaria_gdp_per_capita.html', views.malaria_gdp_per_capita_view, name='malaria_gdp_per_capita'),
    path('malaria_pct_agri_pop.html', views.malaria_pct_agri_pop_view, name='malaria_pct_agri_pop'),
    path('malaria_about.html', views.malaria_about_view, name='malaria_about')

]
