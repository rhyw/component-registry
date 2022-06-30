# Generated by Django 3.2.13 on 2022-05-13 10:06

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_auto_20220512_0306"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductComponentRelation",
            fields=[
                ("last_changed", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("type", models.CharField(choices=[("ERRATA", "Errata")], max_length=50)),
                ("meta_attr", models.JSONField(default=dict)),
                ("external_system_id", models.CharField(default="", max_length=200)),
                ("variant_id", models.CharField(default="", max_length=200)),
                ("build_id", models.CharField(default="", max_length=200)),
            ],
            options={
                "ordering": ("external_system_id",),
            },
        ),
        migrations.AddConstraint(
            model_name="productcomponentrelation",
            constraint=models.UniqueConstraint(
                fields=("external_system_id", "variant_id", "build_id"),
                name="unique_productcomponentrelation",
            ),
        ),
    ]
