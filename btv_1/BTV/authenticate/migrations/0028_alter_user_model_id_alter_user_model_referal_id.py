# Generated by Django 5.0.3 on 2024-04-12 10:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0027_alter_user_model_id_alter_user_model_referal_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_model',
            name='id',
            field=models.UUIDField(default=uuid.UUID('574b08d9-468c-4b1a-a175-d24f623494c9'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='user_model',
            name='referal_id',
            field=models.UUIDField(default=uuid.UUID('69cc1401-fc46-46fc-88e0-9e5c72f14e13'), editable=False, unique=True),
        ),
    ]