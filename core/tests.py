import pytest
from django.core.management import call_command

from core.templatetags.spotters import stars
from flights.models import Flight
from spots.models import Spot


@pytest.mark.parametrize(
    ("value", "expected"),
    [(None, ""), (0, "☆☆☆☆☆"), (3.6, "★★★★☆"), (5, "★★★★★"), (9, "★★★★★")],
)
def test_stars_filter(value, expected):
    assert stars(value) == expected


@pytest.mark.django_db
def test_seed_demo_is_idempotent():
    call_command("seed_demo")
    call_command("seed_demo")
    assert Spot.objects.count() == 5
    assert Flight.objects.count() == 3
