from apps.analytics.models import RedirectEvent


class RedirectEventFactory:
    @staticmethod
    def create(**kwargs):
        from apps.listings.tests.factories import ListingFactory

        values = {
            "listing": kwargs.pop("listing", None) or ListingFactory.create(),
            "session_id": "session-001",
            "referer": "https://placecheck.local/busca",
            "user_agent": "pytest",
        }
        values.update(kwargs)
        return RedirectEvent.objects.create(**values)
