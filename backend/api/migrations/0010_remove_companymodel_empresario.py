# Generated by Django 4.2.5 on 2023-09-15 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_companymodel_nome_socios'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companymodel',
            name='empresario',
        ),
    ]