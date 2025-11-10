from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
import requests

from ioc.models import IOC, Source


class Command(BaseCommand):
    help = "Fetch real IOCs from AbuseIPDB and store them"

    def handle(self, *args, **options):
        api_key = getattr(settings, "ABUSEIPDB_API_KEY", None)
        if not api_key:
            self.stderr.write(
                self.style.ERROR("No ABUSEIPDB_API_KEY set in settings / .env")
            )
            return

        url = "https://api.abuseipdb.com/api/v2/blacklist"

        headers = {
            "Key": api_key,
            "Accept": "application/json",
        }

        self.stdout.write("Requesting data from AbuseIPDB blacklist API...")

        try:
            response = requests.get(url, headers=headers, timeout=30)
        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Request to AbuseIPDB failed: {e}"))
            return

        if response.status_code != 200:
            self.stderr.write(
                self.style.ERROR(
                    f"AbuseIPDB API returned status {response.status_code}: "
                    f"{response.text[:200]}"
                )
            )
            return

        data = response.json()

        # Ensure we have a Source row for AbuseIPDB
        source_obj, _ = Source.objects.get_or_create(
            name="AbuseIPDB",
            defaults={
                "type": "ip-reputation",
                "api_url": url,
            },
        )

        created_count = 0
        updated_count = 0

        for item in data.get("data", []):
            ip = item.get("ipAddress")
            score = item.get("abuseConfidenceScore", 0)

            if not ip:
                continue

            # Normalise score to 0–1 range
            confidence = float(score) / 100.0

            # Use ioc_type (your model field), NOT type
            ioc, created = IOC.objects.update_or_create(
                value=ip,
                ioc_type=IOC.TYPE_IP,   # or just "ip"
                source=source_obj,
                defaults={
                    "confidence": confidence,
                    # Optional: set first_seen if blank
                    "first_seen": timezone.now(),
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done fetching real IOCs from AbuseIPDB "
                f"(created {created_count}, updated {updated_count})"
            )
        )
