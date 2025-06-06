# Generated by Django 5.0.6 on 2025-04-17 17:38

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiseaseDiagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis_date', models.DateField(db_column='diagnosis_date')),
                ('disease_name', models.CharField(max_length=255)),
                ('diagnostic_details', models.TextField()),
                ('image', models.BinaryField(blank=True, null=True)),
            ],
            options={
                'db_table': 'disease_diagnosis',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExternalAppUser',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(db_column='first_name', max_length=255)),
                ('last_name', models.CharField(db_column='last_name', max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'app_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'medical_record',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=64)),
                ('app_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='block.externalappuser')),
            ],
        ),
        migrations.CreateModel(
            name='DiagnosisBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('block_hash', models.CharField(max_length=64)),
                ('previous_hash', models.CharField(blank=True, max_length=64, null=True)),
                ('diagnosis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='block.diseasediagnosis')),
            ],
            options={
                'db_table': 'diagnosis_block',
                'managed': True,
            },
        ),
    ]
