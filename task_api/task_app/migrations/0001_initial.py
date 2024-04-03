# Generated by Django 5.0 on 2023-12-31 02:37

import django.core.validators
import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=20)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female'), ('transgender', 'transgender')], max_length=50)),
                ('profile', models.ImageField(upload_to='user/')),
                ('address', models.TextField()),
                ('pincode', models.IntegerField(validators=[django.core.validators.MaxValueValidator(6)])),
                ('city', models.CharField(max_length=20)),
                ('contact_no', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('role', models.CharField(choices=[('manager', 'manager'), ('team_leader', 'team_leader'), ('developer', 'developer')], max_length=20)),
                ('company', models.TextField()),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.IntegerField(primary_key=True, serialize=False)),
                ('task_name', models.CharField(max_length=200)),
                ('task_description', models.TextField()),
                ('task_status', models.CharField(choices=[('pending', 'pending'), ('completed', 'completed'), ('in_progress', 'in_progress')], max_length=30)),
                ('task_assigned_date', models.DateTimeField()),
                ('task_completed_date', models.DateTimeField(blank=True)),
                ('task_deadline', models.DateTimeField()),
                ('task_assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager_or_team_leader', to=settings.AUTH_USER_MODEL)),
                ('task_assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='developer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserActivateToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('act_link', models.CharField(max_length=32)),
                ('created_at', models.DateTimeField()),
                ('expired_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]