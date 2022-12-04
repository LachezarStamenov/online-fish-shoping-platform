# Generated by Django 4.1.2 on 2022-11-20 12:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=40, unique=True, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
    ]