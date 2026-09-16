from django.urls import path

from . import views

app_name = "spots"

urlpatterns = [
    path("", views.SpotListView.as_view(), name="list"),
    path("new/", views.SpotCreateView.as_view(), name="create"),
    path("<int:pk>/", views.SpotDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.SpotUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.SpotDeleteView.as_view(), name="delete"),
    path("<int:pk>/reviews/new/", views.ReviewCreateView.as_view(), name="review_create"),
    path("reviews/<int:pk>/edit/", views.ReviewUpdateView.as_view(), name="review_update"),
    path("reviews/<int:pk>/delete/", views.ReviewDeleteView.as_view(), name="review_delete"),
]
