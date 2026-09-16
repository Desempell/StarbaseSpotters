from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from flights.scoring import user_stats

from .forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f"Добро пожаловать на борт, {self.object.username}!")
        return response


class ProfileView(DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "accounts/profile.html"
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.object
        context["spots"] = profile_user.spots.all()
        context["reviews"] = profile_user.reviews.select_related("spot")
        context["predictions"] = profile_user.predictions.select_related("flight")
        context["stats"] = user_stats(profile_user)
        return context
