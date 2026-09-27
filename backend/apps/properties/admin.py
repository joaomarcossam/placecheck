from django.contrib import admin

from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("property_type", "city", "state", "neighborhood", "area")
    list_filter = ("property_type", "state", "city")
    search_fields = ("city", "neighborhood")
