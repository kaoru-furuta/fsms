# Generated by Django 2.2.12 on 2020-05-13 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fruits", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="fruit",
            name="image",
            field=models.FileField(default=None, null=True, upload_to=""),
        ),
    ]
