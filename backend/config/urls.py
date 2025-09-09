
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/analytics/', include('backend.analytics.urls')),

    path('api/core/', include('backend.core.urls')),

    path("api/", include("analytics.urls")),
    path("api/", include("importers.urls")),
    path("api/", include("transactions.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
    path("api/auth/", include("users.urls")),
]
