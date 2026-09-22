from datetime import timedelta

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from core.choices import LaunchSite

RATING_VALIDATORS = [MinValueValidator(1), MaxValueValidator(5)]


class Spot(models.Model):

    class Crowd(models.TextChoices):
        LOW = "low", _("Almost empty")
        MEDIUM = "medium", _("Moderate")
        HIGH = "high", _("Crowded")

    title = models.CharField(_("title"), max_length=120)
    site = models.CharField(
        _("launch site"), max_length=20, choices=LaunchSite.choices, default=LaunchSite.STARBASE
    )
    description = models.TextField(_("description"), blank=True)
    latitude = models.DecimalField(
        _("latitude"),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        _("longitude"),
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    distance_km = models.DecimalField(
        _("distance to launch pad, km"),
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    visibility = models.PositiveSmallIntegerField(
        _("visibility (1–5)"), validators=RATING_VALIDATORS, default=3
    )
    crowd = models.CharField(_("crowd"), max_length=10, choices=Crowd.choices, default=Crowd.MEDIUM)
    has_parking = models.BooleanField(_("parking available"), default=False)
    has_cell_signal = models.BooleanField(_("cell signal available"), default=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="spots", verbose_name=_("author")
    )
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated"), auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("viewing spot")
        verbose_name_plural = _("viewing spots")
        constraints = [
            models.CheckConstraint(
                condition=models.Q(visibility__gte=1, visibility__lte=5),
                name="spot_visibility_between_1_and_5",
            ),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("spots:detail", args=[self.pk])

    @property
    def has_coordinates(self):
        return self.latitude is not None and self.longitude is not None


class Review(models.Model):

    spot = models.ForeignKey(
        Spot, on_delete=models.CASCADE, related_name="reviews", verbose_name=_("spot")
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews", verbose_name=_("author")
    )
    rating = models.PositiveSmallIntegerField(_("rating"), validators=RATING_VALIDATORS)
    text = models.TextField(_("review"), max_length=2000)
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated"), auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("review")
        verbose_name_plural = _("reviews")
        constraints = [
            models.UniqueConstraint(fields=["spot", "author"], name="one_review_per_user_per_spot"),
            models.CheckConstraint(
                condition=models.Q(rating__gte=1, rating__lte=5),
                name="review_rating_between_1_and_5",
            ),
        ]

    def __str__(self):
        return f"{self.author} → {self.spot} ({self.rating}/5)"

    def get_absolute_url(self):
        return self.spot.get_absolute_url()

    @property
    def was_edited(self):
        return self.updated_at - self.created_at > timedelta(seconds=1)
