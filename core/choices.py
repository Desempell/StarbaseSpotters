from django.db import models


class LaunchSite(models.TextChoices):
    STARBASE = "starbase", "Starbase, Техас"
    KSC = "ksc", "Космический центр Кеннеди, Флорида"
