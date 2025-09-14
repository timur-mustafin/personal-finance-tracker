from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/analytics/", include("analytics.urls")),
    path("api/core/", include("core.urls")),
    path("api/transactions/", include("transactions.urls")),
    path("api/auth/", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
