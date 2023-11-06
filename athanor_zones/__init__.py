from collections import defaultdict


def init(settings, plugins: dict):
    import athanor

    settings.INSTALLED_APPS.extend("athanor_zones")
    settings.CMD_MODULES_CHARACTER.append("athanor_zones.commands")
    settings.AT_SERVER_STARTSTOP_MODULE.append("athanor_zones.startup_hooks")
    settings.FACTION_ACCESS_FUNCTIONS = defaultdict(list)
    athanor.FACTION_ACCESS_FUNCTIONS = defaultdict(list)
