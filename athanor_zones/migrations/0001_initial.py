# Generated by Django 4.1.11 on 2023-11-08 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [("typeclasses", "0016_alter_attribute_id_alter_tag_id")]

    operations = [
        migrations.CreateModel(
            name="ZoneDB",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "db_key",
                    models.CharField(db_index=True, max_length=255, verbose_name="key"),
                ),
                (
                    "db_typeclass_path",
                    models.CharField(
                        db_index=True,
                        help_text="this defines what 'type' of entity this is. This variable holds a Python path to a module with a valid Evennia Typeclass.",
                        max_length=255,
                        null=True,
                        verbose_name="typeclass",
                    ),
                ),
                (
                    "db_date_created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="creation date"
                    ),
                ),
                (
                    "db_lock_storage",
                    models.TextField(
                        blank=True,
                        help_text="locks limit access to an entity. A lock is defined as a 'lock string' on the form 'type:lockfunctions', defining what functionality is locked and how to determine access. Not defining a lock means no access is granted.",
                        verbose_name="locks",
                    ),
                ),
                ("db_config", models.JSONField(default=dict)),
                ("db_deleted", models.BooleanField(default=False)),
                (
                    "db_attributes",
                    models.ManyToManyField(
                        help_text="attributes on this object. An attribute can hold any pickle-able python object (see docs for special cases).",
                        to="typeclasses.attribute",
                    ),
                ),
                (
                    "db_parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="children",
                        to="athanor_zones.zonedb",
                    ),
                ),
                (
                    "db_tags",
                    models.ManyToManyField(
                        help_text="tags on this object. Tags are simple string markers to identify, group and alias objects.",
                        to="typeclasses.tag",
                    ),
                ),
            ],
            options={
                "verbose_name": "Evennia Database Object",
                "ordering": ["-db_date_created", "id", "db_typeclass_path", "db_key"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ZoneObject",
            fields=[
                (
                    "id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="zone",
                        serialize=False,
                        to="objects.objectdb",
                    ),
                ),
                (
                    "zone",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="objects",
                        to="athanor_zones.zonedb",
                    ),
                ),
            ],
        ),
    ]