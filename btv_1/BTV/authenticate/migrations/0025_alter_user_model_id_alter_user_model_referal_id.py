# Generated by Django 5.0.3 on 2024-04-12 09:59

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0024_alter_user_model_id_alter_user_model_referal_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_model',
            name='id',
            field=models.UUIDField(default=uuid.UUID('b0f9418f-1a55-42b3-b739-2dbc3048aa63'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='user_model',
            name='referal_id',
            field=models.UUIDField(default=uuid.UUID('beb7882d-7daf-4325-9446-9eca5736ced4'), editable=False, unique=True),
        ),
    ]
