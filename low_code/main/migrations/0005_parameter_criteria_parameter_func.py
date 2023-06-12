# Generated by Django 4.2.2 on 2023-06-12 13:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_col_idx_parameter_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameter',
            name='criteria',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parameter',
            name='func',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
