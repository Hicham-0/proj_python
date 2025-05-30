# Generated by Django 5.0.1 on 2025-05-23 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0010_remove_dossiermedical_antecedents'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('lu', models.BooleanField(default=False)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('medecin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='cabinet.medecin')),
            ],
        ),
    ]
