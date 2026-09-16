from django.contrib.auth import views as auth_views
from django.urls import path

from .forms import LoginForm
from .views import ProfileView, SignUpView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(authentication_form=LoginForm), name="login"),
    path("users/<str:username>/", ProfileView.as_view(), name="profile"),
]
