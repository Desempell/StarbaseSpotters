from django import template

register = template.Library()


@register.filter
def stars(value, max_stars=5):
    if value is None:
        return ""
    max_stars = int(max_stars)
    filled = max(0, min(max_stars, round(float(value))))
    return "★" * filled + "☆" * (max_stars - filled)
