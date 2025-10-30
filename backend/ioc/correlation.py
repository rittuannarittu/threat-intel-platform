from .models import IOC, Correlation

def correlate():
    created = 0
    # deterministic: same value & type across different sources
    for ioc in IOC.objects.all().iterator():
        matches = IOC.objects.filter(ioc_type=ioc.ioc_type, value=ioc.value).exclude(id=ioc.id)
        for m in matches:
            i1, i2 = (ioc, m) if ioc.id < m.id else (m, ioc)
            obj, made = Correlation.objects.get_or_create(
                ioc1=i1, ioc2=i2, match_type=f"same_{ioc.ioc_type}",
                defaults={"confidence": (ioc.confidence + m.confidence)/2}
            )
            if made: created += 1
    return created
