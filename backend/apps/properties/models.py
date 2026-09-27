from django.db import models


class Property(models.Model):
    class PropertyType(models.TextChoices):
        APARTMENT = "apartment", "Apartamento"
        HOUSE = "house", "Casa"
        LAND = "land", "Terreno"
        COMMERCIAL = "commercial", "Comercial"
        OTHER = "other", "Outro"

    property_type = models.CharField(max_length=30, choices=PropertyType.choices)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=2)
    neighborhood = models.CharField(max_length=120, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    area = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    bedrooms = models.PositiveSmallIntegerField(null=True, blank=True)
    bathrooms = models.PositiveSmallIntegerField(null=True, blank=True)
    suites = models.PositiveSmallIntegerField(null=True, blank=True)
    parking_spaces = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["city", "neighborhood", "id"]

    def __str__(self):
        location = ", ".join(part for part in [self.neighborhood, self.city] if part)
        return f"{self.get_property_type_display()} em {location}"
