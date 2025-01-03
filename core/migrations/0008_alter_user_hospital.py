# Generated by Django 5.0.6 on 2024-06-18 11:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_user_hospital'),
        ('laboratory', '0014_remove_hospital_admins_alter_hospital_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='hospital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admins', to='laboratory.hospital'),
        ),
    ]
