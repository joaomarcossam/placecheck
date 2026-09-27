from django.contrib import admin

from .models import Listing, ListingPriceHistory


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "source", "transaction_type", "price", "city", "is_active")
    list_filter = ("transaction_type", "is_active", "source", "state")
    search_fields = ("title", "external_id", "city", "neighborhood")
    autocomplete_fields = ("source", "property")


@admin.register(ListingPriceHistory)
class ListingPriceHistoryAdmin(admin.ModelAdmin):
    list_display = ("listing", "price", "captured_at")
    list_filter = ("captured_at",)
