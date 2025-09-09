
from rest_framework.routers import DefaultRouter
from .views import ImportSessionViewSet

router = DefaultRouter()
router.register(r'import-sessions', ImportSessionViewSet, basename='importsession')

urlpatterns = router.urls
