# Generated by Django 4.2.5 on 2023-09-15 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_companymodel_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companymodel',
            old_name='cpnj',
            new_name='cnpj',
        ),
    ]