from datetime import timedelta

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from core.choices import LaunchSite

RATING_VALIDATORS = [MinValueValidator(1), MaxValueValidator(5)]


class Spot(models.Model):

    class Crowd(models.TextChoices):
        LOW = "low", "Почти никого"
        MEDIUM = "medium", "Умеренно"
        HIGH = "high", "Толпа"

    title = models.CharField("название", max_length=120)
    site = models.CharField(
        "космодром", max_length=20, choices=LaunchSite.choices, default=LaunchSite.STARBASE
    )
    description = models.TextField("описание", blank=True)
    latitude = models.DecimalField(
        "широта",
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        "долгота",
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    distance_km = models.DecimalField(
        "до стартового стола, км",
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    visibility = models.PositiveSmallIntegerField(
        "обзор (1–5)", validators=RATING_VALIDATORS, default=3
    )
    crowd = models.CharField("людей", max_length=10, choices=Crowd.choices, default=Crowd.MEDIUM)
    has_parking = models.BooleanField("есть парковка", default=False)
    has_cell_signal = models.BooleanField("есть мобильная связь", default=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="spots", verbose_name="автор"
    )
    created_at = models.DateTimeField("создано", auto_now_add=True)
    updated_at = models.DateTimeField("изменено", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "точка наблюдения"
        verbose_name_plural = "точки наблюдения"
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
        Spot, on_delete=models.CASCADE, related_name="reviews", verbose_name="точка"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews", verbose_name="автор"
    )
    rating = models.PositiveSmallIntegerField("оценка", validators=RATING_VALIDATORS)
    text = models.TextField("отзыв", max_length=2000)
    created_at = models.DateTimeField("создано", auto_now_add=True)
    updated_at = models.DateTimeField("изменено", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
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
