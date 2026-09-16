from django.contrib import admin

from .models import Flight, Prediction


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("name", "site", "launch_date", "status", "booster_caught", "ship_splashdown")
    list_filter = ("status", "site")
    search_fields = ("name",)
    fieldsets = (
        (None, {"fields": ("name", "site", "launch_date", "description", "status")}),
        (
            "Итоги полёта",
            {
                "description": "Заполните после полёта и переведите статус в «Состоялся» — очки начислятся автоматически.",
                "fields": ("booster_caught", "ship_splashdown", "actual_launch_time"),
            },
        ),
    )


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("flight", "author", "booster_caught", "ship_splashdown", "predicted_launch_time")
    list_filter = ("flight",)
