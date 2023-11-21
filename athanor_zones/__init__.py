from collections import defaultdict


def init(settings, plugins: dict):
    import athanor

    settings.INSTALLED_APPS.append("athanor_zones")
    settings.BASE_ZONE_TYPECLASS = "athanor_zones.zones.DefaultZone"
    settings.CMD_MODULES_CHARACTER.append("athanor_zones.commands")
    settings.ZONE_ACCESS_FUNCTIONS = defaultdict(list)
    athanor.ZONE_ACCESS_FUNCTIONS = defaultdict(list)

    # those who pass this lockstring always pass permission checks on Zones.
    # This is required to manage Zones. (Create, Delete, Re-parent, Rename, change locks, etc).
    settings.ZONE_PERMISSIONS_ADMIN_OVERRIDE = "perm(Developer)"

    # those who pass this lockstring are considered to be "Builders" for all Zones.
    settings.ZONE_PERMISSIONS_ADMIN_BUILDER = "perm(Admin)"

    # These are the access_types that will be removed from an object when
    # it is added to the Zone.
    settings.ZONE_ACCESS_TYPES = [
        "control",
        "delete",
        "edit",
        "examine",
        "teleport_here",
    ]

    settings.ZONE_DEFAULT_LOCK_TYPES = [
        "OBJECT_OBJECT",
        "OBJECT_ROOM",
        "OBJECT_CHARACTER",
        "OBJECT_EXIT",
    ]

    settings.OPTIONS_ZONE_DEFAULT = dict()

    settings.ACCESS_FUNCTIONS_LIST.append("ZONE")


def post_init(settings, plugins):
    for t in settings.ZONE_DEFAULT_LOCK_TYPES:
        func_type = f"{t}_DEFAULT_LOCKS"
        func_dict = getattr(settings, func_type)

        for zat in settings.ZONE_ACCESS_TYPES:
            func_dict[zat].insert(0, "athanor_zones.access.zone")
