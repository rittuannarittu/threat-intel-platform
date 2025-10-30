from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import SourceViewSet, IOCViewSet, CorrelationViewSet, correlate_now

router = DefaultRouter()
router.register(r"sources", SourceViewSet)
router.register(r"iocs", IOCViewSet)
router.register(r"correlations", CorrelationViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("correlate/", correlate_now, name="correlate"),
]
