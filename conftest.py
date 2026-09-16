from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from flights.models import Flight
from spots.models import Spot

PASSWORD = "Str0ng-pass-for-tests"


@pytest.fixture
def user(db):
    return User.objects.create_user("alice", password=PASSWORD)


@pytest.fixture
def other_user(db):
    return User.objects.create_user("bob", password=PASSWORD)


@pytest.fixture
def spot(user):
    return Spot.objects.create(title="Isla Blanca Park", author=user, visibility=5)


@pytest.fixture
def planned_flight(db):
    return Flight.objects.create(name="Flight 99", launch_date=timezone.now() + timedelta(days=3))


@pytest.fixture
def resolved_flight(db):
    launch = timezone.now() - timedelta(days=5)
    return Flight.objects.create(
        name="Flight 98",
        launch_date=launch,
        status=Flight.Status.COMPLETED,
        booster_caught=True,
        ship_splashdown=False,
        actual_launch_time=launch + timedelta(minutes=20),
    )
