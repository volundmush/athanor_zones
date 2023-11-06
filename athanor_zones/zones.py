import typing

from django.conf import settings

from evennia.typeclasses.models import TypeclassBase
from evennia.utils.optionhandler import OptionHandler
from evennia.utils.utils import lazy_property

import athanor
from athanor.utils import partial_match
from athanor.typeclasses.mixin import AthanorAccess

from .models import ZoneDB
from .managers import ZoneManager


class DefaultZone(AthanorAccess, ZoneDB, metaclass=TypeclassBase):
    system_name = "ZONE"
    objects = ZoneManager()
    lock_access_functions = athanor.ZONE_ACCESS_FUNCTIONS

    def at_first_save(self):
        pass

    def ancestors(self):
        if self.parent:
            yield self.parent
            yield from self.parent.ancestors()

    def full_path(self):
        chain = [self]
        for ancestor in self.ancestors():
            chain.append(ancestor)
        return "/".join([f.key for f in reversed(chain)])

    def is_deleted(self):
        if self.deleted:
            return True
        if self.parent:
            return self.parent.is_deleted()
        return False
