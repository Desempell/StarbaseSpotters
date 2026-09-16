from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, F, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.choices import LaunchSite
from core.mixins import AuthorRequiredMixin

from .forms import ReviewForm, SpotForm
from .models import Review, Spot


def with_rating(queryset):
    return queryset.annotate(avg_rating=Avg("reviews__rating"), review_count=Count("reviews"))


def map_point(spot):
    return {
        "title": spot.title,
        "url": spot.get_absolute_url(),
        "lat": float(spot.latitude),
        "lng": float(spot.longitude),
    }


class SpotListView(ListView):
    template_name = "spots/spot_list.html"
    context_object_name = "spots"
    paginate_by = 12

    def get_queryset(self):
        queryset = with_rating(Spot.objects.select_related("author")).order_by("-created_at")
        site = self.request.GET.get("site")
        if site in LaunchSite.values:
            queryset = queryset.filter(site=site)
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
        if self.request.GET.get("order") == "rating":
            queryset = queryset.order_by(F("avg_rating").desc(nulls_last=True), "-created_at")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sites"] = LaunchSite.choices
        context["current_site"] = self.request.GET.get("site", "")
        context["query"] = self.request.GET.get("q", "")
        context["order"] = self.request.GET.get("order", "")
        context["map_points"] = [
            map_point(spot) for spot in self.object_list if spot.has_coordinates
        ]
        return context


class SpotDetailView(DetailView):
    template_name = "spots/spot_detail.html"
    context_object_name = "spot"

    def get_queryset(self):
        return with_rating(Spot.objects.select_related("author"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spot = self.object
        reviews = spot.reviews.select_related("author")
        user = self.request.user
        context["reviews"] = reviews
        context["user_review"] = (
            reviews.filter(author=user).first() if user.is_authenticated else None
        )
        context["review_form"] = ReviewForm()
        context["map_points"] = [map_point(spot)] if spot.has_coordinates else []
        return context


class SpotCreateView(LoginRequiredMixin, CreateView):
    model = Spot
    form_class = SpotForm
    template_name = "spots/spot_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Точка наблюдения добавлена.")
        return super().form_valid(form)


class SpotUpdateView(AuthorRequiredMixin, UpdateView):
    model = Spot
    form_class = SpotForm
    template_name = "spots/spot_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Изменения сохранены.")
        return super().form_valid(form)


class SpotDeleteView(AuthorRequiredMixin, DeleteView):
    model = Spot
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("spots:list")

    def form_valid(self, form):
        messages.success(self.request, f"Точка «{self.object}» удалена.")
        return super().form_valid(form)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "spots/review_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.spot = get_object_or_404(Spot, pk=kwargs["pk"])
        if request.user.is_authenticated:
            if self.spot.author_id == request.user.id:
                messages.error(request, "Нельзя оценивать собственную точку.")
                return redirect(self.spot)
            if self.spot.reviews.filter(author=request.user).exists():
                messages.info(request, "Вы уже оставили отзыв — его можно отредактировать.")
                return redirect(self.spot)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["spot"] = self.spot
        return context

    def form_valid(self, form):
        form.instance.spot = self.spot
        form.instance.author = self.request.user
        messages.success(self.request, "Спасибо за отзыв!")
        return super().form_valid(form)


class ReviewUpdateView(AuthorRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "spots/review_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["spot"] = self.object.spot
        return context

    def form_valid(self, form):
        messages.success(self.request, "Отзыв обновлён.")
        return super().form_valid(form)


class ReviewDeleteView(AuthorRequiredMixin, DeleteView):
    model = Review
    template_name = "confirm_delete.html"

    def get_success_url(self):
        return self.object.spot.get_absolute_url()

    def form_valid(self, form):
        messages.success(self.request, "Отзыв удалён.")
        return super().form_valid(form)
