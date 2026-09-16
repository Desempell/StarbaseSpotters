import pytest
from django.urls import reverse

from core.choices import LaunchSite

from .models import Review, Spot

pytestmark = pytest.mark.django_db

SPOT_DATA = {
    "title": "Queen Isabella Causeway",
    "site": LaunchSite.STARBASE,
    "description": "Вид с моста",
    "latitude": "26.07",
    "longitude": "-97.2",
    "distance_km": "",
    "visibility": 4,
    "crowd": Spot.Crowd.MEDIUM,
    "has_parking": "on",
}


def test_list_and_detail_are_public(client, spot):
    assert client.get(reverse("spots:list")).status_code == 200
    assert client.get(spot.get_absolute_url()).status_code == 200


def test_anonymous_is_redirected_to_login(client):
    response = client.get(reverse("spots:create"))
    assert response.status_code == 302
    assert reverse("login") in response.url


def test_user_creates_spot(client, user):
    client.force_login(user)
    response = client.post(reverse("spots:create"), SPOT_DATA)
    spot = Spot.objects.get(title=SPOT_DATA["title"])
    assert response.status_code == 302
    assert spot.author == user
    assert spot.has_parking and not spot.has_cell_signal


def test_author_can_update_spot(client, user, spot):
    client.force_login(user)
    client.post(reverse("spots:update", args=[spot.pk]), {**SPOT_DATA, "title": "Новое имя"})
    spot.refresh_from_db()
    assert spot.title == "Новое имя"


def test_other_user_cannot_update_or_delete_spot(client, other_user, spot):
    client.force_login(other_user)
    assert client.post(reverse("spots:update", args=[spot.pk]), SPOT_DATA).status_code == 403
    assert client.post(reverse("spots:delete", args=[spot.pk])).status_code == 403
    assert Spot.objects.filter(pk=spot.pk, title="Isla Blanca Park").exists()


def test_author_can_delete_spot(client, user, spot):
    client.force_login(user)
    response = client.post(reverse("spots:delete", args=[spot.pk]))
    assert response.status_code == 302
    assert not Spot.objects.filter(pk=spot.pk).exists()


def test_list_filters_by_site(client, user, spot):
    Spot.objects.create(title="Playalinda", site=LaunchSite.KSC, author=user)
    response = client.get(reverse("spots:list"), {"site": LaunchSite.KSC})
    assert [s.title for s in response.context["spots"]] == ["Playalinda"]


def test_review_create_and_average(client, other_user, spot):
    client.force_login(other_user)
    client.post(reverse("spots:review_create", args=[spot.pk]), {"rating": 4, "text": "Отлично видно"})
    assert Review.objects.filter(spot=spot, author=other_user, rating=4).exists()
    response = client.get(spot.get_absolute_url())
    assert response.context["spot"].avg_rating == 4


def test_cannot_review_own_spot(client, user, spot):
    client.force_login(user)
    client.post(reverse("spots:review_create", args=[spot.pk]), {"rating": 5, "text": "Моя точка лучшая"})
    assert not Review.objects.exists()


def test_second_review_is_rejected(client, other_user, spot):
    Review.objects.create(spot=spot, author=other_user, rating=3, text="Первый")
    client.force_login(other_user)
    client.post(reverse("spots:review_create", args=[spot.pk]), {"rating": 5, "text": "Второй"})
    assert Review.objects.filter(spot=spot, author=other_user).count() == 1


def test_rating_out_of_range_is_invalid(client, other_user, spot):
    client.force_login(other_user)
    response = client.post(reverse("spots:review_create", args=[spot.pk]), {"rating": 6, "text": "?"})
    assert response.status_code == 200
    assert not Review.objects.exists()


def test_only_author_edits_review(client, user, other_user, spot):
    review = Review.objects.create(spot=spot, author=other_user, rating=3, text="Норм")
    client.force_login(user)
    response = client.post(reverse("spots:review_update", args=[review.pk]), {"rating": 1, "text": "Взлом"})
    assert response.status_code == 403
    review.refresh_from_db()
    assert review.rating == 3
