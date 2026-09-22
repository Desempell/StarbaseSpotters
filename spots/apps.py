from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SpotsConfig(AppConfig):
    name = "spots"
    verbose_name = _("Viewing spots")
