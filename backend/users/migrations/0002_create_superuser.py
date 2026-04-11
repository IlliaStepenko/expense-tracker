import os

from django.contrib.auth import get_user_model
from django.db import migrations


def create_superuser(apps, schema_editor):
    User = get_user_model()

    admin_username = os.getenv('ADMIN_USERNAME')
    admin_password = os.getenv('ADMIN_PASSWORD')
    admin_email = os.getenv('ADMIN_EMAIL')

    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password,
            first_name="admin",
            last_name="admin",
        )


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
