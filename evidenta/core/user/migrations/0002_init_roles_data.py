from django.db import migrations

from evidenta.initial_data import create_roles_and_permissions


def _create_roles_and_permissions(*_):
    create_roles_and_permissions()


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
        # ("auth", "0012_auto_20210601_1212"),  # Závislost na migraci 'auth'
    ]

    operations = [
        migrations.RunPython(_create_roles_and_permissions),
    ]
