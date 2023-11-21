from django.conf import settings


def zone(accessed_obj, access_type):
    if not (z := getattr(accessed_obj, "zone", None)):
        return None
    while z:
        if locks := z.locks.get(access_type, None):
            return locks
        z = z.parent
    return settings.ZONE_PERMISSIONS_ADMIN_BUILDER
