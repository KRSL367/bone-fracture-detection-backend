# Generated by Django 5.0.6 on 2024-06-16 12:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_user_hospital_id'),
        ('laboratory', '0008_remove_hospital_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='hospital_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='laboratory.hospital'),
        ),
    ]