from django.db import models

# Create your models here.
class Malaria(models.Model):
    WHO_region = models.CharField(max_length=200)
    Country = models.CharField(max_length=20)
    Year = models.IntegerField()
    Population_at_risk = models.IntegerField()
    Cases = models.IntegerField()
    Deaths = models.IntegerField()