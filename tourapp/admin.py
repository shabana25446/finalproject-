from django.contrib import admin
from .models import *

class TourPackageAdmin(admin.ModelAdmin):
    list_display=('title','vendor','status','available_from','available_to')
    list_filter=('status','vendor')
    search_fields=('title','description')
    list_editable=('status',)
    
# Register your models here.
admin.site.register(Vendor)
admin.site.register(TourStatus)
admin.site.register(TourPackages)