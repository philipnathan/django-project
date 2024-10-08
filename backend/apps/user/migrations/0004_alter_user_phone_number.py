# Generated by Django 5.1.1 on 2024-10-06 13:21

import apps.user.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=14, unique=True, validators=[apps.user.validators.validate_phone_number], verbose_name='phone number'),
        ),
    ]
