# Generated by Django 5.0.6 on 2024-06-16 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0004_patient_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='email',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='last_name',
        ),
    ]
