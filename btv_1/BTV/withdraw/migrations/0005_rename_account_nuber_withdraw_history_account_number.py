# Generated by Django 5.0.3 on 2024-04-15 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('withdraw', '0004_withdraw_history_account_nuber_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='withdraw_history',
            old_name='account_nuber',
            new_name='account_number',
        ),
    ]