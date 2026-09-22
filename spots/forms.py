from django import forms
from django.utils.translation import gettext_lazy as _

from core.forms import BootstrapFormMixin

from .models import Review, Spot


class SpotForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Spot
        fields = [
            "title",
            "site",
            "description",
            "latitude",
            "longitude",
            "distance_km",
            "visibility",
            "crowd",
            "has_parking",
            "has_cell_signal",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "visibility": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "latitude": forms.NumberInput(attrs={"step": "0.000001", "placeholder": "25.997"}),
            "longitude": forms.NumberInput(attrs={"step": "0.000001", "placeholder": "-97.157"}),
        }
        help_texts = {
            "latitude": _("Optional. If you add coordinates, the spot will appear on the map."),
        }


class ReviewForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "text"]
        widgets = {
            "rating": forms.Select(choices=[(i, "★" * i + "☆" * (5 - i)) for i in range(5, 0, -1)]),
            "text": forms.Textarea(
                attrs={"rows": 3, "placeholder": _("How well can you see the launch? Where to park? When to arrive?")}
            ),
        }
