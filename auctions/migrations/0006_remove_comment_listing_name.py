# Generated by Django 4.2.5 on 2023-10-06 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0005_comment_listing_name"),
    ]

    operations = [
        migrations.RemoveField(model_name="comment", name="listing_name",),
    ]
