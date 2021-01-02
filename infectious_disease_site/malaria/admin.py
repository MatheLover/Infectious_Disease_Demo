from django.contrib import admin
from .models import Malaria
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Malaria)
class MalariaAdmin(ImportExportModelAdmin):
    list_display = ('WHO_region', 'Country', 'Year', 'Population_at_risk', 'Cases', 'Deaths')