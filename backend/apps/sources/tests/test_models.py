import pytest
from django.db import IntegrityError

from apps.sources.models import Source
from apps.sources.tests.factories import SourceFactory


@pytest.mark.django_db
def test_source_has_unique_slug():
    SourceFactory.create(slug="fonte-manual")

    with pytest.raises(IntegrityError):
        SourceFactory.create(name="Outra fonte", slug="fonte-manual")


@pytest.mark.django_db
def test_source_can_be_registered_manually():
    source = SourceFactory.create(name="Portal autorizado")

    assert source.provider_type == Source.ProviderType.MANUAL
    assert source.is_active is True
