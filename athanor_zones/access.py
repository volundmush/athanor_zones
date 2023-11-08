def zone(accessed_obj, accessing_obj, access_type, **kwargs) -> bool:
    if not (z := getattr(accessed_obj, "zone", None)):
        return False
    return z.access(accessing_obj, access_type, **kwargs)
