from django.db import models
from django.conf import settings
from evennia.typeclasses.models import TypedObject
from athanor.utils import utcnow
from .managers import ZoneDBManager


class ZoneDB(TypedObject):
    objects = ZoneDBManager()

    # defaults
    __settingsclasspath__ = settings.BASE_ZONE_TYPECLASS
    __defaultclasspath__ = "athanor_zones.zones.DefaultZone"
    __applabel__ = "athanor_zones"

    db_config = models.JSONField(null=False, default=dict)
    db_parent = models.ForeignKey(
        "self", related_name="children", null=True, blank=True, on_delete=models.PROTECT
    )
    db_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.key
