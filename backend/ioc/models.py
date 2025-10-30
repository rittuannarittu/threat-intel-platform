from django.db import models

class Source(models.Model):
    name = models.CharField(max_length=128, unique=True)
    type = models.CharField(max_length=64, blank=True)
    api_url = models.URLField(blank=True)
    def __str__(self): return self.name

class IOC(models.Model):
    TYPE_CHOICES = [("ip","IP"), ("domain","Domain"), ("hash","Hash"), ("url","URL")]
    ioc_type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    value = models.TextField(db_index=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, related_name="iocs")
    first_seen = models.DateTimeField(null=True, blank=True)
    last_seen = models.DateTimeField(auto_now=True)
    confidence = models.FloatField(default=0.5)

    class Meta:
        indexes = [models.Index(fields=["ioc_type","value"])]

    def __str__(self): return f"{self.ioc_type}:{self.value}"

class Correlation(models.Model):
    ioc1 = models.ForeignKey(IOC, on_delete=models.CASCADE, related_name="corr_from")
    ioc2 = models.ForeignKey(IOC, on_delete=models.CASCADE, related_name="corr_to")
    match_type = models.CharField(max_length=64)
    confidence = models.FloatField(default=0.5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("ioc1","ioc2","match_type")
