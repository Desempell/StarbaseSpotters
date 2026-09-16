from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone

from .models import T0_TOLERANCE, Flight, Prediction
from .scoring import leaderboard, user_stats

pytestmark = pytest.mark.django_db


def make_prediction(flight, author, **overrides):
    fields = {
        "booster_caught": True,
        "ship_splashdown": False,
        "predicted_launch_time": flight.actual_launch_time or flight.launch_date,
        **overrides,
    }
    return Prediction.objects.create(flight=flight, author=author, **fields)


def form_data(flight, **overrides):
    return {
        "booster_caught": "True",
        "ship_splashdown": "False",
        "predicted_launch_time": flight.launch_date.strftime("%Y-%m-%dT%H:%M"),
        "comment": "",
        **overrides,
    }


def test_perfect_prediction_scores_max(resolved_flight, user):
    assert make_prediction(resolved_flight, user).score() == 3


def test_partial_prediction(resolved_flight, user):
    prediction = make_prediction(
        resolved_flight,
        user,
        booster_caught=False,
        predicted_launch_time=resolved_flight.actual_launch_time + timedelta(hours=2),
    )
    assert prediction.score() == 1


def test_launch_time_tolerance_is_inclusive(resolved_flight, user):
    prediction = make_prediction(
        resolved_flight, user, predicted_launch_time=resolved_flight.actual_launch_time - T0_TOLERANCE
    )
    assert prediction.score() == 3


def test_unresolved_flight_has_no_score(planned_flight, user):
    assert make_prediction(planned_flight, user).score() is None


def test_completed_flight_requires_outcome():
    flight = Flight(name="Flight X", launch_date=timezone.now(), status=Flight.Status.COMPLETED)
    with pytest.raises(ValidationError):
        flight.clean()


def test_create_prediction_when_open(client, user, planned_flight):
    client.force_login(user)
    response = client.post(reverse("flights:prediction_create", args=[planned_flight.pk]), form_data(planned_flight))
    assert response.status_code == 302
    prediction = Prediction.objects.get(flight=planned_flight, author=user)
    assert prediction.booster_caught is True
    assert prediction.ship_splashdown is False


def test_second_prediction_redirects_to_edit(client, user, planned_flight):
    existing = make_prediction(planned_flight, user)
    client.force_login(user)
    response = client.post(reverse("flights:prediction_create", args=[planned_flight.pk]), form_data(planned_flight))
    assert response.url == reverse("flights:prediction_update", args=[existing.pk])
    assert Prediction.objects.count() == 1


def test_predictions_closed_after_launch(client, user, resolved_flight):
    client.force_login(user)
    response = client.post(reverse("flights:prediction_create", args=[resolved_flight.pk]), form_data(resolved_flight))
    assert response.status_code == 302
    assert not Prediction.objects.exists()


def test_cannot_edit_prediction_after_launch(client, user, planned_flight):
    prediction = make_prediction(planned_flight, user)
    planned_flight.launch_date = timezone.now() - timedelta(minutes=1)
    planned_flight.save()
    client.force_login(user)
    client.post(
        reverse("flights:prediction_update", args=[prediction.pk]),
        form_data(planned_flight, booster_caught="False"),
    )
    prediction.refresh_from_db()
    assert prediction.booster_caught is True


def test_other_user_cannot_edit_prediction(client, user, other_user, planned_flight):
    prediction = make_prediction(planned_flight, user)
    client.force_login(other_user)
    response = client.post(reverse("flights:prediction_update", args=[prediction.pk]), form_data(planned_flight))
    assert response.status_code == 403


def test_leaderboard_orders_by_points(resolved_flight, planned_flight, user, other_user):
    make_prediction(resolved_flight, user)
    make_prediction(resolved_flight, other_user, booster_caught=False, ship_splashdown=True)
    make_prediction(planned_flight, other_user)

    rows = leaderboard()
    assert [row.user for row in rows] == [user, other_user]
    assert rows[0].accuracy == 100
    assert user_stats(other_user).predictions == 1


def test_public_pages(client, planned_flight, resolved_flight):
    for url in (
        reverse("home"),
        reverse("flights:list"),
        reverse("flights:leaderboard"),
        planned_flight.get_absolute_url(),
        resolved_flight.get_absolute_url(),
    ):
        assert client.get(url).status_code == 200, url
