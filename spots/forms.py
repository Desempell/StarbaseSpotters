from django import forms

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
            "latitude": "Необязательно. Если указать координаты, точка появится на карте.",
        }


class ReviewForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "text"]
        widgets = {
            "rating": forms.Select(choices=[(i, "★" * i + "☆" * (5 - i)) for i in range(5, 0, -1)]),
            "text": forms.Textarea(attrs={"rows": 3, "placeholder": "Как видно запуск? Где парковаться? Когда приезжать?"}),
        }
