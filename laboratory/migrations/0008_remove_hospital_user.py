# Generated by Django 5.0.6 on 2024-06-16 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0007_hospital_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospital',
            name='user',
        ),
    ]