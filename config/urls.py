from django.contrib import admin
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

from core.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("spots/", include("spots.urls")),
    path("flights/", include("flights.urls")),
]
