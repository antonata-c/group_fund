# Generated by Django 4.2.10 on 2024-05-16 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("fund", "0003_rename_author_collect_user_alter_collect_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="collect",
            name="current_amount",
        ),
    ]
