# Generated by Django 4.2.10 on 2024-05-20 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("fund", "0005_emailtemplate"),
    ]

    operations = [
        migrations.RenameField(
            model_name="collect",
            old_name="planned_amount",
            new_name="amount",
        ),
    ]