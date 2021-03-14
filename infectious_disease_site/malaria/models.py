from django.db import models

# Create your models here.
class Malaria(models.Model):
    WHO_region = models.CharField(max_length=200)
    Country = models.CharField(max_length=20)
    Latitude = models.DecimalField(max_digits=13, decimal_places=10, default=0.0)
    Longitude = models.DecimalField(max_digits=13, decimal_places=10, default=0.0)
    Year = models.IntegerField()
    Population_at_risk = models.IntegerField()
    Cases = models.IntegerField()
    Deaths = models.IntegerField()
    Rural_pop_pct = models.IntegerField(default=0)
    GDP_per_capita = models.IntegerField(default=0)
    Rainfall_gauge = models.IntegerField(default=0)