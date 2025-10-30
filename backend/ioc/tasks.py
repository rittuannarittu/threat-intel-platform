from celery import shared_task
from django.conf import settings
from .models import IOC, Source
import requests

OTX_URL = "https://otx.alienvault.com/api/v1/indicators/export"
ABUSE_IPDB = "https://api.abuseipdb.com/api/v2/blacklist"
MALWAREBAZAAR_URL = "https://mb-api.abuse.ch/api/v1/"

def get_or_create_source(name, typ="", url=""):
    src, _ = Source.objects.get_or_create(name=name, defaults={"type":typ, "api_url":url})
    return src

@shared_task
def fetch_otx():
    key = settings.OTX_API_KEY
    if not key: return 0
    src = get_or_create_source("AlienVault OTX","feed", OTX_URL)
    params, headers = {"type":"IPv4","since":"1 day"}, {"X-OTX-API-KEY": key}
    r = requests.get(OTX_URL, headers=headers, params=params, timeout=20)
    count = 0
    if r.ok:
        for line in r.text.splitlines():
            val = line.strip()
            if val and not val.startswith("#"):
                IOC.objects.get_or_create(ioc_type="ip", value=val, source=src); count += 1
    return count

@shared_task
def fetch_abuseipdb():
    key = settings.ABUSEIPDB_API_KEY
    headers = {"Key": key, "Accept":"application/json"}
    src = get_or_create_source("AbuseIPDB","feed", ABUSE_IPDB)
    r = requests.get(ABUSE_IPDB, headers=headers, params={"confidenceMinimum":90}, timeout=20)
    count = 0
    if r.ok:
        for row in r.json().get("data", [])[:500]:
            IOC.objects.get_or_create(ioc_type="ip", value=row.get("ipAddress"), source=src); count += 1
    return count

@shared_task
def fetch_malwarebazaar():
    src = get_or_create_source("MalwareBazaar","feed", MALWAREBAZAAR_URL)
    r = requests.post(MALWAREBAZAAR_URL, data={"query":"get_recent","selector":"time"}, timeout=20)
    count = 0
    if r.ok:
        for item in r.json().get("data", [])[:500]:
            IOC.objects.get_or_create(ioc_type="hash", value=item.get("sha256_hash"), source=src); count += 1
    return count

@shared_task
def run_all_feeds():
    return {
        "otx": fetch_otx(),
        "abuseipdb": fetch_abuseipdb(),
        "malwarebazaar": fetch_malwarebazaar()
    }
