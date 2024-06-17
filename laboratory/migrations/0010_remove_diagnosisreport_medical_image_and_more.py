# Generated by Django 5.0.6 on 2024-06-17 09:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0009_alter_diagnosisreport_doctor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diagnosisreport',
            name='medical_image',
        ),
        migrations.RemoveField(
            model_name='diagnosisreport',
            name='doctor',
        ),
        migrations.CreateModel(
            name='DiagnosisReportImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='report_images/')),
                ('diagnosis_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diagnosis_images', to='laboratory.diagnosisreport')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_images', to='laboratory.patient')),
            ],
        ),
        migrations.AddField(
            model_name='diagnosisreport',
            name='medical_data',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='diagnosis_report', to='laboratory.medicaldata'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='MedicalDataImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='medical_images/')),
                ('medical_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_image', to='laboratory.medicaldata')),
            ],
        ),
        migrations.DeleteModel(
            name='MedicalImage',
        ),
    ]