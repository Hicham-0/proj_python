# Generated by Django 5.0.1 on 2025-05-01 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facture',
            name='statut_paiement',
            field=models.CharField(choices=[('EN_ATTENTE', 'En attente'), ('PAYEE', 'Payée')], default='EN_ATTENTE', max_length=20),
        ),
    ]
