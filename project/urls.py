from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from apps.balance.urls import patterns as balance_patterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include((balance_patterns, "balance"))),
]

if settings.DEBUG:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
