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


class ZoneManager(ZoneDBManager, TypeclassManager):
    pass
