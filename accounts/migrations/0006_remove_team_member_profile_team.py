# Generated by Django 5.0.2 on 2024-03-12 17:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_otpcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='member',
        ),
        migrations.AddField(
            model_name='profile',
            name='team',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.team'),
        ),
    ]
