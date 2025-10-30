from rest_framework import viewsets, decorators, response
from .models import IOC, Source, Correlation
from .serializers import IOCSerializer, SourceSerializer, CorrelationSerializer
from .correlation import correlate

class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

class IOCViewSet(viewsets.ModelViewSet):
    queryset = IOC.objects.all().order_by("-last_seen")
    serializer_class = IOCSerializer
    filterset_fields = ["ioc_type","source__name"]

class CorrelationViewSet(viewsets.ModelViewSet):
    queryset = Correlation.objects.all().order_by("-created_at")
    serializer_class = CorrelationSerializer

@decorators.api_view(["POST"])
def correlate_now(request):
    created = correlate()
    return response.Response({"created": created})
