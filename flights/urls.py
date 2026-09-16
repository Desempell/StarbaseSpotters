from django.urls import path

from . import views

app_name = "flights"

urlpatterns = [
    path("", views.FlightListView.as_view(), name="list"),
    path("leaderboard/", views.LeaderboardView.as_view(), name="leaderboard"),
    path("<int:pk>/", views.FlightDetailView.as_view(), name="detail"),
    path("<int:pk>/predict/", views.PredictionCreateView.as_view(), name="prediction_create"),
    path("predictions/<int:pk>/edit/", views.PredictionUpdateView.as_view(), name="prediction_update"),
    path("predictions/<int:pk>/delete/", views.PredictionDeleteView.as_view(), name="prediction_delete"),
]
