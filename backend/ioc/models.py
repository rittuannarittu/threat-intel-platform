from django.db import models
from django.utils import timezone


class Source(models.Model):
    """
    A threat-intelligence feed or data source.
    Example: AbuseIPDB, AlienVault OTX, MalwareBazaar, etc.
    """
    name = models.CharField(max_length=128, unique=True)
    type = models.CharField(
        max_length=64,
        blank=True,
        help_text="Optional: e.g. 'ip-reputation', 'malware-feed', etc."
    )
    api_url = models.URLField(
        blank=True,
        help_text="Base API URL for this source (if applicable)."
    )

    def __str__(self) -> str:
        return self.name


class IOC(models.Model):
    """
    Indicator of Compromise (IOC).
    Stores IPs / domains / hashes / URLs along with where they came from.
    """

    TYPE_IP = "ip"
    TYPE_DOMAIN = "domain"
    TYPE_HASH = "hash"
    TYPE_URL = "url"

    TYPE_CHOICES = [
        (TYPE_IP, "IP"),
        (TYPE_DOMAIN, "Domain"),
        (TYPE_HASH, "Hash"),
        (TYPE_URL, "URL"),
    ]

    ioc_type = models.CharField(
        max_length=16,
        choices=TYPE_CHOICES,
        db_index=True,
    )
    value = models.TextField(
        db_index=True,
        help_text="The raw IOC value (IP address, domain, hash, URL, etc.).",
    )
    source = models.ForeignKey(
        Source,
        on_delete=models.SET_NULL,
        null=True,
        related_name="iocs",
        help_text="Which feed / source reported this IOC.",
    )
    first_seen = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this IOC was first observed (if known).",
    )
    last_seen = models.DateTimeField(
        auto_now=True,
        help_text="Automatically updated when this record is saved.",
    )
    confidence = models.FloatField(
        default=0.5,
        help_text="Confidence score between 0 and 1.",
    )

    class Meta:
        indexes = [
            models.Index(fields=["ioc_type", "value"]),
        ]
        ordering = ["-last_seen"]

    def save(self, *args, **kwargs):
        # If first_seen not set, default it to 'now' on first save
        if self.first_seen is None:
            self.first_seen = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.ioc_type}:{self.value}"


class Correlation(models.Model):
    """
    A relationship between two IOCs.
    For example: same IP, same domain, same campaign, etc.
    """
    ioc1 = models.ForeignKey(
        IOC,
        on_delete=models.CASCADE,
        related_name="corr_from",
    )
    ioc2 = models.ForeignKey(
        IOC,
        on_delete=models.CASCADE,
        related_name="corr_to",
    )
    match_type = models.CharField(
        max_length=64,
        help_text="Rule or reason for the match, e.g. 'same_ip', 'same_domain'.",
    )
    confidence = models.FloatField(
        default=0.5,
        help_text="Confidence score for this correlation (0–1).",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ("ioc1", "ioc2", "match_type")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.match_type}: {self.ioc1} -> {self.ioc2}"
