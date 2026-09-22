from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FlightsConfig(AppConfig):
    name = "flights"
    verbose_name = _("Flights and predictions")
