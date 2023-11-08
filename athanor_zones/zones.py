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

    zone_access_types = settings.ZONE_ACCESS_TYPES

    def at_first_save(self):
        pass

    @lazy_property
    def options(self):
        return OptionHandler(
            self,
            options_dict=settings.OPTIONS_ZONE_DEFAULT,
            savefunc=self.attributes.add,
            loadfunc=self.attributes.get,
            save_kwargs={"category": "option"},
            load_kwargs={"category": "option"},
        )

    def access(self, *args, **kwargs):
        if kwargs.pop("check_admin", True) and self.check_admin(args[0]):
            return True
        if super().access(*args, **kwargs):
            return True
        if self.parent:
            return self.parent.access(*args, check_admin=False, **kwargs)
        return False

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

    def add_object(self, obj: "DefaultObject"):
        if z := getattr(obj, "zone", None):
            if z == self:
                return
            self.objects.filter(id=obj).delete()
        z, created = self.objects.get_or_create(id=obj)
        self.at_add_object(obj)

    def at_add_object(self, obj: "DefaultObject"):
        for a_type in self.zone_access_types:
            obj.locks.remove(a_type)

    def check_override(self, accessing_obj):
        return self.__class__.objects.check_override(accessing_obj)

    def check_admin(self, accessing_obj):
        return self.__class__.objects.check_admin(accessing_obj)
