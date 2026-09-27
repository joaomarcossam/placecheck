import pytest

from apps.analytics.tests.factories import RedirectEventFactory


@pytest.mark.django_db
def test_redirect_event_records_original_listing_and_session():
    event = RedirectEventFactory.create()

    assert event.listing_id is not None
    assert event.session_id == "session-001"
