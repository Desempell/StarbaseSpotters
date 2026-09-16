from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from core.mixins import AuthorRequiredMixin

from .forms import PredictionForm
from .models import T0_TOLERANCE, Flight, Prediction
from .scoring import leaderboard


class FlightListView(ListView):
    template_name = "flights/flight_list.html"
    context_object_name = "flights"

    def get_queryset(self):
        return Flight.objects.annotate(prediction_count=Count("predictions"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        flights = list(self.object_list)
        context["upcoming"] = sorted(
            (f for f in flights if f.status == Flight.Status.PLANNED and f.launch_date >= now),
            key=lambda f: f.launch_date,
        )
        context["past"] = [f for f in flights if f not in context["upcoming"]]
        return context


class FlightDetailView(DetailView):
    model = Flight
    template_name = "flights/flight_detail.html"
    context_object_name = "flight"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        predictions = list(self.object.predictions.select_related("author", "flight"))
        user = self.request.user
        total = len(predictions)
        context["predictions"] = predictions
        context["user_prediction"] = next(
            (p for p in predictions if user.is_authenticated and p.author_id == user.id), None
        )
        context["crowd"] = {
            "total": total,
            "booster_yes": round(100 * sum(p.booster_caught for p in predictions) / total) if total else 0,
            "ship_yes": round(100 * sum(p.ship_splashdown for p in predictions) / total) if total else 0,
        }
        context["tolerance_minutes"] = int(T0_TOLERANCE.total_seconds() // 60)
        return context


class PredictionsOpenMixin:

    def get_flight(self):
        raise NotImplementedError

    def dispatch(self, request, *args, **kwargs):
        flight = self.get_flight()
        if not flight.predictions_open:
            messages.warning(request, "Приём прогнозов на этот полёт закрыт.")
            return redirect(flight)
        return super().dispatch(request, *args, **kwargs)


class PredictionCreateView(PredictionsOpenMixin, LoginRequiredMixin, CreateView):
    model = Prediction
    form_class = PredictionForm
    template_name = "flights/prediction_form.html"

    def get_flight(self):
        self.flight = get_object_or_404(Flight, pk=self.kwargs["pk"])
        return self.flight

    def get(self, request, *args, **kwargs):
        existing = self.flight.predictions.filter(author=request.user).first()
        if existing:
            return redirect("flights:prediction_update", pk=existing.pk)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        existing = self.flight.predictions.filter(author=request.user).first()
        if existing:
            messages.info(request, "Вы уже сделали прогноз — его можно изменить.")
            return redirect("flights:prediction_update", pk=existing.pk)
        return super().post(request, *args, **kwargs)

    def get_initial(self):
        return {"predicted_launch_time": self.flight.launch_date}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flight"] = self.flight
        return context

    def form_valid(self, form):
        form.instance.flight = self.flight
        form.instance.author = self.request.user
        messages.success(self.request, "Прогноз принят. Удачи!")
        return super().form_valid(form)


class PredictionUpdateView(PredictionsOpenMixin, AuthorRequiredMixin, UpdateView):
    model = Prediction
    form_class = PredictionForm
    template_name = "flights/prediction_form.html"

    def get_flight(self):
        return get_object_or_404(Prediction.objects.select_related("flight"), pk=self.kwargs["pk"]).flight

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flight"] = self.object.flight
        return context

    def form_valid(self, form):
        messages.success(self.request, "Прогноз обновлён.")
        return super().form_valid(form)


class PredictionDeleteView(PredictionsOpenMixin, AuthorRequiredMixin, DeleteView):
    model = Prediction
    template_name = "confirm_delete.html"

    def get_flight(self):
        return get_object_or_404(Prediction.objects.select_related("flight"), pk=self.kwargs["pk"]).flight

    def get_success_url(self):
        return self.object.flight.get_absolute_url()

    def form_valid(self, form):
        messages.success(self.request, "Прогноз удалён.")
        return super().form_valid(form)


class LeaderboardView(TemplateView):
    template_name = "flights/leaderboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rows"] = leaderboard()
        return context
