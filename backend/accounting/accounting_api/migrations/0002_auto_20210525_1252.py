# Generated by Django 3.2.3 on 2021-05-25 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='profession_id',
            new_name='profession',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='user_id',
            new_name='user',
        ),
    ]
