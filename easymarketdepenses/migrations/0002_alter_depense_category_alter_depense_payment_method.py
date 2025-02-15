# Generated by Django 5.1.5 on 2025-02-13 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easymarketdepenses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depense',
            name='category',
            field=models.CharField(choices=[('SALAIRE', 'SALAIRE'), ('EAU', 'EAU'), ('ELECTRICITE', 'ELECTRICITE'), ('LOYER', 'LOYER'), ('TRANSPORT', 'TRANSPORT'), ('APPROVISIONNEMENT', 'APPROVISIONNEMENT'), ('AUTRE', 'AUTRE')], max_length=50),
        ),
        migrations.AlterField(
            model_name='depense',
            name='payment_method',
            field=models.CharField(choices=[('WAVE', 'WAVE'), ('ORANGE_MONEY', 'ORANGE MONEY'), ('FREE_MONEY', 'FREE MONEY'), ('CASH', 'CASH')], max_length=20),
        ),
    ]
