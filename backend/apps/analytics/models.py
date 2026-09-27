from django.db import models

from apps.listings.models import Listing
from apps.properties.models import Property


class RedirectEvent(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="redirect_events")
    property = models.ForeignKey(
        Property,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="redirect_events",
    )
    session_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    referer = models.URLField(blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"Redirect para {self.listing} em {self.created_at:%Y-%m-%d %H:%M}"
