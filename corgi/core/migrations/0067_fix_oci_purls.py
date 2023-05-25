# Generated by Django 3.2.18 on 2023-04-27 05:18

from django.db import migrations


def fix_oci_purls(apps, schema_editor):
    """Remove namespace from OCI purls by saving all
    container images and their cnodes."""
    Component = apps.get_model("core", "Component")
    for container in Component.objects.filter(type="OCI").iterator():
        container.save()
        for node in container.cnodes.iterator():
            node.save()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0066_adjust_softwarebuild_indexes"),
    ]

    operations = [
        migrations.RunPython(fix_oci_purls),
    ]
