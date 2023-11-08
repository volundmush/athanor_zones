import re
import math
from django.db import IntegrityError, transaction
from django.db import models
from django.db.models.functions import Concat
from django.conf import settings
from evennia.typeclasses.managers import TypeclassManager, TypedObjectManager
from evennia.utils import class_from_module
from evennia.locks.lockhandler import LockException
from athanor.utils import (
    Operation,
    validate_name,
    online_accounts,
    online_characters,
    staff_alert,
    utcnow,
)


class ZoneDBManager(TypedObjectManager):
    system_name = "ZONE"

    def check_override(self, accessing_obj):
        return accessing_obj.locks.check_lockstring(
            accessing_obj, settings.ZONE_PERMISSIONS_ADMIN_OVERRIDE
        )

    def check_admin(self, accessing_obj):
        return accessing_obj.locks.check_lockstring(
            accessing_obj, settings.ZONE_PERMISSIONS_ADMIN_MEMBERSHIP
        ) or self.check_override(accessing_obj)

    def find_zone(self, operation: Operation, key: str = "zone"):
        if (input := operation.kwargs.get(key, None)) is None:
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex("You must provide a Zone ID or Path/Name.")

        if isinstance(input, self.model):
            zone = input
        elif isinstance(input, str):
            path = input.split("/")
            if not len(path):
                operation.status = operation.st.HTTP_400_BAD_REQUEST
                raise operation.ex("You must provide a Zone ID or Path/Name.")

            start_check = path[0]
            rest = path[1:]

            choices = self.filter(db_parent=None)
            if not choices:
                operation.status = operation.st.HTTP_404_NOT_FOUND
                raise operation.ex("No Factions found.")
            if not (choice := partial_match(start_check, choices)):
                operation.status = operation.st.HTTP_404_NOT_FOUND
                raise operation.ex(f"No Zone found called: {start_check}")

            while rest:
                start_check = rest[0]
                rest = rest[1:]
                choices = choice.children.all()
                if not choices:
                    operation.status = operation.st.HTTP_404_NOT_FOUND
                    raise operation.ex(f"No Factions found under: {start_check}")
                if not (new_choice := partial_match(start_check, choices)):
                    operation.status = operation.st.HTTP_404_NOT_FOUND
                    raise operation.ex(
                        f"No Zone found under {choice.full_path()} called: {start_check}"
                    )
                choice = new_choice
            else:
                zone = choice

        elif isinstance(input, int):
            zone = self.filter(id=input).first()
            if zone is None:
                operation.status = operation.st.HTTP_404_NOT_FOUND
                raise operation.ex("No Zone found with that ID.")
        else:
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex("You must provide a Zone ID or Path/Name.")

        if zone is None:
            operation.status = operation.st.HTTP_404_NOT_FOUND
            raise operation.ex("No Zone found.")

        return zone

    def op_find_zone(self, operation: Operation):
        zone = self.find_zone(operation)
        operation.results = {"success": True, "zone": zone}

    def _validate_name(self, operation: Operation, key="name"):
        if not (
            name := validate_name(operation.kwargs.get(key, None), thing_type="Zone")
        ):
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex("You must provide a name for the Zone.")
        return name

    def op_create(self, operation: Operation):
        if not self.check_override(operation.actor):
            operation.status = operation.st.HTTP_403_FORBIDDEN
            raise operation.ex("You do not have permission to create a Zone.")

        name = self._validate_name(operation)
        parent = None

        if "parent" in operation.kwargs:
            parent = self.find_zone(operation, key="parent")

        if exists := self.filter(db_key__iexact=name, db_parent=parent).first():
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex(f"A Zone already exists with that name: {exists}")

        zone = self.create(db_key=name, db_parent=parent)

        message = f"A new Zone was created: {zone.full_path()}."
        operation.results = {"success": True, "zone": zone, "message": message}
        staff_alert(message, operation.actor)

    def op_rename(self, operation: Operation):
        if not self.check_override(operation.actor):
            operation.status = operation.st.HTTP_403_FORBIDDEN
            raise operation.ex("You do not have permission to rename Zones.")

        zone = self.find_zone(operation)

        name = self._validate_name(operation)

        if (
            conflict := self.filter(db_parent=zone.parent, db_key__iexact=name)
            .exclude(id=zone)
            .first()
        ):
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex(f"A Zone already exists with that name: {conflict}")

        message = f"{zone.full_path()} was renamed to: {name}."
        zone.key = name
        operation.results = {"success": True, "zone": zone, "message": message}
        staff_alert(message, operation.actor)

    def op_parent(self, operation: Operation):
        if not self.check_override(operation.actor):
            operation.status = operation.st.HTTP_403_FORBIDDEN
            raise operation.ex("You do not have permission to restructure Zones.")

        zone = self.find_zone(operation)

        parent = operation.kwargs.get("parent", None)
        if parent == "/":
            parent = None
        else:
            parent = self.find_zone(operation, key="parent")

        if parent == zone:
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex("A Zone cannot be its own parent.")

        if parent and zone in parent.ancestors():
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex("A Zone cannot be its own ancestor.")

        if zone.contains_sub_zone(parent):
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex("A Zone cannot be its own descendant.")

        old_path = zone.full_path()
        old_parent = zone.parent
        zone.parent = parent
        new_path = zone.full_path()
        message = f"{old_path} was moved to {new_path}."
        operation.results = {"success": True, "zone": zone, "message": message}
        staff_alert(message, operation.actor)

    def op_config_set(self, operation: Operation):
        zone = self.find_zone(operation)

        if not zone.is_leader(operation.character):
            operation.status = operation.st.HTTP_403_FORBIDDEN
            raise operation.ex("You do not have permission to configure this Zone.")

        try:
            result = zone.options.set(
                operation.kwargs.get("key", None), operation.kwargs.get("value", None)
            )
        except ValueError as err:
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex(str(err))

        message = f"Zone '{zone.full_path()}' config '{result.key}' set to '{result.display()}'."
        operation.results = {
            "success": True,
            "zone": zone,
            "message": message,
        }

    def op_config_list(self, operation: Operation):
        zone = self.find_zone(operation)

        if not zone.is_leader(operation.character):
            operation.status = operation.st.HTTP_403_FORBIDDEN
            raise operation.ex("You do not have permission to configure this Faction.")

        config = zone.options.all(return_objs=True)

        out = list()
        for op in config:
            out.append(
                {
                    "name": op.key,
                    "description": op.description,
                    "type": op.__class__.__name__,
                    "value": str(op.display()),
                }
            )

        operation.results = {
            "success": True,
            "zone": zone,
            "config": out,
        }

    def op_list(self, operation: Operation):
        zone = None
        if "zone" in operation.kwargs:
            zone = self.find_zone(operation, key="zone")

        root_zones = self.filter(db_parent=zone)
        zones = [f.serialize(include_children=True) for f in root_zones]
        operation.results = {"success": True, "zones": zones}


class ZoneManager(ZoneDBManager, TypeclassManager):
    pass
