from apps.sources.models import Source


class SourceFactory:
    @staticmethod
    def create(**kwargs):
        values = {
            "name": "Fonte manual",
            "provider_type": Source.ProviderType.MANUAL,
            "base_url": "https://example.com",
        }
        values.update(kwargs)
        values.setdefault("slug", f"fonte-manual-{Source.objects.count() + 1}")
        return Source.objects.create(**values)
