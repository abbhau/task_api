# Generated by Django 5.0 on 2023-12-31 10:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pincode',
            field=models.IntegerField(validators=[django.core.validators.MaxLengthValidator(6)]),
        ),
    ]
