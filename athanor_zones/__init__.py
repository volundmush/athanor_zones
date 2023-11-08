from collections import defaultdict


def init(settings, plugins: dict):
    import athanor

    settings.INSTALLED_APPS.append("athanor_zones")
    settings.BASE_ZONE_TYPECLASS = "athanor_zones.zones.DefaultZone"
    settings.CMD_MODULES_CHARACTER.append("athanor_zones.commands")
    settings.AT_SERVER_STARTSTOP_MODULE.append("athanor_zones.startup_hooks")
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
        "traverse",
        "teleport_here",
    ]

    for zat in settings.ZONE_ACCESS_TYPES:
        settings.OBJECT_ACCESS_FUNCTIONS[zat].append("athanor_zones.access.zone")

    settings.OPTIONS_ZONE_DEFAULT = dict()
