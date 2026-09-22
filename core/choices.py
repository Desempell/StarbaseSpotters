from django.db import models
from django.utils.translation import gettext_lazy as _


class LaunchSite(models.TextChoices):
    STARBASE = "starbase", _("Starbase, Texas")
    KSC = "ksc", _("Kennedy Space Center, Florida")
