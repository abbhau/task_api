# Generated by Django 4.2.6 on 2024-01-02 05:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0006_alter_task_task_completed_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to='user/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]),
        ),
    ]
