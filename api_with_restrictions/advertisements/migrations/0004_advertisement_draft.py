# Generated by Django 4.2.6 on 2023-10-20 17:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("advertisements", "0003_favorite_delete_favoriteadvertisement"),
    ]

    operations = [
        migrations.AddField(
            model_name="advertisement",
            name="draft",
            field=models.BooleanField(default=True),
        ),
    ]