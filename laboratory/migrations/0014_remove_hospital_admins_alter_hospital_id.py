# Generated by Django 5.0.6 on 2024-06-18 10:27

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0013_hospital_admins'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospital',
            name='admins',
        ),
        migrations.AlterField(
            model_name='hospital',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
