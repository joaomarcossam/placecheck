from django.db import models


class Source(models.Model):
    class ProviderType(models.TextChoices):
        API = "api", "API"
        XML = "xml", "XML"
        CRAWLER = "crawler", "Crawler"
        MANUAL = "manual", "Manual"

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    provider_type = models.CharField(max_length=20, choices=ProviderType.choices)
    base_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    can_store_images = models.BooleanField(default=False)
    can_store_description = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
