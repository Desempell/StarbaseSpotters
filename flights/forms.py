from django import forms
from django.utils.translation import gettext_lazy as _

from core.forms import BootstrapFormMixin

from .models import Prediction

YES_NO = [("True", _("Yes")), ("False", _("No"))]


def yes_no_field(label):
    return forms.TypedChoiceField(
        label=label,
        choices=YES_NO,
        coerce=lambda value: value == "True",
        widget=forms.RadioSelect,
    )


class PredictionForm(BootstrapFormMixin, forms.ModelForm):
    booster_caught = yes_no_field(_("Will the tower catch the booster?"))
    ship_splashdown = yes_no_field(_("Will the ship splash down successfully?"))

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
            "predicted_launch_time": _("Counts if you are off by no more than 30 minutes."),
        }
