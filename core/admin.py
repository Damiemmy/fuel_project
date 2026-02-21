from django.contrib import admin
from .models import TruckStop,RackPrice

# Register your models here.

from django.contrib import admin
from .models import TruckStop, RackPrice

# Inline to show RackPrice under TruckStop
class RackPriceInline(admin.TabularInline):
    model = RackPrice
    extra = 0  # don’t show empty extra forms
    readonly_fields = ('created_at', 'updated_at')
    fields = ('rack_id', 'retail_price', 'created_at', 'updated_at')

class TruckStopAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'latitude', 'longitude')
    list_filter = ('state', 'city')
    search_fields = ('name', 'city', 'state', 'address')
    inlines = [RackPriceInline]  # <-- add the inline here
    
admin.site.register(TruckStop, TruckStopAdmin)
admin.site.register(RackPrice)  # optional if you want a separate RackPrice page