# Generated by Django 3.2.15 on 2022-12-21 04:27
import uuid

import django
from django.db import migrations, models


class Migration(migrations.Migration):
    operations = [
        migrations.AddConstraint(
            model_name="softwarebuild",
            constraint=models.UniqueConstraint(
                fields=("build_id", "build_type"), name="unique_build_id_by_type"
            ),
        ),
        migrations.RunSQL(
            sql=[
                # allow uuid_generate_v4
                'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'
                # add new uuid columns to softwarebuild and generate values
                "ALTER TABLE core_softwarebuild ADD COLUMN uuid uuid DEFAULT uuid_generate_v4 ()",
                # add new uuid columns to softwarebuildtag and populate with new values
                "ALTER TABLE core_softwarebuildtag ADD COLUMN tagged_model_uuid UUID",
                "UPDATE core_softwarebuildtag "
                "SET tagged_model_uuid=subquery.uuid "
                "FROM (SELECT uuid, build_id"
                "      FROM core_softwarebuild) AS subquery "
                "WHERE core_softwarebuildtag.tagged_model_id = subquery.build_id",
                # add new uuid columns to component and populate with new values
                "ALTER TABLE core_component ADD COLUMN software_build_uuid UUID",
                "UPDATE core_component "
                "SET software_build_uuid=subquery.uuid "
                "FROM (select uuid, build_id"
                "      FROM core_softwarebuild) AS subquery "
                "WHERE core_component.software_build_id = subquery.build_id",
                # drop the existing primary key on softwarebuild
                "ALTER TABLE core_softwarebuild DROP CONSTRAINT core_softwarebuild_pkey CASCADE",
                # make the new uuid column the primary key
                "ALTER TABLE core_softwarebuild ADD CONSTRAINT core_softwarebuild_pkey "
                "PRIMARY KEY (uuid)",
                # recreate the foreign key on softwarebuildtag
                "ALTER TABLE core_softwarebuildtag DROP COLUMN tagged_model_id",
                "ALTER TABLE core_softwarebuildtag ADD FOREIGN KEY (tagged_model_uuid) "
                "REFERENCES core_softwarebuild (uuid) ON DELETE CASCADE",
                # recreate the foreign key on component
                "ALTER TABLE core_component DROP COLUMN software_build_id",
                "ALTER TABLE core_component ADD FOREIGN KEY (software_build_uuid) "
                "REFERENCES core_softwarebuild(uuid) ON DELETE CASCADE",
            ],
            reverse_sql=[
                # add id columns to softwarebuildtag and populate with values
                "ALTER TABLE core_softwarebuildtag ADD COLUMN tagged_model_id INTEGER",
                "UPDATE core_softwarebuildtag "
                "SET tagged_model_id=subquery.build_id "
                "FROM (SELECT uuid, build_id"
                "      FROM core_softwarebuild) AS subquery "
                "WHERE core_softwarebuildtag.tagged_model_uuid = subquery.uuid",
                # drop foreign key constraint on softwarebuildtag
                "ALTER TABLE core_softwarebuildtag DROP CONSTRAINT "
                "core_softwarebuildtag_tagged_model_uuid_fkey",
                # Remove the old foreign key column as well
                "ALTER TABLE core_softwarebuildtag DROP COLUMN tagged_model_uuid",
                # add software_build_id column to component and populate withe values
                "ALTER TABLE core_component ADD COLUMN software_build_id INTEGER",
                "UPDATE core_component "
                "SET software_build_id=subquery.build_id "
                "FROM (select uuid, build_id"
                "      FROM core_softwarebuild) AS subquery "
                "WHERE core_component.software_build_uuid = subquery.uuid",
                # drop foreign key constraint on component
                "ALTER TABLE core_component DROP CONSTRAINT "
                "core_component_software_build_uuid_fkey",
                # remove the uuid field as well
                "ALTER TABLE core_component DROP COLUMN software_build_uuid",
                "ALTER TABLE core_softwarebuild DROP CONSTRAINT core_softwarebuild_pkey CASCADE",
                "ALTER TABLE core_softwarebuild DROP COLUMN uuid",
                "ALTER TABLE core_softwarebuild ADD PRIMARY KEY (build_id)",
                "ALTER TABLE core_softwarebuildtag ADD FOREIGN KEY (tagged_model_id) "
                "REFERENCES core_softwarebuild (build_id) ON DELETE CASCADE",
                "ALTER TABLE core_component ADD FOREIGN KEY (software_build_id) "
                "REFERENCES core_softwarebuild (build_id) ON DELETE CASCADE",
            ],
            state_operations=[
                migrations.RemoveIndex(model_name="softwarebuild", name="core_softwarebuild_pkey"),
                migrations.AlterField(
                    model_name="softwarebuild", name="build_id", field=models.IntegerField()
                ),
                migrations.AddField(
                    model_name="softwarebuild",
                    name="uuid",
                    field=models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                migrations.AlterField(
                    model_name="softwarebuildtag",
                    name="tagged_model",
                    field=models.ForeignKey(
                        related_name="tags",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.softwarebuild",
                        db_column="tagged_model_uuid",
                    ),
                ),
                migrations.AlterField(
                    model_name="component",
                    name="software_build",
                    field=models.ForeignKey(
                        related_name="components",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.softwarebuild",
                        db_column="software_build_uuid",
                    ),
                ),
            ],
        ),
    ]

    dependencies = [
        ("core", "0060_enforce_unique_purls"),
    ]
