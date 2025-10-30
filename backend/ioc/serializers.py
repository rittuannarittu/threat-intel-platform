from rest_framework import serializers
from .models import IOC, Source, Correlation

class SourceSerializer(serializers.ModelSerializer):
    class Meta: model = Source; fields = "__all__"

class IOCSerializer(serializers.ModelSerializer):
    source = SourceSerializer(read_only=True)
    source_id = serializers.PrimaryKeyRelatedField(
        queryset=Source.objects.all(), source="source", write_only=True, required=False)
    class Meta:
        model = IOC
        fields = ["id","ioc_type","value","source","source_id","first_seen","last_seen","confidence"]

class CorrelationSerializer(serializers.ModelSerializer):
    ioc1 = IOCSerializer(read_only=True)
    ioc1_id = serializers.PrimaryKeyRelatedField(queryset=IOC.objects.all(), source="ioc1", write_only=True)
    ioc2 = IOCSerializer(read_only=True)
    ioc2_id = serializers.PrimaryKeyRelatedField(queryset=IOC.objects.all(), source="ioc2", write_only=True)
    class Meta:
        model = Correlation
        fields = ["id","ioc1","ioc1_id","ioc2","ioc2_id","match_type","confidence","created_at"]
