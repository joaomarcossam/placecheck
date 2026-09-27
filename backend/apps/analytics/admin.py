from django.contrib import admin

from .models import RedirectEvent


@admin.register(RedirectEvent)
class RedirectEventAdmin(admin.ModelAdmin):
    list_display = ("listing", "property", "session_id", "created_at")
    list_filter = ("created_at",)
    search_fields = ("listing__title", "session_id")
    readonly_fields = ("created_at",)
