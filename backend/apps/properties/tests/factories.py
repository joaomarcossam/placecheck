from apps.properties.models import Property


class PropertyFactory:
    @staticmethod
    def create(**kwargs):
        values = {
            "property_type": Property.PropertyType.APARTMENT,
            "city": "São Paulo",
            "state": "SP",
            "neighborhood": "Pinheiros",
            "area": "80.00",
            "bedrooms": 2,
        }
        values.update(kwargs)
        return Property.objects.create(**values)
