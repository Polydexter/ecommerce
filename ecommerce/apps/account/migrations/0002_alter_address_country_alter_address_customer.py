# Generated by Django 4.1.2 on 2022-11-22 13:54

import django.db.models.deletion
import django_countries.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="country",
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name="address",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_adresses",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Customer",
            ),
        ),
    ]
