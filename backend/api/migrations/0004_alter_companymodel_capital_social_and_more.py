# Generated by Django 4.2.5 on 2023-09-15 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_companymodel_razao_social'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companymodel',
            name='capital_social',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='invoicingmodel',
            name='value',
            field=models.FloatField(),
        ),
    ]
