from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Stock)
admin.site.register(Provider)
admin.site.register(Import)
admin.site.register(Export)
admin.site.register(ImportDetail)
admin.site.register(ExportDetail)