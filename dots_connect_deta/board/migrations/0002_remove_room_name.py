# Generated by Django 3.2.7 on 2021-10-03 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("board", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="room",
            name="name",
        ),
    ]