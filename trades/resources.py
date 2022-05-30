from import_export import resources
from .models import Center, Enterprise, Models, Staff

class CenterResource(resources.ModelResource):

    class Meta:
        model = Center
        import_id_fields = ['name']

class EnterpriseResource(resources.ModelResource):

    class Meta:
        model = Enterprise
        import_id_fields = ['name','country','city','supply_center','industry']

class ModelsResource(resources.ModelResource):

    class Meta:
        model = Models
        import_id_fields = ['number', 'model', 'name', 'unit_price']

class StaffResource(resources.ModelResource):

    class Meta:
        model = Staff
        import_id_fields = ['name', 'age', 'gender', 'number','supply_center','mobile_number','type']