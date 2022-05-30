from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
import trades.models as models
import trades.resources as resources

# Register your models here.
class CenterAdmin(ImportExportModelAdmin):
    resource_class = resources.CenterResource

class EnterpriseAdmin(ImportExportModelAdmin):
    resource_class = resources.EnterpriseResource

class ModelsAdmin(ImportExportModelAdmin):
    resource_class = resources.ModelsResource

class StaffAdmin(ImportExportModelAdmin):
    resource_class = resources.StaffResource

admin.site.register(models.Center,CenterAdmin)
admin.site.register(models.Enterprise,EnterpriseAdmin)
admin.site.register(models.Models,ModelsAdmin)
admin.site.register(models.Staff,StaffAdmin)
admin.site.register(models.Model_center)
admin.site.register(models.Contract)
admin.site.register(models.Order)