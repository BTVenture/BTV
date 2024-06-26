# Generated by Django 5.0.3 on 2024-04-12 10:09

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0032_alter_user_model_id_alter_user_model_referal_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_model',
            name='id',
            field=models.UUIDField(default=uuid.UUID('f85fc932-0c18-4338-863d-4fff61cbfe8a'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='user_model',
            name='referal_id',
            field=models.UUIDField(default=uuid.UUID('47f8b0fe-1aa8-4d82-afa5-858c4c533490'), editable=False, unique=True),
        ),
    ]
