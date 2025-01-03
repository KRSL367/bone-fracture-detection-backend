# Generated by Django 5.0.6 on 2024-06-17 09:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_user_hospital_id_user_hospital_user_role'),
        ('laboratory', '0010_remove_diagnosisreport_medical_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.AddField(
            model_name='user',
            name='is_hospital_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='hospital',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='laboratory.hospital'),
        ),
    ]
