from django.db.models import Avg, Count
from django.utils import timezone
from django.views.generic import TemplateView

from flights.models import Flight, Prediction
from flights.scoring import leaderboard
from spots.models import Review, Spot


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next_flight"] = (
            Flight.objects.filter(status=Flight.Status.PLANNED, launch_date__gte=timezone.now())
            .order_by("launch_date")
            .first()
        )
        context["top_spots"] = (
            Spot.objects.annotate(avg_rating=Avg("reviews__rating"), review_count=Count("reviews"))
            .filter(review_count__gt=0)
            .order_by("-avg_rating", "-review_count")[:3]
        )
        context["leaders"] = leaderboard(limit=5)
        context["totals"] = {
            "spots": Spot.objects.count(),
            "reviews": Review.objects.count(),
            "predictions": Prediction.objects.count(),
        }
        return context
