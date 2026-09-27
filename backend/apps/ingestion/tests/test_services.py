import pytest
from decimal import Decimal

from apps.ingestion.services import ingest_provider
from apps.listings.models import Listing
from apps.sources.providers import ManualProvider
from apps.sources.tests.factories import SourceFactory
from apps.sources.tests.test_provider import sample_record


@pytest.mark.django_db
def test_provider_pipeline_persists_normalized_listings():
    source = SourceFactory.create()
    provider = ManualProvider({"manual-001": sample_record()})

    persisted = ingest_provider(source, provider)

    listing = Listing.objects.get(source=source, external_id="manual-001")
    assert persisted == [listing]
    assert listing.price == Decimal("650000.00")
    assert listing.area == Decimal("80.50")
    assert listing.bedrooms == 3
    assert listing.transaction_type == Listing.TransactionType.SALE


@pytest.mark.django_db
def test_provider_pipeline_updates_existing_listing():
    source = SourceFactory.create()
    provider = ManualProvider({"manual-001": sample_record()})
    first = ingest_provider(source, provider)[0]

    changed = sample_record()
    changed["price"] = "R$ 640.000,00"
    ingest_provider(source, ManualProvider({"manual-001": changed}))

    assert Listing.objects.get(pk=first.pk).price == Decimal("640000.00")
    assert Listing.objects.filter(source=source, external_id="manual-001").count() == 1
