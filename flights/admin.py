from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Flight, Prediction


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("name", "site", "launch_date", "status", "booster_caught", "ship_splashdown")
    list_filter = ("status", "site")
    search_fields = ("name",)
    fieldsets = (
        (None, {"fields": ("name", "site", "launch_date", "description", "status")}),
        (
            _("Flight results"),
            {
                "description": _(
                    "Fill in after the flight and set the status to “Completed” — "
                    "points will be awarded automatically."
                ),
                "fields": ("booster_caught", "ship_splashdown", "actual_launch_time"),
            },
        ),
    )


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("flight", "author", "booster_caught", "ship_splashdown", "predicted_launch_time")
    list_filter = ("flight",)
