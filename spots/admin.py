from django.contrib import admin

from .models import Review, Spot


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0


@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ("title", "site", "visibility", "crowd", "author", "created_at")
    list_filter = ("site", "crowd", "has_parking", "has_cell_signal")
    search_fields = ("title", "description")
    inlines = [ReviewInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("spot", "author", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("text",)
