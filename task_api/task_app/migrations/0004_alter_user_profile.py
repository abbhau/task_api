# Generated by Django 5.0 on 2023-12-31 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0003_alter_user_pincode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to='user/'),
        ),
    ]
