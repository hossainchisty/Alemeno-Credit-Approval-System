from django.contrib import admin
from customer.models import Customer
from import_export.admin import ImportExportModelAdmin

@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    pass
