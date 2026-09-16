from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from core.choices import LaunchSite

T0_TOLERANCE = timedelta(minutes=30)
MAX_SCORE = 3


class Flight(models.Model):

    class Status(models.TextChoices):
        PLANNED = "planned", "Запланирован"
        COMPLETED = "completed", "Состоялся"
        SCRUBBED = "scrubbed", "Отменён"

    name = models.CharField("название", max_length=80, unique=True)
    site = models.CharField(
        "космодром", max_length=20, choices=LaunchSite.choices, default=LaunchSite.STARBASE
    )
    launch_date = models.DateTimeField("плановое время старта (UTC)")
    description = models.TextField("описание", blank=True)
    status = models.CharField("статус", max_length=10, choices=Status.choices, default=Status.PLANNED)

    booster_caught = models.BooleanField("бустер пойман башней", null=True, blank=True)
    ship_splashdown = models.BooleanField("корабль приводнился", null=True, blank=True)
    actual_launch_time = models.DateTimeField("фактическое время старта (UTC)", null=True, blank=True)

    class Meta:
        ordering = ["-launch_date"]
        verbose_name = "полёт"
        verbose_name_plural = "полёты"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("flights:detail", args=[self.pk])

    def clean(self):
        if self.status == self.Status.COMPLETED and not self.has_outcome:
            raise ValidationError(
                "Для состоявшегося полёта заполните все результаты: бустер, корабль и фактическое время старта."
            )

    @property
    def has_outcome(self):
        return (
            self.booster_caught is not None
            and self.ship_splashdown is not None
            and self.actual_launch_time is not None
        )

    @property
    def is_resolved(self):
        return self.status == self.Status.COMPLETED and self.has_outcome

    @property
    def predictions_open(self):
        return self.status == self.Status.PLANNED and timezone.now() < self.launch_date


class PredictionQuerySet(models.QuerySet):
    def resolved(self):
        return self.filter(
            flight__status=Flight.Status.COMPLETED,
            flight__booster_caught__isnull=False,
            flight__ship_splashdown__isnull=False,
            flight__actual_launch_time__isnull=False,
        )


class Prediction(models.Model):

    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="predictions", verbose_name="полёт"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="predictions",
        verbose_name="автор",
    )
    booster_caught = models.BooleanField("бустер поймают башней?")
    ship_splashdown = models.BooleanField("корабль успешно приводнится?")
    predicted_launch_time = models.DateTimeField("во сколько реально стартуют (UTC)?")
    comment = models.TextField("комментарий", max_length=500, blank=True)
    created_at = models.DateTimeField("создано", auto_now_add=True)
    updated_at = models.DateTimeField("изменено", auto_now=True)

    objects = PredictionQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "прогноз"
        verbose_name_plural = "прогнозы"
        constraints = [
            models.UniqueConstraint(fields=["flight", "author"], name="one_prediction_per_user_per_flight"),
        ]

    def __str__(self):
        return f"{self.author} → {self.flight}"

    def get_absolute_url(self):
        return self.flight.get_absolute_url()

    def score(self):
        flight = self.flight
        if not flight.is_resolved:
            return None
        points = int(self.booster_caught == flight.booster_caught)
        points += int(self.ship_splashdown == flight.ship_splashdown)
        if abs(self.predicted_launch_time - flight.actual_launch_time) <= T0_TOLERANCE:
            points += 1
        return points
