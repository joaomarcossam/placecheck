import pytest

from apps.properties.models import Property
from apps.properties.tests.factories import PropertyFactory


@pytest.mark.django_db
def test_property_represents_a_place_not_an_ad():
    property_ = PropertyFactory.create()

    assert property_.city == "São Paulo"
    assert property_.get_property_type_display() == "Apartamento"
