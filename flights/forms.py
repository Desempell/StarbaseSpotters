from django import forms

from core.forms import BootstrapFormMixin

from .models import Prediction

YES_NO = [("True", "Да"), ("False", "Нет")]


def yes_no_field(label):
    return forms.TypedChoiceField(
        label=label,
        choices=YES_NO,
        coerce=lambda value: value == "True",
        widget=forms.RadioSelect,
    )


class PredictionForm(BootstrapFormMixin, forms.ModelForm):
    booster_caught = yes_no_field("Бустер поймают башней?")
    ship_splashdown = yes_no_field("Корабль успешно приводнится?")

    class Meta:
        model = Prediction
        fields = ["booster_caught", "ship_splashdown", "predicted_launch_time", "comment"]
        widgets = {
            "predicted_launch_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "comment": forms.Textarea(attrs={"rows": 3}),
        }
        help_texts = {
            "predicted_launch_time": "Засчитывается, если ошибка не больше 30 минут.",
        }
