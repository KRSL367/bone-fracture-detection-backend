# Generated by Django 5.0.6 on 2024-06-16 12:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('laboratory', '0008_remove_hospital_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hospital_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='laboratory.hospital'),
        ),
    ]
