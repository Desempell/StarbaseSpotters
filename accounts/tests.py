import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from conftest import PASSWORD

pytestmark = pytest.mark.django_db


def test_signup_creates_user_and_logs_in(client):
    response = client.post(
        reverse("signup"),
        {"username": "starfan", "email": "", "password1": PASSWORD, "password2": PASSWORD},
    )
    assert response.status_code == 302
    assert User.objects.filter(username="starfan").exists()
    assert "_auth_user_id" in client.session


def test_signup_rejects_mismatched_passwords(client):
    response = client.post(
        reverse("signup"),
        {"username": "starfan", "password1": PASSWORD, "password2": PASSWORD + "x"},
    )
    assert response.status_code == 200
    assert not User.objects.filter(username="starfan").exists()


def test_login_redirects_home(client, user):
    response = client.post(reverse("login"), {"username": "alice", "password": PASSWORD})
    assert response.status_code == 302
    assert response.url == reverse("home")


def test_logout(client, user):
    client.force_login(user)
    client.post(reverse("logout"))
    assert "_auth_user_id" not in client.session


def test_profile_shows_user_content(client, spot):
    response = client.get(reverse("profile", args=["alice"]))
    assert response.status_code == 200
    assert spot.title in response.content.decode()


def test_unknown_profile_is_404(client, db):
    assert client.get(reverse("profile", args=["nobody"])).status_code == 404
