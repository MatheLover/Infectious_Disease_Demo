from import_export import resources
from .models import Malaria

class MalariaResource(resources.ModelResource):
    class Meta:
        model = Malaria