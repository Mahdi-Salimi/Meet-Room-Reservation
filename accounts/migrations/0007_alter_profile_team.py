# Generated by Django 5.0.2 on 2024-03-12 17:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_team_member_profile_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='team',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.team'),
        ),
    ]
