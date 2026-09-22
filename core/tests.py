import pytest
from django.core.management import call_command
from django.urls import reverse

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


@pytest.mark.django_db
def test_default_language_is_russian(client):
    response = client.get(reverse("home"))
    assert '<html lang="ru"' in response.content.decode()
    assert "Точки наблюдения" in response.content.decode()


@pytest.mark.django_db
def test_accept_language_switches_to_english(client):
    response = client.get(reverse("home"), headers={"accept-language": "en"})
    assert '<html lang="en"' in response.content.decode()
    assert "Viewing spots" in response.content.decode()


@pytest.mark.django_db
def test_set_language_persists_choice(client):
    response = client.post(reverse("set_language"), {"language": "en", "next": reverse("spots:list")})
    assert response.status_code == 302
    assert response.url == reverse("spots:list")
    assert "Search by title and description" in client.get(reverse("spots:list")).content.decode()
